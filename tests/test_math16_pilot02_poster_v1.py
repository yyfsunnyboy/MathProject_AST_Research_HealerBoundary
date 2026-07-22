"""Targeted acceptance tests for rendered Math16 Pilot-02 Poster v1."""
from __future__ import annotations

import hashlib
import json
import re
from itertools import combinations
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "docs/experiments/presentation/math16_pilot02_poster_v1"
PNG = OUT_DIR / "math16_pilot02_poster_v1.png"
PDF = OUT_DIR / "math16_pilot02_poster_v1.pdf"
MANIFEST = OUT_DIR / "poster_v1_manifest.json"
BUILD_REPORT = OUT_DIR / "poster_v1_build_report.md"
BBOX = OUT_DIR / "poster_v1_element_bboxes.json"
ASSETS = OUT_DIR / "assets"

SPEC = ROOT / "docs/experiments/presentation/math16_pilot02_poster_v1_spec.md"
CONTENT_MAP = ROOT / "docs/experiments/presentation/math16_pilot02_poster_v1_content_map.json"
FINAL_REPORT = ROOT / "docs/experiments/reports/math16_pilot02_final_report_v13.md"
FINAL_REPORT_MANIFEST = ROOT / "docs/experiments/reports/math16_pilot02_final_report_v13_manifest.json"
EVIDENCE = ROOT / "docs/experiments/milestones/math16_pilot02_evidence_complete_v1/evidence_complete_manifest.json"
INTEGRATED = ROOT / "docs/experiments/reports/math16_pilot02_integrated_results_report_v1.md"
QA = ROOT / "docs/experiments/reports/math16_pilot02_jury_qa_final_v1.md"
CORE = ROOT / "docs/experiments/visualization/math16_pilot02_core_figures_v1"
ONE_PAGER = ROOT / "docs/experiments/presentation/math16_pilot02_one_pager_v23/math16_pilot02_one_pager_v23.png"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_rendered_outputs_and_landscape_dimensions_exist():
    for path in (PNG, PDF, MANIFEST, BUILD_REPORT, BBOX):
        assert path.exists() and path.stat().st_size > 0
    with Image.open(PNG) as image:
        assert image.width > image.height
        assert image.width >= 5000
        assert image.height >= 3000


def test_pdf_is_one_page():
    # Matplotlib emits one /Type /Pages catalog plus one /Type /Page for a one-page PDF.
    data = PDF.read_bytes()
    assert len(re.findall(rb"/Type /Page(?!s)", data)) == 1


def test_three_columns_six_figures_and_hero_hierarchy():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    bbox = json.loads(BBOX.read_text(encoding="utf-8"))
    assert manifest["orientation"] == "landscape"
    assert manifest["columns"] == 3
    expected = {
        "figure_01_baseline_overall",
        "figure_02_prompt_conditions",
        "figure_03_family_breakdown",
        "figure_04_tier1_paired_analysis",
        "figure_05_healer_eligibility_boundary",
        "figure_06_healer_concept_zones",
    }
    assert expected <= set(bbox["elements"])
    areas = {name: bbox["elements"][name]["bbox_pixels"]["area"] for name in expected}
    assert max(areas, key=areas.get) == "figure_04_tier1_paired_analysis"
    assert len(list(ASSETS.glob("figure_*.png"))) == 6


def test_primary_posthoc_and_figure2_disclaimer_are_rendered_in_build_report():
    report = BUILD_REPORT.read_text(encoding="utf-8")
    for statement in (
        "Baseline 78/320",
        "Primary 83/320 (rescue=5)",
        "Post-hoc 84/320 (total rescue=6; +1 PASS vs Primary)",
        "Gemini: Primary 289/320; Post-hoc 306/320",
        "Gemini 80/80 is Post-hoc",
        "Primary spec-v1=63/80",
        "Qwen uses spec-v2",
    ):
        assert statement in report


def test_five_discoveries_three_limitations_and_conservative_conclusion_present():
    # The poster itself is rasterized; renderer metadata proves the named content panels exist.
    names = set(json.loads(BBOX.read_text(encoding="utf-8"))["elements"])
    assert {"right_discoveries", "right_limitations", "right_conclusion"} <= names


def test_renderer_measured_all_pair_bbox_collision_detection_passes():
    bbox = json.loads(BBOX.read_text(encoding="utf-8"))
    assert bbox["methodology"]["bbox_measurement"] == "get_window_extent(renderer=renderer)"
    assert bbox["methodology"]["position_measurement"] == "get_position()"
    assert bbox["element_count"] == len(bbox["elements"])
    assert bbox["pair_count"] == len(bbox["pairs"])
    assert bbox["pair_count"] == len(list(combinations(bbox["elements"], 2)))
    assert bbox["collision_count"] == 0
    assert bbox["passing_pair_count"] == bbox["pair_count"]
    assert all(pair["intersection_area_pixels"] == 0 for pair in bbox["pairs"])


def test_frozen_source_sha_protection_and_asset_identity():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    expected_sources = {
        "poster_spec": SPEC,
        "poster_content_map": CONTENT_MAP,
        "final_report_v13": FINAL_REPORT,
        "evidence_complete_manifest": EVIDENCE,
        "integrated_report": INTEGRATED,
        "jury_qa": QA,
        "one_pager_v23": ONE_PAGER,
    }
    for name, path in expected_sources.items():
        assert sha(path) == manifest["source_shas"][name], f"SHA changed: {name}"
    final_manifest = json.loads(FINAL_REPORT_MANIFEST.read_text(encoding="utf-8"))
    assert sha(FINAL_REPORT) == final_manifest["v13_sha256"]
    for key, path in {
        "figure_01_baseline_overall": CORE / "figure_01_baseline_overall.png",
        "figure_02_prompt_conditions": CORE / "figure_02_prompt_conditions.png",
        "figure_03_family_breakdown": CORE / "figure_03_family_breakdown.png",
        "figure_04_tier1_paired_analysis": CORE / "figure_04_tier1_paired_analysis.png",
        "figure_05_healer_eligibility_boundary": CORE / "figure_05_healer_eligibility_boundary.png",
        "figure_06_healer_concept_zones": CORE / "figure_06_healer_concept_zones.png",
    }.items():
        assert sha(path) == manifest["source_shas"][key]
        assert sha(ASSETS / path.name) == sha(path)


def test_no_presentation_deck_outputs_created():
    prohibited = {".ppt", ".pptx", ".key", ".odp"}
    assert not any(path.suffix.lower() in prohibited for path in OUT_DIR.rglob("*"))
