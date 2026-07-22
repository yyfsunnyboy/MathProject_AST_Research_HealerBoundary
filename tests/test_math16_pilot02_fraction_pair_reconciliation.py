# -*- coding: utf-8 -*-
"""Verification tests for Fraction Pair Reconciliation."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RECONCILE_DIR = (
    ROOT / "docs/experiments/audits/math16_pilot02_fraction_pair_reconciliation_v1"
)
TIER1_DIR = (
    ROOT / "docs/experiments/results/math16_pilot02_qwen4b_vs_qwen9b_tier1_paired_analysis_v1"
)
REPORT_PATH = ROOT / "docs/experiments/reports/math16_pilot02_integrated_results_report_v1.md"


def test_reconciliation_artifacts_exist():
    required_files = [
        "rebuilt_fraction_pair_ledger.jsonl",
        "tier1_fraction_sets.json",
        "fraction_audit_sets.json",
        "set_differences.json",
        "seven_cell_root_cause.json",
        "script_logic_comparison.md",
        "reconciliation_summary.json",
        "audit_report.md",
        "audit_manifest.json",
    ]
    for name in required_files:
        assert (RECONCILE_DIR / name).exists(), f"Missing reconciliation file: {name}"


def test_rebuilt_fraction_pair_counts():
    ledger_path = RECONCILE_DIR / "rebuilt_fraction_pair_ledger.jsonl"
    rows = [json.loads(line) for line in ledger_path.read_text(encoding="utf-8").splitlines() if line.strip()]

    assert len(rows) == 80
    assert len({r["pair_id"] for r in rows}) == 80

    both_pass = sum(1 for r in rows if r["pair_category"] == "BOTH_PASS")
    four_b_only = sum(1 for r in rows if r["pair_category"] == "FOUR_B_ONLY_PASS")
    nine_b_only = sum(1 for r in rows if r["pair_category"] == "NINE_B_ONLY_PASS")
    both_fail = sum(1 for r in rows if r["pair_category"] == "BOTH_FAIL")

    assert both_pass == 10
    assert four_b_only == 7
    assert nine_b_only == 21
    assert both_fail == 42

    assert both_pass + four_b_only == 17
    assert both_pass + nine_b_only == 31
    assert nine_b_only - four_b_only == 14


def test_zero_set_mismatches():
    diffs = json.loads((RECONCILE_DIR / "set_differences.json").read_text(encoding="utf-8"))
    assert diffs["reconciliation_status"] == "ZERO_SET_MISMATCHES"
    assert len(diffs["rebuilt_vs_tier1_4b_only_mismatches"]) == 0
    assert len(diffs["rebuilt_vs_tier1_9b_only_mismatches"]) == 0
    assert len(diffs["rebuilt_vs_audit_9b_only_mismatches"]) == 0


def test_overall_table_untouched():
    overall = json.loads((TIER1_DIR / "overall_paired_summary.json").read_text(encoding="utf-8"))
    assert overall["total_pairs"] == 320
    assert overall["qwen4b_baseline_pass"] == 78
    assert overall["qwen9b_baseline_pass"] == 101
    assert overall["net_difference"] == 23
    assert overall["paired_contingency_table"]["BOTH_PASS"] == 52
    assert overall["paired_contingency_table"]["FOUR_B_ONLY_PASS"] == 26
    assert overall["paired_contingency_table"]["NINE_B_ONLY_PASS"] == 49
    assert overall["paired_contingency_table"]["BOTH_FAIL"] == 193


def test_integrated_report_reconciliation_declaration():
    report_text = REPORT_PATH.read_text(encoding="utf-8")
    assert "Fraction Family 9B 獨勝 (NINE_B_ONLY_PASS) 機制分布診斷" in report_text
    assert "COMPLETED_WITH_INTERPRETATION_LIMITATIONS" in report_text
