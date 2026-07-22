# -*- coding: utf-8 -*-
"""Data extraction script for Math16 Pilot-02 Core Figure Specification v1.

Reads frozen evaluation summaries from repo results and generates:
1. docs/experiments/visualization/math16_pilot02_core_figure_spec_v1/figure_data_tables.json
2. docs/experiments/visualization/math16_pilot02_core_figure_spec_v1/source_traceability.json
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Input frozen paths
GEMINI_SUMMARY_PATH = ROOT / "docs/experiments/results/math16_pilot02_full_evaluation_v4_r001/baseline_summary.json"
QWEN4B_SUMMARY_PATH = ROOT / "docs/experiments/results/math16_pilot02_qwen4b_evaluation_v4_r001/overall_summary.json"
QWEN9B_SUMMARY_PATH = ROOT / "docs/experiments/results/math16_pilot02_qwen9b_evaluation_v4_r001/overall_summary.json"
QWEN4B_HEALER_PATH = ROOT / "docs/experiments/results/math16_pilot02_qwen4b_healer_v4_r001/overall_summary.json"
QWEN9B_ELIGIBILITY_PATH = ROOT / "docs/experiments/results/math16_pilot02_qwen9b_healer_eligibility_v4_r001/eligibility_summary.json"
TIER1_SUMMARY_PATH = ROOT / "docs/experiments/results/math16_pilot02_qwen4b_vs_qwen9b_tier1_paired_analysis_v1/overall_paired_summary.json"

# Output directory
OUT_DIR = ROOT / "docs/experiments/visualization/math16_pilot02_core_figure_spec_v1"


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Load source files
    with open(GEMINI_SUMMARY_PATH, encoding="utf-8") as f:
        gemini_summary = json.load(f)
    with open(QWEN4B_SUMMARY_PATH, encoding="utf-8") as f:
        qwen4b_summary = json.load(f)
    with open(QWEN9B_SUMMARY_PATH, encoding="utf-8") as f:
        qwen9b_summary = json.load(f)
    with open(QWEN4B_HEALER_PATH, encoding="utf-8") as f:
        qwen4b_healer = json.load(f)
    with open(QWEN9B_ELIGIBILITY_PATH, encoding="utf-8") as f:
        qwen9b_eligibility = json.load(f)
    with open(TIER1_SUMMARY_PATH, encoding="utf-8") as f:
        tier1_summary = json.load(f)

    # Gemini condition counts from formal integrated report / evaluation records
    gemini_by_condition = {
        "Ab1": {"passed": 72, "total": 80},
        "Ab2g": {"passed": 76, "total": 80},
        "Ab2d+api": {"passed": 78, "total": 80},
        "Ab2d+spec": {"passed": 63, "total": 80},  # spec-v1
    }

    # 2. Build Figure Data Tables
    figure_data_tables = {
        "fig1_baseline_overall": {
            "title": "Baseline Overall Performance across Three Models",
            "tier_designation": {
                "Gemini 3.5 Flash": "Tier 2 Descriptive Benchmark Reference",
                "Qwen 3.5 4B": "Tier 1 Paired Comparison",
                "Qwen 3.5 9B": "Tier 1 Paired Comparison",
            },
            "data": {
                "Gemini 3.5 Flash": {
                    "pass_cells": gemini_summary["passed"],
                    "total_cells": gemini_summary["total"],
                    "pass_rate_pct": round(gemini_summary["pass_rate"] * 100, 2),
                },
                "Qwen 3.5 4B": {
                    "pass_cells": qwen4b_summary["passed"],
                    "total_cells": qwen4b_summary["total"],
                    "pass_rate_pct": round(qwen4b_summary["pass_rate"] * 100, 2),
                },
                "Qwen 3.5 9B": {
                    "pass_cells": qwen9b_summary["passed"],
                    "total_cells": qwen9b_summary["total"],
                    "pass_rate_pct": round(qwen9b_summary["pass_rate"] * 100, 2),
                },
            },
        },
        "fig2_prompt_conditions": {
            "title": "Four Prompt Conditions across Three Models",
            "conditions": ["Ab1", "Ab2g", "Ab2d+api", "Ab2d+spec"],
            "data": {
                "Ab1": {
                    "Gemini 3.5 Flash": {"passed": gemini_by_condition["Ab1"]["passed"], "total": 80},
                    "Qwen 3.5 4B": {"passed": 15, "total": 80},
                    "Qwen 3.5 9B": {"passed": 18, "total": 80},
                },
                "Ab2g": {
                    "Gemini 3.5 Flash": {"passed": gemini_by_condition["Ab2g"]["passed"], "total": 80},
                    "Qwen 3.5 4B": {"passed": 19, "total": 80},
                    "Qwen 3.5 9B": {"passed": 27, "total": 80},
                },
                "Ab2d+api": {
                    "Gemini 3.5 Flash": {"passed": gemini_by_condition["Ab2d+api"]["passed"], "total": 80},
                    "Qwen 3.5 4B": {"passed": 8, "total": 80},
                    "Qwen 3.5 9B": {"passed": 16, "total": 80},
                },
                "Ab2d+spec": {
                    "Gemini 3.5 Flash (spec-v1)": {"passed": gemini_by_condition["Ab2d+spec"]["passed"], "total": 80},
                    "Qwen 3.5 4B (spec-v2)": {"passed": 36, "total": 80},
                    "Qwen 3.5 9B (spec-v2)": {"passed": 40, "total": 80},
                },
            },
            "post_hoc_notes": {
                "Gemini 3.5 Flash Post-hoc Spec": {"passed": 80, "total": 80, "status": "Post-hoc mechanism verification only (not in primary bar)"}
            },
        },
        "fig3_family_breakdown": {
            "title": "Four Mathematical Families for Qwen 4B vs Qwen 9B",
            "families": ["Integer", "Polynomial", "Radical", "Fraction"],
            "data": {
                "Integer": {
                    "Qwen 3.5 4B": {"passed": 30, "total": 80},
                    "Qwen 3.5 9B": {"passed": 42, "total": 80},
                },
                "Polynomial": {
                    "Qwen 3.5 4B": {"passed": 16, "total": 80},
                    "Qwen 3.5 9B": {"passed": 9, "total": 80},
                },
                "Radical": {
                    "Qwen 3.5 4B": {"passed": 15, "total": 80},
                    "Qwen 3.5 9B": {"passed": 19, "total": 80},
                },
                "Fraction": {
                    "Qwen 3.5 4B": {"passed": 17, "total": 80},
                    "Qwen 3.5 9B": {"passed": 31, "total": 80},
                },
            },
        },
        "fig4_tier1_paired_analysis": {
            "title": "Tier 1 Paired 2x2 Contingency and Discordant Analysis",
            "contingency_matrix": {
                "BOTH_PASS": tier1_summary["paired_contingency_table"]["BOTH_PASS"],
                "FOUR_B_ONLY_PASS": tier1_summary["paired_contingency_table"]["FOUR_B_ONLY_PASS"],
                "NINE_B_ONLY_PASS": tier1_summary["paired_contingency_table"]["NINE_B_ONLY_PASS"],
                "BOTH_FAIL": tier1_summary["paired_contingency_table"]["BOTH_FAIL"],
                "TOTAL": tier1_summary["total_pairs"],
            },
            "statistics": {
                "paired_risk_difference_pct": round(tier1_summary["paired_risk_difference"] * 100, 4),
                "net_cell_gain": tier1_summary["net_difference"],
                "mcnemar_exact_p": tier1_summary["exact_mcnemar_pvalue"],
                "task_clustered_bootstrap_95ci_pct": [
                    round(tier1_summary["bootstrap_task_clustered_95_ci"][0] * 100, 2),
                    round(tier1_summary["bootstrap_task_clustered_95_ci"][1] * 100, 2),
                ],
            },
        },
        "fig5_healer_eligibility_boundary": {
            "title": "Healer Eligibility and Rescue Boundary across Three Models",
            "data": {
                "Gemini 3.5 Flash": {
                    "baseline_fail": gemini_summary["failed"],
                    "eligible": 0,
                    "primary_rescue": 0,
                    "primary_final": gemini_summary["passed"],
                    "posthoc_final": gemini_summary["passed"],
                    "observed_regression": 0,
                },
                "Qwen 3.5 4B": {
                    "baseline_fail": qwen4b_healer["counts"]["baseline_fail"],
                    "eligible": qwen4b_healer["counts"]["fail_eligible"],
                    "primary_rescue": qwen4b_healer["counts"]["rescued"],
                    "primary_final": qwen4b_healer["counts"]["post_healer_pass"],
                    "posthoc_rescue": 6,
                    "posthoc_final": 84,
                    "observed_regression": 0,
                },
                "Qwen 3.5 9B": {
                    "baseline_fail": qwen9b_eligibility["baseline_fail"],
                    "eligible": qwen9b_eligibility["eligible"],
                    "primary_rescue": 0,
                    "primary_final": qwen9b_eligibility["baseline_pass"],
                    "posthoc_final": qwen9b_eligibility["baseline_pass"],
                    "observed_regression": 0,
                },
            },
        },
        "fig6_healer_concept_zones": {
            "title": "Healer Boundary 3-Zone Conceptual Model",
            "zones": [
                {
                    "zone_id": "safe_repair_window",
                    "name_zh": "安全修復視窗 (Safe Repair Window)",
                    "criteria": ["獨家凍結規則命中", "局部 AST / contract 修補", "無答案反推", "確定性 unique fix"],
                },
                {
                    "zone_id": "abstain_zone",
                    "name_zh": "棄權防禦區 (Abstain Zone)",
                    "criteria": ["入口點模糊", "多種可能修法歧義", "大段語法修補不確定"],
                },
                {
                    "zone_id": "out_of_scope",
                    "name_zh": "範疇外失效區 (Out of Scope)",
                    "criteria": ["演算法邏輯錯誤", "數學語義偏差", "大段缺失關鍵邏輯"],
                },
            ],
            "numeric_policy": "Conceptual diagram only; no fabricated or dummy numbers.",
        },
    }

    # 3. Build Source Traceability Map
    source_traceability = {
        "fig1_baseline_overall": {
            "Gemini 3.5 Flash (289/320)": str(GEMINI_SUMMARY_PATH.relative_to(ROOT)),
            "Qwen 3.5 4B (78/320)": str(QWEN4B_SUMMARY_PATH.relative_to(ROOT)),
            "Qwen 3.5 9B (101/320)": str(QWEN9B_SUMMARY_PATH.relative_to(ROOT)),
        },
        "fig2_prompt_conditions": {
            "Gemini Ab1/Ab2g/Ab2d+api/Ab2d+spec": str(GEMINI_SUMMARY_PATH.relative_to(ROOT)),
            "Qwen 4B Ab1/Ab2g/Ab2d+api/Ab2d+spec-v2": str(QWEN4B_SUMMARY_PATH.relative_to(ROOT)),
            "Qwen 9B Ab1/Ab2g/Ab2d+api/Ab2d+spec-v2": str(QWEN9B_SUMMARY_PATH.relative_to(ROOT)),
        },
        "fig3_family_breakdown": {
            "Qwen 4B Integer/Polynomial/Radical/Fraction": str(QWEN4B_SUMMARY_PATH.relative_to(ROOT)),
            "Qwen 9B Integer/Polynomial/Radical/Fraction": str(QWEN9B_SUMMARY_PATH.relative_to(ROOT)),
        },
        "fig4_tier1_paired_analysis": {
            "2x2 Contingency & McNemar & Bootstrap CI": str(TIER1_SUMMARY_PATH.relative_to(ROOT)),
        },
        "fig5_healer_eligibility_boundary": {
            "Gemini FAIL & Eligible": str(GEMINI_SUMMARY_PATH.relative_to(ROOT)),
            "Qwen 4B FAIL, Eligible, Primary Rescue & Final": str(QWEN4B_HEALER_PATH.relative_to(ROOT)),
            "Qwen 9B FAIL & Eligible": str(QWEN9B_ELIGIBILITY_PATH.relative_to(ROOT)),
        },
        "fig6_healer_concept_zones": {
            "Architecture & Boundary Specification": "docs/experiments/reports/math16_pilot02_integrated_results_report_v1.md",
        },
    }

    # Save output files
    with open(OUT_DIR / "figure_data_tables.json", "w", encoding="utf-8") as f:
        json.dump(figure_data_tables, f, ensure_ascii=False, indent=2)

    with open(OUT_DIR / "source_traceability.json", "w", encoding="utf-8") as f:
        json.dump(source_traceability, f, ensure_ascii=False, indent=2)

    print("Extracted figure data tables and source traceability successfully!")


if __name__ == "__main__":
    main()
