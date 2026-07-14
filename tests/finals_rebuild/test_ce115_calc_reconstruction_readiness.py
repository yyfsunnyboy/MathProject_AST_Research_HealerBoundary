"""Milestone 2B — corrected four-task reconstruction readiness (no model runs)."""
from __future__ import annotations

import json
from fractions import Fraction
from math import gcd, isqrt
from pathlib import Path

import pytest

from agent_tools.finals_rebuild.ce115_calc_golden_generators import (
    FORMAL_L1_TASK_IDS,
    GOLDEN_SEED,
    NOTATION_POLICY,
    all_golden_sources,
    build_golden_generate_source,
    build_golden_return,
    formal_l1_tasks,
    load_manifest_tasks,
    render_question_text,
)
from agent_tools.finals_rebuild.generator_success import (
    FAIL,
    NOT_OBSERVED,
    PASS,
    assemble_observed_success_fields,
    serialize_artifact,
)
from agent_tools.finals_rebuild.math_answer_contracts import (
    CONTRACTS,
    NEUTRAL_TASK_STATEMENTS,
    render_answer_contract,
)
from agent_tools.finals_rebuild.math_boundary_pilot import (
    TASK_IDS,
    build_ab1_prompt,
    build_ab2g_prompt,
    classify_response,
    frozen_payloads,
)
from agent_tools.finals_rebuild.math_task_oracles import evaluate_math_task_oracle
from agent_tools.finals_rebuild.math_task_sampler import sample_task_parameters

MANIFEST = Path(__file__).parent / "fixtures" / "math_generation_tasks_ce115_pilot.jsonl"


@pytest.fixture(scope="module")
def tasks():
    return formal_l1_tasks()


@pytest.mark.parametrize("task_id", FORMAL_L1_TASK_IDS)
def test_manifest_formal_task_exists_with_correct_id(task_id, tasks):
    assert task_id in TASK_IDS
    task = tasks[task_id]
    assert task["task_id"] == task_id
    assert task["required_entry_point"] == "generate"
    assert task["required_output_keys"] == ["question_text", "correct_answer", "oracle_payload"]
    assert task["difficulty_level"] == 1


def test_formal_set_matches_pilot_task_ids(tasks):
    assert tuple(tasks) == TASK_IDS == FORMAL_L1_TASK_IDS
    assert "ce115_cr01_training_sequence_threshold_l3" not in load_manifest_tasks() or (
        "ce115_cr01_training_sequence_threshold_l3" not in TASK_IDS
    )


@pytest.mark.parametrize("task_id", FORMAL_L1_TASK_IDS)
def test_frozen_parameters_schema_and_oracle_independence(task_id, tasks):
    task = tasks[task_id]
    sampled = sample_task_parameters(task, GOLDEN_SEED)
    payload = sampled["oracle_payload"]
    assert isinstance(payload, dict) and payload
    # Sampler freezes exact JSON-safe values; generator must echo them unchanged.
    text = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    restored = json.loads(text)
    assert restored == payload
    verdict = evaluate_math_task_oracle(task["oracle_type"], payload, None)
    assert verdict["error"] is None
    assert verdict["expected_answer"] is not None
    # Oracle must not need the generator's correct_answer to produce expected.
    assert evaluate_math_task_oracle(task["oracle_type"], payload, {"sentinel": True})["is_correct"] is False


@pytest.mark.parametrize("task_id", FORMAL_L1_TASK_IDS)
def test_oracle_accepts_expected_and_rejects_wrong_answer(task_id, tasks):
    task = tasks[task_id]
    payload = sample_task_parameters(task, GOLDEN_SEED)["oracle_payload"]
    expected = evaluate_math_task_oracle(task["oracle_type"], payload, None)["expected_answer"]
    assert evaluate_math_task_oracle(task["oracle_type"], payload, expected)["is_correct"] is True
    wrong = json.loads(json.dumps(expected))
    key = next(iter(wrong))
    if isinstance(wrong[key], list):
        wrong[key] = list(wrong[key]) + [999]
    elif isinstance(wrong[key], int):
        wrong[key] = wrong[key] + 1
    else:
        wrong[key] = "999/1"
    assert evaluate_math_task_oracle(task["oracle_type"], payload, wrong)["is_correct"] is False


@pytest.mark.parametrize("task_id", FORMAL_L1_TASK_IDS)
def test_answer_contract_registered_for_formal_task(task_id, tasks):
    task = tasks[task_id]
    assert task["oracle_type"] in CONTRACTS
    assert task["oracle_type"] in NEUTRAL_TASK_STATEMENTS
    payload = sample_task_parameters(task, GOLDEN_SEED)["oracle_payload"]
    contract = render_answer_contract(task, payload)
    assert "Required return schema" in contract
    assert json.dumps(payload, sort_keys=True) in contract
    assert NOTATION_POLICY[task["oracle_type"]]


@pytest.mark.parametrize("task_id", FORMAL_L1_TASK_IDS)
def test_golden_generator_contract_and_g1_g6_full_pass(task_id, tasks):
    task = tasks[task_id]
    source = build_golden_generate_source(task, seed=GOLDEN_SEED)
    returned = build_golden_return(task, seed=GOLDEN_SEED)
    assert isinstance(returned["question_text"], str) and returned["question_text"].strip()
    frozen = {
        "task_id": task["task_id"],
        "oracle_type": task["oracle_type"],
        "oracle_payload": returned["oracle_payload"],
    }
    outcome, candidate, detail = classify_response(source, frozen, task)
    assert outcome == "passed", detail
    assert candidate and "def generate" in candidate
    assert detail["actual_question_text"] == returned["question_text"]
    assert detail["ledger_stage"] == "observed"
    gates = detail["evaluation_gates"]
    assert {name: gates[name]["status"] for name in gates} == {
        "g1_evaluability": PASS,
        "g2_executability": PASS,
        "g3_contract_compliance": PASS,
        "g4_semantic_correctness": PASS,
        "g5_problem_presentation": PASS,
        "g6_math_notation": PASS,
    }
    assert detail["composite_outcomes"]["full_pass"] == PASS
    row = {
        "task_id": task_id,
        "raw_first_attempt_output": source,
        "candidate_extracted": candidate,
        **{k: detail[k] for k in ("ledger_stage", "actual_question_text", "evaluation_gates", "composite_outcomes")},
    }
    restored = json.loads(serialize_artifact(row))
    assert restored["composite_outcomes"]["full_pass"] == PASS


def test_radical_canonical_invariant(tasks):
    task = tasks["ce115_calc_radical_simplification_l1"]
    payload = sample_task_parameters(task, GOLDEN_SEED)["oracle_payload"]
    expected = evaluate_math_task_oracle(task["oracle_type"], payload, None)["expected_answer"]
    radicand = payload["radicand"]
    outer = payload.get("outer_coefficient", 1)
    k, m = expected["coefficient"], expected["radicand"]
    assert k > 0 and m > 1 and isqrt(m) ** 2 != m
    factor = 2
    while factor * factor <= m:
        assert m % (factor * factor) != 0
        factor += 1
    assert (k // outer) ** 2 * m == radicand and k % outer == 0


def test_rational_canonical_reduction(tasks):
    task = tasks["ce115_calc_exact_rational_expression_l1"]
    payload = sample_task_parameters(task, GOLDEN_SEED)["oracle_payload"]
    total = sum(p["sign"] * Fraction(p["left"]) * Fraction(p["right"]) for p in payload["products"])
    expected = evaluate_math_task_oracle(task["oracle_type"], payload, None)["expected_answer"]
    value = expected["value"]
    assert isinstance(value, str) and "." not in value
    assert Fraction(value) == total
    if "/" in value:
        numerator, denominator = value.split("/")
        assert int(denominator) > 1
        assert gcd(abs(int(numerator)), int(denominator)) == 1


def test_polynomial_remainder_invariant(tasks):
    task = tasks["ce115_calc_polynomial_division_l1"]
    payload = sample_task_parameters(task, GOLDEN_SEED)["oracle_payload"]
    expected = evaluate_math_task_oracle(task["oracle_type"], payload, None)["expected_answer"]
    divisor = [Fraction(c) for c in payload["divisor_coefficients"]]
    quotient = [Fraction(str(v)) for v in expected["quotient_coefficients"]]
    remainder = [Fraction(str(v)) for v in expected["remainder_coefficients"]]
    assert len(remainder) == 1
    product = [Fraction(0)] * (len(quotient) + 1)
    for i, q in enumerate(quotient):
        product[i] += q * divisor[0]
        product[i + 1] += q * divisor[1]
    product[-1] += remainder[0]
    assert product == [Fraction(c) for c in payload["dividend_coefficients"]]


def test_root_ordering_invariant(tasks):
    task = tasks["ce115_calc_polynomial_factor_roots_l1"]
    payload = sample_task_parameters(task, GOLDEN_SEED)["oracle_payload"]
    a, b, c = payload["quadratic_coefficients"]
    expected = evaluate_math_task_oracle(task["oracle_type"], payload, None)["expected_answer"]
    roots = [Fraction(str(v)) for v in expected["roots"]]
    assert len(roots) == 2 and roots[0] < roots[1]
    assert "linear_combination" not in payload  # calc family reconstructs roots only
    for root in roots:
        assert a * root * root + b * root + c == 0


def test_golden_generators_absent_from_prompt_assembly(tasks):
    sources = all_golden_sources()
    markers = []
    for task_id, source in sources.items():
        task = tasks[task_id]
        returned = build_golden_return(task)
        markers.extend(
            [
                "ce115_calc_golden_generators",
                "GOLDEN_SEED",
                returned["question_text"],
                json.dumps(returned["correct_answer"], sort_keys=True, ensure_ascii=False),
            ]
        )
        frozen = frozen_payloads((task,), (GOLDEN_SEED,))[0]
        for prompt in (
            build_ab1_prompt(task, frozen),
            build_ab2g_prompt(task, frozen),
            render_answer_contract(task, frozen["oracle_payload"]),
        ):
            for marker in markers[-4:]:
                assert marker not in prompt, f"{task_id} leaked golden marker into prompt"


@pytest.mark.parametrize("task_id", FORMAL_L1_TASK_IDS)
def test_question_text_matches_frozen_parameters_without_answer_leak(task_id, tasks):
    task = tasks[task_id]
    returned = build_golden_return(task)
    question = returned["question_text"]
    assert question == render_question_text(task, returned["oracle_payload"])
    answer_json = json.dumps(returned["correct_answer"], sort_keys=True)
    assert answer_json not in question
    fields = assemble_observed_success_fields(
        outcome="passed",
        raw_response_available=True,
        candidate_extracted="def generate():\n return {}\n",
        returned_value=returned,
        frozen_payload=returned["oracle_payload"],
    )
    assert fields["evaluation_gates"]["g5_problem_presentation"]["status"] == PASS
    assert fields["evaluation_gates"]["g6_math_notation"]["status"] == PASS
    assert fields["evaluation_gates"]["g5_problem_presentation"]["status"] != FAIL
    assert fields["actual_question_text"] is not None
    assert fields["evaluation_gates"]["g5_problem_presentation"]["status"] != NOT_OBSERVED
