"""Acceptance tests for the Math16 Pilot-02 Poster v1.1 readability hotfix."""
from __future__ import annotations

import hashlib
import json
import re
from itertools import combinations
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs/experiments/presentation/math16_pilot02_poster_v11"
PNG = OUT / "math16_pilot02_poster_v11.png"
PDF = OUT / "math16_pilot02_poster_v11.pdf"
MANIFEST = OUT / "poster_v11_manifest.json"
BBOX = OUT / "poster_v11_element_bboxes.json"
BUILD_REPORT = OUT / "poster_v11_build_report.md"
ASSETS = OUT / "assets"

SPEC = ROOT / "docs/experiments/presentation/math16_pilot02_poster_v1_spec.md"
CONTENT = ROOT / "docs/experiments/presentation/math16_pilot02_poster_v1_content_map.json"
FINAL = ROOT / "docs/experiments/reports/math16_pilot02_final_report_v13.md"
FINAL_MANIFEST = ROOT / "docs/experiments/reports/math16_pilot02_final_report_v13_manifest.json"
EVIDENCE = ROOT / "docs/experiments/milestones/math16_pilot02_evidence_complete_v1/evidence_complete_manifest.json"
INTEGRATED = ROOT / "docs/experiments/reports/math16_pilot02_integrated_results_report_v1.md"
QA = ROOT / "docs/experiments/reports/math16_pilot02_jury_qa_final_v1.md"
ONE_PAGER = ROOT / "docs/experiments/presentation/math16_pilot02_one_pager_v23/math16_pilot02_one_pager_v23.png"
POSTER_V1_PNG = ROOT / "docs/experiments/presentation/math16_pilot02_poster_v1/math16_pilot02_poster_v1.png"
POSTER_V1_PDF = ROOT / "docs/experiments/presentation/math16_pilot02_poster_v1/math16_pilot02_poster_v1.pdf"
CORE = ROOT / "docs/experiments/visualization/math16_pilot02_core_figures_v1"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_outputs_exist_landscape_and_pdf_is_one_page():
    for path in (PNG, PDF, MANIFEST, BBOX, BUILD_REPORT):
        assert path.exists() and path.stat().st_size > 0
    with Image.open(PNG) as image:
        assert image.width == 5400 and image.height == 3600
    assert len(re.findall(rb"/Type /Page(?!s)", PDF.read_bytes())) == 1


def test_header_scope_cards_and_three_second_messages_present():
    bbox = json.loads(BBOX.read_text(encoding="utf-8"))["elements"]
    assert {"header", "card_gemini", "card_qwen4b", "card_qwen9b", "hero_messages", "left_window"} <= set(bbox)
    # Cards are deliberately enlarged relative to the v1 cards: 0.083 vs 0.045 poster height.
    assert bbox["card_qwen4b"]["position_figure_fraction"]["height"] == 0.083
    assert bbox["header"]["position_figure_fraction"]["height"] == 0.155
    report = BUILD_REPORT.read_text(encoding="utf-8")
    for phrase in ("Math16 Pilot-02 子實驗", "960 cells", "救回 5 格", "49 vs 26", "窄小且可驗證"):
        assert phrase in report


def test_figure4_largest_and_six_figures_each_once():
    bbox = json.loads(BBOX.read_text(encoding="utf-8"))["elements"]
    figures = {"figure_01", "figure_02", "figure_03", "figure_04", "figure_05", "figure_06"}
    assert figures <= set(bbox)
    areas = {name: bbox[name]["bbox_pixels"]["area"] for name in figures}
    assert max(areas, key=areas.get) == "figure_04"
    assert len(list(ASSETS.glob("*_compact_v11.png"))) == 6


def test_figure2_warning_findings_limitations_and_accounting_are_preserved():
    report = BUILD_REPORT.read_text(encoding="utf-8")
    for phrase in (
        "Gemini 80/80 is Post-hoc",
        "Primary spec-v1=63/80",
        "Qwen uses spec-v2",
        "4B Baseline 78/320",
        "Primary 83/320 (rescue=5)",
        "Post-hoc 84/320 (total rescue=6; +1 PASS)",
        "Gemini Primary 289/320",
        "Gemini Post-hoc 306/320",
    ):
        assert phrase in report
    names = set(json.loads(BBOX.read_text(encoding="utf-8"))["elements"])
    assert {"figure_02_warning", "right_findings", "bottom_limitations", "bottom_conclusion"} <= names


def test_renderer_bbox_pairwise_collision_check_passes():
    data = json.loads(BBOX.read_text(encoding="utf-8"))
    assert data["methodology"]["bbox_measurement"] == "get_window_extent(renderer=renderer)"
    assert data["methodology"]["position_measurement"] == "get_position()"
    assert data["pair_count"] == len(list(combinations(data["elements"], 2)))
    assert data["collision_count"] == 0
    assert data["passing_pair_count"] == data["pair_count"]
    assert all(item["intersection_area_pixels"] == 0 for item in data["pairs"])


def test_protected_source_shas_and_v1_outputs_are_unchanged():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    expected = {
        "poster_v1_spec": SPEC, "poster_v1_content_map": CONTENT, "final_report_v13": FINAL,
        "evidence_complete": EVIDENCE, "integrated_report": INTEGRATED, "jury_qa": QA,
        "one_pager_v23": ONE_PAGER, "poster_v1_png": POSTER_V1_PNG, "poster_v1_pdf": POSTER_V1_PDF,
    }
    for name, path in expected.items():
        assert sha(path) == manifest["source_shas"][name], f"changed protected source: {name}"
    final_manifest = json.loads(FINAL_MANIFEST.read_text(encoding="utf-8"))
    assert sha(FINAL) == final_manifest["v13_sha256"]
    for key, path in {
        "fig1": CORE / "figure_01_baseline_overall.png",
        "fig2": CORE / "figure_02_prompt_conditions.png",
        "fig3": CORE / "figure_03_family_breakdown.png",
        "fig4": CORE / "figure_04_tier1_paired_analysis.png",
        "fig5": CORE / "figure_05_healer_eligibility_boundary.png",
        "fig6": CORE / "figure_06_healer_concept_zones.png",
    }.items():
        assert sha(path) == manifest["source_shas"][key]


def test_no_presentation_deck_outputs():
    assert not any(path.suffix.lower() in {".ppt", ".pptx", ".odp", ".key"} for path in OUT.rglob("*"))
