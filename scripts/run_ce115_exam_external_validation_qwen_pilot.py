"""Qwen 3.5 4B pilot: 113/114 six-task external validation (6×3=18 cells).

Shares identical clean-incremental builder / canonical prompts / hashes with
the Gemini exam external-validation pilot. First attempt only; retry=0; healer=0.
Does not overwrite existing output dirs. Does not modify freeze/prompt/oracle/evaluator.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
import traceback
from collections import Counter
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.ce115_ab2d_assembly import scan_toolbox
from agent_tools.finals_rebuild.ce115_clean_incremental_ablation import (
    LINEAGE_ID,
    build_condition_prompt,
)
from agent_tools.finals_rebuild.ce115_exam_external_validation import (
    EXPECTED_ANSWERS,
    LINEAGE_NOTE,
    PROVENANCE,
    TASK_IDS,
)
from agent_tools.finals_rebuild.extraction import extract_code
from agent_tools.finals_rebuild.math_boundary_pilot import classify_response
from agent_tools.finals_rebuild.math_task_sampler import sample_task_parameters
from scripts.ce115_qwen_ollama_transport import (
    MODEL_ID as QWEN_MODEL_ID,
    build_chat_payload,
    call_ollama_once,
    probe_ollama,
)
from scripts.preflight_ce115_exam_external_validation import (
    CONDITIONS,
    SEED,
    load_tasks,
    preflight as zero_model_preflight,
)
from scripts.run_ce115_exam_external_validation_gemini_pilot import (
    _classify_failure,
    preliminary_failure_layer,
)

PREFIX = "qwen3_5_4b"
FREEZE_HASHES = ROOT / "docs/experiments/analysis/ce115_exam_ext_113_114_canonical_prompt_hashes.json"
GEMINI_PILOT = ROOT / "docs/experiments/results/ce115_exam_ext_113_114_gemini_pilot_01"
PREFLIGHT_DIR = ROOT / "docs/experiments/results/ce115_exam_ext_113_114_preflight_01"


def _hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )


def build_plan(output_dir: Path, *, service_meta: dict[str, Any]) -> dict[str, Any]:
    tasks = load_tasks()
    cells = []
    hashes: dict[str, dict[str, str]] = {}
    for task_id in TASK_IDS:
        task = tasks[task_id]
        sampled = sample_task_parameters(task, SEED)
        frozen = {
            "task_id": task_id,
            "oracle_type": task["oracle_type"],
            "oracle_payload": sampled["oracle_payload"],
            "repeat_seed": SEED,
        }
        hashes[task_id] = {}
        for condition in CONDITIONS:
            prompt = build_condition_prompt(condition, task, frozen)
            sample = build_chat_payload(prompt, seed=SEED, model=QWEN_MODEL_ID)
            cell_id = f"{PREFIX}__{task_id}__{condition}__seed_{SEED}"
            cells.append(
                {
                    "cell_id": cell_id,
                    "task_id": task_id,
                    "family": task["skill_id"],
                    "condition": condition,
                    "seed": SEED,
                    "model": QWEN_MODEL_ID,
                    "model_digest": service_meta.get("model_digest"),
                    "frozen_parameters": frozen["oracle_payload"],
                    "expected_answer": EXPECTED_ANSWERS[task_id],
                    "prompt": prompt,
                    "canonical_prompt_hash": _hash(prompt),
                    "prompt_hash": _hash(prompt),
                    "prompt_lineage": LINEAGE_ID,
                    "provenance": PROVENANCE[task_id],
                    "first_attempt_only": True,
                    "retry": 0,
                    "healer": 0,
                    "think": False,
                    "request_think": sample["think"],
                    "request_api": "/api/chat",
                }
            )
            hashes[task_id][condition] = _hash(prompt)
    plan: dict[str, Any] = {
        "run_id": output_dir.name,
        "cohort": LINEAGE_NOTE,
        "model_family": "qwen",
        "model": QWEN_MODEL_ID,
        "model_digest": service_meta.get("model_digest"),
        "runtime": "ollama",
        "runtime_version": service_meta.get("runtime_version"),
        "api": "/api/chat",
        "seed": SEED,
        "prompt_lineage": LINEAGE_ID,
        "conditions": list(CONDITIONS),
        "task_ids": list(TASK_IDS),
        "planned_cells": len(cells),
        "cells": cells,
        "canonical_prompt_hashes": hashes,
        "think": False,
        "service_meta": service_meta,
    }
    plan["plan_hash"] = _hash(json.dumps(plan, sort_keys=True, default=str))
    return plan


def structural_preflight(output_dir: Path) -> dict[str, Any]:
    output_dir = Path(output_dir)
    checks: dict[str, Any] = {
        "gemini_pilot_present": (GEMINI_PILOT / "summary.json").is_file()
        and (GEMINI_PILOT / "cell_results.json").is_file(),
        "zero_model_preflight_present": (PREFLIGHT_DIR / "summary.json").is_file(),
        "freeze_hashes_present": FREEZE_HASHES.is_file(),
        "output_isolated": not output_dir.exists(),
        "real_model_calls": 0,
    }
    service_meta: dict[str, Any] | None = None
    sample = build_chat_payload("probe", seed=SEED, model=QWEN_MODEL_ID)
    checks["think_false_top_level"] = sample.get("think") is False and "think" not in sample["options"]
    checks["api_chat"] = sample.get("model") == QWEN_MODEL_ID
    try:
        service_meta = probe_ollama()
        runtime_version = str(service_meta.get("runtime_version") or "")
        checks["ollama_service_available"] = True
        # Accept 0.32.x patch bumps without editing shared transport constants.
        checks["ollama_version_ok"] = bool(service_meta.get("version_ok")) or runtime_version.startswith(
            "0.32."
        )
        checks["model_available"] = bool(
            service_meta.get("model_present") and service_meta.get("digest_ok")
        )
        checks["model_identity"] = service_meta.get("model") == QWEN_MODEL_ID
        checks["real_model_calls"] = int(service_meta.get("chat_calls") or 0)
        checks["ollama_runtime_version"] = runtime_version
        checks["model_digest"] = service_meta.get("model_digest")
    except Exception as exc:
        checks["ollama_service_available"] = False
        checks["ollama_version_ok"] = False
        checks["model_available"] = False
        checks["model_identity"] = False
        checks["ollama_error"] = f"{type(exc).__name__}: {exc}"

    zm = zero_model_preflight(output_dir)
    freeze = json.loads(FREEZE_HASHES.read_text(encoding="utf-8"))
    checks["zero_model_preflight_passed"] = zm["checks"]["passed"] is True
    checks["hashes_match_freeze"] = zm["canonical_prompt_hashes"] == freeze
    checks["planned_cells_exactly_18"] = zm["checks"].get("planned_cells_exactly_18") is True
    checks["no_healer"] = zm["checks"].get("no_healer") is True

    skip = {"real_model_calls", "ollama_error", "blocker", "ollama_runtime_version", "model_digest"}
    structural_ok = all(v is True for k, v in checks.items() if k not in skip and isinstance(v, bool))
    checks["passed"] = structural_ok and checks["real_model_calls"] == 0
    checks["blocker"] = None if checks["passed"] else "PREFLIGHT_FAILED"
    return {
        "checks": checks,
        "service_meta": service_meta,
        "canonical_prompt_hashes": zm["canonical_prompt_hashes"],
        "zero_model": {k: zm["checks"][k] for k in ("passed", "real_model_calls") if k in zm["checks"]},
    }


def run(
    output_dir: Path,
    *,
    transport: Callable[[str], dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    output_dir = Path(output_dir)
    if output_dir.exists():
        raise RuntimeError(f"output directory already exists: {output_dir}")
    pf = structural_preflight(output_dir)
    if not pf["checks"]["passed"]:
        raise RuntimeError(pf["checks"]["blocker"] or "PREFLIGHT_FAILED")
    service_meta = pf["service_meta"] or {}
    transport = transport or (lambda prompt: call_ollama_once(prompt, seed=SEED, model=QWEN_MODEL_ID))

    output_dir.mkdir(parents=True)
    _write_json(
        output_dir / "preflight.json",
        {
            "checks": pf["checks"],
            "service_meta": service_meta,
            "canonical_prompt_hashes": pf["canonical_prompt_hashes"],
            "real_model_calls": 0,
        },
    )
    plan = build_plan(output_dir, service_meta=service_meta)
    if plan["canonical_prompt_hashes"] != pf["canonical_prompt_hashes"]:
        raise RuntimeError("canonical prompt hash drift vs freeze/preflight")
    _write_json(output_dir / "manifest.json", plan)

    tasks = load_tasks()
    rows: list[dict[str, Any]] = []
    model_calls = 0
    for cell in plan["cells"]:
        task = tasks[cell["task_id"]]
        cell_dir = output_dir / "cells" / cell["cell_id"]
        cell_dir.mkdir(parents=True)
        prompt = cell["prompt"]
        (cell_dir / "prompt.txt").write_text(prompt, encoding="utf-8")
        started = time.monotonic()
        raw = ""
        code = None
        exception_type = exception_message = trace = None
        metadata: dict[str, Any] = {}
        completion = "INFRASTRUCTURE_FAILURE"
        adoption = "NOT_APPLICABLE"
        evaluator = "NOT_RUN"
        details: dict[str, Any] = {}
        parse_status = "not_run"
        predicted = None
        try:
            response = transport(prompt)
            raw = response["raw_text"]
            if raw:
                model_calls += 1
            metadata = dict(response.get("metadata") or {})
            extraction = extract_code(raw)
            parse_status = extraction.extraction_status
            code = extraction.extracted_code if extraction.extraction_status == "extracted" else None
            completion = "NATURAL_COMPLETE" if code else "EXTRACTION_FAILURE"
            outcome, evaluated_code, details = classify_response(
                raw, {"oracle_payload": cell["frozen_parameters"]}, task
            )
            code = evaluated_code or code
            evaluator = "PASSED" if outcome == "passed" else outcome.upper()
            if isinstance(details.get("returned_value"), dict):
                predicted = details["returned_value"].get("correct_answer")
            if cell["condition"] == "ab2d" and code:
                adoption = scan_toolbox(code, cell["task_id"], cell["frozen_parameters"])[
                    "classification"
                ]
        except BaseException as exc:
            exception_type, exception_message = type(exc).__name__, str(exc)
            trace = traceback.format_exc()
            parse_status = "infrastructure_failure"
            evaluator = "INFRASTRUCTURE_FAILURE"
        wall = time.monotonic() - started
        (cell_dir / "raw_response.txt").write_text(raw, encoding="utf-8")
        if code is not None:
            (cell_dir / "extracted_candidate.py").write_text(code, encoding="utf-8")
        artifact = {k: v for k, v in cell.items() if k != "prompt"}
        artifact.update(
            {
                "run_id": plan["run_id"],
                "model_family": "qwen",
                "completion_status": completion,
                "parse_status": parse_status,
                "adoption_status": adoption,
                "evaluator_status": evaluator,
                "predicted_answer": predicted,
                "failure_class": _classify_failure(completion, evaluator, exception_type),
                "failure_layer": preliminary_failure_layer(evaluator),
                "exception_type": exception_type,
                "exception_message": exception_message,
                "traceback": trace,
                "evaluator_details": details,
                "token_metadata": metadata,
                "duration_metadata": {
                    "wall_clock_seconds": wall,
                    "provider_duration": metadata.get("total_duration"),
                    "latency_ms": metadata.get("latency_ms"),
                },
                "code_size_chars": len(code or ""),
                "infrastructure_valid": exception_type is None and bool(raw),
                "hashes": {
                    "prompt": _hash(prompt),
                    "raw": _hash(raw),
                    "extracted_candidate": _hash(code or ""),
                },
                "provenance_run": {
                    "first_attempt_only": True,
                    "retry": 0,
                    "healer": 0,
                    "model_calls": 1 if raw else 0,
                    "think": False,
                },
            }
        )
        artifact["artifact_sha256"] = _hash(
            json.dumps(
                {k: v for k, v in artifact.items() if k != "artifact_sha256"},
                sort_keys=True,
                default=str,
            )
        )
        _write_json(cell_dir / "artifact.json", artifact)
        rows.append(artifact)
        print(
            json.dumps(
                {
                    "progress": f"{len(rows)}/18",
                    "cell_id": cell["cell_id"],
                    "evaluator_status": evaluator,
                    "failure_layer": artifact["failure_layer"].get("primary_layer"),
                    "model_calls_so_far": model_calls,
                },
                ensure_ascii=False,
            ),
            flush=True,
        )

    by_condition: dict[str, Any] = {}
    for condition in CONDITIONS:
        subset = [r for r in rows if r["condition"] == condition]
        by_condition[condition] = {
            "cells": len(subset),
            "evaluable": sum(
                r["evaluator_status"]
                not in {"NOT_RUN", "EXTRACTION_FAILURE", "INFRASTRUCTURE_FAILURE"}
                for r in subset
            ),
            "execution_pass": sum(r["evaluator_status"] == "PASSED" for r in subset),
            "exact_pass": sum(r["evaluator_status"] == "PASSED" for r in subset),
            "failure_count": sum(r["failure_class"] != "none" for r in subset),
            "infrastructure_failures": sum(
                r["failure_class"] == "transport_or_infrastructure_failure" for r in subset
            ),
            "wall_clock_seconds": sum(r["duration_metadata"]["wall_clock_seconds"] for r in subset),
            "total_token_count": sum(
                (r.get("token_metadata") or {}).get("total_token_count") or 0 for r in subset
            ),
        }
    by_task: dict[str, Any] = {}
    for task_id in TASK_IDS:
        subset = [r for r in rows if r["task_id"] == task_id]
        by_task[task_id] = {
            condition: next(r["evaluator_status"] for r in subset if r["condition"] == condition)
            for condition in CONDITIONS
        }
        by_task[task_id]["failure_layers"] = {
            r["condition"]: r["failure_layer"].get("primary_layer") for r in subset
        }
        by_task[task_id]["pass_count"] = sum(r["evaluator_status"] == "PASSED" for r in subset)
    layer_counts = Counter(r["failure_layer"].get("primary_layer") or "PASSED" for r in rows)
    ab2d = [r for r in rows if r["condition"] == "ab2d"]
    summary = {
        "cohort": LINEAGE_NOTE,
        "model_family": "qwen",
        "model": QWEN_MODEL_ID,
        "model_digest": service_meta.get("model_digest"),
        "runtime_version": service_meta.get("runtime_version"),
        "seed": SEED,
        "conditions": by_condition,
        "by_task": by_task,
        "failure_classes": dict(Counter(r["failure_class"] for r in rows)),
        "failure_layer_distribution": dict(layer_counts),
        "canonical_prompt_hashes": plan["canonical_prompt_hashes"],
        "real_model_calls": model_calls,
        "retries": 0,
        "healer_calls": 0,
        "infrastructure_failures": sum(
            r["failure_class"] == "transport_or_infrastructure_failure" for r in rows
        ),
        "healer_used": False,
        "cells": len(rows),
        "unique_cell_ids": len({r["cell_id"] for r in rows}),
        "domain_adoption_ab2d": dict(Counter(r["adoption_status"] for r in ab2d)),
        "code_size_chars": {
            "mean": round(sum(r["code_size_chars"] for r in rows) / max(len(rows), 1), 1),
            "max": max((r["code_size_chars"] for r in rows), default=0),
            "min": min((r["code_size_chars"] for r in rows), default=0),
        },
        "token_totals": {
            "prompt_eval_count": sum(
                (r.get("token_metadata") or {}).get("prompt_eval_count") or 0 for r in rows
            ),
            "eval_count": sum((r.get("token_metadata") or {}).get("eval_count") or 0 for r in rows),
            "total_token_count": sum(
                (r.get("token_metadata") or {}).get("total_token_count") or 0 for r in rows
            ),
        },
        "combined_census_ready_hint": (
            model_calls == 18
            and len(rows) == 18
            and len({r["cell_id"] for r in rows}) == 18
            and sum(r["failure_class"] == "transport_or_infrastructure_failure" for r in rows) == 0
        ),
    }
    _write_json(output_dir / "cell_results.json", rows)
    _write_json(output_dir / "summary.json", summary)
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description="CE115 exam external-validation Qwen 18-cell pilot")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "docs/experiments/results/ce115_exam_ext_113_114_qwen_pilot_01",
    )
    parser.add_argument("--preflight-only", action="store_true")
    args = parser.parse_args()
    if args.preflight_only:
        pf = structural_preflight(args.output_dir)
        print(json.dumps(pf, ensure_ascii=False, indent=2, default=str))
        return 0 if pf["checks"]["passed"] else 2
    rows = run(args.output_dir)
    print(
        json.dumps(
            {
                "output_dir": str(args.output_dir),
                "cells": len(rows),
                "real_model_calls": sum(r["provenance_run"]["model_calls"] for r in rows),
                "passed": sum(r["evaluator_status"] == "PASSED" for r in rows),
                "failure_layer_distribution": dict(
                    Counter((r["failure_layer"].get("primary_layer") or "PASSED") for r in rows)
                ),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
