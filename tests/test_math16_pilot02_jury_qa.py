# -*- coding: utf-8 -*-
"""Verification tests for Jury Defense Q&A 19 Finalized artifact and Section 16."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

QA_FINAL_PATH = ROOT / "docs/experiments/reports/math16_pilot02_jury_qa_final_v1.md"
REPORT_PATH = ROOT / "docs/experiments/reports/math16_pilot02_integrated_results_report_v1.md"


def test_qa_files_exist():
    assert QA_FINAL_PATH.exists(), "Missing Jury QA final artifact"
    assert REPORT_PATH.exists(), "Missing Integrated report artifact"


def test_exactly_19_questions():
    qa_content = QA_FINAL_PATH.read_text(encoding="utf-8")
    q_matches = re.findall(r"### Q(\d+):", qa_content)
    assert len(q_matches) == 19
    assert [int(q) for q in q_matches] == list(range(1, 20))

    report_content = REPORT_PATH.read_text(encoding="utf-8")
    report_q_matches = re.findall(r"### Q(\d+):", report_content)
    assert len(report_q_matches) == 19
    assert [int(q) for q in report_q_matches] == list(range(1, 20))


def test_formal_and_oral_short_answers_exist():
    qa_content = QA_FINAL_PATH.read_text(encoding="utf-8")
    for i in range(1, 20):
        assert f"### Q{i}:" in qa_content

    formal_count = len(re.findall(r"\*\*正式回答[：:]\*\*", qa_content))
    oral_count = len(re.findall(r"\*\*口試短答[：:]\*\*", qa_content))

    assert formal_count == 19
    assert oral_count == 19


def test_numeric_consistency_in_qa():
    qa_content = QA_FINAL_PATH.read_text(encoding="utf-8")

    # Gemini & Qwen core numbers
    assert "289" in qa_content
    assert "78" in qa_content
    assert "101" in qa_content
    assert "320" in qa_content
    assert "83/320" in qa_content
    assert "84/320" in qa_content
    assert "219" in qa_content

    # Tier 1 paired numbers
    assert "0.010582" in qa_content
    assert "0.012541" in qa_content
    assert "14" in qa_content
    assert "77.8%" in qa_content
    assert "18.5%" in qa_content
    assert "3.7%" in qa_content


def test_q9_gemini_v2_boundary_clarification():
    qa_content = QA_FINAL_PATH.read_text(encoding="utf-8")
    assert "Gemini 的正式生成只比較到 Ab2d+spec-v1" in qa_content
    assert "Gemini 沒有正式重新生成 Ab2d+spec-v2" in qa_content
    assert "不能當作正式四條件比較結果" in qa_content
    assert "Prompt 效果依模型、提示版本與部署條件而異" in qa_content


def test_q17_corrected_chain_disposition_reconciliation():
    qa_content = QA_FINAL_PATH.read_text(encoding="utf-8")
    assert "8 格在 Primary 與 corrected-chain replay 間完全不變" in qa_content
    assert "2 格處置狀態改變" in qa_content
    assert "1 格改變最終 PASS/FAIL 結果" in qa_content
    assert "其餘 9 格" not in qa_content
    assert "9 格完全一致" not in qa_content


def test_non_overclaiming_guardrails():
    qa_content = QA_FINAL_PATH.read_text(encoding="utf-8")
    report_content = REPORT_PATH.read_text(encoding="utf-8")

    prohibited_phrases = [
        "其餘 9 格",
        "9 格完全一致",
        "保證實驗結果真實",
        "證明高能力模型",
        "自然收斂至 0",
        "零倒退工程防禦",
        "McNemar 證明",
        "深層邏輯缺失",
        "71.43% 失敗於語法與格式",
    ]

    for phrase in prohibited_phrases:
        assert phrase not in qa_content, f"Prohibited phrase '{phrase}' found in QA final"
        assert phrase not in report_content, f"Prohibited phrase '{phrase}' found in Integrated report"

    # In body answers, regression should be qualified
    body_content = qa_content.split("## 二、 評審口試不可宣稱之事項")[0]
    assert "保證絕不倒退" not in body_content
    assert "100%安全" not in body_content
    assert "完全不會倒退" not in body_content
