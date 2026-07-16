"""Nine-cell CE115 Gemini 3.5 Flash pilot (Ab1, Ab2g, Ab2d-v4)."""
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
from agent_tools.finals_rebuild.extraction import extract_code
from agent_tools.finals_rebuild.math_boundary_pilot import (
    classify_response,
    frozen_payloads,
    load_pilot_tasks,
)
from scripts.ce115_v4_gemini_transport import MODEL_ID, call_gemini_once

TASK_MANIFEST = ROOT / "tests/finals_rebuild/fixtures/math_generation_tasks_ce115_pilot.jsonl"
TASK_IDS = (
    "ce115_calc_polynomial_division_l1",
    "ce115_calc_radical_simplification_l1",
    "ce115_calc_exact_rational_expression_l1",
)
EXCLUDED_TASK = "ce115_calc_polynomial_factor_roots_l1"
CONDITIONS = ("ab1", "ab2g", "ab2d")
SEED = 2026071301


def _hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")


def _tasks() -> dict[str, dict[str, Any]]:
    loaded = {task["task_id"]: task for task in load_pilot_tasks(TASK_MANIFEST)}
    return {task_id: loaded[task_id] for task_id in TASK_IDS}


def build_plan(output_dir: Path) -> dict[str, Any]:
    tasks = _tasks()
    frozen_by_task = {
        row["task_id"]: row for row in frozen_payloads(tasks.values(), (SEED,))
    }
    cells = []
    for task_id in TASK_IDS:
        task = tasks[task_id]
        frozen = frozen_by_task[task_id]
        for condition in CONDITIONS:
            params = frozen["oracle_payload"]
            prompt = build_condition_prompt(condition, task, frozen)
            cell_id = f"gemini_3_5_flash__{task_id}__{condition}__seed_{SEED}"
            cells.append({
                "cell_id": cell_id, "task_id": task_id, "family": task["skill_id"],
                "condition": condition, "seed": SEED, "model": MODEL_ID,
                "frozen_parameters": params, "prompt": prompt, "prompt_hash": _hash(prompt),
                "prompt_lineage": LINEAGE_ID,
                "first_attempt_only": True, "retry": 0, "healer": 0,
            })
    plan = {
        "run_id": output_dir.name, "model": MODEL_ID, "seed": SEED,
        "prompt_lineage": LINEAGE_ID,
        "conditions": list(CONDITIONS), "task_ids": list(TASK_IDS),
        "structural_exclusions": [{"task_id": EXCLUDED_TASK, "reason": "STRUCTURAL_EXCLUSION_ASSEMBLY_COVERAGE_UNAVAILABLE"}],
        "planned_cells": len(cells), "cells": cells,
    }
    plan["plan_hash"] = _hash(json.dumps(plan, sort_keys=True))
    return plan


def preflight(output_dir: Path, *, require_api_key: bool = True) -> dict[str, Any]:
    output_dir = Path(output_dir)
    plan = build_plan(output_dir)
    identities: dict[str, set[str]] = {}
    for cell in plan["cells"]:
        identities.setdefault(cell["task_id"], set()).add(
            _hash(json.dumps(cell["frozen_parameters"], sort_keys=True))
        )
    checks = {
        "planned_cells_exactly_9": len(plan["cells"]) == 9,
        "matrix_exact": len({(c["task_id"], c["condition"]) for c in plan["cells"]}) == 9,
        "frozen_identity_cross_condition": all(len(values) == 1 for values in identities.values()),
        "seed_consistent": {c["seed"] for c in plan["cells"]} == {SEED},
        "model_consistent": {c["model"] for c in plan["cells"]} == {"gemini-3.5-flash"},
        "prompt_builders_nonempty": all(c["prompt"].strip() for c in plan["cells"]),
        "clean_incremental_ab2d": all(
            "## Clean-incremental DOMAIN" in c["prompt"] and "CE115 Ab2d-Assembly domain contract" not in c["prompt"]
            for c in plan["cells"] if c["condition"] == "ab2d"
        ),
        "clean_incremental_ab2g": all(
            "## Clean-incremental GENERIC" in c["prompt"] and "PolynomialOps" not in c["prompt"]
            for c in plan["cells"] if c["condition"] == "ab2g"
        ),
        "ab1_uncontaminated": all(
            "## Clean-incremental GENERIC" not in c["prompt"] and "PolynomialOps" not in c["prompt"]
            for c in plan["cells"] if c["condition"] == "ab1"
        ),
        "fourth_task_excluded": EXCLUDED_TASK not in {c["task_id"] for c in plan["cells"]},
        "output_isolated": not output_dir.exists(),
        "api_key_present": bool(os.getenv("GEMINI_API_KEY")),
        "real_model_calls": 0,
    }
    checks["passed"] = all(value for key, value in checks.items() if key not in {"real_model_calls", "api_key_present"}) and (checks["api_key_present"] or not require_api_key)
    checks["blocker"] = None if checks["passed"] else ("API_KEY_REQUIRED" if not checks["api_key_present"] and require_api_key else "PREFLIGHT_FAILED")
    return {"run_id": plan["run_id"], "checks": checks, "plan": plan}


def _classify_failure(completion: str, evaluator: str, exception_type: str | None) -> str:
    if exception_type:
        return "transport_or_infrastructure_failure"
    if completion != "NATURAL_COMPLETE":
        return "model_generated_failure"
    if evaluator != "PASSED":
        return "model_generated_failure"
    return "none"


def run(output_dir: Path, *, transport: Callable[[str], dict[str, Any]] = call_gemini_once, require_api_key: bool = True) -> list[dict[str, Any]]:
    output_dir = Path(output_dir)
    pf = preflight(output_dir, require_api_key=require_api_key)
    if not pf["checks"]["passed"]:
        raise RuntimeError(pf["checks"]["blocker"] or "PREFLIGHT_FAILED")
    output_dir.mkdir(parents=True)
    _write_json(output_dir / "manifest.json", pf["plan"])
    _write_json(output_dir / "preflight.json", pf["checks"])
    tasks = _tasks()
    rows = []
    for cell in pf["plan"]["cells"]:
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
        try:
            response = transport(prompt)
            raw = response["raw_text"]
            metadata = dict(response.get("metadata") or {})
            extraction = extract_code(raw)
            code = extraction.extracted_code if extraction.extraction_status == "extracted" else None
            completion = "NATURAL_COMPLETE" if code else "EXTRACTION_FAILURE"
            outcome, evaluated_code, details = classify_response(raw, {"oracle_payload": cell["frozen_parameters"]}, tasks[cell["task_id"]])
            code = evaluated_code or code
            evaluator = "PASSED" if outcome == "passed" else outcome.upper()
            adoption = scan_toolbox(code or "", cell["task_id"], cell["frozen_parameters"])["classification"] if cell["condition"] == "ab2d" else "NOT_APPLICABLE"
        except BaseException as exc:
            exception_type, exception_message = type(exc).__name__, str(exc)
            trace = traceback.format_exc()
        wall = time.monotonic() - started
        (cell_dir / "raw_response.txt").write_text(raw, encoding="utf-8")
        if code is not None:
            (cell_dir / "extracted_candidate.py").write_text(code, encoding="utf-8")
        artifact = {k: v for k, v in cell.items() if k != "prompt"}
        artifact.update({
            "run_id": pf["plan"]["run_id"], "completion_status": completion,
            "adoption_status": adoption, "evaluator_status": evaluator,
            "failure_class": _classify_failure(completion, evaluator, exception_type),
            "exception_type": exception_type, "exception_message": exception_message,
            "traceback": trace, "evaluator_details": details,
            "token_metadata": metadata, "duration_metadata": {"wall_clock_seconds": wall, "provider_duration": metadata.get("latency_ms")},
            "hashes": {"prompt": _hash(prompt), "raw": _hash(raw), "extracted_candidate": _hash(code or "")},
            "provenance": {"first_attempt_only": True, "retry": 0, "healer": 0, "model_calls": 1 if raw else 0},
        })
        _write_json(cell_dir / "artifact.json", artifact)
        rows.append(artifact)
    _write_json(output_dir / "cell_results.json", rows)
    by_condition = {}
    for condition in CONDITIONS:
        subset = [r for r in rows if r["condition"] == condition]
        by_condition[condition] = {
            "cells": 3, "evaluable": sum(r["evaluator_status"] not in {"NOT_RUN", "EXTRACTION_FAILURE"} for r in subset),
            "execution_pass": sum(r["evaluator_status"] == "PASSED" for r in subset),
            "exact_pass": sum(r["evaluator_status"] == "PASSED" for r in subset),
            "failure_count": sum(r["failure_class"] != "none" for r in subset),
            "token_count": sum((r["token_metadata"].get("total_token_count") or 0) for r in subset),
            "wall_clock_seconds": sum(r["duration_metadata"]["wall_clock_seconds"] for r in subset),
        }
    _write_json(output_dir / "summary.json", {"conditions": by_condition, "failure_classes": dict(Counter(r["failure_class"] for r in rows))})
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "docs/experiments/results/ce115_gemini_three_condition_pilot_20260716_01")
    args = parser.parse_args()
    pf = preflight(args.output_dir)
    if args.preflight_only:
        print(json.dumps(pf, ensure_ascii=False, indent=2, default=str))
        return 0 if pf["checks"]["passed"] else 2
    rows = run(args.output_dir)
    print(json.dumps({"output_dir": str(args.output_dir), "cells": len(rows)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
