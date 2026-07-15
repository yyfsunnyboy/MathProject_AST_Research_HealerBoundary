"""Formal CE115 local confirmatory runner — frozen-plan driven, transport-injectable.

Prompt source of truth: cell.prompt_text from ce115_calc_run_plan expansion.
Legacy math_boundary_pilot prompt builders are never used on this path.

This module must not import Ollama/HTTP clients at module level. Live transport is
injected by the caller; classify_response is lazy-imported only inside execute_cell.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable, Mapping

from agent_tools.finals_rebuild.ce115_calc_golden_generators import formal_l1_tasks
from agent_tools.finals_rebuild.ce115_calc_prompt_freeze import prompt_sha256
from agent_tools.finals_rebuild.ce115_calc_run_plan import (
    DEFAULT_MANIFEST_REL,
    REPO_ROOT,
    UNSET_SENTINELS,
    assert_cell_distribution,
    assert_cross_model_prompt_identity,
    assert_output_path_safety,
    load_manifest,
    run_preflight,
)
from agent_tools.finals_rebuild.generator_success import (
    EXPERIMENT_NOT_RUN,
    merge_success_fields,
    serialize_artifact,
)
from agent_tools.finals_rebuild.math_task_sampler import sample_task_parameters

RUN_TYPE = "local_confirmatory"
RECORD_STATE_PLANNED = "planned"
RECORD_STATE_EXECUTED = "executed"

Transport = Callable[[dict[str, Any]], dict[str, Any]]


class FormalRunnerError(RuntimeError):
    """Blocking formal runner integrity / I/O failure."""


def build_local_confirmatory_plan(
    manifest_path: Path | str | None = None,
    *,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    """Expand and validate the frozen 72-cell plan (no model calls)."""
    return run_preflight(manifest_path, repo_root=repo_root, write_results=False)


def verify_cell_prompt_integrity(cell: Mapping[str, Any], manifest: Mapping[str, Any]) -> None:
    recomputed = prompt_sha256(cell["prompt_text"])
    if recomputed != cell["prompt_hash"]:
        raise FormalRunnerError(
            f"sha256(prompt_text) != cell.prompt_hash for {cell['cell_id']}: "
            f"{recomputed} != {cell['prompt_hash']}"
        )
    hash_seed = int(manifest.get("prompt_hash_seed", -1))
    if cell["seed"] == hash_seed:
        expected = manifest["per_task_prompt_hashes"][cell["task_id"]][cell["prompt_condition"]]
        if cell["prompt_hash"] != expected:
            raise FormalRunnerError(
                f"cell.prompt_hash != manifest hash for {cell['cell_id']}: "
                f"{cell['prompt_hash']} != {expected}"
            )


def build_ollama_request_payload(cell: Mapping[str, Any]) -> dict[str, Any]:
    """Chat payload with only explicitly set generation options.

    Formal Qwen3.5 policy: top-level ``think: false``. Fields declared
    ``not_explicitly_set`` must be omitted — never filled from model defaults.
    """
    if cell.get("temperature") != 0.0:
        raise FormalRunnerError(f"unexpected temperature: {cell.get('temperature')!r}")
    thinking = cell.get("thinking_requested")
    if thinking is not False:
        raise FormalRunnerError(
            f"formal confirmatory cells require thinking_requested=false; got {thinking!r}"
        )
    options: dict[str, Any] = {
        "temperature": 0.0,
        "seed": int(cell["seed"]),
    }
    for name in ("top_p", "top_k", "presence_penalty", "num_predict"):
        value = cell.get(name)
        if value in UNSET_SENTINELS or value is None:
            continue
        raise FormalRunnerError(
            f"{name} is set on confirmatory cell but formal payload forbids undeclared values: {value!r}"
        )

    payload = {
        "model": cell["model_tag"],
        "messages": [{"role": "user", "content": cell["prompt_text"]}],
        "stream": False,
        "think": False,
        "options": options,
    }
    forbidden_options = {"think", "thinking", "top_p", "top_k", "presence_penalty", "num_predict"}
    leaking = forbidden_options.intersection(options)
    if leaking:
        raise FormalRunnerError(f"forbidden keys in options: {sorted(leaking)}")
    if payload.get("think") is not False:
        raise FormalRunnerError("payload.think must be false")
    if "top_p" in payload or "top_k" in payload or "presence_penalty" in payload:
        raise FormalRunnerError("unset sampling knobs leaked into top-level payload")
    return payload


def build_planned_record(
    cell: Mapping[str, Any],
    *,
    run_id: str,
    manifest_hash: str,
    git_commit: str,
) -> dict[str, Any]:
    """Planned (not yet executed) observed-ledger placeholder."""
    return {
        "record_state": RECORD_STATE_PLANNED,
        "run_type": RUN_TYPE,
        "run_id": run_id,
        "cell_id": cell["cell_id"],
        "task_id": cell["task_id"],
        "prompt_condition": cell["prompt_condition"],
        "seed": cell["seed"],
        "model_tag": cell["model_tag"],
        "model_digest": cell["model_digest"],
        "manifest_hash": manifest_hash,
        "prompt_hash": cell["prompt_hash"],
        "git_commit": git_commit,
        "request_count": 1,
        "retry_count": 0,
        "first_attempt_is_ITT": True,
        "healer_enabled": False,
        "ledger_stage": "observed",
        "included_in_formal_analysis": True,
        "temperature": 0.0,
        "top_p": "not_explicitly_set",
        "top_k": "not_explicitly_set",
        "presence_penalty": "not_explicitly_set",
        "num_predict": "not_explicitly_set",
        "thinking_requested": False,
        "think": False,
        "raw_first_attempt_output": None,
        "candidate_extracted": None,
        "actual_question_text": None,
        "evaluation_gates": None,
        "composite_outcomes": None,
        "failure_category": None,
        "token_duration_diagnostics": None,
        "outcome": None,
        "observation_status": EXPERIMENT_NOT_RUN,
        "output_path": cell["output_path"],
    }


def record_eligible_for_formal_analysis(record: Mapping[str, Any]) -> bool:
    """Formal analysis loaders may only accept executed confirmatory records."""
    if record.get("record_state") != RECORD_STATE_EXECUTED:
        return False
    if record.get("run_type") != RUN_TYPE:
        return False
    if record.get("included_in_formal_analysis") is not True:
        return False
    if record.get("healer_enabled") is True:
        return False
    if int(record.get("request_count", -1)) != 1:
        return False
    if int(record.get("retry_count", -1)) != 0:
        return False
    return True


def load_existing_records(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def assert_output_writable(path: Path, *, cell_id: str) -> None:
    if not path.exists():
        return
    if path.is_dir():
        raise FormalRunnerError(f"output path is a directory: {path}")
    if path.stat().st_size == 0:
        return
    existing = load_existing_records(path)
    ids = [row.get("cell_id") for row in existing]
    if cell_id in ids:
        raise FormalRunnerError(f"cell_id already present in artifact (refuse overwrite): {cell_id}")
    raise FormalRunnerError(f"existing non-empty artifact would be overwritten: {path}")


def write_executed_record(path: Path, record: Mapping[str, Any]) -> None:
    if record.get("record_state") != RECORD_STATE_EXECUTED:
        raise FormalRunnerError("refusing to write non-executed record as formal result")
    cell_id = record["cell_id"]
    assert_output_writable(path, cell_id=cell_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_file() and path.stat().st_size > 0:
        raise FormalRunnerError(f"refuse append into conflicting artifact: {path}")
    path.write_text(serialize_artifact(dict(record)) + "\n", encoding="utf-8")


def load_executed_cell_ids(results_dir: Path) -> set[str]:
    found: set[str] = set()
    if not results_dir.is_dir():
        return found
    for path in sorted(results_dir.glob("*.jsonl")):
        for row in load_existing_records(path):
            if row.get("record_state") == RECORD_STATE_EXECUTED and row.get("cell_id"):
                found.add(str(row["cell_id"]))
    return found


def _extract_message_content(response: Mapping[str, Any]) -> str:
    message = response.get("message")
    if isinstance(message, dict) and isinstance(message.get("content"), str):
        return message["content"]
    if isinstance(response.get("response"), str):
        return response["response"]
    if isinstance(response.get("raw_text"), str):
        return response["raw_text"]
    raise FormalRunnerError("transport response missing message.content")


def _diagnostics_from_response(response: Mapping[str, Any]) -> dict[str, Any]:
    keys = (
        "prompt_eval_count",
        "eval_count",
        "total_duration",
        "load_duration",
        "prompt_eval_duration",
        "eval_duration",
    )
    return {key: response.get(key) for key in keys}


def execute_cell(
    cell: Mapping[str, Any],
    *,
    transport: Transport,
    run_id: str,
    manifest: Mapping[str, Any],
    manifest_hash: str,
    write_artifact: bool = False,
    results_root: Path | None = None,
) -> dict[str, Any]:
    """One-shot cell execution. Never retries. Never uses legacy prompt builders."""
    # Lazy import keeps module import graph free of Ollama transport for plan-only tools.
    from agent_tools.finals_rebuild.math_boundary_pilot import classify_response

    verify_cell_prompt_integrity(cell, manifest)
    payload = build_ollama_request_payload(cell)
    planned = build_planned_record(
        cell,
        run_id=run_id,
        manifest_hash=manifest_hash,
        git_commit=str(manifest["git_commit"]),
    )

    transport_error: str | None = None
    raw = ""
    diagnostics: dict[str, Any] | None = None
    try:
        response = transport(payload)
        raw = _extract_message_content(response)
        diagnostics = _diagnostics_from_response(response)
    except Exception as exc:  # noqa: BLE001 — preserve first-attempt record; no retry
        transport_error = f"{type(exc).__name__}: {exc}"
        raw = ""
        diagnostics = None

    tasks = formal_l1_tasks()
    task = tasks[cell["task_id"]]
    oracle_payload = sample_task_parameters(task, int(cell["seed"]))["oracle_payload"]
    frozen = {
        "task_id": cell["task_id"],
        "oracle_type": task["oracle_type"],
        "oracle_payload": oracle_payload,
        "repeat_seed": cell["seed"],
    }

    if transport_error is not None:
        outcome, candidate, details = classify_response("", frozen, task)
        outcome = "infrastructure_failure"
        candidate = None
        details = dict(details)
        details["runtime_error"] = transport_error
    else:
        outcome, candidate, details = classify_response(raw, frozen, task)

    executed = dict(planned)
    executed["record_state"] = RECORD_STATE_EXECUTED
    executed["raw_first_attempt_output"] = raw
    executed["candidate_extracted"] = candidate
    executed["outcome"] = outcome
    executed["failure_category"] = None if outcome == "passed" else outcome
    executed["token_duration_diagnostics"] = diagnostics
    executed["request_payload_options"] = payload["options"]
    executed["request_count"] = 1
    executed["retry_count"] = 0
    merge_success_fields(executed, details)
    for key in ("evaluation_gates", "composite_outcomes", "actual_question_text", "ledger_stage"):
        if key in details:
            executed[key] = details[key]
    if outcome == "passed":
        executed["observation_status"] = "observed_success"
    else:
        executed["observation_status"] = "generator_failure"
    if transport_error:
        executed["transport_error"] = transport_error

    if write_artifact:
        root = results_root or REPO_ROOT
        out_path = root / cell["output_path"]
        write_executed_record(out_path, executed)
    return executed


def run_local_confirmatory(
    manifest_path: Path | str | None = None,
    *,
    transport: Transport | None = None,
    run_id: str = "ce115_calc_local_confirmatory",
    repo_root: Path | None = None,
    write_artifacts: bool = False,
    cell_limit: int | None = None,
    resume: bool = True,
    results_dir: Path | None = None,
) -> dict[str, Any]:
    """Execute confirmatory cells from the frozen plan.

    ``transport`` is required. This function never imports a live Ollama client.
    """
    if transport is None:
        raise FormalRunnerError(
            "transport is required; live Ollama must be injected by caller "
            "(Milestone 3D forbids default model calls)"
        )
    root = repo_root or REPO_ROOT
    path = Path(manifest_path) if manifest_path is not None else root / DEFAULT_MANIFEST_REL
    plan = build_local_confirmatory_plan(path, repo_root=root)
    manifest = load_manifest(path)
    cells = list(plan["cells"])
    assert_cell_distribution(cells)
    assert_cross_model_prompt_identity(cells)
    if write_artifacts:
        assert_output_path_safety(cells, repo_root=root)

    out_dir = results_dir or (root / "docs" / "experiments" / "results" / "ce115_calc_local_confirmatory")
    executed_ids = load_executed_cell_ids(out_dir) if resume else set()

    rows: list[dict[str, Any]] = []
    transport_calls = 0
    skipped = 0
    for cell in cells:
        if cell["cell_id"] in executed_ids:
            skipped += 1
            continue
        if cell_limit is not None and transport_calls >= cell_limit:
            break
        row = execute_cell(
            cell,
            transport=transport,
            run_id=run_id,
            manifest=manifest,
            manifest_hash=plan["manifest_hash"],
            write_artifact=write_artifacts,
            results_root=root,
        )
        transport_calls += 1
        rows.append(row)
        if write_artifacts:
            executed_ids.add(cell["cell_id"])

    return {
        "run_id": run_id,
        "planned_cells": len(cells),
        "executed_cells": len(rows),
        "skipped_executed_cells": skipped,
        "transport_calls": transport_calls,
        "model_calls": transport_calls,
        "rows": rows,
        "manifest_hash": plan["manifest_hash"],
        "local_confirmatory_frozen": True,
        "cell_ids": [c["cell_id"] for c in cells],
    }


def assert_formal_runner_source_has_no_transport(source: str) -> None:
    snippets = (
        "urllib" + ".request",
        "import " + "requests",
        "import " + "httpx",
        "call_" + "ollama_chat",
        "Google" + "AIClient",
    )
    for snippet in snippets:
        if snippet in source:
            raise FormalRunnerError(f"transport leak in formal runner source: {snippet}")
