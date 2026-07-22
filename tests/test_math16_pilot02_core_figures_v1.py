# -*- coding: utf-8 -*-
"""Targeted unit tests for Math16 Pilot-02 Core Figures Batch 01 (Figures 1, 3, 4, 5)."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

OUT_DIR = ROOT / "docs/experiments/visualization/math16_pilot02_core_figures_v1"
MILESTONE_CLAIMS_PATH = ROOT / "docs/experiments/milestones/math16_pilot02_evidence_complete_v1/frozen_numeric_claims.json"

MANIFEST_PATH = OUT_DIR / "figure_build_manifest.json"
REPORT_PATH = OUT_DIR / "figure_build_report.md"


def test_core_figures_files_exist():
    assert OUT_DIR.exists()
    assert MANIFEST_PATH.exists()
    assert REPORT_PATH.exists()

    expected_files = [
        "figure_01_baseline_overall.png",
        "figure_01_baseline_overall.svg",
        "figure_03_family_breakdown.png",
        "figure_03_family_breakdown.svg",
        "figure_04_tier1_paired_analysis.png",
        "figure_04_tier1_paired_analysis.svg",
        "figure_05_healer_eligibility_boundary.png",
        "figure_05_healer_eligibility_boundary.svg",
    ]

    for fname in expected_files:
        fpath = OUT_DIR / fname
        assert fpath.exists(), f"Expected figure file missing: {fname}"
        assert fpath.stat().st_size > 0, f"Figure file is empty: {fname}"


def test_figure_2_and_6_not_generated_in_batch01():
    forbidden_files = [
        "figure_02_prompt_conditions.png",
        "figure_02_prompt_conditions.svg",
        "figure_06_healer_concept_zones.png",
        "figure_06_healer_concept_zones.svg",
    ]
    for fname in forbidden_files:
        fpath = OUT_DIR / fname
        assert not fpath.exists(), f"Figure file from other batches should not be generated: {fname}"


def test_manifest_structure_and_hashes():
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        manifest = json.load(f)

    assert manifest["manifest_id"] == "math16_pilot02_core_figures_v1_manifest"
    assert manifest["batch"] == "batch_01_figures_1_3_4_5"
    assert manifest["font_family_used"] == "Microsoft JhengHei"

    rendered = manifest["rendered_figures"]
    assert len(rendered) == 4

    for item in rendered:
        assert item["dpi"] == 300
        assert len(item["png_sha256"]) == 64
        assert len(item["svg_sha256"]) == 64


def test_numbers_match_frozen_milestone_claims():
    with open(MILESTONE_CLAIMS_PATH, encoding="utf-8") as f:
        claims = json.load(f)

    # Gemini = 289, 4B = 78, 9B = 101
    assert claims["gemini_primary"]["baseline_pass"] == 289
    assert claims["qwen_4b"]["baseline_pass"] == 78
    assert claims["qwen_9b"]["baseline_pass"] == 101

    # Family table
    f_data = claims["family_tables"]
    assert f_data["Integer"]["BOTH_PASS"] + f_data["Integer"]["FOUR_B_ONLY"] == 30
    assert f_data["Integer"]["BOTH_PASS"] + f_data["Integer"]["NINE_B_ONLY"] == 42
    assert f_data["Polynomial"]["BOTH_PASS"] + f_data["Polynomial"]["FOUR_B_ONLY"] == 16
    assert f_data["Polynomial"]["BOTH_PASS"] + f_data["Polynomial"]["NINE_B_ONLY"] == 9

    # Tier 1 Overall
    t1 = claims["tier1_overall"]
    assert t1["BOTH_PASS"] == 52
    assert t1["FOUR_B_ONLY"] == 26
    assert t1["NINE_B_ONLY"] == 49
    assert t1["BOTH_FAIL"] == 193
    assert t1["exact_mcnemar_p"] == 0.010582
    assert t1["task_clustered_bootstrap_ci"] == [-0.0094, 0.1438]

    # Rescue counts
    assert claims["qwen_4b"]["primary_rescue"] == 5
    assert claims["qwen_4b"]["posthoc_rescue"] == 6
