"""Math16 Phase 1: Qwen multiseed H0 generation (additive; does not modify freeze assets).

Generates one model x seed block (48 cells) under:
  docs/experiments/results/<slug>_math16_ab123_run_003_multiseed/seed_<seed>/

Resume: complete cells are identity-skipped (no model call). Divergent raw for the
same completed cell raises PROTOCOL_DUPLICATE_DIVERGENT_RAW.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
import time
import traceback
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.ce115_ab2d_assembly import resolve_task_operations, scan_toolbox
from agent_tools.finals_rebuild.ce115_clean_incremental_ablation import (
    LINEAGE_ID,
    build_condition_prompt,
    prompt_sha256,
)
from agent_tools.finals_rebuild.failure_classification_v2 import (
    classify_math16_cell_for_future_runner,
)
from agent_tools.finals_rebuild.generator_success import evaluate_math_notation
from agent_tools.finals_rebuild.latex_render_validation import evaluate_notation_lint
from agent_tools.finals_rebuild.math16_pool import (
    POOL_ID,
    frozen_for_prompt,
    load_pool_manifest,
    tasks_by_id,
)
from scripts.math16_qwen_ollama_adapter import (
    DEFAULT_BASE_URL,
    TEMPERATURE,
    TOP_K,
    TOP_P,
    InvalidInfrastructureError,
    call_qwen_with_retries,
    frozen_inference_config,
    probe_ollama,
)
from scripts.run_math16_latex_v1_qwen_ollama_live import (
    CONDITIONS,
    MODEL_SLUG,
    _adoption_status,
    build_summary,
    preliminary_failure_layer,
    verify_freeze_assets_match,
    verify_prompt_hashes_unchanged,
)
from scripts.run_math16_latex_v1_gemini_live import classify_math16_response

ALLOWED_SEEDS = (2026072001, 2026072002, 2026072003, 2026072004)
EXPECTED_DIGEST = {
    "qwen3.5:4b": "2a654d98e6fba55d452b7043684e9b57a947e393bbffa62485a7aac05ee4eefd",
    "qwen3.5:9b": "6488c96fa5faab64bb65cbd30d4289e20e6130ef535a93ef9a49f42eda893ea7",
}
FORBIDDEN_PATH_MARKERS = (
    "qwen35_4b_math16_ab123_run_002",
    "qwen35_9b_math16_ab123_run_002",
    "gemini35flash_math16_latex_v1_ab123_run_001",
)


def _hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=path.name + ".", dir=str(path.parent))
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_path, path)
    finally:
        if tmp_path.exists():
            try:
                tmp_path.unlink()
            except OSError:
                pass


def _write_json(path: Path, value: object) -> None:
    _atomic_write_text(
        path,
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, default=str) + "\n",
    )


def _model_prefix(model: str) -> str:
    return MODEL_SLUG[model]


def _run_root(model: str) -> Path:
    return ROOT / "docs/experiments/results" / f"{_model_prefix(model)}_math16_ab123_run_003_multiseed"


def _seed_dir(model: str, seed: int) -> Path:
    return _run_root(model) / f"seed_{seed}"


def _assert_safe_output(path: Path) -> None:
    resolved = str(path.resolve()).replace("\\", "/")
    for marker in FORBIDDEN_PATH_MARKERS:
        if marker in resolved:
            raise RuntimeError(f"REFUSING_WRITE_TO_FORBIDDEN_PATH: {path}")
    if "run_003_multiseed" not in resolved:
        raise RuntimeError(f"output must be under run_003_multiseed: {path}")


def _cell_complete(cell_dir: Path) -> bool:
    art = cell_dir / "artifact.json"
    raw = cell_dir / "raw_response.txt"
    if not art.exists() or not raw.exists():
        return False
    try:
        artifact = json.loads(art.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    return bool(artifact.get("persisted_complete")) and raw.stat().st_size >= 0


def build_plan(
    output_dir: Path,
    *,
    model: str,
    seed: int,
    service_meta: dict[str, Any],
) -> dict[str, Any]:
    manifest = load_pool_manifest()
    tasks = tasks_by_id()
    prefix = _model_prefix(model)
    cells = []
    for tid in manifest["task_ids"]:
        task = tasks[tid]
        frozen = frozen_for_prompt(task)
        for condition in CONDITIONS:
            prompt = build_condition_prompt(condition, task, frozen)
            cell_id = f"{prefix}__{tid}__{condition}__seed_{seed}"
            cells.append(
                {
                    "cell_id": cell_id,
                    "task_id": tid,
                    "domain": task["domain"],
                    "domain_ops": task["domain_ops"],
                    "family": task["skill_id"],
                    "oracle_type": task["oracle_type"],
                    "condition": condition,
                    "treatment": condition,
                    "seed": seed,
                    "model": model,
                    "model_digest": service_meta.get("model_digest"),
                    "frozen_parameters": frozen["oracle_payload"],
                    "audit_oracle_payload": task["oracle_payload"],
                    "expected_answer": task["correct_answer"],
                    "math16_question_text": task["math16_question_text"],
                    "prompt": prompt,
                    "canonical_prompt_hash": prompt_sha256(prompt),
                    "prompt_hash": prompt_sha256(prompt),
                    "prompt_lineage": LINEAGE_ID,
                    "pool_id": POOL_ID,
                    "first_attempt_only": True,
                    "healer": 0,
                }
            )
    cfg = frozen_inference_config()
    cfg["model"] = model
    cfg["seed_default"] = seed
    plan = {
        "run_id": f"{_model_prefix(model)}_math16_ab123_run_003_multiseed",
        "seed_block_id": f"seed_{seed}",
        "pool_id": POOL_ID,
        "model": model,
        "model_digest": service_meta.get("model_digest"),
        "runtime": "ollama",
        "runtime_version": service_meta.get("runtime_version"),
        "seed": seed,
        "prompt_lineage": LINEAGE_ID,
        "conditions": list(CONDITIONS),
        "task_ids": list(manifest["task_ids"]),
        "planned_cells": len(cells),
        "cells": cells,
        "itt_protocol": "first_valid_model_response_fixed; api_retry_same_cell; healer=0",
        "itt_policy": "first_valid_model_response_fixed; api_retry_same_cell; healer=0",
        "inference_config": cfg,
        "service_meta": service_meta,
        "qwen_live": True,
        "phase": "MATH16-R05-Phase1",
        "resume_enabled": True,
    }
    plan["plan_hash"] = _hash(
        json.dumps({k: v for k, v in plan.items() if k != "cells"}, sort_keys=True, default=str)
    )
    return plan


def validate_block(output_dir: Path, *, model: str, seed: int) -> dict[str, Any]:
    cells_root = output_dir / "cells"
    arts = sorted(cells_root.glob("*/artifact.json")) if cells_root.exists() else []
    raws = sorted(cells_root.glob("*/raw_response.txt")) if cells_root.exists() else []
    extracted = list(cells_root.glob("*/extracted_candidate.py")) if cells_root.exists() else []
    ids = []
    hash_ok = 0
    for art_path in arts:
        art = json.loads(art_path.read_text(encoding="utf-8"))
        ids.append(art["cell_id"])
        h = art.get("hashes") or {}
        if h.get("prompt") and h.get("raw") is not None and "extracted_candidate" in h:
            hash_ok += 1
    unique = len(set(ids))
    report = {
        "model": model,
        "seed": seed,
        "artifact_count": len(arts),
        "raw_count": len(raws),
        "extracted_count": len(extracted),
        "unique_cell_ids": unique,
        "hashes_complete": hash_ok,
        "duplicate": len(ids) - unique,
        "ok": len(arts) == 48 and len(raws) == 48 and unique == 48 and hash_ok == 48 and len(ids) == unique,
    }
    return report


def run_block(model: str, seed: int, *, resume: bool = True) -> dict[str, Any]:
    if seed not in ALLOWED_SEEDS:
        raise RuntimeError(f"seed not in Phase-1 allowlist: {seed}")
    if model not in MODEL_SLUG:
        raise RuntimeError(f"model not allowed: {model}")

    output_dir = _seed_dir(model, seed)
    _assert_safe_output(output_dir)

    prompt_check = verify_prompt_hashes_unchanged()
    if not prompt_check["ok"]:
        raise RuntimeError(f"PROMPT_HASH_CHANGED: {prompt_check['mismatches'][:3]}")
    freeze_check = verify_freeze_assets_match()
    if not freeze_check["ok"]:
        raise RuntimeError(f"FREEZE_HASH_MISMATCH: {freeze_check['mismatches']}")

    service_meta = probe_ollama(base_url=DEFAULT_BASE_URL, model=model)
    expected = EXPECTED_DIGEST[model]
    if service_meta.get("model_digest") != expected:
        raise RuntimeError(
            f"MODEL_DIGEST_MISMATCH: got {service_meta.get('model_digest')} expected {expected}"
        )

    plan = build_plan(output_dir, model=model, seed=seed, service_meta=service_meta)
    if len(plan["cells"]) != 48:
        raise RuntimeError(f"planned cells != 48: {len(plan['cells'])}")

    output_dir.mkdir(parents=True, exist_ok=True)
    _write_json(
        output_dir / "preflight_checks.json",
        {
            "prompt_hash_check": prompt_check,
            "freeze_hash_check": freeze_check,
            "service_meta": service_meta,
            "inference_config": plan["inference_config"],
            "seed": seed,
            "model": model,
        },
    )
    plan_for_disk = dict(plan)
    plan_for_disk["cells"] = [
        {k: v for k, v in cell.items() if k != "prompt"} for cell in plan["cells"]
    ]
    _write_json(output_dir / "manifest.json", plan_for_disk)

    tasks = tasks_by_id()
    rows: list[dict[str, Any]] = []
    journal_path = output_dir / "cell_journal.jsonl"
    fatal_stop: str | None = None
    run_started = time.monotonic()
    consecutive_l0 = 0
    skipped = 0
    generated = 0
    block_model_calls_before = 0

    for index, cell in enumerate(plan["cells"]):
        if fatal_stop:
            break
        cell_dir = output_dir / "cells" / cell["cell_id"]
        prompt = cell["prompt"]

        if resume and _cell_complete(cell_dir):
            existing = json.loads((cell_dir / "artifact.json").read_text(encoding="utf-8"))
            existing_raw = (cell_dir / "raw_response.txt").read_text(encoding="utf-8")
            existing_hash = (existing.get("hashes") or {}).get("raw")
            current_hash = _hash(existing_raw)
            if existing_hash and existing_hash != current_hash:
                raise RuntimeError(
                    f"PROTOCOL_DUPLICATE_DIVERGENT_RAW: {cell['cell_id']} "
                    f"artifact.raw_hash={existing_hash} file_hash={current_hash}"
                )
            # Identity-skip: never call the model again for a complete cell.
            rows.append(existing)
            skipped += 1
            continue

        # Incomplete / missing: if raw exists without complete artifact, treat as incomplete resume.
        if cell_dir.exists() and (cell_dir / "raw_response.txt").exists() and not _cell_complete(cell_dir):
            # Safe to continue completing evaluation from existing raw without re-calling model.
            raw_existing = (cell_dir / "raw_response.txt").read_text(encoding="utf-8")
            partial_resume = True
        else:
            raw_existing = None
            partial_resume = False

        cell_dir.mkdir(parents=True, exist_ok=True)
        _atomic_write_text(cell_dir / "prompt.txt", prompt)

        started = time.monotonic()
        raw = ""
        code = None
        exception_type = exception_message = trace = None
        metadata: dict[str, Any] = {}
        api_attempts: list[dict[str, Any]] = []
        completion = "INFRASTRUCTURE_FAILURE"
        adoption: Any = "NOT_APPLICABLE"
        evaluator = "NOT_RUN"
        details: dict[str, Any] = {}
        failure_category = "none"
        validity: str | None = None
        timestamp = datetime.now(timezone.utc).isoformat()

        try:
            if partial_resume:
                raw = raw_existing or ""
                metadata = {
                    "resume_from_existing_raw": True,
                    "model": model,
                    "seed": seed,
                    "think": False,
                    "done_reason": "resume_partial_no_model_call",
                }
                api_attempts = [
                    {
                        "attempt": 0,
                        "status": "identity_resume_raw",
                        "retryable": False,
                        "exception_type": None,
                        "exception_message": None,
                    }
                ]
            else:
                response = call_qwen_with_retries(
                    prompt,
                    seed=seed,
                    model=model,
                    base_url=DEFAULT_BASE_URL,
                )
                raw = response["raw_text"]
                metadata = dict(response.get("metadata") or {})
                api_attempts = list(response.get("api_attempts") or [])
                generated += 1
                block_model_calls_before += 1

            task = tasks[cell["task_id"]]
            outcome, evaluated_code, details = classify_math16_response(
                raw,
                frozen_params=cell["frozen_parameters"],
                audit_oracle_payload=cell["audit_oracle_payload"],
                task=task,
            )
            code = evaluated_code
            completion = "NATURAL_COMPLETE" if code else outcome.upper()
            if outcome == "passed":
                evaluator = "PASSED"
            elif outcome == "answer_incorrect":
                evaluator = "ANSWER_INCORRECT"
            elif outcome in {"runtime_failure", "infrastructure_failure"}:
                evaluator = "EXECUTION_FAILURE"
            elif outcome == "schema_failure":
                evaluator = "SCHEMA_FAILURE"
            elif outcome == "structural_mismatch":
                evaluator = "STRUCTURAL_MISMATCH"
            elif outcome == "latex_mismatch":
                evaluator = "LATEX_MISMATCH"
            else:
                evaluator = outcome.upper()
            adoption = _adoption_status(
                code, cell["task_id"], cell["frozen_parameters"], cell["condition"]
            )
            if evaluator == "PASSED":
                failure_category = "none"
                consecutive_l0 = 0
            elif evaluator == "ANSWER_INCORRECT":
                failure_category = "answer_incorrect"
                consecutive_l0 = 0
            else:
                failure_category = outcome if outcome != "passed" else "model_generated_failure"
                consecutive_l0 = 0
        except InvalidInfrastructureError as exc:
            exception_type, exception_message = type(exc).__name__, str(exc)
            trace = traceback.format_exc()
            api_attempts = list(exc.api_attempts)
            metadata = exc.as_metadata()
            failure_category = "L0_INVALID_INFRASTRUCTURE"
            evaluator = "L0_INVALID_INFRASTRUCTURE"
            completion = "INFRASTRUCTURE_FAILURE"
            validity = "INVALID_INFRASTRUCTURE"
            consecutive_l0 += 1
        except BaseException as exc:
            exception_type, exception_message = type(exc).__name__, str(exc)
            trace = traceback.format_exc()
            failure_category = "transport_or_infrastructure_failure"
            evaluator = "INFRASTRUCTURE_FAILURE"
            validity = "INVALID_INFRASTRUCTURE"
            consecutive_l0 += 1
            fatal_stop = f"UNEXPECTED_STOP at {cell['cell_id']}: {exception_type}: {exc}"

        wall = time.monotonic() - started
        if not partial_resume:
            # Only write raw when we produced a first-attempt (or L0 empty) in this call.
            # For partial resume, raw file already exists — do not overwrite.
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
        g6a = (
            evaluate_notation_lint(question_text, side="question")
            if question_text
            else {"status": "NOT_OBSERVED", "reason": "question_text_unavailable"}
        )
        failure_layer = preliminary_failure_layer(evaluator, validity=validity)

        load_duration = metadata.get("load_duration")
        cold_start = False
        if isinstance(load_duration, (int, float)) and load_duration >= 1_000_000_000:
            # Ollama load_duration is nanoseconds; >=1s implies model load.
            cold_start = True
        elif generated == 1 and not partial_resume:
            cold_start = True
        warm_run = not cold_start

        req_opts = ((metadata.get("request_payload") or {}).get("options")) or {}
        effective_settings = {
            "temperature": req_opts.get("temperature", TEMPERATURE),
            "top_p": req_opts.get("top_p", TOP_P),
            "top_k": req_opts.get("top_k", TOP_K),
            "repeat_penalty": "ollama_default",
            "num_ctx": req_opts.get("num_ctx"),
            "num_predict": req_opts.get("num_predict"),
            "think": False,
            "seed": seed,
            "model": model,
            "model_digest": service_meta.get("model_digest"),
        }

        artifact = {k: v for k, v in cell.items() if k != "prompt"}
        artifact.update(
            {
                "run_id": plan["run_id"],
                "seed_block_id": plan["seed_block_id"],
                "completion_status": completion,
                "adoption_status": adoption,
                "evaluator_status": evaluator,
                "failure_category": failure_category,
                "failure_class": failure_category,
                "failure_layer": failure_layer,
                "validity": validity,
                "exception_type": exception_type,
                "exception_message": exception_message,
                "traceback": trace,
                "evaluator_details": details,
                "first_attempt_evaluator_outcome": evaluator,
                "pipeline_correction": {
                    "applied": False,
                    "note": "pipeline correction disabled; accounted separately",
                },
                "healer": {
                    "enabled": False,
                    "eligibility": failure_layer.get("eligibility"),
                    "healer_eligible": failure_layer.get("healer_eligible"),
                    "attempted": False,
                    "outcome": "NOT_RUN",
                    "note": "healer=0; eligibility marked only; H0 has no repaired source",
                },
                "api_attempts": api_attempts,
                "token_metadata": metadata,
                "duration_metadata": {
                    "wall_clock_seconds": wall,
                    "provider_duration": metadata.get("latency_ms"),
                },
                "latex_g6": g6,
                "latex_g6a": g6a,
                "gates": details.get("evaluation_gates") or details.get("gates"),
                "failure_classification_v2": classify_math16_cell_for_future_runner(
                    evaluation_gates=details.get("evaluation_gates") or details.get("gates"),
                    evaluator_status=evaluator,
                    validity=validity,
                    infrastructure_valid=validity != "INVALID_INFRASTRUCTURE",
                    raw_response_present=bool(raw),
                ),
                "hashes": {
                    "prompt": _hash(prompt),
                    "raw": _hash(raw),
                    "extracted_candidate": _hash(code or ""),
                    "source": _hash(code or raw or ""),
                },
                "provenance": {
                    "first_attempt_only": True,
                    "api_retry_same_cell": True,
                    "healer": 0,
                    "model_calls": sum(1 for a in api_attempts if a.get("status") == "success"),
                    "api_attempt_count": len(api_attempts),
                    "identity_skip": False,
                    "partial_resume_no_model_call": partial_resume,
                },
                "effective_generation_settings": effective_settings,
                "done_reason": metadata.get("done_reason"),
                "timestamp_utc": timestamp,
                "cold_start": cold_start,
                "warm_run": warm_run,
                "persisted_complete": True,
                "cell_index": index,
                "evaluator_provenance": {
                    "revision": "math16_latex_semantic_v2",
                    "module": "agent_tools/finals_rebuild/math16_oracles.py",
                    "via": "scripts.run_math16_latex_v1_gemini_live.classify_math16_response",
                },
            }
        )
        _write_json(cell_dir / "artifact.json", artifact)
        rows.append(artifact)
        with journal_path.open("a", encoding="utf-8") as handle:
            handle.write(
                json.dumps(
                    {
                        "cell_id": artifact["cell_id"],
                        "evaluator_status": evaluator,
                        "failure_category": failure_category,
                        "primary_layer": failure_layer.get("primary_layer"),
                        "identity_skip": False,
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )
            handle.flush()
            os.fsync(handle.fileno())

        _write_json(
            output_dir / "checkpoint.json",
            {
                "run_id": plan["run_id"],
                "model": model,
                "seed": seed,
                "completed_cells": len(rows),
                "planned_cells": 48,
                "skipped_identity": skipped,
                "generated_this_invocation": generated,
                "last_cell_id": artifact["cell_id"],
                "fatal_stop": fatal_stop,
                "consecutive_l0": consecutive_l0,
            },
        )

        if consecutive_l0 >= 3:
            fatal_stop = (
                f"STOP_AFTER_3_CONSECUTIVE_L0 at {artifact['cell_id']}; "
                "awaiting human instruction"
            )
            break
        if fatal_stop:
            break

    # Reload all completed cells for authoritative summary (includes prior skips).
    all_rows: list[dict[str, Any]] = []
    for cell in plan["cells"]:
        art_path = output_dir / "cells" / cell["cell_id"] / "artifact.json"
        if art_path.exists():
            all_rows.append(json.loads(art_path.read_text(encoding="utf-8")))

    wall_total = time.monotonic() - run_started
    _write_json(output_dir / "cell_results.json", all_rows)
    summary = build_summary(plan, all_rows, fatal_stop=fatal_stop, wall_clock_seconds=wall_total)
    summary["identity_skipped"] = skipped
    summary["generated_this_invocation"] = generated
    summary["seed"] = seed
    block_validation = validate_block(output_dir, model=model, seed=seed)
    summary["block_validation"] = block_validation
    _write_json(output_dir / "summary.json", summary)
    if fatal_stop:
        _write_json(
            output_dir / "breakpoint.json",
            {
                "fatal_stop": fatal_stop,
                "completed_cells": len(all_rows),
                "last_cell_id": all_rows[-1]["cell_id"] if all_rows else None,
                "instruction": "Do not clear completed cells; resume with --resume.",
            },
        )
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, choices=sorted(MODEL_SLUG))
    parser.add_argument("--seed", required=True, type=int, choices=list(ALLOWED_SEEDS))
    parser.add_argument("--resume", action="store_true", default=True)
    parser.add_argument("--no-resume", action="store_true")
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    resume = not args.no_resume
    output_dir = _seed_dir(args.model, args.seed)
    if args.validate_only:
        report = validate_block(output_dir, model=args.model, seed=args.seed)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if report["ok"] else 1

    summary = run_block(args.model, args.seed, resume=resume)
    print(
        json.dumps(
            {
                "output_dir": str(output_dir),
                "complete_48": summary.get("complete_48"),
                "attempted_cells": summary.get("attempted_cells"),
                "identity_skipped": summary.get("identity_skipped"),
                "generated_this_invocation": summary.get("generated_this_invocation"),
                "fatal_stop": summary.get("fatal_stop"),
                "block_validation": summary.get("block_validation"),
                "failure_layer_distribution": summary.get("failure_layer_distribution"),
                "by_treatment": summary.get("by_treatment"),
                "wall_clock_seconds": summary.get("wall_clock_seconds"),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if summary.get("complete_48") and summary.get("block_validation", {}).get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
