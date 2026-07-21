# -*- coding: utf-8 -*-
"""
scripts/build_math16_integer_ab2d_spec_prompts.py
=================================================
Assembler script to generate and freeze Ab2d+spec exact prompts for the 4 target Integer tasks.
"""

import os
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

TARGET_TASKS = [
    "ce111_q03_prime_factor_selection",
    "ce112_q01_negative_integer_power",
    "ce112_q09_divisor_multiple_intersection",
    "ce111_nonchoice_q01_part1_exponential_growth"
]

OUTPUT_DIR = ROOT / "docs/experiments/prompts/ab2d_spec"
PROMPTS_OUT_DIR = OUTPUT_DIR / "prompts"

def get_rel_path_str(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")

def get_file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    os.makedirs(PROMPTS_OUT_DIR, exist_ok=True)

    # Load sources
    pool_manifest_path = ROOT / "docs/experiments/manifests/math16_latex_v1_pool_manifest.json"
    ab2g_prefix_path = ROOT / "agent_tools/finals_rebuild/ce115_clean_incremental_ablation.py"
    scaffold_path = ROOT / "docs/experiments/templates/ab2d_spec/integer_domain_scaffold_compact.py"

    pool_manifest_sha = get_file_sha256(pool_manifest_path)
    ab2g_prefix_sha = get_file_sha256(ab2g_prefix_path)
    scaffold_sha = get_file_sha256(scaffold_path)

    scaffold_content = scaffold_path.read_text(encoding="utf-8").strip()

    final_check = (
        "Final check before output:\n"
        "- Output one complete Python source only.\n"
        "- Define the required generate() entry point.\n"
        "- Use the frozen parameters exactly.\n"
        "- Return the exact required keys and answer schema.\n"
        "- Do not use IntegerOps or invented APIs."
    )

    tasks = {t["task_id"]: t for t in build_pool_tasks()}
    manifest_records = []

    for tid in TARGET_TASKS:
        task = tasks[tid]
        frozen = frozen_for_prompt(task)
        ab2g_prompt = build_condition_prompt("ab2g", task, frozen)

        # Load guardrail
        guardrail_path = ROOT / f"docs/experiments/prompts/ab2d_spec/task_guardrails/integer/{tid}.md"
        guardrail_sha = get_file_sha256(guardrail_path)
        guardrail_content = guardrail_path.read_text(encoding="utf-8").strip()

        # Assemble exact prompt
        exact_prompt = (
            f"{ab2g_prompt.strip()}\n\n"
            f"## Compact Domain Scaffold\n{scaffold_content}\n\n"
            f"## Task Guardrails\n{guardrail_content}\n\n"
            f"## Final Check\n{final_check}\n"
        )

        # Write to txt
        prompt_txt_path = PROMPTS_OUT_DIR / f"{tid}.txt"
        prompt_txt_path.write_text(exact_prompt, encoding="utf-8")

        prompt_sha = hashlib.sha256(exact_prompt.encode("utf-8")).hexdigest()

        # Record manifest
        manifest_records.append({
            "condition": "ab2d_spec",
            "task_id": tid,
            "domain": "IntegerOps",
            "api_policy": "native_only",
            "prompt_revision": "ab2d_spec_v1",
            "task_contract_source": get_rel_path_str(pool_manifest_path),
            "task_contract_sha256": pool_manifest_sha,
            "ab2g_prefix_source": get_rel_path_str(ab2g_prefix_path),
            "ab2g_prefix_sha256": ab2g_prefix_sha,
            "domain_scaffold_source": get_rel_path_str(scaffold_path),
            "domain_scaffold_sha256": scaffold_sha,
            "task_guardrail_source": get_rel_path_str(guardrail_path),
            "task_guardrail_sha256": guardrail_sha,
            "exact_prompt_sha256": prompt_sha,
            "character_count": len(exact_prompt),
            "utf8_byte_count": len(exact_prompt.encode("utf-8")),
            "prompt_frozen": True,
            "historical_error_informed": True,
            "pilot02_same_run_results_used": False,
            "model_called": False
        })

    manifest_out = {
        "manifest_id": "math16_ab2d_spec_pilot02_freeze_v1",
        "tasks": manifest_records
    }

    manifest_json_path = OUTPUT_DIR / "manifest.json"
    with open(manifest_json_path, "w", encoding="utf-8") as f:
        json.dump(manifest_out, f, indent=2, ensure_ascii=False)

    print("Prompts and manifest compiled successfully!")

if __name__ == "__main__":
    main()
