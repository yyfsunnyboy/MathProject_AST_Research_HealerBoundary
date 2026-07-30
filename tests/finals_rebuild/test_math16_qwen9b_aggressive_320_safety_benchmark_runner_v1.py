# -*- coding: utf-8 -*-
"""Focused tests for Qwen9B Aggressive 320-cell safety benchmark runner v1.

Covers population lock (320/102/218), schemas, transition stubs, dual-account
overlay helper, evaluator injectability, formal-execution guards, and
zero-execution preflight. Does not execute formal 320-cell benchmark.
"""
from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from agent_tools.finals_rebuild.math16_observational_evaluator_v1 import (
    AUTHORITATIVE_BINDING,
    evaluator_binding_report,
    make_observational_pass_fail_evaluator,
)
from agent_tools.finals_rebuild.math16_qwen9b_aggressive_320_safety_benchmark_v1 import (
    AGGREGATE_SUMMARY_REQUIRED_FIELDS,
    CELL_JOURNAL_REQUIRED_FIELDS,
    EXPECTED_FAIL,
    EXPECTED_PASS,
    EXPECTED_TOTAL,
    FormalExecutionBlocked,
    RESULTS_ROOT,
    SafetyBenchmarkProtocolError,
    assert_all_320_active,
    build_aggregate_summary,
    build_sealed_source_sensitivity,
    check_duplicate_and_formal_guards,
    empty_aggregate_summary,
    load_safety_population,
    read_round1_final_source,
    run_formal_safety_benchmark,
    run_one_cell_with_stub_stack,
    run_preflight,
    sha256_text,
)


def test_population_locks_all_320_including_pass_102():
    pop = load_safety_population()
    assert len(pop.cells) == EXPECTED_TOTAL == 320
    assert len(pop.pass_cells) == EXPECTED_PASS == 102
    assert len(pop.fail_cells) == EXPECTED_FAIL == 218
    assert len({c.cell_id for c in pop.cells}) == 320
    assert_all_320_active(pop, [c.cell_id for c in pop.cells])
    assert all(c.model_group == "qwen9b" for c in pop.cells)
    with pytest.raises(SafetyBenchmarkProtocolError):
        assert_all_320_active(pop, [c.cell_id for c in pop.cells][:-1])


def test_round1_sources_readable_for_pass_and_fail_samples():
    pop = load_safety_population()
    sample_pass = pop.pass_cells[0]
    sample_fail = pop.fail_cells[0]
    for cell in (sample_pass, sample_fail):
        text = read_round1_final_source(cell)
        assert sha256_text(text) == cell.round1_final_source_sha256


def test_preflight_zero_execution_and_locks():
    before_exists = RESULTS_ROOT.exists()
    report = run_preflight()
    assert report["ok"] is True
    assert report["formal_benchmark_executed"] is False
    assert report["healer_cells_executed"] == 0
    assert report["model_calls"] == 0
    assert report["evaluator_invocations"] == 0
    assert report["population"]["n_cells"] == 320
    assert report["population"]["n_input_pass"] == 102
    assert report["population"]["n_input_fail"] == 218
    assert report["population"]["unique_ids"] == 320
    assert report["population"]["duplicate_ids"] == 0
    assert report["population"]["total_locked"] is True
    assert report["population"]["no_4b_pass_fail_leak"] is True
    assert report["sources"]["missing"] == 0
    assert report["sources"]["sha_mismatches"] == 0
    assert report["fixed_sequence"] == "A→B→C1→C2→D3→D1→D5→D2"
    assert report["freeze_checks"]["ok"] is True
    assert (
        report["observational_evaluator"]["binding"]["binding_id"]
        == AUTHORITATIVE_BINDING["binding_id"]
    )
    if not before_exists:
        assert not RESULTS_ROOT.exists()


def test_formal_benchmark_blocked_by_default_and_without_evaluator():
    with pytest.raises(FormalExecutionBlocked):
        run_formal_safety_benchmark(allow_formal_execution=False)
    with pytest.raises(FormalExecutionBlocked):
        run_formal_safety_benchmark(
            allow_formal_execution=True,
            evaluate=None,
            inject_authoritative_evaluator=False,
        )


def test_authoritative_evaluator_factory_is_uniquely_injectable():
    binding = evaluator_binding_report()
    assert binding["ok"] is True
    pop = load_safety_population()
    cell = pop.cells[0]
    cb = make_observational_pass_fail_evaluator(task_id=cell.task_id)
    assert callable(cb)
    assert "math16_observational" in cb.__name__


def test_journal_and_summary_schemas_with_stub_transitions():
    stubs = [
        run_one_cell_with_stub_stack(
            cell_id="p_keep",
            input_status="PASS",
            source="ok",
            output_status="PASS",
            mutate=lambda s: s,
        ),
        run_one_cell_with_stub_stack(
            cell_id="p_reg",
            input_status="PASS",
            source="ok",
            output_status="FAIL",
            mutate=lambda s: s + "!",
        ),
        run_one_cell_with_stub_stack(
            cell_id="f_rescue",
            input_status="FAIL",
            source="bad",
            output_status="PASS",
            mutate=lambda s: s + "!",
        ),
        run_one_cell_with_stub_stack(
            cell_id="f_unchanged",
            input_status="FAIL",
            source="bad",
            output_status="FAIL",
            mutate=lambda s: s,
        ),
        run_one_cell_with_stub_stack(
            cell_id="f_mod",
            input_status="FAIL",
            source="bad",
            output_status="FAIL",
            mutate=lambda s: s + "!",
        ),
    ]
    rows = [s.journal_row() for s in stubs]
    for row in rows:
        assert set(CELL_JOURNAL_REQUIRED_FIELDS) <= set(row)
    assert rows[0]["transition"] == "preserved_pass"
    assert rows[1]["transition"] == "regression"
    assert rows[2]["transition"] == "verified_rescue"
    assert rows[3]["transition"] == "unchanged_fail"
    assert rows[4]["transition"] == "modified_still_failed"

    padded = []
    for i in range(EXPECTED_TOTAL):
        base = rows[i % 5]
        padded.append({**base, "cell_id": f"c{i:03d}"})
    summary = empty_aggregate_summary(formal_benchmark_executed=False)
    assert set(AGGREGATE_SUMMARY_REQUIRED_FIELDS) <= set(summary)
    assert summary["n_input_pass"] == 102
    assert summary["n_input_fail"] == 218
    assert summary["model_group"] == "qwen9b"

    built = build_aggregate_summary(padded)
    assert built["n_cells"] == 320
    assert sum(built["transition_counts"].values()) == 320
    assert built["net_pass_change"] == built["verified_rescue_n"] - built["regression_n"]
    assert abs(built["rescue_rate"] - built["verified_rescue_n"] / 218) < 1e-12
    assert abs(built["regression_rate"] - built["regression_n"] / 102) < 1e-12


def test_sealed_source_sensitivity_overlay_does_not_rewrite_primary():
    primary = []
    reval = {}
    for i in range(EXPECTED_TOTAL):
        # One synthetic mismatch: frozen PASS but revalidated FAIL on cell 0.
        frozen = "PASS" if i < 102 else "FAIL"
        primary.append(
            {
                "cell_id": f"c{i:03d}",
                "input_status": frozen,
                "output_status": frozen,
                "source_changed": False,
                "modified": False,
                "transition": "preserved_pass" if frozen == "PASS" else "unchanged_fail",
            }
        )
        reval[f"c{i:03d}"] = "FAIL" if i == 0 else frozen
    overlay = build_sealed_source_sensitivity(
        primary_rows=primary,
        revalidated_input_status_by_cell=reval,
    )
    assert overlay["label_source_mismatch_n"] == 1
    assert overlay["label_source_mismatch_cell_ids"] == ["c000"]
    assert overlay["n_input_pass"] == 101
    assert overlay["n_input_fail"] == 219
    # Primary row unchanged.
    assert primary[0]["input_status"] == "PASS"


def test_duplicate_guard_when_outputs_exist():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "results"
        root.mkdir()
        (root / "summary.json").write_text("{}\n", encoding="utf-8")
        blocked = check_duplicate_and_formal_guards(results_root=root, allow_resume=False)
        assert blocked["ok"] is False
        clear = check_duplicate_and_formal_guards(results_root=Path(tmp) / "empty")
        assert clear["ok"] is True
