# -*- coding: utf-8 -*-
"""
scripts/build_math16_full_plans.py
==================================
Script to generate the full Math16 execution plans:
1. Full runtime manifest
2. 240-cell generation plan
3. Combined 320-cell analysis inventory
"""

import json
import hashlib
import sys
from pathlib import Path

# Add project root to sys.path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.math16_pool import build_pool_tasks, frozen_for_prompt
from agent_tools.finals_rebuild.ce115_clean_incremental_ablation import build_condition_prompt

INTEGER_TASKS = [
    "ce111_q03_prime_factor_selection",
    "ce112_q01_negative_integer_power",
    "ce112_q09_divisor_multiple_intersection",
    "ce111_nonchoice_q01_part1_exponential_growth"
]

NON_INTEGER_TASKS = [
    # Polynomials
    "ce111_q02_polynomial_division_remainder",
    "ce111_q08_polynomial_factor_parameter_recovery",
    "ce115_calc_polynomial_division_l1",
    "ce115_calc_polynomial_factor_roots_l1",
    # Radicals
    "ce111_q10_ordered_quadratic_roots_radical",
    "ce112_q04_radical_simplification",
    "ce113_q11_rationalize_denominator",
    "ce115_calc_radical_simplification_l1",
    # Fractions
    "ce111_q05_exact_fraction_expression",
    "ce112_q12_independent_probability_fraction",
    "ce113_q01_negative_fraction_subtraction",
    "ce115_calc_exact_rational_expression_l1"
]

CONDITIONS = ["ab1", "ab2g", "ab2d", "ab2d_spec"]
SEEDS = [2026071301, 2026072001, 2026072002, 2026072003, 2026072004]

def get_file_sha256(path: Path) -> str:
    content = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    return hashlib.sha256(content.encode("utf-8")).hexdigest()

def main():
    tasks = {t["task_id"]: t for t in build_pool_tasks()}

    # 1. Build runtime manifest
    runtime_manifest = {
        "experiment_id": "math16_pilot02_full_gemini_freeze_v1",
        "model_provider": "google",
        "model_tag": "gemini-3.5-flash",
        "model_version": "gemini-3.5-flash",
        "runtime": "vertex_ai_api",
        "runtime_version": "v1",
        "thinking_mode": False,
        "temperature": 0.0,
        "top_p": 1.0,
        "top_k": 1,
        "max_output_tokens": 24576,
        "timeout_seconds": 600,
        "retry_policy": {
            "max_attempts": 3,
            "retry_delays_seconds": [5, 20]
        },
        "seed_list": SEEDS,
        "source_commit": "7b298b0c8784032a4063498f4e36653036a9b770",
        "created_at_utc": "2026-07-21T09:20:00Z"
    }

    # Calculate fingerprint of full runtime manifest
    keys = [
        "experiment_id", "model_provider", "model_tag", "model_version",
        "runtime", "runtime_version", "thinking_mode", "temperature",
        "top_p", "top_k", "max_output_tokens", "timeout_seconds",
        "retry_policy", "seed_list", "source_commit"
    ]
    sub = {k: runtime_manifest[k] for k in keys}
    serialized = json.dumps(sub, sort_keys=True, ensure_ascii=False)
    fingerprint = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
    runtime_manifest["runtime_config_fingerprint"] = fingerprint

    manifest_json_path = ROOT / "docs/experiments/manifests/math16_pilot02_full_runtime_manifest.json"
    manifest_json_path.write_text(json.dumps(runtime_manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # 2. Build 240-cell generation plan
    generation_plan = []
    for tid in NON_INTEGER_TASKS:
        task = tasks[tid]
        frozen = frozen_for_prompt(task)

        for cond in CONDITIONS:
            # For ab2d_spec, the prompt is frozen on disk
            if cond == "ab2d_spec":
                prompt_file = ROOT / f"docs/experiments/prompts/ab2d_spec/prompts/{tid}.txt"
                p_sha = get_file_sha256(prompt_file)
            else:
                prompt_text = build_condition_prompt(cond, task, frozen).replace("\r\n", "\n")
                p_sha = hashlib.sha256(prompt_text.encode("utf-8")).hexdigest()

            for seed in SEEDS:
                cell_id = f"gemini_3_5_flash__{tid}__{cond}__seed_{seed}"
                rel_path = f"cells/{cell_id}"

                generation_plan.append({
                    "cell_id": cell_id,
                    "task_id": tid,
                    "condition": cond,
                    "seed": seed,
                    "model_tag": "gemini-3.5-flash",
                    "prompt_sha256": p_sha,
                    "output_relative_path": rel_path
                })

    plan_json_path = ROOT / "docs/experiments/manifests/math16_pilot02_full_generation_plan.json"
    plan_json_path.write_text(json.dumps(generation_plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # 3. Build combined 320-cell analysis inventory
    analysis_inventory = []

    # First: add 80 reused frozen cells from the Integer run
    integer_plan_path = ROOT / "docs/experiments/manifests/math16_pilot02_integer_cell_plan.json"
    integer_plan = json.loads(integer_plan_path.read_text(encoding="utf-8"))

    for cell in integer_plan:
        analysis_inventory.append({
            "cell_id": cell["cell_id"],
            "task_id": cell["task_id"],
            "condition": cell["condition"],
            "seed": cell["seed"],
            "model_tag": cell["model_tag"],
            "prompt_sha256": cell["prompt_sha256"],
            "output_relative_path": f"math16_pilot02_integer_gemini/{cell['output_relative_path']}",
            "reused": True
        })

    # Second: add 240 new cells
    for cell in generation_plan:
        analysis_inventory.append({
            "cell_id": cell["cell_id"],
            "task_id": cell["task_id"],
            "condition": cell["condition"],
            "seed": cell["seed"],
            "model_tag": cell["model_tag"],
            "prompt_sha256": cell["prompt_sha256"],
            "output_relative_path": f"math16_pilot02_full_gemini/{cell['output_relative_path']}",
            "reused": False
        })

    inventory_json_path = ROOT / "docs/experiments/manifests/math16_pilot02_full_analysis_inventory.json"
    inventory_json_path.write_text(json.dumps(analysis_inventory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Plans generated. Fingerprint: {fingerprint}")

if __name__ == "__main__":
    main()
