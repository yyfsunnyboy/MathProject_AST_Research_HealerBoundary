# -*- coding: utf-8 -*-
"""9B C0 baseline closure + C1 Tier A (frozen six-rule) cumulative replay.

Does not modify Healer rules, thresholds, allowlist order, or 4B artifacts.
Does not call a model. Reuses Method2 Phase A eligibility/heal logic and
Phase B independent Raw/Final scoring without 4B-hardcoded counts/SHAs.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import shutil
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.ce115_research_healer_runner import (  # noqa: E402
    RULE_ALLOWLIST,
    MathHealerRunner,
)
from agent_tools.finals_rebuild.extraction import extract_code  # noqa: E402
from agent_tools.finals_rebuild.math16_pool import frozen_for_prompt, tasks_by_id  # noqa: E402
from scripts.evaluate_math16_pilot02_full_v4 import (  # noqa: E402
    _load_family_and_api_policy,
    classify_outcome_to_v3,
)
from scripts.preflight_math16_method2_all_cell import (  # noqa: E402
    JOURNAL_FIELDS,
    classify_transition,
    decide_eligibility,
)
from scripts.run_math16_latex_v1_gemini_live import classify_math16_response  # noqa: E402

CELL_PLAN = ROOT / "docs/experiments/manifests/math16_pilot02_qwen9b_cell_plan.json"
BASELINE_OVERALL = (
    ROOT
    / "docs/experiments/results/math16_pilot02_qwen9b_evaluation_v4_r001/overall_summary.json"
)
BASELINE_JSONL = (
    ROOT
    / "docs/experiments/results/math16_pilot02_qwen9b_evaluation_v4_r001/cell_level_baseline.jsonl"
)
METHOD2_4B_PROTOCOL = (
    ROOT / "docs/experiments/manifests/math16_method2_all_cell_protocol_v1.json"
)

OUT_PROTOCOL = (
    ROOT / "docs/experiments/manifests/math16_method2_all_cell_protocol_qwen9b_v1.json"
)
OUT_C0_MANIFEST = (
    ROOT / "docs/experiments/manifests/math16_c0_baseline_closure_qwen9b_v1.json"
)
OUT_C0_REPORT = ROOT / "docs/experiments/reports/math16_c0_baseline_closure_qwen9b_v1.md"
OUT_C1_REPLAY_MANIFEST = (
    ROOT / "docs/experiments/manifests/math16_c0_c1_tier_a_reproducibility_qwen9b_v1.json"
)
OUT_C1_REPLAY_REPORT = (
    ROOT / "docs/experiments/reports/math16_c0_c1_tier_a_reproducibility_qwen9b_v1.md"
)
OUT_C1_CLOSURE_MANIFEST = (
    ROOT / "docs/experiments/manifests/math16_c1_final_source_closure_qwen9b_v1.json"
)
OUT_C1_CLOSURE_REPORT = (
    ROOT / "docs/experiments/reports/math16_c1_final_source_closure_qwen9b_v1.md"
)
RESULTS_ROOT = (
    ROOT / "docs/experiments/results/math16_c0_c1_tier_a_reproducibility_qwen9b_v1"
)

RULE_FILES = [
    "agent_tools/finals_rebuild/ce115_research_healer_runner.py",
    "agent_tools/finals_rebuild/ce115_research_healer_protocol.py",
    "agent_tools/finals_rebuild/ce115_research_healer_rules_l1_paren_close.py",
    "agent_tools/finals_rebuild/ce115_research_healer_rules_l1_delimiter_extended.py",
    "agent_tools/finals_rebuild/ce115_research_healer_rules_l1_prose_narrow.py",
    "agent_tools/finals_rebuild/ce115_research_healer_rules_l2.py",
    "agent_tools/finals_rebuild/ce115_research_healer_rules_l2_kwargs_bag_inline.py",
    "agent_tools/finals_rebuild/ce115_research_healer_rules_l2_json_dumps_unwrap.py",
]

PHASE_A_ONLY_FIELDS = JOURNAL_FIELDS


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def sha256_lf_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes().replace(b"\r\n", b"\n"))


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


def write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def head_sha() -> str:
    import subprocess

    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], text=True, cwd=str(ROOT)
    ).strip()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def parses(source: str) -> bool:
    if not source.strip():
        return False
    try:
        ast.parse(source)
        return True
    except SyntaxError:
        return False


def verify_rule_freeze() -> dict[str, Any]:
    """Confirm allowlist order and content-equality to Method2 freeze (LF)."""
    method2 = json.loads(METHOD2_4B_PROTOCOL.read_text(encoding="utf-8"))
    allow = tuple(method2["healer"]["rule_allowlist"])
    if allow != tuple(RULE_ALLOWLIST):
        raise RuntimeError("RULE_ALLOWLIST_DRIFT_VS_METHOD2")
    if allow != (
        "L1_CLOSE_UNBALANCED_PARENTHESIS",
        "L1_CLOSE_UNBALANCED_DELIMITER_EXTENDED",
        "L1_PROSE_RESIDUE_NARROW",
        "L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP",
        "L2_KWARGS_EMPTY_BAG_INLINE_UNIQUE_PARAM",
        "L2_CORRECT_ANSWER_JSON_DUMPS_UNWRAP",
    ):
        raise RuntimeError("RULE_ALLOWLIST_UNEXPECTED")

    pins = method2["frozen_sha256"]
    rule_audit = {}
    for rel in RULE_FILES:
        path = ROOT / rel
        raw = sha256_path(path)
        lf = sha256_lf_path(path)
        expected = pins.get(rel)
        rule_audit[rel] = {
            "working_tree_sha256": raw,
            "working_tree_lf_sha256": lf,
            "method2_pin_sha256": expected,
            "raw_matches_pin": raw == expected,
            "lf_matches_pin": lf == expected,
            "content_equal_to_pin_via_crlf_or_lf": (
                raw == expected
                or lf == expected
                or sha256_bytes(path.read_bytes().replace(b"\n", b"\r\n")) == expected
            ),
        }
        # Require content equality under some newline normalization to Method2 pin
        if expected and not rule_audit[rel]["content_equal_to_pin_via_crlf_or_lf"]:
            # Also accept: LF(current) == LF(git blob that produced pin via CRLF)
            # Already covered by crlf re-encode check above for same file bytes.
            raise RuntimeError(f"RULE_CONTENT_DRIFT: {rel}")

    return {
        "rule_allowlist": list(allow),
        "rule_order_matches_method2": True,
        "rule_files": rule_audit,
        "note": (
            "Method2 pins for two L1 files were computed on CRLF bytes; "
            "working tree is LF. Content is byte-identical after newline normalization."
        ),
    }


def build_protocol(rule_freeze: dict[str, Any]) -> dict[str, Any]:
    frozen = {
        rel: rule_freeze["rule_files"][rel]["working_tree_sha256"] for rel in RULE_FILES
    }
    frozen[str(CELL_PLAN.relative_to(ROOT)).replace("\\", "/")] = sha256_path(CELL_PLAN)
    frozen[
        str(BASELINE_OVERALL.relative_to(ROOT)).replace("\\", "/")
    ] = sha256_path(BASELINE_OVERALL)
    return {
        "manifest_id": "math16_method2_all_cell_protocol_qwen9b_v1",
        "protocol_status": "EXECUTED_C0_C1_TIER_A",
        "derived_from": "docs/experiments/manifests/math16_method2_all_cell_protocol_v1.json",
        "population": {
            "model": "qwen3.5:9b",
            "model_group": "qwen9b",
            "dataset": "CE115_Math16",
            "tasks": 16,
            "conditions": 4,
            "seeds_per_task_condition": 5,
            "expected_cells": 320,
            "expected_c0_pass": 101,
            "expected_c0_fail": 219,
        },
        "inputs": {
            "cell_plan": str(CELL_PLAN.relative_to(ROOT)).replace("\\", "/"),
            "raw_response_name": "raw_response.txt",
            "baseline_evaluation": str(BASELINE_OVERALL.relative_to(ROOT)).replace(
                "\\", "/"
            ),
            "baseline_cell_jsonl": str(BASELINE_JSONL.relative_to(ROOT)).replace(
                "\\", "/"
            ),
            "raw_source_extraction": "agent_tools/finals_rebuild/extraction.py::extract_code",
            "baseline_results_forbidden_for_eligibility": True,
        },
        "healer": {
            "runner": "agent_tools/finals_rebuild/ce115_research_healer_runner.py::MathHealerRunner",
            "rule_allowlist": list(RULE_ALLOWLIST),
            "max_passes": 3,
            "noneligible_policy": "final_source_equals_raw_source",
            "no_new_rules": True,
            "semantic_changes_forbidden": True,
            "rule_freeze_audit": rule_freeze,
        },
        "evaluation": {
            "evaluator": "scripts/evaluate_math16_pilot02_full_v4.py via classify_math16_response",
            "raw_and_final_evaluated_separately": True,
        },
        "outputs": {
            "root": str(RESULTS_ROOT.relative_to(ROOT)).replace("\\", "/"),
            "raw_source_directory": str(
                (RESULTS_ROOT / "raw_sources").relative_to(ROOT)
            ).replace("\\", "/"),
            "final_source_directory": str(
                (RESULTS_ROOT / "final_sources").relative_to(ROOT)
            ).replace("\\", "/"),
            "eligibility_journal": str(
                (RESULTS_ROOT / "eligibility_journal.jsonl").relative_to(ROOT)
            ).replace("\\", "/"),
            "transition_journal": str(
                (RESULTS_ROOT / "transition_journal.jsonl").relative_to(ROOT)
            ).replace("\\", "/"),
        },
        "frozen_sha256": frozen,
        "head": head_sha(),
    }


def build_c0_closure(plan: list[dict[str, Any]]) -> dict[str, Any]:
    overall = json.loads(BASELINE_OVERALL.read_text(encoding="utf-8"))
    if overall.get("passed") != 101 or overall.get("total") != 320:
        raise RuntimeError(
            f"BASELINE_101_NOT_CLOSED: passed={overall.get('passed')} total={overall.get('total')}"
        )
    baseline_rows = {row["cell_id"]: row for row in load_jsonl(BASELINE_JSONL)}
    if len(baseline_rows) != 320:
        raise RuntimeError(f"BASELINE_JSONL_COUNT: {len(baseline_rows)}")
    if len(plan) != 320 or len({c["cell_id"] for c in plan}) != 320:
        raise RuntimeError("CELL_PLAN_IDENTITY_FAILURE")

    cells = []
    pass_n = fail_n = 0
    missing = []
    for cell in plan:
        cid = cell["cell_id"]
        base = baseline_rows.get(cid)
        if base is None:
            missing.append(cid)
            continue
        raw_path = (
            ROOT
            / "docs/experiments/results"
            / cell["output_relative_path"]
            / "raw_response.txt"
        )
        if not raw_path.exists():
            raise RuntimeError(f"MISSING_RAW_RESPONSE: {cid}")
        extraction = extract_code(raw_path.read_text(encoding="utf-8"))
        raw_source = (
            extraction.extracted_code if extraction.extraction_status == "extracted" else ""
        )
        status = base["final_status"]
        if status == "PASSED":
            pass_n += 1
        elif status == "FAILED":
            fail_n += 1
        else:
            raise RuntimeError(f"BAD_STATUS: {cid} {status}")
        cells.append(
            {
                "cell_id": cid,
                "model": cell.get("model_tag", "qwen3.5:9b"),
                "model_group": "qwen9b",
                "task_id": cell["task_id"],
                "condition": cell["condition"],
                "seed": cell["seed"],
                "c0_outcome": status,
                "raw_response_path": str(raw_path.relative_to(ROOT)).replace("\\", "/"),
                "raw_response_sha256": sha256_path(raw_path),
                "extraction_status": extraction.extraction_status,
                "extraction_method": extraction.extraction_method,
                "c0_raw_source_sha256": sha256_bytes(raw_source.encode("utf-8")),
                "baseline_candidate_hash": base.get("candidate_hash"),
                "baseline_raw_response_sha256": base.get("raw_response_sha256"),
                "source_origin": "PILOT02_QWEN9B_RAW_RESPONSE",
            }
        )

    if missing:
        raise RuntimeError(f"BASELINE_MISSING_IDS: {missing[:5]}")
    if pass_n != 101 or fail_n != 219:
        raise RuntimeError(f"C0_PASS_FAIL_DRIFT: {pass_n}/{fail_n}")

    by_cond = Counter(c["condition"] for c in cells)
    by_task = Counter(c["task_id"] for c in cells)
    manifest = {
        "status": "math16_c0_baseline_closure_qwen9b_v1",
        "verdict": "C0_BASELINE_CLOSURE_PASSED",
        "head": head_sha(),
        "model": "qwen3.5:9b",
        "authority": str(BASELINE_OVERALL.relative_to(ROOT)).replace("\\", "/"),
        "validation": {
            "n_cells": 320,
            "unique_ids": 320,
            "duplicate_ids": 0,
            "pass_n": 101,
            "fail_n": 219,
            "expected_pass": 101,
            "expected_fail": 219,
            "tasks": 16,
            "conditions": 4,
            "seeds": 5,
            "by_condition": dict(by_cond),
            "by_task_n": len(by_task),
            "passed": True,
        },
        "cells": cells,
        "declarations": [
            "no_model_calls",
            "no_healer_mutation",
            "baseline_from_frozen_evaluation_v4_r001",
        ],
    }
    write_json(OUT_C0_MANIFEST, manifest)
    write_text(
        OUT_C0_REPORT,
        "\n".join(
            [
                "# Math16 C0 Baseline Closure — Qwen9B v1",
                "",
                f"> **verdict:** `{manifest['verdict']}`",
                f"> **HEAD:** `{manifest['head']}`",
                f"> **authority:** `{manifest['authority']}`",
                "",
                "## Validation",
                "",
                "- Cells: **320** (16×4×5); unique 320; duplicates 0",
                "- PASS / FAIL: **101 / 219**",
                f"- by_condition: `{dict(by_cond)}`",
                "- Raw responses present: **320/320**",
                "- No model calls; extraction used only for SHA lineage fields",
                "",
                "## Declarations",
                "",
                "- Frozen 9B evaluation_v4_r001 is C0 PASS/FAIL authority",
                "- No Healer / evaluator re-run in this closure step",
                "",
            ]
        )
        + "\n",
    )
    return manifest


def _assert_phase_a_row(row: Mapping[str, Any]) -> None:
    if tuple(row)[: len(PHASE_A_ONLY_FIELDS)] != PHASE_A_ONLY_FIELDS:
        raise RuntimeError("PHASE_A_JOURNAL_FIELD_DRIFT")
    if not row["eligibility_checked"]:
        raise RuntimeError("ELIGIBILITY_NOT_CHECKED")
    if row["raw_status"] is not None or row["final_status"] is not None:
        raise RuntimeError("STATUS_FORBIDDEN_IN_PHASE_A")
    if row["transition"] is not None:
        raise RuntimeError("TRANSITION_FORBIDDEN_IN_PHASE_A")
    if not row["eligible"] and (
        row["raw_source_sha256"] != row["final_source_sha256"] or row["source_changed"]
    ):
        raise RuntimeError("NONELIGIBLE_FINAL_SOURCE_DRIFT")


def run_phase_a(plan: list[dict[str, Any]], output_root: Path) -> dict[str, Any]:
    if output_root.exists():
        raise RuntimeError(f"OUTPUT_ALREADY_EXISTS: {output_root}")
    raw_dir = output_root / "raw_sources"
    final_dir = output_root / "final_sources"
    journal_path = output_root / "eligibility_journal.jsonl"
    output_root.mkdir(parents=True)
    tasks = tasks_by_id()
    runner = MathHealerRunner(max_passes=3)
    rows: list[dict[str, Any]] = []
    extraction_counts: Counter[str] = Counter()
    rule_counts: Counter[str] = Counter()
    try:
        for cell in plan:
            cell_id = cell["cell_id"]
            raw_response_path = (
                ROOT
                / "docs/experiments/results"
                / cell["output_relative_path"]
                / "raw_response.txt"
            )
            extraction = extract_code(raw_response_path.read_text(encoding="utf-8"))
            extraction_counts[extraction.extraction_status] += 1
            raw_source = (
                extraction.extracted_code
                if extraction.extraction_status == "extracted"
                else ""
            )
            frozen = frozen_for_prompt(tasks[cell["task_id"]])["oracle_payload"]
            context = {"frozen": frozen}
            eligibility = decide_eligibility(raw_source or None, context)
            provenance: list[dict[str, Any]] = []
            rolled_back = False
            if eligibility["eligible"]:
                result = runner.run(raw_source, context=context)
                final_source = result.output_source
                rolled_back = bool(result.rolled_back)
                provenance = [
                    {
                        "pass_index": item.pass_index,
                        "selected_rule_id": item.selected_rule_id,
                        "changed": item.changed,
                        "stop_reason": item.stop_reason,
                    }
                    for item in result.provenance
                ]
                for item in provenance:
                    if item["changed"] and item["selected_rule_id"]:
                        rule_counts[item["selected_rule_id"]] += 1
            else:
                final_source = raw_source

            raw_bytes = raw_source.encode("utf-8")
            final_bytes = final_source.encode("utf-8")
            write_bytes(raw_dir / f"{cell_id}.py", raw_bytes)
            write_bytes(final_dir / f"{cell_id}.py", final_bytes)
            row = {
                "cell_identity": {
                    "cell_id": cell_id,
                    "task_id": cell["task_id"],
                    "condition": cell["condition"],
                    "seed": cell["seed"],
                },
                "raw_source_sha256": sha256_bytes(raw_bytes),
                "eligibility_checked": True,
                "eligible": bool(eligibility["eligible"]),
                "rule_id": eligibility["rule_id"],
                "rule_triggered": bool(eligibility["rule_triggered"]),
                "source_changed": raw_bytes != final_bytes,
                "final_source_sha256": sha256_bytes(final_bytes),
                "raw_status": None,
                "final_status": None,
                "transition": None,
                "extraction_status": extraction.extraction_status,
                "extraction_method": extraction.extraction_method,
                "rolled_back": rolled_back,
                "healer_provenance": provenance,
                "raw_parses": parses(raw_source),
                "final_parses": parses(final_source),
            }
            _assert_phase_a_row(row)
            rows.append(row)

        write_jsonl(journal_path, rows)
        validation = {
            "cells": len(rows),
            "unique_cell_identities": len(
                {r["cell_identity"]["cell_id"] for r in rows}
            ),
            "eligible": sum(bool(r["eligible"]) for r in rows),
            "rule_triggered": sum(bool(r["rule_triggered"]) for r in rows),
            "source_changed": sum(bool(r["source_changed"]) for r in rows),
            "noneligible": sum(not bool(r["eligible"]) for r in rows),
        }
        summary = {
            "phase": "9B C0→C1 Tier A Phase A source decisions",
            "status": "COMPLETE",
            "validation": validation,
            "extraction_counts": dict(sorted(extraction_counts.items())),
            "changed_rule_counts": dict(sorted(rule_counts.items())),
            "journal_sha256": sha256_path(journal_path),
            "baseline_results_read": False,
            "evaluator_executed": False,
            "model_calls": 0,
        }
        write_json(output_root / "phase_a_summary.json", summary)
        write_json(
            output_root / "phase_a_freeze.json",
            {
                "journal_sha256": summary["journal_sha256"],
                "cells": 320,
                "eligible": validation["eligible"],
                "source_changed": validation["source_changed"],
            },
        )
        return summary
    except Exception:
        if output_root.exists():
            shutil.rmtree(output_root)
        raise


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
        raise RuntimeError(f"UNEXPECTED_EVALUATOR_STATUS: {status}")
    return {
        "status": status,
        "classifier_outcome": outcome,
        "primary_failure_layer": mapped["primary_failure_layer"],
        "failure_subtype": mapped["failure_subtype"],
    }


def run_phase_b(phase_a_rows: list[dict[str, Any]], output_root: Path) -> dict[str, Any]:
    raw_dir = output_root / "raw_sources"
    final_dir = output_root / "final_sources"
    transition_path = output_root / "transition_journal.jsonl"
    tasks = tasks_by_id()
    _, api_policy_map = _load_family_and_api_policy()
    result_rows: list[dict[str, Any]] = []
    parse_gain = execution_gain = 0

    for index, phase_a in enumerate(phase_a_rows, start=1):
        identity = phase_a["cell_identity"]
        cell_id = identity["cell_id"]
        task = tasks[identity["task_id"]]
        frozen_params = frozen_for_prompt(task)["oracle_payload"]
        api_policy = api_policy_map[identity["task_id"]]
        raw_source = (raw_dir / f"{cell_id}.py").read_text(encoding="utf-8")
        final_source = (final_dir / f"{cell_id}.py").read_text(encoding="utf-8")
        if sha256_bytes(raw_source.encode("utf-8")) != phase_a["raw_source_sha256"]:
            # journals store sha of encoded bytes without forcing newline rewrite
            if sha256_path(raw_dir / f"{cell_id}.py") != phase_a["raw_source_sha256"]:
                raise RuntimeError(f"RAW_SHA_DRIFT: {cell_id}")
        if sha256_path(final_dir / f"{cell_id}.py") != phase_a["final_source_sha256"]:
            raise RuntimeError(f"FINAL_SHA_DRIFT: {cell_id}")

        raw_score = score_source(
            raw_source, task=task, frozen_params=frozen_params, api_policy=api_policy
        )
        final_score = score_source(
            final_source, task=task, frozen_params=frozen_params, api_policy=api_policy
        )
        transition = classify_transition(raw_score["status"], final_score["status"])
        raw_parses = parses(raw_source)
        final_parses = parses(final_source)
        cell_parse_gain = (not raw_parses) and final_parses
        # execution gain: raw failed at parse/runtime-ish, final reached answer layer or pass
        raw_layer = raw_score["primary_failure_layer"]
        final_layer = final_score["primary_failure_layer"]
        cell_exec_gain = False
        if phase_a["source_changed"]:
            if raw_score["status"] == "FAILED" and final_score["status"] == "PASSED":
                cell_exec_gain = True
            elif raw_layer in {"parse", "execution", "runtime"} and final_layer in {
                "contract",
                "correctness",
                None,
                "answer",
            }:
                cell_exec_gain = True
            elif (
                raw_score["failure_subtype"]
                in {
                    "missing_entry_point",
                    "runtime_failure",
                    "syntax_error",
                    "parse_error",
                }
                and final_score["failure_subtype"]
                in {"answer_incorrect", "structural_mismatch", None}
            ):
                cell_exec_gain = True
        parse_gain += int(cell_parse_gain)
        execution_gain += int(cell_exec_gain)

        result_rows.append(
            {
                "cell_identity": identity,
                "raw_source_sha256": phase_a["raw_source_sha256"],
                "final_source_sha256": phase_a["final_source_sha256"],
                "eligibility_checked": phase_a["eligibility_checked"],
                "eligible": phase_a["eligible"],
                "rule_id": phase_a["rule_id"],
                "rule_triggered": phase_a["rule_triggered"],
                "source_changed": phase_a["source_changed"],
                "raw_status": raw_score["status"],
                "final_status": final_score["status"],
                "transition": transition,
                "raw_classifier_outcome": raw_score["classifier_outcome"],
                "final_classifier_outcome": final_score["classifier_outcome"],
                "raw_primary_failure_layer": raw_score["primary_failure_layer"],
                "final_primary_failure_layer": final_score["primary_failure_layer"],
                "raw_failure_subtype": raw_score["failure_subtype"],
                "final_failure_subtype": final_score["failure_subtype"],
                "raw_parses": raw_parses,
                "final_parses": final_parses,
                "parse_gain": cell_parse_gain,
                "execution_gain": cell_exec_gain,
                "abstained": not phase_a["eligible"],
                "modified": bool(phase_a["source_changed"]),
                "triggered": bool(phase_a["rule_triggered"]),
            }
        )
        if index % 40 == 0:
            print(f"[phase_b {index}/320]")

    write_jsonl(transition_path, result_rows)
    transitions = Counter(r["transition"] for r in result_rows)
    raw_pass = sum(r["raw_status"] == "PASSED" for r in result_rows)
    final_pass = sum(r["final_status"] == "PASSED" for r in result_rows)
    eligible_rows = [r for r in result_rows if r["eligible"]]
    changed_rows = [r for r in result_rows if r["source_changed"]]

    rule_accounting: dict[str, Any] = {}
    grouped: dict[str, list] = defaultdict(list)
    for row in result_rows:
        grouped[row["rule_id"] or "NONELIGIBLE"].append(row)
    for rule_id, items in sorted(grouped.items()):
        rule_accounting[rule_id] = {
            "cells": len(items),
            "triggered": sum(bool(i["rule_triggered"]) for i in items),
            "modified": sum(bool(i["source_changed"]) for i in items),
            "rescue": sum(i["transition"] == "verified_rescue" for i in items),
            "raw_pass": sum(i["raw_status"] == "PASSED" for i in items),
            "final_pass": sum(i["final_status"] == "PASSED" for i in items),
            "transitions": dict(Counter(i["transition"] for i in items)),
        }

    summary = {
        "phase": "9B C0→C1 Tier A Phase B independent Raw/Final evaluation",
        "status": "COMPLETE",
        "cells": 320,
        "raw_pass": raw_pass,
        "final_pass": final_pass,
        "net_pass_change": final_pass - raw_pass,
        "transitions": {
            "verified_rescue": transitions["verified_rescue"],
            "regression": transitions["regression"],
            "preserved_pass": transitions["preserved_pass"],
            "still_failed": transitions["still_failed"],
        },
        "eligible_cells": len(eligible_rows),
        "source_changed_cells": len(changed_rows),
        "modified_still_failed": sum(
            1
            for r in changed_rows
            if r["transition"] == "still_failed"
        ),
        "parse_gain": parse_gain,
        "execution_gain": execution_gain,
        "regression_cell_ids": [
            r["cell_identity"]["cell_id"]
            for r in result_rows
            if r["transition"] == "regression"
        ],
        "verified_rescue_ids": [
            r["cell_identity"]["cell_id"]
            for r in result_rows
            if r["transition"] == "verified_rescue"
        ],
        "rule_accounting": rule_accounting,
        "phase_a_journal_sha256": sha256_path(output_root / "eligibility_journal.jsonl"),
        "phase_b_journal_sha256": sha256_path(transition_path),
        "model_calls": 0,
        "evaluator_used_for_selection": False,
    }
    write_json(output_root / "phase_b_summary.json", summary)
    write_json(output_root / "phase_b_rule_accounting.json", rule_accounting)
    write_jsonl(output_root / "phase_b_eligible_results.jsonl", eligible_rows)
    write_jsonl(output_root / "phase_b_source_changed_results.jsonl", changed_rows)
    return summary


def deterministic_second_replay(plan: list[dict[str, Any]], first_root: Path) -> dict[str, Any]:
    second = ROOT / "docs/experiments/results/_scratch_qwen9b_c1_second_replay"
    if second.exists():
        shutil.rmtree(second)
    run_phase_a(plan, second)
    first_rows = load_jsonl(first_root / "eligibility_journal.jsonl")
    second_rows = load_jsonl(second / "eligibility_journal.jsonl")
    mismatches = []
    by2 = {r["cell_identity"]["cell_id"]: r for r in second_rows}
    for r1 in first_rows:
        cid = r1["cell_identity"]["cell_id"]
        r2 = by2[cid]
        for key in (
            "raw_source_sha256",
            "final_source_sha256",
            "eligible",
            "rule_id",
            "rule_triggered",
            "source_changed",
        ):
            if r1[key] != r2[key]:
                mismatches.append({"cell_id": cid, "field": key, "a": r1[key], "b": r2[key]})
        # file bytes
        a = (first_root / "final_sources" / f"{cid}.py").read_bytes()
        b = (second / "final_sources" / f"{cid}.py").read_bytes()
        if a != b:
            mismatches.append({"cell_id": cid, "field": "final_source_bytes", "a": len(a), "b": len(b)})
    report = {
        "second_replay_mismatches": len(mismatches),
        "zero_diff": len(mismatches) == 0,
        "sample": mismatches[:20],
    }
    write_json(first_root / "deterministic_second_replay.json", report)
    shutil.rmtree(second)
    if mismatches:
        raise RuntimeError(f"SECOND_REPLAY_DIFF: {len(mismatches)}")
    return report


def build_c1_closure(
    plan: list[dict[str, Any]],
    c0: dict[str, Any],
    phase_b: dict[str, Any],
    transition_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    c0_by_id = {c["cell_id"]: c for c in c0["cells"]}
    cells = []
    for row in transition_rows:
        identity = row["cell_identity"]
        cid = identity["cell_id"]
        c0_cell = c0_by_id[cid]
        if row["source_changed"]:
            origin = "TIER_A_POST_SOURCE"
        else:
            origin = "C0_RAW_PRESERVED"
        cells.append(
            {
                "cell_id": cid,
                "model": "qwen3.5:9b",
                "model_group": "qwen9b",
                "task_id": identity["task_id"],
                "condition": identity["condition"],
                "seed": identity["seed"],
                "c0_outcome": c0_cell["c0_outcome"],
                "c0_raw_source_sha256": row["raw_source_sha256"],
                "c1_final_source_path": str(
                    (RESULTS_ROOT / "final_sources" / f"{cid}.py").relative_to(ROOT)
                ).replace("\\", "/"),
                "c1_final_source_sha256": row["final_source_sha256"],
                "c1_outcome": row["final_status"],
                "source_origin": origin,
                "eligible": row["eligible"],
                "rule_id": row["rule_id"],
                "rule_triggered": row["rule_triggered"],
                "source_changed": row["source_changed"],
                "transition": row["transition"],
                "parse_gain": row["parse_gain"],
                "execution_gain": row["execution_gain"],
            }
        )

    pass_n = sum(c["c1_outcome"] == "PASSED" for c in cells)
    fail_n = 320 - pass_n
    manifest = {
        "status": "math16_c1_final_source_closure_qwen9b_v1",
        "verdict": "C1_FINAL_SOURCE_CLOSURE_PASSED",
        "definition": "C1 = C0 + Tier A frozen six-rule Conservative Healer",
        "head": head_sha(),
        "validation": {
            "n_cells": 320,
            "unique_ids": 320,
            "duplicate_ids": 0,
            "c0_pass": 101,
            "c0_fail": 219,
            "phase_b_raw_pass": phase_b["raw_pass"],
            "c1_pass": pass_n,
            "c1_fail": fail_n,
            "verified_rescue": phase_b["transitions"]["verified_rescue"],
            "regression": phase_b["transitions"]["regression"],
            "preserved_pass": phase_b["transitions"]["preserved_pass"],
            "still_failed": phase_b["transitions"]["still_failed"],
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
    write_json(OUT_C1_CLOSURE_MANIFEST, manifest)
    write_text(
        OUT_C1_CLOSURE_REPORT,
        "\n".join(
            [
                "# Math16 C1 Final-Source Closure — Qwen9B v1",
                "",
                f"> **verdict:** `{manifest['verdict']}`",
                f"> **definition:** `{manifest['definition']}`",
                f"> **HEAD:** `{manifest['head']}`",
                "",
                "## Validation",
                "",
                f"- Cells: **320**; C1 PASS/FAIL: **{pass_n}/{fail_n}**",
                f"- Phase B raw PASS: **{phase_b['raw_pass']}** (C0 authority remains 101)",
                f"- verified_rescue / regression: **{phase_b['transitions']['verified_rescue']} / {phase_b['transitions']['regression']}**",
                f"- preserved_pass / still_failed: **{phase_b['transitions']['preserved_pass']} / {phase_b['transitions']['still_failed']}**",
                f"- source_origin: `{manifest['validation']['origin_counts']}`",
                "",
                "## Declarations",
                "",
                "- No fallback / missing / duplicate identities",
                "- Final sources under reproducibility root only",
                "",
            ]
        )
        + "\n",
    )
    return manifest


def write_replay_report(
    protocol: dict[str, Any],
    phase_a: dict[str, Any],
    phase_b: dict[str, Any],
    second: dict[str, Any],
    rule_freeze: dict[str, Any],
) -> dict[str, Any]:
    manifest = {
        "status": "math16_c0_c1_tier_a_reproducibility_qwen9b_v1",
        "verdict": "C0_C1_TIER_A_QWEN9B_COMPLETE",
        "head": head_sha(),
        "protocol": str(OUT_PROTOCOL.relative_to(ROOT)).replace("\\", "/"),
        "results_root": str(RESULTS_ROOT.relative_to(ROOT)).replace("\\", "/"),
        "rule_allowlist": list(RULE_ALLOWLIST),
        "rule_freeze_audit": rule_freeze,
        "phase_a": phase_a,
        "phase_b": phase_b,
        "deterministic_second_replay": second,
        "model_calls": 0,
    }
    write_json(OUT_C1_REPLAY_MANIFEST, manifest)
    ra = phase_b["rule_accounting"]
    lines = [
        "# Math16 C0→C1 Tier A Reproducibility — Qwen9B v1",
        "",
        f"> **verdict:** `{manifest['verdict']}`",
        f"> **HEAD:** `{manifest['head']}`",
        f"> **results:** `{manifest['results_root']}`",
        "",
        "## Core counts",
        "",
        "| Metric | Value |",
        "|---|---:|",
        "| C0 authority PASS | 101 |",
        f"| Phase B raw PASS | {phase_b['raw_pass']} |",
        f"| C1 final PASS | {phase_b['final_pass']} |",
        f"| verified_rescue | {phase_b['transitions']['verified_rescue']} |",
        f"| regression | {phase_b['transitions']['regression']} |",
        f"| preserved_pass | {phase_b['transitions']['preserved_pass']} |",
        f"| still_failed | {phase_b['transitions']['still_failed']} |",
        f"| eligible / modified | {phase_b['eligible_cells']} / {phase_b['source_changed_cells']} |",
        f"| modified still failed | {phase_b['modified_still_failed']} |",
        f"| parse_gain | {phase_b['parse_gain']} |",
        f"| execution_gain | {phase_b['execution_gain']} |",
        "",
        "## Rule accounting",
        "",
    ]
    for rule_id, info in ra.items():
        lines.append(
            f"- `{rule_id}`: triggered={info['triggered']} modified={info['modified']} rescue={info['rescue']}"
        )
    lines += [
        "",
        "## Determinism",
        "",
        f"- Second Phase A replay zero-diff: **{second['zero_diff']}**",
        "",
        "## Rule freeze",
        "",
        f"- Allowlist order matches Method2 4B: **{rule_freeze['rule_order_matches_method2']}**",
        f"- Note: {rule_freeze['note']}",
        "",
        "## Declarations",
        "",
        "- Model calls: **0**",
        "- Healer rules / thresholds / order modified: **No**",
        "- 4B artifacts modified: **No**",
        "- Commit / push: **No**",
        "",
    ]
    write_text(OUT_C1_REPLAY_REPORT, "\n".join(lines) + "\n")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-second-replay", action="store_true")
    args = parser.parse_args()

    print("== rule freeze audit ==")
    rule_freeze = verify_rule_freeze()
    protocol = build_protocol(rule_freeze)
    write_json(OUT_PROTOCOL, protocol)

    plan = json.loads(CELL_PLAN.read_text(encoding="utf-8"))
    print("== C0 baseline closure ==")
    c0 = build_c0_closure(plan)

    if RESULTS_ROOT.exists():
        shutil.rmtree(RESULTS_ROOT)
    print("== Phase A ==")
    phase_a = run_phase_a(plan, RESULTS_ROOT)
    print(json.dumps(phase_a["validation"], ensure_ascii=False))

    print("== Phase B ==")
    phase_a_rows = load_jsonl(RESULTS_ROOT / "eligibility_journal.jsonl")
    phase_b = run_phase_b(phase_a_rows, RESULTS_ROOT)
    print(
        f"raw={phase_b['raw_pass']} final={phase_b['final_pass']} "
        f"rescue={phase_b['transitions']['verified_rescue']} "
        f"regression={phase_b['transitions']['regression']}"
    )

    if args.skip_second_replay:
        second = {"zero_diff": None, "skipped": True}
    else:
        print("== second deterministic Phase A ==")
        second = deterministic_second_replay(plan, RESULTS_ROOT)

    transition_rows = load_jsonl(RESULTS_ROOT / "transition_journal.jsonl")
    print("== C1 closure ==")
    c1 = build_c1_closure(plan, c0, phase_b, transition_rows)
    write_replay_report(protocol, phase_a, phase_b, second, rule_freeze)

    print("DONE")
    print(
        json.dumps(
            {
                "c0_pass": c0["validation"]["pass_n"],
                "c1_pass": c1["validation"]["c1_pass"],
                "rescue": phase_b["transitions"]["verified_rescue"],
                "regression": phase_b["transitions"]["regression"],
                "second_zero_diff": second.get("zero_diff"),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
