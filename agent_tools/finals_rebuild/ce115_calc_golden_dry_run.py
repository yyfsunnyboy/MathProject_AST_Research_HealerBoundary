"""No-model infrastructure dry run for corrected CE115 calc L1 tasks.

Uses tests/infrastructure golden generators + classify_response only.
Never calls Ollama, Gemini, HTTP, or any network client.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from agent_tools.finals_rebuild.ce115_calc_golden_generators import (
    FORMAL_L1_TASK_IDS,
    GOLDEN_SEED,
    build_golden_generate_source,
    build_golden_return,
    formal_l1_tasks,
)
from agent_tools.finals_rebuild.generator_success import merge_success_fields, serialize_artifact
from agent_tools.finals_rebuild.math_boundary_pilot import classify_response

RUN_TYPE = "infrastructure_dry_run"
MODEL_TAG = "synthetic_golden_no_model"
PROVIDER = "synthetic"
DEFAULT_RUN_ID = "ce115-calc-golden-dry-run"
FORMAL_RESULTS_RELATIVE = ("docs", "experiments", "results")


def assert_no_model_transport_imports() -> None:
    """Hard guard: this module must stay offline."""
    # Use dotted fragments carefully so the guard itself does not trip static scanners.
    forbidden = ("urllib", "requests", "aiohttp", "ollama", "generativeai")
    for name in forbidden:
        if name in globals():
            raise RuntimeError(f"model/network import leaked into dry-run module: {name}")


def path_is_formal_results_dir(path: Path) -> bool:
    parts = path.resolve().parts
    for index in range(len(parts) - len(FORMAL_RESULTS_RELATIVE) + 1):
        if parts[index:index + len(FORMAL_RESULTS_RELATIVE)] == FORMAL_RESULTS_RELATIVE:
            return True
    return False


def record_eligible_for_formal_analysis(record: dict[str, Any]) -> bool:
    """Shared exclusion gate for synthetic infrastructure dry-run records."""
    if record.get("included_in_formal_analysis") is False:
        return False
    if record.get("run_type") == RUN_TYPE:
        return False
    if record.get("model_called") is False and record.get("model_tag") == MODEL_TAG:
        return False
    return True


def build_dry_run_record(
    task: dict[str, Any],
    *,
    run_id: str = DEFAULT_RUN_ID,
    seed: int = GOLDEN_SEED,
) -> dict[str, Any]:
    source = build_golden_generate_source(task, seed=seed)
    returned = build_golden_return(task, seed=seed)
    frozen = {
        "task_id": task["task_id"],
        "oracle_type": task["oracle_type"],
        "oracle_payload": returned["oracle_payload"],
        "repeat_seed": seed,
    }
    outcome, candidate, details = classify_response(source, frozen, task)
    row: dict[str, Any] = {
        "task_id": task["task_id"],
        "run_id": run_id,
        "run_type": RUN_TYPE,
        "included_in_formal_analysis": False,
        "model_called": False,
        "model_tag": MODEL_TAG,
        "provider": PROVIDER,
        "request_count": 0,
        "retry_count": 0,
        "healer_enabled": False,
        "prompt_condition": "synthetic_golden_no_model",
        "seed": seed,
        "oracle_type": task["oracle_type"],
        "skill_id": task["skill_id"],
        "task_parameters": returned["oracle_payload"],
        "raw_first_attempt_output": source,
        "candidate_extracted": candidate,
        "parse_status": outcome,
        "evaluable": outcome not in {
            "empty_response", "catastrophic_truncation", "extraction_failure",
            "parse_minor", "missing_entry_point", "infrastructure_failure",
        },
        "oracle_pass": outcome == "passed",
        "failure_category": None if outcome == "passed" else outcome,
        "failure_detail": details.get("runtime_error") or details.get("parse_error") or details.get("oracle_error"),
        "oracle_expected": details.get("expected_answer"),
        "pipeline_corrected": False,
        "post_healer": False,
    }
    merge_success_fields(row, details)
    if row.get("ledger_stage") != "observed":
        raise ValueError(f"dry-run must remain observed; got {row.get('ledger_stage')!r}")
    serialize_artifact(row)
    return row


def run_golden_dry_run(
    *,
    output_path: Path,
    run_id: str = DEFAULT_RUN_ID,
    seed: int = GOLDEN_SEED,
) -> list[dict[str, Any]]:
    """Classify all formal L1 golden candidates and write excluded JSONL artifacts."""
    assert_no_model_transport_imports()
    output_path = Path(output_path)
    if path_is_formal_results_dir(output_path):
        raise ValueError(
            "refusing to write synthetic dry-run artifacts under docs/experiments/results"
        )
    tasks = formal_l1_tasks()
    records = [
        build_dry_run_record(tasks[task_id], run_id=run_id, seed=seed)
        for task_id in FORMAL_L1_TASK_IDS
    ]
    if [record["task_id"] for record in records] != list(FORMAL_L1_TASK_IDS):
        raise ValueError("dry-run task order drifted from formal L1 set")
    for record in records:
        if record["composite_outcomes"]["full_pass"] != "PASS":
            raise ValueError(f"dry-run full_pass failed for {record['task_id']}")
        if record_eligible_for_formal_analysis(record):
            raise ValueError(f"dry-run record incorrectly marked formal: {record['task_id']}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(serialize_artifact(record) + "\n")
    return records


def write_dry_run_summary(records: list[dict[str, Any]], summary_path: Path) -> None:
    if path_is_formal_results_dir(summary_path):
        raise ValueError("refusing to write dry-run summary under docs/experiments/results")
    full_pass = sum(record["composite_outcomes"]["full_pass"] == "PASS" for record in records)
    lines = [
        "# CE115 Calc Golden Infrastructure Dry Run",
        "",
        "- synthetic: true",
        "- no model: true",
        "- excluded from formal analysis: true",
        f"- run_type: {RUN_TYPE}",
        f"- model_tag: {MODEL_TAG}",
        f"- records: {len(records)}",
        f"- full PASS: {full_pass}/{len(records)}",
        f"- model/API calls: 0",
        "",
        "| task_id | full_pass | ledger_stage | model_called |",
        "|---|---|---|---|",
    ]
    for record in records:
        lines.append(
            f"| {record['task_id']} | {record['composite_outcomes']['full_pass']} | "
            f"{record['ledger_stage']} | {record['model_called']} |"
        )
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
