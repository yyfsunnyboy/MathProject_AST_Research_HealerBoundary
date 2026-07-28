import json
from pathlib import Path

import pytest

from scripts.preflight_math16_method2_all_cell import (
    FORBIDDEN_DECISION_FIELDS,
    JOURNAL_FIELDS,
    classify_transition,
    decide_eligibility,
    finalize_statuses,
    make_pre_evaluation_record,
    run_preflight,
)


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = (
    ROOT / "docs/experiments/manifests/math16_method2_all_cell_protocol_v1.json"
)


def test_zero_model_preflight_covers_all_320_cells_without_formal_replay():
    result = run_preflight(MANIFEST)
    assert result["expected_cells"] == 320
    assert result["eligibility_checked"] == 320
    assert result["raw_final_paths_distinct"] is True
    assert result["formal_replay_executed"] is False
    assert result["evaluator_executed"] is False
    assert result["model_calls"] == 0


def test_eligibility_api_has_no_baseline_status_or_evaluator_inputs():
    assert FORBIDDEN_DECISION_FIELDS == {
        "final_status",
        "baseline_final_status",
        "raw_status",
        "correct_answer",
        "classifier_outcome",
        "evaluator_result",
        "evaluation_gates",
    }
    decision = decide_eligibility("x = 1\n", {"frozen": {}})
    assert decision["eligibility_checked"] is True


def test_noneligible_final_source_is_byte_identical_to_raw_source():
    record = make_pre_evaluation_record(
        cell_identity={"cell_id": "synthetic"},
        raw_source="x = 1\n",
        eligibility={
            "eligibility_checked": True,
            "eligible": False,
            "rule_id": None,
            "rule_triggered": False,
        },
    )
    assert tuple(record) == JOURNAL_FIELDS
    assert record["source_changed"] is False
    assert record["raw_source_sha256"] == record["final_source_sha256"]


@pytest.mark.parametrize(
    ("raw_status", "final_status", "expected"),
    [
        ("FAILED", "PASSED", "verified_rescue"),
        ("PASSED", "FAILED", "regression"),
        ("PASSED", "PASSED", "preserved_pass"),
        ("FAILED", "FAILED", "still_failed"),
    ],
)
def test_transition_contract(raw_status, final_status, expected):
    assert classify_transition(raw_status, final_status) == expected
    base = {field: None for field in JOURNAL_FIELDS}
    result = finalize_statuses(
        base, raw_status=raw_status, final_status=final_status
    )
    assert result["transition"] == expected


def test_manifest_freezes_runner_journal_and_separate_sources():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["protocol_status"] == "FROZEN_NOT_EXECUTED"
    assert manifest["population"]["expected_cells"] == 320
    assert manifest["decision_order"] == [
        "extract_raw_source",
        "eligibility_all_cells",
        "healer_if_eligible",
        "freeze_final_source",
        "evaluate_raw_and_final_separately",
        "derive_transition",
    ]
    assert set(manifest["journal"]["required_fields"]) == set(JOURNAL_FIELDS)
    assert (
        manifest["outputs"]["raw_source_directory"]
        != manifest["outputs"]["final_source_directory"]
    )
