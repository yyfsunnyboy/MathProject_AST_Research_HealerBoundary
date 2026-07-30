# -*- coding: utf-8 -*-
"""Focused checks for Qwen4B Aggressive 320-cell safety benchmark protocol v1.

Protocol freeze only: validates sealed Round 1 locks, frozen protocol fields,
and pure transition / rate helpers. Does not execute the 320-cell benchmark.
"""
from __future__ import annotations

import json
from pathlib import Path

from agent_tools.finals_rebuild.math16_qwen4b_aggressive_320_safety_benchmark_v1 import (
    EXPECTED_FAIL,
    EXPECTED_PASS,
    EXPECTED_TOTAL,
    PROTOCOL_ID,
    TRANSITION_ENUM,
    classify_transition,
    compute_rates,
)

ROOT = Path(__file__).resolve().parents[2]
PROTOCOL_DOC = (
    ROOT
    / "docs/experiments/design/math16_qwen4b_aggressive_320_safety_benchmark_protocol_v1.md"
)
PROTOCOL_MANIFEST = (
    ROOT
    / "docs/experiments/manifests/math16_qwen4b_aggressive_320_safety_benchmark_protocol_v1.json"
)
ROUND1_SUMMARY = (
    ROOT / "docs/experiments/manifests/math16_three_model_round1_summary_v1.json"
)
C5A_CLOSURE = (
    ROOT / "docs/experiments/manifests/math16_c5a_final_source_closure_v1.json"
)


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_protocol_files_exist_and_status_frozen_not_executed():
    assert PROTOCOL_DOC.is_file()
    assert PROTOCOL_MANIFEST.is_file()
    text = PROTOCOL_DOC.read_text(encoding="utf-8")
    assert "FROZEN_PROTOCOL_NOT_EXECUTED" in text
    assert "Aggressive Healer full 320-cell safety benchmark" in text
    assert "不是**三模型 Round 2" in text or "not Round 2" in text.lower() or "Relation to Round 2" in text
    assert "fixpoint" in text and "Method 2" in text
    m = _load(PROTOCOL_MANIFEST)
    assert m["protocol_status"] == "FROZEN_PROTOCOL_NOT_EXECUTED"
    assert m["manifest_id"] == PROTOCOL_ID
    assert m["this_round"]["formal_benchmark_execution"] is False
    assert m["this_round"]["model_calls"] is False
    assert m["population"]["active_n"] == 320
    assert m["execution_model"]["iterative_fixpoint"] is False


def test_round1_population_locks_in_authorities():
    summary = _load(ROUND1_SUMMARY)
    c5a = _load(C5A_CLOSURE)
    q4 = summary["models"]["qwen4b"]
    assert q4["final_pass"] == EXPECTED_PASS == 88
    assert q4["final_fail"] == EXPECTED_FAIL == 232
    assert q4["final_pass"] + q4["final_fail"] == EXPECTED_TOTAL
    val = c5a["validation"]
    assert val["pass_n"] == 88 and val["fail_n"] == 232 and val["n_cells"] == 320


def test_transition_classification_five_ways():
    assert classify_transition(
        input_status="PASS", output_status="PASS", source_changed=False
    ) == "preserved_pass"
    assert classify_transition(
        input_status="PASS", output_status="FAIL", source_changed=True
    ) == "regression"
    assert classify_transition(
        input_status="FAIL", output_status="PASS", source_changed=True
    ) == "verified_rescue"
    assert classify_transition(
        input_status="FAIL", output_status="FAIL", source_changed=False
    ) == "unchanged_fail"
    assert classify_transition(
        input_status="FAIL", output_status="FAIL", source_changed=True
    ) == "modified_still_failed"
    assert set(TRANSITION_ENUM) == {
        "preserved_pass",
        "regression",
        "verified_rescue",
        "unchanged_fail",
        "modified_still_failed",
    }


def test_rate_formulas_use_locked_denominators():
    rates = compute_rates(
        verified_rescue_n=10,
        regression_n=2,
        preserved_pass_n=86,
        modified_n=40,
    )
    assert rates["rescue_rate"] == 10 / 232
    assert rates["regression_rate"] == 2 / 88
    assert rates["preservation_rate"] == 86 / 88
    assert rates["modification_rate"] == 40 / 320
    assert rates["net_pass_change"] == 8.0


def test_protocol_blinding_and_not_mixed_with_siblings():
    m = _load(PROTOCOL_MANIFEST)
    assert m["blinding"]["input_status_must_not_gate_eligibility_or_mutation"] is True
    assert m["blinding"]["evaluator_must_not_accept_or_rollback_source"] is True
    assert m["positioning"]["not_method2"] is True
    assert m["positioning"]["not_fixpoint"] is True
    assert m["positioning"]["not_round2"] is True
    assert m["fixed_sequence"] == "A→B→C1→C2→D3→D1→D5→D2"
