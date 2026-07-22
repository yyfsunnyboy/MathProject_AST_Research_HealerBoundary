# -*- coding: utf-8 -*-
"""Verification script for Math16 Pilot-02 Integrated Results Report consistency.

Reads formal evidence JSON files and validates numbers against the report.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

GEMINI_BASELINE_PATH = (
    ROOT / "docs/experiments/results/math16_pilot02_full_evaluation_v4_r001/baseline_summary.json"
)
QWEN4B_BASELINE_PATH = (
    ROOT / "docs/experiments/results/math16_pilot02_qwen4b_evaluation_v4_r001/overall_summary.json"
)
QWEN4B_PRIMARY_HEALER_PATH = (
    ROOT / "docs/experiments/results/math16_pilot02_qwen4b_healer_v4_r001/overall_summary.json"
)
QWEN4B_POSTHOC_FREEZE_PATH = (
    ROOT / "docs/experiments/audits/math16_pilot02_qwen4b_posthoc_corrected_chain_freeze_v1.json"
)
QWEN9B_BASELINE_PATH = (
    ROOT / "docs/experiments/results/math16_pilot02_qwen9b_evaluation_v4_r001/overall_summary.json"
)
QWEN9B_ELIGIBILITY_PATH = (
    ROOT
    / "docs/experiments/results/math16_pilot02_qwen9b_healer_eligibility_v4_r001/eligibility_summary.json"
)
REPORT_PATH = ROOT / "docs/experiments/reports/math16_pilot02_integrated_results_report_v1.md"


def test_evidence_files_exist():
    assert GEMINI_BASELINE_PATH.exists()
    assert QWEN4B_BASELINE_PATH.exists()
    assert QWEN4B_PRIMARY_HEALER_PATH.exists()
    assert QWEN4B_POSTHOC_FREEZE_PATH.exists()
    assert QWEN9B_BASELINE_PATH.exists()
    assert QWEN9B_ELIGIBILITY_PATH.exists()
    assert REPORT_PATH.exists()


def test_reconcile_evidence_numbers():
    # 1. Gemini
    gemini_summary = json.loads(GEMINI_BASELINE_PATH.read_text(encoding="utf-8"))
    gemini_baseline_passed = gemini_summary["passed"]
    gemini_total = gemini_summary["total"]
    assert gemini_total == 320
    assert gemini_baseline_passed == 289
    gemini_eligible = 0
    gemini_final = gemini_baseline_passed

    # 2. Qwen 4B
    qwen4b_base_summary = json.loads(QWEN4B_BASELINE_PATH.read_text(encoding="utf-8"))
    qwen4b_baseline_passed = qwen4b_base_summary["passed"]
    qwen4b_total = qwen4b_base_summary["total"]
    assert qwen4b_total == 320
    assert qwen4b_baseline_passed == 78

    qwen4b_primary_summary = json.loads(QWEN4B_PRIMARY_HEALER_PATH.read_text(encoding="utf-8"))
    qwen4b_eligible = qwen4b_primary_summary["counts"]["fail_eligible"]
    qwen4b_primary_rescue = qwen4b_primary_summary["counts"]["rescued"]
    qwen4b_primary_final = qwen4b_primary_summary["counts"]["post_healer_pass"]
    assert qwen4b_eligible == 10
    assert qwen4b_primary_rescue == 5
    assert qwen4b_primary_final == 83

    qwen4b_posthoc_freeze = json.loads(QWEN4B_POSTHOC_FREEZE_PATH.read_text(encoding="utf-8"))
    qwen4b_posthoc_rescue = qwen4b_posthoc_freeze["corrected_rescued"]
    qwen4b_posthoc_final = int(qwen4b_posthoc_freeze["corrected_post_healer_pass_fraction"].split("/")[0])
    assert qwen4b_posthoc_rescue == 6
    assert qwen4b_posthoc_final == 84

    # 3. Qwen 9B
    qwen9b_base_summary = json.loads(QWEN9B_BASELINE_PATH.read_text(encoding="utf-8"))
    qwen9b_baseline_passed = qwen9b_base_summary["passed"]
    qwen9b_baseline_failed = qwen9b_base_summary["failed"]
    qwen9b_total = qwen9b_base_summary["total"]
    assert qwen9b_total == 320
    assert qwen9b_baseline_passed == 101
    assert qwen9b_baseline_failed == 219

    qwen9b_elig_summary = json.loads(QWEN9B_ELIGIBILITY_PATH.read_text(encoding="utf-8"))
    qwen9b_eligible = qwen9b_elig_summary["eligible"]
    qwen9b_noneligible = qwen9b_elig_summary["noneligible_no_rule_triggered"]
    qwen9b_ambiguous = qwen9b_elig_summary["abstain_ambiguous_entry_point"]
    qwen9b_final = qwen9b_baseline_passed
    assert qwen9b_eligible == 0
    assert qwen9b_noneligible == 214
    assert qwen9b_ambiguous == 5
    assert qwen9b_final == 101

    # Check text consistency in report
    report_text = REPORT_PATH.read_text(encoding="utf-8")
    assert "289" in report_text
    assert "78" in report_text
    assert "101" in report_text
    assert "320" in report_text
    assert "960" in report_text
    assert "83/320" in report_text
    assert "84/320" in report_text
    assert "219" in report_text
    assert "214" in report_text
    assert "MATH16_PILOT02_INTEGRATED_RESULTS_REPORT_V1_COMPLETED" in report_text

    # Assertions for non-overclaiming rules
    assert "100%安全" not in report_text
    assert "絕對安全" not in report_text
    assert "零倒退防禦" not in report_text
    assert "Polynomial 異常未污染整體比較" not in report_text
    assert "100%深層數學邏輯錯誤" not in report_text

    # Assertions for tiering and methodology
    assert "Tier 1" in report_text
    assert "Tier 2" in report_text
    assert "only-Python" in report_text
    assert "LaTeX" in report_text

    # Assertions for gap inventory categories
    assert "REQUIRED_BEFORE_FINAL" in report_text
    assert "REQUIRED_FOR_PRESENTATION" in report_text
    assert "OPTIONAL" in report_text
