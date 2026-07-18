"""Gemini 3.5 Flash pilot: 113/114 six-task external validation (6×3=18 cells).

Shared clean-incremental prompts. First attempt only; retry=0; healer=0.
Does not run Qwen. Does not modify prompt/oracle/evaluator after cells run.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
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
from scripts.ce115_v4_gemini_transport import MODEL_ID as GEMINI_MODEL_ID, call_gemini_once
from scripts.preflight_ce115_exam_external_validation import (
    CONDITIONS,
    SEED,
    load_tasks,
    preflight as zero_model_preflight,
    write_preflight_artifacts,
)

PREFIX = "gemini_3_5_flash"


def _hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )


def preliminary_failure_layer(evaluator_status: str) -> dict[str, Any]:
    status = evaluator_status.upper()
    if status == "PASSED":
        return {"primary_layer": None, "eligibility": "N/A", "note": "passed"}
    if status in {
        "PARSE_MINOR",
        "EXTRACTION_FAILURE",
        "MISSING_ENTRY_POINT",
        "CATASTROPHIC_TRUNCATION",
        "EMPTY_RESPONSE",
    }:
        return {"primary_layer": "L1", "eligibility": "CONDITIONAL", "note": "parse/extract class"}
    if status == "SCHEMA_FAILURE":
        return {"primary_layer": "L2", "eligibility": "CONDITIONAL", "note": "schema"}
    if status == "RUNTIME_FAILURE":
        return {"primary_layer": "L4", "latent_layers": ["L5"], "eligibility": "CONDITIONAL", "note": "runtime"}
    if status == "ANSWER_INCORRECT":
        return {"primary_layer": "L5", "eligibility": "INELIGIBLE", "note": "answer semantics"}
    if status == "INTRINSIC_SAFETY":
        return {"primary_layer": "L5", "eligibility": "INELIGIBLE", "note": "oracle rejected payload"}
    if status in {"NOT_RUN", "INFRASTRUCTURE_FAILURE"} or "INFRASTRUCTURE" in status:
        return {"primary_layer": "L0", "eligibility": "INFRA", "note": "transport/infrastructure"}
    return {"primary_layer": "META", "eligibility": "UNKNOWN", "note": status}


def _classify_failure(completion: str, evaluator: str, exception_type: str | None) -> str:
    if exception_type:
        return "transport_or_infrastructure_failure"
    if completion != "NATURAL_COMPLETE":
        return "model_generated_failure"
    if evaluator != "PASSED":
        return "model_generated_failure"
    return "none"


def build_plan(output_dir: Path) -> dict[str, Any]:
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
            cell_id = f"{PREFIX}__{task_id}__{condition}__seed_{SEED}"
            cells.append(
                {
                    "cell_id": cell_id,
                    "task_id": task_id,
                    "family": task["skill_id"],
                    "condition": condition,
                    "seed": SEED,
                    "model": GEMINI_MODEL_ID,
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
                }
            )
            hashes[task_id][condition] = _hash(prompt)
    plan = {
        "run_id": output_dir.name,
        "cohort": LINEAGE_NOTE,
        "model_family": "gemini",
        "model": GEMINI_MODEL_ID,
        "seed": SEED,
        "prompt_lineage": LINEAGE_ID,
        "conditions": list(CONDITIONS),
        "task_ids": list(TASK_IDS),
        "planned_cells": len(cells),
        "cells": cells,
        "canonical_prompt_hashes": hashes,
        "think": False,
    }
    plan["plan_hash"] = _hash(json.dumps(plan, sort_keys=True, default=str))
    return plan


def run(
    output_dir: Path,
    *,
    transport: Callable[[str], dict[str, Any]] | None = None,
    require_api_key: bool = True,
) -> list[dict[str, Any]]:
    output_dir = Path(output_dir)
    if output_dir.exists():
        raise RuntimeError(f"output directory already exists: {output_dir}")
    zm = zero_model_preflight(output_dir)
    if not zm["checks"]["passed"]:
        raise RuntimeError(zm["checks"]["blocker"] or "ZERO_MODEL_PREFLIGHT_FAILED")
    if require_api_key and not os.getenv("GEMINI_API_KEY"):
        raise RuntimeError("API_KEY_REQUIRED")
    transport = transport or call_gemini_once
    write_preflight_artifacts(output_dir, zm)
    plan = build_plan(output_dir)
    # Freeze hashes must match zero-model preflight
    if plan["canonical_prompt_hashes"] != zm["canonical_prompt_hashes"]:
        raise RuntimeError("canonical prompt hash drift vs zero-model preflight")
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
                "model_family": "gemini",
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
                    "provider_duration": metadata.get("latency_ms"),
                    "latency_ms": metadata.get("latency_ms"),
                },
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

    by_condition: dict[str, Any] = {}
    for condition in CONDITIONS:
        subset = [r for r in rows if r["condition"] == condition]
        by_condition[condition] = {
            "cells": len(subset),
            "evaluable": sum(
                r["evaluator_status"] not in {"NOT_RUN", "EXTRACTION_FAILURE", "INFRASTRUCTURE_FAILURE"}
                for r in subset
            ),
            "execution_pass": sum(r["evaluator_status"] == "PASSED" for r in subset),
            "exact_pass": sum(r["evaluator_status"] == "PASSED" for r in subset),
            "failure_count": sum(r["failure_class"] != "none" for r in subset),
            "infrastructure_failures": sum(
                r["failure_class"] == "transport_or_infrastructure_failure" for r in subset
            ),
            "wall_clock_seconds": sum(r["duration_metadata"]["wall_clock_seconds"] for r in subset),
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
    layer_counts = Counter(
        r["failure_layer"].get("primary_layer") or "PASSED" for r in rows
    )
    summary = {
        "cohort": LINEAGE_NOTE,
        "model_family": "gemini",
        "model": GEMINI_MODEL_ID,
        "seed": SEED,
        "conditions": by_condition,
        "by_task": by_task,
        "failure_classes": dict(Counter(r["failure_class"] for r in rows)),
        "failure_layer_distribution": dict(layer_counts),
        "canonical_prompt_hashes": plan["canonical_prompt_hashes"],
        "real_model_calls": model_calls,
        "infrastructure_failures": sum(
            r["failure_class"] == "transport_or_infrastructure_failure" for r in rows
        ),
        "healer_used": False,
        "cells": len(rows),
        "qwen_external_validation_ready_hint": (
            model_calls == 18
            and sum(r["failure_class"] == "transport_or_infrastructure_failure" for r in rows) == 0
        ),
    }
    _write_json(output_dir / "cell_results.json", rows)
    _write_json(output_dir / "summary.json", summary)
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description="CE115 exam external-validation Gemini 18-cell pilot")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "docs/experiments/results/ce115_exam_ext_113_114_gemini_pilot_01",
    )
    parser.add_argument("--preflight-only", action="store_true")
    args = parser.parse_args()
    if args.preflight_only:
        pf = zero_model_preflight(args.output_dir)
        write_preflight_artifacts(args.output_dir, pf)
        print(json.dumps({"passed": pf["checks"]["passed"], "hashes": pf["canonical_prompt_hashes"]}, indent=2))
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
