# -*- coding: utf-8 -*-
"""Evaluate q02 ab2d_spec_v2 patch (2 cells) and recompute global Ab2d+spec hybrid."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.evaluate_math16_pilot02_full_v4 import classify_outcome_to_v3

PLAN_PATH = ROOT / "docs/experiments/manifests/math16_pilot02_ab2d_spec_v2_q02_patch_plan.json"
V4_BASELINE = (
    ROOT / "docs/experiments/results/math16_pilot02_full_evaluation_v4_r001/cell_level_baseline.jsonl"
)
PREV_V2_EVAL = (
    ROOT / "docs/experiments/results/math16_pilot02_ab2d_spec_v2_evaluation_r001/summary.json"
)
PREV_V2_CELLS = (
    ROOT / "docs/experiments/results/math16_pilot02_ab2d_spec_v2_evaluation_r001/cell_level_baseline.jsonl"
)
OUT_DIR = ROOT / "docs/experiments/results/math16_pilot02_ab2d_spec_v2_q02_patch_evaluation_r001"
TASK_ID = "ce111_q02_polynomial_division_remainder"
SEEDS = [2026071301, 2026072003]
GAP_SUSPECTED = [
    "ce112_q04_radical_simplification",
    "ce115_calc_radical_simplification_l1",
    "ce111_q05_exact_fraction_expression",
    "ce112_q12_independent_probability_fraction",
    "ce113_q01_negative_fraction_subtraction",
    "ce115_calc_exact_rational_expression_l1",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true", required=True)
    parser.parse_args()

    from agent_tools.finals_rebuild.math16_pool import frozen_for_prompt, tasks_by_id
    from scripts.run_math16_latex_v1_gemini_live import classify_math16_response

    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    assert len(plan) == 2
    tasks = tasks_by_id()
    task = tasks[TASK_ID]
    frozen = frozen_for_prompt(task)

    v4_all = [json.loads(l) for l in V4_BASELINE.read_text(encoding="utf-8").splitlines()]
    v4_q02 = {
        (r["task_id"], int(r["seed"])): r
        for r in v4_all
        if r["condition"] == "ab2d_spec" and r["task_id"] == TASK_ID
    }

    rows = []
    for cell in plan:
        seed = int(cell["seed"])
        cell_dir = ROOT / "docs/experiments/results" / cell["output_relative_path"]
        raw = (cell_dir / "raw_response.txt").read_text(encoding="utf-8")
        art = json.loads((cell_dir / "artifact.json").read_text(encoding="utf-8"))
        assert art.get("persisted_complete") is True
        assert art.get("prompt_sha256") == cell["prompt_sha256"]
        outcome, _src, details = classify_math16_response(
            raw,
            frozen_params=frozen["oracle_payload"],
            audit_oracle_payload=task["oracle_payload"],
            task=task,
        )
        mapped = classify_outcome_to_v3(outcome, details, api_policy="API-only")
        v1 = v4_q02[(TASK_ID, seed)]
        rows.append(
            {
                "cell_id": cell["cell_id"],
                "task_id": TASK_ID,
                "seed": seed,
                "condition": "ab2d_spec_v2",
                "final_status": mapped["final_status"],
                "primary_failure_layer": mapped["primary_failure_layer"],
                "exception_class": mapped.get("exception_class"),
                "exception_message": mapped.get("exception_message"),
                "v1_final_status": v1["final_status"],
                "v1_primary_failure_layer": v1.get("primary_failure_layer"),
                "v1_exception_message": v1.get("exception_message"),
                "changed_vs_v1": (v1["final_status"] == "PASSED")
                != (mapped["final_status"] == "PASSED"),
                "prompt_sha256": cell["prompt_sha256"],
                "raw_response_hash": hashlib.sha256(raw.encode("utf-8")).hexdigest(),
            }
        )

    # Hybrid: start from previous v2 hybrid (78/80), replace q02's 2 failing seeds
    prev = json.loads(PREV_V2_EVAL.read_text(encoding="utf-8"))
    prev_hybrid = prev["global_recompute"]["ab2d_spec_hybrid_v2_replace_pass_per_80"]
    # Previous hybrid already replaced Fraction×3 + q08 but NOT q02.
    # q02 under v1 ab2d_spec: 3/5 pass (2 L3 fail). Replacing those 2 fails with v2 results:
    q02_v1_pass_all5 = sum(
        1
        for s in [2026071301, 2026072001, 2026072002, 2026072003, 2026072004]
        if v4_q02[(TASK_ID, s)]["final_status"] == "PASSED"
    )
    q02_v2_pass_patched2 = sum(1 for r in rows if r["final_status"] == "PASSED")
    # For hybrid accounting: remove v1 outcomes for the 2 patched seeds and add v2
    delta = 0
    for r in rows:
        v1_pass = r["v1_final_status"] == "PASSED"
        v2_pass = r["final_status"] == "PASSED"
        if (not v1_pass) and v2_pass:
            delta += 1
        elif v1_pass and (not v2_pass):
            delta -= 1
    hybrid80 = prev_hybrid + delta
    ab2d_api = prev["global_recompute"]["ab2d_api_pass_per_80"]
    overall_prev = prev["global_recompute"]["overall_hybrid_pass_per_320"]
    overall = overall_prev + delta

    # GAP_SUSPECTED recheck using v4 + note that q02 patch is L3 API, not latex schema
    gap_status = {}
    for tid in GAP_SUSPECTED:
        sub = [r for r in v4_all if r["task_id"] == tid]
        gap_status[tid] = {
            "v4_pass": f"{sum(1 for r in sub if r['final_status']=='PASSED')}/20",
            "affected_by_q02_patch": False,
            "note": "schema latex coupling already structural-judge in v4; q02 patch is L3 API signature only",
        }

    # Remaining known ab2d_spec gaps after this patch?
    # Rebuild full ab2d_spec hybrid pass map
    prev_cells = [
        json.loads(l) for l in PREV_V2_CELLS.read_text(encoding="utf-8").splitlines()
    ]
    replaced = {(r["task_id"], int(r["seed"])): r for r in prev_cells}
    for r in rows:
        replaced[(r["task_id"], r["seed"])] = r

    remaining_fails = []
    for r in v4_all:
        if r["condition"] != "ab2d_spec":
            continue
        key = (r["task_id"], int(r["seed"]))
        if key in replaced:
            status = replaced[key]["final_status"]
            layer = replaced[key].get("primary_failure_layer")
            exc = replaced[key].get("exception_message")
        else:
            status = r["final_status"]
            layer = r.get("primary_failure_layer")
            exc = r.get("exception_message")
        if status != "PASSED":
            remaining_fails.append(
                {
                    "task_id": r["task_id"],
                    "seed": r["seed"],
                    "layer": layer,
                    "exception_message": (exc or "")[:120],
                }
            )

    summary = {
        "evaluation_id": "math16_pilot02_ab2d_spec_v2_q02_patch_evaluation_r001",
        "llm_calls": 0,
        "api_cost_usd": 0.0,
        "cells": 2,
        "q02_seed_compare": [
            {
                "task": TASK_ID,
                "seed": r["seed"],
                "v1_ab2d_spec": f"{r['v1_final_status']}/{r['v1_primary_failure_layer']}",
                "v2_ab2d_spec_v2": f"{r['final_status']}/{r['primary_failure_layer']}",
                "exception_v1": r.get("v1_exception_message"),
                "exception_v2": r.get("exception_message"),
            }
            for r in rows
        ],
        "q02_v1_pass_all5": f"{q02_v1_pass_all5}/5",
        "q02_v2_patched2_pass": f"{q02_v2_pass_patched2}/2",
        "global_recompute": {
            "ab2d_spec_prev_hybrid_pass_per_80": prev_hybrid,
            "ab2d_spec_hybrid_after_q02_pass_per_80": hybrid80,
            "ab2d_api_pass_per_80": ab2d_api,
            "gap_hybrid_vs_api": hybrid80 - ab2d_api,
            "overall_prev_hybrid_per_320": overall_prev,
            "overall_after_q02_per_320": overall,
            "delta_from_q02_patch": delta,
        },
        "gap_suspected_recheck": gap_status,
        "remaining_ab2d_spec_failures_after_hybrid": remaining_fails,
        "created_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "cell_level_baseline.jsonl").write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8"
    )
    (OUT_DIR / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    md = [
        "# Ab2d+spec-v2 q02 patch evaluation",
        "",
        "| task | seed | v1(ab2d_spec) | v2(ab2d_spec_v2) | 說明 |",
        "| :--- | ---: | :--- | :--- | :--- |",
    ]
    for r in rows:
        note = "to_latex L3 → format_latex card" if r["changed_vs_v1"] else "unchanged"
        md.append(
            f"| `{TASK_ID}` | {r['seed']} | {r['v1_final_status']} ({r['v1_primary_failure_layer']}) | "
            f"{r['final_status']} ({r['primary_failure_layer']}) | {note} |"
        )
    md.extend(
        [
            "",
            f"- Ab2d+spec hybrid: `{prev_hybrid}/80` → `{hybrid80}/80`",
            f"- vs Ab2d+api `{ab2d_api}/80`: gap `{hybrid80 - ab2d_api}`",
            f"- Overall: `{overall_prev}/320` → `{overall}/320`",
            "",
            "AB2D_SPEC_V2_FULL_COMPARISON_FINAL",
            "",
        ]
    )
    (OUT_DIR / "report.md").write_text("\n".join(md), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
