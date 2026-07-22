# -*- coding: utf-8 -*-
"""Tests for Qwen9B Pilot-02 frozen Healer eligibility closeout (eligibility-only)."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs/experiments/results/math16_pilot02_qwen9b_healer_eligibility_v4_r001"
RUNNER = ROOT / "scripts/evaluate_math16_pilot02_qwen9b_healer_eligibility_v4.py"
BASELINE = (
    ROOT
    / "docs/experiments/results/math16_pilot02_qwen9b_evaluation_v4_r001/cell_level_baseline.jsonl"
)
EVALUATOR = ROOT / "scripts/evaluate_math16_pilot02_full_v4.py"
HEALER_RUNNER = ROOT / "agent_tools/finals_rebuild/ce115_research_healer_runner.py"
PROTOCOL = ROOT / "agent_tools/finals_rebuild/ce115_research_healer_protocol.py"
TAXONOMY = ROOT / "docs/決賽文件/20260720_AI 生成程式共同失敗分類標準_實際使用版 v3.md"
QWEN4B_ELIG = (
    ROOT
    / "docs/experiments/results/math16_pilot02_qwen4b_healer_v4_r001/eligibility_inventory.jsonl"
)

EXPECTED_CLOSURE = "dedac60aceb5d285a86d3b5cc35ce8064a317c2b52ecc66a673f48632fb6cccf"
EXPECTED_EVAL = "2cca19f2258d4ba6134ff10d4e9bcff925e2441c32820fcbc151cb6b1dd740bc"
EXPECTED_TAX = "7df8f4472ce048569967436cbc73ede8fd4bd117ad67d0028ddd95af2055a304"
EXPECTED_RUNNER = "38453d1294382f061efe149484f5a3059a47d085d2aeef358874a954e37adebf"
EXPECTED_PROTO = "bdb4121ee266f91bfa116019a334cf4a528da0d71629b96540a5f763826aff39"
ALLOWED = {
    "eligible",
    "noneligible_no_rule_triggered",
    "abstain_no_extractable_source",
    "abstain_ambiguous_entry_point",
    "pending_review",
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_jsonl(path: Path) -> list[dict]:
    return [
        json.loads(l)
        for l in path.read_text(encoding="utf-8").splitlines()
        if l.strip()
    ]


def test_pins_match_qwen4b_gemini_frozen_policy_assets():
    assert sha(EVALUATOR) == EXPECTED_EVAL
    assert sha(TAXONOMY) == EXPECTED_TAX
    assert sha(HEALER_RUNNER) == EXPECTED_RUNNER
    assert sha(PROTOCOL) == EXPECTED_PROTO
    # Same decide_healer_eligibility symbol used by Qwen4B ledger path.
    text = EVALUATOR.read_text(encoding="utf-8")
    assert "def decide_healer_eligibility" in text
    assert QWEN4B_ELIG.exists()


def test_runner_is_eligibility_only_no_healer_execution():
    text = RUNNER.read_text(encoding="utf-8")
    assert "decide_healer_eligibility" in text
    assert "healer_execution" in text
    assert "MathHealer" + "Runner" not in text
    assert "call_gemini" not in text
    assert "call_qwen" not in text
    assert "--execute" in text


def test_fail_set_and_ledger_completeness():
    baseline = _load_jsonl(BASELINE)
    fails = [r for r in baseline if r["final_status"] != "PASSED"]
    assert len(fails) == 219
    ledger = _load_jsonl(OUT / "eligibility_ledger.jsonl")
    assert len(ledger) == 219
    assert len({r["cell_id"] for r in ledger}) == 219
    assert {r["cell_id"] for r in ledger} == {r["cell_id"] for r in fails}
    assert all(r["baseline_final_status"] == "FAILED" for r in ledger)
    assert all(r["eligibility_disposition"] in ALLOWED for r in ledger)
    assert all(r["healer_execution"] is False for r in ledger)
    assert all(r["rescued"] == "not_run" for r in ledger)
    assert all(r["regression"] == "not_run" for r in ledger)
    assert all(r["llm_calls"] == 0 for r in ledger)


def test_summary_and_audit():
    summary = json.loads((OUT / "eligibility_summary.json").read_text(encoding="utf-8"))
    audit = json.loads((OUT / "eligibility_completeness_audit.json").read_text(encoding="utf-8"))
    man = json.loads((OUT / "eligibility_manifest.json").read_text(encoding="utf-8"))
    assert summary["records"] == 219
    assert summary["baseline_fail"] == 219
    assert summary["corpus_sha_closure"] == EXPECTED_CLOSURE
    assert summary["evaluator_hash"] == EXPECTED_EVAL
    assert summary["healer_runner_sha256"] == EXPECTED_RUNNER
    assert summary["healer_protocol_sha256"] == EXPECTED_PROTO
    assert summary["healer_execution"] is False
    assert summary["eligible"] + summary["noneligible_no_rule_triggered"] + summary[
        "abstain_no_extractable_source"
    ] + summary["abstain_ambiguous_entry_point"] + summary["pending_review"] == 219
    assert audit["passed"] is True
    assert audit["duplicate"] == []
    assert audit["missing"] == []
    assert audit["unprocessed"] == []
    assert audit["raw_sha_mismatch"] == []
    assert audit["math_healer_runner_run_calls"] == 0
    assert man["eligibility_only"] is True
    assert man["noneligible_direct_run"] is False
    assert man["external_eligibility_prefilter"] is True


def test_artifacts_exist():
    for name in (
        "eligibility_ledger.jsonl",
        "eligible_cells.jsonl",
        "noneligible_and_abstain_cells.jsonl",
        "abstain_cells.jsonl",
        "eligibility_summary.json",
        "condition_summary.json",
        "family_summary.json",
        "task_summary.json",
        "layer_summary.json",
        "rule_hit_distribution.json",
        "eligibility_completeness_audit.json",
        "eligibility_manifest.json",
        "report.md",
    ):
        assert (OUT / name).exists()
