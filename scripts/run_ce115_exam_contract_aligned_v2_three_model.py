"""Contract-aligned v2 three-model run: Gemini 3.5 Flash + Qwen3.5 4B + Qwen3.5 9B.

8 cells/model × 3 = 24. First attempt only; retry=0; healer=0.
Refuses to start unless zero-model preflight PASS. Does not overwrite v1 dirs.
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

from agent_tools.finals_rebuild.ce115_contract_aligned_ablation_v2 import (
    LINEAGE_ID,
    scan_v2_domain_adoption,
)
from agent_tools.finals_rebuild.ce115_exam_external_validation import EXPECTED_ANSWERS, TASK_IDS
from agent_tools.finals_rebuild.extraction import extract_code
from agent_tools.finals_rebuild.math_boundary_pilot import classify_response
from scripts.ce115_qwen_ollama_transport import call_ollama_once, probe_ollama
from scripts.ce115_v4_gemini_transport import MODEL_ID as GEMINI_MODEL_ID, call_gemini_once
from scripts.preflight_ce115_exam_contract_aligned_v2 import (
    CELL_SPECS,
    SEED,
    load_tasks,
    preflight as zero_model_preflight,
    write_preflight_artifacts,
)
from scripts.run_ce115_exam_external_validation_gemini_pilot import (
    _classify_failure,
    preliminary_failure_layer,
)

ANALYSIS = ROOT / "docs/experiments/analysis/ce115_exam_ext_contract_aligned_v2"


def _hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )


def _code_metrics(code: str | None) -> dict[str, Any]:
    if not code:
        return {"code_chars": 0, "loc": 0, "ast_nodes": 0}
    import ast

    loc = len([ln for ln in code.splitlines() if ln.strip()])
    try:
        nodes = sum(1 for _ in ast.walk(ast.parse(code)))
    except SyntaxError:
        nodes = 0
    return {"code_chars": len(code), "loc": loc, "ast_nodes": nodes}


def run_model_cohort(
    *,
    output_dir: Path,
    model_family: str,
    model_id: str,
    prefix: str,
    transport: Callable[[str], dict[str, Any]],
    plan_cells: list[dict[str, Any]],
    tasks: dict[str, dict[str, Any]],
    service_meta: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True)
    rows: list[dict[str, Any]] = []
    model_calls = 0
    for idx, cell in enumerate(plan_cells, start=1):
        task_id = cell["task_id"]
        condition = cell["condition"]
        task = tasks[task_id]
        cell_id = f"{prefix}__{task_id}__{condition}__seed_{SEED}"
        print(f"[{model_id}] {idx}/{len(plan_cells)} {cell_id}", flush=True)
        cell_dir = output_dir / "cells" / cell_id
        cell_dir.mkdir(parents=True)
        prompt = cell["prompt"]
        (cell_dir / "prompt.txt").write_text(prompt, encoding="utf-8")
        started = time.monotonic()
        raw = ""
        code = None
        exception_type = exception_message = trace = None
        metadata: dict[str, Any] = {}
        completion = "INFRASTRUCTURE_FAILURE"
        adoption: Any = "NOT_APPLICABLE"
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
            if condition == "ab2d" and code:
                adoption = scan_v2_domain_adoption(code, task_id)
        except BaseException as exc:  # noqa: BLE001 — record infra failures
            exception_type, exception_message = type(exc).__name__, str(exc)
            trace = traceback.format_exc()
            parse_status = "infrastructure_failure"
            evaluator = "INFRASTRUCTURE_FAILURE"
        wall = time.monotonic() - started
        (cell_dir / "raw_response.txt").write_text(raw, encoding="utf-8")
        if code is not None:
            (cell_dir / "extracted_candidate.py").write_text(code, encoding="utf-8")
        metrics = _code_metrics(code)
        artifact = {
            "cell_id": cell_id,
            "run_id": output_dir.name,
            "model_family": model_family,
            "model": model_id,
            "task_id": task_id,
            "condition": condition,
            "condition_label": f"{condition}-v2",
            "seed": SEED,
            "prompt_lineage": LINEAGE_ID,
            "canonical_prompt_hash": cell["canonical_prompt_hash"],
            "frozen_parameters": cell["frozen_parameters"],
            "expected_answer": EXPECTED_ANSWERS[task_id],
            "completion_status": completion,
            "parse_status": parse_status,
            "domain_api_adoption": adoption,
            "evaluator_status": evaluator,
            "predicted_answer": predicted,
            "failure_class": _classify_failure(completion, evaluator, exception_type),
            "failure_layer": preliminary_failure_layer(evaluator),
            "exception_type": exception_type,
            "exception_message": exception_message,
            "traceback": trace,
            "evaluator_details": details,
            "token_metadata": metadata,
            "code_metrics": metrics,
            "duration_metadata": {
                "wall_clock_seconds": wall,
                "latency_ms": metadata.get("latency_ms"),
            },
            "infrastructure_valid": exception_type is None and bool(raw),
            "first_attempt_only": True,
            "retry": 0,
            "healer": 0,
            "hashes": {
                "prompt": _hash(prompt),
                "raw": _hash(raw),
                "extracted_candidate": _hash(code or ""),
            },
            "service_meta": service_meta,
        }
        artifact["artifact_sha256"] = _hash(
            json.dumps({k: v for k, v in artifact.items() if k != "artifact_sha256"}, sort_keys=True, default=str)
        )
        _write_json(cell_dir / "artifact.json", artifact)
        rows.append(artifact)

    summary = {
        "run_id": output_dir.name,
        "model": model_id,
        "model_family": model_family,
        "lineage_id": LINEAGE_ID,
        "planned_cells": len(plan_cells),
        "completed_cells": len(rows),
        "exact_pass": sum(r["evaluator_status"] == "PASSED" for r in rows),
        "by_status": dict(Counter(r["evaluator_status"] for r in rows)),
        "real_model_calls": model_calls,
        "retries": 0,
        "healer_calls": 0,
        "infrastructure_failures": sum(
            r["failure_class"] == "transport_or_infrastructure_failure" for r in rows
        ),
    }
    _write_json(output_dir / "cell_results.json", rows)
    _write_json(output_dir / "summary.json", summary)
    _write_json(
        output_dir / "manifest.json",
        {
            "run_id": output_dir.name,
            "model": model_id,
            "lineage_id": LINEAGE_ID,
            "seed": SEED,
            "cell_specs": [{"task_id": t, "condition": c} for t, c in CELL_SPECS],
            "canonical_prompt_hashes": {
                r["task_id"] + "::" + r["condition"]: r["canonical_prompt_hash"] for r in rows
            },
        },
    )
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--preflight-dir",
        default=str(ROOT / "docs/experiments/results/ce115_exam_ext_contract_aligned_v2_formal16_preflight_01"),
    )
    parser.add_argument(
        "--output-root",
        default=str(ROOT / "docs/experiments/results"),
    )
    parser.add_argument("--dry-run-preflight-only", action="store_true")
    parser.add_argument(
        "--skip-qwen9b",
        action="store_true",
        default=True,
        help="Do not execute qwen3.5:9b (default True for formal 16-cell).",
    )
    parser.add_argument("--include-qwen9b", action="store_true", help="Override: also run 9B.")
    args = parser.parse_args()
    skip_9b = not args.include_qwen9b

    preflight_dir = Path(args.preflight_dir)
    output_root = Path(args.output_root)
    hr02 = ANALYSIS / "human_review_prompts_02" / "canonical_prompt_hashes.json"

    # Refuse overwrite of v1
    for v1 in (
        output_root / "ce115_exam_ext_113_114_gemini_pilot_01",
        output_root / "ce115_exam_ext_113_114_qwen_pilot_01",
        output_root / "ce115_exam_ext_113_114_preflight_01",
    ):
        if not v1.exists():
            print(f"WARN: v1 dir missing (expected preserved): {v1}")

    if preflight_dir.exists():
        print(f"REFUSE: preflight dir already exists: {preflight_dir}", file=sys.stderr)
        return 2

    # Refresh key from User env if process env empty
    if not os.getenv("GEMINI_API_KEY"):
        user_key = os.environ.get("GEMINI_API_KEY") or __import__("os").environ.get("GEMINI_API_KEY")
        try:
            import ctypes  # noqa: F401
            user_key = __import__("os").popen(
                'powershell -NoProfile -Command "[Environment]::GetEnvironmentVariable(\'GEMINI_API_KEY\',\'User\')"'
            ).read().strip()
            if user_key:
                os.environ["GEMINI_API_KEY"] = user_key
        except Exception:  # noqa: BLE001
            pass

    pf = zero_model_preflight(preflight_dir, require_models=True)
    write_preflight_artifacts(preflight_dir, pf)
    if not pf["checks"]["passed"]:
        print("PREFLIGHT_FAILED — refusing model runs", file=sys.stderr)
        print(json.dumps(pf["checks"], indent=2, default=str))
        return 1

    # Gate: builder hashes must match human_review_prompts_02
    if not hr02.is_file():
        print(f"REFUSE: missing {hr02}", file=sys.stderr)
        return 2
    freeze = json.loads(hr02.read_text(encoding="utf-8"))["hashes"]
    plan_hashes = pf["plan"]["canonical_prompt_hashes"]
    for tid, conds in freeze.items():
        for cond, expected in conds.items():
            got = plan_hashes.get(tid, {}).get(cond)
            if got != expected:
                print(
                    f"HASH_MISMATCH vs human_review_prompts_02: {tid}/{cond} "
                    f"plan={got} freeze={expected}",
                    file=sys.stderr,
                )
                return 1

    if args.dry_run_preflight_only:
        print("preflight PASS; dry-run stop")
        return 0

    tasks = load_tasks()
    plan_cells = pf["plan"]["cells"]

    cohorts = [
        {
            "name": "gemini",
            "dir": output_root / "ce115_exam_ext_contract_aligned_v2_gemini_01",
            "family": "gemini",
            "model": GEMINI_MODEL_ID,
            "prefix": "gemini_3_5_flash",
            "transport": lambda p: call_gemini_once(p),
            "meta": {"api_key_present": bool(os.getenv("GEMINI_API_KEY"))},
        },
        {
            "name": "qwen4b",
            "dir": output_root / "ce115_exam_ext_contract_aligned_v2_qwen4b_01",
            "family": "qwen",
            "model": "qwen3.5:4b",
            "prefix": "qwen3_5_4b",
            "transport": lambda p: call_ollama_once(p, seed=SEED, model="qwen3.5:4b"),
            "meta": probe_ollama(model="qwen3.5:4b"),
        },
    ]
    if not skip_9b:
        cohorts.append(
            {
                "name": "qwen9b",
                "dir": output_root / "ce115_exam_ext_contract_aligned_v2_qwen9b_01",
                "family": "qwen",
                "model": "qwen3.5:9b",
                "prefix": "qwen3_5_9b",
                "transport": lambda p: call_ollama_once(p, seed=SEED, model="qwen3.5:9b"),
                "meta": probe_ollama(model="qwen3.5:9b"),
            }
        )

    all_rows: list[dict[str, Any]] = []
    for cohort in cohorts:
        if cohort["dir"].exists():
            print(f"REFUSE: output exists {cohort['dir']}", file=sys.stderr)
            return 2
        print(f"=== running {cohort['model']} ({len(plan_cells)} cells) ===", flush=True)
        rows = run_model_cohort(
            output_dir=cohort["dir"],
            model_family=cohort["family"],
            model_id=cohort["model"],
            prefix=cohort["prefix"],
            transport=cohort["transport"],
            plan_cells=plan_cells,
            tasks=tasks,
            service_meta=cohort["meta"],
        )
        all_rows.extend(rows)
        print(
            json.dumps(
                {
                    "model": cohort["model"],
                    "done": len(rows),
                    "pass": sum(r["evaluator_status"] == "PASSED" for r in rows),
                }
            ),
            flush=True,
        )

    combined = {
        "lineage_id": LINEAGE_ID,
        "seed": SEED,
        "cohort": "formal_16cell_gemini_qwen4b",
        "total_cells": len(all_rows),
        "exact_pass": sum(r["evaluator_status"] == "PASSED" for r in all_rows),
        "by_model": {
            m: {
                "cells": sum(1 for r in all_rows if r["model"] == m),
                "pass": sum(1 for r in all_rows if r["model"] == m and r["evaluator_status"] == "PASSED"),
                "real_model_calls": sum(1 for r in all_rows if r["model"] == m and r["infrastructure_valid"]),
            }
            for m in {r["model"] for r in all_rows}
        },
        "real_model_calls": sum(1 for r in all_rows if r["infrastructure_valid"]),
        "retries": 0,
        "healer_calls": 0,
        "qwen3.5:9b": {
            "status": "not_executed_on_this_machine",
            "excluded_from_denominator": True,
        },
        "starting_head": None,
        "matrix": [
            {
                "model": r["model"],
                "task_id": r["task_id"],
                "condition": r["condition"],
                "evaluator_status": r["evaluator_status"],
                "failure_layer": r["failure_layer"],
                "adoption": r["domain_api_adoption"]
                if isinstance(r["domain_api_adoption"], dict)
                else r["domain_api_adoption"],
                "infrastructure_valid": r["infrastructure_valid"],
            }
            for r in all_rows
        ],
    }
    try:
        import subprocess

        combined["starting_head"] = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip()
    except Exception:  # noqa: BLE001
        combined["starting_head"] = "unknown"

    out_name = "formal_16cell_gemini_qwen4b_combined.json"
    _write_json(ANALYSIS / out_name, combined)
    print(
        json.dumps(
            {
                k: combined[k]
                for k in (
                    "total_cells",
                    "exact_pass",
                    "by_model",
                    "real_model_calls",
                    "retries",
                    "healer_calls",
                    "qwen3.5:9b",
                    "starting_head",
                )
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
