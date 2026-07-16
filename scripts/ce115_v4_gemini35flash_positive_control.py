"""CE115 Ab2d Assembly v4 — Gemini 3.5 Flash single-cell positive control.

Reuses frozen v4 prompt / resolver / scanner / evaluator contracts.
Exactly one Gemini first-attempt model call. Zero retry/repair/Healer.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.ce115_v4_formal_cohort import (  # noqa: E402
    FORBIDDEN_PROMPT,
    PROTOCOL,
    REQUIRED_PROMPT,
    _evaluate_generated_code,
    _h,
    _mark,
    _render_formal_prompt,
)
from scripts.ce115_v4_gemini_transport import (  # noqa: E402
    MODEL_ID,
    api_key_status,
    assert_no_key_leak,
    build_redacted_request,
    call_gemini_once,
    runtime_version,
)

SOURCE_COHORT = ROOT / "docs/experiments/results/ce115_ab2d_assembly_v4_formal_run"
DEFAULT_OUT = (
    ROOT
    / "docs/experiments/results/ce115_ab2d_assembly_v4_gemini35flash_positive_control_01"
)
EXPECTED_PROTOCOL_HASH = "1b86e94b291803b0aa1987af7d728ada756a183bf0bf2039a1563a47a7d70897"
SOURCE_SEQUENCE = 13
SOURCE_EDGE_MODEL = "qwen3.5:9b"


def _write_json(path: Path, obj: object) -> None:
    text = json.dumps(obj, indent=2, default=str) + "\n"
    assert_no_key_leak(text)
    path.write_text(text, encoding="utf8")


def _source_edge_cell() -> dict:
    plan = json.loads((SOURCE_COHORT / "frozen_formal_run_plan.json").read_text(encoding="utf8"))
    matches = [c for c in plan["cells"] if c["sequence"] == SOURCE_SEQUENCE]
    if len(matches) != 1:
        raise RuntimeError(f"source sequence {SOURCE_SEQUENCE} not unique")
    cell = matches[0]
    if cell["model"] != SOURCE_EDGE_MODEL:
        raise RuntimeError(f"source model mismatch: {cell['model']}")
    if cell["task_family"] != "polynomial":
        raise RuntimeError(f"source family mismatch: {cell['task_family']}")
    if int(cell["seed"]) != 2026071301:
        raise RuntimeError(f"source seed mismatch: {cell['seed']}")
    return cell


def _source_edge_artifact(cell_id: str) -> dict:
    path = SOURCE_COHORT / f"{cell_id}.artifact.json"
    if not path.is_file():
        raise RuntimeError(f"missing source artifact: {path}")
    return json.loads(path.read_text(encoding="utf8"))


def build_run_plan() -> dict:
    edge = _source_edge_cell()
    cell = {
        "cell_id": (
            "gemini_3_5_flash__ce115_calc_polynomial_division_l1__"
            "ab2d_assembly_v4_positive_control__seed_2026071301"
        ),
        "source_sequence": SOURCE_SEQUENCE,
        "source_edge_cell_id": edge["cell_id"],
        "source_edge_model": edge["model"],
        "model": MODEL_ID,
        "task": edge["task"],
        "task_family": edge["task_family"],
        "family": edge["task_family"],
        "seed": edge["seed"],
        "condition": "ab2d_assembly_v4",
        "max_model_calls": 1,
        "retry": 0,
        "resume": 0,
        "replacement": 0,
        "replay": 0,
        "repair": 0,
        "healer": 0,
    }
    body = {
        "run_id": "ce115_ab2d_assembly_v4_gemini35flash_positive_control_01",
        "condition": "ab2d_assembly_v4",
        "protocol_id": "ce115_ab2d_assembly_protocol_v4",
        "source_cohort": str(SOURCE_COHORT.relative_to(ROOT)).replace("\\", "/"),
        "source_sequence": SOURCE_SEQUENCE,
        "planned_cells": 1,
        "model_calls_planned": 1,
        "resume": False,
        "no_overwrite": True,
        "cells": [cell],
    }
    body["hash"] = _h(json.dumps({k: v for k, v in body.items() if k != "hash"}, sort_keys=True))
    return body


def run_preflight(out: Path) -> dict:
    if out.exists():
        raise RuntimeError(f"refusing overwrite existing directory: {out}")

    protocol = json.loads(PROTOCOL.read_text(encoding="utf8"))
    protocol_hash = _h(PROTOCOL.read_text(encoding="utf8"))
    edge = _source_edge_cell()
    art = _source_edge_artifact(edge["cell_id"])
    plan = build_run_plan()
    cell = plan["cells"][0]

    prompt, frozen = _render_formal_prompt(cell["task"], int(cell["seed"]))
    if frozen != art.get("frozen_parameters"):
        raise RuntimeError("frozen parameters drifted from source seq 13 artifact")
    if prompt != art.get("exact_rendered_prompt"):
        raise RuntimeError("rendered prompt drifted from source seq 13 artifact")
    if cell["task"] != art.get("task_id"):
        raise RuntimeError("task id mismatch vs source artifact")

    from agent_tools.finals_rebuild.ce115_ab2d_assembly import (
        resolve_task_operations,
        runtime_toolbox_inventory,
    )

    inventory = runtime_toolbox_inventory()
    ops = resolve_task_operations(cell["task"], frozen)
    if ops["required"] != art.get("task_required_operations"):
        raise RuntimeError("required operations mismatch vs source artifact")
    if ops["acceptable_canonical_paths"] != art.get("acceptable_canonical_paths"):
        raise RuntimeError("acceptable canonical paths mismatch vs source artifact")

    prompt_ok = {
        "available_domain_apis": all(x in prompt for x in REQUIRED_PROMPT),
        "no_legacy": not any(x in prompt for x in FORBIDDEN_PROMPT),
        "inventory_consistent": all(
            x["canonical_name"] in prompt
            and x["signature"] in prompt
            and x["return_structure"] in prompt
            for x in inventory
        ),
        "output_contract": "generate(level=1, **kwargs)" in prompt,
        "no_edge_raw": (art.get("raw_model_response") or "___NEVER___") not in prompt,
        "no_edge_verdict_tokens": all(
            tok not in prompt
            for tok in ("EXECUTION_FAILURE", "ASSEMBLY_COMPLIANT", "NATURAL_COMPLETE")
        ),
        "no_evaluator_error_leak": "FractionOps" not in prompt
        or "has no attribute" not in prompt,
    }
    key = api_key_status()
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=30,
    )
    origin = subprocess.run(
        ["git", "rev-parse", "origin/main"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=30,
    )
    branch = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=30,
    )
    git_head = (head.stdout or "").strip()
    git_origin = (origin.stdout or "").strip()
    checks = {
        "repo_root": str(ROOT),
        "branch": (branch.stdout or "").strip(),
        "head": git_head,
        "origin_main": git_origin,
        "head_equals_origin_main": git_head == git_origin and bool(git_head),
        "protocol_status": protocol.get("status"),
        "protocol_status_ok": protocol.get("status") == "FROZEN_ZERO_MODEL_VALIDATED_V2",
        "protocol_hash": protocol_hash,
        "protocol_hash_ok": protocol_hash == EXPECTED_PROTOCOL_HASH,
        "source_sequence": SOURCE_SEQUENCE,
        "source_edge_cell_id": edge["cell_id"],
        "source_edge_completion": art.get("completion"),
        "source_edge_adoption": art.get("adoption_verdict"),
        "source_edge_evaluator": art.get("evaluator_verdict"),
        "source_matches_expected_edge": (
            art.get("completion") == "NATURAL_COMPLETE"
            and art.get("adoption_verdict") == "ASSEMBLY_COMPLIANT"
            and art.get("evaluator_verdict") == "EXECUTION_FAILURE"
        ),
        "output_dir_absent": not out.exists(),
        "planned_cells": plan["planned_cells"],
        "cell_id_unique": True,
        "family": cell["task_family"],
        "seed": cell["seed"],
        "max_model_calls": cell["max_model_calls"],
        "max_model_calls_ok": cell["max_model_calls"] == 1,
        "retry_resume_replacement_repair_replay_healer_disabled": all(
            int(cell[k]) == 0
            for k in ("retry", "resume", "replacement", "replay", "repair", "healer")
        ),
        "model_id": MODEL_ID,
        "model_id_ok": MODEL_ID == "gemini-3.5-flash",
        "prompt_checks": prompt_ok,
        "prompt_checks_passed": all(prompt_ok.values()),
        "task_params_match_source": frozen == art.get("frozen_parameters"),
        "prompt_match_source": prompt == art.get("exact_rendered_prompt"),
        "ops_match_source": ops["required"] == art.get("task_required_operations"),
        "runtime_version": runtime_version(),
        **key,
        "real_model_calls": 0,
        "run_plan_hash": plan["hash"],
        "prompt_hash": _h(prompt),
        "blocker": None,
    }
    if not checks["api_key_present"]:
        checks["blocker"] = "API_KEY_REQUIRED"
        checks["passed"] = False
        return checks

    checks["passed"] = all(
        [
            checks["head_equals_origin_main"],
            checks["protocol_status_ok"],
            checks["protocol_hash_ok"],
            checks["source_matches_expected_edge"],
            checks["output_dir_absent"],
            checks["max_model_calls_ok"],
            checks["retry_resume_replacement_repair_replay_healer_disabled"],
            checks["model_id_ok"],
            checks["prompt_checks_passed"],
            checks["task_params_match_source"],
            checks["prompt_match_source"],
            checks["ops_match_source"],
            checks["api_key_present"],
        ]
    )
    if not checks["passed"]:
        checks["blocker"] = "PREFLIGHT_FAILED"
        return checks

    out.mkdir(parents=True)
    _write_json(out / "frozen_run_plan.json", plan)
    (out / "exact_rendered_prompt.txt").write_text(prompt, encoding="utf8")
    _write_json(
        out / "protocol_and_plan_hashes.json",
        {
            "protocol_path": str(PROTOCOL.relative_to(ROOT)).replace("\\", "/"),
            "protocol_hash": protocol_hash,
            "run_plan_hash": plan["hash"],
            "prompt_hash": _h(prompt),
            "source_sequence": SOURCE_SEQUENCE,
            "source_edge_cell_id": edge["cell_id"],
        },
    )
    _write_json(out / "preflight_summary.json", checks)
    return checks


def run_cell(out: Path) -> dict:
    plan = json.loads((out / "frozen_run_plan.json").read_text(encoding="utf8"))
    cell = plan["cells"][0]
    cid = cell["cell_id"]
    intent_path = out / "call_intent.json"
    ledger_path = out / "model_call_ledger.json"
    raw_path = out / "raw_response.txt"
    code_path = out / "extracted_code.py"
    artifact_path = out / "cell_artifact.json"
    lifecycle_path = out / "lifecycle_provenance.json"
    payload_path = out / "request_payload_redacted.json"
    state_path = out / "system_state.json"

    if intent_path.exists() or artifact_path.exists() or raw_path.exists():
        raise RuntimeError("duplicate cell invocation refused")

    checkpoints: list = []
    model_calls = 0

    def persist_lifecycle(status: str):
        _write_json(
            lifecycle_path,
            {
                "cell_id": cid,
                "status": status,
                "checkpoints": checkpoints,
                "process_id": os.getpid(),
                "exit_provenance": {
                    "pid": os.getpid(),
                    "last_phase": checkpoints[-1]["phase"] if checkpoints else None,
                    "status": status,
                },
            },
        )

    _mark(checkpoints, "CELL_SELECTED", cid, source_sequence=cell["source_sequence"])
    try:
        if int(cell.get("max_model_calls", 1)) != 1:
            raise RuntimeError("max_model_calls must be 1")
        for flag in ("retry", "resume", "replacement", "replay", "repair", "healer"):
            if int(cell.get(flag, 0)) != 0:
                raise RuntimeError(f"{flag} must be disabled")
        if not api_key_status()["api_key_present"]:
            raise RuntimeError("API_KEY_REQUIRED")

        prompt, frozen = _render_formal_prompt(cell["task"], int(cell["seed"]))
        _mark(checkpoints, "PROMPT_RENDERED", cid)
        request = build_redacted_request(prompt, model=cell["model"])
        _write_json(payload_path, request)
        _mark(checkpoints, "PAYLOAD_BUILT", cid)

        intent = {
            "cell": cell,
            "phase": "CALL_INTENT",
            "timestamp": time.time(),
            "prompt_hash": _h(prompt),
            "payload_hash": _h(json.dumps(request, sort_keys=True)),
            "model": cell["model"],
            "api_key_source": "environment",
            "api_key_present": True,
            "model_calls_before": 0,
            "first_attempt_only": True,
            "retry": 0,
            "resume": 0,
            "replacement": 0,
            "replay": 0,
            "repair": 0,
            "healer": 0,
        }
        _write_json(intent_path, intent)
        _mark(checkpoints, "CALL_INTENT_PERSISTED", cid)
        ledger = [
            {
                "cell_id": cid,
                "request_number": 1,
                "status": "intent",
                "model": cell["model"],
                "retry": 0,
                "resume": 0,
                "replacement": 0,
                "replay": 0,
                "repair": 0,
                "healer": 0,
            }
        ]
        _write_json(ledger_path, ledger)
        persist_lifecycle("CALL_INTENT_PERSISTED")

        _mark(checkpoints, "TRANSPORT_ENTERED", cid)
        started = time.monotonic()
        transport = call_gemini_once(prompt, model=cell["model"])
        model_calls = 1  # counted only after transport returns a text body
        _mark(checkpoints, "TRANSPORT_RETURNED", cid)
        raw = transport["raw_text"]
        raw_path.write_text(raw, encoding="utf8")
        assert_no_key_leak(raw)
        _mark(checkpoints, "RAW_PERSISTED", cid)
        ledger[0]["status"] = "raw_persisted"
        _write_json(ledger_path, ledger)
        persist_lifecycle("RAW_PERSISTED")

        from agent_tools.finals_rebuild.ce115_ab2d_assembly import (
            resolve_task_operations,
            runtime_toolbox_inventory,
            scan_toolbox,
        )
        from agent_tools.finals_rebuild.extraction import extract_code

        extraction = extract_code(raw)
        code = extraction.extracted_code if extraction.extraction_status == "extracted" else None
        if code:
            code_path.write_text(code, encoding="utf8")
        ops = resolve_task_operations(cell["task"], frozen)
        _mark(checkpoints, "SCANNER_STARTED", cid)
        scan = scan_toolbox(code or "", cell["task"], frozen)
        _mark(checkpoints, "SCANNER_COMPLETED", cid)

        completion = "NATURAL_COMPLETE" if code else "EXTRACTION_FAILURE"
        _mark(checkpoints, "EVALUATOR_STARTED", cid)
        evaluator, verdict, value = _evaluate_generated_code(code, cell["task"], frozen)
        _mark(checkpoints, "EVALUATOR_COMPLETED", cid)

        wall = time.monotonic() - started
        meta = dict(transport["metadata"])
        meta["wall_clock_seconds"] = wall

        system_defects = []
        if scan.get("classification") is None:
            system_defects.append("scanner_missing_classification")
        prompt_runtime_mismatch = 0

        artifact = {
            "cohort_run_id": plan["run_id"],
            "cell_id": cid,
            "source_sequence": SOURCE_SEQUENCE,
            "source_edge_cell_id": cell["source_edge_cell_id"],
            "task_id": cell["task"],
            "task_family": cell["task_family"],
            "condition": cell["condition"],
            "seed": cell["seed"],
            "model": cell["model"],
            "frozen_run_plan_hash": plan["hash"],
            "exact_rendered_prompt": prompt,
            "available_domain_apis": runtime_toolbox_inventory(),
            "task_required_operations": ops["required"],
            "acceptable_canonical_paths": ops["acceptable_canonical_paths"],
            "frozen_parameters": frozen,
            "request_payload_redacted": request,
            "CALL_INTENT": intent,
            "model_call_ledger": ledger,
            "raw_model_response": raw,
            "extracted_code": code,
            "model_metadata": meta,
            "token_counts": {
                "prompt_token_count": meta.get("prompt_token_count"),
                "candidates_token_count": meta.get("candidates_token_count"),
                "total_token_count": meta.get("total_token_count"),
            },
            "timing": {
                "wall_clock_seconds": wall,
                "latency_ms": meta.get("latency_ms"),
            },
            "scanner_diagnostics": scan,
            "called_domain_apis": scan.get("called_domain_apis", []),
            "irrelevant_api_diagnostics": scan.get("irrelevant_api_calls", []),
            "result_flow_diagnostics": {
                "domain_call_result_bindings": scan.get("domain_call_result_bindings", []),
                "domain_result_reaches_final_output": scan.get(
                    "domain_result_reaches_final_output", []
                ),
                "called_but_result_unused": scan.get("called_but_result_unused", False),
                "manual_recomputation_after_domain_call": scan.get(
                    "manual_recomputation_after_domain_call", False
                ),
            },
            "adoption_verdict": scan.get("classification"),
            "evaluator_verdict": evaluator,
            "evaluator_details": verdict,
            "returned_value": value,
            "completion": completion,
            "lifecycle_checkpoints": checkpoints,
            "process_exit_provenance": {
                "pid": os.getpid(),
                "status": "FINALIZED",
                "model_calls": model_calls,
            },
            "hashes": {
                "prompt": _h(prompt),
                "payload": _h(json.dumps(request, sort_keys=True)),
                "raw": _h(raw),
                "extracted_code": _h(code or ""),
            },
            "provenance": {
                "first_attempt_only": True,
                "no_retry": True,
                "request_number": 1,
                "model_calls": model_calls,
                "retry": 0,
                "resume": 0,
                "replacement": 0,
                "replay": 0,
                "repair": 0,
                "healer": 0,
                "api_key_source": "environment",
                "api_key_present": True,
            },
            "system_defects": system_defects,
            "prompt_runtime_mismatch": prompt_runtime_mismatch,
            "status": "FINALIZED",
        }
        assert_no_key_leak(artifact)
        _write_json(artifact_path, artifact)
        ledger[0]["status"] = "finalized"
        _write_json(ledger_path, ledger)
        _mark(checkpoints, "CELL_FINALIZED", cid)
        persist_lifecycle("FINALIZED")
        return {"status": "FINALIZED", "cell_id": cid, "model_calls": 1}
    except BaseException as exc:
        last = checkpoints[-1]["phase"] if checkpoints else "NONE"
        if raw_path.exists():
            status = "RAW_SAVED_OFFLINE_ADJUDICATION_ONLY"
        elif intent_path.exists():
            status = "SYSTEM_INTERRUPTED_AFTER_CALL_INTENT"
        else:
            status = "PRE_CALL_SYSTEM_FAILURE"
        _mark(checkpoints, "CELL_EXCEPTION", cid, exc)
        _write_json(
            state_path,
            {
                "cell_id": cid,
                "status": status,
                "last_successful_phase": last,
                "exception_type": type(exc).__name__,
                "exception_message": str(exc),
                "model_calls": model_calls,
                "checkpoints": checkpoints,
                "api_key_source": "environment",
                "api_key_present": api_key_status()["api_key_present"],
            },
        )
        persist_lifecycle(status)
        return {
            "status": status,
            "cell_id": cid,
            "model_calls": model_calls,
            "error": str(exc),
        }


def finalize(out: Path) -> dict:
    plan = json.loads((out / "frozen_run_plan.json").read_text(encoding="utf8"))
    cell = plan["cells"][0]
    cid = cell["cell_id"]
    art_path = out / "cell_artifact.json"
    raw_path = out / "raw_response.txt"
    state_path = out / "system_state.json"

    # Offline adjudication if raw saved but artifact missing
    if raw_path.exists() and not art_path.exists():
        from agent_tools.finals_rebuild.ce115_ab2d_assembly import (
            resolve_task_operations,
            runtime_toolbox_inventory,
            scan_toolbox,
        )
        from agent_tools.finals_rebuild.extraction import extract_code

        prompt, frozen = _render_formal_prompt(cell["task"], int(cell["seed"]))
        raw = raw_path.read_text(encoding="utf8")
        extraction = extract_code(raw)
        code = extraction.extracted_code if extraction.extraction_status == "extracted" else None
        if code:
            (out / "extracted_code.py").write_text(code, encoding="utf8")
        ops = resolve_task_operations(cell["task"], frozen)
        scan = scan_toolbox(code or "", cell["task"], frozen)
        completion = "NATURAL_COMPLETE" if code else "EXTRACTION_FAILURE"
        evaluator, verdict, value = _evaluate_generated_code(code, cell["task"], frozen)
        intent = {}
        if (out / "call_intent.json").exists():
            intent = json.loads((out / "call_intent.json").read_text(encoding="utf8"))
        ledger = []
        if (out / "model_call_ledger.json").exists():
            ledger = json.loads((out / "model_call_ledger.json").read_text(encoding="utf8"))
        request = {}
        if (out / "request_payload_redacted.json").exists():
            request = json.loads(
                (out / "request_payload_redacted.json").read_text(encoding="utf8")
            )
        artifact = {
            "cohort_run_id": plan["run_id"],
            "cell_id": cid,
            "source_sequence": SOURCE_SEQUENCE,
            "source_edge_cell_id": cell["source_edge_cell_id"],
            "task_id": cell["task"],
            "task_family": cell["task_family"],
            "condition": cell["condition"],
            "seed": cell["seed"],
            "model": cell["model"],
            "frozen_run_plan_hash": plan["hash"],
            "exact_rendered_prompt": prompt,
            "available_domain_apis": runtime_toolbox_inventory(),
            "task_required_operations": ops["required"],
            "acceptable_canonical_paths": ops["acceptable_canonical_paths"],
            "frozen_parameters": frozen,
            "request_payload_redacted": request,
            "CALL_INTENT": intent,
            "model_call_ledger": ledger,
            "raw_model_response": raw,
            "extracted_code": code,
            "scanner_diagnostics": scan,
            "called_domain_apis": scan.get("called_domain_apis", []),
            "irrelevant_api_diagnostics": scan.get("irrelevant_api_calls", []),
            "result_flow_diagnostics": {
                "domain_call_result_bindings": scan.get("domain_call_result_bindings", []),
                "domain_result_reaches_final_output": scan.get(
                    "domain_result_reaches_final_output", []
                ),
                "called_but_result_unused": scan.get("called_but_result_unused", False),
                "manual_recomputation_after_domain_call": scan.get(
                    "manual_recomputation_after_domain_call", False
                ),
            },
            "adoption_verdict": scan.get("classification"),
            "evaluator_verdict": evaluator,
            "evaluator_details": verdict,
            "returned_value": value,
            "completion": completion,
            "hashes": {
                "prompt": _h(prompt),
                "payload": _h(json.dumps(request, sort_keys=True)) if request else None,
                "raw": _h(raw),
                "extracted_code": _h(code or ""),
            },
            "provenance": {
                "first_attempt_only": True,
                "no_retry": True,
                "offline_finalizer_adjudication": True,
                "model_calls": 1 if ledger else 0,
                "retry": 0,
                "resume": 0,
                "replacement": 0,
                "replay": 0,
                "repair": 0,
                "healer": 0,
                "api_key_source": "environment",
                "api_key_present": api_key_status()["api_key_present"],
            },
            "system_defects": [],
            "prompt_runtime_mismatch": 0,
            "status": "FINALIZED",
        }
        _write_json(art_path, artifact)

    if not art_path.exists():
        st = {}
        if state_path.exists():
            st = json.loads(state_path.read_text(encoding="utf8"))
        ledger = []
        if (out / "model_call_ledger.json").exists():
            ledger = json.loads((out / "model_call_ledger.json").read_text(encoding="utf8"))
        raw_exists = raw_path.exists()
        network_completed = raw_exists
        if st.get("exception_message") == "API_KEY_REQUIRED":
            blocker = "API_KEY_REQUIRED"
        elif st.get("exception_type") == "ModuleNotFoundError":
            blocker = f"TRANSPORT_IMPORT_FAILURE:{st.get('exception_message')}"
        elif st:
            blocker = (
                f"TRANSPORT_OR_RUNTIME_FAILURE:"
                f"{st.get('exception_type')}:{st.get('exception_message')}"
            )
        else:
            blocker = "SYSTEM_BLOCKED_NO_ARTIFACT"
        zero = {
            "retry": 0,
            "resume": 0,
            "replacement": 0,
            "repair": 0,
            "replay": 0,
            "healer": 0,
            "model_calls_ledger_entries": len(ledger),
            "network_model_calls_completed": 1 if network_completed else 0,
            "first_attempt_only": True,
            "no_second_attempt": True,
        }
        summary = {
            "run_id": plan["run_id"],
            "cell_id": cid,
            "source_sequence": SOURCE_SEQUENCE,
            "source_edge_cell_id": cell.get("source_edge_cell_id"),
            "model": MODEL_ID,
            "completion": None,
            "toolbox_adoption": None,
            "evaluator": None,
            "system_state": st,
            "system_defects": [
                {
                    "kind": "transport",
                    "blocker": blocker,
                    "exception_type": st.get("exception_type"),
                    "exception_message": st.get("exception_message"),
                    "last_successful_phase": st.get("last_successful_phase"),
                }
            ],
            "prompt_runtime_mismatch": 0,
            "model_calls": 1 if network_completed else 0,
            "ledger_entries": len(ledger),
            "raw_persisted": raw_exists,
            "retry_resume_replacement_repair_replay_healer": zero,
            "verdict": "GEMINI35FLASH_SINGLE_CELL_SYSTEM_BLOCKED",
            "blocker": blocker,
            "edge_cohort_modified": False,
            "api_key_source": "environment",
            "api_key_present": True,
        }
        hash_integrity = {
            "run_plan_hash": plan["hash"],
            "protocol_hash": _h(PROTOCOL.read_text(encoding="utf8")),
            "prompt_hash": _h((out / "exact_rendered_prompt.txt").read_text(encoding="utf8"))
            if (out / "exact_rendered_prompt.txt").exists()
            else None,
            "raw_persisted": raw_exists,
            "artifact_persisted": False,
            "all_present": False,
        }
        _write_json(out / "positive_control_summary.json", summary)
        _write_json(out / "hash_integrity.json", hash_integrity)
        _write_json(out / "zero_retry_provenance.json", zero)
        return summary

    art = json.loads(art_path.read_text(encoding="utf8"))
    completion = art.get("completion")
    adoption = art.get("adoption_verdict")
    evaluator = art.get("evaluator_verdict")
    model_calls = int(art.get("provenance", {}).get("model_calls") or 0)
    system_defects = art.get("system_defects") or []
    mismatch = int(art.get("prompt_runtime_mismatch") or 0)
    hashes = art.get("hashes") or {}
    hashes_ok = all(hashes.get(k) for k in ("prompt", "raw", "extracted_code"))
    zero = {
        "retry": 0,
        "resume": 0,
        "replacement": 0,
        "repair": 0,
        "replay": 0,
        "healer": 0,
        "model_calls": model_calls,
        "first_attempt_only": True,
    }

    pass_ok = (
        completion == "NATURAL_COMPLETE"
        and adoption == "ASSEMBLY_COMPLIANT"
        and evaluator == "PASSED"
        and len(system_defects) == 0
        and mismatch == 0
        and model_calls == 1
        and hashes_ok
    )
    if pass_ok:
        verdict = "GEMINI35FLASH_SINGLE_CELL_POSITIVE_CONTROL_PASSED"
    elif any(
        x in (completion, adoption, evaluator)
        for x in ("EXTRACTION_FAILURE",)
    ) or system_defects or mismatch:
        # transport/extraction/scanner/evaluator/system issues
        if completion == "NATURAL_COMPLETE" and adoption in {
            "ASSEMBLY_COMPLIANT",
            "REQUIRED_OPERATION_NOT_COVERED",
            "INSUFFICIENT_EVIDENCE",
            "INVALID_API_CALL",
        }:
            # natural complete with model-side noncompliance/wrong answer
            if evaluator in {"ANSWER_INCORRECT", "EXECUTION_FAILURE", "PASSED"} and not system_defects:
                if adoption != "ASSEMBLY_COMPLIANT" or evaluator != "PASSED":
                    verdict = "GEMINI35FLASH_SINGLE_CELL_MODEL_FAILURE"
                else:
                    verdict = "GEMINI35FLASH_SINGLE_CELL_POSITIVE_CONTROL_PASSED"
            else:
                verdict = "GEMINI35FLASH_SINGLE_CELL_SYSTEM_BLOCKED"
        else:
            verdict = "GEMINI35FLASH_SINGLE_CELL_SYSTEM_BLOCKED"
    elif completion == "NATURAL_COMPLETE" and (
        adoption != "ASSEMBLY_COMPLIANT" or evaluator != "PASSED"
    ):
        verdict = "GEMINI35FLASH_SINGLE_CELL_MODEL_FAILURE"
    else:
        verdict = "GEMINI35FLASH_SINGLE_CELL_SYSTEM_BLOCKED"

    # Clarify: NATURAL_COMPLETE + noncompliant/wrong => MODEL_FAILURE
    if (
        completion == "NATURAL_COMPLETE"
        and not system_defects
        and mismatch == 0
        and model_calls == 1
        and (adoption != "ASSEMBLY_COMPLIANT" or evaluator != "PASSED")
    ):
        verdict = "GEMINI35FLASH_SINGLE_CELL_MODEL_FAILURE"

    if pass_ok:
        verdict = "GEMINI35FLASH_SINGLE_CELL_POSITIVE_CONTROL_PASSED"

    summary = {
        "run_id": plan["run_id"],
        "cell_id": cid,
        "source_sequence": SOURCE_SEQUENCE,
        "source_edge_cell_id": cell["source_edge_cell_id"],
        "model": MODEL_ID,
        "completion": completion,
        "toolbox_adoption": adoption,
        "evaluator": evaluator,
        "scanner_diagnostics": art.get("scanner_diagnostics"),
        "evaluator_details": art.get("evaluator_details"),
        "system_defects": system_defects,
        "prompt_runtime_mismatch": mismatch,
        "model_calls": model_calls,
        "retry_resume_replacement_repair_replay_healer": zero,
        "hashes": hashes,
        "verdict": verdict,
        "edge_cohort_modified": False,
        "api_key_source": "environment",
        "api_key_present": True,
    }
    hash_integrity = {
        "run_plan_hash": plan["hash"],
        "protocol_hash": _h(PROTOCOL.read_text(encoding="utf8")),
        "cell_hashes": hashes,
        "all_present": hashes_ok,
        "prompt_matches_file": hashes.get("prompt")
        == _h((out / "exact_rendered_prompt.txt").read_text(encoding="utf8")),
        "raw_matches_file": hashes.get("raw") == _h(raw_path.read_text(encoding="utf8"))
        if raw_path.exists()
        else False,
    }
    _write_json(out / "positive_control_summary.json", summary)
    _write_json(out / "hash_integrity.json", hash_integrity)
    _write_json(out / "zero_retry_provenance.json", zero)
    return summary


def run_cell_subprocess(out: Path) -> dict:
    """Process-isolated cell execution: one OS process, one cell, one model call."""
    proc = subprocess.run(
        [sys.executable, str(Path(__file__).resolve()), "run-cell", "--out", str(out)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=900,
        env=os.environ.copy(),
    )
    if proc.returncode != 0 and not (out / "raw_response.txt").exists():
        raise RuntimeError(
            f"isolated cell process failed rc={proc.returncode}: {(proc.stderr or proc.stdout)[:2000]}"
        )
    try:
        # last JSON object from stdout
        lines = [ln for ln in (proc.stdout or "").splitlines() if ln.strip().startswith("{")]
        return json.loads(lines[-1]) if lines else {"status": "UNKNOWN", "returncode": proc.returncode}
    except Exception:
        return {"status": "UNKNOWN", "returncode": proc.returncode, "stdout_tail": (proc.stdout or "")[-500:]}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="CE115 v4 Gemini 3.5 Flash positive control")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_pre = sub.add_parser("preflight")
    p_pre.add_argument("--out", type=Path, default=DEFAULT_OUT)

    p_run = sub.add_parser("run-cell")
    p_run.add_argument("--out", type=Path, default=DEFAULT_OUT)

    p_iso = sub.add_parser("run-isolated")
    p_iso.add_argument("--out", type=Path, default=DEFAULT_OUT)

    p_fin = sub.add_parser("finalize")
    p_fin.add_argument("--out", type=Path, default=DEFAULT_OUT)

    p_all = sub.add_parser("execute")
    p_all.add_argument("--out", type=Path, default=DEFAULT_OUT)

    args = parser.parse_args(argv)
    if args.cmd == "preflight":
        result = run_preflight(args.out)
        print(json.dumps(result, indent=2))
        return 0 if result.get("passed") else 2
    if args.cmd == "run-cell":
        result = run_cell(args.out)
        print(json.dumps(result, indent=2))
        return 0 if result.get("status") == "FINALIZED" else 1
    if args.cmd == "run-isolated":
        result = run_cell_subprocess(args.out)
        print(json.dumps(result, indent=2))
        return 0 if result.get("status") == "FINALIZED" else 1
    if args.cmd == "finalize":
        summary = finalize(args.out)
        print(json.dumps(summary, indent=2))
        return 0
    if args.cmd == "execute":
        pf = run_preflight(args.out)
        print(json.dumps({"preflight": pf}, indent=2))
        if not pf.get("passed"):
            return 2
        cell_result = run_cell_subprocess(args.out)
        summary = finalize(args.out)
        print(json.dumps({"cell": cell_result, "summary": summary}, indent=2))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
