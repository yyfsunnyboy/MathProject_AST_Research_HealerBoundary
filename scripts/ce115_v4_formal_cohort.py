"""CE115 Ab2d Assembly v4 formal 18-cell process-isolated cohort.

Derives the frozen 18-cell geometry from the committed v3 formal rerun manifest
(same models / tasks / seeds / order). Uses v4 prompt contract + scan_toolbox +
oracle evaluator. One OS process per cell; offline finalizer never calls models.
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

V3_MANIFEST = ROOT / "docs/experiments/manifests/ce115_ab2d_corrected_formal_rerun_manifest.json"
PROTOCOL = ROOT / "docs/experiments/manifests/ce115_ab2d_assembly_protocol_v4.json"
CERT_SUMMARY = (
    ROOT
    / "docs/experiments/results/ce115_ab2d_assembly_v4_process_orchestration_validation"
    / "orchestration_validation_summary.json"
)
SMOKE_SUMMARY = (
    ROOT
    / "docs/experiments/results/ce115_ab2d_assembly_v4_process_isolated_smoke_01"
    / "smoke_summary.json"
)
DEFAULT_COHORT = ROOT / "docs/experiments/results/ce115_ab2d_assembly_v4_formal_run"
OLLAMA_CHAT = "http://127.0.0.1:11434/api/chat"
EXPECTED_DIGESTS = {"qwen3.5:4b": "2a654d98e6fb", "qwen3.5:9b": "6488c96fa5fa"}
TASK_FAMILY = {
    "ce115_calc_polynomial_division_l1": "polynomial",
    "ce115_calc_exact_rational_expression_l1": "fraction",
    "ce115_calc_radical_simplification_l1": "radical",
}
FORBIDDEN_PROMPT = ("Required APIs", "MUST_CALL", "invoke every required API")
REQUIRED_PROMPT = (
    "Available Domain APIs",
    "Select only APIs relevant to the current task",
    "Do not call irrelevant APIs merely for compliance",
    "Use the domain library for every supported core operation actually required by the task",
    "Do not manually reimplement a supported core algorithm",
    "returned value contributes to the final answer",
)


def _h(x: str) -> str:
    return hashlib.sha256(x.encode()).hexdigest()


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


def formal_plan() -> dict:
    """Load frozen 18-cell geometry from v3 formal manifest; remap condition to v4."""
    src = json.loads(V3_MANIFEST.read_text(encoding="utf8"))
    if len(src["cells"]) != 18:
        raise RuntimeError(f"expected 18 source cells, got {len(src['cells'])}")
    cells = []
    for i, c in enumerate(src["cells"], 1):
        if "ab2d_assembly_v3" not in c["cell_id"]:
            raise RuntimeError(f"unexpected source cell_id: {c['cell_id']}")
        cell_id = c["cell_id"].replace("ab2d_assembly_v3", "ab2d_assembly_v4")
        family = TASK_FAMILY[c["task"]]
        cells.append(
            {
                "sequence": i,
                "cell_id": cell_id,
                "source_v3_cell_id": c["cell_id"],
                "model": c["model"],
                "task": c["task"],
                "task_family": family,
                "seed": c["seed"],
                "condition": "ab2d_assembly_v4",
                "max_model_calls": 1,
                "retry": 0,
                "replay": 0,
                "repair": 0,
                "healer": 0,
                "digest_prefix": EXPECTED_DIGESTS[c["model"]],
            }
        )
    body = {
        "run_id": "ce115_ab2d_assembly_v4_formal_run",
        "condition": "ab2d_assembly_v4",
        "protocol_id": "ce115_ab2d_assembly_protocol_v4",
        "source_v3_manifest": str(V3_MANIFEST.relative_to(ROOT)).replace("\\", "/"),
        "source_v3_run_id": src["run_id"],
        "planned_cells": 18,
        "resume": False,
        "no_overwrite": True,
        "model_calls_planned": 18,
        "exclusions": src.get("exclusions", []),
        "cells": cells,
    }
    body["hash"] = _h(json.dumps({k: v for k, v in body.items() if k != "hash"}, sort_keys=True))
    return body


def _load_formal_plan(root: Path) -> dict:
    path = root / "frozen_formal_run_plan.json"
    stored = json.loads(path.read_text(encoding="utf8"))
    expected = formal_plan()
    if stored.get("hash") != expected["hash"]:
        raise RuntimeError(
            f"formal run plan hash mismatch: stored={stored.get('hash')} expected={expected['hash']}"
        )
    if [c["cell_id"] for c in stored["cells"]] != [c["cell_id"] for c in expected["cells"]]:
        raise RuntimeError("formal run plan cell set drifted")
    return stored


def _render_formal_prompt(task_id: str, seed: int) -> tuple[str, dict]:
    from agent_tools.finals_rebuild.ce115_ab2d_assembly import stub_for_task
    from agent_tools.finals_rebuild.ce115_calc_golden_generators import formal_l1_tasks
    from agent_tools.finals_rebuild.ce115_calc_prompt_freeze import render_calc_task_contract
    from agent_tools.finals_rebuild.math_task_sampler import sample_task_parameters

    task = formal_l1_tasks()[task_id]
    frozen = sample_task_parameters(task, seed)["oracle_payload"]
    prompt = (
        stub_for_task(task_id)
        + "\n## Task contract\n"
        + render_calc_task_contract(task)
        + "\n## Frozen parameters\n"
        + json.dumps(frozen, sort_keys=True)
        + "\nReturn only Python source; oracle_payload must exactly equal the frozen parameters.\n"
    )
    return prompt, frozen


def _ollama_provenance() -> dict:
    listing = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=30)
    try:
        ver = subprocess.run(["ollama", "--version"], capture_output=True, text=True, timeout=15)
        version = (ver.stdout or ver.stderr or "").strip()
    except Exception as exc:
        version = f"unavailable: {exc}"
    models = {}
    for tag, digest in EXPECTED_DIGESTS.items():
        ok = listing.returncode == 0 and tag in listing.stdout and digest in listing.stdout
        models[tag] = {
            "tag": tag,
            "digest_prefix": digest,
            "present": ok,
            "quantization": "Q4_K_M",
        }
    return {
        "runtime": "ollama",
        "runtime_version": version,
        "ollama_list_ok": listing.returncode == 0,
        "models": models,
        "all_models_available": all(m["present"] for m in models.values()),
    }


def run_formal_preflight(cohort: Path) -> dict:
    if cohort.exists():
        raise RuntimeError(f"refusing overwrite existing formal directory: {cohort}")
    protocol = json.loads(PROTOCOL.read_text(encoding="utf8"))
    cert = json.loads(CERT_SUMMARY.read_text(encoding="utf8"))
    smoke = json.loads(SMOKE_SUMMARY.read_text(encoding="utf8"))
    from agent_tools.finals_rebuild.ce115_ab2d_assembly import runtime_toolbox_inventory
    from scripts.run_ce115_ab2d_v4_minimal_smoke import preflight as smoke_preflight

    p = formal_plan()
    inventory = runtime_toolbox_inventory()
    smoke_pf = smoke_preflight()
    provenance = _ollama_provenance()
    prompt_checks = {}
    for task_id in sorted(TASK_FAMILY):
        text, _ = _render_formal_prompt(task_id, 2026071301)
        prompt_checks[task_id] = {
            "available_domain_apis": all(x in text for x in REQUIRED_PROMPT),
            "no_legacy": not any(x in text for x in FORBIDDEN_PROMPT),
            "inventory_consistent": all(
                x["canonical_name"] in text
                and x["signature"] in text
                and x["return_structure"] in text
                for x in inventory
            ),
            "output_contract": "generate(level=1, **kwargs)" in text,
        }
    cell_ids = [c["cell_id"] for c in p["cells"]]
    checks = {
        "repo_root": str(ROOT),
        "protocol_status": protocol.get("status"),
        "protocol_status_ok": protocol.get("status") == "FROZEN_ZERO_MODEL_VALIDATED_V2",
        "orchestration_certification": cert.get("verdict"),
        "orchestration_certification_ok": cert.get("verdict")
        == "ONE_CELL_PROCESS_ORCHESTRATION_ZERO_MODEL_CERTIFIED",
        "smoke_verdict": smoke.get("verdict"),
        "smoke_eligible": smoke.get("eligible_for_formal_rerun") is True,
        "cohort_absent": not cohort.exists(),
        "planned_cells": p["planned_cells"],
        "planned_cells_ok": p["planned_cells"] == 18 and len(p["cells"]) == 18,
        "cell_ids_unique": len(set(cell_ids)) == 18,
        "max_model_calls_per_cell_all_1": all(c["max_model_calls"] == 1 for c in p["cells"]),
        "retry_replay_repair_healer_disabled": all(
            all(int(c[k]) == 0 for k in ("retry", "replay", "repair", "healer")) for c in p["cells"]
        ),
        "resume_disabled": p.get("resume") is False,
        "source_geometry_matches_v3": True,
        "prompt_contract_smoke": smoke_pf,
        "prompt_checks": prompt_checks,
        "prompt_checks_passed": all(all(v.values()) for v in prompt_checks.values()),
        "model_provenance": provenance,
        "models_available": provenance["all_models_available"],
        "scanner_evaluator_same_as_smoke": True,
        "real_model_calls": 0,
        "run_plan_hash": p["hash"],
        "protocol_hash": _h(PROTOCOL.read_text(encoding="utf8")),
    }
    checks["passed"] = all(
        [
            checks["protocol_status_ok"],
            checks["orchestration_certification_ok"],
            checks["smoke_eligible"],
            checks["cohort_absent"],
            checks["planned_cells_ok"],
            checks["cell_ids_unique"],
            checks["max_model_calls_per_cell_all_1"],
            checks["retry_replay_repair_healer_disabled"],
            checks["resume_disabled"],
            checks["prompt_checks_passed"],
            smoke_pf.get("passed") is True,
            checks["models_available"],
        ]
    )
    if not checks["passed"]:
        return checks
    cohort.mkdir(parents=True)
    (cohort / "frozen_formal_run_plan.json").write_text(
        json.dumps(p, indent=2) + "\n", encoding="utf8"
    )
    (cohort / "run_plan_hash.txt").write_text(p["hash"] + "\n", encoding="utf8")
    (cohort / "protocol_and_plan_hashes.json").write_text(
        json.dumps(
            {
                "protocol_path": str(PROTOCOL.relative_to(ROOT)).replace("\\", "/"),
                "protocol_hash": checks["protocol_hash"],
                "run_plan_hash": p["hash"],
                "source_v3_manifest": p["source_v3_manifest"],
            },
            indent=2,
        )
        + "\n",
        encoding="utf8",
    )
    (cohort / "model_provenance.json").write_text(
        json.dumps(provenance, indent=2) + "\n", encoding="utf8"
    )
    (cohort / "formal_preflight_summary.json").write_text(
        json.dumps(checks, indent=2) + "\n", encoding="utf8"
    )
    return checks


def _formal_generate_worker(source: str, repo: str):
    """Top-level worker kept for tests/import compatibility; prefer subprocess path."""
    import sys as _sys
    from pathlib import Path as _Path

    root = _Path(repo)
    if str(root) not in _sys.path:
        _sys.path.insert(0, str(root))
    from agent_tools.finals_rebuild.ce115_ab2d_assembly import runtime_namespace

    ns = runtime_namespace()
    exec(compile(source, "<formal>", "exec"), ns, ns)
    return ns["generate"]()


def _evaluate_generated_code(code: str | None, task_id: str, frozen: dict) -> tuple[str, dict, object]:
    """Run generate()+oracle in a killable subprocess with hard timeout."""
    if not code:
        return "EXECUTION_FAILURE", {"error": "empty code"}, None
    helper = r"""
import json, sys
sys.path.insert(0, sys.argv[1])
task_id = sys.argv[2]
frozen = json.loads(sys.argv[3])
from agent_tools.finals_rebuild.ce115_ab2d_assembly import runtime_namespace
from agent_tools.finals_rebuild.math_boundary_pilot import load_pilot_tasks
from agent_tools.finals_rebuild.math_task_oracles import evaluate_math_task_oracle
ns = runtime_namespace()
exec(compile(sys.stdin.read(), "<formal>", "exec"), ns, ns)
value = ns["generate"]()
formal = {x["task_id"]: x for x in load_pilot_tasks(
    __import__("pathlib").Path(sys.argv[1]) / "tests/finals_rebuild/fixtures/math_generation_tasks_ce115_pilot.jsonl"
)}
if isinstance(value, dict):
    verdict = evaluate_math_task_oracle(formal[task_id]["oracle_type"], frozen, value.get("correct_answer"))
    evaluator = "PASSED" if verdict.get("is_correct") else "ANSWER_INCORRECT"
else:
    verdict = {"error": "generate() did not return dict"}
    evaluator = "EXECUTION_FAILURE"
print(json.dumps({"evaluator": evaluator, "verdict": verdict, "value": value}, default=str))
"""
    try:
        proc = subprocess.run(
            [sys.executable, "-c", helper, str(ROOT), task_id, json.dumps(frozen, sort_keys=True)],
            input=code,
            text=True,
            capture_output=True,
            cwd=ROOT,
            timeout=45,
        )
    except subprocess.TimeoutExpired:
        return "EXECUTION_FAILURE", {"error": "timeout"}, None
    if proc.returncode != 0:
        err = (proc.stderr or proc.stdout or "nonzero_exit").strip()
        return "EXECUTION_FAILURE", {"error": err[:2000]}, None
    try:
        payload = json.loads(proc.stdout.strip().splitlines()[-1])
    except Exception as exc:
        return "EXECUTION_FAILURE", {"error": f"parse_output: {exc}"}, None
    return payload.get("evaluator", "EXECUTION_FAILURE"), payload.get("verdict") or {}, payload.get("value")


def run_formal_cell(root: Path, cell: dict) -> dict:
    from agent_tools.finals_rebuild.ce115_ab2d_assembly import (
        resolve_task_operations,
        runtime_namespace,
        runtime_toolbox_inventory,
        scan_toolbox,
    )
    from agent_tools.finals_rebuild.extraction import extract_code
    from agent_tools.finals_rebuild.math_boundary_pilot import load_pilot_tasks
    from agent_tools.finals_rebuild.math_task_oracles import evaluate_math_task_oracle

    root = Path(root)
    plan = _load_formal_plan(root)
    cid = cell["cell_id"]
    intent = root / f"{cid}.intent.json"
    artifact_path = root / f"{cid}.artifact.json"
    raw_path = root / f"{cid}.raw.txt"
    ledger_path = root / f"{cid}.ledger.json"
    lifecycle_path = root / f"{cid}.lifecycle.json"
    state_path = root / f"{cid}.system_state.json"
    if intent.exists() or artifact_path.exists() or raw_path.exists():
        raise RuntimeError(f"duplicate cell invocation refused: {cid}")

    checkpoints: list = []
    model_calls = 0
    model = cell["model"]
    digest = EXPECTED_DIGESTS[model]

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

    _mark(checkpoints, "CELL_SELECTED", cid, sequence=cell["sequence"])
    try:
        if int(cell.get("max_model_calls", 1)) != 1:
            raise RuntimeError("max_model_calls must be 1")
        for flag in ("retry", "replay", "repair", "healer"):
            if int(cell.get(flag, 0)) != 0:
                raise RuntimeError(f"{flag} must be disabled")
        prompt, frozen = _render_formal_prompt(cell["task"], int(cell["seed"]))
        _mark(checkpoints, "PROMPT_RENDERED", cid)
        request = {
            "model": model,
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
        intent.write_text(
            json.dumps(
                {
                    "cell": cell,
                    "phase": "CALL_INTENT",
                    "timestamp": time.time(),
                    "prompt_hash": _h(prompt),
                    "payload_hash": _h(json.dumps(request, sort_keys=True)),
                    "model": model,
                    "digest_prefix": digest,
                },
                indent=2,
            )
            + "\n",
            encoding="utf8",
        )
        _mark(checkpoints, "CALL_INTENT_PERSISTED", cid)
        ledger = [
            {
                "cell_id": cid,
                "request_number": 1,
                "status": "intent",
                "model": model,
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
        with urllib.request.urlopen(req, timeout=1800) as response:
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

        from agent_tools.finals_rebuild.ce115_ab2d_assembly import (
            resolve_task_operations,
            runtime_toolbox_inventory,
            scan_toolbox,
        )
        from agent_tools.finals_rebuild.extraction import extract_code

        extraction = extract_code(raw)
        code = extraction.extracted_code if extraction.extraction_status == "extracted" else None
        ops = resolve_task_operations(cell["task"], frozen)
        _mark(checkpoints, "SCANNER_STARTED", cid)
        scan = scan_toolbox(code or "", cell["task"], frozen)
        _mark(checkpoints, "SCANNER_COMPLETED", cid)

        completion = "NATURAL_COMPLETE" if code else "EXTRACTION_FAILURE"
        _mark(checkpoints, "EVALUATOR_STARTED", cid)
        evaluator, verdict, value = _evaluate_generated_code(code, cell["task"], frozen)
        _mark(checkpoints, "EVALUATOR_COMPLETED", cid)

        artifact_data = {
            "cohort_run_id": plan["run_id"],
            "sequence": cell["sequence"],
            "cell_id": cid,
            "task_id": cell["task"],
            "task_family": cell["task_family"],
            "condition": cell["condition"],
            "seed": cell["seed"],
            "model": model,
            "frozen_run_plan_hash": plan["hash"],
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
            "model_metadata": {
                "model": model,
                "digest_prefix": digest,
                "quantization": "Q4_K_M",
                "runtime": "ollama",
                "prompt_eval_count": reply.get("prompt_eval_count"),
                "eval_count": reply.get("eval_count"),
                "total_duration": reply.get("total_duration"),
                "load_duration": reply.get("load_duration"),
                "prompt_eval_duration": reply.get("prompt_eval_duration"),
                "eval_duration": reply.get("eval_duration"),
                "wall_clock_seconds": time.monotonic() - started,
            },
            "token_counts": {
                "prompt_eval_count": reply.get("prompt_eval_count"),
                "eval_count": reply.get("eval_count"),
            },
            "timing": {
                "wall_clock_seconds": time.monotonic() - started,
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
                "replay": 0,
                "repair": 0,
                "healer": 0,
                "source_v3_cell_id": cell.get("source_v3_cell_id"),
            },
            "status": "FINALIZED",
        }
        artifact_path.write_text(
            json.dumps(artifact_data, indent=2, default=str) + "\n", encoding="utf8"
        )
        ledger[0]["status"] = "finalized"
        ledger_path.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf8")
        _mark(checkpoints, "CELL_FINALIZED", cid)
        persist_lifecycle("FINALIZED")
        return {"status": "FINALIZED", "cell_id": cid, "sequence": cell["sequence"], "model_calls": 1}
    except BaseException as exc:
        last = checkpoints[-1]["phase"] if checkpoints else "NONE"
        if raw_path.exists():
            status = "RAW_SAVED_OFFLINE_ADJUDICATION_ONLY"
        elif intent.exists():
            status = "SYSTEM_INTERRUPTED_AFTER_CALL_INTENT"
        else:
            status = "PRE_CALL_SYSTEM_FAILURE"
        _mark(checkpoints, "CELL_EXCEPTION", cid, exc)
        state_path.write_text(
            json.dumps(
                {
                    "cell_id": cid,
                    "sequence": cell["sequence"],
                    "status": status,
                    "last_successful_phase": last,
                    "exception_type": type(exc).__name__,
                    "exception_message": str(exc),
                    "model_calls": model_calls,
                    "checkpoints": checkpoints,
                },
                indent=2,
            )
            + "\n",
            encoding="utf8",
        )
        persist_lifecycle(status)
        return {
            "status": status,
            "cell_id": cid,
            "sequence": cell["sequence"],
            "model_calls": model_calls,
            "error": str(exc),
        }


def _offline_adjudicate(root: Path, cell: dict) -> None:
    cid = cell["cell_id"]
    raw_path = root / f"{cid}.raw.txt"
    artifact_path = root / f"{cid}.artifact.json"
    if artifact_path.exists() or not raw_path.exists():
        return
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
    ops = resolve_task_operations(cell["task"], frozen)
    scan = scan_toolbox(code or "", cell["task"], frozen)
    completion = "NATURAL_COMPLETE" if code else "EXTRACTION_FAILURE"
    evaluator, verdict, value = _evaluate_generated_code(code, cell["task"], frozen)
    intent = {}
    ip = root / f"{cid}.intent.json"
    if ip.exists():
        intent = json.loads(ip.read_text(encoding="utf8"))
    ledger = []
    lp = root / f"{cid}.ledger.json"
    if lp.exists():
        ledger = json.loads(lp.read_text(encoding="utf8"))
    artifact = {
        "cohort_run_id": "ce115_ab2d_assembly_v4_formal_run",
        "sequence": cell["sequence"],
        "cell_id": cid,
        "task_id": cell["task"],
        "task_family": cell["task_family"],
        "condition": cell["condition"],
        "seed": cell["seed"],
        "model": cell["model"],
        "frozen_run_plan_hash": _load_formal_plan(root)["hash"],
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
            "manual_recomputation_after_domain_call": scan.get(
                "manual_recomputation_after_domain_call", False
            ),
        },
        "adoption_verdict": scan.get("classification"),
        "evaluator_verdict": evaluator,
        "evaluator_details": verdict,
        "returned_value": value,
        "completion": completion,
        "hashes": {"prompt": _h(prompt), "raw": _h(raw), "extracted_code": _h(code or "")},
        "provenance": {
            "first_attempt_only": True,
            "no_retry": True,
            "offline_finalizer_adjudication": True,
            "model_calls": 1 if ledger else 0,
            "retry": 0,
            "replay": 0,
            "repair": 0,
            "healer": 0,
        },
        "status": "FINALIZED",
    }
    artifact_path.write_text(json.dumps(artifact, indent=2, default=str) + "\n", encoding="utf8")


def finalize_formal(root: Path) -> dict:
    root = Path(root)
    plan = _load_formal_plan(root)
    if len(plan["cells"]) != 18:
        raise RuntimeError("formal plan must have 18 cells")
    for c in plan["cells"]:
        _offline_adjudicate(root, c)

    rows = []
    interruptions = []
    call_counts = {}
    states = []
    for c in plan["cells"]:
        cid = c["cell_id"]
        art = root / f"{cid}.artifact.json"
        raw = root / f"{cid}.raw.txt"
        intent = root / f"{cid}.intent.json"
        state = root / f"{cid}.system_state.json"
        ledger_path = root / f"{cid}.ledger.json"
        n = 0
        if ledger_path.exists():
            ledger = json.loads(ledger_path.read_text(encoding="utf8"))
            n = len(ledger)
            if n > 1:
                raise RuntimeError(f"duplicate calls for {cid}: {n}")
        call_counts[cid] = n
        st = {
            "cell_id": cid,
            "sequence": c["sequence"],
            "intent": intent.exists(),
            "raw": raw.exists(),
            "artifact": art.exists(),
        }
        if art.exists():
            row = json.loads(art.read_text(encoding="utf8"))
            rows.append(row)
            st["status"] = "FINALIZED"
        elif state.exists():
            s = json.loads(state.read_text(encoding="utf8"))
            interruptions.append(s)
            st["status"] = s.get("status", "SYSTEM_STATE")
        elif intent.exists() and not raw.exists():
            interruptions.append(
                {"cell_id": cid, "status": "SYSTEM_INTERRUPTED_AFTER_CALL_INTENT"}
            )
            st["status"] = "SYSTEM_INTERRUPTED_AFTER_CALL_INTENT"
        else:
            st["status"] = "MISSING"
            interruptions.append({"cell_id": cid, "status": "MISSING"})
        states.append(st)

    comp = Counter(x.get("completion", "UNKNOWN") for x in rows)
    adopt = Counter(x.get("adoption_verdict", "UNKNOWN") for x in rows)
    ev = Counter(x.get("evaluator_verdict", "UNKNOWN") for x in rows)
    sys_counts = Counter(x.get("status", "UNKNOWN") for x in interruptions)
    by_family = {}
    by_condition = {"ab2d_assembly_v4": {"artifacts": len(rows)}}
    for x in rows:
        fam = x.get("task_family", "unknown")
        by_family.setdefault(fam, Counter())
        by_family[fam]["completion:" + x.get("completion", "?")] += 1
        by_family[fam]["adoption:" + x.get("adoption_verdict", "?")] += 1
        by_family[fam]["evaluator:" + x.get("evaluator_verdict", "?")] += 1
    cross = [
        {
            "cell_id": x["cell_id"],
            "task_family": x.get("task_family"),
            "model": x.get("model"),
            "irrelevant_api_calls": x.get("irrelevant_api_diagnostics", []),
            "called_domain_apis": x.get("called_domain_apis", []),
            "manual_recomputation": x.get("result_flow_diagnostics", {}).get(
                "manual_recomputation_after_domain_call"
            ),
        }
        for x in rows
    ]
    hashes_ok = all(
        isinstance(x.get("hashes"), dict) and all(x["hashes"].values()) for x in rows
    )
    all_raw = all((root / f"{c['cell_id']}.raw.txt").exists() for c in plan["cells"])
    all_art = all((root / f"{c['cell_id']}.artifact.json").exists() for c in plan["cells"])
    exactly_one = all(call_counts.get(c["cell_id"], 0) == 1 for c in plan["cells"])
    no_dup = all(v <= 1 for v in call_counts.values())
    no_retry = True
    for x in rows:
        prov = x.get("provenance", {})
        if any(int(prov.get(k, 0) or 0) for k in ("retry", "replay", "repair", "healer")):
            no_retry = False
    system_interrupt = bool(interruptions) or not all_raw
    formal_complete = all_raw and all_art and exactly_one and no_dup and no_retry
    if formal_complete and not system_interrupt:
        verdict = "FORMAL_V4_RUN_COMPLETED"
    elif len(states) == 18 and no_dup and no_retry:
        verdict = "FORMAL_V4_RUN_COMPLETED_WITH_SYSTEM_INTERRUPTION"
    else:
        verdict = "FORMAL_V4_RUN_INCOMPLETE"

    zero_retry = {
        "retry": 0,
        "resume": 0,
        "replacement_call": 0,
        "repair": 0,
        "replay": 0,
        "healer": 0,
        "duplicate_calls": 0,
        "per_cell_model_calls": call_counts,
        "provenance_ok": no_retry and no_dup,
    }
    offline = {
        "no_model_calls": True,
        "planned": 18,
        "states": states,
        "call_counts": call_counts,
        "interruptions": interruptions,
        "completion_counts": dict(comp),
        "toolbox_adoption_counts": dict(adopt),
        "evaluator_correctness_counts": dict(ev),
        "system_state_counts": dict(sys_counts),
        "cross_domain_diagnostics": cross,
        "smoke_verdict_ref": "V4_PROCESS_ISOLATED_SMOKE_COMPLETED",
        "finalizer_verdict": verdict,
    }
    summary = {
        "planned": 18,
        "executed_artifacts": len(rows),
        "model_calls_per_cell": call_counts,
        "total_model_calls": sum(call_counts.values()),
        "completion_counts": dict(comp),
        "toolbox_adoption_counts": dict(adopt),
        "evaluator_correctness_counts": dict(ev),
        "system_state_counts": dict(sys_counts),
        "per_family_counts": {k: dict(v) for k, v in by_family.items()},
        "per_condition_counts": by_condition,
        "system_interruptions": interruptions,
        "retry_resume_replacement_repair_replay_healer": zero_retry,
        "verdict": verdict,
        "formal_run_complete": formal_complete and not system_interrupt,
        "hashes_complete": hashes_ok and len(rows) == 18 if formal_complete else hashes_ok,
    }
    hash_integrity = {
        "planned_cells": 18,
        "artifacts": len(rows),
        "all_hashes_present": hashes_ok and len(rows) == 18,
        "run_plan_hash": plan["hash"],
        "cells": [{"cell_id": x["cell_id"], "hashes": x.get("hashes")} for x in rows],
    }
    (root / "offline_finalizer_summary.json").write_text(
        json.dumps(offline, indent=2) + "\n", encoding="utf8"
    )
    (root / "formal_run_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf8"
    )
    (root / "hash_integrity.json").write_text(
        json.dumps(hash_integrity, indent=2) + "\n", encoding="utf8"
    )
    (root / "zero_retry_provenance.json").write_text(
        json.dumps(zero_retry, indent=2) + "\n", encoding="utf8"
    )
    (root / "cross_domain_diagnostics_summary.json").write_text(
        json.dumps({"cells": cross, "count": len(cross)}, indent=2) + "\n", encoding="utf8"
    )
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="CE115 v4 formal 18-cell process-isolated cohort")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_pre = sub.add_parser("preflight")
    p_pre.add_argument("--cohort", type=Path, default=DEFAULT_COHORT)

    p_run = sub.add_parser("run-cell")
    p_run.add_argument("--cohort", type=Path, default=DEFAULT_COHORT)
    g = p_run.add_mutually_exclusive_group(required=True)
    g.add_argument("--cell-id", type=str)
    g.add_argument("--sequence", type=int)

    p_fin = sub.add_parser("finalize")
    p_fin.add_argument("--cohort", type=Path, default=DEFAULT_COHORT)

    p_show = sub.add_parser("show-plan")
    p_show.add_argument("--index", type=int, default=None)

    args = parser.parse_args(argv)
    if args.cmd == "show-plan":
        p = formal_plan()
        if args.index is None:
            print(json.dumps({"hash": p["hash"], "n": len(p["cells"]), "cell_ids": [c["cell_id"] for c in p["cells"]]}, indent=2))
        else:
            print(json.dumps(p["cells"][args.index - 1], indent=2))
        return 0
    if args.cmd == "preflight":
        result = run_formal_preflight(args.cohort)
        print(json.dumps(result, indent=2))
        return 0 if result.get("passed") else 2
    if args.cmd == "run-cell":
        plan = _load_formal_plan(args.cohort)
        if args.cell_id:
            matches = [c for c in plan["cells"] if c["cell_id"] == args.cell_id]
        else:
            matches = [c for c in plan["cells"] if c["sequence"] == args.sequence]
        if len(matches) != 1:
            raise SystemExit(f"cell not unique: matches={len(matches)}")
        cell = matches[0]
        intent = args.cohort / f"{cell['cell_id']}.intent.json"
        raw = args.cohort / f"{cell['cell_id']}.raw.txt"
        if intent.exists() or raw.exists():
            raise SystemExit(f"refusing: {cell['cell_id']} already has intent/raw")
        result = run_formal_cell(args.cohort, cell)
        print(json.dumps(result, indent=2))
        return 0 if result.get("status") == "FINALIZED" else 1
    if args.cmd == "finalize":
        summary = finalize_formal(args.cohort)
        print(json.dumps(summary, indent=2))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
