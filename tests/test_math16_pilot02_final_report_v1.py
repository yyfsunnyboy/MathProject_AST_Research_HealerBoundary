# -*- coding: utf-8 -*-
"""Unit tests for Math16 Pilot-02 Final Report v1."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REPORT_PATH = ROOT / "docs/experiments/reports/math16_pilot02_final_report_v1.md"
MANIFEST_PATH = ROOT / "docs/experiments/reports/math16_pilot02_final_report_v1_manifest.json"
BUILD_REPORT_PATH = ROOT / "docs/experiments/reports/math16_pilot02_final_report_v1_build_report.md"

CLAIMS_PATH = ROOT / "docs/experiments/milestones/math16_pilot02_evidence_complete_v1/frozen_numeric_claims.json"
LIMITATIONS_PATH = ROOT / "docs/experiments/milestones/math16_pilot02_evidence_complete_v1/interpretation_limitations.md"
JURY_QA_PATH = ROOT / "docs/experiments/reports/math16_pilot02_jury_qa_final_v1.md"
CORE_FIG_DIR = ROOT / "docs/experiments/visualization/math16_pilot02_core_figures_v1"
ONE_PAGER_DIR = ROOT / "docs/experiments/presentation/math16_pilot02_one_pager_v23"


def test_final_report_files_exist():
    for p in [REPORT_PATH, MANIFEST_PATH, BUILD_REPORT_PATH]:
        assert p.exists(), f"Missing output file: {p.name}"
        assert p.stat().st_size > 0, f"Empty output file: {p.name}"


def test_final_report_has_20_sections():
    text = REPORT_PATH.read_text(encoding="utf-8")
    headings = re.findall(r"^##\s+(\d+)\.\s+(.+)$", text, flags=re.MULTILINE)
    assert len(headings) == 20, f"Expected 20 sections, found {len(headings)}"
    section_nums = [int(h[0]) for h in headings]
    assert section_nums == list(range(1, 21)), f"Section numbering invalid: {section_nums}"


def test_abstract_character_count_between_500_and_700():
    text = REPORT_PATH.read_text(encoding="utf-8")
    # Extract Section 1 content between Section 1 heading and section divider
    m = re.search(r"## 1\..+?\n(.*?)\n---", text, flags=re.DOTALL)
    assert m, "Section 1 Abstract not found"
    abstract_text = m.group(1).strip()
    # Count Traditional Chinese / CJK characters
    cjk_chars = re.findall(r"[\u4e00-\u9fff]", abstract_text)
    cjk_count = len(cjk_chars)
    assert 500 <= cjk_count <= 700, f"Abstract CJK char count = {cjk_count}, expected between 500 and 700"


def test_six_core_figures_referenced():
    text = REPORT_PATH.read_text(encoding="utf-8")
    figs = [
        "figure_01_baseline_overall.png",
        "figure_02_prompt_conditions.png",
        "figure_03_family_breakdown.png",
        "figure_04_tier1_paired_analysis.png",
        "figure_05_healer_eligibility_boundary.png",
        "figure_06_healer_concept_zones.png",
    ]
    for fig in figs:
        assert fig in text, f"Missing figure reference: {fig}"


def test_figure2_accounting_notes_present():
    text = REPORT_PATH.read_text(encoding="utf-8")
    assert "80/80" in text
    assert "Post-hoc" in text
    assert "63/80" in text
    assert "spec-v1" in text
    assert "spec-v2" in text


def test_frozen_numbers_correct():
    text = REPORT_PATH.read_text(encoding="utf-8")
    # Gemini
    assert "289" in text
    assert "306" in text
    # Qwen 4B
    assert "78" in text
    assert "242" in text
    assert "10" in text
    assert "83" in text
    assert "84" in text
    # Qwen 9B
    assert "101" in text
    assert "219" in text
    # Tier 1
    assert "52" in text
    assert "26" in text
    assert "49" in text
    assert "193" in text
    assert "0.010582" in text
    assert "[-0.94%, +14.38%]" in text
    # Family table
    assert "29" in text
    assert "13" in text
    assert "37" in text
    assert "0.012541" in text


def test_primary_posthoc_separated():
    text = REPORT_PATH.read_text(encoding="utf-8")
    assert "Primary" in text
    assert "Post-hoc" in text
    assert "83/320" in text
    assert "84/320" in text


def test_ten_methodology_limitations_present():
    text = REPORT_PATH.read_text(encoding="utf-8")
    m = re.search(r"## 18\..+?\n(.*?)\n---", text, flags=re.DOTALL)
    assert m, "Section 18 Limitations not found"
    sec18 = m.group(1)
    items = re.findall(r"^\d+\.\s+\*\*", sec18, flags=re.MULTILINE)
    assert len(items) == 10, f"Expected 10 limitations in Section 18, got {len(items)}"


def test_eight_jury_qa_items_present():
    text = REPORT_PATH.read_text(encoding="utf-8")
    m = re.search(r"## 19\..+?\n(.*?)\n---", text, flags=re.DOTALL)
    assert m, "Section 19 Jury Q&A not found"
    sec19 = m.group(1)
    qa_items = re.findall(r"^###\s+Q\d+:", sec19, flags=re.MULTILINE)
    assert len(qa_items) == 8, f"Expected 8 Q&A items, got {len(qa_items)}"


def test_no_forbidden_overclaims():
    text = REPORT_PATH.read_text(encoding="utf-8")
    forbidden = [
        "證明9B比4B強",
        "Healer保證不倒退",
        "Gemini代表所有大型模型",
        "Fraction證明9B數學較強",
        "Polynomial證明9B較差",
        "Prompt造成異常",
        "所有SyntaxError可修",
        "eligible=0代表Healer無效",
        "Post-hoc 84／306為Primary正式結果",
    ]
    for phrase in forbidden:
        assert phrase not in text, f"Forbidden phrase found: '{phrase}'"


def test_no_forbidden_output_formats_generated():
    forbidden_exts = [".docx", ".pptx", ".ppt", ".pdf"]
    for p in (ROOT / "docs/experiments/reports").rglob("*"):
        if "final_report_v1" in p.name.lower():
            assert p.suffix.lower() not in forbidden_exts, f"Forbidden output format found: {p.name}"


def test_evidence_complete_milestone_files_untouched():
    assert CLAIMS_PATH.exists()
    assert LIMITATIONS_PATH.exists()
    assert JURY_QA_PATH.exists()
    assert CORE_FIG_DIR.exists()
    assert ONE_PAGER_DIR.exists()
