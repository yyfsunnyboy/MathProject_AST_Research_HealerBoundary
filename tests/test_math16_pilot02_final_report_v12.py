# -*- coding: utf-8 -*-
"""Full-text consistency tests for Math16 Pilot-02 Final Report v1.2."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "docs/experiments/reports/math16_pilot02_final_report_v12.md"
MANIFEST = ROOT / "docs/experiments/reports/math16_pilot02_final_report_v12_manifest.json"
BUILD_REPORT = ROOT / "docs/experiments/reports/math16_pilot02_final_report_v12_build_report.md"
V1 = ROOT / "docs/experiments/reports/math16_pilot02_final_report_v1.md"
V11 = ROOT / "docs/experiments/reports/math16_pilot02_final_report_v11.md"
EVIDENCE_MANIFEST = ROOT / "docs/experiments/milestones/math16_pilot02_evidence_complete_v1/evidence_complete_manifest.json"
LIMITATIONS = ROOT / "docs/experiments/milestones/math16_pilot02_evidence_complete_v1/interpretation_limitations.md"
INTEGRATED = ROOT / "docs/experiments/reports/math16_pilot02_integrated_results_report_v1.md"
QA = ROOT / "docs/experiments/reports/math16_pilot02_jury_qa_final_v1.md"
FIG_DIR = ROOT / "docs/experiments/visualization/math16_pilot02_core_figures_v1"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def section(text: str, number: int) -> str:
    match = re.search(
        rf"^## {number}\..*?\n(.*?)(?=^## {number + 1}\.|\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    assert match, f"section {number} missing"
    return match.group(1)


def normalized(text: str) -> str:
    return re.sub(r"[\s*`]+", "", text).lower()


def test_files_and_structure_preserved():
    for path in (REPORT, MANIFEST, BUILD_REPORT):
        assert path.exists() and path.stat().st_size > 0
    text = REPORT.read_text(encoding="utf-8")
    headings = re.findall(r"^##\s+(\d+)\.", text, flags=re.MULTILINE)
    assert [int(x) for x in headings] == list(range(1, 21))
    figures = [f"figure_0{i}_" for i in range(1, 7)]
    assert all(marker in text for marker in figures)
    assert len(re.findall(r"!\[Figure\s+\d+", text)) == 6


def test_primary_posthoc_four_locations_consistent():
    text = REPORT.read_text(encoding="utf-8")
    scopes = [section(text, 1), section(text, 10), section(text, 11)]
    q5 = re.search(r"### Q5:.*?\n(.*?)(?=### Q6:)", section(text, 19), re.DOTALL)
    assert q5
    scopes.append(q5.group(1))
    for scope in scopes:
        compact = normalized(scope)
        assert "78/320" in compact
        assert (
            "primaryrescue=5" in compact
            or "primaryrescue(救援成功)：5格" in compact
            or "救援5格" in compact
            or "5格(83/320)" in compact
        )
        assert "83/320" in compact
        assert ("totalrescue=6" in compact or "總救援" in compact)
        assert "84/320" in compact
        assert "1個pass" in compact
    forbidden = ("額外增加6格", "額外救回6格", "83+6")
    assert all(term not in normalized(text) for term in forbidden)


def test_fraction_three_locations_consistent():
    text = REPORT.read_text(encoding="utf-8")
    scopes = [section(text, 13), section(text, 14)]
    q8 = re.search(r"### Q8:.*?\n(.*?)(?=^---|\Z)", section(text, 19), re.DOTALL | re.MULTILINE)
    assert q8
    scopes.append(q8.group(1))
    for scope in scopes:
        compact = normalized(scope)
        assert ("nine_b_only=21" in compact or "21格nine_b_only" in compact or "21格9b-only" in compact)
        assert ("l1–l4=15" in compact or "15格屬l1–l4" in compact or "15格(71.43%)屬l1~l4" in compact)
        assert ("l5=6" in compact or "6格屬l5" in compact)
        assert all(term in scope for term in ("語法", "契約", "API", "執行"))
        assert "不可解讀為純數學" in scope


def test_corrected_chain_10_8_2_1_complete():
    text = REPORT.read_text(encoding="utf-8")
    q5 = re.search(r"### Q5:.*?\n(.*?)(?=### Q6:)", section(text, 19), re.DOTALL)
    assert q5
    body = q5.group(1)
    assert "10 個 Eligible" in body
    assert "8 個處置狀態完全不變" in body
    assert "2 個處置狀態改變" in body
    assert "1 格改變最終 PASS/FAIL" in body
    scopes = [section(text, n) for n in (1, 10, 11, 19, 20)]
    for scope in scopes:
        if "84/320" in scope:
            compact = normalized(scope)
            assert "post-hoc" in compact
            assert ("totalrescue" in compact or "總救援" in compact)
            assert "1個pass" in compact


def test_section18_exactly_ten_limitations_preserved():
    text = REPORT.read_text(encoding="utf-8")
    v11 = V11.read_text(encoding="utf-8")
    evidence = LIMITATIONS.read_text(encoding="utf-8")
    sec18 = section(text, 18)
    items = re.findall(r"^(\d+)\.\s+\*\*(.+?)\*\*", sec18, re.MULTILINE)
    assert len(items) == 10
    assert [int(n) for n, _ in items] == list(range(1, 11))
    v11_items = re.findall(r"^(\d+)\.\s+\*\*(.+?)\*\*", section(v11, 18), re.MULTILINE)
    evidence_items = re.findall(r"^(\d+)\.\s+\*\*(.+?)\*\*", evidence, re.MULTILINE)
    assert items == v11_items == evidence_items
    assert "Post-hoc 探索性分析" in sec18
    assert "不可宣稱「保證在任意情境下 100% 絕不倒退」" in sec18


def test_forbidden_phrases_zero_and_frozen_numbers_present():
    text = REPORT.read_text(encoding="utf-8")
    forbidden = [
        "本研究證明",
        "額外救回6格",
        "額外救回 6 格",
        "語法與格式標點缺失",
        "保證不倒退",
    ]
    assert all(phrase not in text for phrase in forbidden)
    required = [
        "289/320", "101/320", "78/320", "83/320", "84/320",
        "52", "26", "49", "193", "0.010582", "[-0.94%, +14.38%]",
        "NINE_B_ONLY = 21", "L1–L4 = 15", "L5 = 6",
    ]
    assert all(value in text for value in required)


def test_source_and_figure_sha_protection():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    recorded = manifest["source_shas"]
    assert sha(V1) == recorded["v1_sha256"]
    assert sha(V11) == recorded["v11_sha256"]
    assert sha(EVIDENCE_MANIFEST) == recorded["evidence_complete_manifest_sha256"]
    assert sha(LIMITATIONS) == recorded["evidence_complete_limitations_sha256"]
    assert sha(INTEGRATED) == recorded["integrated_report_sha256"]
    assert sha(QA) == recorded["jury_qa_sha256"]
    assert sha(REPORT) == manifest["v12_sha256"]
    for name, expected in recorded["core_figure_shas"].items():
        assert sha(FIG_DIR / name) == expected


def test_no_forbidden_binary_outputs():
    forbidden = {".docx", ".pdf", ".ppt", ".pptx"}
    for path in (ROOT / "docs/experiments/reports").glob("math16_pilot02_final_report_v12*"):
        assert path.suffix.lower() not in forbidden
    assert not any(
        token in path.name.lower()
        for path in (ROOT / "docs/experiments/reports").glob("math16_pilot02_final_report_v12*")
        for token in ("poster", "slide")
    )
