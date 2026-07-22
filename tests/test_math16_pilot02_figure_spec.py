# -*- coding: utf-8 -*-
"""Targeted unit tests for Math16 Pilot-02 Core Figure Specification v1."""
from __future__ import annotations

import json
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


def test_fig2_version_differentiation():
    with open(SPEC_JSON_PATH, encoding="utf-8") as f:
        spec = json.load(f)

    fig2 = next(fig for fig in spec["figures"] if fig["figure_id"] == "fig2_prompt_conditions")
    data_str = json.dumps(fig2["exact_data"], ensure_ascii=False)
    assert "spec-v1" in data_str
    assert "spec-v2" in data_str

    annos_str = json.dumps(fig2["mandatory_annotations"], ensure_ascii=False)
    assert "spec-v1" in annos_str
    assert "spec-v2" in annos_str


def test_fig4_dual_statistical_evidence():
    with open(SPEC_JSON_PATH, encoding="utf-8") as f:
        spec = json.load(f)

    fig4 = next(fig for fig in spec["figures"] if fig["figure_id"] == "fig4_tier1_paired_analysis")
    exact_data = fig4["exact_data"]

    assert exact_data["BOTH_PASS"] == 52
    assert exact_data["FOUR_B_ONLY_PASS"] == 26
    assert exact_data["NINE_B_ONLY_PASS"] == 49
    assert exact_data["BOTH_FAIL"] == 193
    assert exact_data["exact_mcnemar_p"] == 0.010582
    assert "[-0.94%, +14.38%]" in exact_data["task_clustered_bootstrap_95ci"]

    annos_str = json.dumps(fig4["mandatory_annotations"], ensure_ascii=False)
    assert "McNemar" in annos_str
    assert "Bootstrap" in annos_str


def test_fig5_rescue_and_regression_qualification():
    with open(SPEC_JSON_PATH, encoding="utf-8") as f:
        spec = json.load(f)

    fig5 = next(fig for fig in spec["figures"] if fig["figure_id"] == "fig5_healer_eligibility_boundary")
    exact_data = fig5["exact_data"]

    assert exact_data["Qwen 3.5 4B"]["Primary_Rescue"] == 5
    assert exact_data["Qwen 3.5 4B"]["Posthoc_Rescue"] == 6
    assert exact_data["Gemini 3.5 Flash"]["Eligible"] == 0
    assert exact_data["Qwen 3.5 9B"]["Eligible"] == 0

    annos_str = json.dumps(fig5["mandatory_annotations"], ensure_ascii=False)
    assert "Observed regression = 0" in annos_str or "Regression=0" in annos_str


def test_fig6_no_fabricated_numbers():
    with open(SPEC_JSON_PATH, encoding="utf-8") as f:
        spec = json.load(f)

    fig6 = next(fig for fig in spec["figures"] if fig["figure_id"] == "fig6_healer_concept_zones")
    assert fig6["denominator"] is None
    assert "no fabricated" in fig6["primary_posthoc_status"].lower() or "no empirical" in fig6["primary_posthoc_status"].lower()


def test_no_forbidden_chart_types():
    with open(SPEC_JSON_PATH, encoding="utf-8") as f:
        spec = json.load(f)

    forbidden_types = ["3d", "pie", "radar", "dual_y"]
    for fig in spec["figures"]:
        c_type = fig["chart_type"].lower()
        for forbidden in forbidden_types:
            assert forbidden not in c_type, f"Forbidden chart type '{forbidden}' found in figure {fig['figure_id']}"


def test_one_pager_selects_exactly_four_figures():
    content = ONE_PAGER_PATH.read_text(encoding="utf-8")
    assert "Figure 1" in content
    assert "Figure 3" in content
    assert "Figure 4" in content
    assert "Figure 5" in content
    assert "精選 4 張圖表" in content or "4 張圖表" in content


def test_data_tables_match_sources():
    with open(DATA_TABLES_PATH, encoding="utf-8") as f:
        data_tables = json.load(f)

    fig1 = data_tables["fig1_baseline_overall"]["data"]
    assert fig1["Gemini 3.5 Flash"]["pass_cells"] == 289
    assert fig1["Qwen 3.5 4B"]["pass_cells"] == 78
    assert fig1["Qwen 3.5 9B"]["pass_cells"] == 101

    fig4 = data_tables["fig4_tier1_paired_analysis"]
    matrix = fig4["contingency_matrix"]
    assert matrix["BOTH_PASS"] == 52
    assert matrix["FOUR_B_ONLY_PASS"] == 26
    assert matrix["NINE_B_ONLY_PASS"] == 49
    assert matrix["BOTH_FAIL"] == 193


def test_integrated_report_gap_inventory_updated():
    content = REPORT_PATH.read_text(encoding="utf-8")
    # Verify Gap Inventory section is present
    assert "17. 正式成果缺口盤點" in content
    assert "Core Figure Specification v1" in content or "Core Figure Spec v1" in content
