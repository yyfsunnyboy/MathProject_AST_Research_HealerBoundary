"""Math16 Phase 2: Gemini multiseed H0 generation (additive; does not modify freeze assets).

Label: repeated generations under fixed nominal seeds (provider does not guarantee
deterministic seed replication).
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
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

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
from scripts.ce115_v4_gemini_transport import (
    MAX_OUTPUT_TOKENS,
    MODEL_ID,
    REQUEST_TIMEOUT_SECONDS,
    TEMPERATURE,
    api_key_status,
    call_gemini_once,
    runtime_version,
)
from scripts.run_math16_latex_v1_gemini_live import (
    CONDITIONS,
    classify_math16_response,
)
from scripts.run_math16_latex_v1_qwen_ollama_live import (
    _adoption_status,
    build_summary,
    preliminary_failure_layer,
    verify_freeze_assets_match,
    verify_prompt_hashes_unchanged,
)

ALLOWED_SEEDS = (2026072001, 2026072002, 2026072003, 2026072004)
MODEL_SLUG = "gemini_3_5_flash"
RUN_PREFIX = "gemini35flash_math16_ab123_run_003_multiseed"
FORBIDDEN = (
    "gemini35flash_math16_latex_v1_ab123_run_001",
    "qwen35_4b_math16_ab123_run_002",
    "qwen35_9b_math16_ab123_run_002",
)
TRANSIENT_MARKERS = (
    "timeout",
    "timed out",
    "500",
    "502",
    "503",
    "504",
    "connection",
    "unavailable",
    "temporarily",
    "deadline",
    "reset",
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


def _seed_dir(seed: int) -> Path:
    return ROOT / "docs/experiments/results" / RUN_PREFIX / f"seed_{seed}"


def _assert_safe(path: Path) -> None:
    resolved = str(path.resolve()).replace("\\", "/")
    for marker in FORBIDDEN:
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
    return bool(artifact.get("persisted_complete"))


def _is_transient(exc: BaseException) -> bool:
    text = f"{type(exc).__name__}: {exc}".lower()
    return any(m in text for m in TRANSIENT_MARKERS)


def call_gemini_with_transient_policy(prompt: str, *, cell_id: str) -> dict[str, Any]:
    """At most one transient resume after no valid raw; max 2 transient failures → stop."""
    attempts: list[dict[str, Any]] = []
    transient_count = 0
    last_exc: BaseException | None = None
    for attempt in range(1, 4):
        started = time.monotonic()
        try:
            resp = call_gemini_once(prompt, model=MODEL_ID)
            raw = resp.get("raw_text") if isinstance(resp, dict) else None
            # call_gemini_once returns dict with raw_text or just text?
            if not isinstance(resp, dict):
                raise RuntimeError("unexpected gemini response type")
            raw = resp.get("raw_text")
            if raw is None and "text" in resp:
                raw = resp["text"]
            # transport returns {"raw_text", "metadata"} typically
            if not isinstance(raw, str) or not raw.strip():
                raise RuntimeError("empty_response")
            meta = dict(resp.get("metadata") or {})
            attempts.append(
                {
                    "attempt": attempt,
                    "status": "success",
                    "retryable": False,
                    "wall_clock_seconds": time.monotonic() - started,
                    "transient_failure_retry": attempt > 1,
                }
            )
            meta.update(
                {
                    "api_attempts": attempts,
                    "transient_failure_retry": attempt > 1,
                    "transient_failure_count": transient_count,
                }
            )
            return {"raw_text": raw, "metadata": meta, "api_attempts": attempts}
        except BaseException as exc:  # noqa: BLE001
            last_exc = exc
            retryable = _is_transient(exc)
            attempts.append(
                {
                    "attempt": attempt,
                    "status": "error",
                    "retryable": retryable,
                    "exception_type": type(exc).__name__,
                    "exception_message": str(exc),
                    "wall_clock_seconds": time.monotonic() - started,
                    "transient_failure_retry": retryable,
                    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                    "cell_id": cell_id,
                }
            )
            if not retryable:
                raise
            transient_count += 1
            if transient_count > 2:
                raise RuntimeError(
                    f"BLOCKED_WITH_EXACT_REASON: API unstable, manual review required "
                    f"(cell={cell_id}, transient_failures={transient_count})"
                ) from exc
            # one resume allowed after no valid raw
            time.sleep(5 * transient_count)
            continue
    raise RuntimeError(f"gemini call exhausted for {cell_id}: {last_exc}")


def build_plan(output_dir: Path, *, seed: int, service_meta: dict[str, Any]) -> dict[str, Any]:
    manifest = load_pool_manifest()
    tasks = tasks_by_id()
    cells = []
    for tid in manifest["task_ids"]:
        task = tasks[tid]
        frozen = frozen_for_prompt(task)
        for condition in CONDITIONS:
            prompt = build_condition_prompt(condition, task, frozen)
            cell_id = f"{MODEL_SLUG}__{tid}__{condition}__seed_{seed}"
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
                    "model": MODEL_ID,
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
    plan = {
        "run_id": RUN_PREFIX,
        "seed_block_id": f"seed_{seed}",
        "pool_id": POOL_ID,
        "model": MODEL_ID,
        "runtime": "google-generativeai",
        "runtime_version": service_meta.get("runtime_version"),
        "seed": seed,
        "seed_policy": "fixed_nominal_seed_field_only; provider_seed_not_guaranteed",
        "generation_label": "repeated generations under fixed nominal seeds",
        "prompt_lineage": LINEAGE_ID,
        "conditions": list(CONDITIONS),
        "task_ids": list(manifest["task_ids"]),
        "planned_cells": len(cells),
        "cells": cells,
        "itt_policy": "first_valid_model_response_fixed; transient_resume_only_if_no_raw; healer=0",
        "inference_config": {
            "provider": "google",
            "model": MODEL_ID,
            "temperature": TEMPERATURE,
            "max_output_tokens": MAX_OUTPUT_TOKENS,
            "top_p": "not_explicitly_set",
            "top_k": "not_explicitly_set",
            "request_timeout_seconds": REQUEST_TIMEOUT_SECONDS,
            "seed_support": "not_passed_to_GenerateContentConfig; nominal seed recorded in cell_id only",
        },
        "service_meta": service_meta,
        "gemini_live": True,
        "phase": "MATH16-R06-Phase2",
        "resume_enabled": True,
    }
    plan["plan_hash"] = _hash(
        json.dumps({k: v for k, v in plan.items() if k != "cells"}, sort_keys=True, default=str)
    )
    return plan


def validate_block(output_dir: Path, *, seed: int) -> dict[str, Any]:
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
    return {
        "model": MODEL_ID,
        "seed": seed,
        "artifact_count": len(arts),
        "raw_count": len(raws),
        "extracted_count": len(extracted),
        "unique_cell_ids": unique,
        "hashes_complete": hash_ok,
        "duplicate": len(ids) - unique,
        "ok": len(arts) == 48 and len(raws) == 48 and unique == 48 and hash_ok == 48,
    }


def run_block(seed: int, *, resume: bool = True) -> dict[str, Any]:
    if seed not in ALLOWED_SEEDS:
        raise RuntimeError(f"seed not allowed: {seed}")
    output_dir = _seed_dir(seed)
    _assert_safe(output_dir)

    prompt_check = verify_prompt_hashes_unchanged()
    if not prompt_check["ok"]:
        raise RuntimeError(f"PROMPT_HASH_CHANGED: {prompt_check['mismatches'][:3]}")
    freeze_check = verify_freeze_assets_match()
    if not freeze_check["ok"]:
        raise RuntimeError(f"FREEZE_HASH_MISMATCH: {freeze_check['mismatches']}")

    key = api_key_status()
    if not key.get("api_key_present"):
        raise RuntimeError("GEMINI_API_KEY missing")
    service_meta = {
        **key,
        "runtime_version": runtime_version(),
        "model": MODEL_ID,
        "temperature": TEMPERATURE,
        "max_output_tokens": MAX_OUTPUT_TOKENS,
    }
    plan = build_plan(output_dir, seed=seed, service_meta=service_meta)
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
        },
    )
    plan_for_disk = dict(plan)
    plan_for_disk["cells"] = [{k: v for k, v in c.items() if k != "prompt"} for c in plan["cells"]]
    _write_json(output_dir / "manifest.json", plan_for_disk)

    tasks = tasks_by_id()
    rows: list[dict[str, Any]] = []
    journal_path = output_dir / "cell_journal.jsonl"
    fatal_stop: str | None = None
    run_started = time.monotonic()
    skipped = 0
    generated = 0
    transient_resumes: list[str] = []

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
            rows.append(existing)
            skipped += 1
            continue

        if cell_dir.exists() and (cell_dir / "raw_response.txt").exists() and not _cell_complete(cell_dir):
            # Incomplete with existing raw: finish eval without model call
            raw = (cell_dir / "raw_response.txt").read_text(encoding="utf-8")
            if not raw.strip():
                raise RuntimeError(
                    f"BLOCKED_WITH_EXACT_REASON: cannot determine valid raw for {cell['cell_id']}"
                )
            partial_resume = True
            metadata = {"resume_from_existing_raw": True, "model": MODEL_ID, "seed": seed}
            api_attempts = [{"attempt": 0, "status": "identity_resume_raw", "retryable": False}]
        else:
            partial_resume = False
            raw = ""
            metadata = {}
            api_attempts = []

        cell_dir.mkdir(parents=True, exist_ok=True)
        _atomic_write_text(cell_dir / "prompt.txt", prompt)

        started = time.monotonic()
        code = None
        exception_type = exception_message = trace = None
        completion = "INFRASTRUCTURE_FAILURE"
        adoption: Any = "NOT_APPLICABLE"
        evaluator = "NOT_RUN"
        details: dict[str, Any] = {}
        failure_category = "none"
        validity: str | None = None
        timestamp = datetime.now(timezone.utc).isoformat()

        try:
            if not partial_resume:
                response = call_gemini_with_transient_policy(prompt, cell_id=cell["cell_id"])
                raw = response["raw_text"]
                metadata = dict(response.get("metadata") or {})
                api_attempts = list(response.get("api_attempts") or [])
                generated += 1
                if any(a.get("transient_failure_retry") for a in api_attempts if a.get("status") == "success"):
                    transient_resumes.append(cell["cell_id"])
                _atomic_write_text(cell_dir / "raw_response.txt", raw)

            task = tasks[cell["task_id"]]
            outcome, evaluated_code, details = classify_math16_response(
                raw,
                frozen_params=cell["frozen_parameters"],
                audit_oracle_payload=cell["audit_oracle_payload"],
                task=task,
            )
            code = evaluated_code
            completion = "NATURAL_COMPLETE" if code else outcome.upper()
            mapping = {
                "passed": "PASSED",
                "answer_incorrect": "ANSWER_INCORRECT",
                "runtime_failure": "EXECUTION_FAILURE",
                "infrastructure_failure": "EXECUTION_FAILURE",
                "schema_failure": "SCHEMA_FAILURE",
                "structural_mismatch": "STRUCTURAL_MISMATCH",
                "latex_mismatch": "LATEX_MISMATCH",
            }
            evaluator = mapping.get(outcome, outcome.upper())
            adoption = _adoption_status(
                code, cell["task_id"], cell["frozen_parameters"], cell["condition"]
            )
            failure_category = "none" if evaluator == "PASSED" else (
                "answer_incorrect" if evaluator == "ANSWER_INCORRECT" else outcome
            )
        except BaseException as exc:  # noqa: BLE001
            exception_type, exception_message = type(exc).__name__, str(exc)
            trace = traceback.format_exc()
            failure_category = "transport_or_infrastructure_failure"
            evaluator = "INFRASTRUCTURE_FAILURE"
            validity = "INVALID_INFRASTRUCTURE"
            if "API unstable" in str(exc):
                fatal_stop = str(exc)
            else:
                fatal_stop = f"UNEXPECTED_STOP at {cell['cell_id']}: {exception_type}: {exc}"

        wall = time.monotonic() - started
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
                "pipeline_correction": {"applied": False, "note": "pipeline correction disabled"},
                "healer": {
                    "enabled": False,
                    "attempted": False,
                    "outcome": "NOT_RUN",
                    "note": "healer=0; H0 has no repaired source",
                    "eligibility": failure_layer.get("eligibility"),
                    "healer_eligible": failure_layer.get("healer_eligible"),
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
                    "healer": 0,
                    "model_calls": sum(1 for a in api_attempts if a.get("status") == "success"),
                    "api_attempt_count": len(api_attempts),
                    "identity_skip": False,
                    "partial_resume_no_model_call": partial_resume,
                    "generation_label": "repeated generations under fixed nominal seeds",
                },
                "effective_generation_settings": {
                    "temperature": TEMPERATURE,
                    "top_p": "not_explicitly_set",
                    "top_k": "not_explicitly_set",
                    "max_output_tokens": MAX_OUTPUT_TOKENS,
                    "requested_seed": seed,
                    "provider_seed_support": "not_passed_to_api",
                    "model": MODEL_ID,
                },
                "done_reason": metadata.get("finish_reason") or metadata.get("done_reason"),
                "timestamp_utc": timestamp,
                "requested_model_name": MODEL_ID,
                "actual_model_version": metadata.get("model_version") or metadata.get("model"),
                "provider_metadata": {
                    "sdk": metadata.get("sdk") or service_meta.get("runtime_version"),
                    "runtime_version": service_meta.get("runtime_version"),
                    "fingerprint": metadata.get("response_id") or metadata.get("fingerprint"),
                },
                "evaluator_provenance": {
                    "revision": "math16_latex_semantic_v2",
                    "module": "agent_tools/finals_rebuild/math16_oracles.py",
                    "via": "scripts.run_math16_latex_v1_gemini_live.classify_math16_response",
                },
                "persisted_complete": True,
                "cell_index": index,
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
                        "primary_layer": failure_layer.get("primary_layer"),
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
                "seed": seed,
                "completed_cells": len(rows),
                "planned_cells": 48,
                "skipped_identity": skipped,
                "generated_this_invocation": generated,
                "last_cell_id": artifact["cell_id"],
                "fatal_stop": fatal_stop,
                "transient_resumes": transient_resumes,
            },
        )
        if fatal_stop:
            break

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
    summary["transient_resumes"] = transient_resumes
    summary["block_validation"] = validate_block(output_dir, seed=seed)
    _write_json(output_dir / "summary.json", summary)
    if fatal_stop:
        _write_json(
            output_dir / "breakpoint.json",
            {
                "fatal_stop": fatal_stop,
                "completed_cells": len(all_rows),
                "instruction": "Do not clear completed cells; resume with --resume.",
            },
        )
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", required=True, type=int, choices=list(ALLOWED_SEEDS))
    parser.add_argument("--resume", action="store_true", default=True)
    parser.add_argument("--no-resume", action="store_true")
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    output_dir = _seed_dir(args.seed)
    if args.validate_only:
        report = validate_block(output_dir, seed=args.seed)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if report["ok"] else 1
    summary = run_block(args.seed, resume=not args.no_resume)
    print(
        json.dumps(
            {
                "output_dir": str(output_dir),
                "complete_48": summary.get("complete_48"),
                "block_validation": summary.get("block_validation"),
                "identity_skipped": summary.get("identity_skipped"),
                "generated_this_invocation": summary.get("generated_this_invocation"),
                "transient_resumes": summary.get("transient_resumes"),
                "fatal_stop": summary.get("fatal_stop"),
                "failure_layer_distribution": summary.get("failure_layer_distribution"),
                "wall_clock_seconds": summary.get("wall_clock_seconds"),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    ok = bool(summary.get("complete_48") and summary.get("block_validation", {}).get("ok"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
