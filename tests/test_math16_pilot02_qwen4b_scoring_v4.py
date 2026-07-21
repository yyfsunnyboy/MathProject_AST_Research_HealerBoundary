# -*- coding: utf-8 -*-
"""Tests for Qwen4B Pilot-02 v4 baseline scoring closeout."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs/experiments/results/math16_pilot02_qwen4b_evaluation_v4_r001"
PLAN = ROOT / "docs/experiments/manifests/math16_pilot02_qwen4b_cell_plan.json"
FREEZE = ROOT / "docs/experiments/manifests/math16_pilot02_qwen4b_generation_evidence_freeze_v1.json"
RUNNER = ROOT / "scripts/evaluate_math16_pilot02_qwen4b_v4.py"
EVALUATOR = ROOT / "scripts/evaluate_math16_pilot02_full_v4.py"
EXPECTED_CLOSURE = "7dd3ba5f7e7a38e7ad20142e8c5c5b2e84c20df1b7f5abcf5701c23d24172a22"
EXPECTED_EVAL = "2cca19f2258d4ba6134ff10d4e9bcff925e2441c32820fcbc151cb6b1dd740bc"
EXPECTED_FP = "33fd7603f58cdc47843bb048456d6d167dd71dc891b636377baf33dea30358f7"


def test_runner_is_offline_baseline_only():
    text = RUNNER.read_text(encoding="utf-8")
    assert "classify_math16_response" in text
    assert "classify_outcome_to_v3" in text
    assert "not_run" in text
    assert "call_qwen" not in text
    assert "call_gemini" not in text
    assert "qwen3.5:9b" not in text
    assert "MathHealerRunner" not in text


def test_evaluator_hash_frozen():
    h = hashlib.sha256(EVALUATOR.read_bytes()).hexdigest()
    assert h == EXPECTED_EVAL
    summary = json.loads((OUT / "baseline_summary.json").read_text(encoding="utf-8"))
    assert summary["evaluator_hash"] == EXPECTED_EVAL
    assert summary["corpus_sha_closure"] == EXPECTED_CLOSURE
    assert summary["runtime_config_fingerprint"] == EXPECTED_FP
    assert summary["healer"]["rescued"] == "not_run"
    assert summary["llm_calls"] == 0
    assert summary["total"] == 320
    assert summary["passed"] + summary["failed"] == 320


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
        assert r["raw_artifact_sha256"]
        assert r["raw_response_sha256"]


def test_completeness_audit_passed():
    audit = json.loads((OUT / "scoring_completeness_audit.json").read_text(encoding="utf-8"))
    assert audit["passed"] is True
    assert audit["scored"] == 320
    assert audit["duplicate"] == []
    assert audit["missing"] == []
    assert audit["evaluator_crash"] == []
    assert audit["raw_sha_mismatch"] == []


def test_corpus_freeze_untouched():
    freeze = json.loads(FREEZE.read_text(encoding="utf-8"))
    assert freeze["corpus_sha_closure"] == EXPECTED_CLOSURE


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
        "report.md",
    ):
        assert (OUT / name).exists()
