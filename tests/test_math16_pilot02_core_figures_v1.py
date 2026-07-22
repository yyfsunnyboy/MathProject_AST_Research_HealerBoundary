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
        "figure_02_prompt_conditions.png",
        "figure_02_prompt_conditions.svg",
        "figure_03_family_breakdown.png",
        "figure_03_family_breakdown.svg",
        "figure_04_tier1_paired_analysis.png",
        "figure_04_tier1_paired_analysis.svg",
        "figure_05_healer_eligibility_boundary.png",
        "figure_05_healer_eligibility_boundary.svg",
        "figure_06_healer_concept_zones.png",
        "figure_06_healer_concept_zones.svg",
    ]

    for fname in expected_files:
        fpath = OUT_DIR / fname
        assert fpath.exists(), f"Expected figure file missing: {fname}"
        assert fpath.stat().st_size > 0, f"Figure file is empty: {fname}"


def test_manifest_structure_and_all_six_figures():
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        manifest = json.load(f)

    assert manifest["manifest_id"] == "math16_pilot02_core_figures_v1_manifest"
    assert manifest["batch"] == "all_six_core_figures_complete"
    assert manifest["rendered_figures_count"] == 6
    assert manifest["font_family_used"] == "Microsoft JhengHei"
    assert manifest["newly_rendered_figures"] == ["fig2_prompt_conditions", "fig6_healer_concept_zones"]
    assert manifest["preserved_figures"] == ["fig1_baseline_overall", "fig3_family_breakdown", "fig4_tier1_paired_analysis", "fig5_healer_eligibility_boundary"]

    rendered = manifest["rendered_figures"]
    assert len(rendered) == 6

    # Verify Figures 1, 3, 4, 5 SHA immutability
    fig1 = next(item for item in rendered if item["figure_id"] == "fig1_baseline_overall")
    assert fig1["png_sha256"] == "5bc0c714769c987710dd124b7f126a53a4c77f96ccd578fbff4a0c82bdb52db2"

    fig3 = next(item for item in rendered if item["figure_id"] == "fig3_family_breakdown")
    assert fig3["png_sha256"] == "f164edc807659c45628cbab4711074879af58d3beaa825f59aaf2ebce4c9fb79"

    fig4 = next(item for item in rendered if item["figure_id"] == "fig4_tier1_paired_analysis")
    assert fig4["png_sha256"] == "f18bbb774e9a75c51da364f080281172e7c35c4a5b2e30245142de0993565fdf"

    fig5 = next(item for item in rendered if item["figure_id"] == "fig5_healer_eligibility_boundary")
    assert fig5["png_sha256"] == "5887f0b829797ab63f30a096ec2e27c80530c1f988dcc16e3bead4bd7feb9885"

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
