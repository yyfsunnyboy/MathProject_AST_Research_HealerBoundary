# -*- coding: utf-8 -*-
"""Focused checks for Qwen4B cell-wise deterministic fixpoint replay protocol v1.

Protocol freeze only: validates sealed Round 1 closures, frozen protocol fields,
and pure termination / SHA-history judgment helpers. Does not execute replay or
call models.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
PROTOCOL_DOC = (
    ROOT
    / "docs/experiments/design/math16_qwen4b_cellwise_fixpoint_replay_protocol_v1.md"
)
PROTOCOL_MANIFEST = (
    ROOT
    / "docs/experiments/manifests/math16_qwen4b_cellwise_fixpoint_replay_protocol_v1.json"
)
ROUND1_SUMMARY = (
    ROOT / "docs/experiments/manifests/math16_three_model_round1_summary_v1.json"
)
C5A_CLOSURE = (
    ROOT / "docs/experiments/manifests/math16_c5a_final_source_closure_v1.json"
)

MAX_ROUND = 8
TERMINATION_ORDER = [
    "ITERATIVE_RESCUE",
    "ZERO_CHANGE_CONVERGENCE",
    "CYCLE_DETECTED",
    "MAX_ROUND_NON_CONVERGENT",
    "CONTINUE_SAME_CELL_ONLY",
]
LAYER_ORDER = [
    "tier_a",
    "tier_b",
    "tier_c1",
    "tier_c2",
    "tier_d3",
    "tier_d1",
    "tier_d5",
    "tier_d2",
]
REQUIRED_JOURNAL_FIELDS = [
    "cell_id",
    "cycle_index",
    "round_start_sha",
    "per_rule_pre_sha",
    "per_rule_post_sha",
    "rule_id",
    "eligible",
    "modified",
    "abstained",
    "round_end_sha",
    "source_changed",
    "full_sha_history",
    "newly_eligible",
    "enabling_prior_rule",
    "iterative_partial_repair",
    "rescue_cycle",
    "rescue_rule_id",
    "convergence_cycle_count",
    "termination_reason",
    "regression",
    "cycle_detected",
    "max_round_reached",
]


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def attribute_rescue_rule_id(rule_trace: list[dict[str, Any]]) -> str | None:
    """Last rule in-cycle that modified source; used when final eval is PASS."""
    last: str | None = None
    for step in rule_trace:
        pre = step["pre_sha"]
        post = step["post_sha"]
        if step.get("modified") and post != pre:
            last = step["rule_id"]
    return last


def judge_after_cycle(
    *,
    final_status: str,
    round_start_sha: str,
    round_end_sha: str,
    full_sha_history: list[str],
    cycle_index: int,
    max_round: int = MAX_ROUND,
    rule_trace: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Apply frozen termination order after one complete cell-wise cycle.

    Returns a decision dict. When CONTINUE, may include an updated
    ``full_sha_history`` with ``round_end_sha`` appended.
    """
    if not full_sha_history:
        raise ValueError("full_sha_history must start from Round 1 final SHA")
    if full_sha_history[0] is None:
        raise ValueError("SHA history origin missing")

    source_changed = round_end_sha != round_start_sha
    history = list(full_sha_history)

    if final_status == "PASS":
        return {
            "termination_reason": "ITERATIVE_RESCUE",
            "rescue_cycle": cycle_index,
            "rescue_rule_id": attribute_rescue_rule_id(rule_trace or []),
            "source_changed": source_changed,
            "cycle_detected": False,
            "max_round_reached": False,
            "convergence_cycle_count": cycle_index,
            "full_sha_history": history,
            "continue": False,
        }

    if final_status != "FAIL":
        raise ValueError(f"unsupported final_status: {final_status}")

    if not source_changed:
        return {
            "termination_reason": "ZERO_CHANGE_CONVERGENCE",
            "rescue_cycle": None,
            "rescue_rule_id": None,
            "source_changed": False,
            "cycle_detected": False,
            "max_round_reached": False,
            "convergence_cycle_count": cycle_index,
            "full_sha_history": history,
            "continue": False,
        }

    if round_end_sha in history:
        return {
            "termination_reason": "CYCLE_DETECTED",
            "rescue_cycle": None,
            "rescue_rule_id": None,
            "source_changed": True,
            "cycle_detected": True,
            "max_round_reached": False,
            "convergence_cycle_count": cycle_index,
            "full_sha_history": history,
            "continue": False,
        }

    history.append(round_end_sha)

    if cycle_index >= max_round:
        return {
            "termination_reason": "MAX_ROUND_NON_CONVERGENT",
            "rescue_cycle": None,
            "rescue_rule_id": None,
            "source_changed": True,
            "cycle_detected": False,
            "max_round_reached": True,
            "convergence_cycle_count": cycle_index,
            "full_sha_history": history,
            "continue": False,
        }

    return {
        "termination_reason": None,
        "rescue_cycle": None,
        "rescue_rule_id": None,
        "source_changed": True,
        "cycle_detected": False,
        "max_round_reached": False,
        "convergence_cycle_count": cycle_index,
        "full_sha_history": history,
        "continue": True,
        "advance_policy": "SAME_CELL_ONLY",
    }


def test_protocol_files_exist_and_json_parses():
    assert PROTOCOL_DOC.is_file()
    manifest = _load(PROTOCOL_MANIFEST)
    assert manifest["manifest_id"] == (
        "math16_qwen4b_cellwise_fixpoint_replay_protocol_v1"
    )
    assert manifest["protocol_status"] == "FROZEN_PROTOCOL_NOT_EXECUTED"
    assert manifest["this_round"]["formal_fixpoint_replay"] is False
    assert manifest["this_round"]["model_calls"] is False


def test_232_residual_fail_and_88_pass_exclusion_closure():
    manifest = _load(PROTOCOL_MANIFEST)
    summary = _load(ROUND1_SUMMARY)
    c5a = _load(C5A_CLOSURE)

    q4 = summary["models"]["qwen4b"]
    assert q4["final_pass"] == 88
    assert q4["final_fail"] == 232
    assert q4["final_pass"] + q4["final_fail"] == 320

    assert c5a["validation"]["pass_n"] == 88
    assert c5a["validation"]["fail_n"] == 232
    assert c5a["validation"]["n_cells"] == 320

    assert manifest["population"]["round1_final_pass_n"] == 88
    assert manifest["population"]["round1_final_fail_n"] == 232
    assert manifest["population"]["fixpoint_active_n"] == 232
    assert manifest["population"]["permanently_excluded_pass_n"] == 88
    assert manifest["population"]["pass_exclusion_policy"] == "NEVER_SCAN_NEVER_MODIFY"

    fail_ids = {
        c["cell_id"] for c in c5a["cells"] if c.get("c5a_outcome") == "FAIL"
    }
    pass_ids = {
        c["cell_id"] for c in c5a["cells"] if c.get("c5a_outcome") == "PASS"
    }
    assert len(fail_ids) == 232
    assert len(pass_ids) == 88
    assert fail_ids.isdisjoint(pass_ids)


def test_max_round_layer_order_and_judgment_order_frozen():
    manifest = _load(PROTOCOL_MANIFEST)
    assert manifest["execution_model"]["max_round"] == MAX_ROUND
    assert manifest["fixed_sequence"] == "A→B→C1→C2→D3→D1→D5→D2"
    assert manifest["layer_order"] == LAYER_ORDER
    assert manifest["termination"]["judgment_order"] == TERMINATION_ORDER
    assert manifest["execution_model"]["batch_resync_forbidden"] is True
    assert manifest["execution_model"]["unit"] == "cell_wise"
    text = PROTOCOL_DOC.read_text(encoding="utf-8")
    assert "A → B → C1 → C2 → D3 → D1 → D5 → D2" in text
    assert "max_round = 8" in text


def test_sha_history_origin_and_journal_fields():
    manifest = _load(PROTOCOL_MANIFEST)
    assert manifest["sha_history"]["origin"] == "Round 1 final source SHA"
    assert manifest["sha_history"]["cycle_detection_before_append"] is True
    assert manifest["sha_history"]["zero_change_is_not_cycle_detected"] is True
    assert set(manifest["journal"]["required_fields"]) == set(REQUIRED_JOURNAL_FIELDS)
    assert (
        manifest["rescue_attribution"]["rescue_rule_id"]
        == (
            "last rule in the rescue cycle that modified source "
            "(post_sha != pre_sha) and after which final evaluation is PASS"
        )
    )


def test_termination_iterative_rescue_and_attribution():
    trace = [
        {
            "rule_id": "TIER_A_EMPTY_SUITE_INSERT_PASS_V1",
            "modified": True,
            "pre_sha": "aaa",
            "post_sha": "bbb",
        },
        {
            "rule_id": "TIER_D_OPS_SHADOW_REMOVAL_V1",
            "modified": True,
            "pre_sha": "bbb",
            "post_sha": "ccc",
        },
        {
            "rule_id": "TIER_D_DUPLICATE_DEFINITION_SELECTION_V1",
            "modified": False,
            "pre_sha": "ccc",
            "post_sha": "ccc",
        },
    ]
    decision = judge_after_cycle(
        final_status="PASS",
        round_start_sha="aaa",
        round_end_sha="ccc",
        full_sha_history=["r1_final"],
        cycle_index=2,
        rule_trace=trace,
    )
    assert decision["termination_reason"] == "ITERATIVE_RESCUE"
    assert decision["rescue_cycle"] == 2
    assert decision["rescue_rule_id"] == "TIER_D_OPS_SHADOW_REMOVAL_V1"
    assert decision["continue"] is False
    assert decision["cycle_detected"] is False


def test_termination_zero_change_convergence():
    decision = judge_after_cycle(
        final_status="FAIL",
        round_start_sha="sha_same",
        round_end_sha="sha_same",
        full_sha_history=["r1_final", "sha_same"],
        cycle_index=3,
    )
    assert decision["termination_reason"] == "ZERO_CHANGE_CONVERGENCE"
    assert decision["source_changed"] is False
    assert decision["cycle_detected"] is False
    assert decision["continue"] is False
    assert decision["full_sha_history"] == ["r1_final", "sha_same"]


def test_termination_cycle_detected_before_append():
    history = ["r1_final", "sha_a", "sha_b"]
    decision = judge_after_cycle(
        final_status="FAIL",
        round_start_sha="sha_b",
        round_end_sha="sha_a",  # revisit earlier SHA
        full_sha_history=history,
        cycle_index=4,
    )
    assert decision["termination_reason"] == "CYCLE_DETECTED"
    assert decision["cycle_detected"] is True
    assert decision["continue"] is False
    # Must not append duplicate on detection.
    assert decision["full_sha_history"] == history


def test_termination_max_round_non_convergent():
    decision = judge_after_cycle(
        final_status="FAIL",
        round_start_sha="sha_7",
        round_end_sha="sha_8",
        full_sha_history=["r1_final", "sha_1", "sha_7"],
        cycle_index=8,
        max_round=8,
    )
    assert decision["termination_reason"] == "MAX_ROUND_NON_CONVERGENT"
    assert decision["max_round_reached"] is True
    assert decision["continue"] is False
    assert decision["full_sha_history"][-1] == "sha_8"
    assert "sha_8" in decision["full_sha_history"]


def test_continue_appends_sha_and_same_cell_only():
    decision = judge_after_cycle(
        final_status="FAIL",
        round_start_sha="sha_1",
        round_end_sha="sha_2",
        full_sha_history=["r1_final", "sha_1"],
        cycle_index=1,
        max_round=8,
    )
    assert decision["termination_reason"] is None
    assert decision["continue"] is True
    assert decision["advance_policy"] == "SAME_CELL_ONLY"
    assert decision["full_sha_history"] == ["r1_final", "sha_1", "sha_2"]


def test_judgment_priority_pass_beats_zero_change_and_cycle():
    # If PASS, even with unchanged SHA, terminate as rescue (observational PASS).
    decision = judge_after_cycle(
        final_status="PASS",
        round_start_sha="same",
        round_end_sha="same",
        full_sha_history=["r1_final", "same"],
        cycle_index=1,
        rule_trace=[],
    )
    assert decision["termination_reason"] == "ITERATIVE_RESCUE"


def test_no_cross_model_or_round1_overwrite_declarations():
    manifest = _load(PROTOCOL_MANIFEST)
    assert set(manifest["positioning"]["cross_model_fixpoint_forbidden"]) == {
        "qwen9b",
        "gemini",
        "qwen2b",
    }
    decls = set(manifest["declarations"])
    assert "no_round1_overwrite" in decls
    assert "4b_only" in decls
    assert "no_fixpoint_replay_executed" in decls
    assert "pass_88_never_scanned" in decls
    assert "residual_fail_232_only" in decls
    assert manifest["this_round"]["round1_artifacts_modified"] is False
    assert manifest["this_round"]["frozen_rules_modified"] is False
