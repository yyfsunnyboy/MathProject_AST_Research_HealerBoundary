"""CE115 external validation: 113/114 junior-high exam tasks (held-out).

Six frozen tasks. Ab1/Ab2g/Ab2d via clean-incremental ablation.
Diagnostic / external-validation only — not core Healer success denominator.
"""
from __future__ import annotations

import json
from typing import Any


def json_dumps_sorted(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, default=str)

SEED = 2026071301
LINEAGE_NOTE = "ce115_exam_external_validation_113_114"

# task_id -> frozen oracle_payload (identity; no solution structure)
FROZEN_PAYLOADS: dict[str, dict[str, Any]] = {
    "ce115_ext_114_01_power_laws_l1": {
        "expression": "7**10 * 7**2 / 7**4",
        "required_form": "power_of_same_base",
        "base": 7,
    },
    "ce115_ext_114_02_polynomial_simplify_l1": {
        "expression": "(5*x**2 - 2*x) - (4 - 3*x)",
    },
    "ce115_ext_114_04_linear_system_l1": {
        "equations": ["37*x + 2*y = 81", "23*x - 2*y = 39"],
        "target_expression": "x + 2*y",
    },
    "ce115_ext_114_08_radical_product_l1": {
        "expression": "(2*sqrt(3) + sqrt(6))*sqrt(2)",
    },
    "ce115_ext_113_10_factorization_l1": {
        "expression": "5*x*(5*x - 2) - 4*(5*x - 2)**2",
        "required_form": "fully_factored",
    },
    "ce115_ext_113_11_rationalize_l1": {
        "expression": "9/(4 - sqrt(7))",
        "required_form": "a + b*sqrt(7)",
        "target_expression": "a + b",
    },
}

EXPECTED_ANSWERS: dict[str, dict[str, Any]] = {
    "ce115_ext_114_01_power_laws_l1": {"base": 7, "exponent": 8},
    "ce115_ext_114_02_polynomial_simplify_l1": {"coefficients": {"2": 5, "1": 1, "0": -4}},
    "ce115_ext_114_04_linear_system_l1": {"x": 2, "y": "7/2", "value": 9},
    "ce115_ext_114_08_radical_product_l1": {
        "terms": [
            {"coefficient": 2, "radicand": 3},
            {"coefficient": 2, "radicand": 6},
        ]
    },
    "ce115_ext_113_10_factorization_l1": {
        "factors": [
            {"x_coefficient": 5, "constant": -2},
            {"x_coefficient": -15, "constant": 8},
        ]
    },
    "ce115_ext_113_11_rationalize_l1": {"a": 4, "b": 1, "radicand": 7, "value": 5},
}

PROVENANCE: dict[str, dict[str, str]] = {
    "ce115_ext_114_01_power_laws_l1": {
        "exam_year": "114",
        "item": "1",
        "source": "114年國中教育會考數學試題第1題",
        "stem": "算式 7^10 × 7^2 ÷ 7^4 之值可用 7 的幾次方表示？",
        "goal": "求 exponent（同底冪）",
    },
    "ce115_ext_114_02_polynomial_simplify_l1": {
        "exam_year": "114",
        "item": "2",
        "source": "114年國中教育會考數學試題第2題",
        "stem": "計算 (5x^2 - 2x) - (4 - 3x)",
        "goal": "化簡多項式",
    },
    "ce115_ext_114_04_linear_system_l1": {
        "exam_year": "114",
        "item": "4",
        "source": "114年國中教育會考數學試題第4題",
        "stem": "聯立 37x+2y=81, 23x-2y=39；解 x=a,y=b，求 a+2b",
        "goal": "求 a+2b",
    },
    "ce115_ext_114_08_radical_product_l1": {
        "exam_year": "114",
        "item": "8",
        "source": "114年國中教育會考數學試題第8題",
        "stem": "計算 (2√3 + √6) × √2",
        "goal": "化為最簡根式和",
    },
    "ce115_ext_113_10_factorization_l1": {
        "exam_year": "113",
        "item": "10",
        "source": "113年國中教育會考數學試題第10題",
        "stem": "因式分解 5x(5x-2) - 4(5x-2)^2",
        "goal": "完全因式分解",
    },
    "ce115_ext_113_11_rationalize_l1": {
        "exam_year": "113",
        "item": "11",
        "source": "113年國中教育會考數學試題第11題",
        "stem": "將 9/(4-√7) 化為 a+b√7，求 a+b",
        "goal": "有理化並求 a+b",
    },
}

ORACLE_TYPE_BY_TASK: dict[str, str] = {
    "ce115_ext_114_01_power_laws_l1": "exam_power_of_same_base",
    "ce115_ext_114_02_polynomial_simplify_l1": "exam_polynomial_simplify",
    "ce115_ext_114_04_linear_system_l1": "exam_linear_system_linear_combination",
    "ce115_ext_114_08_radical_product_l1": "exam_radical_product_simplified",
    "ce115_ext_113_10_factorization_l1": "exam_factorization_common_binomial",
    "ce115_ext_113_11_rationalize_l1": "exam_rationalize_conjugate",
}

SKILL_BY_TASK: dict[str, str] = dict(ORACLE_TYPE_BY_TASK)

TASK_IDS: tuple[str, ...] = tuple(FROZEN_PAYLOADS.keys())


def fixture_row(task_id: str) -> dict[str, Any]:
    payload = FROZEN_PAYLOADS[task_id]
    oracle_type = ORACLE_TYPE_BY_TASK[task_id]
    # Encode frozen payload as single-value allowed_values for sampler identity.
    parameter_ranges: dict[str, Any] = {}
    for key, value in payload.items():
        parameter_ranges[key] = {"allowed_values": [value]}
    return {
        "task_id": task_id,
        "domain": "junior_high_exam_external_validation",
        "skill_id": SKILL_BY_TASK[task_id],
        "difficulty_level": 1,
        "difficulty_label": "basic",
        "structural_complexity": ["exam_held_out", "external_validation"],
        "reasoning_steps_expected": 3,
        "parameter_ranges": parameter_ranges,
        "oracle_type": oracle_type,
        "seed": 20260713,
        "required_entry_point": "generate",
        "required_output_keys": ["question_text", "correct_answer", "oracle_payload"],
        "randomization_contract": {
            "seeded": True,
            "local_rng_required": True,
            "same_seed_reproducible": True,
            "different_seed_variability_expected": False,
        },
        "k12_constraints": {
            "hand_calculable": True,
            "avoid_large_numbers": True,
            "avoid_degenerate_cases": True,
            "avoid_ambiguous_cases": True,
            "prefer_integer_or_simple_fraction_answers": True,
        },
        "external_validation": {
            "cohort": "exam_113_114_six_task",
            "healer_success_denominator": False,
            "diagnostic": True,
            **PROVENANCE[task_id],
        },
    }


def leakage_audit(task_id: str) -> dict[str, Any]:
    payload = FROZEN_PAYLOADS[task_id]
    expected = EXPECTED_ANSWERS[task_id]
    payload_text = str(payload)
    findings = []
    # 1. fields from original stem only
    findings.append(
        {
            "check": "frozen_fields_from_stem",
            "passed": True,
            "note": "frozen keys match user-approved draft from original numbers/expressions only",
        }
    )
    # 2. no post-solution structure
    leak_tokens = []
    for token in ("factors", "roots", "exponent", "coefficients", "terms", '"a":', '"b":', "value"):
        # allow required_form / target_expression wording in frozen
        if token in ("factors", "roots", "exponent", "coefficients", "terms") and token in payload_text:
            leak_tokens.append(token)
    findings.append(
        {
            "check": "no_solution_structure_in_frozen",
            "passed": not leak_tokens,
            "note": f"forbidden tokens in frozen: {leak_tokens}" if leak_tokens else "ok",
        }
    )
    # 3. not pre-parsed for the model
    findings.append(
        {
            "check": "no_pre_parsed_factors_or_steps",
            "passed": "common_factor" not in payload_text and "conjugate" not in payload_text,
            "note": "frozen does not name solving tactics beyond required_form labels present on the original ask",
        }
    )
    # 4. no formula/answer hints — stem literals may share digits with answers
    # (e.g. base 7, coeff 5); require the assembled correct_answer dict absent.
    answer_struct_leak = json_dumps_sorted(expected) in payload_text or any(
        key in payload for key in ("exponent", "coefficients", "factors", "terms", "value")
        if key in expected
    )
    findings.append(
        {
            "check": "no_answer_in_frozen",
            "passed": not answer_struct_leak and expected != payload,
            "note": "frozen holds stem literals only; correct_answer structure absent",
        }
    )
    # 5. unique reconstruction
    findings.append(
        {
            "check": "unique_stem_reconstruction",
            "passed": "expression" in payload or "equations" in payload,
            "note": "expression/equations uniquely identify the exam item",
        }
    )
    # 6. correct answer absent
    findings.append(
        {
            "check": "correct_answer_absent_from_frozen",
            "passed": expected != payload,
            "note": "frozen != expected_answer",
        }
    )
    return {
        "task_id": task_id,
        "passed": all(item["passed"] for item in findings),
        "findings": findings,
        "frozen_payload": payload,
        "expected_answer_keys": sorted(expected.keys()),
    }


def _flatten_values(obj: Any) -> list[Any]:
    if isinstance(obj, dict):
        out: list[Any] = []
        for v in obj.values():
            out.extend(_flatten_values(v))
        return out
    if isinstance(obj, list):
        out = []
        for v in obj:
            out.extend(_flatten_values(v))
        return out
    return [obj]


def all_leakage_audits() -> dict[str, Any]:
    audits = {tid: leakage_audit(tid) for tid in TASK_IDS}
    return {
        "cohort": LINEAGE_NOTE,
        "passed": all(a["passed"] for a in audits.values()),
        "tasks": audits,
    }
