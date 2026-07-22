# -*- coding: utf-8 -*-
"""Final manual acceptance tests for Math16 Pilot-02 Final Report v1.3."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "docs/experiments/reports/math16_pilot02_final_report_v13.md"
MANIFEST = ROOT / "docs/experiments/reports/math16_pilot02_final_report_v13_manifest.json"
BUILD_REPORT = ROOT / "docs/experiments/reports/math16_pilot02_final_report_v13_build_report.md"
V1 = ROOT / "docs/experiments/reports/math16_pilot02_final_report_v1.md"
V11 = ROOT / "docs/experiments/reports/math16_pilot02_final_report_v11.md"
V12 = ROOT / "docs/experiments/reports/math16_pilot02_final_report_v12.md"
TASK_ROSTER = ROOT / "docs/experiments/manifests/math16_three_model_five_seed_manifest.json"
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


def test_files_exist_and_structure_preserved():
    for path in (REPORT, MANIFEST, BUILD_REPORT):
        assert path.exists() and path.stat().st_size > 0
    text = REPORT.read_text(encoding="utf-8")
    headings = re.findall(r"^##\s+(\d+)\.", text, flags=re.MULTILINE)
    assert [int(x) for x in headings] == list(range(1, 21))
    assert len(re.findall(r"!\[Figure\s+\d+", text)) == 6


def test_section4_and_16_no_guarantee_wording_for_regression():
    text = REPORT.read_text(encoding="utf-8")
    sec4 = section(text, 4)
    sec16 = section(text, 16)
    for scope, label in ((sec4, "Section 4"), (sec16, "Section 16")):
        assert "確保" not in scope, f"{label} must not use '確保' to describe Regression defenses"
        assert "保證" not in scope, f"{label} must not use '保證' to describe Regression defenses"
        assert "降低" in scope and "風險" in scope, f"{label} must use risk-reduction wording"
    assert "零倒退防禦" in sec4
    assert "零倒退防線" in sec16


def test_section14_sample_bound_and_no_causal_overclaim():
    text = REPORT.read_text(encoding="utf-8")
    sec14 = section(text, 14)
    assert "證實主因" not in sec14, "Section 14 must not overclaim '證實主因'"
    assert "27 格" in sec14 and "診斷樣本" in sec14
    assert "未建立 Prompt 結構與生成錯誤之因果關係" in sec14 or "未建立" in sec14
    assert "不可外推" in sec14
    assert "完全排除 Parser" not in sec14.replace("亦不可外推為全域比例或完全排除 Parser 影響", "")
    assert "21/27" in sec14 and "18.5%" in sec14


def test_section15_figure2_no_zheng_ming_and_accounting_intact():
    text = REPORT.read_text(encoding="utf-8")
    sec15 = section(text, 15)
    assert "證明" not in sec15, "Section 15 must not contain '證明'"
    assert "80/80" in sec15
    assert "63/80" in sec15
    assert "spec-v1" in sec15 and "spec-v2" in sec15
    assert "Post-hoc 機制驗證" in sec15
    assert "不得假裝為完全同條件之 Primary 直接推論" in sec15


def test_section5_task_ids_match_official_roster():
    text = REPORT.read_text(encoding="utf-8")
    roster = json.loads(TASK_ROSTER.read_text(encoding="utf-8"))
    official_ids = set(roster["task_ids"])
    sec5_match = re.search(r"### 題庫設計\n(.*?)\n\n### 測試模型", text, flags=re.DOTALL)
    assert sec5_match, "Section 5 題庫設計 not found"
    sec5_ids = set(re.findall(r"`(ce\w+)`", sec5_match.group(1)))
    assert sec5_ids == official_ids, f"mismatch: {sec5_ids ^ official_ids}"
    assert len(sec5_ids) == 16
    forbidden_placeholders = [f"`ce10{i}`" for i in range(1, 5)] + [
        "`ce113`", "`ce114`", "`ce116`", "`ce121`", "`ce122`", "`ce123`", "`ce124`",
        "`ce131`", "`ce132`", "`ce133`", "`ce134`",
    ]
    for placeholder in forbidden_placeholders:
        assert placeholder not in text, f"Forbidden placeholder task id found: {placeholder}"
    assert "`ce115`" not in text, "Bare non-official ce115 identifier must not remain"


def test_polynomial_anomaly_task_id_is_full_official_id_everywhere():
    text = REPORT.read_text(encoding="utf-8")
    official_id = "ce115_calc_polynomial_division_l1"
    for number in (5, 14, 18):
        assert official_id in section(text, number), (
            f"Section {number} must use the complete official Polynomial anomaly task id"
        )
    assert not re.search(r"`ce115`", text), "Bare non-official ce115 reference found"


def test_section20_abstain_wording_conservative():
    text = REPORT.read_text(encoding="utf-8")
    sec20 = section(text, 20)
    assert "有效維護整體架構之安全性" not in sec20
    assert "降低盲目修改帶來之風險" in sec20
    assert "維持整體架構之可解釋性" in sec20


def test_primary_posthoc_accounting_preserved():
    text = REPORT.read_text(encoding="utf-8")
    scopes = [section(text, 1), section(text, 10), section(text, 11)]
    q5 = re.search(r"### Q5:.*?\n(.*?)(?=### Q6:)", section(text, 19), re.DOTALL)
    assert q5
    scopes.append(q5.group(1))
    for scope in scopes:
        compact = normalized(scope)
        assert "78/320" in compact
        assert "83/320" in compact
        assert "84/320" in compact
        assert "1個pass" in compact
        assert ("totalrescue=6" in compact or "總救援" in compact)
    forbidden = ("額外增加6格", "額外救回6格", "83+6")
    assert all(term not in normalized(text) for term in forbidden)


def test_fraction_21_15_6_preserved():
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
        assert "不可解讀為純數學" in scope


def test_corrected_chain_10_8_2_1_preserved():
    text = REPORT.read_text(encoding="utf-8")
    q5 = re.search(r"### Q5:.*?\n(.*?)(?=### Q6:)", section(text, 19), re.DOTALL)
    assert q5
    body = q5.group(1)
    assert "10 個 Eligible" in body
    assert "8 個處置狀態完全不變" in body
    assert "2 個處置狀態改變" in body
    assert "1 格改變最終 PASS/FAIL" in body


def test_section18_exactly_ten_limitations_preserved():
    text = REPORT.read_text(encoding="utf-8")
    v12 = V12.read_text(encoding="utf-8")
    evidence = LIMITATIONS.read_text(encoding="utf-8")
    sec18 = section(text, 18)
    items = re.findall(r"^(\d+)\.\s+\*\*(.+?)\*\*", sec18, re.MULTILINE)
    assert len(items) == 10
    assert [int(n) for n, _ in items] == list(range(1, 11))
    v12_items = re.findall(r"^(\d+)\.\s+\*\*(.+?)\*\*", section(v12, 18), re.MULTILINE)
    evidence_items = re.findall(r"^(\d+)\.\s+\*\*(.+?)\*\*", evidence, re.MULTILINE)
    assert items == v12_items == evidence_items


def test_no_forbidden_overclaims_remaining():
    text = REPORT.read_text(encoding="utf-8")
    forbidden = [
        "本研究證明",
        "額外救回6格",
        "額外救回 6 格",
        "語法與格式標點缺失",
        "保證不倒退",
    ]
    assert all(phrase not in text for phrase in forbidden)


def test_source_and_figure_sha_protection():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    recorded = manifest["source_shas"]
    assert sha(V1) == recorded["v1_sha256"]
    assert sha(V11) == recorded["v11_sha256"]
    assert sha(V12) == recorded["v12_sha256"]
    assert sha(TASK_ROSTER) == recorded["task_roster_sha256"]
    assert sha(EVIDENCE_MANIFEST) == recorded["evidence_complete_manifest_sha256"]
    assert sha(LIMITATIONS) == recorded["evidence_complete_limitations_sha256"]
    assert sha(INTEGRATED) == recorded["integrated_report_sha256"]
    assert sha(QA) == recorded["jury_qa_sha256"]
    assert sha(REPORT) == manifest["v13_sha256"]
    for name, expected in recorded["core_figure_shas"].items():
        assert sha(FIG_DIR / name) == expected


def test_no_forbidden_binary_outputs():
    forbidden = {".docx", ".pdf", ".ppt", ".pptx"}
    for path in (ROOT / "docs/experiments/reports").glob("math16_pilot02_final_report_v13*"):
        assert path.suffix.lower() not in forbidden
    assert not any(
        token in path.name.lower()
        for path in (ROOT / "docs/experiments/reports").glob("math16_pilot02_final_report_v13*")
        for token in ("poster", "slide")
    )
