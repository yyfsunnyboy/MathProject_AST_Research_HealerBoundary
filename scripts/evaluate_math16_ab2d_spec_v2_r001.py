# -*- coding: utf-8 -*-
"""Evaluate Ab2d+spec-v2 20 cells with post-schema-normalize (v4) oracles.

Independent revision: ab2d_spec_v2_evaluation_r001
Does not overwrite v3_r001 / v4_r001 / audit V1 / ab2d_spec v1.
Zero LLM calls.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.evaluate_math16_pilot02_full_v4 import (  # noqa: E402
    classify_outcome_to_v3,
    _empty_layer_counter,
)

SPEC_V1_MANIFEST = ROOT / "docs/experiments/prompts/ab2d_spec/manifest.json"
PLAN_PATH = ROOT / "docs/experiments/manifests/math16_pilot02_ab2d_spec_v2_generation_plan.json"
V4_BASELINE = (
    ROOT / "docs/experiments/results/math16_pilot02_full_evaluation_v4_r001/cell_level_baseline.jsonl"
)
OUT_DIR = ROOT / "docs/experiments/results/math16_pilot02_ab2d_spec_v2_evaluation_r001"
EVAL_ID = "math16_pilot02_ab2d_spec_v2_evaluation_r001"
TASK_ORDER = [
    "ce111_q05_exact_fraction_expression",
    "ce112_q12_independent_probability_fraction",
    "ce113_q01_negative_fraction_subtraction",
    "ce111_q08_polynomial_factor_parameter_recovery",
]
SEEDS = [2026071301, 2026072001, 2026072002, 2026072003, 2026072004]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true", required=True)
    parser.parse_args()

    from agent_tools.finals_rebuild.math16_pool import frozen_for_prompt, tasks_by_id
    from scripts.run_math16_latex_v1_gemini_live import classify_math16_response, extract_code

    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    if len(plan) != 20:
        raise ValueError("expected 20-cell plan")

    spec_v1 = json.loads(SPEC_V1_MANIFEST.read_text(encoding="utf-8"))
    family_map = {t["task_id"]: t["family"] for t in spec_v1["tasks"]}
    api_map = {t["task_id"]: t["api_policy"] for t in spec_v1["tasks"]}
    tasks = tasks_by_id()

    v4_index: dict[tuple[str, int], dict[str, Any]] = {}
    v4_all = [
        json.loads(line)
        for line in V4_BASELINE.read_text(encoding="utf-8").splitlines()
    ]
    for row in v4_all:
        if row["condition"] == "ab2d_spec" and row["task_id"] in set(TASK_ORDER):
            v4_index[(row["task_id"], int(row["seed"]))] = row

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    passed = 0

    for cell in plan:
        tid = cell["task_id"]
        seed = int(cell["seed"])
        cell_dir = ROOT / "docs/experiments/results" / cell["output_relative_path"]
        raw = (cell_dir / "raw_response.txt").read_text(encoding="utf-8")
        art = json.loads((cell_dir / "artifact.json").read_text(encoding="utf-8"))
        if art.get("persisted_complete") is not True:
            raise ValueError(f"incomplete cell {cell['cell_id']}")
        if art.get("prompt_sha256") != cell["prompt_sha256"]:
            raise ValueError(f"prompt sha mismatch {cell['cell_id']}")

        task = tasks[tid]
        frozen = frozen_for_prompt(task)
        outcome, _source, details = classify_math16_response(
            raw,
            frozen_params=frozen["oracle_payload"],
            audit_oracle_payload=task["oracle_payload"],
            task=task,
        )
        mapped = classify_outcome_to_v3(outcome, details, api_policy=api_map[tid])
        is_pass = mapped["final_status"] == "PASSED"
        if is_pass:
            passed += 1

        v1 = v4_index[(tid, seed)]
        extracted = extract_code(raw)
        rows.append(
            {
                "cell_id": cell["cell_id"],
                "task_id": tid,
                "family": family_map[tid],
                "condition": "ab2d_spec_v2",
                "condition_display": "Ab2d+spec-v2",
                "seed": seed,
                "evaluation_revision": "ab2d_spec_v2_evaluation_r001",
                "final_status": mapped["final_status"],
                "primary_failure_layer": mapped["primary_failure_layer"],
                "exception_class": mapped.get("exception_class"),
                "exception_message": mapped.get("exception_message"),
                "g4_correctness": mapped["gates"]["g4_correctness"],
                "classifier_outcome": mapped.get("classifier_outcome") or outcome,
                "v1_condition": "ab2d_spec",
                "v1_final_status": v1["final_status"],
                "v1_primary_failure_layer": v1.get("primary_failure_layer"),
                "v1_exception_message": v1.get("exception_message"),
                "changed_vs_v1_ab2d_spec": (v1["final_status"] == "PASSED") != is_pass,
                "prompt_sha256": cell["prompt_sha256"],
                "raw_response_hash": hashlib.sha256(raw.encode("utf-8")).hexdigest(),
                "candidate_present": bool(extracted.extracted_code),
            }
        )

    layers = _empty_layer_counter()
    for r in rows:
        if r["final_status"] != "PASSED":
            layers[r["primary_failure_layer"] or "L5"] += 1

    task_compare: dict[str, dict[str, Any]] = {}
    for tid in TASK_ORDER:
        v1_rows = [v4_index[(tid, s)] for s in SEEDS]
        v1_pass = sum(1 for r in v1_rows if r["final_status"] == "PASSED")
        v2_pass = sum(1 for r in rows if r["task_id"] == tid and r["final_status"] == "PASSED")
        task_compare[tid] = {
            "v1_ab2d_spec_pass": f"{v1_pass}/5",
            "v2_ab2d_spec_v2_pass": f"{v2_pass}/5",
            "delta": v2_pass - v1_pass,
        }

    replace_ids = set(TASK_ORDER)
    v2_by_key = {(r["task_id"], r["seed"]): r for r in rows}
    ab2d_spec_v1_pass = sum(
        1 for r in v4_all if r["condition"] == "ab2d_spec" and r["final_status"] == "PASSED"
    )
    ab2d_spec_hybrid_pass = 0
    for r in v4_all:
        if r["condition"] != "ab2d_spec":
            continue
        if r["task_id"] in replace_ids:
            status = v2_by_key[(r["task_id"], int(r["seed"]))]["final_status"]
        else:
            status = r["final_status"]
        if status == "PASSED":
            ab2d_spec_hybrid_pass += 1

    ab2d_api_pass = sum(
        1 for r in v4_all if r["condition"] == "ab2d" and r["final_status"] == "PASSED"
    )
    overall_v4 = sum(1 for r in v4_all if r["final_status"] == "PASSED")
    overall_hybrid = overall_v4 - ab2d_spec_v1_pass + ab2d_spec_hybrid_pass

    summary = {
        "evaluation_id": EVAL_ID,
        "llm_calls": 0,
        "api_cost_usd": 0.0,
        "cells": 20,
        "baseline_passed": passed,
        "baseline_pass_fraction": f"{passed}/20",
        "layer_counts": layers,
        "task_compare": task_compare,
        "global_recompute": {
            "ab2d_spec_v1_pass_per_80": ab2d_spec_v1_pass,
            "ab2d_spec_hybrid_v2_replace_pass_per_80": ab2d_spec_hybrid_pass,
            "ab2d_api_pass_per_80": ab2d_api_pass,
            "gap_v1_vs_api": ab2d_spec_v1_pass - ab2d_api_pass,
            "gap_hybrid_vs_api": ab2d_spec_hybrid_pass - ab2d_api_pass,
            "overall_v4_pass_per_320": overall_v4,
            "overall_hybrid_pass_per_320": overall_hybrid,
        },
        "created_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    (OUT_DIR / "cell_level_baseline.jsonl").write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n",
        encoding="utf-8",
    )
    (OUT_DIR / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    md = [
        "# Ab2d+spec-v2 Evaluation r001",
        "",
        "Offline re-score of 20 newly generated cells with schema-normalize (v4) oracles.",
        "",
        "- LLM calls: `0`",
        "- API cost: `$0.00`",
        f"- Pass: `{passed}/20`",
        "",
        "## Task v1 vs v2",
        "| task | v1(ab2d_spec) pass | v2(ab2d_spec_v2) pass | delta |",
        "| :--- | ---: | ---: | ---: |",
    ]
    for tid in TASK_ORDER:
        tc = task_compare[tid]
        md.append(
            f"| `{tid}` | {tc['v1_ab2d_spec_pass']} | {tc['v2_ab2d_spec_v2_pass']} | {tc['delta']:+d} |"
        )
    md.extend(
        [
            "",
            "## Global recompute (replace these 4 tasks' ab2d_spec cells)",
            f"- Ab2d+spec v1: `{ab2d_spec_v1_pass}/80`",
            f"- Ab2d+spec hybrid (v2 replace): `{ab2d_spec_hybrid_pass}/80`",
            f"- Ab2d+api: `{ab2d_api_pass}/80`",
            f"- Gap vs api (v1): `{ab2d_spec_v1_pass - ab2d_api_pass}`",
            f"- Gap vs api (hybrid): `{ab2d_spec_hybrid_pass - ab2d_api_pass}`",
            f"- Overall v4: `{overall_v4}/320` → hybrid `{overall_hybrid}/320`",
            "",
            "AB2D_SPEC_V1_V2_COMPARISON_READY",
            "",
        ]
    )
    (OUT_DIR / "report.md").write_text("\n".join(md), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print("AB2D_SPEC_V2_EVALUATION_COMPLETE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
