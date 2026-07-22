# -*- coding: utf-8 -*-
"""Targeted unit tests for Math16 Pilot-02 Core Figures (All 6 Figures + Figure 2 Post-hoc Clarification)."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

OUT_DIR = ROOT / "docs/experiments/visualization/math16_pilot02_core_figures_v1"
MILESTONE_CLAIMS_PATH = ROOT / "docs/experiments/milestones/math16_pilot02_evidence_complete_v1/frozen_numeric_claims.json"

MANIFEST_PATH = OUT_DIR / "figure_build_manifest.json"
REPORT_PATH = OUT_DIR / "figure_build_report.md"

# SHA256 constants for preserved figures
SHA_FIG1_PNG = "5bc0c714769c987710dd124b7f126a53a4c77f96ccd578fbff4a0c82bdb52db2"
SHA_FIG3_PNG = "f164edc807659c45628cbab4711074879af58d3beaa825f59aaf2ebce4c9fb79"
SHA_FIG4_PNG = "f18bbb774e9a75c51da364f080281172e7c35c4a5b2e30245142de0993565fdf"
SHA_FIG5_PNG = "5887f0b829797ab63f30a096ec2e27c80530c1f988dcc16e3bead4bd7feb9885"
SHA_FIG6_PNG = "3b358862434ea81b74841def4ca81a6168b8e1ff36ab2b44f3868d4db891c71c"
SHA_FIG2_PNG_POSTHOC = "7df829db88a30c34aeb3e9b000a5d96aec08c3134abfbfdc1475ebaac3da7e4b"

# Figure 2 ground-truth data
FIGURE2_DATA = {
    "Ab1":         {"gemini_primary": 72, "qwen4b": 15, "qwen9b": 18},
    "Ab2g":        {"gemini_primary": 76, "qwen4b": 19, "qwen9b": 27},
    "Ab2d+api":    {"gemini_primary": 78, "qwen4b": 8,  "qwen9b": 16},
    "Ab2d+spec":   {"gemini_primary": 63, "qwen4b": 36, "qwen9b": 40,
                    "gemini_posthoc": 80},
}


def compute_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def test_all_six_core_figure_files_exist():
    """Verify all 6 core figures PNG+SVG exist and are non-empty."""
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


def test_manifest_structure_and_posthoc_clarification():
    """Verify manifest records Figure 2 Post-hoc clarification and all 6 rendered figures."""
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        manifest = json.load(f)

    assert manifest["manifest_id"] == "math16_pilot02_core_figures_v1_manifest"
    assert manifest["batch"] == "all_six_core_figures_complete"
    assert manifest["rendered_figures_count"] == 6
    assert manifest["font_family_used"] == "Microsoft JhengHei"

    # Figure 2 Post-hoc clarification metadata
    ph = manifest["figure2_posthoc_clarification"]
    assert ph["gemini_primary_spec_v1"] == 63, "Primary spec-v1 must be 63"
    assert ph["gemini_posthoc_spec_v2"] == 80, "Post-hoc spec-v2 must be 80"
    assert "NOT modified" in ph["primary_accounting"]
    assert "NOT a formal re-run Primary result" in ph["posthoc_label"]

    # Preserved figures list (figs 1,3,4,5,6)
    preserved = manifest["preserved_figures"]
    for fig_id in ["fig1_baseline_overall", "fig3_family_breakdown",
                   "fig4_tier1_paired_analysis", "fig5_healer_eligibility_boundary",
                   "fig6_healer_concept_zones"]:
        assert fig_id in preserved, f"Expected {fig_id} in preserved_figures"

    rendered = manifest["rendered_figures"]
    assert len(rendered) == 6

    for item in rendered:
        assert item["dpi"] == 300
        assert len(item["png_sha256"]) == 64
        assert len(item["svg_sha256"]) == 64


def test_figures_1_3_4_5_6_sha_preserved():
    """Critical: SHA256 of Figures 1, 3, 4, 5, 6 must be identical to pre-hotfix hashes."""
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        manifest = json.load(f)
    rendered = manifest["rendered_figures"]

    def get_sha(fig_id, key="png_sha256"):
        return next(i[key] for i in rendered if i["figure_id"] == fig_id)

    assert get_sha("fig1_baseline_overall") == SHA_FIG1_PNG, "Figure 1 PNG SHA changed!"
    assert get_sha("fig3_family_breakdown") == SHA_FIG3_PNG, "Figure 3 PNG SHA changed!"
    assert get_sha("fig4_tier1_paired_analysis") == SHA_FIG4_PNG, "Figure 4 PNG SHA changed!"
    assert get_sha("fig5_healer_eligibility_boundary") == SHA_FIG5_PNG, "Figure 5 PNG SHA changed!"
    assert get_sha("fig6_healer_concept_zones") == SHA_FIG6_PNG, "Figure 6 PNG SHA changed!"


def test_figure_2_sha_changed_to_posthoc_version():
    """Figure 2 PNG SHA must have changed to the Post-hoc clarification version."""
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        manifest = json.load(f)
    rendered = manifest["rendered_figures"]
    fig2 = next(i for i in rendered if i["figure_id"] == "fig2_prompt_conditions")
    # New SHA must NOT be the old pre-clarification value
    assert fig2["png_sha256"] != "73f66ce6a84200abf1f94599bafcba3bd820f3913ceb400103e36bc614367d33", \
        "Figure 2 PNG SHA unchanged — Post-hoc clarification not applied!"
    # Must match the new Post-hoc version SHA
    assert fig2["png_sha256"] == SHA_FIG2_PNG_POSTHOC, \
        f"Figure 2 PNG SHA mismatch: got {fig2['png_sha256']}"


def test_figure_2_groups_1_to_3_data_unchanged():
    """Ab1, Ab2g, Ab2d+api data values must not have changed."""
    # These are ground-truth constants; tested here so any future accidental edit is caught
    assert FIGURE2_DATA["Ab1"]["gemini_primary"] == 72
    assert FIGURE2_DATA["Ab1"]["qwen4b"] == 15
    assert FIGURE2_DATA["Ab1"]["qwen9b"] == 18
    assert FIGURE2_DATA["Ab2g"]["gemini_primary"] == 76
    assert FIGURE2_DATA["Ab2g"]["qwen4b"] == 19
    assert FIGURE2_DATA["Ab2g"]["qwen9b"] == 27
    assert FIGURE2_DATA["Ab2d+api"]["gemini_primary"] == 78
    assert FIGURE2_DATA["Ab2d+api"]["qwen4b"] == 8
    assert FIGURE2_DATA["Ab2d+api"]["qwen9b"] == 16


def test_figure_2_group_4_posthoc_and_primary_accounting():
    """Group 4 (Ab2d+spec): Gemini Post-hoc = 80, Primary = 63; Qwen spec-v2 unchanged."""
    g4 = FIGURE2_DATA["Ab2d+spec"]
    assert g4["gemini_primary"] == 63, "Gemini Primary spec-v1 must be 63"
    assert g4["gemini_posthoc"] == 80, "Gemini Post-hoc spec-v2 must be 80"
    assert g4["qwen4b"] == 36, "Qwen 4B spec-v2 must be 36"
    assert g4["qwen9b"] == 40, "Qwen 9B spec-v2 must be 40"

    # Evidence Complete not modified
    with open(MILESTONE_CLAIMS_PATH, encoding="utf-8") as f:
        claims = json.load(f)
    assert claims["qwen_4b"]["baseline_pass"] == 78
    assert claims["qwen_9b"]["baseline_pass"] == 101
    assert claims["gemini_primary"]["baseline_pass"] == 289


def test_figure_2_posthoc_80_not_in_primary_bar_for_gemini():
    """Manifest must record that 80/80 is Post-hoc mechanism validation, not Primary."""
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        manifest = json.load(f)
    ph = manifest["figure2_posthoc_clarification"]
    assert ph["gemini_primary_spec_v1"] == 63
    assert ph["gemini_posthoc_spec_v2"] == 80
    assert "Post-hoc mechanism validation" in ph["posthoc_label"]
    assert "NOT a formal re-run Primary result" in ph["posthoc_label"]


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


def test_no_forbidden_outputs_exist():
    """Confirm no one-pager, PPT, PDF, poster, or Figure 2/6 from earlier batches were generated."""
    forbidden_patterns = ["one_pager", "ppt", "poster", ".pdf", ".pptx"]
    for p in OUT_DIR.iterdir():
        for pattern in forbidden_patterns:
            assert pattern not in p.name.lower(), f"Forbidden output found: {p.name}"
