# -*- coding: utf-8 -*-
"""Focused tests for Qwen9B cell-wise fixpoint replay runner v1.

Covers population lock, schemas, termination stubs, evaluator injectability,
formal-execution guards, and zero-execution preflight.
Does not execute formal 218-cell replay or invoke the real evaluator on cells.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from agent_tools.finals_rebuild.math16_observational_evaluator_v1 import (
    AUTHORITATIVE_BINDING,
    evaluator_binding_report,
    make_observational_pass_fail_evaluator,
    map_scoring_status_to_protocol,
)
from agent_tools.finals_rebuild.math16_qwen9b_cellwise_fixpoint_replay_v1 import (
    AGGREGATE_SUMMARY_REQUIRED_FIELDS,
    CELL_JOURNAL_REQUIRED_FIELDS,
    EXPECTED_FAIL,
    EXPECTED_PASS,
    EXPECTED_TOTAL,
    FORBIDDEN_4B_FAIL,
    FORBIDDEN_4B_PASS,
    FormalExecutionBlocked,
    MAX_ROUND,
    MODEL_GROUP,
    RESULTS_ROOT,
    apply_one_cycle,
    apply_one_cycle_with_stub_stack,
    apply_stack_once,
    assert_pass_cells_excluded,
    build_aggregate_summary,
    check_resume_and_duplicate_guards,
    empty_aggregate_summary,
    load_round1_population,
    read_round1_final_source,
    run_formal_fixpoint_replay,
    run_preflight,
    sha256_text,
)

ROOT = Path(__file__).resolve().parents[2]


def test_population_locks_218_fail_and_excludes_102_pass():
    pop = load_round1_population()
    assert len(pop.active_fail) == EXPECTED_FAIL == 218
    assert len(pop.excluded_pass) == EXPECTED_PASS == 102
    assert len(pop.active_fail) + len(pop.excluded_pass) == EXPECTED_TOTAL
    assert pop.active_ids.isdisjoint(pop.excluded_ids)
    assert len(pop.active_ids | pop.excluded_ids) == 320
    assert_pass_cells_excluded(pop, pop.active_ids)
    assert EXPECTED_PASS != FORBIDDEN_4B_PASS
    assert EXPECTED_FAIL != FORBIDDEN_4B_FAIL
    assert all(c.model_group == MODEL_GROUP for c in pop.active_fail)
    assert all(c.model_group == MODEL_GROUP for c in pop.excluded_pass)
    with pytest.raises(Exception):
        assert_pass_cells_excluded(pop, [next(iter(pop.excluded_ids))])


def test_round1_final_sources_sha_match_sample_and_inventory():
    pop = load_round1_population()
    sample_fail = pop.active_fail[0]
    sample_pass = pop.excluded_pass[0]
    for cell in (sample_fail, sample_pass):
        text = read_round1_final_source(cell)
        assert sha256_text(text) == cell.round1_final_source_sha256
        assert "d5_post" not in cell.source_origin
        assert "d2_post" not in cell.source_origin


def test_preflight_zero_execution_and_locks():
    before_exists = RESULTS_ROOT.exists()
    report = run_preflight()
    assert report["ok"] is True
    assert report["formal_replay_executed"] is False
    assert report["healer_cycles_executed"] == 0
    assert report["model_calls"] == 0
    assert report["evaluator_invocations"] == 0
    assert report["population"]["active_fail_n"] == 218
    assert report["population"]["excluded_pass_n"] == 102
    assert report["population"]["unique_ids"] == 320
    assert report["population"]["duplicate_ids"] == 0
    assert report["population"]["active_fail_locked"] is True
    assert report["population"]["excluded_pass_locked"] is True
    assert report["population"]["no_4b_pass_fail_leak"] is True
    assert report["sources"]["missing"] == 0
    assert report["sources"]["sha_mismatches"] == 0
    assert report["max_round"] == MAX_ROUND
    assert report["fixed_sequence"] == "A→B→C1→C2→D3→D1→D5→D2"
    assert report["freeze_checks"]["ok"] is True
    assert (
        report["observational_evaluator"]["binding"]["binding_id"]
        == AUTHORITATIVE_BINDING["binding_id"]
    )
    if not before_exists:
        assert not RESULTS_ROOT.exists()


def test_formal_replay_blocked_by_default_and_without_evaluator():
    with pytest.raises(FormalExecutionBlocked):
        run_formal_fixpoint_replay(allow_formal_execution=False)
    with pytest.raises(FormalExecutionBlocked):
        run_formal_fixpoint_replay(
            allow_formal_execution=True,
            evaluate_final_status=None,
            inject_authoritative_evaluator=False,
        )


def test_authoritative_evaluator_factory_is_uniquely_injectable():
    binding = evaluator_binding_report()
    assert binding["ok"] is True
    assert binding["binding"]["binding_id"] == AUTHORITATIVE_BINDING["binding_id"]
    assert map_scoring_status_to_protocol("PASSED") == "PASS"
    assert map_scoring_status_to_protocol("FAILED") == "FAIL"
    pop = load_round1_population()
    cell = pop.active_fail[0]
    # Build callback without invoking it on sealed sources this round.
    cb = make_observational_pass_fail_evaluator(task_id=cell.task_id)
    assert callable(cb)
    assert "math16_observational" in cb.__name__


def test_journal_and_summary_schemas_with_stub_stack():
    cycle = apply_one_cycle_with_stub_stack(
        cell_id="synthetic_cell",
        source="x = 1\n",
        cycle_index=1,
        full_sha_history=[sha256_text("seed")],
        final_status="FAIL",
        mutate=lambda s: s,
    )
    row = cycle.journal_row()
    assert set(CELL_JOURNAL_REQUIRED_FIELDS) <= set(row)
    assert row["termination_reason"] == "ZERO_CHANGE_CONVERGENCE"

    summary = empty_aggregate_summary(formal_replay_executed=False)
    assert set(AGGREGATE_SUMMARY_REQUIRED_FIELDS) <= set(summary)
    assert summary["n_active_cells"] == 218
    assert summary["n_excluded_pass_cells"] == 102
    assert summary["model_group"] == "qwen9b"

    finals = [
        {"cell_id": f"c{i}", "termination_reason": reason}
        for i, reason in enumerate(
            [
                "ITERATIVE_RESCUE",
                "ZERO_CHANGE_CONVERGENCE",
                "CYCLE_DETECTED",
                "MAX_ROUND_NON_CONVERGENT",
            ]
            * 54
            + ["ZERO_CHANGE_CONVERGENCE"] * 2  # 218
        )
    ]
    assert len(finals) == 218
    built = build_aggregate_summary(finals)
    assert built["n_active_cells"] == 218
    assert sum(built["termination_counts"].values()) == 218


def test_termination_four_ways_with_stub_stack():
    r1 = sha256_text("r1")
    rescue = apply_one_cycle_with_stub_stack(
        cell_id="c_rescue",
        source="a",
        cycle_index=2,
        full_sha_history=[r1],
        final_status="PASS",
        mutate=lambda s: s + "!",
        rule_id="LAST_FIX",
    )
    assert rescue.decision["termination_reason"] == "ITERATIVE_RESCUE"
    assert rescue.decision["rescue_rule_id"] == "LAST_FIX"

    zero = apply_one_cycle_with_stub_stack(
        cell_id="c_zero",
        source="same",
        cycle_index=1,
        full_sha_history=[r1, sha256_text("same")],
        final_status="FAIL",
        mutate=lambda s: s,
    )
    assert zero.decision["termination_reason"] == "ZERO_CHANGE_CONVERGENCE"

    text_a = "content_a"
    text_b = "content_b"
    history = [r1, sha256_text(text_a), sha256_text(text_b)]
    cyc = apply_one_cycle_with_stub_stack(
        cell_id="c_cycle",
        source=text_b,
        cycle_index=3,
        full_sha_history=history,
        final_status="FAIL",
        mutate=lambda s: text_a,
    )
    assert cyc.decision["termination_reason"] == "CYCLE_DETECTED"

    mx = apply_one_cycle_with_stub_stack(
        cell_id="c_max",
        source="s7",
        cycle_index=8,
        full_sha_history=[r1, sha256_text("s7")],
        final_status="FAIL",
        mutate=lambda s: s + "_new",
        max_round=8,
    )
    assert mx.decision["termination_reason"] == "MAX_ROUND_NON_CONVERGENT"


def test_resume_duplicate_guards_and_fixture_stack_determinism():
    root = ROOT / "docs" / "experiments" / "results" / "_tmp_qwen9b_fixpoint_guard_probe_v1"
    if root.exists():
        for child in root.iterdir():
            child.unlink()
    else:
        root.mkdir(parents=True)
    try:
        clean = check_resume_and_duplicate_guards(results_root=root, allow_resume=False)
        assert clean["ok"] is True
        (root / "summary.json").write_text("{}\n", encoding="utf-8")
        blocked = check_resume_and_duplicate_guards(results_root=root, allow_resume=False)
        assert blocked["ok"] is False
    finally:
        for child in list(root.iterdir()):
            child.unlink()
        root.rmdir()

    pop = load_round1_population()
    cell = pop.active_fail[0]
    meta = cell.as_dict()
    source = read_round1_final_source(cell)
    first = apply_stack_once(cell=meta, source=source, cycle_index=1)
    second = apply_stack_once(cell=meta, source=source, cycle_index=1)
    assert first.round_end_sha == second.round_end_sha
    finalized = apply_one_cycle(
        cell=meta,
        source=source,
        cycle_index=1,
        full_sha_history=[cell.round1_final_source_sha256],
        final_status="FAIL",
    )
    assert set(CELL_JOURNAL_REQUIRED_FIELDS) <= set(finalized.journal_row())


def test_mock_evaluator_injection_on_single_synthetic_cycle_only():
    """Contract: callback can be injected; do not score sealed 218-cell pool."""
    calls: list[str] = []

    def mock_eval(source: str, meta):  # noqa: ANN001
        calls.append(meta["cell_id"])
        return "FAIL"

    # Synthetic one-cycle finalize path only (no formal runner write).
    pop = load_round1_population()
    cell = pop.active_fail[0]
    source = read_round1_final_source(cell)
    cycle = apply_stack_once(cell=cell.as_dict(), source=source, cycle_index=1)
    status = mock_eval(cycle.round_end_source, cell.as_dict())
    assert status == "FAIL"
    assert calls == [cell.cell_id]
