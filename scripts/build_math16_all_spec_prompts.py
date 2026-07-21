# -*- coding: utf-8 -*-
"""
scripts/build_math16_all_spec_prompts.py
========================================
Assembler script to generate and freeze Ab2d+spec exact prompts for all 16 target tasks.
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

ALL_TASKS = [
    # Integer (4 tasks)
    {
        "task_id": "ce111_q03_prime_factor_selection",
        "family": "integer",
        "domain": "IntegerOps",
        "api_policy": "native-only",
        "scaffold": "integer_domain_scaffold_compact.py",
        "guardrail_subdir": "integer",
        "is_api": False,
        "pre_run_difficulty": "low",
        "discrimination": "medium",
        "ceiling_risk": "high"
    },
    {
        "task_id": "ce112_q01_negative_integer_power",
        "family": "integer",
        "domain": "IntegerOps",
        "api_policy": "native-only",
        "scaffold": "integer_domain_scaffold_compact.py",
        "guardrail_subdir": "integer",
        "is_api": False,
        "pre_run_difficulty": "low",
        "discrimination": "medium",
        "ceiling_risk": "high"
    },
    {
        "task_id": "ce112_q09_divisor_multiple_intersection",
        "family": "integer",
        "domain": "IntegerOps",
        "api_policy": "native-only",
        "scaffold": "integer_domain_scaffold_compact.py",
        "guardrail_subdir": "integer",
        "is_api": False,
        "pre_run_difficulty": "medium",
        "discrimination": "high",
        "ceiling_risk": "medium"
    },
    {
        "task_id": "ce111_nonchoice_q01_part1_exponential_growth",
        "family": "integer",
        "domain": "IntegerOps",
        "api_policy": "native-only",
        "scaffold": "integer_domain_scaffold_compact.py",
        "guardrail_subdir": "integer",
        "is_api": False,
        "pre_run_difficulty": "medium",
        "discrimination": "high",
        "ceiling_risk": "medium"
    },
    # Polynomial (4 tasks)
    {
        "task_id": "ce111_q02_polynomial_division_remainder",
        "family": "polynomial",
        "domain": "PolynomialOps",
        "api_policy": "API-only",
        "scaffold": "polynomial_domain_scaffold_compact.py",
        "guardrail_subdir": "polynomial",
        "is_api": True,
        "pre_run_difficulty": "medium",
        "discrimination": "high",
        "ceiling_risk": "low"
    },
    {
        "task_id": "ce111_q08_polynomial_factor_parameter_recovery",
        "family": "polynomial",
        "domain": "PolynomialOps",
        "api_policy": "native-only",
        "scaffold": "integer_domain_scaffold_compact.py",
        "guardrail_subdir": "polynomial",
        "is_api": False,
        "pre_run_difficulty": "high",
        "discrimination": "very_high",
        "ceiling_risk": "very_low"
    },
    {
        "task_id": "ce115_calc_polynomial_division_l1",
        "family": "polynomial",
        "domain": "PolynomialOps",
        "api_policy": "API-only",
        "scaffold": "polynomial_domain_scaffold_compact.py",
        "guardrail_subdir": "polynomial",
        "is_api": True,
        "pre_run_difficulty": "medium",
        "discrimination": "high",
        "ceiling_risk": "low"
    },
    {
        "task_id": "ce115_calc_polynomial_factor_roots_l1",
        "family": "polynomial",
        "domain": "PolynomialOps",
        "api_policy": "native-only",
        "scaffold": "integer_domain_scaffold_compact.py",
        "guardrail_subdir": "polynomial",
        "is_api": False,
        "pre_run_difficulty": "medium",
        "discrimination": "high",
        "ceiling_risk": "medium"
    },
    # Radical (4 tasks)
    {
        "task_id": "ce111_q10_ordered_quadratic_roots_radical",
        "family": "radical",
        "domain": "RadicalOps",
        "api_policy": "mixed",
        "scaffold": "radical_domain_scaffold_compact.py",
        "guardrail_subdir": "radical",
        "is_api": True,
        "pre_run_difficulty": "high",
        "discrimination": "very_high",
        "ceiling_risk": "very_low"
    },
    {
        "task_id": "ce112_q04_radical_simplification",
        "family": "radical",
        "domain": "RadicalOps",
        "api_policy": "API-only",
        "scaffold": "radical_domain_scaffold_compact.py",
        "guardrail_subdir": "radical",
        "is_api": True,
        "pre_run_difficulty": "low",
        "discrimination": "medium",
        "ceiling_risk": "high"
    },
    {
        "task_id": "ce113_q11_rationalize_denominator",
        "family": "radical",
        "domain": "RadicalOps",
        "api_policy": "native-only",
        "scaffold": "integer_domain_scaffold_compact.py",
        "guardrail_subdir": "radical",
        "is_api": False,
        "pre_run_difficulty": "high",
        "discrimination": "very_high",
        "ceiling_risk": "low"
    },
    {
        "task_id": "ce115_calc_radical_simplification_l1",
        "family": "radical",
        "domain": "RadicalOps",
        "api_policy": "API-only",
        "scaffold": "radical_domain_scaffold_compact.py",
        "guardrail_subdir": "radical",
        "is_api": True,
        "pre_run_difficulty": "low",
        "discrimination": "medium",
        "ceiling_risk": "high"
    },
    # Fraction (4 tasks)
    {
        "task_id": "ce111_q05_exact_fraction_expression",
        "family": "fraction",
        "domain": "FractionOps",
        "api_policy": "API-only",
        "scaffold": "fraction_domain_scaffold_compact.py",
        "guardrail_subdir": "fraction",
        "is_api": True,
        "pre_run_difficulty": "medium",
        "discrimination": "high",
        "ceiling_risk": "low"
    },
    {
        "task_id": "ce112_q12_independent_probability_fraction",
        "family": "fraction",
        "domain": "FractionOps",
        "api_policy": "API-only",
        "scaffold": "fraction_domain_scaffold_compact.py",
        "guardrail_subdir": "fraction",
        "is_api": True,
        "pre_run_difficulty": "medium",
        "discrimination": "medium",
        "ceiling_risk": "medium"
    },
    {
        "task_id": "ce113_q01_negative_fraction_subtraction",
        "family": "fraction",
        "domain": "FractionOps",
        "api_policy": "API-only",
        "scaffold": "fraction_domain_scaffold_compact.py",
        "guardrail_subdir": "fraction",
        "is_api": True,
        "pre_run_difficulty": "low",
        "discrimination": "medium",
        "ceiling_risk": "high"
    },
    {
        "task_id": "ce115_calc_exact_rational_expression_l1",
        "family": "fraction",
        "domain": "FractionOps",
        "api_policy": "API-only",
        "scaffold": "fraction_domain_scaffold_compact.py",
        "guardrail_subdir": "fraction",
        "is_api": True,
        "pre_run_difficulty": "medium",
        "discrimination": "high",
        "ceiling_risk": "low"
    }
]

OUTPUT_DIR = ROOT / "docs/experiments/prompts/ab2d_spec"
PROMPTS_OUT_DIR = OUTPUT_DIR / "prompts"

def get_rel_path_str(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")

def get_file_sha256(path: Path) -> str:
    # Read text, normalize to LF, and encode to UTF-8
    content = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    return hashlib.sha256(content.encode("utf-8")).hexdigest()

def main():
    os.makedirs(PROMPTS_OUT_DIR, exist_ok=True)

    pool_manifest_path = ROOT / "docs/experiments/manifests/math16_latex_v1_pool_manifest.json"
    ab2g_prefix_path = ROOT / "agent_tools/finals_rebuild/ce115_clean_incremental_ablation.py"

    pool_manifest_sha = get_file_sha256(pool_manifest_path)
    ab2g_prefix_sha = get_file_sha256(ab2g_prefix_path)

    tasks_dict = {t["task_id"]: t for t in build_pool_tasks()}
    manifest_records = []

    final_check_api = (
        "Final check before output:\n"
        "- Output one complete Python source only.\n"
        "- Define the required generate() entry point.\n"
        "- Use the frozen parameters exactly.\n"
        "- Return the exact required keys and answer schema.\n"
        "- Only import the specified Domain API."
    )

    final_check_native = (
        "Final check before output:\n"
        "- Output one complete Python source only.\n"
        "- Define the required generate() entry point.\n"
        "- Use the frozen parameters exactly.\n"
        "- Return the exact required keys and answer schema.\n"
        "- Do not use domain APIs or invented APIs."
    )

    for item in ALL_TASKS:
        tid = item["task_id"]
        task = tasks_dict[tid]
        frozen = frozen_for_prompt(task)
        ab2g_prompt = build_condition_prompt("ab2g", task, frozen)

        # Load scaffold
        scaffold_path = ROOT / f"docs/experiments/templates/ab2d_spec/{item['scaffold']}"
        scaffold_sha = get_file_sha256(scaffold_path)
        scaffold_content = scaffold_path.read_text(encoding="utf-8").replace("\r\n", "\n").strip()

        # Load guardrail
        guardrail_path = ROOT / f"docs/experiments/prompts/ab2d_spec/task_guardrails/{item['guardrail_subdir']}/{tid}.md"
        guardrail_sha = get_file_sha256(guardrail_path)
        guardrail_content = guardrail_path.read_text(encoding="utf-8").replace("\r\n", "\n").strip()

        final_check = final_check_api if item["is_api"] else final_check_native

        # Assemble exact prompt with LF endings
        exact_prompt = (
            f"{ab2g_prompt.strip()}\n\n"
            f"## Compact Domain Scaffold\n{scaffold_content}\n\n"
            f"## Task Guardrails\n{guardrail_content}\n\n"
            f"## Final Check\n{final_check}\n"
        ).replace("\r\n", "\n")

        # Write to txt
        prompt_txt_path = PROMPTS_OUT_DIR / f"{tid}.txt"
        prompt_txt_path.write_text(exact_prompt, encoding="utf-8", newline="\n")

        prompt_sha = hashlib.sha256(exact_prompt.encode("utf-8")).hexdigest()

        # Build manifest record
        char_count = len(exact_prompt)
        utf8_bytes = len(exact_prompt.encode("utf-8"))
        est_tokens = int(char_count / 4) # Standard simple character/4 estimation or similar

        # Calculate section lengths
        section_lengths = {
            "header": len(ab2g_prompt),
            "scaffold": len(scaffold_content),
            "guardrail": len(guardrail_content),
            "final_check": len(final_check)
        }

        # Build source paths and hashes
        source_paths = [
            get_rel_path_str(pool_manifest_path),
            get_rel_path_str(ab2g_prefix_path),
            get_rel_path_str(scaffold_path),
            get_rel_path_str(guardrail_path)
        ]
        source_hashes = {
            get_rel_path_str(pool_manifest_path): pool_manifest_sha,
            get_rel_path_str(ab2g_prefix_path): ab2g_prefix_sha,
            get_rel_path_str(scaffold_path): scaffold_sha,
            get_rel_path_str(guardrail_path): guardrail_sha
        }

        manifest_records.append({
            "condition": "ab2d_spec",
            "task_id": tid,
            "family": item["family"],
            "domain": item["domain"],
            "api_policy": item["api_policy"],
            "pre_run_assessment": {
                "pre_run_difficulty": item["pre_run_difficulty"],
                "discrimination": item["discrimination"],
                "ceiling_risk": item["ceiling_risk"]
            },
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
            "prompt_path": get_rel_path_str(prompt_txt_path),
            "char_count": char_count,
            "utf8_byte_count": utf8_bytes,
            "estimated_token_count": est_tokens,
            "section_lengths": section_lengths,
            "source_paths": source_paths,
            "source_hashes": source_hashes,
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

    print("All 16 prompts and manifest compiled successfully!")

if __name__ == "__main__":
    main()
