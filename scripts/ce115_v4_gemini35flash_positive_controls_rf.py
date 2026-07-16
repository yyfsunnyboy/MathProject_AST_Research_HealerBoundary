"""CE115 v4 Gemini 3.5 Flash radical + fraction positive controls.

Exactly two first-attempt Gemini network calls (one per cell), process-isolated.
Does not modify the frozen 18-cell edge cohort.
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
from scripts.ce115_v4_gemini35flash_positive_control import (  # noqa: E402
    _transport_is_flask_free,
)

SOURCE_COHORT = ROOT / "docs/experiments/results/ce115_ab2d_assembly_v4_formal_run"
DEFAULT_OUT = (
    ROOT
    / "docs/experiments/results/ce115_ab2d_assembly_v4_gemini35flash_positive_controls_radical_fraction_01"
)
EXPECTED_PROTOCOL_HASH = "1b86e94b291803b0aa1987af7d728ada756a183bf0bf2039a1563a47a7d70897"
SOURCE_EDGE_MODEL = "qwen3.5:9b"
# Fixed identities — refuse if formal plan disagrees.
FIXED_CELLS = (
    {
        "key": "radical",
        "sequence": 10,
        "task_family": "radical",
        "task": "ce115_calc_radical_simplification_l1",
        "seed": 2026071301,
        "expected_cell_id": (
            "qwen3_5_9b__ce115_calc_radical_simplification_l1__"
            "ab2d_assembly_v4__seed_2026071301"
        ),
    },
    {
        "key": "fraction",
        "sequence": 16,
        "task_family": "fraction",
        "task": "ce115_calc_exact_rational_expression_l1",
        "seed": 2026071301,
        "expected_cell_id": (
            "qwen3_5_9b__ce115_calc_exact_rational_expression_l1__"
            "ab2d_assembly_v4__seed_2026071301"
        ),
    },
)


def _write_json(path: Path, obj: object) -> None:
    text = json.dumps(obj, indent=2, default=str) + "\n"
    assert_no_key_leak(text)
    path.write_text(text, encoding="utf8")


def _load_formal_plan() -> dict:
    return json.loads((SOURCE_COHORT / "frozen_formal_run_plan.json").read_text(encoding="utf8"))


def _source_edge(spec: dict) -> tuple[dict, dict]:
    plan = _load_formal_plan()
    matches = [c for c in plan["cells"] if c["sequence"] == spec["sequence"]]
    if len(matches) != 1:
        raise RuntimeError(f"sequence {spec['sequence']} not unique")
    cell = matches[0]
    if cell["cell_id"] != spec["expected_cell_id"]:
        raise RuntimeError(
            f"identity mismatch seq {spec['sequence']}: "
            f"got={cell['cell_id']} expected={spec['expected_cell_id']}"
        )
    if cell["model"] != SOURCE_EDGE_MODEL:
        raise RuntimeError(f"model mismatch seq {spec['sequence']}: {cell['model']}")
    if cell["task"] != spec["task"] or cell["task_family"] != spec["task_family"]:
        raise RuntimeError(f"task/family mismatch seq {spec['sequence']}")
    if int(cell["seed"]) != int(spec["seed"]):
        raise RuntimeError(f"seed mismatch seq {spec['sequence']}")
    art_path = SOURCE_COHORT / f"{cell['cell_id']}.artifact.json"
    if not art_path.is_file():
        raise RuntimeError(f"missing artifact: {art_path}")
    art = json.loads(art_path.read_text(encoding="utf8"))
    if art.get("evaluator_verdict") != "EXECUTION_FAILURE":
        raise RuntimeError(
            f"seq {spec['sequence']} evaluator is not EXECUTION_FAILURE: "
            f"{art.get('evaluator_verdict')}"
        )
    return cell, art


def build_run_plan(out: Path | None = None) -> dict:
    out = Path(out) if out is not None else DEFAULT_OUT
    cells = []
    for spec in FIXED_CELLS:
        edge, _ = _source_edge(spec)
        cells.append(
            {
                "key": spec["key"],
                "cell_id": (
                    f"gemini_3_5_flash__{spec['task']}__"
                    f"ab2d_assembly_v4_positive_control_rf01__seed_{spec['seed']}"
                ),
                "source_sequence": spec["sequence"],
                "source_edge_cell_id": edge["cell_id"],
                "source_edge_model": edge["model"],
                "model": MODEL_ID,
                "task": spec["task"],
                "task_family": spec["task_family"],
                "family": spec["task_family"],
                "seed": spec["seed"],
                "condition": "ab2d_assembly_v4",
                "max_model_calls": 1,
                "retry": 0,
                "resume": 0,
                "replacement": 0,
                "replay": 0,
                "repair": 0,
                "healer": 0,
            }
        )
    body = {
        "run_id": out.name,
        "condition": "ab2d_assembly_v4",
        "protocol_id": "ce115_ab2d_assembly_protocol_v4",
        "source_cohort": str(SOURCE_COHORT.relative_to(ROOT)).replace("\\", "/"),
        "planned_cells": 2,
        "model_calls_planned": 2,
        "resume": False,
        "no_overwrite": True,
        "cells": cells,
    }
    body["hash"] = _h(json.dumps({k: v for k, v in body.items() if k != "hash"}, sort_keys=True))
    return body


def _cell_by_key(plan: dict, key: str) -> dict:
    matches = [c for c in plan["cells"] if c["key"] == key]
    if len(matches) != 1:
        raise RuntimeError(f"cell key not unique: {key}")
    return matches[0]


def run_preflight(out: Path) -> dict:
    out = Path(out)
    if out.exists():
        raise RuntimeError(f"refusing overwrite existing directory: {out}")

    protocol = json.loads(PROTOCOL.read_text(encoding="utf8"))
    protocol_hash = _h(PROTOCOL.read_text(encoding="utf8"))
    plan = build_run_plan(out)
    from agent_tools.finals_rebuild.ce115_ab2d_assembly import (
        resolve_task_operations,
        runtime_toolbox_inventory,
    )

    inventory = runtime_toolbox_inventory()
    per_cell = {}
    for spec in FIXED_CELLS:
        edge, art = _source_edge(spec)
        cell = _cell_by_key(plan, spec["key"])
        prompt, frozen = _render_formal_prompt(cell["task"], int(cell["seed"]))
        if frozen != art.get("frozen_parameters"):
            raise RuntimeError(f"{spec['key']}: frozen parameters drifted")
        if prompt != art.get("exact_rendered_prompt"):
            raise RuntimeError(f"{spec['key']}: rendered prompt drifted")
        ops = resolve_task_operations(cell["task"], frozen)
        if ops["required"] != art.get("task_required_operations"):
            raise RuntimeError(f"{spec['key']}: required ops drifted")
        if ops["acceptable_canonical_paths"] != art.get("acceptable_canonical_paths"):
            raise RuntimeError(f"{spec['key']}: acceptable paths drifted")
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
        }
        per_cell[spec["key"]] = {
            "source_sequence": spec["sequence"],
            "source_edge_cell_id": edge["cell_id"],
            "task": cell["task"],
            "task_family": cell["task_family"],
            "seed": cell["seed"],
            "prompt_hash": _h(prompt),
            "source_completion": art.get("completion"),
            "source_adoption": art.get("adoption_verdict"),
            "source_evaluator": art.get("evaluator_verdict"),
            "source_is_edge_failure": art.get("evaluator_verdict") == "EXECUTION_FAILURE",
            "prompt_checks": prompt_ok,
            "prompt_checks_passed": all(prompt_ok.values()),
            "max_model_calls": cell["max_model_calls"],
            "frozen_parameters": frozen,
            "task_required_operations": ops["required"],
        }

    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, timeout=30
    )
    origin = subprocess.run(
        ["git", "rev-parse", "origin/main"], cwd=ROOT, capture_output=True, text=True, timeout=30
    )
    branch = subprocess.run(
        ["git", "branch", "--show-current"], cwd=ROOT, capture_output=True, text=True, timeout=30
    )
    git_head = (head.stdout or "").strip()
    git_origin = (origin.stdout or "").strip()
    key = api_key_status()
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
        "output_dir_absent": not out.exists(),
        "transport_flask_free": _transport_is_flask_free(),
        "model_id": MODEL_ID,
        "model_id_ok": MODEL_ID == "gemini-3.5-flash",
        "planned_cells": plan["planned_cells"],
        "model_calls_planned": plan["model_calls_planned"],
        "budget_ok": plan["planned_cells"] == 2 and plan["model_calls_planned"] == 2,
        "per_cell_budget_one": all(c["max_model_calls"] == 1 for c in plan["cells"]),
        "retry_flags_disabled": all(
            all(int(c[k]) == 0 for k in ("retry", "resume", "replacement", "replay", "repair", "healer"))
            for c in plan["cells"]
        ),
        "cells": per_cell,
        "source_cells_ok": all(v["source_is_edge_failure"] and v["prompt_checks_passed"] for v in per_cell.values()),
        "runtime_version": runtime_version(),
        **key,
        "real_model_calls": 0,
        "run_plan_hash": plan["hash"],
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
            checks["output_dir_absent"],
            checks["transport_flask_free"],
            checks["model_id_ok"],
            checks["budget_ok"],
            checks["per_cell_budget_one"],
            checks["retry_flags_disabled"],
            checks["source_cells_ok"],
            checks["api_key_present"],
        ]
    )
    if not checks["passed"]:
        checks["blocker"] = "PREFLIGHT_FAILED"
        return checks

    out.mkdir(parents=True)
    _write_json(out / "frozen_run_plan.json", plan)
    _write_json(
        out / "protocol_and_plan_hashes.json",
        {
            "protocol_path": str(PROTOCOL.relative_to(ROOT)).replace("\\", "/"),
            "protocol_hash": protocol_hash,
            "run_plan_hash": plan["hash"],
            "prompt_hashes": {k: v["prompt_hash"] for k, v in per_cell.items()},
            "source_sequences": {k: v["source_sequence"] for k, v in per_cell.items()},
        },
    )
    for key_name, info in per_cell.items():
        cell = _cell_by_key(plan, key_name)
        prompt, _ = _render_formal_prompt(cell["task"], int(cell["seed"]))
        (out / f"{key_name}.exact_rendered_prompt.txt").write_text(prompt, encoding="utf8")
    _write_json(out / "preflight_summary.json", checks)
    return checks


def _paths(out: Path, key: str) -> dict[str, Path]:
    """Short on-disk prefixes (radical./fraction.) — full cell_id lives inside artifacts."""
    return {
        "intent": out / f"{key}.call_intent.json",
        "ledger": out / f"{key}.model_call_ledger.json",
        "raw": out / f"{key}.raw_response.txt",
        "code": out / f"{key}.extracted_code.py",
        "artifact": out / f"{key}.cell_artifact.json",
        "lifecycle": out / f"{key}.lifecycle.json",
        "payload": out / f"{key}.request_payload_redacted.json",
        "state": out / f"{key}.system_state.json",
        "prompt": out / f"{key}.exact_rendered_prompt.txt",
    }


def run_cell(out: Path, key: str) -> dict:
    out = Path(out)
    plan = json.loads((out / "frozen_run_plan.json").read_text(encoding="utf8"))
    cell = _cell_by_key(plan, key)
    cid = cell["cell_id"]
    p = _paths(out, key)
    intent_path = p["intent"]
    ledger_path = p["ledger"]
    raw_path = p["raw"]
    code_path = p["code"]
    artifact_path = p["artifact"]
    lifecycle_path = p["lifecycle"]
    payload_path = p["payload"]
    state_path = p["state"]
    prompt_path = p["prompt"]

    if intent_path.exists() or artifact_path.exists() or raw_path.exists():
        raise RuntimeError(f"duplicate cell invocation refused: {cid}")

    checkpoints: list = []
    model_calls = 0

    def persist_lifecycle(status: str):
        _write_json(
            lifecycle_path,
            {
                "cell_id": cid,
                "key": key,
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

    _mark(checkpoints, "CELL_SELECTED", cid, key=key, source_sequence=cell["source_sequence"])
    try:
        if int(cell.get("max_model_calls", 1)) != 1:
            raise RuntimeError("max_model_calls must be 1")
        for flag in ("retry", "resume", "replacement", "replay", "repair", "healer"):
            if int(cell.get(flag, 0)) != 0:
                raise RuntimeError(f"{flag} must be disabled")
        if not api_key_status()["api_key_present"]:
            raise RuntimeError("API_KEY_REQUIRED")

        prompt, frozen = _render_formal_prompt(cell["task"], int(cell["seed"]))
        if prompt_path.exists():
            stored = prompt_path.read_text(encoding="utf8")
            if stored != prompt:
                raise RuntimeError("preflight prompt drifted before call")
        else:
            prompt_path.write_text(prompt, encoding="utf8")
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
                "key": key,
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
        model_calls = 1
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
        artifact = {
            "cohort_run_id": plan["run_id"],
            "key": key,
            "cell_id": cid,
            "source_sequence": cell["source_sequence"],
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
            "timing": {"wall_clock_seconds": wall, "latency_ms": meta.get("latency_ms")},
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
            "system_defects": [],
            "prompt_runtime_mismatch": 0,
            "status": "FINALIZED",
        }
        assert_no_key_leak(artifact)
        _write_json(artifact_path, artifact)
        ledger[0]["status"] = "finalized"
        _write_json(ledger_path, ledger)
        _mark(checkpoints, "CELL_FINALIZED", cid)
        persist_lifecycle("FINALIZED")
        return {"status": "FINALIZED", "cell_id": cid, "key": key, "model_calls": 1}
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
                "key": key,
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
            "key": key,
            "model_calls": model_calls,
            "error": str(exc),
        }


def run_cell_subprocess(out: Path, key: str) -> dict:
    proc = subprocess.run(
        [
            sys.executable,
            str(Path(__file__).resolve()),
            "run-cell",
            "--out",
            str(out),
            "--family",
            key,
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=900,
        env=os.environ.copy(),
    )
    plan = json.loads((out / "frozen_run_plan.json").read_text(encoding="utf8"))
    cell = _cell_by_key(plan, key)
    cid = cell["cell_id"]
    paths = _paths(out, key)
    artifact = paths["artifact"]
    raw = paths["raw"]
    if artifact.exists():
        art = json.loads(artifact.read_text(encoding="utf8"))
        return {
            "status": art.get("status", "FINALIZED"),
            "cell_id": cid,
            "key": key,
            "model_calls": art.get("provenance", {}).get("model_calls", 1),
            "subprocess_returncode": proc.returncode,
        }
    if proc.returncode != 0 and not raw.exists():
        raise RuntimeError(
            f"isolated {key} failed rc={proc.returncode}: {(proc.stderr or proc.stdout)[:2000]}"
        )
    if raw.exists():
        return {
            "status": "RAW_SAVED_OFFLINE_ADJUDICATION_ONLY",
            "key": key,
            "model_calls": 1,
            "subprocess_returncode": proc.returncode,
        }
    return {"status": "UNKNOWN", "key": key, "returncode": proc.returncode}


def _offline_adjudicate_cell(out: Path, cell: dict) -> None:
    cid = cell["cell_id"]
    key = cell["key"]
    paths = _paths(out, key)
    raw_path = paths["raw"]
    artifact_path = paths["artifact"]
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
    if code:
        paths["code"].write_text(code, encoding="utf8")
    ops = resolve_task_operations(cell["task"], frozen)
    scan = scan_toolbox(code or "", cell["task"], frozen)
    completion = "NATURAL_COMPLETE" if code else "EXTRACTION_FAILURE"
    evaluator, verdict, value = _evaluate_generated_code(code, cell["task"], frozen)
    intent = {}
    if paths["intent"].exists():
        intent = json.loads(paths["intent"].read_text(encoding="utf8"))
    ledger = []
    if paths["ledger"].exists():
        ledger = json.loads(paths["ledger"].read_text(encoding="utf8"))
    request = {}
    if paths["payload"].exists():
        request = json.loads(paths["payload"].read_text(encoding="utf8"))
    artifact = {
        "cohort_run_id": json.loads((out / "frozen_run_plan.json").read_text(encoding="utf8"))[
            "run_id"
        ],
        "key": cell["key"],
        "cell_id": cid,
        "source_sequence": cell["source_sequence"],
        "source_edge_cell_id": cell["source_edge_cell_id"],
        "task_id": cell["task"],
        "task_family": cell["task_family"],
        "seed": cell["seed"],
        "model": cell["model"],
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
        },
        "system_defects": [],
        "prompt_runtime_mismatch": 0,
        "status": "FINALIZED",
    }
    _write_json(artifact_path, artifact)


def _cell_pass(art: dict) -> bool:
    return (
        art.get("completion") == "NATURAL_COMPLETE"
        and art.get("adoption_verdict") == "ASSEMBLY_COMPLIANT"
        and art.get("evaluator_verdict") == "PASSED"
        and not (art.get("system_defects") or [])
        and int(art.get("prompt_runtime_mismatch") or 0) == 0
        and int(art.get("provenance", {}).get("model_calls") or 0) == 1
    )


def finalize(out: Path) -> dict:
    out = Path(out)
    plan = json.loads((out / "frozen_run_plan.json").read_text(encoding="utf8"))
    for cell in plan["cells"]:
        _offline_adjudicate_cell(out, cell)

    rows = {}
    system_states = {}
    for cell in plan["cells"]:
        key = cell["key"]
        paths = _paths(out, key)
        if paths["artifact"].exists():
            rows[key] = json.loads(paths["artifact"].read_text(encoding="utf8"))
        if paths["state"].exists():
            system_states[key] = json.loads(paths["state"].read_text(encoding="utf8"))

    per = {}
    for cell in plan["cells"]:
        key = cell["key"]
        art = rows.get(key)
        if not art:
            st = system_states.get(key, {})
            per[key] = {
                "cell_id": cell["cell_id"],
                "source_sequence": cell["source_sequence"],
                "completion": None,
                "toolbox_adoption": None,
                "evaluator": None,
                "model_calls": int(st.get("model_calls") or 0),
                "system_state": st.get("status"),
                "pass": False,
                "blocker": st.get("exception_message") or "MISSING_ARTIFACT",
            }
            continue
        per[key] = {
            "cell_id": art["cell_id"],
            "source_sequence": art["source_sequence"],
            "completion": art.get("completion"),
            "toolbox_adoption": art.get("adoption_verdict"),
            "evaluator": art.get("evaluator_verdict"),
            "evaluator_details": art.get("evaluator_details"),
            "scanner_diagnostics": {
                "classification": (art.get("scanner_diagnostics") or {}).get("classification"),
                "missing_operations": (art.get("scanner_diagnostics") or {}).get(
                    "missing_operations"
                ),
                "irrelevant_api_calls": art.get("irrelevant_api_diagnostics"),
                "called_domain_apis": art.get("called_domain_apis"),
                "result_flow": art.get("result_flow_diagnostics"),
            },
            "model_calls": int(art.get("provenance", {}).get("model_calls") or 0),
            "system_defects": art.get("system_defects") or [],
            "hashes": art.get("hashes"),
            "pass": _cell_pass(art),
        }

    radical_pass = per.get("radical", {}).get("pass") is True
    fraction_pass = per.get("fraction", {}).get("pass") is True
    any_system = any(
        (not rows.get(k) and system_states.get(k))
        or (rows.get(k) and (rows[k].get("system_defects") or []))
        for k in ("radical", "fraction")
    )
    scanner_suspect = False
    evaluator_suspect = False
    model_failure = False
    for key, art in rows.items():
        if _cell_pass(art):
            continue
        adoption = art.get("adoption_verdict")
        evaluator = art.get("evaluator_verdict")
        completion = art.get("completion")
        if completion == "NATURAL_COMPLETE" and evaluator == "PASSED" and adoption != "ASSEMBLY_COMPLIANT":
            scanner_suspect = True
        elif (
            completion == "NATURAL_COMPLETE"
            and adoption == "ASSEMBLY_COMPLIANT"
            and evaluator != "PASSED"
        ):
            evaluator_suspect = True
        elif completion == "NATURAL_COMPLETE" and (
            adoption != "ASSEMBLY_COMPLIANT" or evaluator != "PASSED"
        ):
            model_failure = True
        else:
            any_system = True

    if radical_pass and fraction_pass:
        verdict = "GEMINI35FLASH_RADICAL_FRACTION_POSITIVE_CONTROLS_PASSED"
        decision = "DIRECT_EDGE_FORENSIC"
    elif any_system and not rows:
        verdict = "GEMINI35FLASH_POSITIVE_CONTROL_SYSTEM_BLOCKED"
        decision = "SYSTEM_BLOCKED"
    elif scanner_suspect and not (radical_pass and fraction_pass):
        verdict = "GEMINI35FLASH_POSITIVE_CONTROL_SCANNER_OR_RESOLVER_SUSPECT"
        decision = "CHECK_RESOLVER_SCANNER"
    elif evaluator_suspect and not model_failure:
        verdict = "GEMINI35FLASH_POSITIVE_CONTROL_EVALUATOR_SUSPECT"
        decision = "CHECK_EVALUATOR"
    elif any_system and not (radical_pass or fraction_pass):
        verdict = "GEMINI35FLASH_POSITIVE_CONTROL_SYSTEM_BLOCKED"
        decision = "SYSTEM_BLOCKED"
    else:
        verdict = "GEMINI35FLASH_POSITIVE_CONTROL_MODEL_FAILURE"
        decision = "DIRECT_EDGE_FORENSIC"

    zero = {
        "retry": 0,
        "resume": 0,
        "replacement": 0,
        "repair": 0,
        "replay": 0,
        "healer": 0,
        "total_network_calls": sum(int(v.get("model_calls") or 0) for v in per.values()),
        "per_cell_network_calls": {k: int(v.get("model_calls") or 0) for k, v in per.items()},
        "first_attempt_only": True,
    }
    summary = {
        "run_id": plan["run_id"],
        "model": MODEL_ID,
        "cells": per,
        "radical_pass": radical_pass,
        "fraction_pass": fraction_pass,
        "both_pass": radical_pass and fraction_pass,
        "retry_resume_replacement_repair_replay_healer": zero,
        "verdict": verdict,
        "decision_recommendation": decision,
        "edge_cohort_modified": False,
        "api_key_source": "environment",
        "api_key_present": True,
    }
    hash_integrity = {
        "run_plan_hash": plan["hash"],
        "protocol_hash": _h(PROTOCOL.read_text(encoding="utf8")),
        "cells": {
            plan_cell["key"]: {
                "hashes": rows[plan_cell["key"]].get("hashes") if plan_cell["key"] in rows else None,
                "raw_present": _paths(out, plan_cell["key"])["raw"].exists(),
                "artifact_present": plan_cell["key"] in rows,
                "on_disk_prefix": plan_cell["key"],
                "cell_id": plan_cell["cell_id"],
            }
            for plan_cell in plan["cells"]
        },
        "all_artifacts_present": len(rows) == 2,
        "all_hashes_present": all(
            rows[k].get("hashes", {}).get("prompt")
            and rows[k].get("hashes", {}).get("raw")
            and rows[k].get("hashes", {}).get("extracted_code") is not None
            for k in rows
        )
        if len(rows) == 2
        else False,
    }
    _write_json(out / "positive_controls_summary.json", summary)
    _write_json(out / "hash_integrity.json", hash_integrity)
    _write_json(out / "zero_retry_provenance.json", zero)
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="CE115 v4 Gemini radical/fraction positive controls")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_pre = sub.add_parser("preflight")
    p_pre.add_argument("--out", type=Path, default=DEFAULT_OUT)

    p_run = sub.add_parser("run-cell")
    p_run.add_argument("--out", type=Path, default=DEFAULT_OUT)
    p_run.add_argument("--family", choices=("radical", "fraction"), required=True)

    p_iso = sub.add_parser("run-isolated")
    p_iso.add_argument("--out", type=Path, default=DEFAULT_OUT)
    p_iso.add_argument("--family", choices=("radical", "fraction"), required=True)

    p_fin = sub.add_parser("finalize")
    p_fin.add_argument("--out", type=Path, default=DEFAULT_OUT)

    args = parser.parse_args(argv)
    if args.cmd == "preflight":
        result = run_preflight(args.out)
        print(json.dumps(result, indent=2))
        return 0 if result.get("passed") else 2
    if args.cmd == "run-cell":
        result = run_cell(args.out, args.family)
        print(json.dumps(result, indent=2))
        return 0 if result.get("status") == "FINALIZED" else 1
    if args.cmd == "run-isolated":
        result = run_cell_subprocess(args.out, args.family)
        print(json.dumps(result, indent=2))
        return 0 if result.get("status") == "FINALIZED" else 1
    if args.cmd == "finalize":
        summary = finalize(args.out)
        print(json.dumps(summary, indent=2))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
