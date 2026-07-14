"""Milestone 1C — synthetic artifact / three-ledger validation (no model runs)."""
from __future__ import annotations

import copy
import json

import pytest

from agent_tools.finals_rebuild.generator_success import (
    EXPERIMENT_NOT_RUN,
    FAIL,
    GATE_STATUSES,
    GENERATOR_FAILURE,
    NOT_ASSESSED,
    NOT_OBSERVED,
    PASS,
    build_generator_artifact,
    build_healer_fields,
    derive_pipeline_corrected_record,
    derive_post_healer_record,
    read_success_fields,
    serialize_artifact,
    validate_gate_statuses,
)

CANDIDATE = "def generate(level=1, **kwargs):\n return {}\n"
FROZEN = {"a": 2, "b": 3}


def _passed_return(question: str, answer: int = 5) -> dict:
    return {
        "question_text": question,
        "correct_answer": answer,
        "oracle_payload": dict(FROZEN),
    }


def _assert_json_safe(record: dict) -> dict:
    text = serialize_artifact(record)
    restored = json.loads(text)
    assert isinstance(restored, dict)
    q = restored.get("actual_question_text")
    assert q is None or isinstance(q, str)
    gates = restored.get("evaluation_gates") or {}
    for name, gate in gates.items():
        assert gate["status"] in GATE_STATUSES, name
    validate_gate_statuses(gates)
    return restored


def _gate_map(record: dict) -> dict[str, str]:
    return {k: v["status"] for k, v in record["evaluation_gates"].items()}


def test_observed_full_success():
    returned = _passed_return("Calculate $2 + 3$.")
    record = build_generator_artifact(
        record_id="obs-full",
        outcome="passed",
        raw_response_available=True,
        candidate_extracted=CANDIDATE,
        returned_value=returned,
        frozen_payload=FROZEN,
        base={"raw_first_attempt_output": CANDIDATE, "task_id": "t_full"},
    )
    assert record["ledger_stage"] == "observed"
    assert record["actual_question_text"] == "Calculate $2 + 3$."
    assert _gate_map(record) == {
        "g1_evaluability": PASS,
        "g2_executability": PASS,
        "g3_contract_compliance": PASS,
        "g4_semantic_correctness": PASS,
        "g5_problem_presentation": PASS,
        "g6_math_notation": PASS,
    }
    assert record["composite_outcomes"] == {
        "technical_pass": PASS,
        "presentation_pass": PASS,
        "full_pass": PASS,
    }
    _assert_json_safe(record)


def test_observed_runtime_failure():
    record = build_generator_artifact(
        record_id="obs-runtime",
        outcome="execution_failure",
        raw_response_available=True,
        candidate_extracted=CANDIDATE,
        returned_value=None,
        detail={
            "exception_type": "NameError",
            "exception_message": "name 'x' is not defined",
        },
        base={"raw_first_attempt_output": CANDIDATE},
    )
    gates = record["evaluation_gates"]
    assert gates["g1_evaluability"]["status"] == PASS
    assert gates["g2_executability"]["status"] == FAIL
    assert gates["g2_executability"]["exception_type"] == "NameError"
    assert gates["g3_contract_compliance"]["status"] == NOT_ASSESSED
    assert gates["g4_semantic_correctness"]["status"] == NOT_ASSESSED
    assert gates["g5_problem_presentation"]["status"] == NOT_OBSERVED
    assert gates["g6_math_notation"]["status"] == NOT_OBSERVED
    assert record["composite_outcomes"]["technical_pass"] == FAIL
    assert record["composite_outcomes"]["full_pass"] == FAIL
    assert record["composite_outcomes"]["presentation_pass"] == NOT_OBSERVED
    _assert_json_safe(record)


def test_observed_semantic_failure():
    returned = _passed_return("Find the sum of 2 and 3.", answer=999)
    record = build_generator_artifact(
        record_id="obs-semantic",
        outcome="oracle_mismatch",
        raw_response_available=True,
        candidate_extracted=CANDIDATE,
        returned_value=returned,
        frozen_payload=FROZEN,
        detail={"mismatch_reason": "oracle_mismatch"},
        base={"raw_first_attempt_output": CANDIDATE},
    )
    assert _gate_map(record) == {
        "g1_evaluability": PASS,
        "g2_executability": PASS,
        "g3_contract_compliance": PASS,
        "g4_semantic_correctness": FAIL,
        "g5_problem_presentation": PASS,
        "g6_math_notation": PASS,
    }
    assert record["composite_outcomes"]["technical_pass"] == FAIL
    assert record["composite_outcomes"]["presentation_pass"] == PASS
    assert record["composite_outcomes"]["full_pass"] == FAIL
    _assert_json_safe(record)


def test_presentation_failure_g6():
    returned = _passed_return("Solve $x + 1.")
    record = build_generator_artifact(
        record_id="obs-g6",
        outcome="passed",
        raw_response_available=True,
        candidate_extracted=CANDIDATE,
        returned_value=returned,
        frozen_payload=FROZEN,
        base={"raw_first_attempt_output": CANDIDATE},
    )
    assert record["evaluation_gates"]["g5_problem_presentation"]["status"] == PASS
    assert record["evaluation_gates"]["g6_math_notation"]["status"] == FAIL
    assert "latex_delimiter_failure" in record["evaluation_gates"]["g6_math_notation"]["reason"]
    assert record["composite_outcomes"]["technical_pass"] == PASS
    assert record["composite_outcomes"]["presentation_pass"] == FAIL
    assert record["composite_outcomes"]["full_pass"] == FAIL
    _assert_json_safe(record)


def test_experiment_not_run_not_fail_and_distinct_from_generator_failure():
    missing = build_generator_artifact(
        record_id="obs-not-run",
        outcome=EXPERIMENT_NOT_RUN,
        raw_response_available=False,
        candidate_extracted=None,
        base={"task_id": "ce115_calc_not_run"},
    )
    assert missing["ledger_stage"] == "observed"
    assert missing["observation_status"] == EXPERIMENT_NOT_RUN
    for name, gate in missing["evaluation_gates"].items():
        assert gate["status"] == NOT_OBSERVED, name
        assert gate["status"] != FAIL
    assert missing["composite_outcomes"]["full_pass"] == NOT_OBSERVED
    assert missing["composite_outcomes"]["technical_pass"] == NOT_OBSERVED

    empty = build_generator_artifact(
        record_id="obs-empty",
        outcome="empty_response",
        raw_response_available=True,
        candidate_extracted=None,
        base={"raw_first_attempt_output": ""},
    )
    assert empty["observation_status"] == GENERATOR_FAILURE
    assert empty["evaluation_gates"]["g1_evaluability"]["status"] == FAIL
    assert empty["observation_status"] != missing["observation_status"]
    _assert_json_safe(missing)
    _assert_json_safe(empty)


def test_pipeline_corrected_independent_record():
    observed = build_generator_artifact(
        record_id="obs-pipe-src",
        outcome="parse_failure",
        raw_response_available=True,
        candidate_extracted=None,
        base={
            "raw_first_attempt_output": "```python\ndef generate(\n",
            "task_id": "t_pipe",
            "oracle_pass": False,
        },
    )
    observed_snapshot = copy.deepcopy(observed)
    repaired_candidate = (
        "def generate(level=1, **kwargs):\n"
        " return {'question_text':'Calculate 2 + 3.','correct_answer':5,"
        f"'oracle_payload':{json.dumps(FROZEN)}}}\n"
    )
    corrected = derive_pipeline_corrected_record(
        observed,
        record_id="pipe-1",
        correction_actions=["fence_trim", "trailing_fence_close"],
        outcome="passed",
        candidate_extracted=repaired_candidate,
        returned_value=_passed_return("Calculate 2 + 3."),
        frozen_payload=FROZEN,
    )
    assert corrected is not observed
    assert corrected["ledger_stage"] == "pipeline_corrected"
    assert corrected["source_record_id"] == "obs-pipe-src"
    assert corrected["correction_actions"] == ["fence_trim", "trailing_fence_close"]
    assert corrected["raw_first_attempt_output"] == observed["raw_first_attempt_output"]
    assert corrected["candidate_extracted"] == repaired_candidate
    assert corrected["candidate_extracted"] != observed.get("candidate_extracted")
    # Must not rewrite observed, and must not inject oracle answers into correction_actions.
    assert observed == observed_snapshot
    assert "oracle" not in json.dumps(corrected["correction_actions"]).lower()
    assert "5" not in corrected["correction_actions"]
    _assert_json_safe(corrected)


def test_post_healer_rescued():
    observed = build_generator_artifact(
        record_id="obs-rescue-src",
        outcome="parse_minor",
        raw_response_available=True,
        candidate_extracted="def generate(:\n pass\n",
        base={"raw_first_attempt_output": "def generate(:\n pass\n", "oracle_pass": False},
    )
    observed_snapshot = copy.deepcopy(observed)
    healer = build_healer_fields(
        eligible=True,
        attempted=True,
        rescued=True,
        regression=False,
        reason="deterministic_fence_repair",
        actions=["close_fence"],
    )
    healed = derive_post_healer_record(
        observed,
        record_id="heal-rescued",
        healer=healer,
        outcome="passed",
        candidate_extracted=CANDIDATE,
        returned_value=_passed_return("Calculate 2 + 3."),
        frozen_payload=FROZEN,
        correction_actions=["close_fence"],
    )
    assert healed["ledger_stage"] == "post_healer"
    assert healed["source_record_id"] == "obs-rescue-src"
    assert healed["healer"] == {
        "eligible": True,
        "attempted": True,
        "rescued": True,
        "regression": False,
        "reason": "deterministic_fence_repair",
        "actions": ["close_fence"],
    }
    assert observed == observed_snapshot
    assert healed["composite_outcomes"]["full_pass"] == PASS
    _assert_json_safe(healed)


def test_post_healer_ineligible():
    observed = build_generator_artifact(
        record_id="obs-ineligible-src",
        outcome="oracle_mismatch",
        raw_response_available=True,
        candidate_extracted=CANDIDATE,
        returned_value=_passed_return("Find 2+3.", answer=9),
        frozen_payload=FROZEN,
        detail={"mismatch_reason": "oracle_mismatch"},
        base={"raw_first_attempt_output": CANDIDATE, "oracle_pass": False},
    )
    observed_snapshot = copy.deepcopy(observed)
    healer = build_healer_fields(
        eligible=False,
        attempted=True,  # must be forced false by helper
        rescued=True,
        regression=False,
        reason="semantic_oracle_mismatch_out_of_scope",
    )
    assert healer["eligible"] is False
    assert healer["attempted"] is False
    assert healer["rescued"] is False
    post = derive_post_healer_record(
        observed,
        record_id="heal-ineligible",
        healer=healer,
        outcome="passed",  # must not invent a repaired passing candidate
        candidate_extracted="REPAIRED_SHOULD_NOT_APPEAR",
        returned_value=_passed_return("Find 2+3.", answer=5),
        frozen_payload=FROZEN,
    )
    assert post["ledger_stage"] == "post_healer"
    assert post["healer"]["eligible"] is False
    assert post["healer"]["attempted"] is False
    assert post["candidate_extracted"] == observed["candidate_extracted"]
    assert post["candidate_extracted"] != "REPAIRED_SHOULD_NOT_APPEAR"
    assert observed == observed_snapshot
    assert observed["evaluation_gates"]["g4_semantic_correctness"]["status"] == FAIL
    _assert_json_safe(post)


def test_healer_regression():
    observed = build_generator_artifact(
        record_id="obs-regress-src",
        outcome="passed",
        raw_response_available=True,
        candidate_extracted=CANDIDATE,
        returned_value=_passed_return("Calculate 2 + 3."),
        frozen_payload=FROZEN,
        base={"raw_first_attempt_output": CANDIDATE, "oracle_pass": True},
    )
    pipe = derive_pipeline_corrected_record(
        observed,
        record_id="pipe-regress",
        correction_actions=["whitespace_normalize"],
        outcome="passed",
        candidate_extracted=CANDIDATE,
        returned_value=_passed_return("Calculate 2 + 3."),
        frozen_payload=FROZEN,
    )
    observed_snapshot = copy.deepcopy(observed)
    pipe_snapshot = copy.deepcopy(pipe)
    healer = build_healer_fields(
        eligible=True,
        attempted=True,
        rescued=False,
        regression=True,
        reason="healer_broke_entry_point",
        actions=["aggressive_rewrite"],
    )
    post = derive_post_healer_record(
        observed,
        record_id="heal-regress",
        healer=healer,
        outcome="missing_entry_point",
        candidate_extracted="print('oops')\n",
        correction_actions=["aggressive_rewrite"],
    )
    assert post["healer"]["attempted"] is True
    assert post["healer"]["rescued"] is False
    assert post["healer"]["regression"] is True
    assert post["evaluation_gates"]["g1_evaluability"]["status"] == FAIL
    assert observed == observed_snapshot
    assert pipe == pipe_snapshot
    _assert_json_safe(post)


def test_backward_compatibility_legacy_record():
    legacy = {
        "task_id": "legacy_t",
        "oracle_pass": False,
        "raw_first_attack_output": None,
        "raw_first_attempt_output": "x",
        "failure_category": "empty_response",
    }
    values = read_success_fields(legacy)
    assert values["ledger_stage"] is None
    assert values["evaluation_gates"] is None
    assert values["healer"] is None
    assert values["source_record_id"] is None
    # Must not auto-promote missing evidence to FAIL
    assert values["composite_outcomes"] is None
    text = json.dumps(legacy, sort_keys=True)
    restored = json.loads(text)
    assert "evaluation_gates" not in restored
    assert restored["oracle_pass"] is False


@pytest.mark.parametrize(
    ("outcome", "gate", "status", "extra"),
    [
        ("empty_response", "g1_evaluability", FAIL, {}),
        ("parse_failure", "g1_evaluability", FAIL, {}),
        (
            "execution_failure",
            "g2_executability",
            FAIL,
            {"detail": {"exception_type": "RuntimeError", "exception_message": "boom"}},
        ),
        (
            "contract_schema_failure",
            "g3_contract_compliance",
            FAIL,
            {
                "returned_value": {"question_text": "q", "correct_answer": 1},
                "frozen_payload": {},
            },
        ),
        (
            "oracle_mismatch",
            "g4_semantic_correctness",
            FAIL,
            {
                "returned_value": _passed_return("q", answer=0),
                "frozen_payload": FROZEN,
                "detail": {"mismatch_reason": "oracle_mismatch"},
            },
        ),
    ],
)
def test_failure_taxonomy_gate_mapping(outcome, gate, status, extra):
    kwargs = {
        "returned_value": None,
        "frozen_payload": None,
        "detail": None,
        "candidate_extracted": CANDIDATE if outcome not in {"empty_response"} else None,
    }
    kwargs.update(extra)
    record = build_generator_artifact(
        record_id=f"tax-{outcome}",
        outcome=outcome,
        raw_response_available=True,
        base={"raw_first_attempt_output": "x"},
        **kwargs,
    )
    assert record["evaluation_gates"][gate]["status"] == status
    if outcome == "empty_response":
        assert record["evaluation_gates"]["g1_evaluability"]["reason"] == "empty_response"
    if outcome == "parse_failure":
        assert record["evaluation_gates"]["g1_evaluability"]["reason"] == "parse_failure"
    if outcome == "execution_failure":
        assert record["evaluation_gates"]["g2_executability"]["reason"] == "execution_failure"
    if outcome == "contract_schema_failure":
        assert record["evaluation_gates"]["g3_contract_compliance"]["reason"] == "contract_schema_failure"
    if outcome == "oracle_mismatch":
        assert record["evaluation_gates"]["g4_semantic_correctness"]["reason"] == "oracle_mismatch"
    _assert_json_safe(record)


def test_taxonomy_question_missing_and_placeholder_and_latex():
    missing_q = build_generator_artifact(
        record_id="tax-q-missing",
        outcome="passed",
        raw_response_available=True,
        candidate_extracted=CANDIDATE,
        returned_value={"correct_answer": 1, "oracle_payload": FROZEN},
        frozen_payload=FROZEN,
    )
    # Missing question_text → G5/G6 NOT_OBSERVED (not FAIL)
    assert missing_q["actual_question_text"] is None
    assert missing_q["evaluation_gates"]["g5_problem_presentation"]["status"] == NOT_OBSERVED
    assert missing_q["evaluation_gates"]["g6_math_notation"]["status"] == NOT_OBSERVED

    placeholder = build_generator_artifact(
        record_id="tax-placeholder",
        outcome="passed",
        raw_response_available=True,
        candidate_extracted=CANDIDATE,
        returned_value=_passed_return("Solve {{value}}."),
        frozen_payload=FROZEN,
    )
    g5 = placeholder["evaluation_gates"]["g5_problem_presentation"]
    assert g5["status"] == FAIL
    assert "placeholder_leak" in g5["reason"]

    latex = build_generator_artifact(
        record_id="tax-latex",
        outcome="passed",
        raw_response_available=True,
        candidate_extracted=CANDIDATE,
        returned_value=_passed_return("Solve $x + 1."),
        frozen_payload=FROZEN,
    )
    g6 = latex["evaluation_gates"]["g6_math_notation"]
    assert g6["status"] == FAIL
    assert "latex_delimiter_failure" in g6["reason"]
    _assert_json_safe(missing_q)
    _assert_json_safe(placeholder)
    _assert_json_safe(latex)


def test_json_rejects_raw_exception_objects():
    with pytest.raises(TypeError):
        build_generator_artifact(
            record_id="bad-exc",
            outcome="execution_failure",
            raw_response_available=True,
            candidate_extracted=CANDIDATE,
            detail={"exception_type": "ValueError", "exception_message": ValueError("nope")},
            base={"raw_first_attempt_output": CANDIDATE},
        )


def test_exception_serialized_as_type_and_message_only():
    record = build_generator_artifact(
        record_id="exc-ok",
        outcome="execution_failure",
        raw_response_available=True,
        candidate_extracted=CANDIDATE,
        detail={
            "exception_type": "ValueError",
            "exception_message": "invalid literal",
        },
        base={"raw_first_attempt_output": CANDIDATE},
    )
    g2 = record["evaluation_gates"]["g2_executability"]
    assert g2["exception_type"] == "ValueError"
    assert g2["exception_message"] == "invalid literal"
    assert isinstance(g2["exception_type"], str)
    assert isinstance(g2["exception_message"], str)
    _assert_json_safe(record)


def test_additive_fields_do_not_delete_legacy_keys():
    base = {
        "task_id": "keep_me",
        "oracle_pass": True,
        "raw_first_attempt_output": CANDIDATE,
        "legacy_score": 0.91,
    }
    record = build_generator_artifact(
        record_id="additive-1",
        outcome="passed",
        raw_response_available=True,
        candidate_extracted=CANDIDATE,
        returned_value=_passed_return("Calculate 2 + 3."),
        frozen_payload=FROZEN,
        base=base,
    )
    assert record["task_id"] == "keep_me"
    assert record["oracle_pass"] is True
    assert record["legacy_score"] == 0.91
    assert "evaluation_gates" in record
    _assert_json_safe(record)


def test_three_ledgers_are_independent_records():
    observed = build_generator_artifact(
        record_id="obs-independent",
        outcome="parse_failure",
        raw_response_available=True,
        candidate_extracted=None,
        base={"raw_first_attempt_output": "broken"},
    )
    pipe = derive_pipeline_corrected_record(
        observed,
        record_id="pipe-independent",
        correction_actions=["recover_fence"],
        outcome="passed",
        candidate_extracted=CANDIDATE,
        returned_value=_passed_return("Calculate 2 + 3."),
        frozen_payload=FROZEN,
    )
    post = derive_post_healer_record(
        observed,
        record_id="heal-independent",
        healer=build_healer_fields(eligible=True, attempted=True, rescued=True, actions=["fix"]),
        outcome="passed",
        candidate_extracted=CANDIDATE,
        returned_value=_passed_return("Calculate 2 + 3."),
        frozen_payload=FROZEN,
    )
    assert len({id(observed), id(pipe), id(post)}) == 3
    assert observed["ledger_stage"] == "observed"
    assert pipe["ledger_stage"] == "pipeline_corrected"
    assert post["ledger_stage"] == "post_healer"
    assert pipe["source_record_id"] == observed["record_id"]
    assert post["source_record_id"] == observed["record_id"]
