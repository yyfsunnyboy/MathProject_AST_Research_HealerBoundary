# -*- coding: utf-8 -*-
"""9B C1→C2 Tier B cumulative replay (frozen four-rule pipeline).

Input: 9B C1 final sources (320). Does not modify rules/thresholds/order,
4B artifacts, Tier E census, or call a model.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import shutil
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.aggressive_healer_tier_a import (  # noqa: E402
    RULE_ORDER,
    run_tier_a_pipeline,
)
from agent_tools.finals_rebuild.math16_pool import frozen_for_prompt, tasks_by_id  # noqa: E402
from scripts.evaluate_math16_pilot02_full_v4 import (  # noqa: E402
    _load_family_and_api_policy,
    classify_outcome_to_v3,
)
from scripts.preflight_math16_method2_all_cell import classify_transition  # noqa: E402
from scripts.run_math16_latex_v1_gemini_live import classify_math16_response  # noqa: E402

C1_CLOSURE = ROOT / "docs/experiments/manifests/math16_c1_final_source_closure_qwen9b_v1.json"
RESULTS = ROOT / "docs/experiments/results/math16_c1_c2_tier_b_reproducibility_qwen9b_v1"
OUT_REPLAY_MANIFEST = (
    ROOT / "docs/experiments/manifests/math16_c1_c2_tier_b_reproducibility_qwen9b_v1.json"
)
OUT_REPLAY_REPORT = (
    ROOT / "docs/experiments/reports/math16_c1_c2_tier_b_reproducibility_qwen9b_v1.md"
)
OUT_C2_CLOSURE = (
    ROOT / "docs/experiments/manifests/math16_c2_final_source_closure_qwen9b_v1.json"
)
OUT_C2_REPORT = ROOT / "docs/experiments/reports/math16_c2_final_source_closure_qwen9b_v1.md"

TIER_B_FILES = [
    "agent_tools/finals_rebuild/aggressive_healer_tier_a/pipeline.py",
    "agent_tools/finals_rebuild/aggressive_healer_tier_a/rule_a1_fullwidth.py",
    "agent_tools/finals_rebuild/aggressive_healer_tier_a/rule_a2_delimiter.py",
    "agent_tools/finals_rebuild/aggressive_healer_tier_a/rule_a3_empty_suite.py",
    "agent_tools/finals_rebuild/aggressive_healer_tier_a/rule_a4_import_binding.py",
    "agent_tools/finals_rebuild/aggressive_healer_tier_a/common.py",
    "agent_tools/finals_rebuild/aggressive_healer_tier_a/types.py",
]

EXPECTED_ORDER = (
    "core.normalize_fullwidth_python_punctuation",
    "TIER_A_UNIQUE_MISSING_DELIMITER_REPAIR_V1",
    "TIER_A_EMPTY_SUITE_INSERT_PASS_V1",
    "TIER_A_UNIQUE_IMPORT_BINDING_REPAIR_V1",
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def head_sha() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], text=True, cwd=str(ROOT)
    ).strip()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def parses(source: str) -> bool:
    if not source.strip():
        return False
    try:
        ast.parse(source)
        return True
    except SyntaxError:
        return False


def is_executable_obs(score: dict[str, Any]) -> bool:
    """Observation-only executable flag (not used for selection)."""
    if score["status"] == "PASSED":
        return True
    blob = " ".join(
        [
            str(score.get("failure_subtype") or ""),
            str(score.get("classifier_outcome") or ""),
            str(score.get("primary_failure_layer") or ""),
        ]
    ).lower()
    blockers = (
        "parse",
        "syntax",
        "runtime",
        "missing_entry",
        "extraction",
        "unparseable",
    )
    return not any(b in blob for b in blockers)


def score_source(
    source: str,
    *,
    task: dict[str, Any],
    frozen_params: dict[str, Any],
    api_policy: str,
) -> dict[str, Any]:
    outcome, _source, details = classify_math16_response(
        source,
        frozen_params=frozen_params,
        audit_oracle_payload=task["oracle_payload"],
        task=task,
    )
    mapped = classify_outcome_to_v3(outcome, details, api_policy=api_policy)
    status = mapped["final_status"]
    if status not in {"PASSED", "FAILED"}:
        raise RuntimeError(f"UNEXPECTED_STATUS: {status}")
    return {
        "status": status,
        "classifier_outcome": outcome,
        "primary_failure_layer": mapped["primary_failure_layer"],
        "failure_subtype": mapped["failure_subtype"],
    }


def verify_c1_input(c1: dict[str, Any]) -> None:
    v = c1["validation"]
    if not v.get("passed"):
        raise RuntimeError("C1_CLOSURE_NOT_PASSED")
    if v.get("n_cells") != 320 or v.get("c1_pass") != 101 or v.get("c1_fail") != 219:
        raise RuntimeError(f"C1_COUNTS_DRIFT: {v}")
    ids = [c["cell_id"] for c in c1["cells"]]
    if len(ids) != 320 or len(set(ids)) != 320:
        raise RuntimeError("C1_IDENTITY_FAILURE")
    for cell in c1["cells"]:
        path = ROOT / cell["c1_final_source_path"]
        if not path.exists():
            raise RuntimeError(f"MISSING_C1_SOURCE: {cell['cell_id']}")
        if sha256_path(path) != cell["c1_final_source_sha256"]:
            raise RuntimeError(f"C1_SHA_DRIFT: {cell['cell_id']}")


def rule_freeze_audit() -> dict[str, Any]:
    if tuple(RULE_ORDER) != EXPECTED_ORDER:
        raise RuntimeError(f"RULE_ORDER_DRIFT: {RULE_ORDER}")
    files = {}
    for rel in TIER_B_FILES:
        path = ROOT / rel
        files[rel] = {
            "sha256": sha256_path(path),
            "lf_sha256": sha256_bytes(path.read_bytes().replace(b"\r\n", b"\n")),
        }
    return {
        "current_tier": "Tier B",
        "layer_role": "safe_structural_extension",
        "rule_order": list(RULE_ORDER),
        "rule_order_matches_frozen": True,
        "files": files,
        "note": "Historical package path aggressive_healer_tier_a = Tier B per cumulative protocol",
    }


def run_replay(c1: dict[str, Any], results_root: Path) -> dict[str, Any]:
    if results_root.exists():
        shutil.rmtree(results_root)
    pre_dir = results_root / "pre_sources"
    post_dir = results_root / "post_sources"
    pre_dir.mkdir(parents=True)
    post_dir.mkdir(parents=True)

    tasks = tasks_by_id()
    _, api_policy_map = _load_family_and_api_policy()
    rows: list[dict[str, Any]] = []
    rule_stats = {
        rid: {"triggered": 0, "modified": 0, "abstained": 0, "rescue": 0}
        for rid in RULE_ORDER
    }

    for index, cell in enumerate(c1["cells"], start=1):
        cid = cell["cell_id"]
        pre_path = ROOT / cell["c1_final_source_path"]
        pre_source = pre_path.read_text(encoding="utf-8")
        if sha256_path(pre_path) != cell["c1_final_source_sha256"]:
            raise RuntimeError(f"PRE_SHA_DRIFT: {cid}")

        pipe = run_tier_a_pipeline(pre_source)
        post_source = pipe.post_source
        (pre_dir / f"{cid}.py").write_bytes(pre_source.encode("utf-8"))
        (post_dir / f"{cid}.py").write_bytes(post_source.encode("utf-8"))

        task = tasks[cell["task_id"]]
        frozen_params = frozen_for_prompt(task)["oracle_payload"]
        api_policy = api_policy_map[cell["task_id"]]
        pre_score = score_source(
            pre_source, task=task, frozen_params=frozen_params, api_policy=api_policy
        )
        post_score = score_source(
            post_source, task=task, frozen_params=frozen_params, api_policy=api_policy
        )
        transition = classify_transition(pre_score["status"], post_score["status"])

        pre_parse = parses(pre_source)
        post_parse = parses(post_source)
        pre_exec = is_executable_obs(pre_score)
        post_exec = is_executable_obs(post_score)
        parse_gain = (not pre_parse) and post_parse
        execution_gain = (not pre_exec) and post_exec
        modified = pre_source != post_source
        # Blocker removal: structural gain without verified rescue
        blocker_removal = modified and transition != "verified_rescue" and (
            parse_gain or execution_gain
        )

        per_rule = []
        for log in pipe.rule_logs:
            rid = log["rule_id"]
            per_rule.append(
                {
                    "rule_id": rid,
                    "current_tier": "Tier B",
                    "triggered": bool(log.get("triggered")),
                    "modified": bool(log.get("applied")),
                    "abstained": bool(log.get("abstained")),
                    "abstention_reason": log.get("abstention_reason") or "",
                    "trigger_evidence": log.get("trigger_evidence") or "",
                    "pre_source_sha": log.get("pre_source_sha"),
                    "post_source_sha": log.get("post_source_sha"),
                }
            )
            if log.get("triggered"):
                rule_stats[rid]["triggered"] += 1
            if log.get("applied"):
                rule_stats[rid]["modified"] += 1
            if log.get("abstained"):
                rule_stats[rid]["abstained"] += 1

        if transition == "verified_rescue" and pipe.rules_fired:
            # attribute rescue to last fired rule (single forward pass)
            rule_stats[pipe.rules_fired[-1]]["rescue"] += 1

        rows.append(
            {
                "cell_id": cid,
                "model": "qwen3.5:9b",
                "model_group": "qwen9b",
                "task_id": cell["task_id"],
                "condition": cell["condition"],
                "seed": cell["seed"],
                "c1_outcome": cell["c1_outcome"],
                "c1_final_source_path": cell["c1_final_source_path"],
                "c1_final_source_sha256": cell["c1_final_source_sha256"],
                "pre_source_path": str((pre_dir / f"{cid}.py").relative_to(ROOT)).replace(
                    "\\", "/"
                ),
                "post_source_path": str(
                    (post_dir / f"{cid}.py").relative_to(ROOT)
                ).replace("\\", "/"),
                "pre_source_sha256": pipe.pre_source_sha,
                "post_source_sha256": pipe.post_source_sha,
                "used_c1_final_source": True,
                "rules_fired": list(pipe.rules_fired),
                "mutation_count": pipe.mutation_count,
                "pipeline_idempotent": pipe.pipeline_idempotent,
                "rolled_back": pipe.rolled_back,
                "outcome_taxonomy": pipe.outcome_taxonomy,
                "abstention_reason": pipe.abstention_reason,
                "modified": modified,
                "triggered_any": bool(pipe.rules_fired),
                "abstained_all": (not pipe.rules_fired) and all(
                    log.get("abstained") for log in pipe.rule_logs
                ),
                "per_rule": per_rule,
                "pre_status": pre_score["status"],
                "post_status": post_score["status"],
                "transition": transition,
                "pre_classifier_outcome": pre_score["classifier_outcome"],
                "post_classifier_outcome": post_score["classifier_outcome"],
                "pre_primary_failure_layer": pre_score["primary_failure_layer"],
                "post_primary_failure_layer": post_score["primary_failure_layer"],
                "pre_failure_subtype": pre_score["failure_subtype"],
                "post_failure_subtype": post_score["failure_subtype"],
                "pre_parseable": pre_parse,
                "post_parseable": post_parse,
                "pre_executable": pre_exec,
                "post_executable": post_exec,
                "parse_gain": parse_gain,
                "execution_gain": execution_gain,
                "blocker_removal_only": blocker_removal,
                "evaluator_used_for_selection": False,
                "model_calls": 0,
            }
        )
        if index % 40 == 0:
            print(f"[c1_c2 {index}/320]")

    write_jsonl(results_root / "transition_journal.jsonl", rows)

    transitions = Counter(r["transition"] for r in rows)
    c2_pass = sum(r["post_status"] == "PASSED" for r in rows)
    c1_pass_obs = sum(r["pre_status"] == "PASSED" for r in rows)
    summary = {
        "phase": "9B C1→C2 Tier B cumulative replay",
        "status": "COMPLETE",
        "cells": 320,
        "c1_pass_observed": c1_pass_obs,
        "c2_pass": c2_pass,
        "c2_fail": 320 - c2_pass,
        "net_pass_change": c2_pass - c1_pass_obs,
        "transitions": {
            "verified_rescue": transitions["verified_rescue"],
            "regression": transitions["regression"],
            "preserved_pass": transitions["preserved_pass"],
            "still_failed": transitions["still_failed"],
        },
        "modified_cells": sum(r["modified"] for r in rows),
        "modified_still_failed": sum(
            1 for r in rows if r["modified"] and r["transition"] == "still_failed"
        ),
        "triggered_any": sum(r["triggered_any"] for r in rows),
        "parse_gain": sum(r["parse_gain"] for r in rows),
        "execution_gain": sum(r["execution_gain"] for r in rows),
        "blocker_removal_only": sum(r["blocker_removal_only"] for r in rows),
        "rollback_count": sum(r["rolled_back"] for r in rows),
        "idempotence_failures": sum(not r["pipeline_idempotent"] for r in rows),
        "rule_accounting": rule_stats,
        "verified_rescue_ids": [
            r["cell_id"] for r in rows if r["transition"] == "verified_rescue"
        ],
        "regression_ids": [
            r["cell_id"] for r in rows if r["transition"] == "regression"
        ],
        "model_calls": 0,
        "evaluator_used_for_selection": False,
    }
    write_json(results_root / "summary.json", summary)
    return {"summary": summary, "rows": rows}


def deterministic_second(c1: dict[str, Any], first_rows: list[dict[str, Any]]) -> dict[str, Any]:
    scratch = ROOT / "docs/experiments/results/_scratch_qwen9b_c2_second_replay"
    if scratch.exists():
        shutil.rmtree(scratch)
    scratch.mkdir(parents=True)
    mismatches = []
    by_id = {r["cell_id"]: r for r in first_rows}
    for cell in c1["cells"]:
        cid = cell["cell_id"]
        pre = (ROOT / cell["c1_final_source_path"]).read_text(encoding="utf-8")
        pipe = run_tier_a_pipeline(pre)
        first = by_id[cid]
        if pipe.post_source_sha != first["post_source_sha256"]:
            mismatches.append(
                {
                    "cell_id": cid,
                    "field": "post_source_sha256",
                    "a": first["post_source_sha256"],
                    "b": pipe.post_source_sha,
                }
            )
        if list(pipe.rules_fired) != list(first["rules_fired"]):
            mismatches.append(
                {
                    "cell_id": cid,
                    "field": "rules_fired",
                    "a": first["rules_fired"],
                    "b": list(pipe.rules_fired),
                }
            )
    report = {
        "second_replay_mismatches": len(mismatches),
        "zero_diff": len(mismatches) == 0,
        "sample": mismatches[:20],
    }
    write_json(RESULTS / "deterministic_second_replay.json", report)
    shutil.rmtree(scratch)
    if mismatches:
        raise RuntimeError(f"SECOND_REPLAY_DIFF: {len(mismatches)}")
    return report


def build_c2_closure(
    c1: dict[str, Any], rows: list[dict[str, Any]], summary: dict[str, Any]
) -> dict[str, Any]:
    by_id = {r["cell_id"]: r for r in rows}
    cells = []
    for cell in c1["cells"]:
        r = by_id[cell["cell_id"]]
        origin = "TIER_B_POST_SOURCE" if r["modified"] else "C1_PRESERVED"
        cells.append(
            {
                "cell_id": cell["cell_id"],
                "model": "qwen3.5:9b",
                "model_group": "qwen9b",
                "task_id": cell["task_id"],
                "condition": cell["condition"],
                "seed": cell["seed"],
                "c1_outcome": cell["c1_outcome"],
                "c1_final_source_path": cell["c1_final_source_path"],
                "c1_final_source_sha256": cell["c1_final_source_sha256"],
                "c2_final_source_path": r["post_source_path"],
                "c2_final_source_sha256": r["post_source_sha256"],
                "c2_outcome": r["post_status"],
                "source_origin": origin,
                "rules_fired": r["rules_fired"],
                "modified": r["modified"],
                "transition": r["transition"],
                "parse_gain": r["parse_gain"],
                "execution_gain": r["execution_gain"],
                "blocker_removal_only": r["blocker_removal_only"],
            }
        )
    manifest = {
        "status": "math16_c2_final_source_closure_qwen9b_v1",
        "verdict": "C2_FINAL_SOURCE_CLOSURE_PASSED",
        "definition": "C2 = C1 + Tier B frozen four-rule safe structural extension",
        "head": head_sha(),
        "validation": {
            "n_cells": 320,
            "unique_ids": 320,
            "duplicate_ids": 0,
            "c1_pass": 101,
            "c2_pass": summary["c2_pass"],
            "c2_fail": summary["c2_fail"],
            "verified_rescue": summary["transitions"]["verified_rescue"],
            "regression": summary["transitions"]["regression"],
            "preserved_pass": summary["transitions"]["preserved_pass"],
            "still_failed": summary["transitions"]["still_failed"],
            "origin_counts": dict(Counter(c["source_origin"] for c in cells)),
            "no_missing_duplicate_fallback": True,
            "passed": True,
        },
        "cells": cells,
        "declarations": [
            "no_model_calls",
            "no_rule_threshold_order_changes",
            "no_4b_artifact_modification",
            "evaluator_blind_selection",
        ],
    }
    write_json(OUT_C2_CLOSURE, manifest)
    write_text(
        OUT_C2_REPORT,
        "\n".join(
            [
                "# Math16 C2 Final-Source Closure — Qwen9B v1",
                "",
                f"> **verdict:** `{manifest['verdict']}`",
                f"> **definition:** `{manifest['definition']}`",
                f"> **HEAD:** `{manifest['head']}`",
                "",
                "## Validation",
                "",
                f"- Cells: **320**; C2 PASS/FAIL: **{summary['c2_pass']}/{summary['c2_fail']}**",
                f"- verified_rescue / regression: **{summary['transitions']['verified_rescue']} / {summary['transitions']['regression']}**",
                f"- preserved_pass / still_failed: **{summary['transitions']['preserved_pass']} / {summary['transitions']['still_failed']}**",
                f"- source_origin: `{manifest['validation']['origin_counts']}`",
                "",
                "## Declarations",
                "",
                "- No fallback / missing / duplicate identities",
                "- Tier C／D not executed",
                "",
            ]
        )
        + "\n",
    )
    return manifest


def write_reports(
    freeze: dict[str, Any],
    summary: dict[str, Any],
    second: dict[str, Any],
) -> dict[str, Any]:
    manifest = {
        "status": "math16_c1_c2_tier_b_reproducibility_qwen9b_v1",
        "verdict": "C1_C2_TIER_B_QWEN9B_COMPLETE",
        "head": head_sha(),
        "results_root": str(RESULTS.relative_to(ROOT)).replace("\\", "/"),
        "input_c1_closure": str(C1_CLOSURE.relative_to(ROOT)).replace("\\", "/"),
        "rule_freeze_audit": freeze,
        "summary": summary,
        "deterministic_second_replay": second,
        "model_calls": 0,
    }
    write_json(OUT_REPLAY_MANIFEST, manifest)
    ra = summary["rule_accounting"]
    lines = [
        "# Math16 C1→C2 Tier B Reproducibility — Qwen9B v1",
        "",
        f"> **verdict:** `{manifest['verdict']}`",
        f"> **HEAD:** `{manifest['head']}`",
        f"> **results:** `{manifest['results_root']}`",
        f"> **input:** 9B C1 final source 320（PASS=101）",
        "",
        "## Core counts",
        "",
        "| Metric | Value |",
        "|---|---:|",
        "| C1 PASS (authority／observed) | 101／"
        + str(summary["c1_pass_observed"])
        + " |",
        f"| C2 PASS／FAIL | {summary['c2_pass']}／{summary['c2_fail']} |",
        f"| verified_rescue | {summary['transitions']['verified_rescue']} |",
        f"| regression | {summary['transitions']['regression']} |",
        f"| preserved_pass | {summary['transitions']['preserved_pass']} |",
        f"| still_failed | {summary['transitions']['still_failed']} |",
        f"| modified／modified still failed | {summary['modified_cells']}／{summary['modified_still_failed']} |",
        f"| parse_gain | {summary['parse_gain']} |",
        f"| execution_gain | {summary['execution_gain']} |",
        f"| blocker_removal_only（≠ verified rescue） | {summary['blocker_removal_only']} |",
        "",
        "## Tier B rule accounting",
        "",
        "| Rule | triggered | modified | abstained | rescue |",
        "|---|---:|---:|---:|---:|",
    ]
    for rid in RULE_ORDER:
        info = ra[rid]
        lines.append(
            f"| `{rid}` | {info['triggered']} | {info['modified']} | {info['abstained']} | {info['rescue']} |"
        )
    lines += [
        "",
        "## Determinism / freeze",
        "",
        f"- Second pipeline replay zero-diff: **{second['zero_diff']}**",
        f"- Rule order matches frozen: **{freeze['rule_order_matches_frozen']}**",
        f"- Order: `{list(RULE_ORDER)}`",
        "",
        "## Declarations",
        "",
        "- Model calls: **0**",
        "- Rules／thresholds／order modified: **No**",
        "- 4B artifacts modified: **No**",
        "- Tier C／D executed: **No**",
        "- Commit／push: **No**",
        "",
    ]
    write_text(OUT_REPLAY_REPORT, "\n".join(lines) + "\n")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-second-replay", action="store_true")
    args = parser.parse_args()

    print("== C1 input ==")
    c1 = json.loads(C1_CLOSURE.read_text(encoding="utf-8"))
    verify_c1_input(c1)
    freeze = rule_freeze_audit()
    print("RULE_ORDER", list(RULE_ORDER))

    print("== C1→C2 Tier B replay ==")
    replay = run_replay(c1, RESULTS)
    summary = replay["summary"]
    print(
        f"c2_pass={summary['c2_pass']} rescue={summary['transitions']['verified_rescue']} "
        f"regression={summary['transitions']['regression']} modified={summary['modified_cells']}"
    )

    if args.skip_second_replay:
        second = {"zero_diff": None, "skipped": True}
    else:
        print("== second deterministic replay ==")
        second = deterministic_second(c1, replay["rows"])

    print("== C2 closure ==")
    build_c2_closure(c1, replay["rows"], summary)
    write_reports(freeze, summary, second)
    print("DONE")
    print(json.dumps({
        "c2_pass": summary["c2_pass"],
        "rescue": summary["transitions"]["verified_rescue"],
        "regression": summary["transitions"]["regression"],
        "parse_gain": summary["parse_gain"],
        "execution_gain": summary["execution_gain"],
        "blocker_removal_only": summary["blocker_removal_only"],
        "second_zero_diff": second.get("zero_diff"),
        "rule_accounting": summary["rule_accounting"],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
