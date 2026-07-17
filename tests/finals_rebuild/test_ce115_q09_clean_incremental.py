"""Tests for CE115 Q9 clean-incremental formal task freeze."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from agent_tools.finals_rebuild.ce115_clean_incremental_ablation import (
    LINEAGE_ID,
    TASK_DOMAIN_APIS,
    assert_clean_ablation_invariants,
    build_condition_prompt,
    extract_generic_section,
    generic_section,
    prompt_sha256,
)
from agent_tools.finals_rebuild.math_task_oracles import evaluate_math_task_oracle
from agent_tools.finals_rebuild.math_task_sampler import sample_task_parameters
from scripts import preflight_ce115_q09_clean_incremental as preflight

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "tests/finals_rebuild/fixtures/math_generation_tasks_ce115_pilot.jsonl"
TASK_ID = "ce115_calc_common_factor_quadratic_root_ordering_l1"
SEED = 2026071301
EXPECTED_FROZEN = {
    "shared_shift": 7,
    "leading_factor": 2,
    "subtracted_factor": 10,
    "root_order": "a>b",
    "linear_combination": {"a": 1, "b": 2},
}
EXPECTED_ANSWER = {"roots": [5, -7], "a": 5, "b": -7, "value": -9}


def _task() -> dict:
    rows = [json.loads(line) for line in MANIFEST.read_text(encoding="utf-8").splitlines() if line.strip()]
    return next(row for row in rows if row["task_id"] == TASK_ID)


def test_fixture_row_present_and_reconstructs_original():
    task = _task()
    assert task["skill_id"] == "common_factor_quadratic_root_ordering"
    assert task["oracle_type"] == "common_factor_quadratic_root_ordering"
    payload = sample_task_parameters(task, SEED)["oracle_payload"]
    assert payload == EXPECTED_FROZEN
    assert preflight.reconstruct_original_equation(payload) == "2x(x+7)-10(x+7)=0"


def test_oracle_computes_roots_ordering_and_value_without_hardcode():
    payload = EXPECTED_FROZEN
    verdict = evaluate_math_task_oracle("common_factor_quadratic_root_ordering", payload, EXPECTED_ANSWER)
    assert verdict["error"] is None
    assert verdict["expected_answer"] == EXPECTED_ANSWER
    assert verdict["is_correct"] is True
    # Wrong ordering / value rejected
    assert evaluate_math_task_oracle(
        "common_factor_quadratic_root_ordering",
        payload,
        {"roots": [-7, 5], "a": -7, "b": 5, "value": -9},
    )["is_correct"] is False
    assert evaluate_math_task_oracle(
        "common_factor_quadratic_root_ordering",
        payload,
        {"roots": [5, -7], "a": 5, "b": -7, "value": 3},
    )["is_correct"] is False


def test_clean_incremental_composition_and_shared_generic():
    task = _task()
    frozen = {
        "task_id": TASK_ID,
        "oracle_type": task["oracle_type"],
        "oracle_payload": sample_task_parameters(task, SEED)["oracle_payload"],
    }
    prompts = assert_clean_ablation_invariants(task, frozen)
    assert TASK_ID in TASK_DOMAIN_APIS
    assert extract_generic_section(prompts["ab2g"]) == generic_section()
    assert "FractionOps.create" in prompts["ab2d"]
    assert "FractionOps" not in prompts["ab2g"]
    assert "-9" not in prompts["ab1"]
    assert "roots" in prompts["ab1"] and "a>b" in prompts["ab1"]


def test_zero_model_preflight_passes(tmp_path):
    pf = preflight.preflight(tmp_path / "q09_preflight")
    assert pf["checks"]["real_model_calls"] == 0
    assert pf["checks"]["passed"] is True
    assert pf["checks"]["existing_three_not_included"] is True
    assert set(pf["canonical_prompt_hashes"]) == {"ab1", "ab2g", "ab2d"}
    for condition, digest in pf["canonical_prompt_hashes"].items():
        assert len(digest) == 64
        rebuilt = build_condition_prompt(
            condition,
            _task(),
            {
                "task_id": TASK_ID,
                "oracle_type": "common_factor_quadratic_root_ordering",
                "oracle_payload": EXPECTED_FROZEN,
            },
        )
        assert prompt_sha256(rebuilt) == digest
    assert pf["plan"]["prompt_lineage"] == LINEAGE_ID


def test_write_artifacts_keeps_real_model_calls_zero(tmp_path):
    out = tmp_path / "ce115_q09_clean_incremental_preflight_01"
    pf = preflight.preflight(out)
    preflight.write_preflight_artifacts(out, pf)
    summary = json.loads((out / "summary.json").read_text(encoding="utf-8"))
    checks = json.loads((out / "preflight.json").read_text(encoding="utf-8"))
    assert summary["real_model_calls"] == 0
    assert checks["real_model_calls"] == 0
    assert summary["safe_for_formal_model_pilot"] is True
    assert (out / "prompts" / "ab1.txt").exists()
    assert (out / "prompts" / "ab2g.txt").exists()
    assert (out / "prompts" / "ab2d.txt").exists()
