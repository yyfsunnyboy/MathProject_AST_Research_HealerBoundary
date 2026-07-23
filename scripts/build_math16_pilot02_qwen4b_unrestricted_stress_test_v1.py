"""
build_math16_pilot02_qwen4b_unrestricted_stress_test_v1.py
===========================================================
Preregistration Builder for Math16 Qwen4B Unrestricted Healer Stress Test v1.

Pre-allocates the 242 baseline FAIL cells from the Qwen 3.5 4B 320-cell matrix,
verifies frozen rule allowlists and inherited audit SHAs, and writes the preregistered
cell plan.

Supports --dry-run for zero-model / zero-healer preflight validation.
"""

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
BASE_BASELINE_JSONL = REPO_ROOT / "docs/experiments/results/math16_pilot02_qwen4b_evaluation_v4_r001/cell_level_baseline.jsonl"
OUTPUT_DIR = REPO_ROOT / "artifacts/math16_pilot02_qwen4b_unrestricted_stress_test_v1/preregistration"

FROZEN_RULES = [
    "L1_CLOSE_UNBALANCED_PARENTHESIS",
    "L1_CLOSE_UNBALANCED_DELIMITER_EXTENDED",
    "L1_PROSE_RESIDUE_NARROW",
    "L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP",
    "L2_KWARGS_EMPTY_BAG_INLINE_UNIQUE_PARAM",
    "L2_CORRECT_ANSWER_JSON_DUMPS_UNWRAP",
]

INHERITED_SHAS = {
    "six_cell_rescue_audit_manifest": ("docs/experiments/manifests/math16_posthoc_six_cell_rescue_audit_v1_result_manifest.json", "97392be833786bab90bcd5f1cb9eb9b57edaffc681466bdda62650f29dda35de"),
    "before_after_recovery_manifest": ("docs/experiments/manifests/math16_posthoc_six_cell_before_after_recovery_v1_manifest.json", "19aece906497104b7c8880f2cdd261d4ee22fca49e0c216c61612a3e46359dae"),
    "before_signature_confirmation_manifest": ("docs/experiments/manifests/math16_posthoc_six_cell_before_signature_confirmation_v1_manifest.json", "1b52f0680a644f4637703dab2f7817b88e64e6fa87a667d22f237f4e0d2716ef"),
}

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def verify_prerequisites():
    print("[1] Verifying inherited audit SHAs...")
    for label, (rel_path, expected_sha) in INHERITED_SHAS.items():
        p = REPO_ROOT / rel_path
        if not p.exists():
            raise FileNotFoundError(f"Missing audit prerequisite file: {rel_path}")
        actual_sha = sha256_file(p)
        if actual_sha != expected_sha:
            raise ValueError(f"SHA mismatch for {label} ({rel_path}): expected {expected_sha}, got {actual_sha}")
        print(f"  PASS: {label} SHA match ({actual_sha[:10]}...)")

def extract_fail_cells():
    print("[2] Extracting ALL_BASELINE_FAIL_SET (242 cells)...")
    if not BASE_BASELINE_JSONL.exists():
        raise FileNotFoundError(f"Missing baseline records file: {BASE_BASELINE_JSONL}")

    fail_cells = []
    pass_cells = []
    with open(BASE_BASELINE_JSONL, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                r = json.loads(line)
                if r.get("final_status") == "PASSED":
                    pass_cells.append(r)
                else:
                    fail_cells.append(r)

    print(f"  Baseline PASS cells: {len(pass_cells)}")
    print(f"  Baseline FAIL cells: {len(fail_cells)}")

    if len(fail_cells) != 242:
        raise ValueError(f"Expected 242 baseline FAIL cells, found {len(fail_cells)}")
    if len(pass_cells) != 78:
        raise ValueError(f"Expected 78 baseline PASS cells, found {len(pass_cells)}")

    return fail_cells

def run_builder(dry_run: bool = True):
    print("======================================================================")
    print("Math16 Qwen4B Unrestricted Healer Stress Test v1 — Preregistration")
    print("======================================================================")
    print(f"Dry run mode: {dry_run}")
    print(f"Repo root: {REPO_ROOT}\n")

    verify_prerequisites()
    fail_cells = extract_fail_cells()

    if not dry_run:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        plan_file = OUTPUT_DIR / "unrestricted_stress_test_cell_plan.json"
        plan_data = {
            "plan_id": "math16_pilot02_qwen4b_unrestricted_stress_test_cell_plan_v1",
            "population_size": len(fail_cells),
            "target_set": "ALL_BASELINE_FAIL_SET",
            "frozen_rules": FROZEN_RULES,
            "fail_cell_ids": [c["cell_id"] for c in fail_cells]
        }
        with open(plan_file, "w", encoding="utf-8") as f:
            json.dump(plan_data, f, indent=2, ensure_ascii=False)
        print(f"\nSaved cell plan to: {plan_file}")

    print("\n======================================================================")
    print("BUILDER RESULT: PREFLIGHT_PASS")
    print("======================================================================")

def main():
    parser = argparse.ArgumentParser(description="Preregistration builder for Math16 Qwen4B Unrestricted Healer Stress Test v1.")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Run in dry-run preflight mode without creating files.")
    parser.add_argument("--execute-plan", action="store_true", help="Write preregistered plan files.")
    args = parser.parse_args()

    dry_run = not args.execute_plan
    run_builder(dry_run=dry_run)

if __name__ == "__main__":
    main()
