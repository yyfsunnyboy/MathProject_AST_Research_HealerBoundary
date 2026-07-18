"""Tests for 113/114 exam external-validation freeze (oracles + leakage + ablation)."""
from __future__ import annotations

import json
from pathlib import Path

from agent_tools.finals_rebuild.ce115_clean_incremental_ablation import (
    DOMAIN_BUDGET,
    TASK_DOMAIN_APIS,
    assert_clean_ablation_invariants,
    domain_section,
)
from agent_tools.finals_rebuild.ce115_exam_external_validation import (
    EXPECTED_ANSWERS,
    FROZEN_PAYLOADS,
    TASK_IDS,
    all_leakage_audits,
)
from agent_tools.finals_rebuild.math_task_oracles import evaluate_math_task_oracle
from agent_tools.finals_rebuild.math_task_sampler import sample_task_parameters

MANIFEST = Path("tests/finals_rebuild/fixtures/math_generation_tasks_ce115_pilot.jsonl")
SEED = 2026071301


def _load_exam_tasks() -> dict[str, dict]:
    rows = [
        json.loads(line)
        for line in MANIFEST.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    by_id = {row["task_id"]: row for row in rows}
    return {tid: by_id[tid] for tid in TASK_IDS}


def test_six_tasks_in_fixture_and_domain_map():
    loaded = _load_exam_tasks()
    for tid in TASK_IDS:
        assert tid in loaded
        assert tid in TASK_DOMAIN_APIS
        assert DOMAIN_BUDGET[0] <= len(domain_section(tid)) <= DOMAIN_BUDGET[1]


def test_sampler_identity_and_oracles():
    loaded = _load_exam_tasks()
    for tid in TASK_IDS:
        sampled = sample_task_parameters(loaded[tid], SEED)
        assert sampled["oracle_payload"] == FROZEN_PAYLOADS[tid]
        verdict = evaluate_math_task_oracle(
            loaded[tid]["oracle_type"], FROZEN_PAYLOADS[tid], EXPECTED_ANSWERS[tid]
        )
        assert verdict["is_correct"] is True
        assert verdict["expected_answer"] == EXPECTED_ANSWERS[tid]


def test_factorization_accepts_order_swap_not_string_only():
    tid = "ce115_ext_113_10_factorization_l1"
    payload = FROZEN_PAYLOADS[tid]
    swapped = {
        "factors": [
            {"x_coefficient": -15, "constant": 8},
            {"x_coefficient": 5, "constant": -2},
        ]
    }
    ok = evaluate_math_task_oracle("exam_factorization_common_binomial", payload, swapped)
    assert ok["is_correct"] is True
    wrong = evaluate_math_task_oracle(
        "exam_factorization_common_binomial",
        payload,
        {"factors": [{"x_coefficient": 5, "constant": -2}, {"x_coefficient": 1, "constant": 1}]},
    )
    assert wrong["is_correct"] is False


def test_leakage_audit_and_ablation_invariants():
    assert all_leakage_audits()["passed"] is True
    loaded = _load_exam_tasks()
    for tid in TASK_IDS:
        frozen = {
            "task_id": tid,
            "oracle_type": loaded[tid]["oracle_type"],
            "oracle_payload": FROZEN_PAYLOADS[tid],
            "repeat_seed": SEED,
        }
        prompts = assert_clean_ablation_invariants(loaded[tid], frozen)
        assert set(prompts) == {"ab1", "ab2g", "ab2d"}
        assert "## Clean-incremental GENERIC" not in prompts["ab1"]
        assert "## Clean-incremental DOMAIN" in prompts["ab2d"]
        assert "Preserve frozen parameters exactly" in prompts["ab2g"]
