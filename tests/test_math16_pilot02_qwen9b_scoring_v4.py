# -*- coding: utf-8 -*-
"""Tests for Qwen9B Pilot-02 v4 baseline scoring closeout."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs/experiments/results/math16_pilot02_qwen9b_evaluation_v4_r001"
PLAN = ROOT / "docs/experiments/manifests/math16_pilot02_qwen9b_cell_plan.json"
FREEZE = ROOT / "docs/experiments/manifests/math16_pilot02_qwen9b_generation_evidence_freeze_v1.json"
RUNNER = ROOT / "scripts/evaluate_math16_pilot02_qwen9b_v4.py"
EVALUATOR = ROOT / "scripts/evaluate_math16_pilot02_full_v4.py"
TAXONOMY = ROOT / "docs/決賽文件/20260720_AI 生成程式共同失敗分類標準_實際使用版 v3.md"
EXPECTED_CLOSURE = "dedac60aceb5d285a86d3b5cc35ce8064a317c2b52ecc66a673f48632fb6cccf"
EXPECTED_EVAL = "2cca19f2258d4ba6134ff10d4e9bcff925e2441c32820fcbc151cb6b1dd740bc"
EXPECTED_TAX = "7df8f4472ce048569967436cbc73ede8fd4bd117ad67d0028ddd95af2055a304"
EXPECTED_FP = "f45f79238bbf9400729fd00dbfaf4e33a7a7716cb9f81d4095a1fd1d52e0da5b"
EXPECTED_DIGEST = "6488c96fa5faab64bb65cbd30d4289e20e6130ef535a93ef9a49f42eda893ea7"
EXPECTED_HEAD = "74d1e56cf14e3cf01e68e5bda018fa3f143cbe30"


def test_runner_is_offline_baseline_only():
    text = RUNNER.read_text(encoding="utf-8")
    assert "classify_math16_response" in text
    assert "classify_outcome_to_v3" in text
    assert "not_run" in text
    assert "call_qwen" not in text
    assert "call_gemini" not in text
    assert "MathHealerRunner" not in text
    assert "EXPECTED_EVAL_HASH" in text
    assert EXPECTED_EVAL in text
    assert EXPECTED_TAX in text


def test_evaluator_and_taxonomy_match_qwen4b_formal():
    assert hashlib.sha256(EVALUATOR.read_bytes()).hexdigest() == EXPECTED_EVAL
    assert hashlib.sha256(TAXONOMY.read_bytes()).hexdigest() == EXPECTED_TAX
    q4 = json.loads(
        (
            ROOT
            / "docs/experiments/results/math16_pilot02_qwen4b_evaluation_v4_r001/baseline_summary.json"
        ).read_text(encoding="utf-8")
    )
    assert q4["evaluator_hash"] == EXPECTED_EVAL
    assert q4["taxonomy_hash"] == EXPECTED_TAX


def test_evaluator_hash_frozen_in_summary():
    summary = json.loads((OUT / "baseline_summary.json").read_text(encoding="utf-8"))
    assert summary["evaluator_hash"] == EXPECTED_EVAL
    assert summary["taxonomy_hash"] == EXPECTED_TAX
    assert summary["corpus_sha_closure"] == EXPECTED_CLOSURE
    assert summary["runtime_config_fingerprint"] == EXPECTED_FP
    assert summary["model_digest"] == EXPECTED_DIGEST
    assert summary["source_generation_commit"] == EXPECTED_HEAD
    assert summary["model_tag"] == "qwen3.5:9b"
    assert summary["healer"]["rescued"] == "not_run"
    assert summary["healer"]["regression"] == "not_run"
    assert summary["healer"]["post_healer"] == "not_run"
    assert summary["llm_calls"] == 0
    assert summary["ab3"] is False
    assert summary["total"] == 320
    assert summary["passed"] + summary["failed"] == 320
    assert summary["suspected_schema_false_negative_candidates"] == 0


def test_scored_all_320_unique():
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    rows = [
        json.loads(l)
        for l in (OUT / "cell_level_baseline.jsonl").read_text(encoding="utf-8").splitlines()
        if l.strip()
    ]
    assert len(rows) == 320
    assert len({r["cell_id"] for r in rows}) == 320
    assert {r["cell_id"] for r in rows} == {c["cell_id"] for c in plan}
    for r in rows:
        assert r["evaluation_revision"] == "v4_r001"
        assert r["rescued"] == "not_run"
        assert r["regression"] == "not_run"
        assert r["post_healer_status"] == "not_run"
        assert r["baseline_only"] is True
        assert r["raw_artifact_sha256"]
        assert r["raw_response_sha256"]
        assert r["evaluator_hash"] == EXPECTED_EVAL
        assert r["taxonomy_hash"] == EXPECTED_TAX
        assert r["model_tag"] == "qwen3.5:9b"


def test_completeness_audit_passed():
    audit = json.loads((OUT / "scoring_completeness_audit.json").read_text(encoding="utf-8"))
    assert audit["passed"] is True
    assert audit["scored"] == 320
    assert audit["duplicate"] == []
    assert audit["missing"] == []
    assert audit["unscored"] == []
    assert audit["evaluator_crash"] == []
    assert audit["raw_sha_mismatch"] == []
    assert audit["unknown_cell_identity"] == []
    assert audit["suspected_schema_false_negative_candidates"] == 0
    assert audit["rescued"] == "not_run"
    assert audit["llm_calls"] == 0


def test_corpus_freeze_untouched():
    freeze = json.loads(FREEZE.read_text(encoding="utf-8"))
    assert freeze["corpus_sha_closure"] == EXPECTED_CLOSURE
    assert freeze["runtime_config_fingerprint"] == EXPECTED_FP
    assert freeze["model_digest"] == EXPECTED_DIGEST


def test_summaries_exist():
    for name in (
        "baseline_summary.json",
        "overall_summary.json",
        "condition_summary.json",
        "family_summary.json",
        "task_summary.json",
        "seed_summary.json",
        "failure_taxonomy_summary.json",
        "scoring_manifest.json",
        "scoring_completeness_audit.json",
        "suspected_schema_false_negative_candidates.json",
        "report.md",
        "cell_level_baseline.jsonl",
    ):
        assert (OUT / name).exists()
