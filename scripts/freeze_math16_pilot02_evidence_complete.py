# -*- coding: utf-8 -*-
"""Milestone freezing script for Math16 Pilot-02 Evidence Complete v1.

Calculates SHA-256 hashes of all frozen evidence artifacts and generates:
1. source_sha_closure.json
2. frozen_numeric_claims.json
3. primary_posthoc_accounting.json
4. category_status.json
5. evidence_complete_manifest.json
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

OUT_DIR = ROOT / "docs/experiments/milestones/math16_pilot02_evidence_complete_v1"

# Target evidence files for cryptographic hashing
FILES_TO_HASH = {
    "integrated_report": "docs/experiments/reports/math16_pilot02_integrated_results_report_v1.md",
    "jury_qa_final": "docs/experiments/reports/math16_pilot02_jury_qa_final_v1.md",
    "figure_spec_manifest": "docs/experiments/visualization/math16_pilot02_core_figure_spec_v1/manifest.json",
    "figure_spec_json": "docs/experiments/visualization/math16_pilot02_core_figure_spec_v1/core_figure_spec.json",
    "gemini_baseline_summary": "docs/experiments/results/math16_pilot02_full_evaluation_v4_r001/baseline_summary.json",
    "qwen4b_baseline_summary": "docs/experiments/results/math16_pilot02_qwen4b_evaluation_v4_r001/overall_summary.json",
    "qwen4b_primary_healer_summary": "docs/experiments/results/math16_pilot02_qwen4b_healer_v4_r001/overall_summary.json",
    "qwen4b_corrected_chain_audit": "docs/experiments/audits/math16_pilot02_qwen4b_posthoc_corrected_chain_freeze_v1.json",
    "qwen9b_baseline_summary": "docs/experiments/results/math16_pilot02_qwen9b_evaluation_v4_r001/overall_summary.json",
    "qwen9b_eligibility_summary": "docs/experiments/results/math16_pilot02_qwen9b_healer_eligibility_v4_r001/eligibility_summary.json",
    "tier1_paired_summary": "docs/experiments/results/math16_pilot02_qwen4b_vs_qwen9b_tier1_paired_analysis_v1/overall_paired_summary.json",
    "fraction_reconciliation_summary": "docs/experiments/audits/math16_pilot02_fraction_pair_reconciliation_v1/reconciliation_summary.json",
    "fraction_mechanism_audit": "docs/experiments/results/math16_pilot02_fraction_9b_only_pass_mechanism_audit_v1/audit_report.md",
    "family_revalidation_summary": "docs/experiments/audits/math16_pilot02_nonfraction_family_table_revalidation_v1/rebuilt_family_tables.json",
    "qwen4b_ab2d_anomaly_audit": "docs/experiments/audits/math16_pilot02_qwen4b_ab2d_api_anomaly_diagnosis_v1.json",
    "ce115_spec_vs_assembly_comparison": "docs/experiments/results/ce115_ab2d_spec_vs_assembly_comparison.json",
    "test_figure_spec": "tests/test_math16_pilot02_figure_spec.py",
    "test_jury_qa": "tests/test_math16_pilot02_jury_qa.py",
    "test_tier1_paired_analysis": "tests/test_math16_pilot02_tier1_paired_analysis.py",
    "test_fraction_reconciliation": "tests/test_math16_pilot02_fraction_pair_reconciliation.py",
    "test_family_revalidation": "tests/test_math16_pilot02_family_tables_revalidation.py",
}


def compute_sha256(rel_path: str) -> str:
    abs_path = ROOT / rel_path
    if not abs_path.exists():
        raise FileNotFoundError(f"File not found for hashing: {abs_path}")
    h = hashlib.sha256()
    with open(abs_path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Compute SHA256 closure
    sha_closure = {
        "starting_head_commit": "5c15b0aee0ef0d4bfa0439c8d0759ed0e4e2af49",
        "frozen_at_utc": "2026-07-22T13:28:00Z",
        "hashes": {key: {"rel_path": rel_p, "sha256": compute_sha256(rel_p)} for key, rel_p in FILES_TO_HASH.items()},
    }

    # 2. Frozen Numeric Claims
    frozen_numeric_claims = {
        "gemini_primary": {
            "baseline_pass": 289,
            "baseline_total": 320,
            "pass_rate_pct": 90.31,
            "eligible": 0,
            "primary_final": 289,
        },
        "gemini_posthoc": {
            "hybrid_final": 306,
            "pass_rate_pct": 95.63,
            "spec_posthoc_condition": "80/80",
            "posthoc_only": True,
        },
        "qwen_4b": {
            "baseline_pass": 78,
            "baseline_fail": 242,
            "pass_rate_pct": 24.38,
            "eligible": 10,
            "primary_rescue": 5,
            "primary_final": 83,
            "primary_pass_rate_pct": 25.94,
            "posthoc_rescue": 6,
            "posthoc_final": 84,
            "posthoc_pass_rate_pct": 26.25,
            "observed_regression": 0,
        },
        "qwen_9b": {
            "baseline_pass": 101,
            "baseline_fail": 219,
            "pass_rate_pct": 31.56,
            "eligible": 0,
            "noneligible": 214,
            "ambiguous_entry_point_abstain": 5,
            "final": 101,
            "observed_regression": 0,
        },
        "tier1_overall": {
            "BOTH_PASS": 52,
            "FOUR_B_ONLY": 26,
            "NINE_B_ONLY": 49,
            "BOTH_FAIL": 193,
            "TOTAL": 320,
            "net_cell_gain": 23,
            "paired_risk_difference": 0.071875,
            "exact_mcnemar_p": 0.010582,
            "task_clustered_bootstrap_ci": [-0.0094, 0.1438],
        },
        "family_tables": {
            "column_order": ["BOTH_PASS", "FOUR_B_ONLY", "NINE_B_ONLY", "BOTH_FAIL"],
            "Integer": {"BOTH_PASS": 29, "FOUR_B_ONLY": 1, "NINE_B_ONLY": 13, "BOTH_FAIL": 37, "exact_mcnemar_p": 0.001831},
            "Polynomial": {"BOTH_PASS": 3, "FOUR_B_ONLY": 13, "NINE_B_ONLY": 6, "BOTH_FAIL": 58, "exact_mcnemar_p": 0.167089},
            "Radical": {"BOTH_PASS": 10, "FOUR_B_ONLY": 5, "NINE_B_ONLY": 9, "BOTH_FAIL": 56, "exact_mcnemar_p": 0.423950},
            "Fraction": {"BOTH_PASS": 10, "FOUR_B_ONLY": 7, "NINE_B_ONLY": 21, "BOTH_FAIL": 42, "exact_mcnemar_p": 0.012541},
        },
    }

    # 3. Primary / Post-hoc Accounting
    primary_posthoc_accounting = {
        "gemini": {
            "primary_score": "289/320",
            "posthoc_score": "306/320 (Hybrid)",
            "rule": "289/320 is the sole Primary pre-registered score. 306/320 is Post-hoc mechanism verification.",
            "prompt_spec_rule": "Ab2d+api (78/80) and Ab2d+spec-v1 (63/80) are Primary. Post-hoc spec-v2 (80/80) cannot enter primary 4-condition bar chart.",
        },
        "qwen_4b": {
            "primary_score": "83/320 (Primary rescue = 5)",
            "posthoc_score": "84/320 (Post-hoc rescue = 6)",
            "rule": "83/320 is the sole pre-registered Primary baseline+healer result. 84/320 is Post-hoc corrected-chain replay.",
            "visual_rule": "Primary rescue = 5 shown in solid bar; Post-hoc rescue = 6 shown in dashed overlay only.",
        },
        "default_reporting_policy": "All formal reports, One-Pager, Poster, and Slides default to Primary figures.",
    }

    # 4. Category Status
    category_status = {
        "CATEGORY_A_STATUS": "CATEGORY_A_COMPLETED_WITH_INTERPRETATION_LIMITATIONS",
        "CATEGORY_B_QA_STATUS": "CATEGORY_B_QA_COMPLETED",
        "CATEGORY_B_FIGURE_SPEC_STATUS": "CATEGORY_B_FIGURE_SPEC_COMPLETED",
        "CATEGORY_B_ACTUAL_FIGURES_STATUS": "CATEGORY_B_ACTUAL_FIGURES_PENDING",
        "ONE_PAGER_STATUS": "ONE_PAGER_PENDING",
        "FINAL_REPORT_STATUS": "FINAL_REPORT_PENDING",
        "POSTER_STATUS": "POSTER_PENDING",
        "ORAL_SLIDES_STATUS": "ORAL_SLIDES_PENDING",
    }

    # 5. Milestone Manifest
    evidence_complete_manifest = {
        "manifest_id": "math16_pilot02_evidence_complete_v1_manifest",
        "version": "1.0.0",
        "project": "Ivan旺宏科學展 HealerBoundary",
        "repository": "C:\\Projects\\MathProject_AST_Research_HealerBoundary",
        "git_commit": "5c15b0aee0ef0d4bfa0439c8d0759ed0e4e2af49",
        "frozen_at_utc": "2026-07-22T13:28:00Z",
        "author": "Antigravity Research HealerBoundary Agent",
        "milestone_status": "EVIDENCE_COMPLETE_V1_FROZEN",
        "presentation_phase_opened": True,
        "files": [
            "evidence_complete_manifest.json",
            "frozen_numeric_claims.json",
            "primary_posthoc_accounting.json",
            "source_sha_closure.json",
            "category_status.json",
            "interpretation_limitations.md",
            "presentation_handoff.md",
            "evidence_complete_report.md",
        ],
    }

    # Write files
    with open(OUT_DIR / "source_sha_closure.json", "w", encoding="utf-8") as f:
        json.dump(sha_closure, f, ensure_ascii=False, indent=2)

    with open(OUT_DIR / "frozen_numeric_claims.json", "w", encoding="utf-8") as f:
        json.dump(frozen_numeric_claims, f, ensure_ascii=False, indent=2)

    with open(OUT_DIR / "primary_posthoc_accounting.json", "w", encoding="utf-8") as f:
        json.dump(primary_posthoc_accounting, f, ensure_ascii=False, indent=2)

    with open(OUT_DIR / "category_status.json", "w", encoding="utf-8") as f:
        json.dump(category_status, f, ensure_ascii=False, indent=2)

    with open(OUT_DIR / "evidence_complete_manifest.json", "w", encoding="utf-8") as f:
        json.dump(evidence_complete_manifest, f, ensure_ascii=False, indent=2)

    print("Evidence Complete Milestone v1 JSON files generated successfully!")


if __name__ == "__main__":
    main()
