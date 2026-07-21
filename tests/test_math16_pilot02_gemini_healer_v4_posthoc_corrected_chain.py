# -*- coding: utf-8 -*-
"""Closeout tests for Gemini post-hoc corrected-chain Healer replay."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRIMARY = ROOT / "docs/experiments/results/math16_pilot02_full_evaluation_v4_r001"
OUT = (
    ROOT
    / "docs/experiments/results/math16_pilot02_gemini_healer_v4_posthoc_corrected_chain_r001"
)
SCRIPT = (
    ROOT
    / "scripts/evaluate_math16_pilot02_gemini_healer_v4_posthoc_corrected_chain.py"
)
HEALER_RUNNER = ROOT / "agent_tools/finals_rebuild/ce115_research_healer_runner.py"
PROTOCOL = ROOT / "agent_tools/finals_rebuild/ce115_research_healer_protocol.py"

EXPECTED_RUNNER = "38453d1294382f061efe149484f5a3059a47d085d2aeef358874a954e37adebf"
EXPECTED_PROTO = "bdb4121ee266f91bfa116019a334cf4a528da0d71629b96540a5f763826aff39"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_jsonl(path: Path) -> list[dict]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def test_primary_gemini_preserved():
    post = json.loads((PRIMARY / "post_healer_summary.json").read_text(encoding="utf-8"))
    assert post["baseline_pass_fraction"] == "289/320"
    assert post["final_pass_fraction"] == "289/320"
    assert post["rescued"] == 0
    assert post["eligible"] == 0
    assert post["abstained"] == 31
    base = _load_jsonl(PRIMARY / "cell_level_baseline.jsonl")
    assert len(base) == 320
    assert sum(1 for r in base if r["final_status"] == "PASSED") == 289
    assert sum(1 for r in base if r["final_status"] != "PASSED") == 31


def test_pins_and_nature():
    assert sha(HEALER_RUNNER) == EXPECTED_RUNNER
    assert sha(PROTOCOL) == EXPECTED_PROTO
    man = json.loads((OUT / "execution_manifest.json").read_text(encoding="utf-8"))
    assert man["healer_runner_sha256"] == EXPECTED_RUNNER
    assert man["healer_protocol_sha256"] == EXPECTED_PROTO
    assert man["preregistered_primary"] is False
    assert man["chain_kind"] == "posthoc_corrected_chain"
    assert man["primary_result_preserved"] is True
    assert man["baseline_fail"] == 31
    assert man["fail_eligible"] == 0
    assert man["fail_noneligible"] == 31
    assert man["healer_ran"] == 0
    assert man["noneligible_executed"] == 0
    assert man["baseline_pass_executed"] == 0
    assert man["llm_calls"] == 0
    assert man["qwen9b"] is False


def test_completeness_and_eligibility():
    audit = json.loads((OUT / "completeness_audit.json").read_text(encoding="utf-8"))
    assert audit["passed"] is True
    assert audit["baseline_fail"] == 31
    assert audit["eligibility_records"] == 31
    assert audit["duplicate"] == []
    assert audit["missing"] == []
    assert audit["unprocessed"] == []
    assert audit["noneligible_executed"] == []
    assert audit["baseline_pass_executed"] == []
    assert audit["unauthorized_rule"] == []
    assert audit["evaluator_crash"] == []
    assert audit["protocol_error"] == []
    assert audit["raw_sha_mismatch"] == []
    assert audit["model_calls"] == 0
    assert audit["primary_overwritten"] is False

    elig = _load_jsonl(OUT / "eligibility_inventory.jsonl")
    assert len(elig) == 31
    assert all(r["healer_eligible"] is False for r in elig)
    assert all(r["healer_eligibility"] == "noneligible" for r in elig)
    assert all(
        r["eligibility_reason"] == "No frozen allowlist rule triggered." for r in elig
    )
    assert _load_jsonl(OUT / "eligible_execution_records.jsonl") == []
    assert len(_load_jsonl(OUT / "abstain_records.jsonl")) == 31


def test_corrected_chain_overall_and_layers():
    overall = json.loads((OUT / "overall_summary.json").read_text(encoding="utf-8"))
    assert overall["baseline_pass_fraction"] == "289/320"
    assert overall["post_healer_pass_fraction"] == "289/320"
    assert overall["counts"]["rescued"] == 0
    assert overall["counts"]["fail_eligible"] == 0
    assert overall["counts"]["abstained"] == 31
    assert overall["counts"]["healer_ran"] == 0
    assert overall["fail_layer_distribution"] == {"L3": 17, "L5": 11, "L1": 3}
    assert overall["preregistered_primary"] is False
    assert overall["primary_post_healer_pass_fraction"] == "289/320"

    comp = json.loads(
        (
            OUT / "primary_vs_original_healer_vs_corrected_chain_comparison.json"
        ).read_text(encoding="utf-8")
    )
    assert comp["eligibility_still_zero"] is True
    assert comp["new_rescues_vs_primary"] == 0
    assert comp["false_loop_missed_rescue_cases"] == 0
    assert comp["special_answers"]["gemini_vs_qwen4b_healer_differential_holds"] is True


def test_script_isolation():
    text = SCRIPT.read_text(encoding="utf-8")
    assert "gemini_healer_v4_posthoc_corrected_chain_r001" in text
    assert "PRIMARY_DIR" in text
    assert "preregistered_primary" in text
    assert "call_gemini" not in text
    assert "qwen3.5:9b" not in text
