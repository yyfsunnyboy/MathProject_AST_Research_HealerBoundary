# -*- coding: utf-8 -*-
"""Verification tests for Fraction 9B-Only Pass Mechanism Audit."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

AUDIT_DIR = (
    ROOT / "docs/experiments/results/math16_pilot02_fraction_9b_only_pass_mechanism_audit_v1"
)
REPORT_PATH = ROOT / "docs/experiments/reports/math16_pilot02_integrated_results_report_v1.md"


def test_audit_artifacts_exist():
    required_files = [
        "fraction_9b_only_pass_ledger.jsonl",
        "task_distribution.json",
        "condition_distribution.json",
        "layer_distribution.json",
        "mechanism_distribution.json",
        "ab2d_api_overlap.json",
        "audit_manifest.json",
        "audit_report.md",
    ]
    for name in required_files:
        assert (AUDIT_DIR / name).exists(), f"Missing audit file: {name}"


def test_audit_ledger_counts_and_outcomes():
    ledger_path = AUDIT_DIR / "fraction_9b_only_pass_ledger.jsonl"
    rows = [json.loads(line) for line in ledger_path.read_text(encoding="utf-8").splitlines() if line.strip()]

    assert len(rows) == 21
    assert len({r["pair_id"] for r in rows}) == 21

    for r in rows:
        assert r["qwen4b_outcome"] == "FAILED"
        assert r["qwen9b_outcome"] == "PASSED"
        assert r["task_id"] in [
            "ce111_q05_exact_fraction_expression",
            "ce112_q12_independent_probability_fraction",
            "ce113_q01_negative_fraction_subtraction",
            "ce115_calc_exact_rational_expression_l1",
        ]


def test_audit_manifest_status():
    manifest = json.loads((AUDIT_DIR / "audit_manifest.json").read_text(encoding="utf-8"))
    assert manifest["nine_b_only_pass_c"] == 21
    assert manifest["four_b_only_pass_b"] == 7
    assert manifest["paired_net_difference"] == 14
    assert manifest["primary_verdict"] == "FRACTION_GAP_MAINLY_FORMAT_EXECUTION_RELATED"
    assert manifest["category_a_status"] == "COMPLETED_WITH_INTERPRETATION_LIMITATIONS"


def test_integrated_report_updated_with_fraction_audit():
    report_text = REPORT_PATH.read_text(encoding="utf-8")
    assert "Fraction Family 9B 獨勝 (NINE_B_ONLY_PASS) 機制分布診斷" in report_text
    assert "FRACTION_GAP_MAINLY_FORMAT_EXECUTION_RELATED" in report_text
    assert "Q19: 為什麼 Fraction family 的 9B 優勢最明顯" in report_text
    assert "COMPLETED_WITH_INTERPRETATION_LIMITATIONS" in report_text
