"""Live validation for frozen Ab2d-v2 contract-aligned prompts (16 cells).

Reads ab2d_v2_rerun_manifest.json. Does not modify prompts, toolbox, SSOT,
task contracts, oracles, evaluators, or evaluation_revision_003.
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
from agent_tools.finals_rebuild.math16_pool import frozen_for_prompt, tasks_by_id
from scripts.ce115_v4_gemini_transport import MODEL_ID
from scripts.run_math16_latex_v1_gemini_live import (
    call_gemini_with_retries,
    classify_math16_response,
    ensure_api_key_via_dialog,
)

RUN_ID = "gemini35flash_math16_ab2d_v2_r1"
RERUN_MANIFEST = (
    ROOT
    / "docs/experiments/results/domain_api_contract_hardening_v2/ab2d_v2_rerun_manifest.json"
)
FREEZE_MANIFEST = (
    ROOT
    / "docs/experiments/results/domain_api_contract_hardening_v2/ab2d_v2_freeze_manifest.json"
)
OUT_DIR = ROOT / "docs/experiments/results" / RUN_ID
ORIG_RUN = "gemini35flash_math16_latex_v1_ab123_run_001"
SEED = 2026071301
EXPECTED_CELLS = 16


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


def _short_cell_id(task_id: str, condition: str) -> str:
    short = (
        task_id.replace("ce115_calc_", "c115_")
        .replace("ce111_", "c111_")
        .replace("ce112_", "c112_")
        .replace("ce113_", "c113_")
        .replace("ce111_nonchoice_", "c111_nc_")
    )
    return f"g35f__{short}__{condition}__s{SEED}__ab2d_v2_r1"


def main() -> int:
    if OUT_DIR.exists():
        raise SystemExit(f"output exists: {OUT_DIR}")
    freeze = json.loads(FREEZE_MANIFEST.read_text(encoding="utf-8"))
    rerun = json.loads(RERUN_MANIFEST.read_text(encoding="utf-8"))
    if _sha256_file(RERUN_MANIFEST) != freeze["rerun_manifest_sha256"]:
        raise SystemExit("rerun manifest sha256 drift vs freeze")
    planned = rerun["cells"]
    if len(planned) != EXPECTED_CELLS or rerun.get("cell_count") != EXPECTED_CELLS:
        raise SystemExit(f"expected {EXPECTED_CELLS} cells, got {len(planned)}")
    if freeze.get("changed_cells") != EXPECTED_CELLS:
        raise SystemExit("freeze changed_cells != 16")
    if freeze.get("unexpected_prompt_hash_changes", 0) != 0:
        raise SystemExit("freeze reports unexpected hash changes")

    by_id = tasks_by_id()
    ensure_api_key_via_dialog()
    OUT_DIR.mkdir(parents=True)
    rows: list[dict[str, Any]] = []
    for item in planned:
        tid = item["task_id"]
        cond = item["condition"]
        if cond != "ab2d":
            raise SystemExit(f"non-ab2d planned cell forbidden: {tid}@{cond}")
        task = by_id[tid]
        frozen = frozen_for_prompt(task)
        prompt = build_condition_prompt(cond, task, frozen)
        live_hash = prompt_sha256(prompt)
        if live_hash != item["frozen_prompt_hash"]:
            raise SystemExit(
                f"prompt hash drift for {tid}@{cond}: "
                f"live={live_hash} frozen={item['frozen_prompt_hash']}"
            )
        cell_id = _short_cell_id(tid, cond)
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
            failure_category = {
                "PASSED": "none",
                "ANSWER_INCORRECT": "answer_incorrect",
                "LATEX_MISMATCH": "latex_mismatch",
                "STRUCTURAL_MISMATCH": "structural_mismatch",
                "EXECUTION_FAILURE": "execution_failure",
                "SCHEMA_FAILURE": "schema_failure",
                "INTRINSIC_SAFETY": "intrinsic_safety",
            }.get(evaluator, "model_generated_failure")
        except BaseException as exc:  # noqa: BLE001
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
        g6 = (
            evaluate_math_notation(question_text)
            if question_text
            else {"status": "NOT_OBSERVED", "reason": "question_text_unavailable"}
        )

        adoption: Any = "NOT_APPLICABLE"
        if code:
            try:
                ops = resolve_task_operations(tid, frozen["oracle_payload"])
                adoption = scan_toolbox(code, ops)
            except Exception as exc:  # noqa: BLE001
                adoption = {"classification": "ASSEMBLY_SCAN_UNAVAILABLE", "note": str(exc)}

        provenance = {
            "post_hoc_v2_validation": True,
            "ab2d_v2_scope": "api_contract_only",
            "freeze_id": freeze.get("freeze_id"),
            "original_run_id": ORIG_RUN,
            "old_prompt_hash": item["old_prompt_hash"],
            "frozen_prompt_hash": item["frozen_prompt_hash"],
            "not_merged_into_evaluation_revision_003": True,
            "rerun_manifest_cell_id": item["cell_id"],
        }
        if tid == "ce115_calc_polynomial_factor_roots_l1":
            provenance["original_cell_adjudication"] = (
                "INVALID_CONTRACT / API_DOCUMENTATION_MISMATCH"
            )
            provenance["original_cell_retained"] = True

        artifact = {
            "run_id": RUN_ID,
            "cell_id": cell_id,
            "task_id": tid,
            "condition": cond,
            "seed": SEED,
            "model": MODEL_ID,
            "post_hoc_v2_validation": True,
            "not_merged_into_evaluation_revision_003": True,
            "provenance": provenance,
            "component_hashes": {
                "domain_api_ssot": _sha256_file(
                    ROOT / "agent_tools/finals_rebuild/domain_api_ssot.py"
                ),
                "clean_incremental_ablation": _sha256_file(
                    ROOT / "agent_tools/finals_rebuild/ce115_clean_incremental_ablation.py"
                ),
                "prompt_sha256": live_hash,
            },
            "frozen_parameters": frozen["oracle_payload"],
            "audit_oracle_payload": task["oracle_payload"],
            "canonical_prompt_hash": live_hash,
            "prompt_hash": live_hash,
            "evaluator_status": evaluator,
            "failure_category": failure_category,
            "first_attempt_evaluator_outcome": evaluator,
            "first_attempt_only": True,
            "api_attempts": api_attempts,
            "token_metadata": metadata,
            "duration_metadata": {"wall_clock_seconds": wall},
            "evaluator_details": details,
            "adoption_status": adoption,
            "exception_type": exception_type,
            "exception_message": exception_message,
            "traceback": trace,
            "g6_math_notation": g6,
            "gates": details.get("evaluation_gates"),
        }
        _write_json(cell_dir / "artifact.json", artifact)
        rows.append(
            {
                "cell_id": cell_id,
                "task_id": tid,
                "condition": cond,
                "evaluator_status": evaluator,
                "old_prompt_hash": item["old_prompt_hash"],
                "frozen_prompt_hash": live_hash,
            }
        )
        print(json.dumps(rows[-1], ensure_ascii=False), flush=True)

    summary = {
        "run_id": RUN_ID,
        "model": MODEL_ID,
        "freeze_id": freeze.get("freeze_id"),
        "planned_cells": len(planned),
        "executed_cells": len(rows),
        "planned_equals_executed": len(planned) == len(rows),
        "post_hoc_v2_validation": True,
        "not_merged_into_evaluation_revision_003": True,
        "ab2d_v2_scope": "api_contract_only",
        "cells": rows,
        "by_status": {
            k: sum(1 for r in rows if r["evaluator_status"] == k)
            for k in sorted({r["evaluator_status"] for r in rows})
        },
    }
    _write_json(OUT_DIR / "summary.json", summary)
    _write_json(
        OUT_DIR / "manifest.json",
        {
            "run_id": RUN_ID,
            "planned_from": str(RERUN_MANIFEST.relative_to(ROOT)).replace("\\", "/"),
            "freeze_manifest": str(FREEZE_MANIFEST.relative_to(ROOT)).replace("\\", "/"),
            "cells": [r["cell_id"] for r in rows],
            "post_hoc_v2_validation": True,
            "not_merged_into_evaluation_revision_003": True,
        },
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
