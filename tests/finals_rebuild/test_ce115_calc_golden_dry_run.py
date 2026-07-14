"""Milestone 2C — no-model infrastructure dry run for corrected CE115 calc L1."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from agent_tools.finals_rebuild.ce115_calc_golden_dry_run import (
    MODEL_TAG,
    RUN_TYPE,
    path_is_formal_results_dir,
    record_eligible_for_formal_analysis,
    run_golden_dry_run,
    write_dry_run_summary,
)
from agent_tools.finals_rebuild.ce115_calc_golden_generators import (
    FORMAL_L1_TASK_IDS,
    build_golden_return,
    formal_l1_tasks,
)
from agent_tools.finals_rebuild.generator_success import PASS, serialize_artifact
from agent_tools.finals_rebuild.math_boundary_pilot import build_ab1_prompt, build_ab2g_prompt, frozen_payloads
from agent_tools.finals_rebuild.math_answer_contracts import render_answer_contract

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "run_ce115_calc_golden_dry_run.py"
DRY_RUN_MODULE = ROOT / "agent_tools" / "finals_rebuild" / "ce115_calc_golden_dry_run.py"
GATE_NAMES = (
    "g1_evaluability",
    "g2_executability",
    "g3_contract_compliance",
    "g4_semantic_correctness",
    "g5_problem_presentation",
    "g6_math_notation",
)


def test_script_and_module_have_no_model_clients():
    for path in (SCRIPT, DRY_RUN_MODULE):
        text = path.read_text(encoding="utf-8")
        for token in (
            "call_ollama",
            "OllamaHTTPError",
            "urllib.request",
            "import requests",
            "from requests",
            "http.client",
            "localhost:11434",
            "generativelanguage",
            "import ollama",
            "from ollama",
        ):
            assert token not in text, f"{path.name} must not contain {token}"
        assert "import google" not in text
        assert "from google" not in text


def test_golden_dry_run_produces_four_full_pass_observed_records(tmp_path):
    output = tmp_path / "ce115_calc_golden_dry_run.jsonl"
    records = run_golden_dry_run(output_path=output, run_id="pytest-dry-run")
    assert [record["task_id"] for record in records] == list(FORMAL_L1_TASK_IDS)
    assert len(records) == 4
    for record in records:
        assert record["run_type"] == RUN_TYPE
        assert record["included_in_formal_analysis"] is False
        assert record["model_called"] is False
        assert record["model_tag"] == MODEL_TAG
        assert record["request_count"] == 0
        assert record["retry_count"] == 0
        assert record["ledger_stage"] == "observed"
        assert record["pipeline_corrected"] is False
        assert record["post_healer"] is False
        assert isinstance(record["raw_first_attempt_output"], str) and "def generate" in record["raw_first_attempt_output"]
        assert isinstance(record["candidate_extracted"], str) and "def generate" in record["candidate_extracted"]
        assert isinstance(record["actual_question_text"], str) and record["actual_question_text"].strip()
        assert {name: record["evaluation_gates"][name]["status"] for name in GATE_NAMES} == {
            name: PASS for name in GATE_NAMES
        }
        assert record["composite_outcomes"] == {
            "technical_pass": PASS,
            "presentation_pass": PASS,
            "full_pass": PASS,
        }
        assert record["oracle_pass"] is True
        assert record["failure_category"] is None
        serialize_artifact(record)


def test_jsonl_round_trip_and_formal_exclusion(tmp_path):
    output = tmp_path / "dry_run.jsonl"
    summary = tmp_path / "dry_run_summary.md"
    records = run_golden_dry_run(output_path=output)
    write_dry_run_summary(records, summary)
    restored = [json.loads(line) for line in output.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert [row["task_id"] for row in restored] == list(FORMAL_L1_TASK_IDS)
    assert all(not record_eligible_for_formal_analysis(row) for row in restored)
    formal_dir = ROOT / "docs" / "experiments" / "results" / "should_not_exist.jsonl"
    assert path_is_formal_results_dir(formal_dir)
    with pytest.raises(ValueError, match="docs/experiments/results"):
        run_golden_dry_run(output_path=formal_dir)
    text = summary.read_text(encoding="utf-8")
    assert "synthetic: true" in text
    assert "no model: true" in text
    assert "excluded from formal analysis: true" in text


def test_no_pipeline_or_post_healer_records_emitted(tmp_path):
    records = run_golden_dry_run(output_path=tmp_path / "out.jsonl")
    assert all(record["ledger_stage"] == "observed" for record in records)
    assert not any(record.get("source_record_id") for record in records)
    assert not any(record["ledger_stage"] in {"pipeline_corrected", "post_healer"} for record in records)


def test_golden_sources_absent_from_prompt_assembly():
    tasks = formal_l1_tasks()
    for task_id in FORMAL_L1_TASK_IDS:
        task = tasks[task_id]
        returned = build_golden_return(task)
        frozen = frozen_payloads((task,), (2026071301,))[0]
        prompts = (
            build_ab1_prompt(task, frozen),
            build_ab2g_prompt(task, frozen),
            render_answer_contract(task, frozen["oracle_payload"]),
        )
        for prompt in prompts:
            assert returned["question_text"] not in prompt
            assert "ce115_calc_golden_generators" not in prompt
            assert "synthetic_golden_no_model" not in prompt
            assert "infrastructure_dry_run" not in prompt
