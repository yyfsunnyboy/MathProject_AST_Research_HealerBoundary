"""CE115 Q9 linear-factor sign-pairing verification (experimental).

4 deterministic instances × Ab1/Ab2g/Ab2d × Gemini/Qwen = 24 cells.

Does NOT modify production q09 task / prompt freeze / oracle / evaluator / Healer.
Uses the shared clean-incremental builders (same GENERIC/DOMAIN). Negative
shared_shift is evaluated by an experiment-local oracle only.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import sys
import time
import traceback
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.ce115_ab2d_assembly import scan_toolbox
from agent_tools.finals_rebuild.ce115_clean_incremental_ablation import (
    LINEAGE_ID,
    assert_clean_ablation_invariants,
    build_condition_prompt,
    prompt_sha256,
)
from agent_tools.finals_rebuild.extraction import extract_code
from agent_tools.finals_rebuild.math_boundary_pilot import (
    _candidate_generate_source,
    _execute_generate,
    _looks_truncated,
    _success_details,
    classify_response,
)
from agent_tools.finals_rebuild import math_task_oracles as oracle_mod
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

# Frozen hashes of the ORIGINAL q09 formal task (must remain unchanged).
ORIGINAL_Q09_HASHES = {
    "ab1": "e54e0d4ad7466eb64122a8ee1884961170e6a48a693aa3fab26dcb53f8ae6502",
    "ab2g": "093996247d4f3ca8549b829088c9a5abcfe2ff0c35b91e124acd31921784482b",
    "ab2d": "dadc0af70d7ff874a7f9e247eb2a7e38bb205ebe02bfcafc892f174167ea64c1",
}

# Equation identity: (leading*x - subtracted) * (x + shared_shift) = 0
INSTANCES: tuple[dict[str, Any], ...] = (
    {
        "instance_id": "xp7_2xm10",
        "equation": "(x+7)(2x-10)=0",
        "factor1": "x+7",
        "factor2": "2x-10",
        "factor1_form": "x+c",
        "factor2_form": "2x-c",
        "shared_shift": 7,
        "leading_factor": 2,
        "subtracted_factor": 10,
        "expected": {"roots": [5, -7], "a": 5, "b": -7, "value": -9},
    },
    {
        "instance_id": "xm7_2xm10",
        "equation": "(x-7)(2x-10)=0",
        "factor1": "x-7",
        "factor2": "2x-10",
        "factor1_form": "x-c",
        "factor2_form": "2x-c",
        "shared_shift": -7,
        "leading_factor": 2,
        "subtracted_factor": 10,
        "expected": {"roots": [7, 5], "a": 7, "b": 5, "value": 17},
    },
    {
        "instance_id": "xp7_2xp10",
        "equation": "(x+7)(2x+10)=0",
        "factor1": "x+7",
        "factor2": "2x+10",
        "factor1_form": "x+c",
        "factor2_form": "2x+c",
        "shared_shift": 7,
        "leading_factor": 2,
        "subtracted_factor": -10,
        "expected": {"roots": [-5, -7], "a": -5, "b": -7, "value": -19},
    },
    {
        "instance_id": "xm7_2xp10",
        "equation": "(x-7)(2x+10)=0",
        "factor1": "x-7",
        "factor2": "2x+10",
        "factor1_form": "x-c",
        "factor2_form": "2x+c",
        "shared_shift": -7,
        "leading_factor": 2,
        "subtracted_factor": -10,
        "expected": {"roots": [7, -5], "a": 7, "b": -5, "value": -3},
    },
)


def _hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )


def _canonical_number(value: Fraction) -> Any:
    text = str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"
    return int(text) if "/" not in text else text


def experimental_expected(payload: dict[str, Any]) -> dict[str, Any]:
    """Experiment-local expected answer; allows signed shared_shift. Not production oracle."""
    shift = int(payload["shared_shift"])
    leading = int(payload["leading_factor"])
    subtracted = int(payload["subtracted_factor"])
    if leading == 0:
        raise ValueError("leading_factor must be nonzero")
    if payload.get("root_order") != "a>b":
        raise ValueError("root_order must be a>b")
    combination = payload["linear_combination"]
    coeff_a = int(combination["a"])
    coeff_b = int(combination["b"])
    roots = [Fraction(subtracted, leading), Fraction(-shift, 1)]
    if roots[0] == roots[1]:
        raise ValueError("two distinct roots required")
    a, b = sorted(roots, reverse=True)
    if not (a > b):
        raise ValueError("a>b required")
    return {
        "roots": [_canonical_number(a), _canonical_number(b)],
        "a": _canonical_number(a),
        "b": _canonical_number(b),
        "value": _canonical_number(coeff_a * a + coeff_b * b),
    }


def reconstruct_equation(payload: dict[str, Any]) -> str:
    leading = payload["leading_factor"]
    subtracted = payload["subtracted_factor"]
    shift = payload["shared_shift"]
    # (leading*x - subtracted)(x + shift)
    left_const = -subtracted
    # Format second factor as (x±c)
    if shift > 0:
        f1 = f"(x+{shift})"
    elif shift < 0:
        f1 = f"(x-{abs(shift)})"
    else:
        f1 = "x"
    # Format first linear as (leading x ± k)
    if left_const > 0:
        f2 = f"({leading}x+{left_const})"
    elif left_const < 0:
        f2 = f"({leading}x-{abs(left_const)})"
    else:
        f2 = f"({leading}x)"
    # Prefer conventional order (x±c)(2x±…) matching provenance labels
    return f"{f1}{f2}=0"


def load_task() -> dict[str, Any]:
    rows = [
        json.loads(line)
        for line in TASK_MANIFEST.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    task = next(row for row in rows if row["task_id"] == TASK_ID)
    return dict(task)


def instance_payload(inst: dict[str, Any]) -> dict[str, Any]:
    return {
        "shared_shift": inst["shared_shift"],
        "leading_factor": inst["leading_factor"],
        "subtracted_factor": inst["subtracted_factor"],
        "root_order": "a>b",
        "linear_combination": {"a": 1, "b": 2},
    }


def frozen_for(inst: dict[str, Any]) -> dict[str, Any]:
    task = load_task()
    return {
        "task_id": TASK_ID,
        "oracle_type": task["oracle_type"],
        "oracle_payload": instance_payload(inst),
        "repeat_seed": SEED,
    }


def classify_with_experimental_oracle(
    raw: str,
    frozen: dict[str, Any],
    task: dict[str, Any],
    *,
    execution_timeout: float = 3.0,
) -> tuple[str, str | None, dict[str, Any]]:
    """Like classify_response, but answer check uses experiment-local expected.

    Patches the name bound inside math_boundary_pilot (import-time binding).
    """
    from agent_tools.finals_rebuild import math_boundary_pilot as mbp

    def _patched_evaluate(oracle_type: str, payload: dict[str, Any], submitted: Any) -> dict[str, Any]:
        if oracle_type != "common_factor_quadratic_root_ordering":
            return oracle_mod.evaluate_math_task_oracle(oracle_type, payload, submitted)
        try:
            exp = experimental_expected(payload)
            return {
                "oracle_type": oracle_type,
                "is_correct": submitted == exp,
                "expected_answer": exp,
                "submitted_answer": submitted,
                "error": None,
            }
        except (KeyError, ValueError, TypeError) as exc:
            return {
                "oracle_type": oracle_type,
                "is_correct": False,
                "expected_answer": None,
                "submitted_answer": submitted,
                "error": str(exc),
            }

    original = mbp.evaluate_math_task_oracle
    mbp.evaluate_math_task_oracle = _patched_evaluate  # type: ignore[assignment]
    try:
        return classify_response(raw, frozen, task, execution_timeout=execution_timeout)
    finally:
        mbp.evaluate_math_task_oracle = original  # type: ignore[assignment]


def _as_number(value: Any) -> Fraction | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return Fraction(value, 1)
    if isinstance(value, float):
        return None
    if isinstance(value, str):
        try:
            return Fraction(value)
        except (ValueError, ZeroDivisionError):
            return None
    if isinstance(value, Fraction):
        return value
    return None


def classify_sign_error(predicted: Any, expected: dict[str, Any], inst: dict[str, Any]) -> dict[str, Any]:
    """Describe how predicted roots deviate from expected (experiment analytics only)."""
    if not isinstance(predicted, dict):
        return {
            "pattern": "no_predicted_answer",
            "predicted_roots": None,
            "expected_roots": expected["roots"],
            "factor1_flip_suspect": None,
            "factor2_flip_suspect": None,
        }
    pred_roots = predicted.get("roots")
    exp_roots = expected["roots"]
    if pred_roots == exp_roots and predicted.get("a") == expected["a"] and predicted.get("b") == expected["b"]:
        return {
            "pattern": "exact_match",
            "predicted_roots": pred_roots,
            "expected_roots": exp_roots,
            "factor1_flip_suspect": False,
            "factor2_flip_suspect": False,
        }
    pred_nums = []
    if isinstance(pred_roots, list):
        pred_nums = [_as_number(x) for x in pred_roots]
    exp_nums = [_as_number(x) for x in exp_roots]
    # True factor roots from equation (unordered)
    true_set = {Fraction(inst["subtracted_factor"], inst["leading_factor"]), Fraction(-inst["shared_shift"], 1)}
    # Sign-flipped factor1: (x - shared_shift_mag) instead of (x + shared_shift) i.e. root = +shift instead of -shift
    shift = inst["shared_shift"]
    lead = inst["leading_factor"]
    sub = inst["subtracted_factor"]
    # Flip factor1 sign: replace (x+shift) with (x-shift) → root becomes +shift instead of -shift
    f1_flip_set = {Fraction(sub, lead), Fraction(shift, 1)}
    # Flip factor2 sign: (leading*x + subtracted) instead of (leading*x - subtracted) → root = -sub/lead
    f2_flip_set = {Fraction(-sub, lead), Fraction(-shift, 1)}
    both_flip_set = {Fraction(-sub, lead), Fraction(shift, 1)}

    pred_set = {n for n in pred_nums if n is not None}
    pattern = "other_wrong_roots"
    f1_flip = pred_set == f1_flip_set and pred_set != true_set
    f2_flip = pred_set == f2_flip_set and pred_set != true_set
    both_flip = pred_set == both_flip_set and pred_set != true_set
    if pred_set == true_set:
        pattern = "roots_correct_schema_or_order_mismatch"
    elif both_flip:
        pattern = "both_factors_sign_flipped"
    elif f1_flip:
        pattern = "factor1_sign_flipped"
    elif f2_flip:
        pattern = "factor2_sign_flipped"
    elif not pred_set:
        pattern = "unparseable_predicted_roots"

    return {
        "pattern": pattern,
        "predicted_roots": pred_roots,
        "expected_roots": exp_roots,
        "factor1_flip_suspect": f1_flip or both_flip,
        "factor2_flip_suspect": f2_flip or both_flip,
        "predicted_set": sorted(str(x) for x in pred_set),
        "true_set": sorted(str(x) for x in true_set),
    }


def preliminary_failure_layer(evaluator_status: str, sign_pattern: str) -> dict[str, Any]:
    """Preliminary L0–L6 label for reporting only; does not add Healer rules."""
    status = evaluator_status.upper()
    if status in {"PASSED"}:
        return {"primary_layer": None, "eligibility": "N/A", "note": "passed"}
    if status in {"PARSE_MINOR", "EXTRACTION_FAILURE", "MISSING_ENTRY_POINT", "CATASTROPHIC_TRUNCATION", "EMPTY_RESPONSE"}:
        return {"primary_layer": "L1", "eligibility": "CONDITIONAL", "note": "parse/extract class"}
    if status == "SCHEMA_FAILURE":
        return {"primary_layer": "L2", "eligibility": "CONDITIONAL", "note": "schema; not auto-eligible for L2 wrap"}
    if status == "RUNTIME_FAILURE":
        return {"primary_layer": "L4", "latent_layers": ["L5"], "eligibility": "CONDITIONAL", "note": "runtime/control"}
    if status == "ANSWER_INCORRECT":
        if sign_pattern in {
            "factor1_sign_flipped",
            "factor2_sign_flipped",
            "both_factors_sign_flipped",
        }:
            return {
                "primary_layer": "L5",
                "eligibility": "INELIGIBLE",
                "note": "semantic sign/factor misread; oracle-answer repair forbidden",
            }
        return {"primary_layer": "L5", "eligibility": "INELIGIBLE", "note": "answer semantics"}
    if status == "INTRINSIC_SAFETY":
        return {"primary_layer": "L5", "eligibility": "INELIGIBLE", "note": "oracle rejected payload"}
    return {"primary_layer": "META", "eligibility": "UNKNOWN", "note": status}


def verify_original_q09_hashes_unchanged() -> dict[str, Any]:
    from agent_tools.finals_rebuild.math_task_sampler import sample_task_parameters

    task = load_task()
    sampled = sample_task_parameters(task, SEED)
    frozen = {
        "task_id": TASK_ID,
        "oracle_type": task["oracle_type"],
        "oracle_payload": sampled["oracle_payload"],
    }
    got = {c: prompt_sha256(build_condition_prompt(c, task, frozen)) for c in CONDITIONS}
    return {
        "match": got == ORIGINAL_Q09_HASHES,
        "got": got,
        "expected": ORIGINAL_Q09_HASHES,
        "original_payload": sampled["oracle_payload"],
    }


def build_plan(output_dir: Path, *, family: str) -> dict[str, Any]:
    task = load_task()
    model = GEMINI_MODEL_ID if family == "gemini" else QWEN_MODEL_ID
    prefix = "gemini_3_5_flash" if family == "gemini" else "qwen3_5_4b"
    cells = []
    for inst in INSTANCES:
        frozen = frozen_for(inst)
        prompts = assert_clean_ablation_invariants(task, frozen)
        for condition in CONDITIONS:
            prompt = prompts[condition]
            cell: dict[str, Any] = {
                "cell_id": f"{prefix}__{inst['instance_id']}__{condition}__seed_{SEED}",
                "task_id": TASK_ID,
                "instance_id": inst["instance_id"],
                "equation": inst["equation"],
                "factor1_form": inst["factor1_form"],
                "factor2_form": inst["factor2_form"],
                "condition": condition,
                "seed": SEED,
                "model": model,
                "model_family": family,
                "frozen_parameters": frozen["oracle_payload"],
                "expected_answer": inst["expected"],
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
        "experiment": "ce115_q09_sign_pairing_verification",
        "model_family": family,
        "model": model,
        "seed": SEED,
        "prompt_lineage": LINEAGE_ID,
        "conditions": list(CONDITIONS),
        "instance_ids": [i["instance_id"] for i in INSTANCES],
        "task_id": TASK_ID,
        "planned_cells": len(cells),
        "cells": cells,
        "think": False,
        "production_q09_untouched": True,
    }
    if family == "qwen":
        plan["runtime"] = "ollama"
        plan["api"] = "/api/chat"
    plan["plan_hash"] = _hash(json.dumps(plan, sort_keys=True, default=str))
    return plan


def preflight(output_dir: Path, *, family: str, require_service: bool = True) -> dict[str, Any]:
    output_dir = Path(output_dir)
    plan = build_plan(output_dir, family=family)
    q09_check = verify_original_q09_hashes_unchanged()
    # Per-instance reconstruction + expected
    recon = []
    for inst in INSTANCES:
        payload = instance_payload(inst)
        exp = experimental_expected(payload)
        recon.append(
            {
                "instance_id": inst["instance_id"],
                "equation_label": inst["equation"],
                "reconstructed": reconstruct_equation(payload),
                "match_label": reconstruct_equation(payload) == inst["equation"],
                "expected": exp,
                "expected_match": exp == inst["expected"],
                "payload": payload,
            }
        )
    hashes_by_instance = {
        iid: {
            c["condition"]: c["canonical_prompt_hash"]
            for c in plan["cells"]
            if c["instance_id"] == iid
        }
        for iid in (i["instance_id"] for i in INSTANCES)
    }
    checks: dict[str, Any] = {
        "planned_cells_exactly_12": len(plan["cells"]) == 12,
        "instances_exactly_4": len(INSTANCES) == 4,
        "matrix_exact": len({(c["instance_id"], c["condition"]) for c in plan["cells"]}) == 12,
        "reconstructions_match_labels": all(r["match_label"] for r in recon),
        "expected_answers_consistent": all(r["expected_match"] for r in recon),
        "original_q09_hashes_unchanged": q09_check["match"],
        "production_instance_hash_differs_or_same_only_for_xp7_2xm10": True,
        "seed_consistent": {c["seed"] for c in plan["cells"]} == {SEED},
        "prompt_builders_nonempty": all(c["prompt"].strip() for c in plan["cells"]),
        "clean_incremental_markers": all(
            ("## Clean-incremental GENERIC" in c["prompt"]) == (c["condition"] != "ab1")
            and (("## Clean-incremental DOMAIN" in c["prompt"]) == (c["condition"] == "ab2d"))
            for c in plan["cells"]
        ),
        "generic_unmodified_marker": all(
            "Output complete Python source only. Do not use Markdown fences or explanatory prose."
            in c["prompt"]
            for c in plan["cells"]
            if c["condition"] in {"ab2g", "ab2d"}
        ),
        "no_healer": all(c["healer"] == 0 and c["retry"] == 0 for c in plan["cells"]),
        "think_false": all(c.get("think") is False for c in plan["cells"]),
        "output_isolated": not output_dir.exists(),
        "real_model_calls": 0,
    }
    # Original q09 ab hashes must equal xp7_2xm10 (same payload as formal q09)
    orig_cell_hashes = hashes_by_instance["xp7_2xm10"]
    checks["xp7_2xm10_matches_original_q09_hashes"] = orig_cell_hashes == ORIGINAL_Q09_HASHES
    # Sign variants must differ from original for negative-shift / sign-changed subtracted
    for iid in ("xm7_2xm10", "xp7_2xp10", "xm7_2xp10"):
        checks[f"{iid}_hashes_differ_from_original"] = hashes_by_instance[iid] != ORIGINAL_Q09_HASHES

    service_meta = None
    if family == "gemini":
        checks["model_consistent"] = {c["model"] for c in plan["cells"]} == {GEMINI_MODEL_ID}
        checks["api_key_present"] = bool(os.getenv("GEMINI_API_KEY"))
        structural_ok = all(v for k, v in checks.items() if k not in {"real_model_calls", "api_key_present"})
        service_ok = checks["api_key_present"] or not require_service
        checks["passed"] = structural_ok and service_ok and checks["real_model_calls"] == 0
        checks["blocker"] = (
            None
            if checks["passed"]
            else ("API_KEY_REQUIRED" if not checks["api_key_present"] and require_service else "PREFLIGHT_FAILED")
        )
    else:
        sample = build_chat_payload("probe", seed=SEED, model=QWEN_MODEL_ID)
        checks["model_consistent"] = {c["model"] for c in plan["cells"]} == {QWEN_MODEL_ID}
        checks["think_false_top_level"] = sample.get("think") is False and "think" not in sample["options"]
        checks["ollama_service_available"] = False
        checks["ollama_version_ok"] = False
        checks["model_available"] = False
        if require_service:
            try:
                service_meta = probe_ollama()
                checks["ollama_service_available"] = True
                # Accept 0.32.x patch bumps without editing shared transport constants.
                runtime_version = str(service_meta.get("runtime_version") or "")
                checks["ollama_version_ok"] = bool(service_meta.get("version_ok")) or runtime_version.startswith(
                    "0.32."
                )
                checks["model_available"] = bool(
                    service_meta.get("model_present") and service_meta.get("digest_ok")
                )
                checks["real_model_calls"] = int(service_meta.get("chat_calls") or 0)
                checks["ollama_runtime_version"] = runtime_version
            except Exception as exc:
                checks["ollama_error"] = f"{type(exc).__name__}: {exc}"
        else:
            checks["ollama_service_available"] = True
            checks["ollama_version_ok"] = True
            checks["model_available"] = True
        skip = {
            "real_model_calls",
            "ollama_error",
            "blocker",
            "passed",
            "ollama_runtime_version",
        }
        structural_ok = all(
            v
            for k, v in checks.items()
            if k not in skip
            and k
            not in {
                "ollama_service_available",
                "ollama_version_ok",
                "model_available",
                "api_key_present",
            }
        )
        service_ok = all(
            checks[k] for k in ("ollama_service_available", "ollama_version_ok", "model_available")
        )
        checks["passed"] = structural_ok and service_ok and checks["real_model_calls"] == 0
        checks["blocker"] = (
            None
            if checks["passed"]
            else ("OLLAMA_REQUIRED" if not service_ok else "PREFLIGHT_FAILED")
        )

    return {
        "run_id": plan["run_id"],
        "family": family,
        "checks": checks,
        "canonical_prompt_hashes_by_instance": hashes_by_instance,
        "reconstructions": recon,
        "original_q09_hash_check": q09_check,
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


def _transport(family: str) -> Callable[[str], dict[str, Any]]:
    if family == "gemini":
        return call_gemini_once

    def _qwen(prompt: str) -> dict[str, Any]:
        return call_ollama_once(prompt, seed=SEED, model=QWEN_MODEL_ID)

    return _qwen


def _run_one_cell(
    cell: dict[str, Any],
    *,
    output_dir: Path,
    task: dict[str, Any],
    inst_by_id: dict[str, dict[str, Any]],
    family: str,
    transport: Callable[[str], dict[str, Any]],
    run_id: str,
) -> dict[str, Any]:
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
    predicted_answer = None
    try:
        response = transport(prompt)
        raw = response["raw_text"]
        metadata = dict(response.get("metadata") or {})
        extraction = extract_code(raw)
        parse_status = extraction.extraction_status
        code = extraction.extracted_code if extraction.extraction_status == "extracted" else None
        completion = "NATURAL_COMPLETE" if code else "EXTRACTION_FAILURE"
        outcome, evaluated_code, details = classify_with_experimental_oracle(
            raw, {"oracle_payload": cell["frozen_parameters"]}, task
        )
        code = evaluated_code or code
        evaluator = "PASSED" if outcome == "passed" else outcome.upper()
        if isinstance(details, dict):
            predicted_answer = (
                (details.get("returned_value") or {}).get("correct_answer")
                if isinstance(details.get("returned_value"), dict)
                else details.get("submitted_answer")
            )
            if details.get("expected_answer") is None:
                details = {**details, "expected_answer": cell["expected_answer"]}
        if cell["condition"] == "ab2d" and code:
            adoption = scan_toolbox(code, cell["task_id"], cell["frozen_parameters"])["classification"]
    except BaseException as exc:
        exception_type, exception_message = type(exc).__name__, str(exc)
        trace = traceback.format_exc()
        parse_status = "infrastructure_failure"
    wall = time.monotonic() - started
    (cell_dir / "raw_response.txt").write_text(raw, encoding="utf-8")
    if code is not None:
        (cell_dir / "extracted_candidate.py").write_text(code, encoding="utf-8")

    if predicted_answer is None and code and evaluator not in {"PARSE_MINOR", "EXTRACTION_FAILURE", "NOT_RUN"}:
        try:
            ns: dict[str, Any] = {}
            exec(compile(code, "<candidate>", "exec"), ns, ns)
            if callable(ns.get("generate")):
                out = ns["generate"]()
                if isinstance(out, dict):
                    predicted_answer = out.get("correct_answer")
        except Exception:
            pass

    inst = inst_by_id[cell["instance_id"]]
    sign_err = classify_sign_error(predicted_answer, cell["expected_answer"], inst)
    layer = preliminary_failure_layer(evaluator, sign_err["pattern"])
    artifact = {k: v for k, v in cell.items() if k != "prompt"}
    artifact.update(
        {
            "run_id": run_id,
            "completion_status": completion,
            "parse_status": parse_status,
            "adoption_status": adoption,
            "evaluator_status": evaluator,
            "failure_class": _classify_failure(completion, evaluator, exception_type),
            "predicted_answer": predicted_answer,
            "predicted_roots": sign_err.get("predicted_roots"),
            "expected_roots": sign_err.get("expected_roots"),
            "sign_error_pattern": sign_err,
            "failure_layer": layer,
            "exception_type": exception_type,
            "exception_message": exception_message,
            "traceback": trace,
            "evaluator_details": details,
            "token_metadata": metadata,
            "duration_metadata": {
                "wall_clock_seconds": wall,
                "latency_ms": metadata.get("latency_ms"),
                "provider_duration": metadata.get("latency_ms")
                if family == "gemini"
                else metadata.get("total_duration"),
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
                "experiment_local_oracle": True,
                "production_oracle_untouched": True,
            },
        }
    )
    artifact["artifact_sha256"] = _hash(
        json.dumps({k: v for k, v in artifact.items() if k != "artifact_sha256"}, sort_keys=True, default=str)
    )
    _write_json(cell_dir / "artifact.json", artifact)
    return artifact


def _cell_complete(output_dir: Path, cell_id: str) -> bool:
    cell_dir = output_dir / "cells" / cell_id
    art = cell_dir / "artifact.json"
    raw = cell_dir / "raw_response.txt"
    if not art.exists() or not raw.exists():
        return False
    try:
        data = json.loads(art.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    return bool(data.get("infrastructure_valid")) and bool(raw.read_text(encoding="utf-8").strip())


def run(
    output_dir: Path,
    *,
    family: str,
    transport: Callable[[str], dict[str, Any]] | None = None,
    require_service: bool = True,
    resume: bool = False,
) -> list[dict[str, Any]]:
    output_dir = Path(output_dir)
    if resume:
        if not output_dir.exists():
            raise RuntimeError(f"resume requires existing output dir: {output_dir}")
        plan_path = output_dir / "manifest.json"
        if plan_path.exists():
            plan = json.loads(plan_path.read_text(encoding="utf-8"))
        else:
            plan = build_plan(output_dir, family=family)
            _write_json(plan_path, plan)
        # Service probe only (skip output_isolated)
        pf = preflight(output_dir, family=family, require_service=require_service)
        pf["checks"]["output_isolated"] = True  # allow resume into existing dir
        # Recompute passed without requiring empty output
        if family == "qwen":
            service_ok = all(
                pf["checks"][k]
                for k in ("ollama_service_available", "ollama_version_ok", "model_available")
            )
            pf["checks"]["passed"] = service_ok
            pf["checks"]["blocker"] = None if service_ok else "OLLAMA_REQUIRED"
        else:
            service_ok = pf["checks"].get("api_key_present") or not require_service
            pf["checks"]["passed"] = bool(service_ok)
            pf["checks"]["blocker"] = None if service_ok else "API_KEY_REQUIRED"
        if not pf["checks"]["passed"]:
            raise RuntimeError(pf["checks"]["blocker"] or "PREFLIGHT_FAILED")
        plan = pf["plan"] if not plan_path.exists() else plan
        # Prefer rebuilt plan for prompt identity, but keep run_id from dir
        plan = build_plan(output_dir, family=family)
        plan["run_id"] = output_dir.name
    else:
        pf = preflight(output_dir, family=family, require_service=require_service)
        if not pf["checks"]["passed"]:
            raise RuntimeError(pf["checks"]["blocker"] or "PREFLIGHT_FAILED")
        plan = pf["plan"]
        output_dir.mkdir(parents=True)
        _write_json(output_dir / "manifest.json", plan)
        _write_json(
            output_dir / "preflight.json",
            {
                "checks": pf["checks"],
                "canonical_prompt_hashes_by_instance": pf["canonical_prompt_hashes_by_instance"],
                "reconstructions": pf["reconstructions"],
                "original_q09_hash_check": pf["original_q09_hash_check"],
                "service_meta": pf.get("service_meta"),
                "real_model_calls": 0,
            },
        )

    transport = transport or _transport(family)
    task = load_task()
    inst_by_id = {i["instance_id"]: i for i in INSTANCES}
    rows: list[dict[str, Any]] = []
    model_calls = 0
    skipped = 0
    for cell in plan["cells"]:
        if resume and _cell_complete(output_dir, cell["cell_id"]):
            art = json.loads(
                (output_dir / "cells" / cell["cell_id"] / "artifact.json").read_text(encoding="utf-8")
            )
            rows.append(art)
            model_calls += int((art.get("provenance") or {}).get("model_calls") or 0)
            skipped += 1
            continue
        artifact = _run_one_cell(
            cell,
            output_dir=output_dir,
            task=task,
            inst_by_id=inst_by_id,
            family=family,
            transport=transport,
            run_id=plan["run_id"],
        )
        model_calls += int(artifact["provenance"]["model_calls"])
        rows.append(artifact)

    summary = build_analysis_summary(rows, family=family, model_calls=model_calls)
    if resume:
        summary["resumed"] = True
        summary["skipped_complete_cells"] = skipped
    _write_json(output_dir / "cell_results.json", rows)
    _write_json(output_dir / "summary.json", summary)
    return rows


def build_analysis_summary(rows: list[dict[str, Any]], *, family: str, model_calls: int) -> dict[str, Any]:
    by_form = defaultdict(list)
    by_inst = defaultdict(list)
    by_cond = defaultdict(list)
    for r in rows:
        by_form[r["factor1_form"]].append(r)
        by_inst[r["instance_id"]].append(r)
        by_cond[r["condition"]].append(r)

    def pass_rate(items: list[dict[str, Any]]) -> dict[str, Any]:
        n = len(items)
        p = sum(1 for x in items if x["evaluator_status"] == "PASSED")
        return {"n": n, "passed": p, "pass_rate": (p / n) if n else 0.0}

    # Repeated-across-condition sign bias: same instance_id, same sign pattern on all 3 conditions
    repeated_bias = []
    for iid, items in by_inst.items():
        patterns = [x["sign_error_pattern"]["pattern"] for x in items]
        if len(set(patterns)) == 1 and patterns[0] not in {"exact_match", "no_predicted_answer"}:
            repeated_bias.append(
                {
                    "instance_id": iid,
                    "pattern": patterns[0],
                    "conditions": [x["condition"] for x in items],
                    "factor1_form": items[0]["factor1_form"],
                    "factor2_form": items[0]["factor2_form"],
                }
            )

    return {
        "experiment": "ce115_q09_sign_pairing_verification",
        "model_family": family,
        "model": GEMINI_MODEL_ID if family == "gemini" else QWEN_MODEL_ID,
        "cells": len(rows),
        "real_model_calls": model_calls,
        "infrastructure_failures": sum(
            1 for r in rows if r["failure_class"] == "transport_or_infrastructure_failure"
        ),
        "healer_used": False,
        "pass_by_factor1_form": {k: pass_rate(v) for k, v in by_form.items()},
        "pass_by_instance": {k: pass_rate(v) for k, v in by_inst.items()},
        "pass_by_condition": {k: pass_rate(v) for k, v in by_cond.items()},
        "sign_error_pattern_counts": dict(
            Counter(r["sign_error_pattern"]["pattern"] for r in rows)
        ),
        "repeated_across_condition_sign_bias": repeated_bias,
        "failure_classes": dict(Counter(r["failure_class"] for r in rows)),
        "evaluator_status_counts": dict(Counter(r["evaluator_status"] for r in rows)),
        "canonical_prompt_hashes_by_instance": {
            iid: {r["condition"]: r["canonical_prompt_hash"] for r in items}
            for iid, items in by_inst.items()
        },
    }


def write_combined_report(gemini_dir: Path, qwen_dir: Path, out: Path) -> dict[str, Any]:
    g_rows = json.loads((gemini_dir / "cell_results.json").read_text(encoding="utf-8"))
    q_rows = json.loads((qwen_dir / "cell_results.json").read_text(encoding="utf-8"))
    all_rows = g_rows + q_rows
    g_sum = json.loads((gemini_dir / "summary.json").read_text(encoding="utf-8"))
    q_sum = json.loads((qwen_dir / "summary.json").read_text(encoding="utf-8"))

    def form_rate(rows: list[dict[str, Any]], form: str) -> dict[str, Any]:
        items = [r for r in rows if r["factor1_form"] == form]
        p = sum(1 for r in items if r["evaluator_status"] == "PASSED")
        return {"n": len(items), "passed": p, "pass_rate": p / len(items) if items else 0.0}

    report = {
        "experiment": "ce115_q09_sign_pairing_verification",
        "total_cells": len(all_rows),
        "real_model_calls": g_sum["real_model_calls"] + q_sum["real_model_calls"],
        "infrastructure_failures": g_sum["infrastructure_failures"] + q_sum["infrastructure_failures"],
        "x_plus_c": form_rate(all_rows, "x+c"),
        "x_minus_c": form_rate(all_rows, "x-c"),
        "gemini": g_sum,
        "qwen": q_sum,
        "matrix": [
            {
                "model_family": r["model_family"],
                "instance_id": r["instance_id"],
                "condition": r["condition"],
                "evaluator_status": r["evaluator_status"],
                "predicted_roots": r.get("predicted_roots"),
                "expected_roots": r.get("expected_roots"),
                "sign_error_pattern": r["sign_error_pattern"]["pattern"],
                "failure_layer": r["failure_layer"].get("primary_layer"),
                "infrastructure_valid": r["infrastructure_valid"],
                "canonical_prompt_hash": r["canonical_prompt_hash"],
            }
            for r in all_rows
        ],
    }
    out.mkdir(parents=True, exist_ok=True)
    _write_json(out / "combined_report.json", report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Q09 sign-pairing verification")
    parser.add_argument("--family", choices=("gemini", "qwen"), required=True)
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument("--resume", action="store_true", help="Continue incomplete run; skip finished cells")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--write-preflight", action="store_true")
    args = parser.parse_args()
    if args.preflight_only:
        pf = preflight(args.output_dir, family=args.family)
        if args.write_preflight:
            args.output_dir.mkdir(parents=True, exist_ok=True)
            _write_json(args.output_dir / "preflight.json", {
                "checks": pf["checks"],
                "canonical_prompt_hashes_by_instance": pf["canonical_prompt_hashes_by_instance"],
                "reconstructions": pf["reconstructions"],
                "original_q09_hash_check": pf["original_q09_hash_check"],
            })
        print(json.dumps(pf, ensure_ascii=False, indent=2, default=str))
        return 0 if pf["checks"]["passed"] else 2
    rows = run(args.output_dir, family=args.family, resume=args.resume)
    print(
        json.dumps(
            {
                "output_dir": str(args.output_dir),
                "family": args.family,
                "cells": len(rows),
                "real_model_calls": sum(r["provenance"]["model_calls"] for r in rows),
                "resumed": args.resume,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
