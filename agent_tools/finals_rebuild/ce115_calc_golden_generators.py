"""Deterministic golden generators for corrected CE115 calc L1 tasks.

Tests-only / infrastructure dry-run helpers. NOT treatment prompts — never assemble
these generators into Ab1/Ab2g/Ab2d model prompts.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from agent_tools.finals_rebuild.math_task_oracles import evaluate_math_task_oracle
from agent_tools.finals_rebuild.math_task_sampler import sample_task_parameters

_ROOT = Path(__file__).resolve().parents[2]
MANIFEST = _ROOT / "tests" / "finals_rebuild" / "fixtures" / "math_generation_tasks_ce115_pilot.jsonl"
GOLDEN_SEED = 2026071301

FORMAL_L1_TASK_IDS = (
    "ce115_calc_radical_simplification_l1",
    "ce115_calc_exact_rational_expression_l1",
    "ce115_calc_polynomial_division_l1",
    "ce115_calc_polynomial_factor_roots_l1",
)

# Fixed notation policy per family (no LaTeX delimiters; deterministic lint).
NOTATION_POLICY = {
    "radical_simplification": "unicode_radical_ascii_ops",
    "exact_rational_expression": "ascii_decimal_expression",
    "polynomial_division_general": "ascii_caret_polynomial",
    "polynomial_factor_roots": "ascii_caret_polynomial_equation",
}


def load_manifest_tasks() -> dict[str, dict[str, Any]]:
    rows = [json.loads(line) for line in MANIFEST.read_text(encoding="utf-8").splitlines() if line.strip()]
    return {row["task_id"]: row for row in rows}


def formal_l1_tasks() -> dict[str, dict[str, Any]]:
    by_id = load_manifest_tasks()
    missing = [task_id for task_id in FORMAL_L1_TASK_IDS if task_id not in by_id]
    if missing:
        raise ValueError(f"formal L1 tasks missing from manifest: {missing}")
    return {task_id: by_id[task_id] for task_id in FORMAL_L1_TASK_IDS}


def _poly_term(coeff: int, degree: int, variable: str = "x") -> str:
    if coeff == 0:
        return ""
    if degree == 0:
        return str(coeff)
    body = variable if degree == 1 else f"{variable}^{degree}"
    if coeff == 1:
        return body
    if coeff == -1:
        return f"-{body}"
    return f"{coeff}{body}"


def _format_polynomial(coeffs: list[int], variable: str = "x") -> str:
    degree = len(coeffs) - 1
    parts: list[str] = []
    for index, coeff in enumerate(coeffs):
        term = _poly_term(int(coeff), degree - index, variable)
        if not term:
            continue
        if not parts:
            parts.append(term)
        elif term.startswith("-"):
            parts.append(f" - {term[1:]}")
        else:
            parts.append(f" + {term}")
    return "".join(parts) or "0"


def render_question_text(task: dict[str, Any], oracle_payload: dict[str, Any]) -> str:
    """Build a non-leaking question from frozen payload only (fixed notation policy)."""
    oracle_type = task["oracle_type"]
    if oracle_type == "radical_simplification":
        radicand = oracle_payload["radicand"]
        outer = oracle_payload.get("outer_coefficient", 1)
        expression = f"√{radicand}" if outer == 1 else f"{outer}√{radicand}"
        return (
            f"Rewrite {expression} in simplest radical form a√b, "
            "where b is square-free and a is a positive integer."
        )
    if oracle_type == "exact_rational_expression":
        pieces: list[str] = []
        for index, product in enumerate(oracle_payload["products"]):
            term = f"{product['left']}×{product['right']}"
            sign = product["sign"]
            if index == 0:
                pieces.append(term if sign == 1 else f"-({term})")
            else:
                pieces.append(f" + {term}" if sign == 1 else f" − ({term})")
        return f"Evaluate the exact value of {''.join(pieces)}."
    if oracle_type == "polynomial_division_general":
        dividend = _format_polynomial(oracle_payload["dividend_coefficients"])
        divisor = _format_polynomial(oracle_payload["divisor_coefficients"])
        return (
            f"Divide ({dividend}) by ({divisor}). "
            "Report the quotient and remainder polynomials."
        )
    if oracle_type == "polynomial_factor_roots":
        poly = _format_polynomial(oracle_payload["quadratic_coefficients"])
        return (
            f"Factor the quadratic {poly} = 0 over the rationals and find both distinct roots "
            "in ascending numeric order."
        )
    raise ValueError(f"unsupported oracle_type for golden question: {oracle_type}")


def build_golden_return(task: dict[str, Any], *, seed: int = GOLDEN_SEED) -> dict[str, Any]:
    sampled = sample_task_parameters(task, seed)
    payload = sampled["oracle_payload"]
    verdict = evaluate_math_task_oracle(task["oracle_type"], payload, None)
    if verdict.get("error"):
        raise ValueError(f"oracle failed on frozen payload for {task['task_id']}: {verdict['error']}")
    return {
        "question_text": render_question_text(task, payload),
        "correct_answer": verdict["expected_answer"],
        "oracle_payload": payload,
    }


def build_golden_generate_source(task: dict[str, Any], *, seed: int = GOLDEN_SEED) -> str:
    """Emit a self-contained generate() that returns the golden triple as literals."""
    returned = build_golden_return(task, seed=seed)
    # JSON object literals for these payloads are valid Python dict/list/str/int syntax.
    literal = json.dumps(returned, ensure_ascii=False, sort_keys=True)
    return f"def generate(level=1, **kwargs):\n return {literal}\n"


def all_golden_sources(*, seed: int = GOLDEN_SEED) -> dict[str, str]:
    tasks = formal_l1_tasks()
    return {task_id: build_golden_generate_source(task, seed=seed) for task_id, task in tasks.items()}
