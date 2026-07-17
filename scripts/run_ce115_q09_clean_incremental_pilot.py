"""CE115 Q9 clean-incremental formal pilot: 1 task × 3 conditions.

Gemini and Qwen share identical canonical prompts from
ce115_clean_incremental_ablation_v1. First attempt only; no retry; no Healer.
Does not re-run or overwrite the existing three-task pilot artifacts.
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
from agent_tools.finals_rebuild.extraction import extract_code
from agent_tools.finals_rebuild.math_boundary_pilot import classify_response
from agent_tools.finals_rebuild.math_task_sampler import sample_task_parameters
from scripts.ce115_qwen_ollama_transport import (
    MODEL_ID as QWEN_MODEL_ID,
    build_chat_payload,
    call_ollama_once,
    probe_ollama,
)
from scripts.ce115_v4_gemini_transport import MODEL_ID as GEMINI_MODEL_ID, call_gemini_once

TASK_MANIFEST = ROOT / "tests/finals_rebuild/fixtures/math_generation_tasks_ce115_pilot.jsonl"
TASK_ID = "ce115_calc_common_factor_quadratic_root_ordering_l1"
CONDITIONS = ("ab1", "ab2g", "ab2d")
SEED = 2026071301
FROZEN_HASHES = {
    "ab1": "e54e0d4ad7466eb64122a8ee1884961170e6a48a693aa3fab26dcb53f8ae6502",
    "ab2g": "093996247d4f3ca8549b829088c9a5abcfe2ff0c35b91e124acd31921784482b",
    "ab2d": "dadc0af70d7ff874a7f9e247eb2a7e38bb205ebe02bfcafc892f174167ea64c1",
}
EXISTING_THREE = (
    "ce115_calc_polynomial_division_l1",
    "ce115_calc_radical_simplification_l1",
    "ce115_calc_exact_rational_expression_l1",
)


def _hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )


def load_task() -> dict[str, Any]:
    rows = [
        json.loads(line)
        for line in TASK_MANIFEST.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    by_id = {row["task_id"]: row for row in rows}
    if TASK_ID not in by_id:
        raise ValueError(f"missing task {TASK_ID}")
    return by_id[TASK_ID]


def _frozen(task: dict[str, Any]) -> dict[str, Any]:
    sampled = sample_task_parameters(task, SEED)
    return {
        "task_id": TASK_ID,
        "oracle_type": task["oracle_type"],
        "oracle_payload": sampled["oracle_payload"],
        "repeat_seed": SEED,
    }


def build_plan(output_dir: Path, *, family: str) -> dict[str, Any]:
    if family not in {"gemini", "qwen"}:
        raise ValueError(f"unsupported family: {family}")
    task = load_task()
    frozen = _frozen(task)
    model = GEMINI_MODEL_ID if family == "gemini" else QWEN_MODEL_ID
    prefix = "gemini_3_5_flash" if family == "gemini" else "qwen3_5_4b"
    cells = []
    for condition in CONDITIONS:
        prompt = build_condition_prompt(condition, task, frozen)
        cell: dict[str, Any] = {
            "cell_id": f"{prefix}__{TASK_ID}__{condition}__seed_{SEED}",
            "task_id": TASK_ID,
            "family": task["skill_id"],
            "condition": condition,
            "seed": SEED,
            "model": model,
            "frozen_parameters": frozen["oracle_payload"],
            "prompt": prompt,
            "canonical_prompt_hash": _hash(prompt),
            "prompt_hash": _hash(prompt),
            "prompt_lineage": LINEAGE_ID,
            "first_attempt_only": True,
            "retry": 0,
            "healer": 0,
            "think": False,
        }
        if family == "qwen":
            sample = build_chat_payload(prompt, seed=SEED, model=QWEN_MODEL_ID)
            cell["request_think"] = sample["think"]
            cell["request_api"] = "/api/chat"
        cells.append(cell)
    plan: dict[str, Any] = {
        "run_id": output_dir.name,
        "model_family": family,
        "model": model,
        "seed": SEED,
        "prompt_lineage": LINEAGE_ID,
        "conditions": list(CONDITIONS),
        "task_ids": [TASK_ID],
        "excluded_existing_three": list(EXISTING_THREE),
        "planned_cells": len(cells),
        "cells": cells,
        "think": False,
    }
    if family == "qwen":
        plan["runtime"] = "ollama"
        plan["api"] = "/api/chat"
    plan["plan_hash"] = _hash(json.dumps(plan, sort_keys=True, default=str))
    return plan


def preflight(output_dir: Path, *, family: str, require_service: bool = True) -> dict[str, Any]:
    output_dir = Path(output_dir)
    plan = build_plan(output_dir, family=family)
    hashes = {c["condition"]: c["canonical_prompt_hash"] for c in plan["cells"]}
    frozen_ids = {
        c["condition"]: _hash(json.dumps(c["frozen_parameters"], sort_keys=True))
        for c in plan["cells"]
    }
    checks: dict[str, Any] = {
        "planned_cells_exactly_3": len(plan["cells"]) == 3,
        "matrix_exact": {c["condition"] for c in plan["cells"]} == set(CONDITIONS),
        "only_q09_task": plan["task_ids"] == [TASK_ID],
        "existing_three_not_included": all(t not in plan["task_ids"] for t in EXISTING_THREE),
        "frozen_identity_cross_condition": len(set(frozen_ids.values())) == 1,
        "seed_consistent": {c["seed"] for c in plan["cells"]} == {SEED},
        "prompt_builders_nonempty": all(c["prompt"].strip() for c in plan["cells"]),
        "canonical_hashes_match_freeze": hashes == FROZEN_HASHES,
        "clean_incremental_ab1": all(
            "## Clean-incremental GENERIC" not in c["prompt"] for c in plan["cells"] if c["condition"] == "ab1"
        ),
        "clean_incremental_ab2g": all(
            "## Clean-incremental GENERIC" in c["prompt"] and "FractionOps" not in c["prompt"]
            for c in plan["cells"]
            if c["condition"] == "ab2g"
        ),
        "clean_incremental_ab2d": all(
            "## Clean-incremental DOMAIN" in c["prompt"]
            and "CE115 Ab2d-Assembly domain contract" not in c["prompt"]
            for c in plan["cells"]
            if c["condition"] == "ab2d"
        ),
        "no_healer": all(c["healer"] == 0 and c["retry"] == 0 for c in plan["cells"]),
        "think_false": all(c.get("think") is False for c in plan["cells"]),
        "output_isolated": not output_dir.exists(),
        "real_model_calls": 0,
    }
    service_meta: dict[str, Any] | None = None
    if family == "gemini":
        checks["model_consistent"] = {c["model"] for c in plan["cells"]} == {GEMINI_MODEL_ID}
        checks["api_key_present"] = bool(os.getenv("GEMINI_API_KEY"))
        structural_ok = all(
            checks[k]
            for k in checks
            if k not in {"real_model_calls", "api_key_present"}
        )
        service_ok = checks["api_key_present"] or not require_service
        checks["passed"] = structural_ok and service_ok and checks["real_model_calls"] == 0
        if checks["passed"]:
            checks["blocker"] = None
        elif not checks["api_key_present"] and require_service:
            checks["blocker"] = "API_KEY_REQUIRED"
        else:
            checks["blocker"] = "PREFLIGHT_FAILED"
    else:
        sample = build_chat_payload("probe", seed=SEED, model=QWEN_MODEL_ID)
        checks["model_consistent"] = {c["model"] for c in plan["cells"]} == {QWEN_MODEL_ID}
        checks["think_false_top_level"] = sample.get("think") is False and "think" not in sample["options"]
        checks["api_chat"] = sample.get("model") == QWEN_MODEL_ID
        checks["ollama_service_available"] = False
        checks["ollama_version_ok"] = False
        checks["model_available"] = False
        if require_service:
            try:
                service_meta = probe_ollama()
                checks["ollama_service_available"] = True
                checks["ollama_version_ok"] = bool(service_meta.get("version_ok"))
                checks["model_available"] = bool(
                    service_meta.get("model_present") and service_meta.get("digest_ok")
                )
                checks["real_model_calls"] = int(service_meta.get("chat_calls") or 0)
            except Exception as exc:
                checks["ollama_error"] = f"{type(exc).__name__}: {exc}"
        else:
            checks["ollama_service_available"] = True
            checks["ollama_version_ok"] = True
            checks["model_available"] = True
        structural_keys = [
            "planned_cells_exactly_3",
            "matrix_exact",
            "only_q09_task",
            "existing_three_not_included",
            "frozen_identity_cross_condition",
            "seed_consistent",
            "prompt_builders_nonempty",
            "canonical_hashes_match_freeze",
            "clean_incremental_ab1",
            "clean_incremental_ab2g",
            "clean_incremental_ab2d",
            "no_healer",
            "think_false",
            "output_isolated",
            "model_consistent",
            "think_false_top_level",
            "api_chat",
        ]
        service_keys = ["ollama_service_available", "ollama_version_ok", "model_available"]
        structural_ok = all(checks[k] for k in structural_keys)
        service_ok = all(checks[k] for k in service_keys)
        checks["passed"] = structural_ok and service_ok and checks["real_model_calls"] == 0
        if checks["passed"]:
            checks["blocker"] = None
        elif not structural_ok:
            checks["blocker"] = "PREFLIGHT_FAILED"
        elif not service_ok:
            checks["blocker"] = "OLLAMA_REQUIRED"
        else:
            checks["blocker"] = "PREFLIGHT_FAILED"
    return {
        "run_id": plan["run_id"],
        "family": family,
        "checks": checks,
        "canonical_prompt_hashes": hashes,
        "plan": plan,
        "service_meta": service_meta,
    }


def _classify_failure(completion: str, evaluator: str, exception_type: str | None) -> str:
    if exception_type:
        return "transport_or_infrastructure_failure"
    if completion != "NATURAL_COMPLETE":
        return "model_generated_failure"
    if evaluator != "PASSED":
        return "model_generated_failure"
    return "none"


def _default_transport(family: str) -> Callable[[str], dict[str, Any]]:
    if family == "gemini":
        return call_gemini_once

    def _qwen(prompt: str) -> dict[str, Any]:
        return call_ollama_once(prompt, seed=SEED, model=QWEN_MODEL_ID)

    return _qwen


def run(
    output_dir: Path,
    *,
    family: str,
    transport: Callable[[str], dict[str, Any]] | None = None,
    require_service: bool = True,
) -> list[dict[str, Any]]:
    output_dir = Path(output_dir)
    pf = preflight(output_dir, family=family, require_service=require_service)
    if not pf["checks"]["passed"]:
        raise RuntimeError(pf["checks"]["blocker"] or "PREFLIGHT_FAILED")
    transport = transport or _default_transport(family)
    output_dir.mkdir(parents=True)
    _write_json(output_dir / "manifest.json", pf["plan"])
    _write_json(
        output_dir / "preflight.json",
        {**pf["checks"], "canonical_prompt_hashes": pf["canonical_prompt_hashes"], "service_meta": pf.get("service_meta")},
    )
    task = load_task()
    rows: list[dict[str, Any]] = []
    model_calls = 0
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
        parse_status = "not_run"
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
            if cell["condition"] == "ab2d":
                adoption = scan_toolbox(code or "", cell["task_id"], cell["frozen_parameters"])[
                    "classification"
                ]
        except BaseException as exc:
            exception_type, exception_message = type(exc).__name__, str(exc)
            trace = traceback.format_exc()
            parse_status = "infrastructure_failure"
        wall = time.monotonic() - started
        (cell_dir / "raw_response.txt").write_text(raw, encoding="utf-8")
        if code is not None:
            (cell_dir / "extracted_candidate.py").write_text(code, encoding="utf-8")
        artifact = {k: v for k, v in cell.items() if k != "prompt"}
        artifact.update(
            {
                "run_id": pf["plan"]["run_id"],
                "model_family": family,
                "completion_status": completion,
                "parse_status": parse_status,
                "adoption_status": adoption,
                "evaluator_status": evaluator,
                "failure_class": _classify_failure(completion, evaluator, exception_type),
                "exception_type": exception_type,
                "exception_message": exception_message,
                "traceback": trace,
                "evaluator_details": details,
                "token_metadata": metadata,
                "duration_metadata": {
                    "wall_clock_seconds": wall,
                    "provider_duration": metadata.get("latency_ms")
                    if family == "gemini"
                    else metadata.get("total_duration"),
                    "latency_ms": metadata.get("latency_ms"),
                },
                "infrastructure_valid": exception_type is None and bool(raw),
                "hashes": {
                    "prompt": _hash(prompt),
                    "raw": _hash(raw),
                    "extracted_candidate": _hash(code or ""),
                },
                "provenance": {
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
    by_condition = {}
    for condition in CONDITIONS:
        subset = [r for r in rows if r["condition"] == condition]
        by_condition[condition] = {
            "cells": 1,
            "evaluable": sum(
                r["evaluator_status"] not in {"NOT_RUN", "EXTRACTION_FAILURE"} for r in subset
            ),
            "execution_pass": sum(r["evaluator_status"] == "PASSED" for r in subset),
            "exact_pass": sum(r["evaluator_status"] == "PASSED" for r in subset),
            "failure_count": sum(r["failure_class"] != "none" for r in subset),
            "infrastructure_failures": sum(
                r["failure_class"] == "transport_or_infrastructure_failure" for r in subset
            ),
            "wall_clock_seconds": sum(r["duration_metadata"]["wall_clock_seconds"] for r in subset),
        }
    summary = {
        "task_id": TASK_ID,
        "model_family": family,
        "model": plan_model(family),
        "conditions": by_condition,
        "failure_classes": dict(Counter(r["failure_class"] for r in rows)),
        "canonical_prompt_hashes": pf["canonical_prompt_hashes"],
        "real_model_calls": model_calls,
        "infrastructure_failures": sum(
            r["failure_class"] == "transport_or_infrastructure_failure" for r in rows
        ),
        "healer_used": False,
        "cells": len(rows),
    }
    _write_json(output_dir / "cell_results.json", rows)
    _write_json(output_dir / "summary.json", summary)
    return rows


def plan_model(family: str) -> str:
    return GEMINI_MODEL_ID if family == "gemini" else QWEN_MODEL_ID


def main() -> int:
    parser = argparse.ArgumentParser(description="CE115 Q9 clean-incremental 3-cell pilot")
    parser.add_argument("--family", choices=("gemini", "qwen"), required=True)
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    pf = preflight(args.output_dir, family=args.family)
    if args.preflight_only:
        print(json.dumps(pf, ensure_ascii=False, indent=2, default=str))
        return 0 if pf["checks"]["passed"] else 2
    rows = run(args.output_dir, family=args.family)
    print(
        json.dumps(
            {
                "output_dir": str(args.output_dir),
                "family": args.family,
                "cells": len(rows),
                "real_model_calls": sum(r["provenance"]["model_calls"] for r in rows),
                "canonical_prompt_hashes": {
                    r["condition"]: r["canonical_prompt_hash"] for r in rows
                },
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
