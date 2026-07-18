"""Supplemental single-cell live rerun: q10 Ab2d after Fraction contract boundary fix.

Does not modify or overwrite the original 48-cell run artifacts.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import tempfile
import time
import traceback
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.ce115_ab2d_assembly import resolve_task_operations, scan_toolbox
from agent_tools.finals_rebuild.ce115_clean_incremental_ablation import (
    build_condition_prompt,
    prompt_sha256,
)
from agent_tools.finals_rebuild.generator_success import evaluate_math_notation
from agent_tools.finals_rebuild.latex_render_validation import evaluate_notation_lint
from agent_tools.finals_rebuild.math16_pool import frozen_for_prompt, tasks_by_id
from scripts.ce115_v4_gemini_transport import MODEL_ID
from scripts.run_math16_latex_v1_gemini_live import (
    call_gemini_with_retries,
    classify_math16_response,
    ensure_api_key_via_dialog,
)

REVISION_ID = "Math16-LaTeX-v1-q10-ab2d-contract-fix-r1"
RUN_ID = "gemini35flash_math16_q10_ab2d_contract_fix_r1"
TASK_ID = "ce111_q10_ordered_quadratic_roots_radical"
CONDITION = "ab2d"
SEED = 2026071301
ORIGINAL_RUN = ROOT / "docs/experiments/results/gemini35flash_math16_latex_v1_ab123_run_001"
ORIGINAL_CELL_ID = (
    f"gemini_3_5_flash__{TASK_ID}__{CONDITION}__seed_{SEED}"
)
OUT_DIR = ROOT / "docs/experiments/results" / RUN_ID


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=path.name + ".", dir=str(path.parent))
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
        tmp_path.replace(path)
    finally:
        if tmp_path.exists():
            tmp_path.unlink(missing_ok=True)


def _write_json(path: Path, payload: Any) -> None:
    _atomic_write_text(path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def _adoption_status(code: str | None, task_id: str, frozen: dict[str, Any], condition: str) -> Any:
    if condition != "ab2d" or not code:
        return "NOT_APPLICABLE"
    try:
        ops = resolve_task_operations(task_id, frozen)
        return scan_toolbox(code, ops)
    except Exception as exc:  # noqa: BLE001
        return {"classification": "ASSEMBLY_SCAN_UNAVAILABLE", "note": str(exc)}


def main() -> int:
    if OUT_DIR.exists():
        raise SystemExit(f"output directory already exists: {OUT_DIR}")
    if not (ORIGINAL_RUN / "cells" / ORIGINAL_CELL_ID / "artifact.json").is_file():
        raise SystemExit(f"missing original invalid cell: {ORIGINAL_CELL_ID}")

    original_art = json.loads(
        (ORIGINAL_RUN / "cells" / ORIGINAL_CELL_ID / "artifact.json").read_text(encoding="utf-8")
    )
    original_prompt = (
        ORIGINAL_RUN / "cells" / ORIGINAL_CELL_ID / "prompt.txt"
    ).read_text(encoding="utf-8")

    task = tasks_by_id()[TASK_ID]
    frozen = frozen_for_prompt(task)
    prompt = build_condition_prompt(CONDITION, task, frozen)
    if prompt != original_prompt:
        raise SystemExit(
            "REFUSING_RERUN: rebuilt prompt differs from original cell prompt.txt "
            "(prompt semantics must remain unchanged)"
        )
    if prompt_sha256(prompt) != original_art.get("canonical_prompt_hash") and prompt_sha256(
        prompt
    ) != original_art.get("prompt_hash"):
        # still allow if text equal (already checked); hash field name variance only
        pass

    hashes = {
        "component_evaluator_math16_oracles": _sha256_file(
            ROOT / "agent_tools/finals_rebuild/math16_oracles.py"
        ),
        "component_math_answer_contracts": _sha256_file(
            ROOT / "agent_tools/finals_rebuild/math_answer_contracts.py"
        ),
        "component_runner_math16_live": _sha256_file(
            ROOT / "scripts/run_math16_latex_v1_gemini_live.py"
        ),
        "prompt_sha256": prompt_sha256(prompt),
    }

    ensure_api_key_via_dialog()
    OUT_DIR.mkdir(parents=True)
    cell_id = f"gemini_3_5_flash__{TASK_ID}__{CONDITION}__seed_{SEED}__{REVISION_ID}"
    cell_dir = OUT_DIR / "cells" / cell_id
    cell_dir.mkdir(parents=True)
    _atomic_write_text(cell_dir / "prompt.txt", prompt)

    started = time.monotonic()
    raw = ""
    code = None
    exception_type = exception_message = trace = None
    metadata: dict[str, Any] = {}
    api_attempts: list[dict[str, Any]] = []
    evaluator = "NOT_RUN"
    failure_category = "none"
    details: dict[str, Any] = {}
    try:
        response = call_gemini_with_retries(prompt)
        raw = response["raw_text"]
        metadata = dict(response.get("metadata") or {})
        api_attempts = list(response.get("api_attempts") or [])
        outcome, evaluated_code, details = classify_math16_response(
            raw,
            frozen_params=frozen["oracle_payload"],
            audit_oracle_payload=task["oracle_payload"],
            task=task,
        )
        code = evaluated_code
        if outcome == "passed":
            evaluator = "PASSED"
        elif outcome == "answer_incorrect":
            evaluator = "ANSWER_INCORRECT"
        elif outcome in {"runtime_failure", "infrastructure_failure"}:
            evaluator = "EXECUTION_FAILURE"
        elif outcome == "schema_failure":
            evaluator = "SCHEMA_FAILURE"
        else:
            evaluator = outcome.upper()
        if evaluator == "PASSED":
            failure_category = "none"
        elif evaluator == "ANSWER_INCORRECT":
            failure_category = "answer_incorrect"
        elif evaluator == "EXECUTION_FAILURE":
            failure_category = "execution_failure"
        else:
            failure_category = "model_generated_failure"
    except BaseException as exc:
        exception_type, exception_message = type(exc).__name__, str(exc)
        trace = traceback.format_exc()
        evaluator = "INFRASTRUCTURE_FAILURE"
        failure_category = "transport_or_infrastructure_failure"

    wall = time.monotonic() - started
    _atomic_write_text(cell_dir / "raw_response.txt", raw)
    if code is not None:
        _atomic_write_text(cell_dir / "extracted_candidate.py", code)

    question_text = None
    if isinstance(details.get("returned_value"), dict):
        question_text = details["returned_value"].get("question_text")
    g6 = evaluate_math_notation(question_text) if question_text else {
        "status": "NOT_OBSERVED",
        "reason": "question_text_unavailable",
    }
    g6a = evaluate_notation_lint(question_text, side="question") if question_text else {
        "status": "NOT_OBSERVED",
        "reason": "question_text_unavailable",
    }

    artifact = {
        "run_id": RUN_ID,
        "revision_id": REVISION_ID,
        "cell_id": cell_id,
        "task_id": TASK_ID,
        "condition": CONDITION,
        "seed": SEED,
        "model": MODEL_ID,
        "post_hoc_supplemental_rerun": True,
        "provenance": {
            "original_run_id": "gemini35flash_math16_latex_v1_ab123_run_001",
            "original_cell_id": ORIGINAL_CELL_ID,
            "original_evaluator_status": original_art.get("evaluator_status"),
            "original_failure_category": original_art.get("failure_category"),
            "original_runtime_error": (original_art.get("evaluator_details") or {}).get(
                "runtime_error"
            ),
            "invalid_contract_reason": (
                "Ab2d FractionOps.create returned Fraction; oracle/JSON required int; "
                "fixed by integer-valued Fraction boundary"
            ),
            "original_artifacts_preserved": True,
            "replacement_rule": (
                "final corrected analysis uses this supplemental cell for "
                "q10 Ab2d only; other 47 cells remain from original run / evaluation_revision_002"
            ),
        },
        "component_hashes": hashes,
        "frozen_parameters": frozen["oracle_payload"],
        "audit_oracle_payload": task["oracle_payload"],
        "canonical_prompt_hash": prompt_sha256(prompt),
        "prompt_hash": prompt_sha256(prompt),
        "completion_status": "NATURAL_COMPLETE" if code else evaluator,
        "adoption_status": _adoption_status(code, TASK_ID, frozen["oracle_payload"], CONDITION),
        "evaluator_status": evaluator,
        "failure_category": failure_category,
        "first_attempt_evaluator_outcome": evaluator,
        "first_attempt_only": True,
        "pipeline_correction": {"applied": False, "note": "ITT first valid response fixed"},
        "healer": {
            "enabled": False,
            "attempted": False,
            "eligibility": "NOT_RUN",
            "outcome": "NOT_RUN",
        },
        "exception_type": exception_type,
        "exception_message": exception_message,
        "traceback": trace,
        "evaluator_details": details,
        "expected_answer": task.get("correct_answer"),
        "api_attempts": api_attempts,
        "token_metadata": metadata,
        "duration_metadata": {"wall_clock_seconds": wall, "provider_duration": None},
        "gates": details.get("evaluation_gates"),
        "g6_math_notation": g6,
        "g6a_notation_lint": g6a,
    }
    _write_json(cell_dir / "artifact.json", artifact)
    summary = {
        "run_id": RUN_ID,
        "revision_id": REVISION_ID,
        "cells": 1,
        "task_id": TASK_ID,
        "condition": CONDITION,
        "evaluator_status": evaluator,
        "model": MODEL_ID,
        "component_hashes": hashes,
        "original_cell_id": ORIGINAL_CELL_ID,
        "post_hoc_supplemental_rerun": True,
        "api_failure": evaluator in {"API_FAILURE", "API_FATAL_STOP"},
    }
    _write_json(OUT_DIR / "summary.json", summary)
    _write_json(OUT_DIR / "manifest.json", {
        "run_id": RUN_ID,
        "revision_id": REVISION_ID,
        "cells": [cell_id],
        "model": MODEL_ID,
        "original_run": str(ORIGINAL_RUN.relative_to(ROOT)).replace("\\", "/"),
    })
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if evaluator not in {"API_FAILURE", "API_FATAL_STOP", "INFRASTRUCTURE_FAILURE"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
