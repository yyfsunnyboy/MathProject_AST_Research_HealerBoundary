# -*- coding: utf-8 -*-
"""Protocol consistency: accept frozen producer fallback_loop_detected_* stop_reasons."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from agent_tools.finals_rebuild.ce115_research_healer_protocol import (
    ALLOWED_STOP_REASONS,
    FALLBACK_LOOP_STOP_REASON_PREFIX,
    PassProvenance,
    RuleOutcome,
    RuleProtocolError,
    is_allowed_stop_reason,
    sha256_text,
    validate_provenance,
    validate_rule_outcome,
)
from agent_tools.finals_rebuild.ce115_research_healer_runner import (
    RULE_ALLOWLIST,
    MathHealerRunner,
)
from agent_tools.finals_rebuild.math16_pool import frozen_for_prompt, tasks_by_id
from scripts.evaluate_math16_pilot02_full_v4 import (
    _load_family_and_api_policy,
    classify_outcome_to_v3,
    decide_healer_eligibility,
)
from scripts.run_math16_latex_v1_gemini_live import classify_math16_response

ROOT = Path(__file__).resolve().parents[2]
BLOCKER_CELL_ID = (
    "qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d__seed_2026071301"
)
PLAN_PATH = ROOT / "docs/experiments/manifests/math16_pilot02_qwen4b_cell_plan.json"
OLD_RUNNER_SHA = "b89e6059ce67efb622aa2e085e365b909d0d4f7df1a6814c1dc83df029ce81e1"
HEALER_RUNNER = ROOT / "agent_tools/finals_rebuild/ce115_research_healer_runner.py"


def _hash(path: Path) -> str:
    import hashlib

    return hashlib.sha256(path.read_bytes()).hexdigest()


def _dummy_hashes() -> tuple[str, str]:
    a = sha256_text("before")
    b = sha256_text("after")
    return a, b


def test_runner_sha_unchanged_by_protocol_only_fix():
    """Repair pack / runner bytes must not change in this protocol-consistency fix."""
    assert _hash(HEALER_RUNNER) == OLD_RUNNER_SHA


def test_allowlist_and_max_passes_unchanged():
    assert RULE_ALLOWLIST == (
        "L1_CLOSE_UNBALANCED_PARENTHESIS",
        "L1_CLOSE_UNBALANCED_DELIMITER_EXTENDED",
        "L1_PROSE_RESIDUE_NARROW",
        "L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP",
        "L2_KWARGS_EMPTY_BAG_INLINE_UNIQUE_PARAM",
        "L2_CORRECT_ANSWER_JSON_DUMPS_UNWRAP",
    )
    runner = MathHealerRunner(max_passes=3)
    assert runner.max_passes == 3
    assert runner.allowlist == RULE_ALLOWLIST


def test_existing_literal_stop_reasons_still_allowed():
    for reason in ALLOWED_STOP_REASONS:
        assert is_allowed_stop_reason(reason) is True


@pytest.mark.parametrize(
    "reason",
    [
        "fallback_loop_detected_evaluator_loop_with_verdict_runtime_failure",
        "fallback_loop_detected_compiler_loop_at_line_12",
        "fallback_loop_detected_evaluator_loop_with_verdict_schema_failure",
    ],
)
def test_fallback_loop_prefix_stop_reasons_allowed(reason: str):
    assert reason.startswith(FALLBACK_LOOP_STOP_REASON_PREFIX)
    assert is_allowed_stop_reason(reason) is True
    before, _ = _dummy_hashes()
    prov = PassProvenance(
        pass_index=0,
        chain_position=None,
        candidate_rules_checked=("L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP",),
        selected_rule_id=None,
        selection_priority=None,
        applicable=False,
        triggered=False,
        changed=False,
        guard_results={},
        before_hash=before,
        after_hash=before,
        validation={"loop_detected": True},
        stop_reason=reason,
        stopped_after_change=False,
        final_status="no_op",
    )
    validate_provenance(prov)


def test_unknown_stop_reason_still_rejected():
    before, _ = _dummy_hashes()
    with pytest.raises(RuleProtocolError, match="stop_reason"):
        validate_provenance(
            PassProvenance(
                pass_index=0,
                chain_position=None,
                candidate_rules_checked=(),
                selected_rule_id=None,
                selection_priority=None,
                applicable=False,
                triggered=False,
                changed=False,
                guard_results={},
                before_hash=before,
                after_hash=before,
                validation={},
                stop_reason="not_a_real_stop_reason",
                stopped_after_change=False,
                final_status="no_op",
            )
        )
    with pytest.raises(RuleProtocolError, match="stop_reason"):
        validate_rule_outcome(
            RuleOutcome(
                rule_id="L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP",
                layer="L2",
                priority=100,
                applicable=False,
                triggered=False,
                changed=False,
                guard_results={},
                reason="probe",
                before_hash=before,
                after_hash=before,
                validation={"repair_attempted": False},
                stop_reason="totally_unknown",
            )
        )


def test_blocker_cell_healer_run_no_rule_protocol_error():
    plan = {
        c["cell_id"]: c
        for c in json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    }
    cell = plan[BLOCKER_CELL_ID]
    raw = (
        ROOT
        / "docs/experiments/results"
        / cell["output_relative_path"]
        / "raw_response.txt"
    ).read_text(encoding="utf-8")
    tasks = tasks_by_id()
    _, api_map = _load_family_and_api_policy()
    task = tasks[cell["task_id"]]
    frozen = frozen_for_prompt(task)
    outcome, source, details = classify_math16_response(
        raw,
        frozen_params=frozen["oracle_payload"],
        audit_oracle_payload=task["oracle_payload"],
        task=task,
    )
    mapped = classify_outcome_to_v3(
        outcome, details, api_policy=api_map[cell["task_id"]]
    )
    assert mapped["final_status"] != "PASSED"
    elig = decide_healer_eligibility(
        baseline_passed=False,
        source=source,
        context={"task": task, "frozen": frozen["oracle_payload"]},
        mechanism_tags=list(mapped.get("mechanism_tags") or []),
        classification_status=str(mapped.get("classification_status") or "ADJUDICATED"),
    )
    assert elig["healer_eligible"] is True
    assert "L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP" in elig["probe_hits"]

    result = MathHealerRunner(max_passes=3).run(
        source, context={"task": task, "frozen": frozen["oracle_payload"]}
    )
    assert result.real_model_calls == 0
    assert any(
        (p.stop_reason or "").startswith(FALLBACK_LOOP_STOP_REASON_PREFIX)
        or p.stop_reason in ALLOWED_STOP_REASONS
        for p in result.provenance
    )
    # Eligibility contract unchanged: still allowlist-only probe.
    assert set(elig["probe_hits"]).issubset(set(RULE_ALLOWLIST))
