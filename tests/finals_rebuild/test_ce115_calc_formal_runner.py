"""Milestone 3D — frozen plan / formal confirmatory runner integration tests."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from agent_tools.finals_rebuild.ce115_calc_formal_runner import (
    FormalRunnerError,
    RECORD_STATE_EXECUTED,
    RECORD_STATE_PLANNED,
    assert_formal_runner_source_has_no_transport,
    build_local_confirmatory_plan,
    build_ollama_request_payload,
    build_planned_record,
    execute_cell,
    load_executed_cell_ids,
    record_eligible_for_formal_analysis,
    run_local_confirmatory,
    write_executed_record,
    verify_cell_prompt_integrity,
)
from agent_tools.finals_rebuild.ce115_calc_golden_generators import (
    build_golden_generate_source,
    formal_l1_tasks,
)
from agent_tools.finals_rebuild.ce115_calc_prompt_freeze import prompt_sha256
from agent_tools.finals_rebuild.ce115_calc_run_plan import load_manifest
from agent_tools.finals_rebuild.generator_success import serialize_artifact as gs_serialize
from agent_tools.finals_rebuild import math_boundary_pilot as pilot

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "docs" / "experiments" / "manifests" / "ce115_calc_main_experiment_manifest.json"
CLI = ROOT / "scripts" / "run_ce115_calc_local_confirmatory.py"
FORMAL_RUNNER = ROOT / "agent_tools" / "finals_rebuild" / "ce115_calc_formal_runner.py"


def _counting_transport(factory):
    state = {"calls": 0, "payloads": []}

    def transport(payload):
        state["calls"] += 1
        state["payloads"].append(payload)
        return factory(payload)

    transport.state = state  # type: ignore[attr-defined]
    return transport


@pytest.fixture(scope="module")
def plan():
    return build_local_confirmatory_plan(MANIFEST, repo_root=ROOT)


@pytest.fixture(scope="module")
def cells(plan):
    return plan["cells"]


@pytest.fixture(scope="module")
def manifest():
    return load_manifest(MANIFEST)


def test_formal_runner_source_has_no_transport_import():
    source = FORMAL_RUNNER.read_text(encoding="utf-8")
    assert_formal_runner_source_has_no_transport(source)
    assert "build_ab1_prompt" not in source
    assert "build_ab2g_prompt" not in source
    assert "build_ab2d_prompt" not in source


def test_formal_path_ignores_legacy_prompt_builders(cells, manifest, plan, monkeypatch):
    def _boom(*_a, **_k):
        raise AssertionError("legacy prompt builder must not be called")

    monkeypatch.setattr(pilot, "build_ab1_prompt", _boom)
    monkeypatch.setattr(pilot, "build_ab2g_prompt", _boom)
    monkeypatch.setattr(pilot, "build_ab2d_prompt", _boom)

    cell = cells[0]
    tasks = formal_l1_tasks()
    source = build_golden_generate_source(tasks[cell["task_id"]], seed=cell["seed"])

    def transport(_payload):
        return {"message": {"content": source}, "prompt_eval_count": 1, "eval_count": 2}

    row = execute_cell(
        cell,
        transport=transport,
        run_id="t",
        manifest=manifest,
        manifest_hash=plan["manifest_hash"],
        write_artifact=False,
    )
    assert row["record_state"] == RECORD_STATE_EXECUTED
    assert row["prompt_hash"] == cell["prompt_hash"]


def test_prompt_text_hash_matches_manifest(cells, manifest):
    hash_seed = manifest["prompt_hash_seed"]
    table = manifest["per_task_prompt_hashes"]
    for cell in cells:
        verify_cell_prompt_integrity(cell, manifest)
        assert prompt_sha256(cell["prompt_text"]) == cell["prompt_hash"]
        if cell["seed"] == hash_seed:
            assert cell["prompt_hash"] == table[cell["task_id"]][cell["prompt_condition"]]


def test_72_cell_order_deterministic(plan):
    again = build_local_confirmatory_plan(MANIFEST, repo_root=ROOT)
    assert [c["cell_id"] for c in plan["cells"]] == [c["cell_id"] for c in again["cells"]]
    assert len(plan["cells"]) == 72


def test_no_gemini_or_legacy(cells):
    for cell in cells:
        assert "gemini" not in cell["model_tag"].lower()
        assert not cell["task_id"].startswith("ce115_cr01_")


def test_request_payload_only_explicit_settings(cells):
    for cell in cells:
        payload = build_ollama_request_payload(cell)
        assert set(payload) == {"model", "messages", "stream", "think", "options"}
        assert payload["model"] == cell["model_tag"]
        assert payload["model"] in {"qwen3.5:4b", "qwen3.5:9b"}
        assert payload["messages"] == [{"role": "user", "content": cell["prompt_text"]}]
        assert payload["stream"] is False
        assert payload["think"] is False
        assert set(payload["options"]) == {"temperature", "seed"}
        assert payload["options"]["temperature"] == 0.0
        assert payload["options"]["seed"] == cell["seed"]
        for banned in ("top_p", "top_k", "presence_penalty", "num_predict", "thinking"):
            assert banned not in payload["options"]
            assert banned not in payload


def test_request_retry_healer_policy_on_records(cells, manifest, plan):
    cell = cells[0]

    def transport(_payload):
        return {"message": {"content": ""}}

    planned = build_planned_record(
        cell, run_id="r", manifest_hash=plan["manifest_hash"], git_commit=manifest["git_commit"]
    )
    assert planned["record_state"] == RECORD_STATE_PLANNED
    assert planned["request_count"] == 1
    assert planned["retry_count"] == 0
    assert planned["healer_enabled"] is False

    executed = execute_cell(
        cell,
        transport=transport,
        run_id="r",
        manifest=manifest,
        manifest_hash=plan["manifest_hash"],
    )
    assert executed["request_count"] == 1
    assert executed["retry_count"] == 0
    assert executed["healer_enabled"] is False


def test_planned_vs_executed_distinction(cells, manifest, plan):
    cell = cells[0]
    planned = build_planned_record(
        cell, run_id="r", manifest_hash=plan["manifest_hash"], git_commit=manifest["git_commit"]
    )
    assert planned["raw_first_attempt_output"] is None
    assert record_eligible_for_formal_analysis(planned) is False

    def transport(_payload):
        return {"message": {"content": ""}}

    executed = execute_cell(
        cell,
        transport=transport,
        run_id="r",
        manifest=manifest,
        manifest_hash=plan["manifest_hash"],
    )
    assert executed["record_state"] == RECORD_STATE_EXECUTED
    assert executed["raw_first_attempt_output"] == ""
    assert record_eligible_for_formal_analysis(executed) is True


def test_executed_success_has_g1_g6_and_composites(cells, manifest, plan):
    cell = next(c for c in cells if c["seed"] == 2026071301)
    tasks = formal_l1_tasks()
    source = build_golden_generate_source(tasks[cell["task_id"]], seed=cell["seed"])

    def transport(_payload):
        return {
            "message": {"content": source},
            "prompt_eval_count": 10,
            "eval_count": 20,
            "total_duration": 123,
        }

    row = execute_cell(
        cell,
        transport=transport,
        run_id="r",
        manifest=manifest,
        manifest_hash=plan["manifest_hash"],
    )
    assert row["outcome"] == "passed"
    gates = row["evaluation_gates"]
    for key in (
        "g1_evaluability",
        "g2_executability",
        "g3_contract_compliance",
        "g4_semantic_correctness",
        "g5_problem_presentation",
        "g6_math_notation",
    ):
        assert key in gates
        assert gates[key]["status"] in {"PASS", "FAIL", "NOT_ASSESSED", "NOT_OBSERVED"}
    assert isinstance(row["composite_outcomes"], dict)
    assert row["token_duration_diagnostics"]["eval_count"] == 20


def test_empty_response_keeps_first_attempt(cells, manifest, plan):
    calls = {"n": 0}

    def transport(_payload):
        calls["n"] += 1
        return {"message": {"content": ""}}

    row = execute_cell(
        cells[0],
        transport=transport,
        run_id="r",
        manifest=manifest,
        manifest_hash=plan["manifest_hash"],
    )
    assert calls["n"] == 1
    assert row["outcome"] == "empty_response"
    assert row["raw_first_attempt_output"] == ""
    assert row["retry_count"] == 0
    assert row["evaluation_gates"] is not None


def test_runtime_failure_keeps_first_attempt(cells, manifest, plan):
    calls = {"n": 0}
    bad = "def generate(level=1, **kwargs):\n    raise RuntimeError('boom')\n"

    def transport(_payload):
        calls["n"] += 1
        return {"message": {"content": bad}}

    row = execute_cell(
        cells[0],
        transport=transport,
        run_id="r",
        manifest=manifest,
        manifest_hash=plan["manifest_hash"],
    )
    assert calls["n"] == 1
    assert row["outcome"] == "runtime_failure"
    assert "boom" in (row["raw_first_attempt_output"] or "")
    assert row["retry_count"] == 0


def test_fail_cell_does_not_retry(cells, manifest, plan):
    calls = {"n": 0}

    def transport(_payload):
        calls["n"] += 1
        raise ConnectionError("simulated transport failure")

    row = execute_cell(
        cells[0],
        transport=transport,
        run_id="r",
        manifest=manifest,
        manifest_hash=plan["manifest_hash"],
    )
    assert calls["n"] == 1
    assert row["outcome"] == "infrastructure_failure"
    assert row["retry_count"] == 0
    assert row["request_count"] == 1


def test_duplicate_cell_id_and_existing_artifact_blocked(tmp_path, cells, manifest, plan):
    cell = dict(cells[0])
    out = tmp_path / cell["output_path"]
    out.parent.mkdir(parents=True, exist_ok=True)

    def transport(_payload):
        return {"message": {"content": ""}}

    row = execute_cell(
        cell,
        transport=transport,
        run_id="r",
        manifest=manifest,
        manifest_hash=plan["manifest_hash"],
        write_artifact=False,
    )
    write_executed_record(out, row)
    with pytest.raises(FormalRunnerError, match="already present|overwritten"):
        write_executed_record(out, row)

    other = dict(row)
    other["cell_id"] = cell["cell_id"] + "__other"
    with pytest.raises(FormalRunnerError, match="overwritten"):
        write_executed_record(out, other)


def test_partial_run_resume_skips_executed(tmp_path, monkeypatch):
    root_plan = build_local_confirmatory_plan(MANIFEST, repo_root=ROOT)
    cells_local = []
    for cell in root_plan["cells"][:3]:
        c = dict(cell)
        c["output_path"] = f"docs/experiments/results/ce115_calc_local_confirmatory/{c['cell_id']}.jsonl"
        c["output_path_abs"] = str(tmp_path / c["output_path"])
        cells_local.append(c)

    results_dir = tmp_path / "docs/experiments/results/ce115_calc_local_confirmatory"
    results_dir.mkdir(parents=True, exist_ok=True)

    calls = {"n": 0}

    def transport(_payload):
        calls["n"] += 1
        return {"message": {"content": ""}}

    man = load_manifest(MANIFEST)
    first = execute_cell(
        cells_local[0],
        transport=transport,
        run_id="r",
        manifest=man,
        manifest_hash=root_plan["manifest_hash"],
        write_artifact=True,
        results_root=tmp_path,
    )
    assert first["cell_id"] == cells_local[0]["cell_id"]
    assert calls["n"] == 1
    assert cells_local[0]["cell_id"] in load_executed_cell_ids(results_dir)

    def fake_plan(*_a, **_k):
        return {
            **root_plan,
            "cells": cells_local,
            "planned_cells": len(cells_local),
            "manifest_hash": root_plan["manifest_hash"],
        }

    monkeypatch.setattr(
        "agent_tools.finals_rebuild.ce115_calc_formal_runner.build_local_confirmatory_plan",
        fake_plan,
    )
    monkeypatch.setattr(
        "agent_tools.finals_rebuild.ce115_calc_formal_runner.assert_cell_distribution",
        lambda _cells: None,
    )
    monkeypatch.setattr(
        "agent_tools.finals_rebuild.ce115_calc_formal_runner.assert_cross_model_prompt_identity",
        lambda _cells: None,
    )
    monkeypatch.setattr(
        "agent_tools.finals_rebuild.ce115_calc_formal_runner.assert_output_path_safety",
        lambda *_a, **_k: [],
    )

    before = calls["n"]
    result = run_local_confirmatory(
        MANIFEST,
        transport=transport,
        repo_root=tmp_path,
        write_artifacts=True,
        resume=True,
        results_dir=results_dir,
        cell_limit=10,
    )
    assert result["skipped_executed_cells"] == 1
    assert calls["n"] - before == 2
    assert result["transport_calls"] == 2


def test_formal_analysis_loader_excludes_planned(cells, plan, manifest):
    planned = build_planned_record(
        cells[0], run_id="r", manifest_hash=plan["manifest_hash"], git_commit=manifest["git_commit"]
    )
    assert record_eligible_for_formal_analysis(planned) is False

    def transport(_payload):
        return {"message": {"content": ""}}

    executed = execute_cell(
        cells[0],
        transport=transport,
        run_id="r",
        manifest=manifest,
        manifest_hash=plan["manifest_hash"],
    )
    assert record_eligible_for_formal_analysis(executed) is True


def test_jsonl_round_trip(tmp_path, cells, manifest, plan):
    def transport(_payload):
        return {"message": {"content": ""}}

    row = execute_cell(
        cells[0],
        transport=transport,
        run_id="r",
        manifest=manifest,
        manifest_hash=plan["manifest_hash"],
    )
    path = tmp_path / "one.jsonl"
    write_executed_record(path, row)
    restored = json.loads(path.read_text(encoding="utf-8").splitlines()[0])
    assert restored["cell_id"] == row["cell_id"]
    assert restored["record_state"] == RECORD_STATE_EXECUTED
    again = json.loads(gs_serialize(restored))
    assert again["prompt_hash"] == row["prompt_hash"]


def test_fake_transport_call_count_matches_executed():
    transport = _counting_transport(lambda _p: {"message": {"content": ""}})
    result = run_local_confirmatory(
        MANIFEST,
        transport=transport,
        repo_root=ROOT,
        write_artifacts=False,
        cell_limit=5,
        resume=False,
    )
    assert result["executed_cells"] == 5
    assert transport.state["calls"] == 5
    assert result["model_calls"] == 5
    assert result["planned_cells"] == 72


def test_cell_ids_filter_executes_exactly_one(cells):
    target = cells[0]["cell_id"]
    transport = _counting_transport(lambda _p: {"message": {"content": ""}})
    result = run_local_confirmatory(
        MANIFEST,
        transport=transport,
        repo_root=ROOT,
        write_artifacts=False,
        cell_ids={target},
        cell_limit=1,
        resume=False,
    )
    assert result["selected_cells"] == 1
    assert result["executed_cells"] == 1
    assert result["model_calls"] == 1
    assert result["cell_ids"] == [target]
    assert transport.state["calls"] == 1


def test_cell_ids_unknown_raises():
    transport = _counting_transport(lambda _p: {"message": {"content": ""}})
    with pytest.raises(FormalRunnerError, match="unknown cell_id"):
        run_local_confirmatory(
            MANIFEST,
            transport=transport,
            repo_root=ROOT,
            write_artifacts=False,
            cell_ids={"not_a_real_cell"},
            resume=False,
        )


def test_cli_plan_only_model_calls_zero():
    source = CLI.read_text(encoding="utf-8")
    assert "call_ollama" not in source
    assert "math_boundary_pilot" not in source
    assert "from agent_tools.finals_rebuild.ce115_calc_run_plan import" in source

    proc = subprocess.run(
        [
            sys.executable,
            str(CLI),
            "--manifest",
            str(MANIFEST),
            "--local-confirmatory",
            "--plan-only",
        ],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0 or "existing_output_conflicts=" in proc.stdout
    assert "planned_cells=72" in proc.stdout
    assert "local_confirmatory_frozen=true" in proc.stdout
    assert "prompt_hash_mismatches=0" in proc.stdout
    assert "request_setting_mismatches=0" in proc.stdout
    assert "model_calls=0" in proc.stdout
    # After Milestone 3F smoke, one formal artifact may already exist → NOT READY.
    if "existing_output_conflicts=0" in proc.stdout:
        assert proc.returncode == 0
        assert "verdict=READY" in proc.stdout
    else:
        assert "verdict=NOT READY" in proc.stdout
        assert proc.returncode == 1


def test_payload_rejects_secret_fill_in(cells):
    bad = dict(cells[0])
    bad["top_p"] = 0.9
    with pytest.raises(FormalRunnerError):
        build_ollama_request_payload(bad)


def test_payload_requires_think_false(cells):
    bad = dict(cells[0])
    bad["thinking_requested"] = "not_explicitly_set"
    with pytest.raises(FormalRunnerError, match="thinking_requested=false"):
        build_ollama_request_payload(bad)
    good = build_ollama_request_payload(cells[0])
    assert good["think"] is False
    nine = next(c for c in cells if c["model_tag"] == "qwen3.5:9b")
    assert build_ollama_request_payload(nine)["think"] is False
