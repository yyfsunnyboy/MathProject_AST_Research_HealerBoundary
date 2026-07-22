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
    assert "214" in qa_content

    # Tier 1 paired numbers
    assert "0.010582" in qa_content
    assert "0.012541" in qa_content
    assert "14" in qa_content
    assert "77.8%" in qa_content
    assert "18.5%" in qa_content
    assert "3.7%" in qa_content


def test_non_overclaiming_guardrails():
    qa_content = QA_FINAL_PATH.read_text(encoding="utf-8")

    # In body answers, regression should be qualified as "觀察到" or "Regression=0" rather than absolute guarantee
    assert "保證絕不倒退" not in qa_content.split("## 二、 評審口試不可宣稱之事項")[0]
    assert "100%安全" not in qa_content.split("## 二、 評審口試不可宣稱之事項")[0]
    assert "完全不會倒退" not in qa_content.split("## 二、 評審口試不可宣稱之事項")[0]
