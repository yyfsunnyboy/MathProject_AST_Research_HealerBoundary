"""Frozen-plan one-cell process orchestration.

Fake mode: certification / targeted tests (zero model calls).
Real mode: process-isolated smoke — one OS process, one cell, one model call.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import threading
import time
import urllib.request
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

TASKS = [
    ("polynomial", "ce115_calc_polynomial_division_l1"),
    ("fraction", "ce115_calc_exact_rational_expression_l1"),
    ("radical", "ce115_calc_radical_simplification_l1"),
]
MODEL = "qwen3.5:4b"
EXPECTED_DIGEST_PREFIX = "2a654d98e6fb"
OLLAMA_CHAT = "http://127.0.0.1:11434/api/chat"
PROTOCOL = ROOT / "docs/experiments/manifests/ce115_ab2d_assembly_protocol_v4.json"
CERT_SUMMARY = (
    ROOT
    / "docs/experiments/results/ce115_ab2d_assembly_v4_process_orchestration_validation"
    / "orchestration_validation_summary.json"
)
BLOCKED = [
    ROOT / "docs/experiments/results/ce115_ab2d_assembly_v4_minimal_smoke",
    ROOT / "docs/experiments/results/ce115_ab2d_assembly_v4_minimal_smoke_rerun_01",
    ROOT / "docs/experiments/results/ce115_ab2d_assembly_v4_minimal_smoke_final",
]


def plan():
    # Structure frozen by ONE_CELL_PROCESS_ORCHESTRATION_ZERO_MODEL_CERTIFIED — do not add fields.
    cells = [
        {
            "cell_id": f"process_{f}_2026071301",
            "family": f,
            "task": t,
            "seed": 2026071301,
            "max_model_calls": 1,
            "retry": 0,
            "replay": 0,
            "repair": 0,
            "healer": 0,
        }
        for f, t in TASKS
    ]
    d = {"run_id": "ce115_v4_process_isolated", "cells": cells}
    d["hash"] = hashlib.sha256(json.dumps(d, sort_keys=True).encode()).hexdigest()
    return d


def _h(x: str) -> str:
    return hashlib.sha256(x.encode()).hexdigest()


def _load_plan(root: Path) -> dict:
    p = json.loads((root / "frozen_run_plan.json").read_text(encoding="utf8"))
    recomputed = plan()
    if p.get("hash") != recomputed["hash"]:
        raise RuntimeError(
            f"run plan hash mismatch: stored={p.get('hash')} expected={recomputed['hash']}"
        )
    if [c["cell_id"] for c in p["cells"]] != [c["cell_id"] for c in recomputed["cells"]]:
        raise RuntimeError("run plan cell ids drifted from frozen plan()")
    return p


def _mark(checkpoints: list, phase: str, cell_id=None, exc=None, **extra):
    checkpoints.append(
        {
            "cell_id": cell_id,
            "phase": phase,
            "timestamp": time.time(),
            "process_id": os.getpid(),
            "thread_id": threading.get_ident(),
            "exception_type": type(exc).__name__ if exc else None,
            "exception_message": str(exc) if exc else None,
            **extra,
        }
    )


def run_cell(root, cell, mode="fake", interrupt=None):
    root = Path(root)
    intent = root / f"{cell['cell_id']}.intent.json"
    artifact = root / f"{cell['cell_id']}.artifact.json"
    if intent.exists() or artifact.exists():
        raise RuntimeError("duplicate cell invocation refused")
    if mode == "real":
        # Real path persists CALL_INTENT only after payload is ready (still before transport).
        return _run_cell_real(root, cell)
    intent.write_text(
        json.dumps({"cell": cell, "phase": "CALL_INTENT", "timestamp": time.time()}) + "\n",
        encoding="utf8",
    )
    if interrupt == "after_intent":
        return {"status": "SYSTEM_INTERRUPTED_AFTER_CALL_INTENT"}
    raw = root / f"{cell['cell_id']}.raw.txt"
    raw.write_text(
        'def generate(level=1, **kwargs):\n return {"question_text":"q","correct_answer":0,"oracle_payload":{}}\n',
        encoding="utf8",
    )
    if interrupt == "after_raw":
        return {"status": "RAW_SAVED_OFFLINE_ADJUDICATION_ONLY"}
    artifact.write_text(
        json.dumps({"cell": cell, "status": "FINALIZED", "fake_transport_calls": 1, "retry": 0})
        + "\n",
        encoding="utf8",
    )
    return {"status": "FINALIZED"}


def _run_cell_real(root: Path, cell: dict) -> dict:
    from agent_tools.finals_rebuild.ce115_ab2d_assembly import (
        resolve_task_operations,
        runtime_namespace,
        runtime_toolbox_inventory,
        scan_toolbox,
    )
    from agent_tools.finals_rebuild.extraction import extract_code
    from agent_tools.finals_rebuild.math_boundary_pilot import load_pilot_tasks
    from agent_tools.finals_rebuild.math_task_oracles import evaluate_math_task_oracle
    from scripts.run_ce115_ab2d_v4_minimal_smoke import payload_for

    cid = cell["cell_id"]
    intent = root / f"{cid}.intent.json"
    checkpoints: list = []
    ledger_path = root / f"{cid}.ledger.json"
    lifecycle_path = root / f"{cid}.lifecycle.json"
    state_path = root / f"{cid}.system_state.json"
    raw_path = root / f"{cid}.raw.txt"
    artifact_path = root / f"{cid}.artifact.json"

    def persist_lifecycle(status: str):
        lifecycle_path.write_text(
            json.dumps(
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
                indent=2,
            )
            + "\n",
            encoding="utf8",
        )

    _mark(checkpoints, "CELL_SELECTED", cid)
    model_calls = 0
    try:
        if int(cell.get("max_model_calls", 1)) != 1:
            raise RuntimeError("max_model_calls_per_cell must be 1")
        for flag in ("retry", "replay", "repair", "healer"):
            if int(cell.get(flag, 0)) != 0:
                raise RuntimeError(f"{flag} must be disabled")

        source_cell, prompt, frozen = payload_for(cell["task"])
        if int(source_cell.get("seed")) != int(cell["seed"]):
            raise RuntimeError(f"seed mismatch: plan={cell['seed']} source={source_cell.get('seed')}")
        _mark(checkpoints, "PROMPT_RENDERED", cid)

        request = {
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "think": False,
            "options": {
                "temperature": 0.0,
                "seed": int(cell["seed"]),
                "num_ctx": 65536,
                "num_predict": 24576,
            },
        }
        _mark(checkpoints, "PAYLOAD_BUILT", cid)
        _mark(checkpoints, "CALL_INTENT_PERSISTED", cid)
        intent.write_text(
            json.dumps(
                {
                    "cell": cell,
                    "phase": "CALL_INTENT",
                    "timestamp": time.time(),
                    "prompt_hash": _h(prompt),
                    "payload_hash": _h(json.dumps(request, sort_keys=True)),
                    "model": MODEL,
                },
                indent=2,
            )
            + "\n",
            encoding="utf8",
        )
        ledger = [
            {
                "cell_id": cid,
                "request_number": 1,
                "status": "intent",
                "retry": 0,
                "replay": 0,
                "repair": 0,
                "healer": 0,
            }
        ]
        ledger_path.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf8")
        persist_lifecycle("CALL_INTENT_PERSISTED")

        _mark(checkpoints, "TRANSPORT_ENTERED", cid)
        started = time.monotonic()
        model_calls = 1
        req = urllib.request.Request(
            OLLAMA_CHAT,
            data=json.dumps(request).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=900) as response:
            reply = json.loads(response.read())
        _mark(checkpoints, "TRANSPORT_RETURNED", cid)
        raw = reply.get("message", {}).get("content")
        if not isinstance(raw, str):
            raise RuntimeError("model response missing message.content string")
        raw_path.write_text(raw, encoding="utf8")
        _mark(checkpoints, "RAW_PERSISTED", cid)
        ledger[0]["status"] = "raw_persisted"
        ledger_path.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf8")
        persist_lifecycle("RAW_PERSISTED")

        extraction = extract_code(raw)
        code = extraction.extracted_code if extraction.extraction_status == "extracted" else None
        ops = resolve_task_operations(cell["task"], frozen)
        _mark(checkpoints, "SCANNER_STARTED", cid)
        scan = scan_toolbox(code or "", cell["task"], frozen)
        _mark(checkpoints, "SCANNER_COMPLETED", cid)

        formal = {
            x["task_id"]: x
            for x in load_pilot_tasks(
                ROOT / "tests/finals_rebuild/fixtures/math_generation_tasks_ce115_pilot.jsonl"
            )
        }
        completion = "NATURAL_COMPLETE" if code else "EXTRACTION_FAILURE"
        value = None
        verdict: dict = {}
        evaluator = "SYSTEM_DEFECT"
        _mark(checkpoints, "EVALUATOR_STARTED", cid)
        try:
            ns = runtime_namespace()
            exec(compile(code or "", "<smoke>", "exec"), ns, ns)
            value = ns["generate"]()
            if isinstance(value, dict):
                verdict = evaluate_math_task_oracle(
                    formal[cell["task"]]["oracle_type"], frozen, value.get("correct_answer")
                )
                evaluator = "PASSED" if verdict.get("is_correct") else "ANSWER_INCORRECT"
            else:
                evaluator = "EXECUTION_FAILURE"
                verdict = {"error": "generate() did not return dict"}
        except Exception as exc:
            evaluator = "EXECUTION_FAILURE"
            verdict = {"error": f"{type(exc).__name__}: {exc}"}
        _mark(checkpoints, "EVALUATOR_COMPLETED", cid)

        model_info = {
            "model": MODEL,
            "digest_prefix": EXPECTED_DIGEST_PREFIX,
            "prompt_eval_count": reply.get("prompt_eval_count"),
            "eval_count": reply.get("eval_count"),
            "total_duration": reply.get("total_duration"),
            "load_duration": reply.get("load_duration"),
            "prompt_eval_duration": reply.get("prompt_eval_duration"),
            "eval_duration": reply.get("eval_duration"),
            "wall_clock_seconds": time.monotonic() - started,
        }
        artifact = {
            "cohort_run_id": "ce115_v4_process_isolated",
            "cell_id": cid,
            "task_id": cell["task"],
            "task_family": cell["family"],
            "seed": cell["seed"],
            "frozen_run_plan_hash": _load_plan(root)["hash"],
            "exact_rendered_prompt": prompt,
            "available_domain_apis": runtime_toolbox_inventory(),
            "task_required_operations": ops["required"],
            "acceptable_canonical_paths": ops["acceptable_canonical_paths"],
            "frozen_parameters": frozen,
            "request_payload": request,
            "CALL_INTENT": json.loads(intent.read_text(encoding="utf8")),
            "model_call_ledger": ledger,
            "raw_model_response": raw,
            "raw_transport_response": reply,
            "extracted_code": code,
            "model_metadata": model_info,
            "token_counts": {
                "prompt_eval_count": reply.get("prompt_eval_count"),
                "eval_count": reply.get("eval_count"),
            },
            "timing": {
                "wall_clock_seconds": model_info["wall_clock_seconds"],
                "total_duration": reply.get("total_duration"),
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
                "replay": 0,
                "repair": 0,
                "healer": 0,
                "source_frozen_cell_id": source_cell.get("cell_id"),
            },
            "status": "FINALIZED",
        }
        artifact_path.write_text(json.dumps(artifact, indent=2, default=str) + "\n", encoding="utf8")
        ledger[0]["status"] = "finalized"
        ledger_path.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf8")
        _mark(checkpoints, "CELL_FINALIZED", cid)
        persist_lifecycle("FINALIZED")
        return {"status": "FINALIZED", "cell_id": cid, "model_calls": model_calls}
    except BaseException as exc:
        last = checkpoints[-1]["phase"] if checkpoints else "NONE"
        if raw_path.exists():
            status = "RAW_SAVED_OFFLINE_ADJUDICATION_ONLY"
        elif intent.exists() and model_calls:
            status = "SYSTEM_INTERRUPTED_AFTER_CALL_INTENT"
        elif intent.exists() and last in {
            "CALL_INTENT_PERSISTED",
            "TRANSPORT_ENTERED",
            "PAYLOAD_BUILT",
            "PROMPT_RENDERED",
            "CELL_SELECTED",
        }:
            # Intent file always written by run_cell before real path; distinguish pre-transport.
            if last in {"CALL_INTENT_PERSISTED", "TRANSPORT_ENTERED"}:
                status = "SYSTEM_INTERRUPTED_AFTER_CALL_INTENT"
            else:
                status = "PRE_CALL_SYSTEM_FAILURE"
        else:
            status = "PRE_CALL_SYSTEM_FAILURE"
        _mark(checkpoints, "CELL_EXCEPTION", cid, exc)
        state = {
            "cell_id": cid,
            "status": status,
            "last_successful_phase": last,
            "exception_type": type(exc).__name__,
            "exception_message": str(exc),
            "model_calls": model_calls,
            "checkpoints": checkpoints,
        }
        state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf8")
        persist_lifecycle(status)
        if ledger_path.exists():
            try:
                ledger = json.loads(ledger_path.read_text(encoding="utf8"))
                if ledger:
                    ledger[0]["status"] = status.lower()
                    ledger_path.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf8")
            except Exception:
                pass
        return {"status": status, "cell_id": cid, "model_calls": model_calls, "error": str(exc)}


def finalize(root):
    root = Path(root)
    p = json.loads((root / "frozen_run_plan.json").read_text(encoding="utf8"))
    states = []
    for c in p["cells"]:
        i = root / f"{c['cell_id']}.intent.json"
        a = root / f"{c['cell_id']}.artifact.json"
        r = root / f"{c['cell_id']}.raw.txt"
        states.append(
            {
                "cell_id": c["cell_id"],
                "intent": i.exists(),
                "raw": r.exists(),
                "artifact": a.exists(),
                "status": (
                    "FINALIZED"
                    if a.exists()
                    else "SYSTEM_INTERRUPTED_AFTER_CALL_INTENT"
                    if i.exists()
                    else "MISSING"
                ),
            }
        )
    return {
        "planned": 3,
        "states": states,
        "verdict": "COMPLETE" if all(x["artifact"] for x in states) else "BLOCKED",
    }


def _offline_adjudicate_if_needed(root: Path, cell: dict) -> None:
    """Complete scanner/evaluator offline when raw exists but artifact missing. Never calls model."""
    cid = cell["cell_id"]
    raw_path = root / f"{cid}.raw.txt"
    artifact_path = root / f"{cid}.artifact.json"
    if artifact_path.exists() or not raw_path.exists():
        return
    from agent_tools.finals_rebuild.ce115_ab2d_assembly import (
        resolve_task_operations,
        runtime_namespace,
        runtime_toolbox_inventory,
        scan_toolbox,
    )
    from agent_tools.finals_rebuild.extraction import extract_code
    from agent_tools.finals_rebuild.math_boundary_pilot import load_pilot_tasks
    from agent_tools.finals_rebuild.math_task_oracles import evaluate_math_task_oracle
    from scripts.run_ce115_ab2d_v4_minimal_smoke import payload_for

    source_cell, prompt, frozen = payload_for(cell["task"])
    raw = raw_path.read_text(encoding="utf8")
    extraction = extract_code(raw)
    code = extraction.extracted_code if extraction.extraction_status == "extracted" else None
    ops = resolve_task_operations(cell["task"], frozen)
    scan = scan_toolbox(code or "", cell["task"], frozen)
    formal = {
        x["task_id"]: x
        for x in load_pilot_tasks(
            ROOT / "tests/finals_rebuild/fixtures/math_generation_tasks_ce115_pilot.jsonl"
        )
    }
    completion = "NATURAL_COMPLETE" if code else "EXTRACTION_FAILURE"
    value = None
    verdict: dict = {}
    try:
        ns = runtime_namespace()
        exec(compile(code or "", "<smoke>", "exec"), ns, ns)
        value = ns["generate"]()
        if isinstance(value, dict):
            verdict = evaluate_math_task_oracle(
                formal[cell["task"]]["oracle_type"], frozen, value.get("correct_answer")
            )
            evaluator = "PASSED" if verdict.get("is_correct") else "ANSWER_INCORRECT"
        else:
            evaluator = "EXECUTION_FAILURE"
    except Exception as exc:
        evaluator = "EXECUTION_FAILURE"
        verdict = {"error": f"{type(exc).__name__}: {exc}"}
    intent = {}
    ip = root / f"{cid}.intent.json"
    if ip.exists():
        intent = json.loads(ip.read_text(encoding="utf8"))
    ledger = []
    lp = root / f"{cid}.ledger.json"
    if lp.exists():
        ledger = json.loads(lp.read_text(encoding="utf8"))
    artifact = {
        "cohort_run_id": "ce115_v4_process_isolated",
        "cell_id": cid,
        "task_id": cell["task"],
        "task_family": cell["family"],
        "seed": cell["seed"],
        "frozen_run_plan_hash": _load_plan(root)["hash"],
        "exact_rendered_prompt": prompt,
        "available_domain_apis": runtime_toolbox_inventory(),
        "task_required_operations": ops["required"],
        "acceptable_canonical_paths": ops["acceptable_canonical_paths"],
        "frozen_parameters": frozen,
        "CALL_INTENT": intent,
        "model_call_ledger": ledger,
        "raw_model_response": raw,
        "extracted_code": code,
        "scanner_diagnostics": scan,
        "called_domain_apis": scan.get("called_domain_apis", []),
        "irrelevant_api_diagnostics": scan.get("irrelevant_api_calls", []),
        "result_flow_diagnostics": {
            "domain_call_result_bindings": scan.get("domain_call_result_bindings", []),
            "domain_result_reaches_final_output": scan.get("domain_result_reaches_final_output", []),
            "called_but_result_unused": scan.get("called_but_result_unused", False),
        },
        "adoption_verdict": scan.get("classification"),
        "evaluator_verdict": evaluator,
        "evaluator_details": verdict,
        "returned_value": value,
        "completion": completion,
        "hashes": {
            "prompt": _h(prompt),
            "raw": _h(raw),
            "extracted_code": _h(code or ""),
        },
        "provenance": {
            "first_attempt_only": True,
            "no_retry": True,
            "offline_finalizer_adjudication": True,
            "model_calls": 1 if ledger else 0,
            "retry": 0,
            "replay": 0,
            "repair": 0,
            "healer": 0,
            "source_frozen_cell_id": source_cell.get("cell_id"),
        },
        "status": "FINALIZED",
    }
    artifact_path.write_text(json.dumps(artifact, indent=2, default=str) + "\n", encoding="utf8")


def finalize_smoke(root: Path) -> dict:
    """Offline finalizer for real smoke evidence. Never calls the model."""
    root = Path(root)
    p = _load_plan(root)
    cell_ids = [c["cell_id"] for c in p["cells"]]
    if len(set(cell_ids)) != 3:
        raise RuntimeError("cell ids not unique")

    for c in p["cells"]:
        _offline_adjudicate_if_needed(root, c)

    base = finalize(root)
    rows = []
    call_counts = {}
    interruptions = []
    for c in p["cells"]:
        cid = c["cell_id"]
        art_path = root / f"{cid}.artifact.json"
        state_path = root / f"{cid}.system_state.json"
        ledger_path = root / f"{cid}.ledger.json"
        raw_path = root / f"{cid}.raw.txt"
        intent_path = root / f"{cid}.intent.json"
        model_calls = 0
        if ledger_path.exists():
            ledger = json.loads(ledger_path.read_text(encoding="utf8"))
            model_calls = len(ledger)
            if model_calls > 1:
                raise RuntimeError(f"{cid} model call count > 1")
        call_counts[cid] = model_calls
        if not intent_path.exists():
            interruptions.append({"cell_id": cid, "status": "MISSING_CALL_INTENT"})
        if art_path.exists():
            rows.append(json.loads(art_path.read_text(encoding="utf8")))
        elif state_path.exists():
            st = json.loads(state_path.read_text(encoding="utf8"))
            interruptions.append(st)
        elif intent_path.exists() and not raw_path.exists():
            interruptions.append(
                {
                    "cell_id": cid,
                    "status": "SYSTEM_INTERRUPTED_AFTER_CALL_INTENT",
                    "last_successful_phase": "CALL_INTENT",
                }
            )

    comp = Counter(x.get("completion", "UNKNOWN") for x in rows)
    adopt = Counter(x.get("adoption_verdict", "UNKNOWN") for x in rows)
    ev = Counter(x.get("evaluator_verdict", "UNKNOWN") for x in rows)
    cross = [
        {
            "cell_id": x["cell_id"],
            "irrelevant_api_calls": x.get("irrelevant_api_diagnostics", []),
            "called_domain_apis": x.get("called_domain_apis", []),
        }
        for x in rows
    ]
    hashes_ok = all(
        isinstance(x.get("hashes"), dict) and all(x["hashes"].values()) for x in rows
    ) and len(rows) == 3
    system_interrupt = bool(interruptions) or any(
        not (root / f"{c['cell_id']}.raw.txt").exists() for c in p["cells"]
    )
    duplicate = any(v > 1 for v in call_counts.values())
    exactly_one = all(call_counts.get(c["cell_id"], 0) == 1 for c in p["cells"])
    all_raw = all((root / f"{c['cell_id']}.raw.txt").exists() for c in p["cells"])
    all_art = all((root / f"{c['cell_id']}.artifact.json").exists() for c in p["cells"])
    no_retry = True
    for x in rows:
        prov = x.get("provenance", {})
        if any(int(prov.get(k, 0) or 0) for k in ("retry", "replay", "repair", "healer")):
            no_retry = False

    eligible = (
        exactly_one
        and all_raw
        and all_art
        and not system_interrupt
        and not duplicate
        and no_retry
        and hashes_ok
        and base["verdict"] == "COMPLETE"
    )
    verdict = (
        "V4_PROCESS_ISOLATED_SMOKE_COMPLETED"
        if eligible
        else "V4_PROCESS_ISOLATED_SMOKE_SYSTEM_BLOCKED"
    )

    zero_retry = {
        "retry": 0,
        "resume": 0,
        "replacement_call": 0,
        "repair": 0,
        "replay": 0,
        "healer": 0,
        "duplicate_calls": 0,
        "per_cell_model_calls": call_counts,
        "provenance_ok": no_retry and not duplicate,
    }
    hash_integrity = {
        "planned_cells": 3,
        "artifacts": len(rows),
        "all_hashes_present": hashes_ok,
        "run_plan_hash": p["hash"],
        "cells": [
            {
                "cell_id": x["cell_id"],
                "hashes": x.get("hashes"),
            }
            for x in rows
        ],
    }
    offline = {
        "no_model_calls": True,
        "planned": 3,
        "states": base["states"],
        "call_counts": call_counts,
        "interruptions": interruptions,
        "completion_counts": dict(comp),
        "toolbox_adoption_counts": dict(adopt),
        "evaluator_correctness_counts": dict(ev),
        "cross_domain_diagnostics": cross,
        "finalizer_verdict": base["verdict"],
        "smoke_verdict": verdict,
    }
    summary = {
        "planned": 3,
        "executed_artifacts": len(rows),
        "model_calls_per_cell": call_counts,
        "completion_counts": dict(comp),
        "toolbox_adoption_counts": dict(adopt),
        "evaluator_correctness_counts": dict(ev),
        "cross_domain_diagnostics": cross,
        "system_interruptions": interruptions,
        "retry_resume_replacement_repair_replay_healer": zero_retry,
        "verdict": verdict,
        "eligible_for_formal_rerun": eligible,
        "formal_rerun_not_started": True,
        "hashes_complete": hashes_ok,
    }
    (root / "offline_finalizer_summary.json").write_text(
        json.dumps(offline, indent=2) + "\n", encoding="utf8"
    )
    (root / "smoke_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf8")
    (root / "hash_integrity.json").write_text(
        json.dumps(hash_integrity, indent=2) + "\n", encoding="utf8"
    )
    (root / "zero_retry_provenance.json").write_text(
        json.dumps(zero_retry, indent=2) + "\n", encoding="utf8"
    )
    return summary


def run_preflight(cohort: Path) -> dict:
    if cohort.exists():
        raise RuntimeError(f"refusing overwrite existing cohort directory: {cohort}")
    protocol = json.loads(PROTOCOL.read_text(encoding="utf8"))
    cert = json.loads(CERT_SUMMARY.read_text(encoding="utf8"))
    from scripts.run_ce115_ab2d_v4_minimal_smoke import preflight as smoke_preflight

    smoke_pf = smoke_preflight()
    p = plan()
    cell_ids = [c["cell_id"] for c in p["cells"]]
    listing = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=30)
    model_ok = listing.returncode == 0 and MODEL in listing.stdout and EXPECTED_DIGEST_PREFIX in listing.stdout
    blocked_ok = all(b.exists() for b in BLOCKED)
    checks = {
        "repo_root": str(ROOT),
        "protocol_status": protocol.get("status"),
        "protocol_status_ok": protocol.get("status") == "FROZEN_ZERO_MODEL_VALIDATED_V2",
        "orchestration_certification": cert.get("verdict"),
        "orchestration_certification_ok": cert.get("verdict")
        == "ONE_CELL_PROCESS_ORCHESTRATION_ZERO_MODEL_CERTIFIED",
        "cohort_absent": not cohort.exists(),
        "blocked_cohorts_present": blocked_ok,
        "blocked_cohort_paths": [str(b) for b in BLOCKED],
        "run_plan": p,
        "cell_ids_unique": len(set(cell_ids)) == 3,
        "max_model_calls_per_cell_all_1": all(c["max_model_calls"] == 1 for c in p["cells"]),
        "retry_resume_replacement_repair_replay_healer_disabled": all(
            all(int(c.get(k, 0)) == 0 for k in ("retry", "replay", "repair", "healer"))
            for c in p["cells"]
        ),
        "resume_disabled": True,
        "replacement_call_disabled": True,
        "prompt_contract": smoke_pf,
        "model": MODEL,
        "model_digest_prefix": EXPECTED_DIGEST_PREFIX,
        "model_available": model_ok,
        "real_model_calls": 0,
    }
    checks["passed"] = all(
        [
            checks["protocol_status_ok"],
            checks["orchestration_certification_ok"],
            checks["cohort_absent"],
            checks["blocked_cohorts_present"],
            checks["cell_ids_unique"],
            checks["max_model_calls_per_cell_all_1"],
            checks["retry_resume_replacement_repair_replay_healer_disabled"],
            smoke_pf.get("passed") is True,
            checks["model_available"],
        ]
    )
    if not checks["passed"]:
        return checks
    cohort.mkdir(parents=True)
    (cohort / "frozen_run_plan.json").write_text(json.dumps(p, indent=2) + "\n", encoding="utf8")
    (cohort / "run_plan_hash.txt").write_text(p["hash"] + "\n", encoding="utf8")
    (cohort / "preflight_summary.json").write_text(
        json.dumps(checks, indent=2) + "\n", encoding="utf8"
    )
    return checks


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="CE115 v4 one-cell process orchestrator")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_pre = sub.add_parser("preflight", help="Zero-model preflight; creates cohort dir")
    p_pre.add_argument("--cohort", type=Path, required=True)

    p_run = sub.add_parser("run-cell", help="Run exactly one cell in this process")
    p_run.add_argument("--cohort", type=Path, required=True)
    p_run.add_argument(
        "--family",
        required=True,
        choices=["polynomial", "fraction", "radical"],
    )
    p_run.add_argument("--mode", choices=["real", "fake"], default="real")

    p_fin = sub.add_parser("finalize", help="Offline finalizer; never calls model")
    p_fin.add_argument("--cohort", type=Path, required=True)

    args = parser.parse_args(argv)
    if args.cmd == "preflight":
        result = run_preflight(args.cohort)
        print(json.dumps(result, indent=2))
        return 0 if result.get("passed") else 2
    if args.cmd == "run-cell":
        root = args.cohort
        p = _load_plan(root)
        matches = [c for c in p["cells"] if c["family"] == args.family]
        if len(matches) != 1:
            raise SystemExit(f"family not unique: {args.family}")
        cell = matches[0]
        intent = root / f"{cell['cell_id']}.intent.json"
        raw = root / f"{cell['cell_id']}.raw.txt"
        if intent.exists() or raw.exists():
            raise SystemExit(f"refusing: {cell['cell_id']} already has intent/raw")
        result = run_cell(root, cell, mode=args.mode)
        print(json.dumps(result, indent=2))
        return 0 if result.get("status") == "FINALIZED" else 1
    if args.cmd == "finalize":
        summary = finalize_smoke(args.cohort)
        print(json.dumps(summary, indent=2))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
