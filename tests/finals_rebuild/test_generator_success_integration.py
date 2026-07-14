"""Integration tests for Milestone 1B generator success-chain observability."""
from __future__ import annotations

import json
from pathlib import Path

from agent_tools.finals_rebuild.generator_success import (
    FAIL,
    NOT_ASSESSED,
    NOT_OBSERVED,
    PASS,
    assemble_observed_success_fields,
    composite_outcomes,
    evaluate_math_notation,
    evaluate_problem_presentation,
    merge_success_fields,
    read_success_fields,
)
from agent_tools.finals_rebuild.math_boundary_pilot import classify_response
from agent_tools.finals_rebuild.math_task_sampler import sample_task_parameters

MANIFEST = Path(__file__).parent / "fixtures" / "math_generation_tasks_ce115_pilot.jsonl"


def _task_and_frozen():
    task = next(
        json.loads(line)
        for line in MANIFEST.read_text(encoding="utf-8").splitlines()
        if line.strip() and '"ce115_q07_polynomial_division_l1"' in line
    )
    sampled = sample_task_parameters(task, 2026071301)
    frozen = {
        "task_id": task["task_id"],
        "oracle_type": task["oracle_type"],
        "oracle_payload": sampled["oracle_payload"],
    }
    return task, frozen


def test_successful_return_persists_question_text():
    task, frozen = _task_and_frozen()
    payload = json.dumps(frozen["oracle_payload"], sort_keys=True)
    source = (
        "def generate(level=1, **kwargs):\n"
        " return {'question_text':'Divide the polynomials.',"
        f"'correct_answer':{{'quotient_coefficients':[1,1],'remainder':0}},'oracle_payload':{payload}}}\n"
    )
    outcome, _candidate, detail = classify_response(source, frozen, task)
    assert outcome in {"passed", "answer_incorrect"}
    assert detail["actual_question_text"] == "Divide the polynomials."
    assert detail["ledger_stage"] == "observed"
    assert "evaluation_gates" in detail and "composite_outcomes" in detail


def test_missing_question_text_marks_g5_g6_not_observed():
    fields = assemble_observed_success_fields(
        outcome="schema_failure",
        raw_response_available=True,
        candidate_extracted="def generate():\n return {'correct_answer': 1, 'oracle_payload': {}}\n",
        returned_value={"correct_answer": 1, "oracle_payload": {}},
        frozen_payload={},
    )
    assert fields["actual_question_text"] is None
    assert fields["evaluation_gates"]["g5_problem_presentation"]["status"] == NOT_OBSERVED
    assert fields["evaluation_gates"]["g6_math_notation"]["status"] == NOT_OBSERVED


def test_runtime_name_error_is_g2_fail():
    task, frozen = _task_and_frozen()
    source = "def generate(level=1, **kwargs):\n return missing_name\n"
    outcome, _candidate, detail = classify_response(source, frozen, task)
    assert outcome == "runtime_failure"
    gates = detail["evaluation_gates"]
    assert gates["g1_evaluability"]["status"] == PASS
    assert gates["g2_executability"]["status"] == FAIL
    assert gates["g2_executability"]["exception_type"] == "NameError"
    assert gates["g3_contract_compliance"]["status"] == NOT_ASSESSED
    assert gates["g4_semantic_correctness"]["status"] == NOT_ASSESSED
    assert detail["actual_question_text"] is None


def test_schema_missing_key_is_g3_fail():
    task, frozen = _task_and_frozen()
    source = "def generate(level=1, **kwargs):\n return {'question_text':'q','correct_answer':1}\n"
    outcome, _candidate, detail = classify_response(source, frozen, task)
    assert outcome == "schema_failure"
    gates = detail["evaluation_gates"]
    assert gates["g1_evaluability"]["status"] == PASS
    assert gates["g2_executability"]["status"] == PASS
    assert gates["g3_contract_compliance"]["status"] == FAIL
    assert "oracle_payload" in gates["g3_contract_compliance"]["missing_keys"]
    assert gates["g4_semantic_correctness"]["status"] == NOT_ASSESSED
    assert detail["actual_question_text"] == "q"


def test_oracle_mismatch_is_g4_fail():
    task, frozen = _task_and_frozen()
    payload = json.dumps(frozen["oracle_payload"], sort_keys=True)
    source = (
        "def generate(level=1, **kwargs):\n"
        " return {'question_text':'q',"
        f"'correct_answer':{{'quotient_coefficients':[9,9],'remainder':9}},'oracle_payload':{payload}}}\n"
    )
    outcome, _candidate, detail = classify_response(source, frozen, task)
    assert outcome == "answer_incorrect"
    gates = detail["evaluation_gates"]
    assert gates["g1_evaluability"]["status"] == PASS
    assert gates["g2_executability"]["status"] == PASS
    assert gates["g3_contract_compliance"]["status"] == PASS
    assert gates["g4_semantic_correctness"]["status"] == FAIL


def test_full_pass_when_all_gates_pass():
    returned = {
        "question_text": "Calculate 2 + 2.",
        "correct_answer": {"value": 4},
        "oracle_payload": {"a": 1},
    }
    fields = assemble_observed_success_fields(
        outcome="passed",
        raw_response_available=True,
        candidate_extracted="def generate():\n return {}\n",
        returned_value=returned,
        frozen_payload={"a": 1},
    )
    assert fields["evaluation_gates"]["g1_evaluability"]["status"] == PASS
    assert fields["evaluation_gates"]["g2_executability"]["status"] == PASS
    assert fields["evaluation_gates"]["g3_contract_compliance"]["status"] == PASS
    assert fields["evaluation_gates"]["g4_semantic_correctness"]["status"] == PASS
    assert fields["evaluation_gates"]["g5_problem_presentation"]["status"] == PASS
    assert fields["evaluation_gates"]["g6_math_notation"]["status"] == PASS
    assert fields["composite_outcomes"] == {
        "technical_pass": PASS,
        "presentation_pass": PASS,
        "full_pass": PASS,
    }


def test_g6_fail_keeps_technical_pass_and_fails_full():
    returned = {
        "question_text": "Solve $x + 1.",
        "correct_answer": {"value": 1},
        "oracle_payload": {"a": 1},
    }
    fields = assemble_observed_success_fields(
        outcome="passed",
        raw_response_available=True,
        candidate_extracted="def generate():\n return {}\n",
        returned_value=returned,
        frozen_payload={"a": 1},
    )
    assert fields["evaluation_gates"]["g6_math_notation"]["status"] == FAIL
    assert fields["composite_outcomes"]["technical_pass"] == PASS
    assert fields["composite_outcomes"]["presentation_pass"] == FAIL
    assert fields["composite_outcomes"]["full_pass"] == FAIL


def test_artifact_includes_ledger_stage_observed():
    fields = assemble_observed_success_fields(
        outcome="empty_response",
        raw_response_available=False,
        candidate_extracted=None,
    )
    assert fields["ledger_stage"] == "observed"


def test_old_record_missing_success_fields_does_not_crash():
    legacy = {"task_id": "old", "oracle_pass": False, "raw_first_attempt_output": "x"}
    values = read_success_fields(legacy)
    assert values["ledger_stage"] is None
    assert values["actual_question_text"] is None
    assert values["evaluation_gates"] is None
    assert values["composite_outcomes"] is None
    merged = merge_success_fields(dict(legacy), {})
    assert merged["task_id"] == "old"


def test_artifact_is_json_serializable():
    fields = assemble_observed_success_fields(
        outcome="passed",
        raw_response_available=True,
        candidate_extracted="def generate():\n pass\n",
        returned_value={
            "question_text": "Compute $2$.",
            "correct_answer": 2,
            "oracle_payload": {},
        },
        frozen_payload={},
    )
    row = {"task_id": "t1", "raw_first_attempt_output": "code", "candidate_extracted": "code"}
    merge_success_fields(row, fields)
    serialized = json.dumps(row, sort_keys=True, ensure_ascii=False)
    restored = json.loads(serialized)
    assert restored["ledger_stage"] == "observed"
    assert restored["evaluation_gates"]["g1_evaluability"]["status"] == PASS


def test_helper_unit_cases_still_hold():
    assert evaluate_problem_presentation("Calculate 2 + 2.")["status"] == PASS
    assert evaluate_math_notation("Calculate $x + 1$.")["status"] == PASS
    names = (
        "g1_evaluability", "g2_executability", "g3_contract_compliance",
        "g4_semantic_correctness", "g5_problem_presentation", "g6_math_notation",
    )
    gates = {name: {"status": PASS} for name in names}
    assert composite_outcomes(gates)["full_pass"] == PASS
