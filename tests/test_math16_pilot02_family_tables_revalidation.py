# -*- coding: utf-8 -*-
"""Verification tests for Four Families Table Revalidation and Closure."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

AUDIT_DIR = (
    ROOT / "docs/experiments/audits/math16_pilot02_nonfraction_family_table_revalidation_v1"
)
TIER1_DIR = (
    ROOT / "docs/experiments/results/math16_pilot02_qwen4b_vs_qwen9b_tier1_paired_analysis_v1"
)
REPORT_PATH = ROOT / "docs/experiments/reports/math16_pilot02_integrated_results_report_v1.md"


def test_revalidation_artifacts_exist():
    required_files = [
        "rebuilt_integer_pair_ledger.jsonl",
        "rebuilt_polynomial_pair_ledger.jsonl",
        "rebuilt_radical_pair_ledger.jsonl",
        "rebuilt_family_tables.json",
        "source_comparison.json",
        "family_to_overall_closure.json",
        "revalidation_summary.json",
        "audit_report.md",
        "audit_manifest.json",
    ]
    for name in required_files:
        assert (AUDIT_DIR / name).exists(), f"Missing revalidation file: {name}"


def test_family_tables_exact_match():
    rebuilt = json.loads((AUDIT_DIR / "rebuilt_family_tables.json").read_text(encoding="utf-8"))

    # Integer
    assert rebuilt["integer"]["BOTH_PASS"] == 29
    assert rebuilt["integer"]["FOUR_B_ONLY_PASS"] == 1
    assert rebuilt["integer"]["NINE_B_ONLY_PASS"] == 13
    assert rebuilt["integer"]["BOTH_FAIL"] == 37

    # Polynomial
    assert rebuilt["polynomial"]["BOTH_PASS"] == 3
    assert rebuilt["polynomial"]["FOUR_B_ONLY_PASS"] == 13
    assert rebuilt["polynomial"]["NINE_B_ONLY_PASS"] == 6
    assert rebuilt["polynomial"]["BOTH_FAIL"] == 58

    # Radical
    assert rebuilt["radical"]["BOTH_PASS"] == 10
    assert rebuilt["radical"]["FOUR_B_ONLY_PASS"] == 5
    assert rebuilt["radical"]["NINE_B_ONLY_PASS"] == 9
    assert rebuilt["radical"]["BOTH_FAIL"] == 56

    # Fraction
    assert rebuilt["fraction"]["BOTH_PASS"] == 10
    assert rebuilt["fraction"]["FOUR_B_ONLY_PASS"] == 7
    assert rebuilt["fraction"]["NINE_B_ONLY_PASS"] == 21
    assert rebuilt["fraction"]["BOTH_FAIL"] == 42


def test_family_to_overall_closure_exact():
    closure = json.loads((AUDIT_DIR / "family_to_overall_closure.json").read_text(encoding="utf-8"))
    assert closure["is_closure_exact"] is True
    assert closure["family_sums"]["BOTH_PASS"] == 52
    assert closure["family_sums"]["FOUR_B_ONLY_PASS"] == 26
    assert closure["family_sums"]["NINE_B_ONLY_PASS"] == 49
    assert closure["family_sums"]["BOTH_FAIL"] == 193


def test_integrated_report_family_closure_section():
    report_text = REPORT_PATH.read_text(encoding="utf-8")
    assert "四大 Family 2×2 配對列聯表地面真值覆核與閉合" in report_text
    assert "COMPLETED_WITH_INTERPRETATION_LIMITATIONS" in report_text
