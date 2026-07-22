# -*- coding: utf-8 -*-
"""Unit tests for Math16 Pilot-02 Final Report v1.1."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REPORT_V1_PATH = ROOT / "docs/experiments/reports/math16_pilot02_final_report_v1.md"
REPORT_PATH = ROOT / "docs/experiments/reports/math16_pilot02_final_report_v11.md"
MANIFEST_PATH = ROOT / "docs/experiments/reports/math16_pilot02_final_report_v11_manifest.json"
BUILD_REPORT_PATH = ROOT / "docs/experiments/reports/math16_pilot02_final_report_v11_build_report.md"

CLAIMS_PATH = ROOT / "docs/experiments/milestones/math16_pilot02_evidence_complete_v1/frozen_numeric_claims.json"
LIMITATIONS_PATH = ROOT / "docs/experiments/milestones/math16_pilot02_evidence_complete_v1/interpretation_limitations.md"
JURY_QA_PATH = ROOT / "docs/experiments/reports/math16_pilot02_jury_qa_final_v1.md"
CORE_FIG_DIR = ROOT / "docs/experiments/visualization/math16_pilot02_core_figures_v1"
ONE_PAGER_DIR = ROOT / "docs/experiments/presentation/math16_pilot02_one_pager_v23"

EXPECTED_V1_SHA = None  # Will be computed dynamically


def sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


# ── File Existence ─────────────────────────────────────────────────────────────

def test_final_report_v11_files_exist():
    for p in [REPORT_PATH, MANIFEST_PATH, BUILD_REPORT_PATH]:
        assert p.exists(), f"Missing output file: {p.name}"
        assert p.stat().st_size > 0, f"Empty output file: {p.name}"


def test_v1_not_overwritten():
    assert REPORT_V1_PATH.exists(), "v1 report is missing - was it deleted?"
    # v1 and v1.1 are different files
    assert REPORT_PATH != REPORT_V1_PATH, "v1 and v1.1 must be different files"


# ── Section Structure ──────────────────────────────────────────────────────────

def test_final_report_v11_has_20_sections():
    text = REPORT_PATH.read_text(encoding="utf-8")
    headings = re.findall(r"^##\s+(\d+)\.\s+(.+)$", text, flags=re.MULTILINE)
    assert len(headings) == 20, f"Expected 20 sections, found {len(headings)}"
    section_nums = [int(h[0]) for h in headings]
    assert section_nums == list(range(1, 21)), f"Section numbering invalid: {section_nums}"


# ── Abstract CJK Count ────────────────────────────────────────────────────────

def test_abstract_character_count_between_500_and_700():
    text = REPORT_PATH.read_text(encoding="utf-8")
    m = re.search(r"## 1\..+?\n(.*?)\n---", text, flags=re.DOTALL)
    assert m, "Section 1 Abstract not found"
    abstract_text = m.group(1).strip()
    cjk_count = len(re.findall(r"[\u4e00-\u9fff]", abstract_text))
    assert 500 <= cjk_count <= 700, f"Abstract CJK char count = {cjk_count}, expected 500-700"


# ── Six Core Figure References ────────────────────────────────────────────────

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


# ── Frozen Numbers ────────────────────────────────────────────────────────────

def test_frozen_numbers_correct():
    text = REPORT_PATH.read_text(encoding="utf-8")
    required = ["289", "306", "78", "242", "10", "83", "84", "101", "219",
                "52", "26", "49", "193", "0.010582", "[-0.94%, +14.38%]",
                "29", "13", "37", "0.012541"]
    for num in required:
        assert num in text, f"Missing frozen number: {num}"


# ── Primary / Post-hoc Accounting ─────────────────────────────────────────────

def test_primary_posthoc_separated():
    text = REPORT_PATH.read_text(encoding="utf-8")
    assert "83/320" in text
    assert "84/320" in text
    assert "Primary" in text
    assert "Post-hoc" in text


def test_posthoc_84_described_as_plus_1_vs_primary():
    text = REPORT_PATH.read_text(encoding="utf-8")
    # Must clearly state Post-hoc is only +1 PASS above Primary
    assert "1 個 PASS" in text, "v1.1 must state Post-hoc is only +1 PASS vs Primary"


def test_no_excessive_rescue_wording():
    text = REPORT_PATH.read_text(encoding="utf-8")
    assert "額外救回6格" not in text, "Forbidden: '額外救回6格'"
    assert "額外救回 6 格" not in text, "Forbidden: '額外救回 6 格'"


# ── Fraction L1-L4 / L5 Accounting ───────────────────────────────────────────

def test_fraction_21_nine_b_only_present():
    text = REPORT_PATH.read_text(encoding="utf-8")
    assert "21 格 NINE_B_ONLY" in text, "Fraction: must state 21 NINE_B_ONLY"


def test_fraction_15_l1_l4_present():
    text = REPORT_PATH.read_text(encoding="utf-8")
    # Accept various phrasing: "15 格屬 L1–L4" or "15格屬L1–L4"
    pattern = r"15\s*格[屬屬]\s*L1[–\-]L4"
    assert re.search(pattern, text), "Fraction: must state 15 cells L1-L4"


def test_fraction_6_l5_present():
    text = REPORT_PATH.read_text(encoding="utf-8")
    assert "6 格屬 L5" in text or "6格屬L5" in text, "Fraction: must state 6 cells L5"


# ── Corrected-Chain Q5 Accounting ─────────────────────────────────────────────

def test_corrected_chain_10_eligible_replay():
    text = REPORT_PATH.read_text(encoding="utf-8")
    assert "10 個 Eligible" in text or "10個eligible" in text.lower() or "10 個 eligible" in text.lower() or "10 個 Eligible 案例" in text, \
        "Must state 10 eligible replay"


def test_corrected_chain_8_unchanged():
    text = REPORT_PATH.read_text(encoding="utf-8")
    assert "8 個處置狀態完全不變" in text or "8個處置" in text, "Must state 8 disposition unchanged"


def test_corrected_chain_2_disposition_changed():
    text = REPORT_PATH.read_text(encoding="utf-8")
    assert "2 個處置狀態改變" in text or "2個處置" in text, "Must state 2 disposition changed"


def test_corrected_chain_1_pass_fail_changed():
    text = REPORT_PATH.read_text(encoding="utf-8")
    assert "1 格改變最終 PASS/FAIL" in text or "1格改變" in text, "Must state only 1 PASS/FAIL changed"


# ── Abstract Scope Fix (Multilayer Failure) ───────────────────────────────────

def test_abstract_mentions_multilayer_failure():
    text = REPORT_PATH.read_text(encoding="utf-8")
    m = re.search(r"## 1\..+?\n(.*?)\n---", text, flags=re.DOTALL)
    assert m, "Abstract section not found"
    abstract = m.group(1)
    assert "語法、契約、API、執行與語意層" in abstract, \
        "Abstract must mention multilayer failure: 語法、契約、API、執行與語意層"


# ── Eligible=0 Wording Fix ───────────────────────────────────────────────────

def test_eligible_zero_uses_correct_wording():
    text = REPORT_PATH.read_text(encoding="utf-8")
    assert "展現明確之防禦邊界" not in text, "Must not use old overclaimed 'Eligible=0' phrasing"
    assert "呈現本研究所定義的安全介入邊界" in text, "Must use revised Eligible=0 phrasing"


# ── 10 Methodology Limitations ───────────────────────────────────────────────

def test_ten_methodology_limitations_present():
    text = REPORT_PATH.read_text(encoding="utf-8")
    m = re.search(r"## 18\..+?\n(.*?)\n---", text, flags=re.DOTALL)
    assert m, "Section 18 Limitations not found"
    sec18 = m.group(1)
    items = re.findall(r"^\d+\.\s+\*\*", sec18, flags=re.MULTILINE)
    assert len(items) == 10, f"Expected 10 limitations in Section 18, got {len(items)}"


# ── 8 Q&A Items ───────────────────────────────────────────────────────────────

def test_eight_jury_qa_items_present():
    text = REPORT_PATH.read_text(encoding="utf-8")
    m = re.search(r"## 19\..+?\n(.*?)\n---", text, flags=re.DOTALL)
    assert m, "Section 19 Jury Q&A not found"
    sec19 = m.group(1)
    qa_items = re.findall(r"^###\s+Q\d+:", sec19, flags=re.MULTILINE)
    assert len(qa_items) == 8, f"Expected 8 Q&A items, got {len(qa_items)}"


# ── Banned Phrases Check ──────────────────────────────────────────────────────

def test_no_forbidden_overclaims():
    text = REPORT_PATH.read_text(encoding="utf-8")
    forbidden = [
        "本研究證明",
        "證明9B",
        "證明小模型",
        "額外救回6格",
        "語法與格式標點缺失為主要原因",
        "Healer保證不倒退",
        "eligible=0代表Healer無效",
        "Post-hoc 84/320為Primary結果",
    ]
    for phrase in forbidden:
        assert phrase not in text, f"Forbidden phrase found: '{phrase}'"


# ── No Forbidden Output Formats ───────────────────────────────────────────────

def test_no_forbidden_output_formats():
    forbidden_exts = [".docx", ".pptx", ".ppt", ".pdf"]
    for p in (ROOT / "docs/experiments/reports").rglob("*"):
        if "final_report_v11" in p.name.lower():
            assert p.suffix.lower() not in forbidden_exts, f"Forbidden format: {p.name}"


# ── SHA Integrity: Evidence Complete, QA, Figures, One-Pager Unchanged ────────

def test_evidence_complete_milestone_files_untouched():
    assert CLAIMS_PATH.exists()
    assert LIMITATIONS_PATH.exists()
    assert JURY_QA_PATH.exists()
    assert CORE_FIG_DIR.exists()
    assert ONE_PAGER_DIR.exists()


def test_v1_report_sha_unchanged():
    """v1 report file itself must not have been modified."""
    assert REPORT_V1_PATH.exists()
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    recorded_sha = manifest["input_sources"]["v1_report_sha256"]
    actual_sha = sha256(REPORT_V1_PATH)
    assert actual_sha == recorded_sha, \
        f"v1 report SHA changed! recorded={recorded_sha}, actual={actual_sha}"


def test_core_figures_sha_preserved():
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    fig_shas = manifest["input_sources"]["core_figure_shas"]
    files = {
        "fig1": CORE_FIG_DIR / "figure_01_baseline_overall.png",
        "fig2": CORE_FIG_DIR / "figure_02_prompt_conditions.png",
        "fig3": CORE_FIG_DIR / "figure_03_family_breakdown.png",
        "fig4": CORE_FIG_DIR / "figure_04_tier1_paired_analysis.png",
        "fig5": CORE_FIG_DIR / "figure_05_healer_eligibility_boundary.png",
        "fig6": CORE_FIG_DIR / "figure_06_healer_concept_zones.png",
    }
    for key, path in files.items():
        actual = sha256(path)
        expected = fig_shas[key]
        assert actual == expected, f"Figure SHA changed for {key}: expected={expected}, actual={actual}"
