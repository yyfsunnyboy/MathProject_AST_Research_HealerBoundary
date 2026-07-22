# -*- coding: utf-8 -*-
"""Unit tests for Math16 Pilot-02 Poster v1 Specification."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SPEC_PATH = ROOT / "docs/experiments/presentation/math16_pilot02_poster_v1_spec.md"
CONTENT_MAP_PATH = ROOT / "docs/experiments/presentation/math16_pilot02_poster_v1_content_map.json"
BUILD_REPORT_PATH = ROOT / "docs/experiments/presentation/math16_pilot02_poster_v1_build_report.md"

FINAL_REPORT_V11 = ROOT / "docs/experiments/reports/math16_pilot02_final_report_v11.md"
CLAIMS_PATH = ROOT / "docs/experiments/milestones/math16_pilot02_evidence_complete_v1/frozen_numeric_claims.json"
JURY_QA_PATH = ROOT / "docs/experiments/reports/math16_pilot02_jury_qa_final_v1.md"
CORE_FIG_DIR = ROOT / "docs/experiments/visualization/math16_pilot02_core_figures_v1"
ONE_PAGER_DIR = ROOT / "docs/experiments/presentation/math16_pilot02_one_pager_v23"


def sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def test_poster_v1_spec_files_exist():
    for p in [SPEC_PATH, CONTENT_MAP_PATH, BUILD_REPORT_PATH]:
        assert p.exists(), f"Missing output file: {p.name}"
        assert p.stat().st_size > 0, f"Empty output file: {p.name}"


def test_three_column_header_structure():
    text = SPEC_PATH.read_text(encoding="utf-8")
    assert "Header" in text, "Missing Header section"
    assert "左欄：研究設計" in text, "Missing Left Column"
    assert "中欄：主要證據" in text, "Missing Middle Column"
    assert "右欄：解讀與邊界" in text, "Missing Right Column"


def test_all_six_figures_configured_without_duplicates():
    text = SPEC_PATH.read_text(encoding="utf-8")
    cmap = json.loads(CONTENT_MAP_PATH.read_text(encoding="utf-8"))
    figs = [
        "figure_01_baseline_overall.png",
        "figure_02_prompt_conditions.png",
        "figure_03_family_breakdown.png",
        "figure_04_tier1_paired_analysis.png",
        "figure_05_healer_eligibility_boundary.png",
        "figure_06_healer_concept_zones.png",
    ]
    for fig in figs:
        assert fig in text, f"Missing figure in spec: {fig}"
    fig_paths = list(cmap["figure_paths"].values())
    assert len(fig_paths) == 6, f"Expected 6 figures in content_map, found {len(fig_paths)}"
    assert len(set(fig_paths)) == 6, "Duplicate figures found in content_map"


def test_figure4_marked_as_hero_largest_figure():
    text = SPEC_PATH.read_text(encoding="utf-8")
    cmap = json.loads(CONTENT_MAP_PATH.read_text(encoding="utf-8"))
    assert "Figure 4 Tier 1 配對分析 (Hero Figure - 最大圖)" in text or "Figure 4" in text
    assert "Hero Level" in text or "Hero" in text
    assert cmap["visual_hierarchy"]["hero_figure"]["figure_id"] == "fig4_tier1_paired_analysis"


def test_five_discoveries_present():
    text = SPEC_PATH.read_text(encoding="utf-8")
    cmap = json.loads(CONTENT_MAP_PATH.read_text(encoding="utf-8"))
    discoveries = [
        "Baseline能力與Healer可修復窗口不同",
        "4B存在窄小且可驗證的repair window",
        "9B整體通過較高，但Family結果非單調",
        "Prompt效果依模型、版本與部署條件而異",
        "Abstain是Deterministic Healer的重要安全能力",
    ]
    for d in discoveries:
        assert d in text, f"Missing discovery in spec: {d}"
    assert len(cmap["five_main_discoveries"]) == 5, "Expected 5 discoveries in content_map"


def test_three_poster_limitations_present():
    text = SPEC_PATH.read_text(encoding="utf-8")
    cmap = json.loads(CONTENT_MAP_PATH.read_text(encoding="utf-8"))
    assert "McNemar" in text
    assert "Task-clustered" in text or "task-clustered" in text.lower()
    assert "Fraction" in text
    assert "Observed Regression = 0" in text or "Regression=0" in text
    assert len(cmap["three_poster_limitations"]) == 3, "Expected 3 limitations in content_map"


def test_960_cells_and_core_numbers_correct():
    text = SPEC_PATH.read_text(encoding="utf-8")
    required = ["960 cells", "289", "83", "101", "52", "26", "49", "193", "0.010582", "[-0.94%, +14.38%]"]
    for item in required:
        assert item in text, f"Missing core number/statement: {item}"


def test_primary_posthoc_accounting_correct():
    text = SPEC_PATH.read_text(encoding="utf-8")
    assert "Primary" in text
    assert "Post-hoc" in text
    assert "83/320" in text
    assert "84/320" in text
    assert "救援 5 格" in text or "rescue = 5" in text.lower() or "Rescue = 5" in text or "救援 5" in text


def test_figure2_disclaimer_present():
    text = SPEC_PATH.read_text(encoding="utf-8")
    assert "Gemini 80/80 屬 Post-hoc 機制驗證" in text or "Gemini 80/80" in text
    assert "spec-v1" in text
    assert "spec-v2" in text
    assert "不作完全同條件 Primary 推論" in text or "不作完全同條件" in text


def test_bbox_methodology_frozen():
    text = SPEC_PATH.read_text(encoding="utf-8")
    cmap = json.loads(CONTENT_MAP_PATH.read_text(encoding="utf-8"))
    assert "get_window_extent()" in text
    assert "get_position()" in text
    assert "NAMED_ELEMENT_PAIRWISE_COLLISION_DETECTION" in text or "Pairwise" in text or "pairwise" in text.lower()
    assert cmap["bbox_methodology"] == "renderer_measured_pairwise_collision_free"


def test_no_overclaiming_phrases():
    full_text = SPEC_PATH.read_text(encoding="utf-8")
    # Evaluate content body before the "Banned Claims Guardrails" section
    content_text = full_text.split("## 四、 嚴格禁用語氣與宣稱")[0]
    forbidden = [
        "證明9B較強",
        "證明9B數學能力全面壓倒4B",
        "Healer保證絕不倒退",
        "額外救回6格",
        "語法與格式標點缺失為主要原因",
        "eligible=0代表Healer無效",
        "Post-hoc 84/320為Primary正式結果",
    ]
    for phrase in forbidden:
        assert phrase not in content_text, f"Forbidden positive claim found in content: '{phrase}'"


def test_no_binary_or_slide_outputs_exist():
    forbidden_exts = [".png", ".jpg", ".jpeg", ".pdf", ".ppt", ".pptx"]
    for p in (ROOT / "docs/experiments/presentation").rglob("*"):
        if "poster_v1" in p.name.lower() and p.name not in [
            "math16_pilot02_poster_v1_spec.md",
            "math16_pilot02_poster_v1_content_map.json",
            "math16_pilot02_poster_v1_build_report.md"
        ]:
            assert p.suffix.lower() not in forbidden_exts, f"Forbidden rendered binary file found: {p.name}"


def test_source_files_sha_integrity():
    cmap = json.loads(CONTENT_MAP_PATH.read_text(encoding="utf-8"))
    recorded = cmap["source_shas"]
    assert sha256(FINAL_REPORT_V11) == recorded["final_report_v11_sha256"], "Final Report v1.1 SHA changed!"
    assert sha256(CLAIMS_PATH) == recorded["frozen_numeric_claims_sha256"], "Frozen Claims SHA changed!"
    assert sha256(JURY_QA_PATH) == recorded["jury_qa_sha256"], "Jury QA SHA changed!"
    for fig_id, fig_file in [
        ("fig1", "figure_01_baseline_overall.png"),
        ("fig2", "figure_02_prompt_conditions.png"),
        ("fig3", "figure_03_family_breakdown.png"),
        ("fig4", "figure_04_tier1_paired_analysis.png"),
        ("fig5", "figure_05_healer_eligibility_boundary.png"),
        ("fig6", "figure_06_healer_concept_zones.png"),
    ]:
        actual = sha256(CORE_FIG_DIR / fig_file)
        expected = recorded["core_figures_sha256"][fig_id]
        assert actual == expected, f"Figure SHA changed for {fig_file}: expected={expected}, actual={actual}"
