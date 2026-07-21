# -*- coding: utf-8 -*-
"""Closeout tests for Qwen4B post-hoc corrected-chain Healer replay."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRIMARY = ROOT / "docs/experiments/results/math16_pilot02_qwen4b_healer_v4_r001"
OUT = (
    ROOT
    / "docs/experiments/results/math16_pilot02_qwen4b_healer_v4_posthoc_corrected_chain_r001"
)
SCRIPT = (
    ROOT
    / "scripts/evaluate_math16_pilot02_qwen4b_healer_v4_posthoc_corrected_chain.py"
)
HEALER_RUNNER = ROOT / "agent_tools/finals_rebuild/ce115_research_healer_runner.py"
PROTOCOL = ROOT / "agent_tools/finals_rebuild/ce115_research_healer_protocol.py"

EXPECTED_RUNNER = "38453d1294382f061efe149484f5a3059a47d085d2aeef358874a954e37adebf"
EXPECTED_PROTO = "bdb4121ee266f91bfa116019a334cf4a528da0d71629b96540a5f763826aff39"
CELL_A = "qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d__seed_2026071301"
CELL_B = "qwen3_5_4b__ce112_q09_divisor_multiple_intersection__ab2d__seed_2026072001"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_jsonl(path: Path) -> list[dict]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def test_primary_ledger_preserved():
    overall = json.loads((PRIMARY / "overall_summary.json").read_text(encoding="utf-8"))
    assert overall["baseline_pass_fraction"] == "78/320"
    assert overall["post_healer_pass_fraction"] == "83/320"
    assert overall["counts"]["rescued"] == 5
    assert overall["counts"]["no_op"] == 2
    assert overall["counts"]["fail_eligible"] == 10
    assert overall["counts"]["fail_noneligible"] == 232


def test_pins_and_nature():
    assert sha(HEALER_RUNNER) == EXPECTED_RUNNER
    assert sha(PROTOCOL) == EXPECTED_PROTO
    man = json.loads((OUT / "execution_manifest.json").read_text(encoding="utf-8"))
    assert man["healer_runner_sha256"] == EXPECTED_RUNNER
    assert man["healer_protocol_sha256"] == EXPECTED_PROTO
    assert man["preregistered_primary"] is False
    assert man["chain_kind"] == "posthoc_corrected_chain"
    assert man["primary_result_preserved"] is True
    assert man["primary_post_healer_pass_fraction"] == "83/320"
    assert man["replayed"] == 10
    assert man["noneligible_executed"] == 0
    assert man["baseline_pass_executed"] == 0
    assert man["llm_calls"] == 0
    assert man["qwen9b"] is False


def test_completeness_audit():
    audit = json.loads((OUT / "completeness_audit.json").read_text(encoding="utf-8"))
    assert audit["passed"] is True
    assert audit["replayed"] == 10
    assert audit["duplicate"] == []
    assert audit["missing"] == []
    assert audit["noneligible_executed"] == []
    assert audit["baseline_pass_executed"] == []
    assert audit["unauthorized_rule"] == []
    assert audit["evaluator_crash"] == []
    assert audit["protocol_error"] == []
    assert audit["raw_sha_mismatch"] == []
    assert audit["model_calls"] == 0
    assert audit["primary_overwritten"] is False


def test_corrected_chain_overall():
    overall = json.loads((OUT / "overall_summary.json").read_text(encoding="utf-8"))
    assert overall["baseline_pass_fraction"] == "78/320"
    assert overall["post_healer_pass_fraction"] == "84/320"
    assert overall["counts"]["rescued"] == 6
    assert overall["counts"]["repaired_still_fail"] == 4
    assert overall["counts"]["no_op"] == 0
    assert overall["counts"]["regression"] == 0
    assert overall["counts"]["healer_ran"] == 10
    assert overall["preregistered_primary"] is False
    assert overall["primary_post_healer_pass_fraction"] == "83/320"


def test_replay_records_and_focus_cells():
    rows = _load_jsonl(OUT / "eligible_replay_records.jsonl")
    assert len(rows) == 10
    assert len({r["cell_id"] for r in rows}) == 10
    by_id = {r["cell_id"]: r for r in rows}

    a = by_id[CELL_A]
    assert a["primary_disposition"] == "no_op"
    assert a["noop_to_rescue"] is True
    assert a["rescued"] is True
    assert a["post_healer_status"] == "PASSED"
    assert a["applied_rules"] == ["L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP"]

    b = by_id[CELL_B]
    assert b["post_healer_status"] == "FAILED"
    assert b["rescued"] is False
    assert b["repaired_still_fail"] is True
    assert b["applied_rules"] == ["L2_CORRECT_ANSWER_JSON_DUMPS_UNWRAP"]

    same = [r for r in rows if r["same_as_primary"]]
    changed = [r for r in rows if not r["same_as_primary"]]
    assert len(same) == 8
    assert {r["cell_id"] for r in changed} == {CELL_A, CELL_B}


def test_script_does_not_target_primary_outdir():
    text = SCRIPT.read_text(encoding="utf-8")
    assert "healer_v4_posthoc_corrected_chain_r001" in text
    assert "PRIMARY_DIR" in text
    assert "preregistered_primary" in text
    assert "call_gemini" not in text
    assert "qwen3.5:9b" not in text
