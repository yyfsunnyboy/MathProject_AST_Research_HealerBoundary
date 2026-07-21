# -*- coding: utf-8 -*-
"""Evaluate q02 purity 3 cells + verify all 5 seeds share frozen v2 prompt SHA."""
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

PLAN_PATH = ROOT / "docs/experiments/manifests/math16_pilot02_ab2d_spec_v2_q02_purity_plan.json"
V4_BASELINE = (
    ROOT / "docs/experiments/results/math16_pilot02_full_evaluation_v4_r001/cell_level_baseline.jsonl"
)
PREV_Q02_PATCH = (
    ROOT / "docs/experiments/results/math16_pilot02_ab2d_spec_v2_q02_patch_evaluation_r001/summary.json"
)
PREV_V2_CELLS = (
    ROOT / "docs/experiments/results/math16_pilot02_ab2d_spec_v2_evaluation_r001/cell_level_baseline.jsonl"
)
PREV_Q02_CELLS = (
    ROOT
    / "docs/experiments/results/math16_pilot02_ab2d_spec_v2_q02_patch_evaluation_r001/cell_level_baseline.jsonl"
)
CELLS_ROOT = ROOT / "docs/experiments/results/math16_pilot02_ab2d_spec_v2_gemini/cells"
OUT_DIR = ROOT / "docs/experiments/results/math16_pilot02_ab2d_spec_v2_q02_purity_evaluation_r001"
TASK_ID = "ce111_q02_polynomial_division_remainder"
CONDITION = "ab2d_spec_v2"
EXPECTED_PROMPT_SHA = "f9a51940b166e8613557d1490cf1a331467ffd95af8ca96617aeded15c78fb87"
ALL_SEEDS = [2026071301, 2026072001, 2026072002, 2026072003, 2026072004]
PURITY_SEEDS = [2026072001, 2026072002, 2026072004]


def sha_lf(path: Path) -> str:
    return hashlib.sha256(path.read_text(encoding="utf-8").replace("\r\n", "\n").encode()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true", required=True)
    parser.parse_args()

    from agent_tools.finals_rebuild.math16_pool import frozen_for_prompt, tasks_by_id

    from scripts.run_math16_latex_v1_gemini_live import classify_math16_response

    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    assert len(plan) == 3
    tasks = tasks_by_id()
    task = tasks[TASK_ID]
    frozen = frozen_for_prompt(task)

    v4_all = [json.loads(l) for l in V4_BASELINE.read_text(encoding="utf-8").splitlines()]
    v4_q02 = {
        int(r["seed"]): r
        for r in v4_all
        if r["condition"] == "ab2d_spec" and r["task_id"] == TASK_ID
    }

    purity_rows = []
    for cell in plan:
        seed = int(cell["seed"])
        cell_dir = ROOT / "docs/experiments/results" / cell["output_relative_path"]
        raw = (cell_dir / "raw_response.txt").read_text(encoding="utf-8")
        art = json.loads((cell_dir / "artifact.json").read_text(encoding="utf-8"))
        assert art["prompt_sha256"] == EXPECTED_PROMPT_SHA
        assert sha_lf(cell_dir / "prompt.txt") == EXPECTED_PROMPT_SHA
        outcome, _s, details = classify_math16_response(
            raw,
            frozen_params=frozen["oracle_payload"],
            audit_oracle_payload=task["oracle_payload"],
            task=task,
        )
        mapped = classify_outcome_to_v3(outcome, details, api_policy="API-only")
        v1 = v4_q02[seed]
        v1_pass = v1["final_status"] == "PASSED"
        v2_pass = mapped["final_status"] == "PASSED"
        purity_rows.append(
            {
                "seed": seed,
                "v1_status": v1["final_status"],
                "v1_layer": v1.get("primary_failure_layer"),
                "v2_status": mapped["final_status"],
                "v2_layer": mapped["primary_failure_layer"],
                "consistent_with_v1": v1_pass == v2_pass,
                "prompt_sha256": art["prompt_sha256"],
                "exception_v1": v1.get("exception_message"),
                "exception_v2": mapped.get("exception_message"),
            }
        )

    # All 5 seeds SHA purity table
    sha_table = []
    for seed in ALL_SEEDS:
        d = CELLS_ROOT / f"gemini_3_5_flash__{TASK_ID}__{CONDITION}__seed_{seed}"
        art = json.loads((d / "artifact.json").read_text(encoding="utf-8"))
        file_sha = sha_lf(d / "prompt.txt")
        sha_table.append(
            {
                "seed": seed,
                "artifact_prompt_sha256": art["prompt_sha256"],
                "prompt_file_sha256": file_sha,
                "matches_frozen_v2": art["prompt_sha256"] == EXPECTED_PROMPT_SHA
                and file_sha == EXPECTED_PROMPT_SHA,
            }
        )
    assert all(r["matches_frozen_v2"] for r in sha_table)

    # Score all 5 q02 v2 cells
    q02_v2_pass = 0
    q02_v2_detail = []
    for seed in ALL_SEEDS:
        d = CELLS_ROOT / f"gemini_3_5_flash__{TASK_ID}__{CONDITION}__seed_{seed}"
        raw = (d / "raw_response.txt").read_text(encoding="utf-8")
        outcome, _s, details = classify_math16_response(
            raw,
            frozen_params=frozen["oracle_payload"],
            audit_oracle_payload=task["oracle_payload"],
            task=task,
        )
        mapped = classify_outcome_to_v3(outcome, details, api_policy="API-only")
        ok = mapped["final_status"] == "PASSED"
        if ok:
            q02_v2_pass += 1
        q02_v2_detail.append(
            {
                "seed": seed,
                "v2_status": mapped["final_status"],
                "v1_status": v4_q02[seed]["final_status"],
                "consistent": (mapped["final_status"] == "PASSED")
                == (v4_q02[seed]["final_status"] == "PASSED"),
            }
        )

    prev = json.loads(PREV_Q02_PATCH.read_text(encoding="utf-8"))
    prev_hybrid80 = prev["global_recompute"]["ab2d_spec_hybrid_after_q02_pass_per_80"]
    prev_overall = prev["global_recompute"]["overall_after_q02_per_320"]
    ab2d_api = prev["global_recompute"]["ab2d_api_pass_per_80"]

    # Recompute hybrid using: Fraction3+q08 from prev v2 eval + all 5 pure q02 v2
    prev_cells = [json.loads(l) for l in PREV_V2_CELLS.read_text(encoding="utf-8").splitlines()]
    replaced = {(r["task_id"], int(r["seed"])): r for r in prev_cells}
    # prior q02 patch 2 cells
    for r in [json.loads(l) for l in PREV_Q02_CELLS.read_text(encoding="utf-8").splitlines()]:
        replaced[(r["task_id"], int(r["seed"]))] = r
    # purity 3 cells
    for r in purity_rows:
        # synthesize minimal replace record
        replaced[(TASK_ID, r["seed"])] = {
            "task_id": TASK_ID,
            "seed": r["seed"],
            "final_status": r["v2_status"],
            "primary_failure_layer": r["v2_layer"],
        }

    hybrid_pass = 0
    remaining = []
    for r in v4_all:
        if r["condition"] != "ab2d_spec":
            continue
        key = (r["task_id"], int(r["seed"]))
        if key in replaced:
            status = replaced[key]["final_status"]
            layer = replaced[key].get("primary_failure_layer")
        else:
            status = r["final_status"]
            layer = r.get("primary_failure_layer")
        if status == "PASSED":
            hybrid_pass += 1
        else:
            remaining.append({"task_id": r["task_id"], "seed": r["seed"], "layer": layer})

    # Overall: v4 overall - ab2d_spec_v1 + hybrid
    v4_overall = sum(1 for r in v4_all if r["final_status"] == "PASSED")
    ab2d_spec_v1 = sum(
        1 for r in v4_all if r["condition"] == "ab2d_spec" and r["final_status"] == "PASSED"
    )
    overall_hybrid = v4_overall - ab2d_spec_v1 + hybrid_pass

    deltas = [r for r in purity_rows if not r["consistent_with_v1"]]
    all5_deltas = [r for r in q02_v2_detail if not r["consistent"]]

    summary = {
        "evaluation_id": "math16_pilot02_ab2d_spec_v2_q02_purity_evaluation_r001",
        "llm_calls": 0,
        "api_cost_usd": 0.0,
        "frozen_prompt_sha256": EXPECTED_PROMPT_SHA,
        "purity_seed_compare": purity_rows,
        "all5_prompt_sha_table": sha_table,
        "q02_ab2d_spec_v2_pass": f"{q02_v2_pass}/5",
        "q02_all5_detail": q02_v2_detail,
        "inconsistencies_vs_v1_in_purity3": deltas,
        "inconsistencies_vs_v1_all5": all5_deltas,
        "global_recompute": {
            "ab2d_spec_hybrid_pass_per_80": hybrid_pass,
            "ab2d_spec_prev_claimed_80": prev_hybrid80,
            "ab2d_api_pass_per_80": ab2d_api,
            "gap_hybrid_vs_api": hybrid_pass - ab2d_api,
            "overall_hybrid_pass_per_320": overall_hybrid,
            "overall_prev_claimed_306": prev_overall,
            "verified_unchanged_80_306": hybrid_pass == 80 and overall_hybrid == 306,
        },
        "remaining_ab2d_spec_failures_after_hybrid": remaining,
        "created_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "cell_level_baseline.jsonl").write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in purity_rows) + "\n",
        encoding="utf-8",
    )
    (OUT_DIR / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    md = [
        "# Ab2d+spec-v2 q02 version purity evaluation",
        "",
        "## Purity 3 seeds (this run)",
        "| seed | v1(舊) | v2(新) | 一致 |",
        "| ---: | :--- | :--- | :---: |",
    ]
    for r in purity_rows:
        md.append(
            f"| {r['seed']} | {r['v1_status']} | {r['v2_status']} | "
            f"{'Y' if r['consistent_with_v1'] else 'N'} |"
        )
    md.extend(
        [
            "",
            "## All 5 seeds prompt SHA",
            "| seed | artifact SHA | file SHA | frozen match |",
            "| ---: | :--- | :--- | :---: |",
        ]
    )
    for r in sha_table:
        md.append(
            f"| {r['seed']} | `{r['artifact_prompt_sha256'][:16]}…` | "
            f"`{r['prompt_file_sha256'][:16]}…` | "
            f"{'Y' if r['matches_frozen_v2'] else 'N'} |"
        )
    md.extend(
        [
            "",
            f"- q02 ab2d_spec_v2: `{q02_v2_pass}/5`",
            f"- Ab2d+spec hybrid: `{hybrid_pass}/80` (prev claimed {prev_hybrid80})",
            f"- Overall hybrid: `{overall_hybrid}/320` (prev claimed {prev_overall})",
            "",
            "AB2D_SPEC_V2_Q02_VERSION_PURITY_COMPLETE",
            "",
        ]
    )
    (OUT_DIR / "report.md").write_text("\n".join(md), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
