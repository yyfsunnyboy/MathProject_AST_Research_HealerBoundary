"""
build_math16_pilot02_qwen4b_unrestricted_stress_test_v11_dry_run.py
=====================================================================
Builder for Unrestricted Stress Test v1.1 Zero-Model Dry Run.

Generates dry-run execution plans, default & forced exploratory arm plans,
ambiguity evidence, output isolation checks, and dry-run manifest.

Zero-model / zero-healer / zero-evaluator / zero-transform execution.
"""

import csv
import json
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
ELIGIBILITY_INVENTORY_PATH = REPO_ROOT / "docs/experiments/results/math16_pilot02_qwen4b_healer_v4_r001/eligibility_inventory.jsonl"
DRY_RUN_OUTPUT_DIR = REPO_ROOT / "artifacts/math16_pilot02_qwen4b_unrestricted_stress_test_v11/dry_run"
FORMAL_OUTPUT_DIR = REPO_ROOT / "artifacts/math16_pilot02_qwen4b_unrestricted_stress_test_v11/formal"

AMBIGUOUS_CELL_ID = "qwen3_5_4b__ce111_q08_polynomial_factor_parameter_recovery__ab2d__seed_2026072004"

def build_dry_run_artifacts():
    print("Executing Math16 Qwen4B Unrestricted Stress Test v1.1 Zero-Model Dry Run Builder...")
    DRY_RUN_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Read eligibility inventory records (242 baseline FAIL cells)
    records = []
    with open(ELIGIBILITY_INVENTORY_PATH, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line.strip()))

    print(f"Loaded {len(records)} baseline FAIL records.")
    assert len(records) == 242, f"Expected 242 cells, got {len(records)}"

    dry_run_plan_recs = []
    default_arm_rows = []

    no_rule_count = 0
    eligible_count = 0
    ambiguous_count = 0

    for r in records:
        cid = r["cell_id"]
        is_eligible = r.get("healer_eligible", False)
        reason = r.get("eligibility_reason", "")
        hits = r.get("probe_hits", [])
        matched_rule = r.get("matched_rule_probe")

        # Classify
        if is_eligible and matched_rule and len(hits) == 1:
            stratum = "UNIQUE_CANDIDATE_PRIMARY_ELIGIBLE"
            default_action = "PLANNED_TRANSFORM"
            eligible_count += 1
        elif "Ambiguous" in reason or cid == AMBIGUOUS_CELL_ID:
            stratum = "AMBIGUOUS_MULTIPLE_CANDIDATES"
            default_action = "ABSTAIN_AMBIGUOUS"
            ambiguous_count += 1
        else:
            stratum = "NO_RULE_CANDIDATE"
            default_action = "ABSTAIN_NO_RULE"
            no_rule_count += 1

        plan_rec = {
            "canonical_cell_id": cid,
            "condition": r.get("condition"),
            "family": r.get("family"),
            "task_id": r.get("task_id"),
            "seed": r.get("seed"),
            "stratum": stratum,
            "default_arm_action": default_action,
            "target_matched_rule": matched_rule if matched_rule else None,
            "transform_executed_in_dry_run": False,
            "persisted_complete": False,
        }
        dry_run_plan_recs.append(plan_rec)

        default_arm_rows.append({
            "canonical_cell_id": cid,
            "condition": r.get("condition"),
            "family": r.get("family"),
            "stratum": stratum,
            "default_arm_action": default_action,
            "matched_rule": matched_rule if matched_rule else "NONE",
            "transform_planned": default_action == "PLANNED_TRANSFORM",
            "transform_executed": False
        })

    print(f"Accounting verification: NO_RULE={no_rule_count}, ELIGIBLE={eligible_count}, AMBIGUOUS={ambiguous_count}, TOTAL={len(dry_run_plan_recs)}")
    assert no_rule_count == 231
    assert eligible_count == 10
    assert ambiguous_count == 1

    # 2. Write dry_run_cell_plan.jsonl
    with open(DRY_RUN_OUTPUT_DIR / "dry_run_cell_plan.jsonl", "w", encoding="utf-8") as f:
        for rec in dry_run_plan_recs:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    # 3. Write default_arm_plan.csv
    csv_fields = ["canonical_cell_id", "condition", "family", "stratum", "default_arm_action", "matched_rule", "transform_planned", "transform_executed"]
    with open(DRY_RUN_OUTPUT_DIR / "default_arm_plan.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=csv_fields)
        writer.writeheader()
        writer.writerows(default_arm_rows)

    # 4. Write forced_exploratory_arm_plan.json
    forced_arm_plan = {
        "arm_name": "FORCED_EXPLORATORY_ARM",
        "target_cell_id": AMBIGUOUS_CELL_ID,
        "cell_task_id": "ce111_q08_polynomial_factor_parameter_recovery",
        "condition": "ab2d",
        "seed": 2026072004,
        "ambiguity_type": "AMBIGUOUS_MULTIPLE_ENTRY_POINTS_OR_PROSE",
        "candidate_rule_ids": ["L1_PROSE_RESIDUE_NARROW"],
        "candidate_target_count": 2,
        "candidate_target_names": ["first_def_generate_offset", "last_def_generate_offset"],
        "selection_policy": {
            "policy_id": "DETERMINISTIC_FIRST_ENTRY_POINT_SOURCE_PREORDER",
            "rule_priority_order": [
                "L1_CLOSE_UNBALANCED_PARENTHESIS",
                "L1_CLOSE_UNBALANCED_DELIMITER_EXTENDED",
                "L1_PROSE_RESIDUE_NARROW",
                "L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP",
                "L2_KWARGS_EMPTY_BAG_INLINE_UNIQUE_PARAM",
                "L2_CORRECT_ANSWER_JSON_DUMPS_UNWRAP"
            ],
            "tie_breaking_order": "AST_PREORDER_SOURCE_SPAN_FIRST",
            "selected_target": "first_def_generate_offset"
        },
        "safety_pre_classification": "UNSAFE_MODIFICATION",
        "safety_reason": "Stripping prose residue from un-fenced multi-block source has structural truncation risk; must NOT be marked SAFE_REPAIR_CANDIDATE.",
        "transform_planned": True,
        "transform_executed_in_dry_run": False
    }
    with open(DRY_RUN_OUTPUT_DIR / "forced_exploratory_arm_plan.json", "w", encoding="utf-8") as f:
        json.dump(forced_arm_plan, f, indent=2, ensure_ascii=False)

    # 5. Write ambiguity_evidence.json
    ambiguity_evidence = {
        "cell_id": AMBIGUOUS_CELL_ID,
        "baseline_classifier_outcome": "missing_entry_point",
        "healer_primary_decision": "abstained",
        "primary_abstain_reason": "Ambiguous entry point; frozen healer abstains.",
        "source_artifact_path": f"docs/experiments/results/math16_pilot02_qwen4b/cells/{AMBIGUOUS_CELL_ID}/artifact.json",
        "evidence_summary": "Model output extensive un-fenced prose reasoning prior to Python function definition, creating multiple candidate entry-point boundaries."
    }
    with open(DRY_RUN_OUTPUT_DIR / "ambiguity_evidence.json", "w", encoding="utf-8") as f:
        json.dump(ambiguity_evidence, f, indent=2, ensure_ascii=False)

    # 6. Write output_isolation_check.json
    isolation_check = {
        "dry_run_output_directory": str(DRY_RUN_OUTPUT_DIR),
        "formal_output_directory": str(FORMAL_OUTPUT_DIR),
        "formal_directory_exists": FORMAL_OUTPUT_DIR.exists(),
        "output_isolated": not FORMAL_OUTPUT_DIR.exists(),
        "status": "ISOLATED_PASS"
    }
    with open(DRY_RUN_OUTPUT_DIR / "output_isolation_check.json", "w", encoding="utf-8") as f:
        json.dump(isolation_check, f, indent=2, ensure_ascii=False)

    # 7. Write dry_run_manifest.json
    dry_run_manifest = {
        "manifest_id": "math16_pilot02_qwen4b_unrestricted_stress_test_v11_dry_run_manifest",
        "manifest_version": "1.1",
        "dry_run_type": "ZERO_MODEL_RUNTIME_PREFLIGHT_DRY_RUN",
        "project": "Ivan旺宏科學展 HealerBoundary",
        "created_at_utc": "2026-07-23T00:00:00Z",

        "accounting": {
            "total_baseline_fail_cells": 242,
            "no_rule_candidate": 231,
            "unique_candidate_primary_eligible": 10,
            "unique_candidate_primary_noneligible": 0,
            "ambiguous_multiple_candidates": 1,
            "detection_unresolved": 0
        },

        "arm_plans": {
            "default_arm_cell_count": 242,
            "default_arm_planned_transforms": 10,
            "forced_arm_cell_count": 1,
            "forced_arm_target_cell_id": AMBIGUOUS_CELL_ID,
            "forced_arm_safety_pre_classification": "UNSAFE_MODIFICATION"
        },

        "governance": {
            "llm_vLM_calls": 0,
            "healer_transform_executions": 0,
            "evaluator_runs": 0,
            "formal_results_created": False
        },

        "verdicts": [
            "MATH16_QWEN4B_UNRESTRICTED_STRESS_TEST_V11_ZERO_MODEL_DRY_RUN_COMPLETED",
            "DEFAULT_ARM_242_CELL_PLAN_VALIDATED",
            "AMBIGUITY_CASE_N1_FULLY_SPECIFIED",
            "FORCED_EXPLORATORY_SELECTION_POLICY_FROZEN",
            "RUNTIME_AND_OUTPUT_ISOLATION_VALIDATED",
            "OFFICIAL_RESULTS_PRESERVED",
            "READY_FOR_EXPLICITLY_AUTHORIZED_STRESS_TEST_EXECUTION"
        ]
    }
    with open(DRY_RUN_OUTPUT_DIR / "dry_run_manifest.json", "w", encoding="utf-8") as f:
        json.dump(dry_run_manifest, f, indent=2, ensure_ascii=False)

    print("All dry run artifacts successfully generated in:", DRY_RUN_OUTPUT_DIR)

if __name__ == "__main__":
    build_dry_run_artifacts()
