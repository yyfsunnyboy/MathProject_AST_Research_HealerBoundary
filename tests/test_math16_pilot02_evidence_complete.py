# -*- coding: utf-8 -*-
"""Targeted unit tests for Math16 Pilot-02 Evidence Complete Milestone v1."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MILESTONE_DIR = ROOT / "docs/experiments/milestones/math16_pilot02_evidence_complete_v1"
MANIFEST_PATH = MILESTONE_DIR / "evidence_complete_manifest.json"
NUMERIC_CLAIMS_PATH = MILESTONE_DIR / "frozen_numeric_claims.json"
ACCOUNTING_PATH = MILESTONE_DIR / "primary_posthoc_accounting.json"
SHA_CLOSURE_PATH = MILESTONE_DIR / "source_sha_closure.json"
CATEGORY_STATUS_PATH = MILESTONE_DIR / "category_status.json"
LIMITATIONS_PATH = MILESTONE_DIR / "interpretation_limitations.md"
HANDOFF_PATH = MILESTONE_DIR / "presentation_handoff.md"
REPORT_MILESTONE_PATH = MILESTONE_DIR / "evidence_complete_report.md"

INTEGRATED_REPORT_PATH = ROOT / "docs/experiments/reports/math16_pilot02_integrated_results_report_v1.md"


def test_milestone_files_exist():
    assert MILESTONE_DIR.exists()
    assert MANIFEST_PATH.exists()
    assert NUMERIC_CLAIMS_PATH.exists()
    assert ACCOUNTING_PATH.exists()
    assert SHA_CLOSURE_PATH.exists()
    assert CATEGORY_STATUS_PATH.exists()
    assert LIMITATIONS_PATH.exists()
    assert HANDOFF_PATH.exists()
    assert REPORT_MILESTONE_PATH.exists()


def test_frozen_numeric_claims_ground_truth():
    with open(NUMERIC_CLAIMS_PATH, encoding="utf-8") as f:
        claims = json.load(f)

    # Gemini Primary
    gemini = claims["gemini_primary"]
    assert gemini["baseline_pass"] == 289
    assert gemini["baseline_total"] == 320
    assert gemini["eligible"] == 0
    assert gemini["primary_final"] == 289

    # Gemini Post-hoc
    gemini_ph = claims["gemini_posthoc"]
    assert gemini_ph["hybrid_final"] == 306
    assert gemini_ph["spec_posthoc_condition"] == "80/80"
    assert gemini_ph["posthoc_only"] is True

    # Qwen 4B
    q4b = claims["qwen_4b"]
    assert q4b["baseline_pass"] == 78
    assert q4b["baseline_fail"] == 242
    assert q4b["eligible"] == 10
    assert q4b["primary_rescue"] == 5
    assert q4b["primary_final"] == 83
    assert q4b["posthoc_rescue"] == 6
    assert q4b["posthoc_final"] == 84
    assert q4b["observed_regression"] == 0

    # Qwen 9B
    q9b = claims["qwen_9b"]
    assert q9b["baseline_pass"] == 101
    assert q9b["baseline_fail"] == 219
    assert q9b["eligible"] == 0
    assert q9b["noneligible"] == 214
    assert q9b["ambiguous_entry_point_abstain"] == 5
    assert q9b["final"] == 101
    assert q9b["observed_regression"] == 0

    # Tier 1 Overall
    overall = claims["tier1_overall"]
    assert overall["BOTH_PASS"] == 52
    assert overall["FOUR_B_ONLY"] == 26
    assert overall["NINE_B_ONLY"] == 49
    assert overall["BOTH_FAIL"] == 193
    assert overall["TOTAL"] == 320
    assert overall["paired_risk_difference"] == 0.071875
    assert overall["exact_mcnemar_p"] == 0.010582
    assert overall["task_clustered_bootstrap_ci"] == [-0.0094, 0.1438]


def test_family_tables_revalidation():
    with open(NUMERIC_CLAIMS_PATH, encoding="utf-8") as f:
        claims = json.load(f)

    family = claims["family_tables"]
    assert family["column_order"] == ["BOTH_PASS", "FOUR_B_ONLY", "NINE_B_ONLY", "BOTH_FAIL"]

    # Integer: 29 / 1 / 13 / 37
    assert family["Integer"]["BOTH_PASS"] == 29
    assert family["Integer"]["FOUR_B_ONLY"] == 1
    assert family["Integer"]["NINE_B_ONLY"] == 13
    assert family["Integer"]["BOTH_FAIL"] == 37

    # Polynomial: 3 / 13 / 6 / 58
    assert family["Polynomial"]["BOTH_PASS"] == 3
    assert family["Polynomial"]["FOUR_B_ONLY"] == 13
    assert family["Polynomial"]["NINE_B_ONLY"] == 6
    assert family["Polynomial"]["BOTH_FAIL"] == 58

    # Radical: 10 / 5 / 9 / 56
    assert family["Radical"]["BOTH_PASS"] == 10
    assert family["Radical"]["FOUR_B_ONLY"] == 5
    assert family["Radical"]["NINE_B_ONLY"] == 9
    assert family["Radical"]["BOTH_FAIL"] == 56

    # Fraction: 10 / 7 / 21 / 42
    assert family["Fraction"]["BOTH_PASS"] == 10
    assert family["Fraction"]["FOUR_B_ONLY"] == 7
    assert family["Fraction"]["NINE_B_ONLY"] == 21
    assert family["Fraction"]["BOTH_FAIL"] == 42
    assert family["Fraction"]["exact_mcnemar_p"] == 0.012541


def test_primary_posthoc_accounting():
    with open(ACCOUNTING_PATH, encoding="utf-8") as f:
        acct = json.load(f)

    assert "289" in acct["gemini"]["primary_score"]
    assert "306" in acct["gemini"]["posthoc_score"]
    assert "83" in acct["qwen_4b"]["primary_score"]
    assert "84" in acct["qwen_4b"]["posthoc_score"]


def test_sha_closure_files_exist():
    with open(SHA_CLOSURE_PATH, encoding="utf-8") as f:
        sha_data = json.load(f)

    assert sha_data["starting_head_commit"] == "5c15b0aee0ef0d4bfa0439c8d0759ed0e4e2af49"
    hashes = sha_data["hashes"]

    for key, item in hashes.items():
        rel_p = item["rel_path"]
        abs_p = ROOT / rel_p
        assert abs_p.exists(), f"Source file referenced in SHA closure does not exist: {rel_p}"
        assert len(item["sha256"]) == 64, f"Invalid SHA256 string for {key}"


def test_category_status():
    with open(CATEGORY_STATUS_PATH, encoding="utf-8") as f:
        status = json.load(f)

    assert status["CATEGORY_A_STATUS"] == "CATEGORY_A_COMPLETED_WITH_INTERPRETATION_LIMITATIONS"
    assert status["CATEGORY_B_QA_STATUS"] == "CATEGORY_B_QA_COMPLETED"
    assert status["CATEGORY_B_FIGURE_SPEC_STATUS"] == "CATEGORY_B_FIGURE_SPEC_COMPLETED"
    assert status["CATEGORY_B_ACTUAL_FIGURES_STATUS"] == "CATEGORY_B_ACTUAL_FIGURES_PENDING"


def test_interpretation_limitations_has_ten_items():
    content = LIMITATIONS_PATH.read_text(encoding="utf-8")
    for i in range(1, 11):
        assert f"{i}." in content or f"## {i}" in content


def test_presentation_handoff_rules():
    content = HANDOFF_PATH.read_text(encoding="utf-8")
    assert "PRESENTATION_HANDOFF_SPEC_V1_FROZEN" in content
    assert "NO_SILENT_DATA_MUTATION_PERMITTED" in content or "靜默" in content


def test_integrated_report_milestone_status():
    content = INTEGRATED_REPORT_PATH.read_text(encoding="utf-8")
    assert "Evidence Complete Milestone v1" in content
    assert "17.3 里程碑凍結狀態" in content or "MILESTONE_STATUS" in content
