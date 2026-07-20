"""Math16-LaTeX-v1 Qwen Ollama 48-cell live run (Ab1/Ab2g/Ab2d).

Mirrors scripts/run_math16_latex_v1_gemini_live.py structure; only the model
call is replaced by math16_qwen_ollama_adapter.call_qwen_with_retries.

Prompts are runtime-built exclusively via
build_condition_prompt("ab1"|"ab2g"|"ab2d", ...) from
ce115_clean_incremental_ablation — never concatenated or rewritten here.

Does not modify pool/contract/oracle/prompt/evaluator/SSOT/toolbox freeze assets.
ITT: first valid model response is fixed; API retries stay on the same cell; healer=0.
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
from collections import Counter, defaultdict
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
from agent_tools.finals_rebuild.generator_success import evaluate_math_notation
from agent_tools.finals_rebuild.git_blob_hash import sha256_git_blob_lf
from agent_tools.finals_rebuild.latex_render_validation import evaluate_notation_lint
from agent_tools.finals_rebuild.math16_pool import (
    POOL_ID,
    SEED,
    frozen_for_prompt,
    load_pool_manifest,
    tasks_by_id,
)
from scripts.math16_qwen_ollama_adapter import (
    DEFAULT_BASE_URL,
    InvalidInfrastructureError,
    call_qwen_with_retries,
    frozen_inference_config,
    probe_ollama,
)
from scripts.run_math16_latex_v1_gemini_live import (
    classify_math16_response,
)

CONDITIONS = ("ab1", "ab2g", "ab2d")
PROMPT_DIFF = (
    ROOT
    / "docs/experiments/results/domain_api_contract_hardening_v2/prompt_hash_diff_48.json"
)
FREEZE_MANIFEST = (
    ROOT
    / "docs/experiments/results/domain_api_contract_hardening_v2/ab2d_v2_freeze_manifest.json"
)
MODEL_SLUG = {
    "qwen3.5:4b": "qwen35_4b",
    "qwen3.5:9b": "qwen35_9b",
}


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
    return MODEL_SLUG.get(model, model.replace(":", "_").replace(".", "_"))


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


def preliminary_failure_layer(evaluator_status: str, *, validity: str | None = None) -> dict[str, Any]:
    """L0–L5 label for reporting only; does not execute Healer."""
    if validity == "INVALID_INFRASTRUCTURE" or evaluator_status in {
        "INFRASTRUCTURE_FAILURE",
        "API_FAILURE",
        "API_FATAL_STOP",
        "L0_INVALID_INFRASTRUCTURE",
    }:
        return {
            "primary_layer": "L0",
            "eligibility": "INELIGIBLE",
            "note": "infrastructure / transport",
            "healer_eligible": False,
        }
    status = evaluator_status.upper()
    if status == "PASSED":
        return {
            "primary_layer": None,
            "eligibility": "N/A",
            "note": "passed",
            "healer_eligible": False,
        }
    if status in {
        "PARSE_MINOR",
        "EXTRACTION_FAILURE",
        "MISSING_ENTRY_POINT",
        "CATASTROPHIC_TRUNCATION",
        "EMPTY_RESPONSE",
    }:
        return {
            "primary_layer": "L1",
            "eligibility": "CONDITIONAL",
            "note": "parse/extract class",
            "healer_eligible": True,
        }
    if status == "SCHEMA_FAILURE":
        return {
            "primary_layer": "L2",
            "eligibility": "CONDITIONAL",
            "note": "schema / payload contract",
            "healer_eligible": True,
        }
    if status in {"STRUCTURAL_MISMATCH", "LATEX_MISMATCH"}:
        return {
            "primary_layer": "L3",
            "eligibility": "CONDITIONAL",
            "note": "structure/latex contract-adjacent",
            "healer_eligible": True,
        }
    if status in {"EXECUTION_FAILURE", "RUNTIME_FAILURE"}:
        return {
            "primary_layer": "L4",
            "eligibility": "CONDITIONAL",
            "note": "runtime/control",
            "healer_eligible": True,
        }
    if status in {"ANSWER_INCORRECT", "INTRINSIC_SAFETY"}:
        return {
            "primary_layer": "L5",
            "eligibility": "INELIGIBLE",
            "note": "answer semantics / oracle reject",
            "healer_eligible": False,
        }
    return {
        "primary_layer": "META",
        "eligibility": "UNKNOWN",
        "note": status,
        "healer_eligible": False,
    }


def load_frozen_prompt_hashes() -> dict[tuple[str, str], str]:
    diff = json.loads(PROMPT_DIFF.read_text(encoding="utf-8"))
    expected: dict[tuple[str, str], str] = {}
    for section in ("changed_cells", "unchanged_cells"):
        for row in diff.get(section, []):
            tid, cond = row["task_id"], row["condition"]
            if row.get("changed"):
                expected[(tid, cond)] = row["new_prompt_hash"]
            else:
                expected[(tid, cond)] = (
                    row.get("new_prompt_hash") or row.get("old_prompt_hash") or row["prompt_hash"]
                )
    if len(expected) != 48:
        raise RuntimeError(f"frozen prompt hash table size != 48: {len(expected)}")
    return expected


def verify_prompt_hashes_unchanged() -> dict[str, Any]:
    """Runtime-build 48 prompts; require zero diffs vs prompt_hash_diff_48.json."""
    expected = load_frozen_prompt_hashes()
    tasks = tasks_by_id()
    runtime: dict[tuple[str, str], str] = {}
    changed: list[dict[str, str]] = []
    for tid, task in tasks.items():
        frozen = frozen_for_prompt(task)
        for condition in CONDITIONS:
            prompt = build_condition_prompt(condition, task, frozen)
            h = prompt_sha256(prompt)
            runtime[(tid, condition)] = h
            exp = expected[(tid, condition)]
            if h != exp:
                changed.append(
                    {
                        "task_id": tid,
                        "condition": condition,
                        "runtime": h,
                        "expected": exp,
                    }
                )
    return {
        "cells": 48,
        "changed": len(changed),
        "unchanged": 48 - len(changed),
        "mismatches": changed,
        "ok": len(changed) == 0,
    }


def verify_freeze_assets_match() -> dict[str, Any]:
    freeze = json.loads(FREEZE_MANIFEST.read_text(encoding="utf-8"))
    if freeze.get("hash_basis") != "git_blob_lf":
        raise RuntimeError(f"unexpected hash_basis: {freeze.get('hash_basis')}")
    paths = {
        "toolbox": ROOT / "core/prompts/domain_function_library.py",
        "ssot": ROOT / "agent_tools/finals_rebuild/domain_api_ssot.py",
        "skills": ROOT / "agent_skills/domain_api_contract_v2/SKILL.md",
        "task_assembly": ROOT / "agent_tools/finals_rebuild/domain_answer_assembly.py",
        "answer_contract": ROOT / "agent_tools/finals_rebuild/math_answer_contracts.py",
        "oracle_evaluator": ROOT / "agent_tools/finals_rebuild/math16_oracles.py",
        "api_inventory": ROOT
        / "docs/experiments/results/domain_api_contract_hardening_v2/api_inventory.json",
        "typed_contracts": ROOT
        / "docs/experiments/results/domain_api_contract_hardening_v2/typed_contracts.json",
        "task_assembly_artifact": ROOT
        / "docs/experiments/results/domain_api_contract_hardening_v2/task_output_assembly.json",
        "math16_pool_manifest": ROOT
        / "docs/experiments/manifests/math16_latex_v1_pool_manifest.json",
    }
    mismatches = []
    for key, path in paths.items():
        got = sha256_git_blob_lf(path, repo_root=ROOT)
        exp = freeze["component_sha256"][key]
        if got != exp:
            mismatches.append({"key": key, "got": got, "expected": exp})
    return {
        "hash_basis": freeze["hash_basis"],
        "ok": not mismatches,
        "mismatches": mismatches,
    }


def build_plan(output_dir: Path, *, model: str, service_meta: dict[str, Any]) -> dict[str, Any]:
    manifest = load_pool_manifest()
    tasks = tasks_by_id()
    prefix = _model_prefix(model)
    cells = []
    for tid in manifest["task_ids"]:
        task = tasks[tid]
        frozen = frozen_for_prompt(task)
        for condition in CONDITIONS:
            prompt = build_condition_prompt(condition, task, frozen)
            cell_id = f"{prefix}__{tid}__{condition}__seed_{SEED}"
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
                    "model": model,
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
        "model": model,
        "model_digest": service_meta.get("model_digest"),
        "runtime": "ollama",
        "runtime_version": service_meta.get("runtime_version"),
        "seed": SEED,
        "prompt_lineage": LINEAGE_ID,
        "conditions": list(CONDITIONS),
        "task_ids": list(manifest["task_ids"]),
        "planned_cells": len(cells),
        "cells": cells,
        "itt_policy": "first_valid_model_response_fixed; api_retry_same_cell; healer=0",
        "inference_config": frozen_inference_config(),
        "service_meta": service_meta,
        "qwen_live": True,
    }
    plan["plan_hash"] = _hash(
        json.dumps({k: v for k, v in plan.items() if k != "cells"}, sort_keys=True, default=str)
    )
    return plan


def build_summary(
    plan: dict[str, Any],
    rows: list[dict[str, Any]],
    *,
    fatal_stop: str | None,
    wall_clock_seconds: float,
) -> dict[str, Any]:
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
            "STRUCTURAL_MISMATCH": counter.get("STRUCTURAL_MISMATCH", 0),
            "LATEX_MISMATCH": counter.get("LATEX_MISMATCH", 0),
            "API_FAILURE": counter.get("API_FAILURE", 0),
            "L0_INVALID_INFRASTRUCTURE": counter.get("L0_INVALID_INFRASTRUCTURE", 0),
            "other": sum(
                v
                for k, v in counter.items()
                if k
                not in {
                    "PASSED",
                    "ANSWER_INCORRECT",
                    "EXECUTION_FAILURE",
                    "SCHEMA_FAILURE",
                    "STRUCTURAL_MISMATCH",
                    "LATEX_MISMATCH",
                    "API_FAILURE",
                    "L0_INVALID_INFRASTRUCTURE",
                }
            ),
        }
    cell_ids = [r["cell_id"] for r in rows]
    layer_counts = Counter(
        (r.get("failure_layer") or {}).get("primary_layer") or "PASSED" for r in rows
    )
    healer_eligible = sum(
        1 for r in rows if (r.get("failure_layer") or {}).get("healer_eligible") is True
    )
    l0 = sum(
        1
        for r in rows
        if (r.get("failure_layer") or {}).get("primary_layer") == "L0"
        or r.get("evaluator_status") == "L0_INVALID_INFRASTRUCTURE"
    )
    return {
        "run_id": plan["run_id"],
        "pool_id": POOL_ID,
        "model": plan["model"],
        "planned_cells": 48,
        "attempted_cells": len(rows),
        "executed_cells": len(rows),
        "persisted_cells": sum(1 for r in rows if r.get("persisted_complete")),
        "l0_cells": l0,
        "duplicate_cell_ids": [cid for cid, n in Counter(cell_ids).items() if n > 1],
        "missing_cells": 48 - len(rows),
        "complete_48": len(rows) == 48 and len(set(cell_ids)) == 48 and not fatal_stop,
        "json_parseable": True,
        "fatal_stop": fatal_stop,
        "wall_clock_seconds": wall_clock_seconds,
        "by_treatment": by_treatment,
        "failure_categories": dict(Counter(r["failure_category"] for r in rows)),
        "failure_layer_distribution": dict(layer_counts),
        "healer_eligible_cells": healer_eligible,
        "healer_accounting": {
            "enabled": False,
            "first_attempt_fixed": True,
            "healer_attempt_count": 0,
            "eligibility_marked_only": True,
        },
        "inference_config": plan.get("inference_config"),
    }


def run_live(output_dir: Path, *, model: str) -> dict[str, Any]:
    output_dir = Path(output_dir)
    if output_dir.exists():
        raise RuntimeError(f"output directory already exists: {output_dir}")

    prompt_check = verify_prompt_hashes_unchanged()
    if not prompt_check["ok"]:
        raise RuntimeError(
            f"PROMPT_HASH_CHANGED: changed={prompt_check['changed']} "
            f"sample={prompt_check['mismatches'][:3]}"
        )
    freeze_check = verify_freeze_assets_match()
    if not freeze_check["ok"]:
        raise RuntimeError(f"FREEZE_HASH_MISMATCH: {freeze_check['mismatches']}")

    service_meta = probe_ollama(base_url=DEFAULT_BASE_URL, model=model)
    plan = build_plan(output_dir, model=model, service_meta=service_meta)
    if len(plan["cells"]) != 48:
        raise RuntimeError(f"planned cells != 48: {len(plan['cells'])}")

    output_dir.mkdir(parents=True)
    _write_json(
        output_dir / "preflight_checks.json",
        {
            "prompt_hash_check": prompt_check,
            "freeze_hash_check": freeze_check,
            "service_meta": service_meta,
            "inference_config": frozen_inference_config(),
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

    for index, cell in enumerate(plan["cells"]):
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
        validity: str | None = None

        try:
            response = call_qwen_with_retries(
                prompt,
                seed=SEED,
                model=model,
                base_url=DEFAULT_BASE_URL,
            )
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
            # Unexpected failure: persist breakpoint and stop for human.
            fatal_stop = f"UNEXPECTED_STOP at {cell['cell_id']}: {exception_type}: {exc}"

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
                    "note": "healer=0; eligibility marked only",
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
                        "failure_category": failure_category,
                        "primary_layer": failure_layer.get("primary_layer"),
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )
            handle.flush()
            os.fsync(handle.fileno())

        # Checkpoint after every cell so mid-stop never loses progress.
        _write_json(
            output_dir / "checkpoint.json",
            {
                "run_id": plan["run_id"],
                "model": model,
                "completed_cells": len(rows),
                "planned_cells": 48,
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

    wall_total = time.monotonic() - run_started
    _write_json(output_dir / "cell_results.json", rows)
    summary = build_summary(plan, rows, fatal_stop=fatal_stop, wall_clock_seconds=wall_total)
    _write_json(output_dir / "summary.json", summary)
    if fatal_stop:
        _write_json(
            output_dir / "breakpoint.json",
            {
                "fatal_stop": fatal_stop,
                "completed_cells": len(rows),
                "last_cell_id": rows[-1]["cell_id"] if rows else None,
                "instruction": "Do not clear or rerun; await human direction.",
            },
        )
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, choices=sorted(MODEL_SLUG))
    parser.add_argument(
        "--run-id",
        default=None,
        help="Run directory name under docs/experiments/results "
        "(default: {slug}_math16_ab123_run_001).",
    )
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument("--preflight-only", action="store_true")
    args = parser.parse_args()
    model = args.model
    run_id = args.run_id or f"{MODEL_SLUG[model]}_math16_ab123_run_001"
    output_dir = args.output_dir or (ROOT / "docs/experiments/results" / run_id)

    prompt_check = verify_prompt_hashes_unchanged()
    freeze_check = verify_freeze_assets_match()
    print(
        json.dumps(
            {
                "model": model,
                "output_dir": str(output_dir),
                "prompt_hash_ok": prompt_check["ok"],
                "prompt_changed": prompt_check["changed"],
                "freeze_hash_ok": freeze_check["ok"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    if not prompt_check["ok"] or not freeze_check["ok"]:
        return 2
    if args.preflight_only:
        return 0

    summary = run_live(output_dir, model=model)
    print(
        json.dumps(
            {
                "output_dir": str(output_dir),
                "complete_48": summary["complete_48"],
                "attempted_cells": summary["attempted_cells"],
                "l0_cells": summary["l0_cells"],
                "fatal_stop": summary["fatal_stop"],
                "wall_clock_seconds": summary["wall_clock_seconds"],
                "by_treatment": summary["by_treatment"],
                "failure_layer_distribution": summary["failure_layer_distribution"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if summary["complete_48"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
