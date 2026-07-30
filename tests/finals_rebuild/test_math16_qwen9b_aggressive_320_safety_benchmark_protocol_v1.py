# -*- coding: utf-8 -*-
"""Focused checks for Qwen9B Aggressive 320-cell safety benchmark protocol v1.

Protocol freeze only: validates sealed C5c locks, frozen protocol fields, and
transition helpers. Does not execute the 320-cell benchmark.
"""
from __future__ import annotations

import json
from pathlib import Path

from agent_tools.finals_rebuild.math16_observational_evaluator_v1 import (
    AUTHORITATIVE_BINDING,
)
from agent_tools.finals_rebuild.math16_qwen9b_aggressive_320_safety_benchmark_v1 import (
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
    / "docs/experiments/design/math16_qwen9b_aggressive_320_safety_benchmark_protocol_v1.md"
)
PROTOCOL_MANIFEST = (
    ROOT
    / "docs/experiments/manifests/math16_qwen9b_aggressive_320_safety_benchmark_protocol_v1.json"
)
ROUND1_SUMMARY = (
    ROOT / "docs/experiments/manifests/math16_three_model_round1_summary_v1.json"
)
C5C_CLOSURE = (
    ROOT
    / "docs/experiments/manifests/math16_c5c_final_source_closure_qwen9b_fail_gated_authoritative_v1.json"
)


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_protocol_files_exist_and_status_frozen_not_executed():
    assert PROTOCOL_DOC.is_file()
    assert PROTOCOL_MANIFEST.is_file()
    text = PROTOCOL_DOC.read_text(encoding="utf-8")
    assert "FROZEN_PROTOCOL_NOT_EXECUTED" in text
    assert "320" in text and "102" in text and "218" in text
    m = _load(PROTOCOL_MANIFEST)
    assert m["protocol_status"] == "FROZEN_PROTOCOL_NOT_EXECUTED"
    assert m["manifest_id"] == PROTOCOL_ID
    assert m["this_round"]["formal_benchmark_execution"] is False
    assert m["this_round"]["model_calls"] is False
    assert m["population"]["active_n"] == 320
    assert m["population"]["input_pass_n"] == 102
    assert m["population"]["input_fail_n"] == 218
    assert m["population"]["input_pass_n"] != 88
    assert m["population"]["input_fail_n"] != 232
    assert m["execution_model"]["iterative_fixpoint"] is False
    assert m["observational_evaluator"]["binding_id"] == AUTHORITATIVE_BINDING["binding_id"]
    assert m["dual_accounting"]["must_not_rewrite_primary_journal"] is True


def test_round1_population_locks_in_authorities():
    summary = _load(ROUND1_SUMMARY)
    c5c = _load(C5C_CLOSURE)
    q9 = summary["models"]["qwen9b"]
    assert q9["final_pass"] == EXPECTED_PASS == 102
    assert q9["final_fail"] == EXPECTED_FAIL == 218
    assert q9["final_pass"] + q9["final_fail"] == EXPECTED_TOTAL
    val = c5c["validation"]
    assert val["c5c_pass"] == 102 and val["c5c_fail"] == 218 and val["n_cells"] == 320


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


def test_rates_use_102_218_denominators_not_4b():
    rates = compute_rates(
        verified_rescue_n=2,
        regression_n=1,
        preserved_pass_n=101,
        modified_n=4,
    )
    assert abs(rates["rescue_rate"] - 2 / 218) < 1e-12
    assert abs(rates["regression_rate"] - 1 / 102) < 1e-12
    assert abs(rates["preservation_rate"] - 101 / 102) < 1e-12
    assert abs(rates["modification_rate"] - 4 / 320) < 1e-12
    assert rates["net_pass_change"] == 1.0
