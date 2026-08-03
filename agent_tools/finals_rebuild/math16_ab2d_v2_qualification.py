# -*- coding: utf-8 -*-
"""Math16 Ab2d V2 qualification: 8-cell matrix, 6 live (Qwen4B), 2 pending.

Per user instruction: only Qwen4B can run live in this environment (Ollama reachable,
qwen3.5:4b installed). Qwen9B cannot run on this machine and Gemini has no API key
available -- those 2 cells are prepared/frozen but NOT called, and tagged
PENDING_9B_CAPACITY / PENDING_API_KEY respectively. This script must never search for,
set, or read a value for GEMINI_API_KEY, and must never attempt to download/run qwen3.5:9b.

Reuses the real evaluator (`classify_math16_response`, same one the formal 480-cell run
uses) and the real Ollama call path (`call_model_with_math16_retries`) from
agent_tools/finals_rebuild/math16_ab2d_formal_execution.py -- this qualification exercises
the actual runtime, not a simulation.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.math16_ab2d_formal_execution import (  # noqa: E402
    call_model_with_math16_retries,
    sha256_text,
)
from agent_tools.finals_rebuild.math16_pool import build_pool_tasks  # noqa: E402
from scripts.run_math16_latex_v1_gemini_live import classify_math16_response  # noqa: E402

MENU_DIR = ROOT / "docs/experiments/prompts/ab2d_domain_menu_v2/prompts"
FULL_DIR = ROOT / "docs/experiments/prompts/ab2d_full_v2/prompts"
ARTIFACT_ROOT = ROOT / "artifacts/math16_ab2d_menu_vs_full_runtime_contract_v2/qualification"
MODEL_SETTINGS_PATH = ROOT / "artifacts/math16_ab2d_full_domain_assisted_v1/preregistration/model_settings.json"

SEED = 2026071301

QUAL_MATRIX = [
    {"model_key": "qwen_4b", "condition": "ab2d_domain_menu_v2", "task_id": "ce112_q04_radical_simplification", "live": True},
    {"model_key": "qwen_4b", "condition": "ab2d_full_v2", "task_id": "ce112_q04_radical_simplification", "live": True},
    {"model_key": "qwen_4b", "condition": "ab2d_domain_menu_v2", "task_id": "ce113_q01_negative_fraction_subtraction", "live": True},
    {"model_key": "qwen_4b", "condition": "ab2d_full_v2", "task_id": "ce113_q01_negative_fraction_subtraction", "live": True},
    {"model_key": "qwen_4b", "condition": "ab2d_domain_menu_v2", "task_id": "ce115_calc_polynomial_division_l1", "live": True},
    {"model_key": "qwen_4b", "condition": "ab2d_full_v2", "task_id": "ce115_calc_polynomial_division_l1", "live": True},
    {"model_key": "qwen_9b", "condition": "ab2d_full_v2", "task_id": "ce112_q04_radical_simplification", "live": False, "pending_reason": "PENDING_9B_CAPACITY"},
    {"model_key": "gemini", "condition": "ab2d_full_v2", "task_id": "ce115_calc_polynomial_division_l1", "live": False, "pending_reason": "PENDING_API_KEY"},
]

KWARGS_ANTI_PATTERN_RE = re.compile(r'kwargs\.get\(\s*["\']frozen_params["\']\s*\)')


def _prompt_path(condition: str, task_id: str) -> Path:
    base = MENU_DIR if condition == "ab2d_domain_menu_v2" else FULL_DIR
    return base / f"{task_id}.txt"


def _cell_id(row: dict) -> str:
    return f"{row['model_key']}__{row['task_id']}__{row['condition']}__seed_{SEED}"


def run_one_live(row: dict, task: dict, settings: dict) -> dict:
    cell_id = _cell_id(row)
    cell_dir = ARTIFACT_ROOT / "cells" / cell_id
    cell_dir.mkdir(parents=True, exist_ok=True)

    prompt_path = _prompt_path(row["condition"], row["task_id"])
    prompt_text = prompt_path.read_text(encoding="utf-8")
    (cell_dir / "prompt.txt").write_text(prompt_text, encoding="utf-8", newline="\n")

    call_result = call_model_with_math16_retries(
        model_key=row["model_key"], prompt=prompt_text, seed=SEED, settings=settings
    )
    (cell_dir / "request_metadata.json").write_text(
        json.dumps({"model_key": row["model_key"], "seed": SEED, "metadata": call_result.get("metadata")},
                    ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    raw = call_result.get("raw_text") or ""
    (cell_dir / "raw_response.txt").write_text(raw, encoding="utf-8", newline="\n")

    if call_result.get("transport_error"):
        outcome = "transport_failure"
        source = None
        details = {"transport_error": call_result["transport_error"], "api_attempts": call_result.get("api_attempts")}
    else:
        outcome, source, details = classify_math16_response(
            raw,
            frozen_params=task["frozen_params"],
            audit_oracle_payload=task["oracle_payload"],
            task=task,
            execution_timeout=10.0,
        )

    if source:
        (cell_dir / "extracted_source.py").write_text(source, encoding="utf-8", newline="\n")
    kwargs_anti_pattern_present = bool(source and KWARGS_ANTI_PATTERN_RE.search(source))

    result = {
        "cell_id": cell_id,
        "model_key": row["model_key"],
        "condition": row["condition"],
        "task_id": row["task_id"],
        "seed": SEED,
        "live": True,
        "outcome": outcome,
        "prompt_sha256": sha256_text(prompt_text),
        "kwargs_get_frozen_params_in_generated_source": kwargs_anti_pattern_present,
        "understood_zero_arg_generate": (
            source is not None and "def generate(" in source and "def generate():" not in source.replace(" ", "")
        ),
        "embedded_frozen_literals_in_source": bool(
            source and any(str(v) in source for v in _flatten_values(task["frozen_params"]))
        ),
        "details": details,
    }
    (cell_dir / "evaluation_result.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8", newline="\n"
    )
    return result


def _flatten_values(obj: Any) -> list[Any]:
    out: list[Any] = []
    if isinstance(obj, dict):
        for v in obj.values():
            out.extend(_flatten_values(v))
    elif isinstance(obj, list):
        for v in obj:
            out.extend(_flatten_values(v))
    else:
        if isinstance(obj, (int, str)) and str(obj) not in ("", "0", "1"):
            out.append(obj)
    return out


def prepare_pending(row: dict, task: dict) -> dict:
    cell_id = _cell_id(row)
    cell_dir = ARTIFACT_ROOT / "cells" / cell_id
    cell_dir.mkdir(parents=True, exist_ok=True)
    prompt_path = _prompt_path(row["condition"], row["task_id"])
    prompt_text = prompt_path.read_text(encoding="utf-8")
    (cell_dir / "prompt.txt").write_text(prompt_text, encoding="utf-8", newline="\n")
    result = {
        "cell_id": cell_id,
        "model_key": row["model_key"],
        "condition": row["condition"],
        "task_id": row["task_id"],
        "seed": SEED,
        "live": False,
        "outcome": row["pending_reason"],
        "prompt_sha256": sha256_text(prompt_text),
        "note": "Prompt frozen; model not called this round per explicit user instruction.",
    }
    (cell_dir / "evaluation_result.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    return result


def run_qualification() -> dict:
    ARTIFACT_ROOT.mkdir(parents=True, exist_ok=True)
    tasks = {t["task_id"]: t for t in build_pool_tasks()}
    settings = json.loads(MODEL_SETTINGS_PATH.read_text(encoding="utf-8"))["models"]

    live_results = []
    pending_results = []
    for row in QUAL_MATRIX:
        task = tasks[row["task_id"]]
        if row["live"]:
            live_results.append(run_one_live(row, task, {"models": settings}))
        else:
            pending_results.append(prepare_pending(row, task))

    n_live_pass = sum(1 for r in live_results if r["outcome"] == "passed")
    n_kwargs_anti_pattern = sum(1 for r in live_results if r["kwargs_get_frozen_params_in_generated_source"])

    summary = {
        "experiment_id": "math16_ab2d_menu_vs_full_runtime_contract_v2",
        "planned": len(QUAL_MATRIX),
        "executed_live": len(live_results),
        "pending_9B": sum(1 for r in QUAL_MATRIX if not r["live"] and r.get("pending_reason") == "PENDING_9B_CAPACITY"),
        "pending_gemini": sum(1 for r in QUAL_MATRIX if not r["live"] and r.get("pending_reason") == "PENDING_API_KEY"),
        "live_pass": n_live_pass,
        "live_fail": len(live_results) - n_live_pass,
        "kwargs_get_frozen_params_reappeared": n_kwargs_anti_pattern,
        "live_results": live_results,
        "pending_results": pending_results,
    }
    (ARTIFACT_ROOT / "qualification_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8", newline="\n"
    )
    return summary


if __name__ == "__main__":
    result = run_qualification()
    print(json.dumps({
        "planned": result["planned"], "executed_live": result["executed_live"],
        "pending_9B": result["pending_9B"], "pending_gemini": result["pending_gemini"],
        "live_pass": result["live_pass"], "live_fail": result["live_fail"],
        "kwargs_get_frozen_params_reappeared": result["kwargs_get_frozen_params_reappeared"],
    }, ensure_ascii=False, indent=2))
