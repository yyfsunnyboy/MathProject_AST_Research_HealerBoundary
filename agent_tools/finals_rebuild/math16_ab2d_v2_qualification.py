# -*- coding: utf-8 -*-
"""Math16 Ab2d V2 qualification — model completions for runtime contract fix.

Runs live qualification against frozen V2 prompts using Math16 formal model
settings and the same evaluator path as formal 480-cell execution.

Historical note: the original 2026-08 run executed Qwen 4B live only (6 cells:
3 domains × 2 conditions) with 2 pending cells for 9B/Gemini capacity/API.

This module supports:
  --model qwen_4b   historical matrix (default if requested)
  --model gemini    8 cells: 4 domains × {domain-menu, full-plan}
  --model qwen_9b   8 cells: same matrix
  --model both_pending   run gemini + qwen_9b
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.math16_ab2d_formal_execution import (  # noqa: E402
    MATH16_MODEL_SETTINGS_REL,
    build_math16_gemini_request_metadata,
    call_model_with_math16_retries,
    load_math16_model_settings,
    math16_gemini_generation_config,
    sha256_text,
)
from agent_tools.finals_rebuild.math16_ab2d_full_artifact_assembly import (  # noqa: E402
    QFIX_001_ID,
    atomic_write_json,
    atomic_write_text,
    build_evaluation_result,
    write_artifact_manifest,
    write_evaluation_artifacts,
)
from agent_tools.finals_rebuild.math16_pool import build_pool_tasks  # noqa: E402
from scripts.run_math16_latex_v1_gemini_live import classify_math16_response  # noqa: E402

MENU_DIR = ROOT / "docs/experiments/prompts/ab2d_domain_menu_v2/prompts"
FULL_DIR = ROOT / "docs/experiments/prompts/ab2d_full_v2/prompts"
ARTIFACT_ROOT = ROOT / "artifacts/math16_ab2d_menu_vs_full_runtime_contract_v2/qualification"
EXPERIMENT_ID = "math16_ab2d_menu_vs_full_runtime_contract_v2"

SEED = 2026071301

# 4 domains × 2 conditions (matches user gate for Gemini / Qwen 9B completion).
DOMAIN_TASKS = [
    {"domain": "Radical", "task_id": "ce112_q04_radical_simplification"},
    {"domain": "Fraction", "task_id": "ce113_q01_negative_fraction_subtraction"},
    {"domain": "Polynomial", "task_id": "ce115_calc_polynomial_division_l1"},
    {"domain": "Integer", "task_id": "ce112_q09_divisor_multiple_intersection"},
]
CONDITIONS = ("ab2d_domain_menu_v2", "ab2d_full_v2")

# Historical Qwen 4B matrix (6 live cells only; kept for documentable replay).
QWEN4B_HISTORICAL = [
    {"model_key": "qwen_4b", "condition": "ab2d_domain_menu_v2", "task_id": "ce112_q04_radical_simplification"},
    {"model_key": "qwen_4b", "condition": "ab2d_full_v2", "task_id": "ce112_q04_radical_simplification"},
    {"model_key": "qwen_4b", "condition": "ab2d_domain_menu_v2", "task_id": "ce113_q01_negative_fraction_subtraction"},
    {"model_key": "qwen_4b", "condition": "ab2d_full_v2", "task_id": "ce113_q01_negative_fraction_subtraction"},
    {"model_key": "qwen_4b", "condition": "ab2d_domain_menu_v2", "task_id": "ce115_calc_polynomial_division_l1"},
    {"model_key": "qwen_4b", "condition": "ab2d_full_v2", "task_id": "ce115_calc_polynomial_division_l1"},
]

KWARGS_ANTI_PATTERN_RE = re.compile(r'kwargs\.get\(\s*["\']frozen_params["\']\s*\)')
KWARGS_FROZEN_RE = re.compile(r"kwargs\s*\[\s*[\"']frozen_params[\"']\s*\]")
OPTIONAL_KWARGS_FROZEN_RE = re.compile(
    r"kwargs\.get\(\s*[\"']frozen_params[\"']\s*,|\.get\(\s*[\"']frozen_params[\"']"
)

MODEL_OUT_DIR = {
    "gemini": "gemini",
    "qwen_9b": "qwen9b",
    "qwen_4b": "qwen4b",
}


def _prompt_path(condition: str, task_id: str) -> Path:
    base = MENU_DIR if condition == "ab2d_domain_menu_v2" else FULL_DIR
    return base / f"{task_id}.txt"


def _cell_id(model_key: str, condition: str, task_id: str) -> str:
    return f"{model_key}__{task_id}__{condition}__seed_{SEED}"


def _matrix_for_model(model_key: str) -> list[dict[str, Any]]:
    if model_key == "qwen_4b":
        return list(QWEN4B_HISTORICAL)
    rows: list[dict[str, Any]] = []
    for task in DOMAIN_TASKS:
        for condition in CONDITIONS:
            rows.append(
                {
                    "model_key": model_key,
                    "condition": condition,
                    "task_id": task["task_id"],
                    "domain": task["domain"],
                }
            )
    return rows


def _kwargs_misuse_flags(source: str | None) -> dict[str, Any]:
    if not source:
        return {
            "kwargs_get_frozen_params_in_generated_source": False,
            "kwargs_bracket_frozen_params_in_generated_source": False,
            "any_kwargs_frozen_params_misuse": False,
            "kwargs_misuse_count": 0,
        }
    get_hits = KWARGS_ANTI_PATTERN_RE.findall(source)
    bracket_hits = KWARGS_FROZEN_RE.findall(source)
    # Also catch kwargs.get("frozen_params", default) which anti-pattern RE already covers;
    # optional broader count:
    optional_hits = OPTIONAL_KWARGS_FROZEN_RE.findall(source)
    n = len(get_hits) + len(bracket_hits)
    return {
        "kwargs_get_frozen_params_in_generated_source": bool(get_hits),
        "kwargs_bracket_frozen_params_in_generated_source": bool(bracket_hits),
        "optional_get_hits": len(optional_hits),
        "any_kwargs_frozen_params_misuse": n > 0,
        "kwargs_misuse_count": n,
    }


def _failure_bucket(outcome: str) -> str:
    if outcome == "passed":
        return "passed"
    if outcome == "schema_failure":
        return "schema_failure"
    if outcome in {
        "empty_response",
        "catastrophic_truncation",
        "extraction_failure",
        "parse_minor",
        "missing_entry_point",
    }:
        return "unparseable"
    if outcome in {"runtime_failure", "infrastructure_failure"}:
        return "execution_failure"
    if outcome in {
        "answer_incorrect",
        "structural_mismatch",
        "latex_mismatch",
        "structural_or_latex_mismatch",
    }:
        return "answer_incorrect"
    if outcome == "transport_failure":
        return "transport_failure"
    return "other"


def run_one_live(
    *,
    model_key: str,
    condition: str,
    task_id: str,
    domain: str | None,
    task: dict[str, Any],
    settings: dict[str, Any],
    model_root: Path,
) -> dict[str, Any]:
    cell_id = _cell_id(model_key, condition, task_id)
    cell_dir = model_root / "cells" / cell_id
    cell_dir.mkdir(parents=True, exist_ok=True)

    prompt_path = _prompt_path(condition, task_id)
    prompt_text = prompt_path.read_text(encoding="utf-8").replace("\r\n", "\n")
    prompt_sha = sha256_text(prompt_text)
    atomic_write_text(cell_dir / "prompt.txt", prompt_text)

    ms = settings["models"][model_key]
    if model_key == "gemini":
        req_meta = build_math16_gemini_request_metadata(prompt_text, ms)
        req_meta.update(
            {
                "model_key": model_key,
                "condition": condition,
                "seed": SEED,
                "qualification_only": True,
                "primary_evidence": False,
                "experiment_id": EXPERIMENT_ID,
            }
        )
    else:
        req_meta = {
            "provider": "ollama",
            "model": ms["model_identifier"],
            "model_key": model_key,
            "condition": condition,
            "seed": SEED,
            "temperature": ms["temperature"],
            "top_p": ms["top_p"],
            "top_k": ms["top_k"],
            "num_predict": ms.get("num_predict", ms.get("max_output_tokens")),
            "timeout_seconds": ms["timeout_seconds"],
            "num_ctx_context_limit": ms.get("num_ctx_context_limit"),
            "qualification_only": True,
            "primary_evidence": False,
            "experiment_id": EXPERIMENT_ID,
            "parameter_authority": MATH16_MODEL_SETTINGS_REL,
        }
    atomic_write_json(cell_dir / "request_metadata.json", req_meta)

    print(f"Calling {model_key} (V2 qual, no replan): {cell_id}", flush=True)
    started = datetime.now(timezone.utc).isoformat()
    t0 = time.monotonic()
    call = call_model_with_math16_retries(
        model_key=model_key, prompt=prompt_text, seed=SEED, settings=settings
    )
    duration = time.monotonic() - t0
    raw = call.get("raw_text") or ""
    atomic_write_text(cell_dir / "raw_response.txt", raw)
    atomic_write_json(
        cell_dir / "logs.json",
        {
            "started_at_utc": started,
            "duration_seconds": duration,
            "api_attempts": call.get("api_attempts"),
            "transport_error": call.get("transport_error"),
            "provider_metadata": call.get("metadata"),
            "model_calls": 0 if call.get("transport_error") and not raw else 1,
        },
    )

    pipeline = {
        "model_call_attempted": True,
        "raw_response_preserved": True,
        "extraction_attempted": False,
        "execution_evaluation_completed_or_recorded": False,
        "transport_error": call.get("transport_error"),
    }

    if call.get("transport_error") and not raw:
        outcome = "transport_failure"
        source = None
        details: dict[str, Any] = {
            "error": call["transport_error"],
            "api_attempts": call.get("api_attempts"),
        }
        evaluation = build_evaluation_result(
            outcome=outcome,
            source=None,
            details=details,
            frozen_params=task["frozen_params"],
        )
        pipeline["execution_evaluation_completed_or_recorded"] = True
    else:
        pipeline["extraction_attempted"] = True
        outcome, source, details = classify_math16_response(
            raw,
            frozen_params=task["frozen_params"],
            audit_oracle_payload=task["oracle_payload"],
            task=task,
            execution_timeout=10.0,
        )
        if source:
            atomic_write_text(cell_dir / "extracted_source.py", source)
        elif not (cell_dir / "extracted_source.py").exists():
            atomic_write_text(cell_dir / "extracted_source.py", "")
        evaluation = build_evaluation_result(
            outcome=outcome,
            source=source,
            details=details,
            frozen_params=task["frozen_params"],
        )
        pipeline["execution_evaluation_completed_or_recorded"] = True

    write_evaluation_artifacts(cell_dir, evaluation=evaluation, outcome=outcome)

    kwargs_flags = _kwargs_misuse_flags(source)
    required = [
        "prompt.txt",
        "raw_response.txt",
        "request_metadata.json",
        "extracted_source.py",
        "evaluation_result.json",
        "execution_result.json",
        "logs.json",
    ]
    missing = [n for n in required if not (cell_dir / n).exists()]
    pipeline_complete = (
        not missing
        and pipeline["model_call_attempted"]
        and pipeline["raw_response_preserved"]
        and pipeline["execution_evaluation_completed_or_recorded"]
    )

    artifact = {
        "experiment_id": EXPERIMENT_ID,
        "cell_id": cell_id,
        "qualification_only": True,
        "primary_evidence": False,
        "model": ms["model_identifier"],
        "model_key": model_key,
        "task_id": task_id,
        "domain": domain,
        "condition": condition,
        "seed": SEED,
        "prompt_sha256": prompt_sha,
        "outcome": outcome,
        "pipeline": pipeline,
        "pipeline_complete": pipeline_complete,
        "missing_files": missing,
        "duration_seconds": duration,
        "started_at_utc": started,
        "completed_at_utc": datetime.now(timezone.utc).isoformat(),
        "persisted_complete": True,
        "artifact_assembly": QFIX_001_ID,
        "parameter_authority": MATH16_MODEL_SETTINGS_REL,
        "kwargs_misuse": kwargs_flags,
        "failure_bucket": _failure_bucket(outcome),
        "healer": False,
    }
    write_artifact_manifest(cell_dir, artifact)

    return {
        "cell_id": cell_id,
        "model_key": model_key,
        "condition": condition,
        "task_id": task_id,
        "domain": domain,
        "seed": SEED,
        "live": True,
        "outcome": outcome,
        "failure_bucket": _failure_bucket(outcome),
        "pipeline_complete": pipeline_complete,
        "missing_files": missing,
        "prompt_sha256": prompt_sha,
        **kwargs_flags,
        "runtime_error": evaluation.get("runtime_error"),
        "three_key_output": evaluation.get("three_key_output"),
        "oracle_payload_equals_frozen_params": evaluation.get(
            "oracle_payload_equals_frozen_params"
        ),
        "duration_seconds": duration,
    }


def run_model_qualification(model_key: str) -> dict[str, Any]:
    if model_key not in MODEL_OUT_DIR:
        raise SystemExit(f"unknown model_key: {model_key}")

    settings = load_math16_model_settings()
    # Fail-closed pin check for declared authorities.
    g = settings["models"]["gemini"]
    assert float(g["temperature"]) == 0.0 and float(g["top_p"]) == 1.0 and int(g["top_k"]) == 1
    assert int(g["max_output_tokens"]) == 24576 and int(g["timeout_seconds"]) == 600
    for qk in ("qwen_9b", "qwen_4b"):
        q = settings["models"][qk]
        assert float(q["temperature"]) == 0.2 and float(q["top_p"]) == 0.8 and int(q["top_k"]) == 20
        num_predict = int(q.get("num_predict", q.get("max_output_tokens")))
        assert num_predict == 24576
        assert int(q["timeout_seconds"]) == 1800
        assert int(q["num_ctx_context_limit"]) == 65536

    tasks = {t["task_id"]: t for t in build_pool_tasks()}
    matrix = _matrix_for_model(model_key)
    model_root = ARTIFACT_ROOT / MODEL_OUT_DIR[model_key]
    model_root.mkdir(parents=True, exist_ok=True)
    (model_root / "cells").mkdir(parents=True, exist_ok=True)

    results: list[dict[str, Any]] = []
    for row in matrix:
        task = tasks[row["task_id"]]
        domain = row.get("domain")
        if domain is None:
            domain = next(
                (t["domain"] for t in DOMAIN_TASKS if t["task_id"] == row["task_id"]), None
            )
        results.append(
            run_one_live(
                model_key=model_key,
                condition=row["condition"],
                task_id=row["task_id"],
                domain=domain,
                task=task,
                settings=settings,
                model_root=model_root,
            )
        )

    n_pass = sum(1 for r in results if r["outcome"] == "passed")
    n_kwargs = sum(1 for r in results if r["any_kwargs_frozen_params_misuse"])
    n_pipeline = sum(1 for r in results if r["pipeline_complete"])
    bucket_counts: dict[str, int] = {}
    for r in results:
        bucket_counts[r["failure_bucket"]] = bucket_counts.get(r["failure_bucket"], 0) + 1

    ms = settings["models"][model_key]
    gen_cfg = None
    if model_key == "gemini":
        gen_cfg = math16_gemini_generation_config(ms)

    summary = {
        "experiment_id": EXPERIMENT_ID,
        "model_key": model_key,
        "namespace": MODEL_OUT_DIR[model_key],
        "qualification_only": True,
        "primary_evidence": False,
        "seed": SEED,
        "parameter_authority": MATH16_MODEL_SETTINGS_REL,
        "model_settings_snapshot": {
            "model_identifier": ms["model_identifier"],
            "temperature": ms["temperature"],
            "top_p": ms["top_p"],
            "top_k": ms["top_k"],
            "max_output_tokens": ms.get("max_output_tokens"),
            "num_predict": ms.get("num_predict", ms.get("max_output_tokens")),
            "timeout_seconds": ms["timeout_seconds"],
            "num_ctx_context_limit": ms.get("num_ctx_context_limit"),
            "generation_config": gen_cfg,
        },
        "planned": len(matrix),
        "executed_live": len(results),
        "pipeline_complete_count": n_pipeline,
        "all_pipeline_complete": n_pipeline == len(results),
        "live_pass": n_pass,
        "live_fail": len(results) - n_pass,
        "kwargs_get_frozen_params_reappeared": n_kwargs,
        "kwargs_misuse_cells": [
            r["cell_id"] for r in results if r["any_kwargs_frozen_params_misuse"]
        ],
        "failure_bucket_counts": bucket_counts,
        "passed_gate": n_pipeline == len(results) and n_kwargs == 0,
        "note": (
            "Gate = all pipeline_complete AND kwargs frozen_params misuse count == 0. "
            "Answer correctness is not required for qualification gate."
        ),
        "results": results,
    }
    atomic_write_json(model_root / "qualification_summary.json", summary)
    # Mirror root pointer for this model completion.
    atomic_write_json(ARTIFACT_ROOT / f"qualification_summary_{MODEL_OUT_DIR[model_key]}.json", summary)
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Math16 Ab2d V2 qualification")
    parser.add_argument(
        "--model",
        required=True,
        choices=["gemini", "qwen_9b", "qwen_4b", "both_pending"],
        help="Which model qualification matrix to execute",
    )
    args = parser.parse_args(argv)

    models = ["gemini", "qwen_9b"] if args.model == "both_pending" else [args.model]
    summaries = []
    for model_key in models:
        summary = run_model_qualification(model_key)
        summaries.append(summary)
        print(
            json.dumps(
                {
                    "model_key": summary["model_key"],
                    "planned": summary["planned"],
                    "executed_live": summary["executed_live"],
                    "all_pipeline_complete": summary["all_pipeline_complete"],
                    "live_pass": summary["live_pass"],
                    "live_fail": summary["live_fail"],
                    "kwargs_get_frozen_params_reappeared": summary[
                        "kwargs_get_frozen_params_reappeared"
                    ],
                    "failure_bucket_counts": summary["failure_bucket_counts"],
                    "passed_gate": summary["passed_gate"],
                },
                ensure_ascii=False,
                indent=2,
            )
        )

    overall = {
        "experiment_id": EXPERIMENT_ID,
        "models_run": models,
        "all_passed_gate": all(s["passed_gate"] for s in summaries),
        "summaries": [
            {
                "model_key": s["model_key"],
                "passed_gate": s["passed_gate"],
                "live_pass": s["live_pass"],
                "live_fail": s["live_fail"],
                "kwargs_reappeared": s["kwargs_get_frozen_params_reappeared"],
            }
            for s in summaries
        ],
    }
    atomic_write_json(ARTIFACT_ROOT / "qualification_completion_summary.json", overall)
    return 0 if overall["all_passed_gate"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
