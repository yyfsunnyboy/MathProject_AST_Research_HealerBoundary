# -*- coding: utf-8 -*-
"""Targeted unit tests for Math16 Pilot-02 Core Figure Specification v1."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SPEC_DIR = ROOT / "docs/experiments/visualization/math16_pilot02_core_figure_spec_v1"
SPEC_JSON_PATH = SPEC_DIR / "core_figure_spec.json"
DATA_TABLES_PATH = SPEC_DIR / "figure_data_tables.json"
GOVERNANCE_PATH = SPEC_DIR / "primary_posthoc_visual_governance.md"
CAPTIONS_PATH = SPEC_DIR / "figure_caption_bank.md"
ONE_PAGER_PATH = SPEC_DIR / "one_pager_figure_selection.md"
POSTER_ORAL_PATH = SPEC_DIR / "poster_and_oral_figure_order.md"
TRACEABILITY_PATH = SPEC_DIR / "source_traceability.json"
REPORT_SPEC_PATH = SPEC_DIR / "figure_spec_report.md"
MANIFEST_PATH = SPEC_DIR / "manifest.json"

REPORT_PATH = ROOT / "docs/experiments/reports/math16_pilot02_integrated_results_report_v1.md"


def test_spec_files_exist():
    assert SPEC_DIR.exists()
    assert SPEC_JSON_PATH.exists()
    assert DATA_TABLES_PATH.exists()
    assert GOVERNANCE_PATH.exists()
    assert CAPTIONS_PATH.exists()
    assert ONE_PAGER_PATH.exists()
    assert POSTER_ORAL_PATH.exists()
    assert TRACEABILITY_PATH.exists()
    assert REPORT_SPEC_PATH.exists()
    assert MANIFEST_PATH.exists()


def test_exactly_six_core_figures():
    with open(SPEC_JSON_PATH, encoding="utf-8") as f:
        spec = json.load(f)

    figures = spec["figures"]
    assert len(figures) == 6, f"Expected exactly 6 core figures, got {len(figures)}"

    fig_ids = [fig["figure_id"] for fig in figures]
    expected_ids = [
        "fig1_baseline_overall",
        "fig2_prompt_conditions",
        "fig3_family_breakdown",
        "fig4_tier1_paired_analysis",
        "fig5_healer_eligibility_boundary",
        "fig6_healer_concept_zones",
    ]
    assert fig_ids == expected_ids


def test_every_figure_has_required_fields():
    with open(SPEC_JSON_PATH, encoding="utf-8") as f:
        spec = json.load(f)

    required_keys = [
        "figure_id",
        "title_zh",
        "title_en",
        "one_sentence_message",
        "chart_type",
        "x_axis",
        "y_axis",
        "exact_data",
        "source_files",
        "primary_posthoc_status",
        "mandatory_annotations",
        "forbidden_interpretations",
        "caption_report",
        "caption_oral",
    ]

    for fig in spec["figures"]:
        for key in required_keys:
            assert key in fig, f"Figure {fig['figure_id']} missing required key '{key}'"
            assert fig[key], f"Figure {fig['figure_id']} key '{key}' is empty"


def test_one_pager_exactly_four_figures():
    with open(SPEC_JSON_PATH, encoding="utf-8") as f:
        spec = json.load(f)

    constraints = spec.get("layout_constraints", {})
    assert constraints.get("exactly_4_core_figures_in_one_pager") is True

    one_pager_content = ONE_PAGER_PATH.read_text(encoding="utf-8")
    assert "EXACTLY_4_CORE_FIGURES = TRUE" in one_pager_content or "exactly_4_core_figures = true" in one_pager_content
    assert "Figure 1" in one_pager_content
    assert "Figure 3" in one_pager_content
    assert "Figure 4" in one_pager_content
    assert "Figure 5" in one_pager_content

    # Figure 6 must NOT be an independent figure in One-Pager
    assert "Figure 6" not in [f for f in constraints.get("one_pager_figures", [])]


def test_poster_exactly_five_figures():
    with open(SPEC_JSON_PATH, encoding="utf-8") as f:
        spec = json.load(f)

    constraints = spec.get("layout_constraints", {})
    assert constraints.get("exactly_5_core_figures_in_poster") is True

    poster_content = POSTER_ORAL_PATH.read_text(encoding="utf-8")
    assert "POSTER_EXACTLY_FIVE_FIGURES = TRUE" in poster_content or "exactly_5_core_figures = true" in poster_content
    assert "Figure 1" in poster_content
    assert "Figure 2" in poster_content
    assert "Figure 6" in poster_content
    assert "Figure 4" in poster_content
    assert "Figure 5" in poster_content

    # Figure 3 must NOT be a main figure in Poster selection
    assert "Figure 3" not in [f for f in constraints.get("poster_figures", [])]
    assert "完全排除 Figure 3" in poster_content or "Moved to report and backup slides" in poster_content or "Excluded from main poster" in poster_content


def test_no_vague_rescue_range_phrases():
    spec_files = [
        SPEC_JSON_PATH,
        DATA_TABLES_PATH,
        GOVERNANCE_PATH,
        CAPTIONS_PATH,
        ONE_PAGER_PATH,
        POSTER_ORAL_PATH,
        REPORT_SPEC_PATH,
    ]

    vague_phrases = ["5~6", "5-6", "5至6", "救回 5~6 格", "5/6格"]

    for filepath in spec_files:
        content = filepath.read_text(encoding="utf-8")
        for phrase in vague_phrases:
            assert phrase not in content, f"Vague phrase '{phrase}' found in {filepath.name}"


def test_explicit_primary_posthoc_rescue_accounting():
    captions = CAPTIONS_PATH.read_text(encoding="utf-8")
    assert "5" in captions
    assert "6" in captions
    assert "83/320" in captions
    assert "84/320" in captions

    governance = GOVERNANCE_PATH.read_text(encoding="utf-8")
    assert "Primary rescue = 5" in governance
    assert "Post-hoc corrected-chain rescue = 6" in governance or "Post-hoc rescue = 6" in governance


def test_fig6_retained_in_spec():
    with open(SPEC_JSON_PATH, encoding="utf-8") as f:
        spec = json.load(f)

    fig6 = next((fig for fig in spec["figures"] if fig["figure_id"] == "fig6_healer_concept_zones"), None)
    assert fig6 is not None, "Figure 6 must be retained in core figure spec"
    assert fig6["denominator"] is None


def test_no_forbidden_chart_types():
    with open(SPEC_JSON_PATH, encoding="utf-8") as f:
        spec = json.load(f)

    forbidden_types = ["3d", "pie", "radar", "dual_y"]
    for fig in spec["figures"]:
        c_type = fig["chart_type"].lower()
        for forbidden in forbidden_types:
            assert forbidden not in c_type, f"Forbidden chart type '{forbidden}' found in figure {fig['figure_id']}"


def test_integrated_report_gap_inventory_updated():
    content = REPORT_PATH.read_text(encoding="utf-8")
    assert "17. 正式成果缺口盤點" in content
    assert "Core Figure Specification v1" in content or "Core Figure Spec v1" in content
