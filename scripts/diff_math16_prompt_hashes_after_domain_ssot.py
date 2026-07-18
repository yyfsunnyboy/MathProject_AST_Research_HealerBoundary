"""Compare freeze/run_001 prompt hashes vs current builder after Domain API SSOT."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.ce115_clean_incremental_ablation import (
    build_condition_prompt,
    prompt_sha256,
)
from agent_tools.finals_rebuild.math16_pool import frozen_for_prompt, load_pool_manifest

FREEZE = ROOT / "docs/experiments/results/math16_latex_v1_freeze_closeout_report.json"
ORIG = ROOT / "docs/experiments/results/gemini35flash_math16_latex_v1_ab123_run_001"
OUT = ROOT / "docs/experiments/results/math16_domain_api_ssot_prompt_hash_diff.json"

# Reasons for expected return-text changes under SSOT.
EXPECTED_REASON = {
    "PolynomialOps.factor_quadratic_exact": (
        "AMBIGUOUS returns prose replaced with list[dict,dict] length-2 schema"
    ),
    "IntegerOps.safe_eval": "AMBIGUOUS 'exact numeric value' -> int|float",
    "PolynomialOps.mul": "AMBIGUOUS bare 'list' -> list[int|str] coeffs",
    "RadicalOps.simplify_term": (
        "AMBIGUOUS 'exact coefficient' prose -> tuple[int|Fraction, int]"
    ),
}


def main() -> int:
    freeze = json.loads(FREEZE.read_text(encoding="utf-8"))
    old_by_key = {
        (row["task_id"], row["condition"]): row["prompt_sha256"]
        for row in freeze["prompt_hashes_48"]
    }
    # Prefer run_001 artifact hashes when present (should match freeze).
    for cell_dir in sorted((ORIG / "cells").glob("gemini_3_5_flash__*")):
        art = json.loads((cell_dir / "artifact.json").read_text(encoding="utf-8"))
        key = (art["task_id"], art["condition"])
        old_by_key[key] = art.get("canonical_prompt_hash") or art.get("prompt_hash")

    from agent_tools.finals_rebuild.ce115_clean_incremental_ablation import TASK_DOMAIN_APIS

    changed = []
    unchanged = []
    tasks = {t["task_id"]: t for t in load_pool_manifest()["tasks"]}
    for tid, task in sorted(tasks.items()):
        frozen = frozen_for_prompt(task)
        for cond in ("ab1", "ab2g", "ab2d"):
            prompt = build_condition_prompt(cond, task, frozen)
            new_h = prompt_sha256(prompt)
            old_h = old_by_key[(tid, cond)]
            row = {
                "task_id": tid,
                "condition": cond,
                "old_prompt_hash": old_h,
                "new_prompt_hash": new_h,
                "changed": old_h != new_h,
            }
            if old_h != new_h:
                apis = [a["name"] for a in TASK_DOMAIN_APIS[tid]] if cond == "ab2d" else []
                reasons = [EXPECTED_REASON[a] for a in apis if a in EXPECTED_REASON]
                row["hash_change_reason"] = reasons or ["UNEXPECTED"]
                row["ab2d_apis"] = apis
                changed.append(row)
            else:
                unchanged.append(row)

    unexpected = [r for r in changed if r.get("hash_change_reason") == ["UNEXPECTED"]]
    # Ab1/Ab2g must not change
    bad_non_ab2d = [r for r in changed if r["condition"] != "ab2d"]
    payload = {
        "changed_count": len(changed),
        "unchanged_count": len(unchanged),
        "changed_cells": changed,
        "unexpected_changes": unexpected + bad_non_ab2d,
        "planned_validation_cells": changed,
        "q10_ab2d": next(
            r
            for r in changed + unchanged
            if r["task_id"] == "ce111_q10_ordered_quadratic_roots_radical"
            and r["condition"] == "ab2d"
        ),
        "factor_roots_ab2d": next(
            r
            for r in changed + unchanged
            if r["task_id"] == "ce115_calc_polynomial_factor_roots_l1"
            and r["condition"] == "ab2d"
        ),
        "stop": bool(unexpected or bad_non_ab2d),
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "changed_count": payload["changed_count"],
        "unexpected": len(payload["unexpected_changes"]),
        "stop": payload["stop"],
        "changed_task_conditions": [
            f"{r['task_id']}@{r['condition']}" for r in changed
        ],
        "q10_ab2d_changed": payload["q10_ab2d"]["changed"],
        "factor_roots_ab2d_changed": payload["factor_roots_ab2d"]["changed"],
        "out": str(OUT),
    }, ensure_ascii=False, indent=2))
    return 1 if payload["stop"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
