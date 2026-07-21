# -*- coding: utf-8 -*-
"""Math16 Healer revalidation: fix false loop rollback; preserve true-loop guards."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from agent_tools.finals_rebuild.ce115_research_healer_runner import (
    MathHealerRunner,
    RULE_ALLOWLIST,
    _is_math16_task,
    _is_phase_b_evaluator_loop,
    _maybe_reevaluate,
    _rule_would_change,
)
from agent_tools.finals_rebuild.ce115_research_healer_runner import RULE_REGISTRY
from agent_tools.finals_rebuild.math16_pool import frozen_for_prompt, tasks_by_id
from scripts.run_math16_latex_v1_gemini_live import classify_math16_response

ROOT = Path(__file__).resolve().parents[2]
PLAN = ROOT / "docs/experiments/manifests/math16_pilot02_qwen4b_cell_plan.json"
PRIMARY = (
    ROOT
    / "docs/experiments/results/math16_pilot02_qwen4b_healer_v4_r001/overall_summary.json"
)

CELL_A = "qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d__seed_2026071301"
CELL_B = "qwen3_5_4b__ce112_q09_divisor_multiple_intersection__ab2d__seed_2026072001"


def _plan() -> dict[str, dict]:
    return {c["cell_id"]: c for c in json.loads(PLAN.read_text(encoding="utf-8"))}


def _load_source(cell_id: str) -> tuple[str, dict, dict]:
    cell = _plan()[cell_id]
    raw = (
        ROOT
        / "docs/experiments/results"
        / cell["output_relative_path"]
        / "raw_response.txt"
    ).read_text(encoding="utf-8")
    task = tasks_by_id()[cell["task_id"]]
    frozen = frozen_for_prompt(task)["oracle_payload"]
    outcome, source, _details = classify_math16_response(
        raw,
        frozen_params=frozen,
        audit_oracle_payload=task["oracle_payload"],
        task=task,
    )
    assert source
    assert outcome != "passed"
    return source, task, frozen


def test_primary_qwen4b_ledger_untouched():
    overall = json.loads(PRIMARY.read_text(encoding="utf-8"))
    assert overall["baseline_pass_fraction"] == "78/320"
    assert overall["post_healer_pass_fraction"] == "83/320"
    assert overall["counts"]["rescued"] == 5
    assert overall["counts"]["no_op"] == 2


def test_math16_task_routing_helper():
    task = tasks_by_id()["ce115_calc_radical_simplification_l1"]
    assert _is_math16_task(task) is True
    assert _is_math16_task({"oracle_type": "radical_simplification"}) is False


def test_cell_a_radical_wrap_retained_and_math16_pass():
    source, task, frozen = _load_source(CELL_A)
    ctx = {"task": task, "frozen": frozen}
    re = _maybe_reevaluate(source, ctx)
    assert re["evaluator_rerun"] is True
    assert re["evaluator_backend"] == "classify_math16_response"
    assert re["evaluator_outcome"] == "schema_failure"

    result = MathHealerRunner(max_passes=3).run(source, context=ctx)
    assert result.real_model_calls == 0
    assert result.final_status == "changed"
    assert result.input_hash != result.output_hash
    assert not any(
        (p.stop_reason or "").startswith("fallback_loop_detected_")
        for p in result.provenance
    )
    changed = [p for p in result.provenance if p.changed]
    assert changed
    assert changed[0].selected_rule_id == "L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP"

    after_outcome, _, _ = classify_math16_response(
        result.output_source,
        frozen_params=frozen,
        audit_oracle_payload=task["oracle_payload"],
        task=task,
    )
    assert after_outcome == "passed"


def test_cell_b_q09_still_fail_not_rescue():
    source, task, frozen = _load_source(CELL_B)
    ctx = {"task": task, "frozen": frozen}
    result = MathHealerRunner(max_passes=3).run(source, context=ctx)
    assert result.real_model_calls == 0
    after_outcome, _, details = classify_math16_response(
        result.output_source,
        frozen_params=frozen,
        audit_oracle_payload=task["oracle_payload"],
        task=task,
    )
    assert after_outcome != "passed"
    # Must not be a formal rescue; NameError root cause remains in scope.
    text = result.output_source
    assert "safe_eval" in text or after_outcome == "runtime_failure"
    assert after_outcome == "runtime_failure"


def test_true_evaluator_loop_still_detected_with_churn():
    """Same outcome + same signature + rule would still change ⇒ loop."""
    source, task, frozen = _load_source(CELL_B)
    ctx = {"task": task, "frozen": frozen}
    rule = RULE_REGISTRY["L2_CORRECT_ANSWER_JSON_DUMPS_UNWRAP"]
    # Force a synthetic after_eval identical to before, but claim rule still churns
    # by using the *before* source as new_source for would_change (still triggered).
    before_eval = _maybe_reevaluate(source, ctx)
    assert before_eval["evaluator_rerun"] is True
    is_loop, reason = _is_phase_b_evaluator_loop(
        before_eval=before_eval,
        after_eval=dict(before_eval),
        rule=rule,
        new_source=source,  # unwrap still applicable on original → would_change True
        context=ctx,
    )
    assert is_loop is True
    assert reason.startswith("evaluator_loop_with_verdict_")
    assert _rule_would_change(source, rule, ctx) is True


def test_same_outcome_alone_not_loop_when_rule_exhausted():
    source, task, frozen = _load_source(CELL_B)
    ctx = {"task": task, "frozen": frozen}
    rule = RULE_REGISTRY["L2_CORRECT_ANSWER_JSON_DUMPS_UNWRAP"]
    new_source, _, _ = rule.apply(source, ctx)
    before_eval = _maybe_reevaluate(source, ctx)
    after_eval = _maybe_reevaluate(new_source, ctx)
    assert before_eval["evaluator_outcome"] == after_eval["evaluator_outcome"]
    is_loop, _reason = _is_phase_b_evaluator_loop(
        before_eval=before_eval,
        after_eval=after_eval,
        rule=rule,
        new_source=new_source,
        context=ctx,
    )
    assert is_loop is False
    assert _rule_would_change(new_source, rule, ctx) is False


def test_revalidator_error_fail_closed(monkeypatch):
    source, task, frozen = _load_source(CELL_A)
    ctx = {"task": task, "frozen": frozen, "reevaluator": "math16"}

    def _boom(*_a, **_k):
        raise RuntimeError("synthetic_revalidator_failure")

    monkeypatch.setattr(
        "scripts.run_math16_latex_v1_gemini_live.classify_math16_response",
        _boom,
    )
    err = _maybe_reevaluate(source, ctx)
    assert err.get("evaluator_error") is True
    assert err.get("evaluator_rerun") is False

    result = MathHealerRunner(max_passes=3).run(source, context=ctx)
    # Change must not be accepted when revalidator errors.
    assert result.input_hash == result.output_hash
    assert any(
        (p.stop_reason or "").startswith("fallback_loop_detected_revalidator_error_")
        for p in result.provenance
    )


def test_allowlist_and_max_passes_unchanged():
    assert RULE_ALLOWLIST == (
        "L1_CLOSE_UNBALANCED_PARENTHESIS",
        "L1_CLOSE_UNBALANCED_DELIMITER_EXTENDED",
        "L1_PROSE_RESIDUE_NARROW",
        "L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP",
        "L2_KWARGS_EMPTY_BAG_INLINE_UNIQUE_PARAM",
        "L2_CORRECT_ANSWER_JSON_DUMPS_UNWRAP",
    )
    assert MathHealerRunner(max_passes=3).max_passes == 3
