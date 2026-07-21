# -*- coding: utf-8 -*-
"""Closeout tests for Qwen4B Pilot-02 frozen Healer v4_r001."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs/experiments/results/math16_pilot02_qwen4b_healer_v4_r001"
RUNNER = ROOT / "scripts/evaluate_math16_pilot02_qwen4b_healer_v4.py"
BASELINE = (
    ROOT
    / "docs/experiments/results/math16_pilot02_qwen4b_evaluation_v4_r001/cell_level_baseline.jsonl"
)
EVALUATOR = ROOT / "scripts/evaluate_math16_pilot02_full_v4.py"
HEALER_RUNNER = ROOT / "agent_tools/finals_rebuild/ce115_research_healer_runner.py"
PROTOCOL = ROOT / "agent_tools/finals_rebuild/ce115_research_healer_protocol.py"
TAXONOMY = ROOT / "docs/決賽文件/20260720_AI 生成程式共同失敗分類標準_實際使用版 v3.md"

EXPECTED_CLOSURE = "7dd3ba5f7e7a38e7ad20142e8c5c5b2e84c20df1b7f5abcf5701c23d24172a22"
EXPECTED_EVAL = "2cca19f2258d4ba6134ff10d4e9bcff925e2441c32820fcbc151cb6b1dd740bc"
EXPECTED_TAX = "7df8f4472ce048569967436cbc73ede8fd4bd117ad67d0028ddd95af2055a304"
EXPECTED_RUNNER = "b89e6059ce67efb622aa2e085e365b909d0d4f7df1a6814c1dc83df029ce81e1"
EXPECTED_PROTO = "bdb4121ee266f91bfa116019a334cf4a528da0d71629b96540a5f763826aff39"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_jsonl(path: Path) -> list[dict]:
    return [
        json.loads(l)
        for l in path.read_text(encoding="utf-8").splitlines()
        if l.strip()
    ]


def test_pins_unchanged():
    assert sha(EVALUATOR) == EXPECTED_EVAL
    assert sha(TAXONOMY) == EXPECTED_TAX
    assert sha(HEALER_RUNNER) == EXPECTED_RUNNER
    assert sha(PROTOCOL) == EXPECTED_PROTO
    man = json.loads((OUT / "execution_manifest.json").read_text(encoding="utf-8"))
    assert man["corpus_sha_closure"] == EXPECTED_CLOSURE
    assert man["evaluator_hash"] == EXPECTED_EVAL
    assert man["healer_runner_sha256"] == EXPECTED_RUNNER
    assert man["healer_protocol_sha256"] == EXPECTED_PROTO
    assert man["external_eligibility_prefilter"] is True
    assert man["noneligible_direct_run"] is False
    assert man["llm_calls"] == 0
    assert man["qwen9b"] is False


def test_runner_retains_external_prefilter_only_eligible_run():
    text = RUNNER.read_text(encoding="utf-8")
    assert "decide_healer_eligibility" in text
    assert "EXPECTED_ELIGIBLE = 10" in text
    assert "EXPECTED_NONELIGIBLE = 232" in text
    assert "noneligible_direct_run" in text
    assert "MathHealerRunner" in text
    assert "call_gemini" not in text
    assert "qwen3.5:9b" not in text


def test_eligibility_and_execution_completeness():
    elig = _load_jsonl(OUT / "eligibility_inventory.jsonl")
    execs = _load_jsonl(OUT / "eligible_execution_records.jsonl")
    abstain = _load_jsonl(OUT / "abstain_records.jsonl")
    healer = _load_jsonl(OUT / "healer_results.jsonl")
    assert len(elig) == 242
    assert len({r["cell_id"] for r in elig}) == 242
    assert len(execs) == 10
    assert len(abstain) == 232
    assert len(healer) == 320
    assert sum(1 for r in elig if r["healer_eligible"]) == 10
    assert sum(1 for r in elig if not r["healer_eligible"]) == 232
    assert all(r["healer_ran"] for r in execs)
    assert all(not r["healer_ran"] for r in abstain)
    assert all(
        not r["healer_ran"]
        for r in healer
        if r["baseline_final_status"] == "PASSED"
    )
    assert all(
        (not r["healer_eligible"]) or r["healer_ran"]
        for r in healer
        if r["baseline_final_status"] != "PASSED"
    )
    assert all(
        (not r["healer_ran"])
        for r in healer
        if (not r["healer_eligible"]) and r["baseline_final_status"] != "PASSED"
    )


def test_baseline_untouched_and_ledger():
    baseline = _load_jsonl(BASELINE)
    assert sum(1 for r in baseline if r["final_status"] == "PASSED") == 78
    overall = json.loads((OUT / "overall_summary.json").read_text(encoding="utf-8"))
    audit = json.loads((OUT / "completeness_audit.json").read_text(encoding="utf-8"))
    assert overall["counts"]["baseline_pass"] == 78
    assert overall["counts"]["fail_eligible"] == 10
    assert overall["counts"]["fail_noneligible"] == 232
    assert overall["counts"]["healer_ran"] == 10
    assert overall["counts"]["abstained"] == 232
    assert overall["counts"]["regression"] == 0
    assert overall["counts"]["post_healer_pass"] == 83
    assert overall["counts"]["rescued"] == 5
    assert overall["llm_calls"] == 0
    assert overall["qwen9b"] is False
    assert audit["passed"] is True
    assert audit["duplicate"] == []
    assert audit["missing"] == []
    assert audit["unprocessed"] == []
    assert audit["unauthorized_rule"] == []
    assert audit["evaluator_crash"] == []
    assert audit["protocol_error"] == []
    assert audit["raw_sha_mismatch"] == []
    assert audit["noneligible_direct_run"] is False


def test_summaries_exist():
    for name in (
        "eligibility_inventory.jsonl",
        "eligible_execution_records.jsonl",
        "abstain_records.jsonl",
        "healer_results.jsonl",
        "post_healer_scoring.jsonl",
        "overall_summary.json",
        "condition_summary.json",
        "family_summary.json",
        "task_summary.json",
        "completeness_audit.json",
        "execution_manifest.json",
        "report.md",
    ):
        assert (OUT / name).exists()
