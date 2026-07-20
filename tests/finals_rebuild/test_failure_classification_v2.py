"""Unit tests for failure_classification_v2 (standard §8–§9 + fixtures)."""
from __future__ import annotations

import copy

import pytest

from agent_tools.finals_rebuild import failure_classification_v2 as v2


def _base_record(**overrides):
    record = {
        "dataset": "CE115",
        "task_id": "ce111_q02_polynomial_division_remainder",
        "model": "gemini-3.5-flash",
        "condition": "ab1",
        "seed": 2026071301,
        "prompt_hash": "sha256:abc",
        "evaluator_hash": "sha256:def",
        "evaluation_revision": "revision_003",
        "infrastructure_valid": True,
        "raw_response_present": True,
        "candidate_present": True,
        "g1_parse": "PASS",
        "g2_execution": "PASS",
        "g3_contract": "FAIL",
        "g3a_required_api": "NOT_APPLICABLE",
        "g3c_canonical_form": "NOT_APPLICABLE",
        "g4_correctness": "NOT_ASSESSED",
        "final_status": "FAILED",
        "primary_failure_layer": "L2",
        "outcome_validity": "VALID_MODEL_OUTCOME",
        "failure_subtype": "OUTPUT_PACKAGING",
        "mechanism_tags": ["output_packaging"],
        "failure_chain": [],
        "exception_type": None,
        "exception_message": None,
        "healer_eligible": True,
        "matched_rule": None,
        "healer_outcome": "noneligible",
        "review_status": "machine_labeled",
        "notes": "",
    }
    record.update(overrides)
    return record


# ---------------------------------------------------------------------------
# §9 flow branches
# ---------------------------------------------------------------------------


def test_s9_l0_infrastructure() -> None:
    out = v2.classify_cell(
        {},
        {"infrastructure_valid": False, "raw_response_present": False},
    )
    assert out["primary_failure_layer"] == "L0"
    assert out["outcome_validity"] == "INVALID_INFRASTRUCTURE"
    assert "infrastructure_failure" in out["mechanism_tags"]
    assert out["needs_human_review"] is False


def test_s9_l1_parse_fail() -> None:
    out = v2.classify_cell(
        {"g1_parse": "FAIL", "g2_execution": "NOT_ASSESSED"},
        {"infrastructure_valid": True, "raw_response_present": True},
    )
    assert out["primary_failure_layer"] == "L1"
    assert out["outcome_validity"] == "VALID_MODEL_OUTCOME"


def test_s9_l3_api_call_valid_model() -> None:
    out = v2.classify_cell(
        {"g1_parse": "PASS", "g2_execution": "FAIL"},
        {
            "infrastructure_valid": True,
            "raw_response_present": True,
            "exception_source": "api_call",
            "api_documentation_consistent": True,
        },
    )
    assert out["primary_failure_layer"] == "L3"
    assert out["outcome_validity"] == "VALID_MODEL_OUTCOME"


def test_s9_l3_api_call_invalid_contract() -> None:
    out = v2.classify_cell(
        {"g1_parse": "PASS", "g2_execution": "FAIL"},
        {
            "infrastructure_valid": True,
            "raw_response_present": True,
            "exception_source": "api_call",
            "api_documentation_consistent": False,
            "mechanism_tags": ["return_shape_hallucination"],
        },
    )
    assert out["primary_failure_layer"] == "L3"
    assert out["outcome_validity"] == "INVALID_CONTRACT"
    assert "prompt_api_mismatch" in out["mechanism_tags"]


def test_s9_l4_dataflow() -> None:
    out = v2.classify_cell(
        {"g1_parse": "PASS", "g2_execution": "FAIL"},
        {
            "infrastructure_valid": True,
            "raw_response_present": True,
            "exception_source": "dataflow",
        },
    )
    assert out["primary_failure_layer"] == "L4"
    assert out["outcome_validity"] == "VALID_MODEL_OUTCOME"


def test_s9_l4_serialization_invalid_contract() -> None:
    out = v2.classify_cell(
        {"g1_parse": "PASS", "g2_execution": "FAIL"},
        {
            "infrastructure_valid": True,
            "raw_response_present": True,
            "exception_source": "serialization",
        },
    )
    assert out["primary_failure_layer"] == "L4"
    assert out["outcome_validity"] == "INVALID_CONTRACT"


def test_s9_g2_undistinguished_needs_review() -> None:
    out = v2.classify_cell(
        {"g1_parse": "PASS", "g2_execution": "FAIL"},
        {
            "infrastructure_valid": True,
            "raw_response_present": True,
            # exception_source omitted
        },
    )
    assert out["primary_failure_layer"] is None
    assert out["needs_human_review"] is True
    assert "needs_human_review" in out["mechanism_tags"]


def test_s9_l2_contract_fail_valid() -> None:
    out = v2.classify_cell(
        {
            "g1_parse": "PASS",
            "g2_execution": "PASS",
            "g3_contract": "FAIL",
            "g4_correctness": "NOT_ASSESSED",
        },
        {
            "infrastructure_valid": True,
            "raw_response_present": True,
            "schema_explicit_in_prompt": True,
        },
    )
    assert out["primary_failure_layer"] == "L2"
    assert out["outcome_validity"] == "VALID_MODEL_OUTCOME"


def test_s9_l2_contract_fail_invalid_contract() -> None:
    out = v2.classify_cell(
        {
            "g1_parse": "PASS",
            "g2_execution": "PASS",
            "g3_contract": "FAIL",
        },
        {
            "infrastructure_valid": True,
            "raw_response_present": True,
            "schema_explicit_in_prompt": False,
        },
    )
    assert out["primary_failure_layer"] == "L2"
    assert out["outcome_validity"] == "INVALID_CONTRACT"


def test_s9_l2_g3c_canonical_fail() -> None:
    out = v2.classify_cell(
        {
            "g1_parse": "PASS",
            "g2_execution": "PASS",
            "g3_contract": "PASS",
            "g3c_canonical_form": "FAIL",
        },
        {
            "infrastructure_valid": True,
            "raw_response_present": True,
            "schema_explicit_in_prompt": True,
        },
    )
    assert out["primary_failure_layer"] == "L2"


def test_s9_l3_g3a_required_api() -> None:
    out = v2.classify_cell(
        {
            "g1_parse": "PASS",
            "g2_execution": "PASS",
            "g3_contract": "PASS",
            "g3a_required_api": "FAIL",
            "g4_correctness": "PASS",
        },
        {"infrastructure_valid": True, "raw_response_present": True},
    )
    assert out["primary_failure_layer"] == "L3"
    assert out["final_status"] == "FAILED"


def test_s9_l5_valid_model() -> None:
    out = v2.classify_cell(
        {
            "g1_parse": "PASS",
            "g2_execution": "PASS",
            "g3_contract": "PASS",
            "g4_correctness": "FAIL",
        },
        {
            "infrastructure_valid": True,
            "raw_response_present": True,
            "evaluator_logic_fault": False,
        },
    )
    assert out["primary_failure_layer"] == "L5"
    assert out["outcome_validity"] == "VALID_MODEL_OUTCOME"


def test_s9_l5_invalid_evaluator() -> None:
    out = v2.classify_cell(
        {
            "g1_parse": "PASS",
            "g2_execution": "PASS",
            "g3_contract": "PASS",
            "g4_correctness": "FAIL",
        },
        {
            "infrastructure_valid": True,
            "raw_response_present": True,
            "evaluator_logic_fault": True,
        },
    )
    assert out["primary_failure_layer"] == "L5"
    assert out["outcome_validity"] == "INVALID_EVALUATOR"


def test_s9_passed() -> None:
    out = v2.classify_cell(
        {
            "g1_parse": "PASS",
            "g2_execution": "PASS",
            "g3_contract": "PASS",
            "g3a_required_api": "NOT_APPLICABLE",
            "g3c_canonical_form": "NOT_APPLICABLE",
            "g4_correctness": "PASS",
        },
        {"infrastructure_valid": True, "raw_response_present": True},
    )
    assert out["primary_failure_layer"] == "PASSED"
    assert out["final_status"] == "PASSED"
    assert out["outcome_validity"] == "VALID_MODEL_OUTCOME"


def test_validity_orthogonality_same_l5_different_validity() -> None:
    gates = {
        "g1_parse": "PASS",
        "g2_execution": "PASS",
        "g3_contract": "PASS",
        "g4_correctness": "FAIL",
    }
    a = v2.classify_cell(
        gates,
        {
            "infrastructure_valid": True,
            "raw_response_present": True,
            "evaluator_logic_fault": True,
        },
    )
    b = v2.classify_cell(
        gates,
        {
            "infrastructure_valid": True,
            "raw_response_present": True,
            "evaluator_logic_fault": False,
        },
    )
    assert a["primary_failure_layer"] == b["primary_failure_layer"] == "L5"
    assert a["outcome_validity"] == "INVALID_EVALUATOR"
    assert b["outcome_validity"] == "VALID_MODEL_OUTCOME"


# ---------------------------------------------------------------------------
# Fixtures from v2 document battle cases
# ---------------------------------------------------------------------------


def test_fixture_evaluator_wrong_case_l5_invalid_evaluator() -> None:
    """評分冤案：6x + 24 vs 6x+24 → L5 + INVALID_EVALUATOR."""
    out = v2.classify_cell(
        {
            "g1_parse": "PASS",
            "g2_execution": "PASS",
            "g3_contract": "PASS",
            "g4_correctness": "FAIL",
        },
        {
            "infrastructure_valid": True,
            "raw_response_present": True,
            "evaluator_logic_fault": True,
            "outcome_validity": "INVALID_EVALUATOR",
        },
    )
    assert out["primary_failure_layer"] == "L5"
    assert out["outcome_validity"] == "INVALID_EVALUATOR"


def test_fixture_q02_l2_valid() -> None:
    """q02 bare-string packaging → L2 + VALID_MODEL_OUTCOME."""
    out = v2.classify_cell(
        {
            "g1_parse": "PASS",
            "g2_execution": "PASS",
            "g3_contract": "FAIL",
            "g4_correctness": "NOT_ASSESSED",
        },
        {
            "infrastructure_valid": True,
            "raw_response_present": True,
            "schema_explicit_in_prompt": True,
            "mechanism_tags": ["output_packaging"],
        },
    )
    assert out["primary_failure_layer"] == "L2"
    assert out["outcome_validity"] == "VALID_MODEL_OUTCOME"


def test_fixture_factor_roots_l3_invalid_contract() -> None:
    """factor_roots ab2d API-doc mismatch → L3 + INVALID_CONTRACT."""
    out = v2.classify_cell(
        {"g1_parse": "PASS", "g2_execution": "FAIL"},
        {
            "infrastructure_valid": True,
            "raw_response_present": True,
            "exception_source": "api_call",
            "api_documentation_consistent": False,
            "mechanism_tags": ["return_shape_hallucination", "prompt_api_mismatch"],
        },
    )
    assert out["primary_failure_layer"] == "L3"
    assert out["outcome_validity"] == "INVALID_CONTRACT"


def test_fixture_q10_l4_invalid_contract() -> None:
    """q10 Fraction JSON serialization → L4 + INVALID_CONTRACT."""
    out = v2.classify_cell(
        {"g1_parse": "PASS", "g2_execution": "FAIL"},
        {
            "infrastructure_valid": True,
            "raw_response_present": True,
            "exception_source": "serialization",
            "outcome_validity": "INVALID_CONTRACT",
        },
    )
    assert out["primary_failure_layer"] == "L4"
    assert out["outcome_validity"] == "INVALID_CONTRACT"


def test_fixture_runaway_l1_degenerate_repetition() -> None:
    """runaway / degenerate repetition → L1 + degenerate_repetition."""
    out = v2.classify_cell(
        {"g1_parse": "FAIL", "g2_execution": "NOT_ASSESSED"},
        {
            "infrastructure_valid": True,
            "raw_response_present": True,
            "mechanism_tags": ["degenerate_repetition"],
        },
    )
    assert out["primary_failure_layer"] == "L1"
    assert "degenerate_repetition" in out["mechanism_tags"]


# ---------------------------------------------------------------------------
# Schema validation
# ---------------------------------------------------------------------------


def test_schema_accepts_complete_record() -> None:
    assert v2.validate_cell_record(_base_record()) == []


def test_schema_rejects_missing_field() -> None:
    record = _base_record()
    del record["prompt_hash"]
    errors = v2.validate_cell_record(record)
    assert any(e.startswith("missing_field:prompt_hash") for e in errors)


def test_schema_rejects_null_gate_instead_of_not_applicable() -> None:
    record = _base_record(g3a_required_api=None)
    errors = v2.validate_cell_record(record)
    assert any("g3a_required_api" in e for e in errors)


def test_schema_rejects_illegal_validity() -> None:
    record = _base_record(outcome_validity="SUSPECTED_INVALID")
    errors = v2.validate_cell_record(record)
    assert any("illegal_outcome_validity" in e for e in errors)


def test_schema_rejects_illegal_mechanism_tag() -> None:
    record = _base_record(mechanism_tags=["not_a_real_tag"])
    errors = v2.validate_cell_record(record)
    assert any("illegal_mechanism_tag" in e for e in errors)


def test_schema_assert_raises() -> None:
    with pytest.raises(v2.CellRecordSchemaError):
        v2.assert_valid_cell_record(_base_record(outcome_validity="NOPE"))


def test_build_v2_fields_roundtrip_valid() -> None:
    classification = v2.classify_cell(
        {
            "g1_parse": "PASS",
            "g2_execution": "PASS",
            "g3_contract": "FAIL",
            "g4_correctness": "NOT_ASSESSED",
        },
        {
            "infrastructure_valid": True,
            "raw_response_present": True,
            "schema_explicit_in_prompt": True,
        },
    )
    record = v2.build_v2_fields_from_classification(
        classification,
        dataset="CE115",
        task_id="ce111_q02_polynomial_division_remainder",
        model="qwen3.5:4b",
        condition="ab1",
        seed=2026071301,
        prompt_hash="sha256:p",
        evaluator_hash="sha256:e",
        evaluation_revision="none",
        infrastructure_valid=True,
        raw_response_present=True,
        candidate_present=True,
        failure_subtype="OUTPUT_PACKAGING",
    )
    assert v2.validate_cell_record(record) == []
    assert record["primary_failure_layer"] == "L2"
