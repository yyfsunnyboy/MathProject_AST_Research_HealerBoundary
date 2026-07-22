# -*- coding: utf-8 -*-
"""Verification tests for Tier 1 Paired Analysis (Qwen 4B vs Qwen 9B)."""
from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PAIRED_DIR = (
    ROOT / "docs/experiments/results/math16_pilot02_qwen4b_vs_qwen9b_tier1_paired_analysis_v1"
)
REPORT_PATH = ROOT / "docs/experiments/reports/math16_pilot02_integrated_results_report_v1.md"


def test_paired_artifacts_exist():
    required_files = [
        "paired_cell_ledger.jsonl",
        "overall_paired_summary.json",
        "condition_paired_summary.json",
        "family_paired_summary.json",
        "seed_stability_summary.json",
        "task_level_summary.json",
        "bootstrap_summary.json",
        "analysis_manifest.json",
        "analysis_report.md",
    ]
    for name in required_files:
        assert (PAIRED_DIR / name).exists(), f"Missing required file: {name}"


def test_mcnemar_exact_small_example():
    from scripts.analyze_math16_pilot02_qwen4b_vs_qwen9b_tier1_paired import (
        compute_exact_mcnemar_pvalue,
    )

    # Test symmetric discordant pairs b=5, c=5 -> p-value = 1.0
    assert compute_exact_mcnemar_pvalue(5, 5) == 1.0

    # Test extreme discordant pairs b=0, c=10 -> p-value = 2 * (1/2)^10 = 0.001953125
    assert math.isclose(compute_exact_mcnemar_pvalue(0, 10), 2.0 / 1024.0, abs_tol=1e-6)


def test_paired_ledger_geometry_and_counts():
    ledger_path = PAIRED_DIR / "paired_cell_ledger.jsonl"
    rows = [json.loads(line) for line in ledger_path.read_text(encoding="utf-8").splitlines() if line.strip()]

    assert len(rows) == 320
    assert len({r["pair_id"] for r in rows}) == 320
    assert len({r["key"] for r in rows}) == 320

    both_pass = sum(1 for r in rows if r["pair_category"] == "BOTH_PASS")
    four_b_only = sum(1 for r in rows if r["pair_category"] == "FOUR_B_ONLY_PASS")
    nine_b_only = sum(1 for r in rows if r["pair_category"] == "NINE_B_ONLY_PASS")
    both_fail = sum(1 for r in rows if r["pair_category"] == "BOTH_FAIL")

    assert both_pass == 52
    assert four_b_only == 26
    assert nine_b_only == 49
    assert both_fail == 193

    q4b_pass = both_pass + four_b_only
    q9b_pass = both_pass + nine_b_only

    assert q4b_pass == 78
    assert q9b_pass == 101
    assert nine_b_only - four_b_only == 23


def test_subgroup_denominators():
    ledger_path = PAIRED_DIR / "paired_cell_ledger.jsonl"
    rows = [json.loads(line) for line in ledger_path.read_text(encoding="utf-8").splitlines() if line.strip()]

    # Condition denominators = 80
    from collections import Counter

    cond_counts = Counter(r["condition"] for r in rows)
    for cond in ["ab1", "ab2g", "ab2d", "ab2d_spec_v2"]:
        assert cond_counts[cond] == 80

    # Family denominators = 80
    fam_counts = Counter(r["family"] for r in rows)
    for fam in ["integer", "polynomial", "radical", "fraction"]:
        assert fam_counts[fam] == 80

    # Seed denominators = 64
    seed_counts = Counter(r["seed"] for r in rows)
    for s in [2026071301, 2026072001, 2026072002, 2026072003, 2026072004]:
        assert seed_counts[s] == 64

    # Task denominators = 20
    task_counts = Counter(r["task_id"] for r in rows)
    assert len(task_counts) == 16
    for t, cnt in task_counts.items():
        assert cnt == 20


def test_overall_summary_values():
    summary = json.loads((PAIRED_DIR / "overall_paired_summary.json").read_text(encoding="utf-8"))
    assert summary["total_pairs"] == 320
    assert summary["qwen4b_baseline_pass"] == 78
    assert summary["qwen9b_baseline_pass"] == 101
    assert summary["net_difference"] == 23
    assert summary["paired_contingency_table"]["BOTH_PASS"] == 52
    assert summary["paired_contingency_table"]["FOUR_B_ONLY_PASS"] == 26
    assert summary["paired_contingency_table"]["NINE_B_ONLY_PASS"] == 49
    assert summary["paired_contingency_table"]["BOTH_FAIL"] == 193
    assert math.isclose(summary["paired_risk_difference"], 0.071875, abs_tol=1e-5)
    assert math.isclose(summary["exact_mcnemar_pvalue"], 0.010582117051705276, abs_tol=1e-5)


def test_integrated_report_contains_paired_statistics():
    report_text = REPORT_PATH.read_text(encoding="utf-8")
    assert "Tier 1 (Qwen 4B vs Qwen 9B) 正式 320-Cell 配對列聯表與統計檢定" in report_text
    assert "0.0106" in report_text or "0.01058" in report_text
    assert "+7.1875%" in report_text or "7.18" in report_text
    assert "Discordant Pairs" in report_text
    assert "Task-Clustered Bootstrap 95% CI" in report_text
