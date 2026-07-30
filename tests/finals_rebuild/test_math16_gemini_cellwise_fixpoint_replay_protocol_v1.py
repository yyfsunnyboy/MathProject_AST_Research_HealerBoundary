# -*- coding: utf-8 -*-
"""Focused checks for Gemini cell-wise fixpoint replay protocol v1.

Protocol freeze only: validates sealed C5c locks, frozen protocol fields, and
reuse of 4B termination judgment. Does not execute replay or call models.
"""
from __future__ import annotations

import json
from pathlib import Path

from agent_tools.finals_rebuild.math16_observational_evaluator_v1 import (
    AUTHORITATIVE_BINDING,
)
from agent_tools.finals_rebuild.math16_qwen4b_cellwise_fixpoint_replay_v1 import (
    judge_after_cycle as judge_4b,
)
from agent_tools.finals_rebuild.math16_gemini_cellwise_fixpoint_replay_v1 import (
    EXPECTED_FAIL,
    EXPECTED_PASS,
    EXPECTED_TOTAL,
    PROTOCOL_ID,
    judge_after_cycle,
    sha256_text,
)

ROOT = Path(__file__).resolve().parents[2]
PROTOCOL_DOC = (
    ROOT
    / "docs/experiments/design/math16_gemini_cellwise_fixpoint_replay_protocol_v1.md"
)
PROTOCOL_MANIFEST = (
    ROOT
    / "docs/experiments/manifests/math16_gemini_cellwise_fixpoint_replay_protocol_v1.json"
)
ROUND1_SUMMARY = (
    ROOT / "docs/experiments/manifests/math16_three_model_round1_summary_v1.json"
)
C5C_CLOSURE = (
    ROOT
    / "docs/experiments/manifests/math16_c5c_final_source_closure_gemini_fail_gated_authoritative_v1.json"
)


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_protocol_files_exist_and_status_frozen_not_executed():
    assert PROTOCOL_DOC.is_file()
    assert PROTOCOL_MANIFEST.is_file()
    text = PROTOCOL_DOC.read_text(encoding="utf-8")
    assert "FROZEN_PROTOCOL_NOT_EXECUTED" in text
    assert "gemini" in text.lower() or "Gemini" in text
    assert "31" in text and "289" in text
    m = _load(PROTOCOL_MANIFEST)
    assert m["protocol_status"] == "FROZEN_PROTOCOL_NOT_EXECUTED"
    assert m["manifest_id"] == PROTOCOL_ID
    assert m["this_round"]["formal_fixpoint_replay"] is False
    assert m["this_round"]["model_calls"] is False
    assert m["population"]["fixpoint_active_n"] == 31
    assert m["population"]["permanently_excluded_pass_n"] == 289
    assert m["population"]["round1_final_pass_n"] != 88
    assert m["population"]["round1_final_fail_n"] != 232
    assert m["population"]["round1_final_pass_n"] != 102
    assert m["population"]["round1_final_fail_n"] != 218
    assert m["observational_evaluator"]["binding_id"] == AUTHORITATIVE_BINDING["binding_id"]


def test_round1_population_locks_in_authorities():
    summary = _load(ROUND1_SUMMARY)
    c5c = _load(C5C_CLOSURE)
    gm = summary["models"]["gemini"]
    assert gm["final_pass"] == EXPECTED_PASS == 289
    assert gm["final_fail"] == EXPECTED_FAIL == 31
    assert gm["final_pass"] + gm["final_fail"] == EXPECTED_TOTAL
    val = c5c["validation"]
    assert val["c5c_pass"] == 289 and val["c5c_fail"] == 31 and val["n_cells"] == 320
    assert c5c["namespace"] == "gemini_fail_gated_authoritative_v1"


def test_termination_judgment_matches_4b_reuse():
    r1 = sha256_text("r1")
    kwargs = dict(
        round_start_sha=sha256_text("same"),
        round_end_sha=sha256_text("same"),
        full_sha_history=[r1, sha256_text("same")],
        cycle_index=1,
    )
    a = judge_after_cycle(final_status="FAIL", **kwargs)
    b = judge_4b(final_status="FAIL", **kwargs)
    assert a["termination_reason"] == b["termination_reason"] == "ZERO_CHANGE_CONVERGENCE"

    rescue_a = judge_after_cycle(
        final_status="PASS",
        round_start_sha=sha256_text("a"),
        round_end_sha=sha256_text("b"),
        full_sha_history=[r1],
        cycle_index=2,
        rule_trace=[{"pre_sha": "x", "post_sha": "y", "modified": True, "rule_id": "R"}],
    )
    rescue_b = judge_4b(
        final_status="PASS",
        round_start_sha=sha256_text("a"),
        round_end_sha=sha256_text("b"),
        full_sha_history=[r1],
        cycle_index=2,
        rule_trace=[{"pre_sha": "x", "post_sha": "y", "modified": True, "rule_id": "R"}],
    )
    assert rescue_a["termination_reason"] == rescue_b["termination_reason"] == "ITERATIVE_RESCUE"
    assert rescue_a["rescue_rule_id"] == rescue_b["rescue_rule_id"] == "R"
