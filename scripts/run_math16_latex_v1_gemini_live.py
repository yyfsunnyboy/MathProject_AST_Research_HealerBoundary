"""Math16-LaTeX-v1 Gemini 48-cell live run (Ab1/Ab2g/Ab2d).

Does not modify pool/contract/oracle/prompt/evaluator/Healer freeze assets.
ITT: first valid model response is fixed; API retries stay on the same cell.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import traceback
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.ce115_ab2d_assembly import resolve_task_operations, scan_toolbox
from agent_tools.finals_rebuild.ce115_clean_incremental_ablation import (
    LINEAGE_ID,
    build_condition_prompt,
    prompt_sha256,
)
from agent_tools.finals_rebuild.extraction import extract_code
from agent_tools.finals_rebuild.generator_success import evaluate_math_notation
from agent_tools.finals_rebuild.latex_render_validation import evaluate_notation_lint
from agent_tools.finals_rebuild.math16_pool import (
    POOL_ID,
    SEED,
    frozen_for_prompt,
    load_pool_manifest,
    tasks_by_id,
)
from agent_tools.finals_rebuild.math_boundary_pilot import (
    _candidate_generate_source,
    _looks_truncated,
    _success_details,
)
from agent_tools.finals_rebuild.math16_oracles import classify_math16_oracle_failure
from agent_tools.finals_rebuild.math_task_oracles import evaluate_math_task_oracle
from scripts.ce115_v4_gemini_transport import MODEL_ID, call_gemini_once

CONDITIONS = ("ab1", "ab2g", "ab2d")
RUN_ID_DEFAULT = "gemini35flash_math16_latex_v1_ab123_run_001"
EXPECTED_HASHES = {
    "pool_identity_hash": "2ff41465d818d7e3d9b990a27ad2a1535e72c271bb04b2a37abe29cec1824636",
    "final_manifest_hash": "a4fc49b035cb6fed2d7a6946e241dc3ef36ed66f1a9fc09b3ecee5714a28a591",
    "task_freeze_hash": "349dfb2f786a4aa029453d844cac7eca07deb24a777ba1be4ef70f7002882e14",
    "manifest_file_sha256": "8f2d6b4a9bc55e2ba8d5c00b372b8421ba89463b9a0802865ff791ffce1c3b9e",
}
FREEZE_REPORT = ROOT / "docs/experiments/results/math16_latex_v1_freeze_closeout_report.json"
BACKOFF_SECONDS = (5, 20, 60)
MAX_ATTEMPTS = 3
RETRYABLE_MARKERS = (
    "timeout",
    "timed out",
    "rate limit",
    "resource_exhausted",
    "429",
    "500",
    "502",
    "503",
    "504",
    "connection reset",
    "connection aborted",
    "temporarily unavailable",
    "unavailable",
    "deadline",
)
FATAL_MARKERS = (
    "api_key",
    "authentication",
    "permission_denied",
    "invalid_argument",
    "invalid request",
    "400",
    "401",
    "403",
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


def ensure_api_key_via_dialog() -> None:
    if os.environ.get("GEMINI_API_KEY"):
        return
    try:
        import tkinter as tk
        from tkinter import simpledialog
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(f"API_KEY_REQUIRED and tkinter unavailable: {exc}") from exc
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    key = simpledialog.askstring(
        "Gemini API Key",
        "請輸入 GEMINI_API_KEY（不會寫入磁碟）：",
        show="*",
        parent=root,
    )
    root.destroy()
    if not key or not key.strip():
        raise RuntimeError("API_KEY_REQUIRED")
    os.environ["GEMINI_API_KEY"] = key.strip()


def verify_freeze_consistency() -> dict[str, Any]:
    manifest = load_pool_manifest()
    manifest_path = ROOT / "docs/experiments/manifests/math16_latex_v1_pool_manifest.json"
    file_sha = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
    got = {
        "pool_identity_hash": manifest["pool_identity_hash"],
        "final_manifest_hash": manifest["manifest_content_sha256"],
        "task_freeze_hash": manifest["task_freeze_hash"],
        "manifest_file_sha256": file_sha,
    }
    mismatches = {k: {"expected": EXPECTED_HASHES[k], "got": got[k]} for k in EXPECTED_HASHES if got[k] != EXPECTED_HASHES[k]}
    freeze = json.loads(FREEZE_REPORT.read_text(encoding="utf-8"))
    tasks = tasks_by_id()
    rows = []
    for tid in manifest["task_ids"]:
        task = tasks[tid]
        frozen = frozen_for_prompt(task)
        for condition in CONDITIONS:
            prompt = build_condition_prompt(condition, task, frozen)
            rows.append(
                {
                    "task_id": tid,
                    "condition": condition,
                    "prompt_sha256": prompt_sha256(prompt),
                }
            )
    prompt_match = rows == freeze["prompt_hashes_48"]
    return {
        "hashes_ok": not mismatches,
        "prompt_hashes_ok": prompt_match,
        "got_hashes": got,
        "mismatches": mismatches,
        "task_count": len(manifest["task_ids"]),
        "domain_ops_distribution": manifest["domain_ops_distribution"],
        "prompt_rows": rows,
        "manifest": manifest,
    }


def _execute_generate_all_ops(source: str, timeout: float = 3.0) -> tuple[str, Any, str | None]:
    """Execute generate with full domain Ops injected (Math16 Ab2d-safe; runner-local)."""
    wrapper = """import json, sys
from fractions import Fraction
source = sys.stdin.read()

def json_safe_default(obj):
    if isinstance(obj, Fraction):
        if obj.denominator == 1:
            return int(obj.numerator)
        raise TypeError(
            f"Object of type Fraction is not JSON serializable for non-integer value {obj}"
        )
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

try:
    from core.prompts.domain_function_library import FractionOps, IntegerOps, PolynomialOps, RadicalOps
    ns = {
        '__name__': '__main__',
        'FractionOps': FractionOps,
        'IntegerOps': IntegerOps,
        'PolynomialOps': PolynomialOps,
        'RadicalOps': RadicalOps,
    }
    exec(compile(source, 'candidate.py', 'exec'), ns)
    print(json.dumps({'ok': True, 'value': ns['generate']()}, ensure_ascii=False, default=json_safe_default))
except BaseException as exc:
    print(json.dumps({'ok': False, 'type': type(exc).__name__, 'message': str(exc)}))
"""
    environment = os.environ | {
        "PYTHONUTF8": "1",
        "PYTHONIOENCODING": "utf-8",
        "PYTHONPATH": os.pathsep.join(
            [str(ROOT)] + ([os.environ["PYTHONPATH"]] if os.environ.get("PYTHONPATH") else [])
        ),
    }
    proc = subprocess.Popen(
        [sys.executable, "-X", "utf8", "-c", wrapper],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=environment,
        cwd=str(ROOT),
    )
    try:
        stdout, stderr = proc.communicate(source, timeout=timeout)
    except subprocess.TimeoutExpired:
        proc.terminate()
        try:
            proc.communicate(timeout=1.0)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.communicate()
        return "runtime_failure", None, f"execution_timeout after {timeout:.3f}s"
    finally:
        if proc.poll() is None:
            proc.kill()
            proc.communicate()
    if proc.returncode:
        return "infrastructure_failure", None, stderr
    try:
        result = json.loads(stdout)
    except json.JSONDecodeError:
        return "infrastructure_failure", None, "invalid evaluator response"
    if result.get("ok"):
        return "passed", result.get("value"), None
    exc_type = result.get("type")
    exc_message = result.get("message") or ""
    error = f"{exc_type}: {exc_message}" if exc_type and exc_message else (exc_message or exc_type)
    return "runtime_failure", None, error


def classify_math16_response(
    raw: str,
    *,
    frozen_params: dict[str, Any],
    audit_oracle_payload: dict[str, Any],
    task: dict[str, Any],
    execution_timeout: float = 3.0,
) -> tuple[str, str | None, dict[str, Any]]:
    """Schema vs frozen_params; oracle vs audit payload. Does not mutate production modules."""
    frozen_view = {"oracle_payload": frozen_params}
    if not raw.strip():
        return "empty_response", None, _success_details(outcome="empty_response", raw=raw, source=None)
    if _looks_truncated(raw):
        return "catastrophic_truncation", None, _success_details(
            outcome="catastrophic_truncation", raw=raw, source=None
        )
    extracted = extract_code(raw)
    if extracted.extraction_status != "extracted" or not extracted.extracted_code:
        return "extraction_failure", extracted.extracted_code, _success_details(
            outcome="extraction_failure",
            raw=raw,
            source=extracted.extracted_code,
            detail={"extraction_status": extracted.extraction_status},
        )
    source = _candidate_generate_source(extracted.extracted_code)
    if source is None:
        return "extraction_failure", None, _success_details(
            outcome="extraction_failure",
            raw=raw,
            source=None,
            detail={"extraction_status": "no_generate_source"},
        )
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        return "parse_minor", source, _success_details(
            outcome="parse_minor", raw=raw, source=source, detail={"parse_error": str(exc)}
        )
    entries = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "generate"]
    if len(entries) != 1:
        return "missing_entry_point", source, _success_details(
            outcome="missing_entry_point",
            raw=raw,
            source=source,
            detail={"entry_point_count": len(entries)},
        )
    status, value, error = _execute_generate_all_ops(source, timeout=execution_timeout)
    if status != "passed":
        return status, source, _success_details(
            outcome=status,
            raw=raw,
            source=source,
            returned_value=None,
            frozen=frozen_view,
            detail={"runtime_error": error},
        )
    if (
        not isinstance(value, dict)
        or set(value) != {"question_text", "correct_answer", "oracle_payload"}
        or not isinstance(value.get("question_text"), str)
        or value.get("oracle_payload") != frozen_params
    ):
        return "schema_failure", source, _success_details(
            outcome="schema_failure",
            raw=raw,
            source=source,
            returned_value=value,
            frozen=frozen_view,
        )
    verdict = evaluate_math_task_oracle(
        task["oracle_type"], audit_oracle_payload, value["correct_answer"]
    )
    outcome = classify_math16_oracle_failure(verdict)
    if outcome == "passed":
        return "passed", source, _success_details(
            outcome="passed",
            raw=raw,
            source=source,
            returned_value=value,
            frozen=frozen_view,
            detail={
                "structural_ok": verdict.get("structural_ok"),
                "latex_ok": verdict.get("latex_ok"),
            },
        )
    return outcome, source, _success_details(
        outcome=outcome,
        raw=raw,
        source=source,
        returned_value=value,
        frozen=frozen_view,
        detail={
            "oracle_error": verdict.get("error"),
            "expected_answer": verdict.get("expected_answer"),
            "mismatch_reason": outcome,
            "structural_ok": verdict.get("structural_ok"),
            "latex_ok": verdict.get("latex_ok"),
        },
    )


def _is_fatal_api_error(exc: BaseException) -> bool:
    text = f"{type(exc).__name__}: {exc}".lower()
    if "api_key_required" in text:
        return True
    return any(marker in text for marker in FATAL_MARKERS) and not any(
        marker in text for marker in ("429", "rate limit", "resource_exhausted")
    )


def _is_retryable_api_error(exc: BaseException) -> bool:
    text = f"{type(exc).__name__}: {exc}".lower()
    if _is_fatal_api_error(exc):
        return False
    return any(marker in text for marker in RETRYABLE_MARKERS)


def call_gemini_with_retries(
    prompt: str,
    *,
    transport: Callable[[str], dict[str, Any]] = call_gemini_once,
) -> dict[str, Any]:
    attempts: list[dict[str, Any]] = []
    for attempt_index in range(1, MAX_ATTEMPTS + 1):
        started = time.monotonic()
        try:
            response = transport(prompt)
            wall = time.monotonic() - started
            attempts.append(
                {
                    "attempt": attempt_index,
                    "status": "success",
                    "wall_clock_seconds": wall,
                    "exception_type": None,
                    "exception_message": None,
                    "retryable": False,
                }
            )
            meta = dict(response.get("metadata") or {})
            meta["api_attempts"] = attempts
            meta["api_attempt_count"] = len(attempts)
            meta["first_valid_attempt"] = attempt_index
            return {"raw_text": response["raw_text"], "metadata": meta, "api_attempts": attempts}
        except BaseException as exc:
            wall = time.monotonic() - started
            retryable = _is_retryable_api_error(exc)
            attempts.append(
                {
                    "attempt": attempt_index,
                    "status": "error",
                    "wall_clock_seconds": wall,
                    "exception_type": type(exc).__name__,
                    "exception_message": str(exc),
                    "retryable": retryable,
                }
            )
            if _is_fatal_api_error(exc):
                raise RuntimeError(f"FATAL_API_STOP: {type(exc).__name__}: {exc}") from exc
            if not retryable or attempt_index == MAX_ATTEMPTS:
                raise RuntimeError(
                    f"API_FAILURE after {attempt_index} attempts: {type(exc).__name__}: {exc}"
                ) from exc
            time.sleep(BACKOFF_SECONDS[attempt_index - 1])
    raise RuntimeError("API_FAILURE unreachable")


def _adoption_status(code: str | None, task_id: str, frozen_params: dict[str, Any], condition: str) -> Any:
    if condition != "ab2d":
        return "NOT_APPLICABLE"
    if not code:
        return "NOT_APPLICABLE"
    try:
        resolve_task_operations(task_id, frozen_params)
    except KeyError:
        return {
            "classification": "ASSEMBLY_SCAN_UNAVAILABLE",
            "note": "task_id not in resolve_task_operations; adoption accounted separately",
        }
    return scan_toolbox(code, task_id, frozen_params)


def build_plan(output_dir: Path, consistency: dict[str, Any]) -> dict[str, Any]:
    manifest = consistency["manifest"]
    tasks = tasks_by_id()
    cells = []
    for tid in manifest["task_ids"]:
        task = tasks[tid]
        frozen = frozen_for_prompt(task)
        for condition in CONDITIONS:
            prompt = build_condition_prompt(condition, task, frozen)
            cell_id = f"gemini_3_5_flash__{tid}__{condition}__seed_{SEED}"
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
                    "seed": SEED,
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
        "run_id": output_dir.name,
        "pool_id": POOL_ID,
        "model": MODEL_ID,
        "seed": SEED,
        "prompt_lineage": LINEAGE_ID,
        "conditions": list(CONDITIONS),
        "task_ids": list(manifest["task_ids"]),
        "planned_cells": len(cells),
        "freeze_hashes": consistency["got_hashes"],
        "cells": cells,
        "itt_policy": "first_valid_model_response_fixed; api_retry_same_cell; healer=0",
        "gemini_live": True,
    }
    plan["plan_hash"] = _hash(json.dumps({k: v for k, v in plan.items() if k != "cells"}, sort_keys=True, default=str))
    return plan


def run_live(output_dir: Path, *, transport: Callable[[str], dict[str, Any]] = call_gemini_once) -> dict[str, Any]:
    output_dir = Path(output_dir)
    if output_dir.exists():
        raise RuntimeError(f"output directory already exists: {output_dir}")
    consistency = verify_freeze_consistency()
    if not consistency["hashes_ok"] or not consistency["prompt_hashes_ok"]:
        raise RuntimeError(f"FREEZE_INCONSISTENCY: {consistency['mismatches']} prompt_ok={consistency['prompt_hashes_ok']}")
    if consistency["task_count"] != 16:
        raise RuntimeError("task_count != 16")
    if consistency["domain_ops_distribution"] != {
        "PolynomialOps": 4,
        "IntegerOps": 4,
        "FractionOps": 4,
        "RadicalOps": 4,
    }:
        raise RuntimeError(f"domain distribution mismatch: {consistency['domain_ops_distribution']}")

    ensure_api_key_via_dialog()
    plan = build_plan(output_dir, consistency)
    if len(plan["cells"]) != 48:
        raise RuntimeError(f"planned cells != 48: {len(plan['cells'])}")

    output_dir.mkdir(parents=True)
    _write_json(output_dir / "preflight_freeze_check.json", {
        "hashes_ok": consistency["hashes_ok"],
        "prompt_hashes_ok": consistency["prompt_hashes_ok"],
        "got_hashes": consistency["got_hashes"],
        "domain_ops_distribution": consistency["domain_ops_distribution"],
    })
    # Strip prompt bodies from persisted plan copy after writing prompts per cell.
    plan_for_disk = dict(plan)
    plan_for_disk["cells"] = [{k: v for k, v in cell.items() if k != "prompt"} for cell in plan["cells"]]
    _write_json(output_dir / "manifest.json", plan_for_disk)

    tasks = tasks_by_id()
    rows: list[dict[str, Any]] = []
    journal_path = output_dir / "cell_journal.jsonl"
    fatal_stop: str | None = None

    for cell in plan["cells"]:
        if fatal_stop:
            break
        task = tasks[cell["task_id"]]
        cell_dir = output_dir / "cells" / cell["cell_id"]
        cell_dir.mkdir(parents=True)
        prompt = cell["prompt"]
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
        persisted = False
        try:
            response = call_gemini_with_retries(prompt, transport=transport)
            raw = response["raw_text"]
            metadata = dict(response.get("metadata") or {})
            api_attempts = list(response.get("api_attempts") or [])
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
            else:
                evaluator = outcome.upper()
            adoption = _adoption_status(code, cell["task_id"], cell["frozen_parameters"], cell["condition"])
            if evaluator == "PASSED":
                failure_category = "none"
            elif evaluator == "ANSWER_INCORRECT":
                failure_category = "answer_incorrect"
            elif evaluator == "LATEX_MISMATCH":
                failure_category = "latex_mismatch"
            elif evaluator == "STRUCTURAL_MISMATCH":
                failure_category = "structural_mismatch"
            elif evaluator == "SCHEMA_FAILURE":
                failure_category = "schema_failure"
            elif evaluator == "EXECUTION_FAILURE":
                failure_category = "execution_failure"
            elif evaluator == "INTRINSIC_SAFETY":
                failure_category = "intrinsic_safety"
            else:
                failure_category = "model_generated_failure"
        except RuntimeError as exc:
            message = str(exc)
            exception_type, exception_message = type(exc).__name__, message
            trace = traceback.format_exc()
            if message.startswith("FATAL_API_STOP"):
                fatal_stop = message
                failure_category = "fatal_api_stop"
                evaluator = "API_FATAL_STOP"
            elif message.startswith("API_FAILURE"):
                failure_category = "API_FAILURE"
                evaluator = "API_FAILURE"
                completion = "API_FAILURE"
            else:
                failure_category = "transport_or_infrastructure_failure"
                evaluator = "INFRASTRUCTURE_FAILURE"
        except BaseException as exc:
            exception_type, exception_message = type(exc).__name__, str(exc)
            trace = traceback.format_exc()
            failure_category = "transport_or_infrastructure_failure"
            evaluator = "INFRASTRUCTURE_FAILURE"

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

        artifact = {k: v for k, v in cell.items() if k != "prompt"}
        artifact.update(
            {
                "run_id": plan["run_id"],
                "completion_status": completion,
                "adoption_status": adoption,
                "evaluator_status": evaluator,
                "failure_category": failure_category,
                "failure_class": failure_category,
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
                    "eligibility": "NOT_RUN",
                    "attempted": False,
                    "outcome": "NOT_RUN",
                    "note": "healer=0 for this confirmatory live run; eligibility accounted separately",
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
                "hashes": {
                    "prompt": _hash(prompt),
                    "raw": _hash(raw),
                    "extracted_candidate": _hash(code or ""),
                },
                "provenance": {
                    "first_attempt_only": True,
                    "api_retry_same_cell": True,
                    "healer": 0,
                    "model_calls": sum(1 for a in api_attempts if a.get("status") == "success"),
                    "api_attempt_count": len(api_attempts),
                },
                "persisted_complete": True,
            }
        )
        _write_json(cell_dir / "artifact.json", artifact)
        persisted = True
        artifact["persisted_complete"] = persisted
        rows.append(artifact)
        with journal_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps({"cell_id": artifact["cell_id"], "evaluator_status": evaluator, "failure_category": failure_category}, ensure_ascii=False) + "\n")
            handle.flush()
            os.fsync(handle.fileno())

        if fatal_stop:
            break

    _write_json(output_dir / "cell_results.json", rows)
    summary = build_summary(plan, rows, fatal_stop=fatal_stop)
    _write_json(output_dir / "summary.json", summary)
    return summary


def build_summary(plan: dict[str, Any], rows: list[dict[str, Any]], *, fatal_stop: str | None) -> dict[str, Any]:
    by_treatment: dict[str, dict[str, int]] = {}
    for condition in CONDITIONS:
        subset = [r for r in rows if r["condition"] == condition]
        counter = Counter(r["evaluator_status"] for r in subset)
        by_treatment[condition] = {
            "cells": len(subset),
            "PASSED": counter.get("PASSED", 0),
            "ANSWER_INCORRECT": counter.get("ANSWER_INCORRECT", 0),
            "EXECUTION_FAILURE": counter.get("EXECUTION_FAILURE", 0),
            "SCHEMA_FAILURE": counter.get("SCHEMA_FAILURE", 0),
            "API_FAILURE": counter.get("API_FAILURE", 0),
            "other": sum(
                v
                for k, v in counter.items()
                if k
                not in {
                    "PASSED",
                    "ANSWER_INCORRECT",
                    "EXECUTION_FAILURE",
                    "SCHEMA_FAILURE",
                    "API_FAILURE",
                }
            ),
        }
    domain_treatment: dict[str, dict[str, dict[str, int]]] = defaultdict(dict)
    for domain in ("PolynomialOps", "IntegerOps", "FractionOps", "RadicalOps"):
        for condition in CONDITIONS:
            subset = [r for r in rows if r.get("domain_ops") == domain and r["condition"] == condition]
            domain_treatment[domain][condition] = dict(Counter(r["evaluator_status"] for r in subset))

    task_treatment = []
    for tid in plan["task_ids"]:
        for condition in CONDITIONS:
            matches = [r for r in rows if r["task_id"] == tid and r["condition"] == condition]
            task_treatment.append(
                {
                    "task_id": tid,
                    "condition": condition,
                    "evaluator_status": matches[0]["evaluator_status"] if matches else "MISSING",
                    "failure_category": matches[0]["failure_category"] if matches else "missing_cell",
                    "prompt_hash": matches[0]["prompt_hash"] if matches else None,
                }
            )

    special_ids = {
        "ce111_q08_polynomial_factor_parameter_recovery": "111-8",
        "ce111_q10_ordered_quadratic_roots_radical": "111-10",
        "ce112_q12_independent_probability_fraction": "112-12",
        "ce113_q11_rationalize_denominator": "113-11",
    }
    special = {
        label: [
            {
                "condition": r["condition"],
                "evaluator_status": r["evaluator_status"],
                "failure_category": r["failure_category"],
            }
            for r in rows
            if r["task_id"] == tid
        ]
        for tid, label in special_ids.items()
    }

    cell_ids = [r["cell_id"] for r in rows]
    g6_fail = sum(
        1
        for r in rows
        if isinstance(r.get("latex_g6"), dict) and r["latex_g6"].get("status") == "FAIL"
    )
    return {
        "run_id": plan["run_id"],
        "pool_id": POOL_ID,
        "planned_cells": 48,
        "attempted_cells": len(rows),
        "persisted_cells": sum(1 for r in rows if r.get("persisted_complete")),
        "valid_generation_cells": sum(
            1
            for r in rows
            if r.get("persisted_complete") and r.get("evaluator_status") not in {"API_FAILURE", "API_FATAL_STOP", "NOT_RUN"}
        ),
        "duplicate_cell_ids": [cid for cid, n in Counter(cell_ids).items() if n > 1],
        "missing_cells": 48 - len(rows),
        "complete_48": len(rows) == 48 and len(set(cell_ids)) == 48 and not fatal_stop,
        "fatal_stop": fatal_stop,
        "api_failure_count": sum(1 for r in rows if r["evaluator_status"] == "API_FAILURE"),
        "retry_attempt_total": sum(len(r.get("api_attempts") or []) for r in rows),
        "by_treatment": by_treatment,
        "domain_x_treatment": domain_treatment,
        "task_x_treatment": task_treatment,
        "special_items": special,
        "failure_categories": dict(Counter(r["failure_category"] for r in rows)),
        "healer_accounting": {
            "enabled": False,
            "first_attempt_fixed": True,
            "pipeline_correction_applied_count": 0,
            "healer_attempt_count": 0,
        },
        "latex_g6_fail_count": g6_fail,
        "freeze_hashes": plan["freeze_hashes"],
        "git_head_expected": "f7439a9a6bad70a70437b71b6afb7938dc7b90d7",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "docs/experiments/results" / RUN_ID_DEFAULT,
    )
    parser.add_argument("--preflight-only", action="store_true")
    args = parser.parse_args()
    consistency = verify_freeze_consistency()
    print(
        json.dumps(
            {
                "hashes_ok": consistency["hashes_ok"],
                "prompt_hashes_ok": consistency["prompt_hashes_ok"],
                "task_count": consistency["task_count"],
                "domain_ops_distribution": consistency["domain_ops_distribution"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    if args.preflight_only:
        return 0 if consistency["hashes_ok"] and consistency["prompt_hashes_ok"] else 2
    summary = run_live(args.output_dir)
    print(json.dumps({"output_dir": str(args.output_dir), "summary": {
        "complete_48": summary["complete_48"],
        "attempted_cells": summary["attempted_cells"],
        "api_failure_count": summary["api_failure_count"],
        "fatal_stop": summary["fatal_stop"],
        "by_treatment": summary["by_treatment"],
    }}, ensure_ascii=False, indent=2))
    return 0 if summary["complete_48"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
