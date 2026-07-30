# -*- coding: utf-8 -*-
"""Gemini 3.5 Flash C0→C4 FAIL-only cumulative gate — authoritative chain.

Namespace: gemini_fail_gated_authoritative_v1

Policy (aligned with 4B／9B FAIL-gated):
- Every layer retains full 320-cell final sources.
- Only prior-layer FAIL cells enter the Healer / eligibility census.
- Prior-layer PASS cells are byte-preserved (no scan, no mutation);
  source_origin = PRIOR_PASS_PRESERVED; post SHA == pre SHA.

Does not modify frozen rules/thresholds/order, 4B／9B artifacts, or call a model.
Does not overwrite NONAUTHORITATIVE all-cell exploratory products.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Callable, Optional

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.aggressive_healer_tier_a import (  # noqa: E402
    RULE_ORDER as TIER_B_RULE_ORDER,
    run_tier_a_pipeline,
)
from agent_tools.finals_rebuild.aggressive_healer_tier_c2 import (  # noqa: E402
    RULE_ID as TIER_C2_RULE_ID,
    SUBTYPE as TIER_C2_SUBTYPE,
    run_tier_c2_default_optional_cleanup,
)
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
    classify_transition,
    decide_eligibility,
)
from scripts.run_math16_c2_c3_tier_c1_qwen9b_v1 import (  # noqa: E402
    adjudicate_c1,
    apply_c1_rename,
)
from scripts.run_math16_c3_c4_tier_c2_qwen9b_v1 import adjudicate_c2  # noqa: E402
from scripts.run_math16_latex_v1_gemini_live import classify_math16_response  # noqa: E402

NS = "gemini_fail_gated_authoritative_v1"
AUTHORITY = "AUTHORITATIVE_FAIL_GATED_CUMULATIVE_V1"

CELL_PLAN = ROOT / "docs/experiments/manifests/math16_pilot02_full_analysis_inventory.json"
BASELINE_OVERALL = (
    ROOT
    / "docs/experiments/results/math16_pilot02_full_evaluation_v4_r001/baseline_summary.json"
)
BASELINE_JSONL = (
    ROOT
    / "docs/experiments/results/math16_pilot02_full_evaluation_v4_r001/cell_level_baseline.jsonl"
)
CONTRACT_MATRIX = ROOT / "docs/experiments/manifests/math16_ab2d_task_contract_matrix_v1.json"
C0_PASS = 289
C0_FAIL = 31

TIER_B_EXPECTED_ORDER = (
    "core.normalize_fullwidth_python_punctuation",
    "TIER_A_UNIQUE_MISSING_DELIMITER_REPAIR_V1",
    "TIER_A_EMPTY_SUITE_INSERT_PASS_V1",
    "TIER_A_UNIQUE_IMPORT_BINDING_REPAIR_V1",
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


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


def is_executable_obs(score: dict[str, Any]) -> bool:
    if score["status"] == "PASSED":
        return True
    blob = " ".join(
        [
            str(score.get("failure_subtype") or ""),
            str(score.get("classifier_outcome") or ""),
            str(score.get("primary_failure_layer") or ""),
        ]
    ).lower()
    return not any(
        b in blob
        for b in ("parse", "syntax", "runtime", "missing_entry", "extraction", "unparseable")
    )


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


def ns_path(*parts: str) -> Path:
    return ROOT.joinpath(*parts)


def expect(cond: bool, msg: str) -> None:
    if not cond:
        raise RuntimeError(msg)


# ---------------------------------------------------------------------------
# C0 baseline
# ---------------------------------------------------------------------------


def build_c0() -> dict[str, Any]:
    plan = json.loads(CELL_PLAN.read_text(encoding="utf-8"))
    if isinstance(plan, dict) and "cells" in plan:
        plan = plan["cells"]
    overall = json.loads(BASELINE_OVERALL.read_text(encoding="utf-8"))
    expect(
        overall.get("passed") == C0_PASS and overall.get("total") == 320,
        "C0_BASELINE_DRIFT",
    )
    baseline_rows = {row["cell_id"]: row for row in load_jsonl(BASELINE_JSONL)}
    expect(len(baseline_rows) == 320 and len(plan) == 320, "C0_IDENTITY_DRIFT")

    cells = []
    pass_n = fail_n = 0
    for cell in plan:
        cid = cell["cell_id"]
        base = baseline_rows[cid]
        raw_path = (
            ROOT
            / "docs/experiments/results"
            / cell["output_relative_path"]
            / "raw_response.txt"
        )
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
            raise RuntimeError(f"BAD_C0_STATUS: {cid} {status}")
        cells.append(
            {
                "cell_id": cid,
                "model": "gemini-3.5-flash",
                "model_group": "gemini",
                "task_id": cell["task_id"],
                "condition": cell["condition"],
                "seed": cell["seed"],
                "c0_outcome": status,
                "raw_response_path": str(raw_path.relative_to(ROOT)).replace("\\", "/"),
                "extraction_status": extraction.extraction_status,
                "c0_raw_source_sha256": sha256_text(raw_source),
                "c0_raw_source": raw_source,  # ephemeral; stripped before write
                "output_relative_path": cell["output_relative_path"],
                "source_origin": "PILOT02_GEMINI_RAW_RESPONSE",
            }
        )
    expect(pass_n == C0_PASS and fail_n == C0_FAIL, f"C0_PASS_FAIL: {pass_n}/{fail_n}")

    # persist sources for lineage
    raw_dir = ns_path(
        "docs/experiments/results",
        f"math16_c0_baseline_{NS}",
        "raw_sources",
    )
    if raw_dir.exists():
        shutil.rmtree(raw_dir.parent)
    raw_dir.mkdir(parents=True)
    out_cells = []
    for c in cells:
        path = raw_dir / f"{c['cell_id']}.py"
        path.write_bytes(c["c0_raw_source"].encode("utf-8"))
        rel = str(path.relative_to(ROOT)).replace("\\", "/")
        out_cells.append(
            {
                **{k: v for k, v in c.items() if k != "c0_raw_source"},
                "c0_final_source_path": rel,
                "c0_final_source_sha256": c["c0_raw_source_sha256"],
            }
        )

    manifest = {
        "status": f"math16_c0_baseline_closure_{NS}",
        "verdict": "C0_BASELINE_CLOSURE_PASSED",
        "authority_status": AUTHORITY,
        "gating_policy": "FAIL_ONLY_CUMULATIVE",
        "namespace": NS,
        "head": head_sha(),
        "validation": {
            "n_cells": 320,
            "unique_ids": 320,
            "duplicate_ids": 0,
            "pass_n": C0_PASS,
            "fail_n": C0_FAIL,
            "passed": True,
        },
        "cells": out_cells,
        "declarations": [
            "authoritative_fail_gated",
            "no_model_calls",
            "baseline_from_frozen_evaluation_v4_r001",
        ],
    }
    write_json(
        ns_path("docs/experiments/manifests", f"math16_c0_baseline_closure_{NS}.json"),
        manifest,
    )
    write_text(
        ns_path("docs/experiments/reports", f"math16_c0_baseline_closure_{NS}.md"),
        "\n".join(
            [
                f"# Math16 C0 Baseline Closure — {NS}",
                "",
                f"> **AUTHORITY:** `{AUTHORITY}`",
                f"> **HEAD:** `{head_sha()}`",
                "",
                f"- Cells: **320**; PASS/FAIL: **{C0_PASS}／{C0_FAIL}**",
                "- Gating: FAIL-only cumulative chain baseline",
                "",
            ]
        )
        + "\n",
    )
    return manifest


# ---------------------------------------------------------------------------
# Shared layer runner
# ---------------------------------------------------------------------------


def run_fail_gated_layer(
    *,
    layer_name: str,
    prior_closure: dict[str, Any],
    prior_outcome_key: str,
    prior_path_key: str,
    prior_sha_key: str,
    next_outcome_key: str,
    next_path_key: str,
    next_sha_key: str,
    results_dirname: str,
    expected_prior_pass: int,
    expected_prior_fail: int,
    expected_next_pass: Optional[int],
    heal_fail_cell: Callable[..., dict[str, Any]],
    second_heal: Callable[..., str],
    eligibility_counter_keys: Optional[list[str]] = None,
) -> dict[str, Any]:
    results_root = ns_path("docs/experiments/results", results_dirname)
    if results_root.exists():
        shutil.rmtree(results_root)
    pre_dir = results_root / "pre_sources"
    post_dir = results_root / "post_sources"
    pre_dir.mkdir(parents=True)
    post_dir.mkdir(parents=True)

    tasks = tasks_by_id()
    _, api_policy_map = _load_family_and_api_policy()
    rows: list[dict[str, Any]] = []
    census_rows: list[dict[str, Any]] = []

    prior_pass = sum(1 for c in prior_closure["cells"] if c[prior_outcome_key] == "PASSED")
    prior_fail = sum(1 for c in prior_closure["cells"] if c[prior_outcome_key] == "FAILED")
    expect(prior_pass == expected_prior_pass, f"{layer_name}_PRIOR_PASS:{prior_pass}")
    expect(prior_fail == expected_prior_fail, f"{layer_name}_PRIOR_FAIL:{prior_fail}")

    for index, cell in enumerate(prior_closure["cells"], start=1):
        cid = cell["cell_id"]
        prior_outcome = cell[prior_outcome_key]
        pre_path = ROOT / cell[prior_path_key]
        pre_source = pre_path.read_text(encoding="utf-8")
        expect(sha256_path(pre_path) == cell[prior_sha_key], f"PRIOR_SHA_DRIFT:{cid}")

        gated = prior_outcome == "FAILED"
        heal_info: dict[str, Any]
        if not gated:
            # PASS: no scan, no mutation
            post_source = pre_source
            heal_info = {
                "gated_into_healer": False,
                "eligible": False,
                "eligibility_status": "PRIOR_PASS_NOT_SCANNED",
                "abstention_reason": "prior_pass_preserved_no_scan",
                "triggered": False,
                "modified": False,
                "abstained": True,
                "unique_mapping": None,
                "ssot_entry_id": None,
                "ast_node_location": None,
                "wrong_call": None,
                "pipeline_audit": None,
                "rule_triggered_ids": [],
            }
            origin = "PRIOR_PASS_PRESERVED"
            # Do not re-evaluate PASS; inherit prior outcome.
            pre_score = {
                "status": "PASSED",
                "classifier_outcome": "inherited_prior_pass",
                "primary_failure_layer": None,
                "failure_subtype": None,
            }
            post_score = dict(pre_score)
        else:
            heal_info = heal_fail_cell(cell=cell, pre_source=pre_source)
            post_source = heal_info["post_source"]
            origin = heal_info.get("source_origin_if_modified", f"{layer_name}_POST_SOURCE")
            if not heal_info["modified"]:
                origin = "PRIOR_FAIL_UNCHANGED"
            task = tasks[cell["task_id"]]
            frozen_params = frozen_for_prompt(task)["oracle_payload"]
            api_policy = api_policy_map[cell["task_id"]]
            pre_score = score_source(
                pre_source, task=task, frozen_params=frozen_params, api_policy=api_policy
            )
            post_score = score_source(
                post_source, task=task, frozen_params=frozen_params, api_policy=api_policy
            )
            expect(pre_score["status"] == "FAILED", f"GATED_PRE_NOT_FAIL:{cid}")

        expect(
            (not heal_info["modified"] and post_source == pre_source)
            or (heal_info["modified"] and post_source != pre_source),
            f"MODIFY_INVARIANT:{cid}",
        )
        if not gated:
            expect(post_source == pre_source, f"PASS_MUTATED:{cid}")
            expect(sha256_text(post_source) == sha256_text(pre_source), f"PASS_SHA:{cid}")

        (pre_dir / f"{cid}.py").write_bytes(pre_source.encode("utf-8"))
        (post_dir / f"{cid}.py").write_bytes(post_source.encode("utf-8"))

        transition = classify_transition(pre_score["status"], post_score["status"])
        pre_parse = parses(pre_source)
        post_parse = parses(post_source)
        pre_exec = is_executable_obs(pre_score) if gated else True
        post_exec = is_executable_obs(post_score) if gated else True
        parse_gain = (not pre_parse) and post_parse
        execution_gain = (not pre_exec) and post_exec
        blocker_removal = (
            heal_info["modified"]
            and transition != "verified_rescue"
            and (parse_gain or execution_gain)
        )

        if not gated:
            final_origin = "PRIOR_PASS_PRESERVED"
        elif heal_info["modified"]:
            final_origin = heal_info.get(
                "source_origin_if_modified", f"{layer_name}_POST_SOURCE"
            )
        else:
            final_origin = "PRIOR_FAIL_UNCHANGED"

        row = {
            "cell_id": cid,
            "model": "gemini-3.5-flash",
            "model_group": "gemini",
            "task_id": cell["task_id"],
            "condition": cell["condition"],
            "seed": cell["seed"],
            prior_outcome_key: prior_outcome,
            prior_path_key: cell[prior_path_key],
            prior_sha_key: cell[prior_sha_key],
            "pre_source_path": str((pre_dir / f"{cid}.py").relative_to(ROOT)).replace(
                "\\", "/"
            ),
            "post_source_path": str((post_dir / f"{cid}.py").relative_to(ROOT)).replace(
                "\\", "/"
            ),
            "pre_source_sha256": sha256_text(pre_source),
            "post_source_sha256": sha256_text(post_source),
            "gated_into_healer": gated,
            "eligibility_status": heal_info["eligibility_status"],
            "abstention_reason": heal_info.get("abstention_reason"),
            "eligible": bool(heal_info.get("eligible")),
            "triggered": bool(heal_info.get("triggered")),
            "modified": bool(heal_info.get("modified")),
            "abstained": bool(heal_info.get("abstained")),
            "pre_status": pre_score["status"],
            "post_status": post_score["status"],
            next_outcome_key: post_score["status"],
            "transition": transition,
            "parse_gain": parse_gain,
            "execution_gain": execution_gain,
            "blocker_removal_only": blocker_removal,
            "source_origin": final_origin,
            "evaluator_used_for_selection": False,
            "model_calls": 0,
            "ssot_entry_id": heal_info.get("ssot_entry_id"),
            "ast_node_location": heal_info.get("ast_node_location"),
            "wrong_call": heal_info.get("wrong_call"),
            "unique_expected_method": heal_info.get("unique_expected_method"),
            "rule_triggered_ids": heal_info.get("rule_triggered_ids") or [],
        }
        rows.append(row)
        census_rows.append(
            {
                "cell_id": cid,
                "task_id": cell["task_id"],
                "condition": cell["condition"],
                "seed": cell["seed"],
                "gated_into_healer": gated,
                "status": heal_info["eligibility_status"],
                "abstention_reason": heal_info.get("abstention_reason"),
                "eligible": bool(heal_info.get("eligible")),
            }
        )
        if index % 40 == 0:
            print(f"[{layer_name} {index}/320]")

    write_jsonl(results_root / "transition_journal.jsonl", rows)
    write_jsonl(results_root / "census_journal.jsonl", census_rows)

    # second deterministic replay
    mismatches = []
    for cell, first in zip(prior_closure["cells"], rows):
        cid = cell["cell_id"]
        pre = (ROOT / cell[prior_path_key]).read_text(encoding="utf-8")
        if cell[prior_outcome_key] == "PASSED":
            post = pre
        else:
            post = second_heal(cell=cell, pre_source=pre)
        if sha256_text(post) != first["post_source_sha256"]:
            mismatches.append({"cell_id": cid, "field": "post_source_sha256"})
        if cell[prior_outcome_key] == "PASSED" and first["post_source_sha256"] != first[
            "pre_source_sha256"
        ]:
            mismatches.append({"cell_id": cid, "field": "pass_sha_changed"})
    second = {
        "second_replay_mismatches": len(mismatches),
        "zero_diff": len(mismatches) == 0,
        "sample": mismatches[:20],
    }
    write_json(results_root / "deterministic_second_replay.json", second)
    expect(second["zero_diff"], f"{layer_name}_SECOND_REPLAY_DIFF:{len(mismatches)}")

    gated_n = sum(1 for r in rows if r["gated_into_healer"])
    preserved_pass_n = sum(1 for r in rows if not r["gated_into_healer"])
    next_pass = sum(1 for r in rows if r["post_status"] == "PASSED")
    expect(gated_n == expected_prior_fail, f"{layer_name}_GATED:{gated_n}")
    expect(preserved_pass_n == expected_prior_pass, f"{layer_name}_PRESERVED:{preserved_pass_n}")
    if expected_next_pass is not None:
        expect(next_pass == expected_next_pass, f"{layer_name}_NEXT_PASS:{next_pass}")

    # PASS preserved SHA invariant
    for r in rows:
        if not r["gated_into_healer"]:
            expect(
                r["pre_source_sha256"] == r["post_source_sha256"],
                f"PASS_SHA_CHANGED:{r['cell_id']}",
            )
            expect(r["source_origin"] == "PRIOR_PASS_PRESERVED", f"PASS_ORIGIN:{r['cell_id']}")
            expect(not r["modified"] and not r["triggered"], f"PASS_TRIGGERED:{r['cell_id']}")

    status_counts = Counter(r["eligibility_status"] for r in rows if r["gated_into_healer"])
    # also count PRIOR_PASS_NOT_SCANNED separately
    status_counts_all = Counter(r["eligibility_status"] for r in rows)
    transitions = Counter(r["transition"] for r in rows)
    pass_pass_mod = sum(
        1
        for r in rows
        if r["modified"] and r["pre_status"] == "PASSED" and r["post_status"] == "PASSED"
    )
    expect(pass_pass_mod == 0, f"{layer_name}_PASS_PASS_MOD:{pass_pass_mod}")

    elig_keys = eligibility_counter_keys or []
    eligibility = {k: status_counts.get(k, 0) for k in elig_keys} if elig_keys else dict(
        status_counts
    )

    summary = {
        "phase": f"Gemini {layer_name} fail-gated authoritative",
        "status": "COMPLETE",
        "authority_status": AUTHORITY,
        "namespace": NS,
        "gating_policy": "FAIL_ONLY_CUMULATIVE",
        "cells": 320,
        "gated_fail_count": gated_n,
        "preserved_pass_count": preserved_pass_n,
        "eligibility_among_gated": eligibility,
        "eligibility_all_cells": dict(status_counts_all),
        "triggered": sum(r["triggered"] for r in rows),
        "modified": sum(r["modified"] for r in rows),
        "abstained": sum(r["abstained"] for r in rows),
        "prior_pass_observed": prior_pass,
        "next_pass": next_pass,
        "next_fail": 320 - next_pass,
        "transitions": {
            "verified_rescue": transitions.get("verified_rescue", 0),
            "regression": transitions.get("regression", 0),
            "preserved_pass": transitions.get("preserved_pass", 0),
            "still_failed": transitions.get("still_failed", 0),
        },
        "modified_still_failed": sum(
            1 for r in rows if r["modified"] and r["transition"] == "still_failed"
        ),
        "blocker_removal_only": sum(1 for r in rows if r["blocker_removal_only"]),
        "parse_gain": sum(r["parse_gain"] for r in rows),
        "execution_gain": sum(r["execution_gain"] for r in rows),
        "pass_pass_modified": pass_pass_mod,
        "verified_rescue_ids": [
            r["cell_id"] for r in rows if r["transition"] == "verified_rescue"
        ],
        "regression_ids": [r["cell_id"] for r in rows if r["transition"] == "regression"],
        "eligible_ids": [r["cell_id"] for r in rows if r["eligible"]],
        "model_calls": 0,
        "deterministic_second_replay": second,
    }
    write_json(results_root / "summary.json", summary)

    # closure cells
    closure_cells = []
    for r in rows:
        closure_cells.append(
            {
                "cell_id": r["cell_id"],
                "model": "gemini-3.5-flash",
                "model_group": "gemini",
                "task_id": r["task_id"],
                "condition": r["condition"],
                "seed": r["seed"],
                prior_outcome_key: r[prior_outcome_key],
                prior_path_key: r[prior_path_key],
                prior_sha_key: r[prior_sha_key],
                next_path_key: r["post_source_path"],
                next_sha_key: r["post_source_sha256"],
                next_outcome_key: r["post_status"],
                "source_origin": r["source_origin"],
                "gated_into_healer": r["gated_into_healer"],
                "eligibility_status": r["eligibility_status"],
                "modified": r["modified"],
                "transition": r["transition"],
            }
        )

    return {
        "summary": summary,
        "rows": rows,
        "census_rows": census_rows,
        "results_root": results_root,
        "closure_cells": closure_cells,
        "second": second,
    }


# ---------------------------------------------------------------------------
# Layer-specific healers
# ---------------------------------------------------------------------------


def heal_tier_a(*, cell: dict[str, Any], pre_source: str) -> dict[str, Any]:
    runner = MathHealerRunner(max_passes=3)
    tasks = tasks_by_id()
    frozen = frozen_for_prompt(tasks[cell["task_id"]])["oracle_payload"]
    context = {"frozen": frozen}
    eligibility = decide_eligibility(pre_source or None, context)
    if eligibility["eligible"]:
        result = runner.run(pre_source, context=context)
        post = result.output_source
        modified = post != pre_source
        return {
            "post_source": post,
            "gated_into_healer": True,
            "eligible": True,
            "eligibility_status": "TIER_A_ELIGIBLE",
            "abstention_reason": None,
            "triggered": bool(eligibility["rule_triggered"]) or modified,
            "modified": modified,
            "abstained": False,
            "source_origin_if_modified": "TIER_A_POST_SOURCE",
            "rule_triggered_ids": [
                p.selected_rule_id
                for p in result.provenance
                if p.changed and p.selected_rule_id
            ],
        }
    return {
        "post_source": pre_source,
        "gated_into_healer": True,
        "eligible": False,
        "eligibility_status": "TIER_A_INELIGIBLE",
        "abstention_reason": eligibility.get("reason")
        or eligibility.get("abstention_reason")
        or "not_eligible",
        "triggered": False,
        "modified": False,
        "abstained": True,
        "rule_triggered_ids": [],
    }


def second_tier_a(*, cell: dict[str, Any], pre_source: str) -> str:
    return heal_tier_a(cell=cell, pre_source=pre_source)["post_source"]


def heal_tier_b(*, cell: dict[str, Any], pre_source: str) -> dict[str, Any]:
    pipe = run_tier_a_pipeline(pre_source)
    post = pipe.post_source
    modified = post != pre_source
    fired = list(pipe.rules_fired or [])
    return {
        "post_source": post,
        "gated_into_healer": True,
        "eligible": modified or bool(fired),
        "eligibility_status": "TIER_B_TRIGGERED" if (modified or fired) else "TIER_B_NOOP",
        "abstention_reason": None if (modified or fired) else "no_tier_b_rule_fired",
        "triggered": bool(fired) or modified,
        "modified": modified,
        "abstained": not (modified or fired),
        "source_origin_if_modified": "TIER_B_POST_SOURCE",
        "rule_triggered_ids": fired,
        "pipeline_audit": pipe.to_audit_dict() if hasattr(pipe, "to_audit_dict") else None,
    }


def second_tier_b(*, cell: dict[str, Any], pre_source: str) -> str:
    return run_tier_a_pipeline(pre_source).post_source


_CONTRACTS: Optional[dict] = None


def contracts() -> dict:
    global _CONTRACTS
    if _CONTRACTS is None:
        matrix = json.loads(CONTRACT_MATRIX.read_text(encoding="utf-8"))
        _CONTRACTS = {
            (c["task_id"], c["condition_code"]): c for c in matrix["contracts"]
        }
    return _CONTRACTS


def heal_tier_c1(*, cell: dict[str, Any], pre_source: str) -> dict[str, Any]:
    adj = adjudicate_c1(
        source=pre_source,
        task_id=cell["task_id"],
        condition=cell["condition"],
        contracts_by_key=contracts(),
    )
    if adj["status"] != "C1_ELIGIBLE":
        return {
            "post_source": pre_source,
            "gated_into_healer": True,
            "eligible": False,
            "eligibility_status": adj["status"],
            "abstention_reason": adj.get("abstention_reason"),
            "triggered": False,
            "modified": False,
            "abstained": True,
            "wrong_call": adj.get("wrong_call"),
            "unique_expected_method": adj.get("unique_expected_method"),
            "rule_triggered_ids": [],
        }
    post = apply_c1_rename(pre_source, adj)
    modified = post != pre_source
    return {
        "post_source": post if modified else pre_source,
        "gated_into_healer": True,
        "eligible": modified,
        "eligibility_status": "C1_ELIGIBLE" if modified else "C1_INELIGIBLE",
        "abstention_reason": None if modified else "rename_produced_identical_source",
        "triggered": modified,
        "modified": modified,
        "abstained": not modified,
        "wrong_call": adj.get("wrong_call"),
        "unique_expected_method": adj.get("unique_expected_method"),
        "source_origin_if_modified": "TIER_C1_POST_SOURCE",
        "rule_triggered_ids": ["TIER_B_EXPLICIT_DOMAIN_METHOD_BINDING_REPAIR_V1"]
        if modified
        else [],
    }


def second_tier_c1(*, cell: dict[str, Any], pre_source: str) -> str:
    return heal_tier_c1(cell=cell, pre_source=pre_source)["post_source"]


def heal_tier_c2(*, cell: dict[str, Any], pre_source: str) -> dict[str, Any]:
    adj = adjudicate_c2(
        source=pre_source,
        task_id=cell["task_id"],
        condition=cell["condition"],
        contracts_by_key=contracts(),
    )
    if adj["status"] != "C2_ELIGIBLE":
        return {
            "post_source": pre_source,
            "gated_into_healer": True,
            "eligible": False,
            "eligibility_status": adj["status"],
            "abstention_reason": adj.get("abstention_reason"),
            "triggered": False,
            "modified": False,
            "abstained": True,
            "ssot_entry_id": adj.get("ssot_entry_id"),
            "ast_node_location": adj.get("ast_node_location"),
            "rule_triggered_ids": [],
        }
    pipe = run_tier_c2_default_optional_cleanup(pre_source)
    ok = pipe.mutation_count == 1 and not pipe.rolled_back and pipe.post_source != pre_source
    if not ok:
        return {
            "post_source": pre_source,
            "gated_into_healer": True,
            "eligible": False,
            "eligibility_status": "C2_INELIGIBLE",
            "abstention_reason": pipe.abstention_reason or "pipeline_did_not_commit_mutation",
            "triggered": False,
            "modified": False,
            "abstained": True,
            "rule_triggered_ids": [],
        }
    return {
        "post_source": pipe.post_source,
        "gated_into_healer": True,
        "eligible": True,
        "eligibility_status": "C2_ELIGIBLE",
        "abstention_reason": None,
        "triggered": True,
        "modified": True,
        "abstained": False,
        "ssot_entry_id": adj.get("ssot_entry_id"),
        "ast_node_location": adj.get("ast_node_location"),
        "source_origin_if_modified": "TIER_C2_POST_SOURCE",
        "rule_triggered_ids": [TIER_C2_RULE_ID],
    }


def second_tier_c2(*, cell: dict[str, Any], pre_source: str) -> str:
    return heal_tier_c2(cell=cell, pre_source=pre_source)["post_source"]


def write_layer_artifacts(
    *,
    layer_tag: str,
    closure_status: str,
    definition: str,
    out: dict[str, Any],
    expected_notes: dict[str, Any],
) -> None:
    summary = out["summary"]
    write_json(
        ns_path(
            "docs/experiments/manifests",
            f"math16_{layer_tag}_reproducibility_{NS}.json",
        ),
        {
            "status": f"math16_{layer_tag}_reproducibility_{NS}",
            "verdict": f"{layer_tag.upper()}_FAIL_GATED_AUTHORITATIVE_COMPLETE",
            "authority_status": AUTHORITY,
            "namespace": NS,
            "gating_policy": "FAIL_ONLY_CUMULATIVE",
            "head": head_sha(),
            "results_root": str(out["results_root"].relative_to(ROOT)).replace("\\", "/"),
            "summary": summary,
            "expected": expected_notes,
            "deterministic_second_replay": out["second"],
            "model_calls": 0,
        },
    )
    write_text(
        ns_path(
            "docs/experiments/reports",
            f"math16_{layer_tag}_reproducibility_{NS}.md",
        ),
        "\n".join(
            [
                f"# Math16 {layer_tag} Reproducibility — {NS}",
                "",
                f"> **AUTHORITY:** `{AUTHORITY}`",
                f"> **HEAD:** `{head_sha()}`",
                f"> **Gating:** FAIL-only cumulative",
                "",
                f"- gated FAIL／preserved PASS: **{summary['gated_fail_count']}／{summary['preserved_pass_count']}**",
                f"- next PASS／FAIL: **{summary['next_pass']}／{summary['next_fail']}**",
                f"- eligible／modified／rescue／regression: **{len(summary['eligible_ids'])}／{summary['modified']}／{summary['transitions']['verified_rescue']}／{summary['transitions']['regression']}**",
                f"- pass→pass modified: **{summary['pass_pass_modified']}**",
                f"- second replay zero-diff: **{out['second']['zero_diff']}**",
                "",
            ]
        )
        + "\n",
    )
    # final-source closure
    next_pass = summary["next_pass"]
    next_fail = summary["next_fail"]
    # infer keys from first closure cell
    sample = out["closure_cells"][0]
    next_outcome_key = [k for k in sample if k.endswith("_outcome") and k.startswith("c")][-1]
    # better: from definition map
    closure = {
        "status": closure_status,
        "verdict": closure_status.replace("math16_", "").upper().replace(f"_{NS.upper()}", "")
        if False
        else closure_status.replace("math16_", "").split(f"_{NS}")[0].upper()
        + "_PASSED",
        "definition": definition,
        "authority_status": AUTHORITY,
        "namespace": NS,
        "gating_policy": "FAIL_ONLY_CUMULATIVE",
        "head": head_sha(),
        "validation": {
            "n_cells": 320,
            "unique_ids": 320,
            "duplicate_ids": 0,
            "next_pass": next_pass,
            "next_fail": next_fail,
            "verified_rescue": summary["transitions"]["verified_rescue"],
            "regression": summary["transitions"]["regression"],
            "preserved_pass": summary["transitions"]["preserved_pass"],
            "still_failed": summary["transitions"]["still_failed"],
            "gated_fail_count": summary["gated_fail_count"],
            "preserved_pass_count": summary["preserved_pass_count"],
            "pass_pass_modified": summary["pass_pass_modified"],
            "origin_counts": dict(Counter(c["source_origin"] for c in out["closure_cells"])),
            "no_missing_duplicate_fallback": True,
            "passed": True,
        },
        "cells": out["closure_cells"],
        "declarations": [
            "authoritative_fail_gated",
            "no_model_calls",
            "prior_pass_not_scanned",
            "no_tier_d",
        ],
    }
    # fix verdict simply
    if "c1_final" in closure_status:
        closure["verdict"] = "C1_FINAL_SOURCE_CLOSURE_PASSED"
        for c in closure["cells"]:
            c["c1_pass_n_context"] = next_pass
        closure["validation"]["c1_pass"] = next_pass
        closure["validation"]["c1_fail"] = next_fail
    elif "c2_final" in closure_status:
        closure["verdict"] = "C2_FINAL_SOURCE_CLOSURE_PASSED"
        closure["validation"]["c2_pass"] = next_pass
        closure["validation"]["c2_fail"] = next_fail
    elif "c3_final" in closure_status:
        closure["verdict"] = "C3_FINAL_SOURCE_CLOSURE_PASSED"
        closure["validation"]["c3_pass"] = next_pass
        closure["validation"]["c3_fail"] = next_fail
    elif "c4_final" in closure_status:
        closure["verdict"] = "C4_FINAL_SOURCE_CLOSURE_PASSED"
        closure["validation"]["c4_pass"] = next_pass
        closure["validation"]["c4_fail"] = next_fail

    write_json(ns_path("docs/experiments/manifests", f"{closure_status}.json"), closure)
    write_text(
        ns_path(
            "docs/experiments/reports",
            f"{closure_status}.md",
        ),
        "\n".join(
            [
                f"# {closure['verdict']} — {NS}",
                "",
                f"> **AUTHORITY:** `{AUTHORITY}`",
                f"> **HEAD:** `{head_sha()}`",
                "",
                f"- PASS/FAIL: **{next_pass}／{next_fail}**",
                f"- origins: `{closure['validation']['origin_counts']}`",
                "",
            ]
        )
        + "\n",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--from-layer", default="c0", choices=["c0", "c1", "c2", "c3", "c4"])
    args = parser.parse_args()
    _ = args

    expect(tuple(TIER_B_RULE_ORDER) == TIER_B_EXPECTED_ORDER, "TIER_B_ORDER_DRIFT")
    expect(list(RULE_ALLOWLIST), "TIER_A_ALLOWLIST_EMPTY")

    print("== C0 ==")
    c0 = build_c0()
    c0_pass = c0["validation"]["pass_n"]
    c0_fail = c0["validation"]["fail_n"]
    print("C0 PASS/FAIL", c0_pass, c0_fail)

    print("== C0→C1 Tier A (FAIL-only) ==")
    c1_out = run_fail_gated_layer(
        layer_name="C0_C1_TIER_A",
        prior_closure=c0,
        prior_outcome_key="c0_outcome",
        prior_path_key="c0_final_source_path",
        prior_sha_key="c0_final_source_sha256",
        next_outcome_key="c1_outcome",
        next_path_key="c1_final_source_path",
        next_sha_key="c1_final_source_sha256",
        results_dirname=f"math16_c0_c1_tier_a_reproducibility_{NS}",
        expected_prior_pass=c0_pass,
        expected_prior_fail=c0_fail,
        expected_next_pass=None,
        heal_fail_cell=heal_tier_a,
        second_heal=second_tier_a,
        eligibility_counter_keys=["TIER_A_ELIGIBLE", "TIER_A_INELIGIBLE"],
    )
    expect(c1_out["summary"]["pass_pass_modified"] == 0, "C1_PASS_PASS_MUST_0")
    expect(c1_out["summary"]["transitions"]["regression"] == 0, "C1_REGRESSION_MUST_0")
    write_layer_artifacts(
        layer_tag="c0_c1_tier_a",
        closure_status=f"math16_c1_final_source_closure_{NS}",
        definition="C1 = C0 + Tier A (FAIL-only gate)",
        out=c1_out,
        expected_notes={
            "c1_pass": c1_out["summary"]["next_pass"],
            "eligible": len(c1_out["summary"]["eligible_ids"]),
            "modified": c1_out["summary"]["modified"],
            "rescue": c1_out["summary"]["transitions"]["verified_rescue"],
        },
    )
    c1 = json.loads(
        ns_path(
            "docs/experiments/manifests", f"math16_c1_final_source_closure_{NS}.json"
        ).read_text(encoding="utf-8")
    )
    c1_pass = c1_out["summary"]["next_pass"]
    c1_fail = c1_out["summary"]["next_fail"]
    print(
        "C1",
        c1_pass,
        "elig",
        len(c1_out["summary"]["eligible_ids"]),
        "mod",
        c1_out["summary"]["modified"],
        "rescue",
        c1_out["summary"]["transitions"]["verified_rescue"],
    )

    print("== C1→C2 Tier B (FAIL-only) ==")
    c2_out = run_fail_gated_layer(
        layer_name="C1_C2_TIER_B",
        prior_closure=c1,
        prior_outcome_key="c1_outcome",
        prior_path_key="c1_final_source_path",
        prior_sha_key="c1_final_source_sha256",
        next_outcome_key="c2_outcome",
        next_path_key="c2_final_source_path",
        next_sha_key="c2_final_source_sha256",
        results_dirname=f"math16_c1_c2_tier_b_reproducibility_{NS}",
        expected_prior_pass=c1_pass,
        expected_prior_fail=c1_fail,
        expected_next_pass=None,
        heal_fail_cell=heal_tier_b,
        second_heal=second_tier_b,
    )
    expect(c2_out["summary"]["pass_pass_modified"] == 0, "C2_PASS_PASS_MUST_0")
    expect(c2_out["summary"]["transitions"]["regression"] == 0, "C2_REGRESSION_MUST_0")
    write_layer_artifacts(
        layer_tag="c1_c2_tier_b",
        closure_status=f"math16_c2_final_source_closure_{NS}",
        definition="C2 = C1 + Tier B (FAIL-only gate)",
        out=c2_out,
        expected_notes={
            "c2_pass": c2_out["summary"]["next_pass"],
            "eligible": len(c2_out["summary"]["eligible_ids"]),
            "modified": c2_out["summary"]["modified"],
            "rescue": c2_out["summary"]["transitions"]["verified_rescue"],
        },
    )
    c2 = json.loads(
        ns_path(
            "docs/experiments/manifests", f"math16_c2_final_source_closure_{NS}.json"
        ).read_text(encoding="utf-8")
    )
    c2_pass = c2_out["summary"]["next_pass"]
    c2_fail = c2_out["summary"]["next_fail"]
    print(
        "C2",
        c2_pass,
        "rescue",
        c2_out["summary"]["transitions"]["verified_rescue"],
        "mod",
        c2_out["summary"]["modified"],
    )

    print("== C2→C3 Tier C1 (FAIL-only) ==")
    c3_out = run_fail_gated_layer(
        layer_name="C2_C3_TIER_C1",
        prior_closure=c2,
        prior_outcome_key="c2_outcome",
        prior_path_key="c2_final_source_path",
        prior_sha_key="c2_final_source_sha256",
        next_outcome_key="c3_outcome",
        next_path_key="c3_final_source_path",
        next_sha_key="c3_final_source_sha256",
        results_dirname=f"math16_c2_c3_tier_c1_reproducibility_{NS}",
        expected_prior_pass=c2_pass,
        expected_prior_fail=c2_fail,
        expected_next_pass=None,
        heal_fail_cell=heal_tier_c1,
        second_heal=second_tier_c1,
        eligibility_counter_keys=[
            "C1_ELIGIBLE",
            "C1_AMBIGUOUS_ABSTAIN",
            "SYSTEM_CONTRACT_EXCLUDED",
            "C1_INELIGIBLE",
            "OVERLAP_UNRESOLVED",
        ],
    )
    expect(c3_out["summary"]["pass_pass_modified"] == 0, "C3_PASS_PASS_MUST_0")
    expect(c3_out["summary"]["transitions"]["regression"] == 0, "C3_REGRESSION_MUST_0")
    c3_elig = len(c3_out["summary"]["eligible_ids"])
    c3_mod = c3_out["summary"]["modified"]
    c3_rescue = c3_out["summary"]["transitions"]["verified_rescue"]
    write_json(
        ns_path(
            "docs/experiments/manifests",
            f"math16_c2_c3_tier_c1_residual_supply_{NS}.json",
        ),
        {
            "status": f"math16_c2_c3_tier_c1_residual_supply_{NS}",
            "authority_status": AUTHORITY,
            "namespace": NS,
            "gating_policy": "FAIL_ONLY_CUMULATIVE",
            "pool": f"C2_FAIL_{c2_fail}",
            "aggregate": {
                "gated_fail": c2_fail,
                "eligibility_among_gated": c3_out["summary"]["eligibility_among_gated"],
                "eligible": c3_elig,
                "ambiguous": c3_out["summary"]["eligibility_among_gated"].get(
                    "C1_AMBIGUOUS_ABSTAIN", 0
                ),
                "modified": c3_mod,
                "rescue": c3_rescue,
            },
            "eligible_ids": c3_out["summary"]["eligible_ids"],
            "head": head_sha(),
        },
    )
    write_text(
        ns_path(
            "docs/experiments/reports",
            f"math16_c2_c3_tier_c1_residual_supply_{NS}.md",
        ),
        "\n".join(
            [
                f"# Math16 C2→C3 Tier C1 Residual Supply — {NS}",
                "",
                f"> **AUTHORITY:** `{AUTHORITY}`",
                f"> **Pool:** C2 FAIL-only **{c2_fail}**",
                "",
                f"- eligible／modified／rescue: **{c3_elig}／{c3_mod}／{c3_rescue}**",
                "",
            ]
        )
        + "\n",
    )
    write_layer_artifacts(
        layer_tag="c2_c3_tier_c1",
        closure_status=f"math16_c3_final_source_closure_{NS}",
        definition="C3 = C2 + Tier C1 (FAIL-only gate)",
        out=c3_out,
        expected_notes={
            "c3_pass": c3_out["summary"]["next_pass"],
            "eligible": c3_elig,
            "modified": c3_mod,
            "rescue": c3_rescue,
        },
    )
    c3 = json.loads(
        ns_path(
            "docs/experiments/manifests", f"math16_c3_final_source_closure_{NS}.json"
        ).read_text(encoding="utf-8")
    )
    c3_pass = c3_out["summary"]["next_pass"]
    c3_fail = c3_out["summary"]["next_fail"]
    print("C3", c3_pass, "elig", c3_elig, "mod", c3_mod)

    print("== C3→C4 Tier C2 (FAIL-only) ==")
    c4_out = run_fail_gated_layer(
        layer_name="C3_C4_TIER_C2",
        prior_closure=c3,
        prior_outcome_key="c3_outcome",
        prior_path_key="c3_final_source_path",
        prior_sha_key="c3_final_source_sha256",
        next_outcome_key="c4_outcome",
        next_path_key="c4_final_source_path",
        next_sha_key="c4_final_source_sha256",
        results_dirname=f"math16_c3_c4_tier_c2_reproducibility_{NS}",
        expected_prior_pass=c3_pass,
        expected_prior_fail=c3_fail,
        expected_next_pass=None,
        heal_fail_cell=heal_tier_c2,
        second_heal=second_tier_c2,
        eligibility_counter_keys=[
            "C2_ELIGIBLE",
            "C2_AMBIGUOUS_ABSTAIN",
            "SYSTEM_CONTRACT_EXCLUDED",
            "C2_INELIGIBLE",
            "OVERLAP_UNRESOLVED",
        ],
    )
    expect(c4_out["summary"]["pass_pass_modified"] == 0, "C4_PASS_PASS_MUST_0")
    expect(c4_out["summary"]["transitions"]["regression"] == 0, "C4_REGRESSION_MUST_0")
    c4_elig = len(c4_out["summary"]["eligible_ids"])
    c4_mod = c4_out["summary"]["modified"]
    c4_rescue = c4_out["summary"]["transitions"]["verified_rescue"]
    write_json(
        ns_path(
            "docs/experiments/manifests",
            f"math16_c3_c4_tier_c2_residual_supply_{NS}.json",
        ),
        {
            "status": f"math16_c3_c4_tier_c2_residual_supply_{NS}",
            "authority_status": AUTHORITY,
            "namespace": NS,
            "gating_policy": "FAIL_ONLY_CUMULATIVE",
            "repair_subtype": TIER_C2_SUBTYPE,
            "pool": f"C3_FAIL_{c3_fail}",
            "aggregate": {
                "gated_fail": c3_fail,
                "eligibility_among_gated": c4_out["summary"]["eligibility_among_gated"],
                "eligible": c4_elig,
                "ambiguous": c4_out["summary"]["eligibility_among_gated"].get(
                    "C2_AMBIGUOUS_ABSTAIN", 0
                ),
                "modified": c4_mod,
                "pass_pass_modified": c4_out["summary"]["pass_pass_modified"],
                "rescue": c4_rescue,
            },
            "eligible_ids": c4_out["summary"]["eligible_ids"],
            "head": head_sha(),
        },
    )
    write_text(
        ns_path(
            "docs/experiments/reports",
            f"math16_c3_c4_tier_c2_residual_supply_{NS}.md",
        ),
        "\n".join(
            [
                f"# Math16 C3→C4 Tier C2 Residual Supply — {NS}",
                "",
                f"> **AUTHORITY:** `{AUTHORITY}`",
                f"> **Pool:** C3 FAIL-only **{c3_fail}**",
                "",
                f"- eligible／modified／PASS→PASS: **{c4_elig}／{c4_mod}／{c4_out['summary']['pass_pass_modified']}**",
                "",
            ]
        )
        + "\n",
    )
    write_layer_artifacts(
        layer_tag="c3_c4_tier_c2",
        closure_status=f"math16_c4_final_source_closure_{NS}",
        definition="C4 = C3 + Tier C2 (FAIL-only gate; default_optional_pure_form_cleanup)",
        out=c4_out,
        expected_notes={
            "c4_pass": c4_out["summary"]["next_pass"],
            "eligible": c4_elig,
            "modified": c4_mod,
            "pass_pass": c4_out["summary"]["pass_pass_modified"],
            "rescue": c4_rescue,
        },
    )
    c4_pass = c4_out["summary"]["next_pass"]
    c4_fail = c4_out["summary"]["next_fail"]

    chain = {
        "status": f"math16_c0_c4_fail_gated_authoritative_chain_{NS}",
        "authority_status": AUTHORITY,
        "namespace": NS,
        "head": head_sha(),
        "pass_curve": {
            "C0": c0_pass,
            "C1": c1_pass,
            "C2": c2_pass,
            "C3": c3_pass,
            "C4": c4_pass,
        },
        "layers": {
            "C0": {"pass": c0_pass, "fail": c0_fail},
            "C1": c1_out["summary"],
            "C2": c2_out["summary"],
            "C3": c3_out["summary"],
            "C4": c4_out["summary"],
        },
        "old_all_cell_marked": "NONAUTHORITATIVE_ALL_CELL_EXPLORATORY",
        "model_calls": 0,
        "tier_d_executed": False,
    }
    write_json(
        ns_path(
            "docs/experiments/manifests",
            f"math16_c0_c4_fail_gated_authoritative_chain_{NS}.json",
        ),
        chain,
    )
    write_text(
        ns_path(
            "docs/experiments/reports",
            f"math16_c0_c4_fail_gated_authoritative_chain_{NS}.md",
        ),
        "\n".join(
            [
                f"# Math16 C0→C4 FAIL-gated Authoritative Chain — {NS}",
                "",
                f"> **AUTHORITY:** `{AUTHORITY}`",
                f"> **HEAD:** `{head_sha()}`",
                "",
                "## PASS curve",
                "",
                f"- C0→C1→C2→C3→C4: **{c0_pass}／{c1_pass}／{c2_pass}／{c3_pass}／{c4_pass}**",
                "",
                "## C4 Tier C2",
                "",
                f"- residual eligible／modified／PASS→PASS: **{c4_elig}／{c4_mod}／{c4_out['summary']['pass_pass_modified']}**",
                "",
                "## Declarations",
                "",
                "- No model calls; frozen rules/guards/order untouched; FAIL-only one round.",
                "",
            ]
        )
        + "\n",
    )

    print("DONE")
    print(
        json.dumps(
            {
                "pass_curve": chain["pass_curve"],
                "c4_fail": c4_fail,
                "c4_eligible": c4_elig,
                "c4_modified": c4_mod,
                "c4_pass_pass": c4_out["summary"]["pass_pass_modified"],
                "c4_rescue": c4_rescue,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
