# -*- coding: utf-8 -*-
"""Focused tests for Qwen4B cell-wise fixpoint replay runner v1.

Covers population lock, schemas, termination stubs, resume/duplicate guards,
determinism probe on one fixture cell, and zero-execution preflight.
Does not execute formal 232-cell replay.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from agent_tools.finals_rebuild.math16_qwen4b_cellwise_fixpoint_replay_v1 import (
    AGGREGATE_SUMMARY_REQUIRED_FIELDS,
    CELL_JOURNAL_REQUIRED_FIELDS,
    EXPECTED_FAIL,
    EXPECTED_PASS,
    FixpointProtocolError,
    FormalExecutionBlocked,
    MAX_ROUND,
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


def test_population_locks_232_fail_and_excludes_88_pass():
    pop = load_round1_population()
    assert len(pop.active_fail) == EXPECTED_FAIL == 232
    assert len(pop.excluded_pass) == EXPECTED_PASS == 88
    assert pop.active_ids.isdisjoint(pop.excluded_ids)
    assert_pass_cells_excluded(pop, pop.active_ids)
    with pytest.raises(FixpointProtocolError):
        assert_pass_cells_excluded(pop, [next(iter(pop.excluded_ids))])


def test_round1_final_sources_readable_for_overrides_and_sample():
    pop = load_round1_population()
    overrides = [
        c
        for c in pop.active_fail
        if c.source_origin in {"d5_post", "d2_post"}
    ]
    assert len(overrides) == 2
    for cell in overrides:
        text = read_round1_final_source(cell)
        assert sha256_text(text) == cell.round1_final_source_sha256
    # Sample a non-override FAIL cell.
    sample = next(c for c in pop.active_fail if c.source_origin not in {"d5_post", "d2_post"})
    text = read_round1_final_source(sample)
    assert sha256_text(text) == sample.round1_final_source_sha256


def test_preflight_zero_execution_and_locks():
    report = run_preflight()
    assert report["ok"] is True
    assert report["formal_replay_executed"] is False
    assert report["healer_cycles_executed"] == 0
    assert report["model_calls"] == 0
    assert report["population"]["active_fail_n"] == 232
    assert report["population"]["excluded_pass_n"] == 88
    assert report["population"]["active_fail_locked"] is True
    assert report["population"]["excluded_pass_locked"] is True
    assert report["sources"]["missing"] == 0
    assert report["sources"]["sha_mismatches"] == 0
    assert report["max_round"] == MAX_ROUND
    assert report["fixed_sequence"] == "A→B→C1→C2→D3→D1→D5→D2"
    assert report["freeze_checks"]["ok"] is True


def test_formal_replay_blocked_by_default():
    with pytest.raises(FormalExecutionBlocked):
        run_formal_fixpoint_replay(allow_formal_execution=False)


def test_journal_and_summary_schemas():
    cycle = apply_one_cycle_with_stub_stack(
        cell_id="synthetic_cell",
        source="x = 1\n",
        cycle_index=1,
        full_sha_history=[sha256_text("seed")],
        final_status="FAIL",
        mutate=lambda s: s,  # zero change
    )
    row = cycle.journal_row()
    assert set(CELL_JOURNAL_REQUIRED_FIELDS) <= set(row)
    assert row["termination_reason"] == "ZERO_CHANGE_CONVERGENCE"

    summary = empty_aggregate_summary(formal_replay_executed=False)
    assert set(AGGREGATE_SUMMARY_REQUIRED_FIELDS) <= set(summary)

    finals = [
        {
            "cell_id": f"c{i}",
            "termination_reason": reason,
        }
        for i, reason in enumerate(
            [
                "ITERATIVE_RESCUE",
                "ZERO_CHANGE_CONVERGENCE",
                "CYCLE_DETECTED",
                "MAX_ROUND_NON_CONVERGENT",
            ]
            * 58  # 232
        )
    ]
    built = build_aggregate_summary(finals)
    assert built["n_active_cells"] == 232
    assert sum(built["termination_counts"].values()) == 232


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
    assert rescue.decision["rescue_cycle"] == 2

    zero = apply_one_cycle_with_stub_stack(
        cell_id="c_zero",
        source="same",
        cycle_index=1,
        full_sha_history=[r1, sha256_text("same")],
        final_status="FAIL",
        mutate=lambda s: s,
    )
    assert zero.decision["termination_reason"] == "ZERO_CHANGE_CONVERGENCE"
    assert zero.decision["cycle_detected"] is False

    hist = [r1, "sha_a", "sha_b"]
    # Force SHAs via mutate that returns known content mapping is hard; use judge path
    # through stub by crafting sources whose hashes collide with history.
    src_b = "content_b"
    # Build a mutate that returns content whose sha is already in history.
    # Put sha(text_a) into history then revisit.
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
    assert cyc.decision["cycle_detected"] is True
    assert cyc.decision["full_sha_history"] == history

    # Max round: new sha at cycle 8
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
    assert mx.decision["max_round_reached"] is True


def test_resume_duplicate_guards():
    # Keep probe under repo to avoid Windows Temp permission issues.
    root = ROOT / "docs" / "experiments" / "results" / "_tmp_fixpoint_guard_probe_v1"
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

        resumed = check_resume_and_duplicate_guards(results_root=root, allow_resume=True)
        assert resumed["ok"] is True
        (root / "formal_run.lock").write_text("running\n", encoding="utf-8")
        locked = check_resume_and_duplicate_guards(results_root=root, allow_resume=True)
        assert locked["ok"] is False
    finally:
        for child in list(root.iterdir()):
            child.unlink()
        root.rmdir()


def test_fixture_stack_determinism_one_active_cell():
    pop = load_round1_population()
    cell = pop.active_fail[0]
    meta = cell.as_dict()
    source = read_round1_final_source(cell)
    first = apply_stack_once(cell=meta, source=source, cycle_index=1)
    second = apply_stack_once(cell=meta, source=source, cycle_index=1)
    assert first.round_end_sha == second.round_end_sha
    assert first.source_changed == second.source_changed
    # Journal fields present after observational finalize.
    finalized = apply_one_cycle(
        cell=meta,
        source=source,
        cycle_index=1,
        full_sha_history=[cell.round1_final_source_sha256],
        final_status="FAIL",
    )
    row = finalized.journal_row()
    assert row["cell_id"] == cell.cell_id
    assert set(CELL_JOURNAL_REQUIRED_FIELDS) <= set(row)


def test_results_root_not_created_by_preflight():
    # Preflight must not create formal result artifacts.
    before = RESULTS_ROOT.exists()
    report = run_preflight()
    assert report["ok"] is True
    if not before:
        assert not RESULTS_ROOT.exists()
    else:
        # If directory somehow exists from prior work, still no new formal claim.
        assert report["formal_replay_executed"] is False
