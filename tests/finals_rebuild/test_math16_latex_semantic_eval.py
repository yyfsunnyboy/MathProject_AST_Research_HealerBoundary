"""Targeted regressions for Math16 semantic LaTeX evaluation (structure primary)."""
from __future__ import annotations

import json

# Import math_task_oracles first to avoid math16_oracles ↔ math_task_oracles circular import.
from agent_tools.finals_rebuild.math_task_oracles import evaluate_math_task_oracle
from agent_tools.finals_rebuild.math16_oracles import (
    display_latex_equivalent,
    evaluate_math16_polynomial_division_general,
    evaluate_math16_polynomial_factor_roots,
    normalize_compound_radical,
    normalize_math16_display_latex,
)


DIV_PAYLOAD = {"dividend_coefficients": [6, 0, 6], "divisor_coefficients": [1, -4]}
ROOTS_PAYLOAD = {"quadratic_coefficients": [1, 4, -12]}


def test_poly_division_spacing_equivalent_latex_passes_structurally():
    submitted = {
        "quotient_coefficients": [6, 24],
        "remainder_coefficients": [102],
        "quotient_latex": "6x + 24",
        "remainder_latex": "102",
    }
    verdict = evaluate_math16_polynomial_division_general(DIV_PAYLOAD, submitted)
    assert verdict["structural_ok"] is True
    assert verdict["is_correct"] is True
    assert display_latex_equivalent("6x+24", "6x + 24") is True
    assert normalize_math16_display_latex("6x + 24") == normalize_math16_display_latex("6x+24")


def test_poly_division_rejects_unequal_coefficients():
    submitted = {
        "quotient_coefficients": [6, 23],
        "remainder_coefficients": [102],
        "quotient_latex": "6x+24",
        "remainder_latex": "102",
    }
    verdict = evaluate_math16_polynomial_division_general(DIV_PAYLOAD, submitted)
    assert verdict["is_correct"] is False
    assert verdict["structural_ok"] is False


def test_factor_roots_equivalent_latex_forms_pass_with_correct_roots():
    variants = [
        {
            "roots": [-6, 2],
            "factorization_latex": "(x + 6)(x - 2)",
            "roots_latex": "x = -6, 2",
        },
        {
            "roots": [-6, 2],
            "factorization_latex": "(x+6)(x-2)",
            "roots_latex": "-6, 2",
        },
        {
            "roots": [-6, 2],
            "factorization_latex": r"(x+6)(x-2)=0",
            "roots_latex": r"[-6,\,2]",
        },
    ]
    for submitted in variants:
        verdict = evaluate_math16_polynomial_factor_roots(ROOTS_PAYLOAD, submitted)
        assert verdict["is_correct"] is True, submitted
        assert verdict["structural_ok"] is True


def test_factor_roots_rejects_different_roots():
    submitted = {
        "roots": [-2, 6],
        "factorization_latex": "(x+6)(x-2)=0",
        "roots_latex": r"[-6,\,2]",
    }
    verdict = evaluate_math16_polynomial_factor_roots(ROOTS_PAYLOAD, submitted)
    assert verdict["is_correct"] is False
    assert verdict["structural_ok"] is False


def test_q04_wrong_radical_latex_still_rejected():
    payload = {"radicand": 135}
    submitted = {
        "coefficient": 3,
        "radicand": 15,
        "canonical_latex": r"\sqrt{(3, 15)}",
    }
    verdict = evaluate_math_task_oracle(
        "radical_simplification_canonical", payload, submitted
    )
    assert verdict["structural_ok"] is True
    assert verdict["latex_ok"] is False
    assert verdict["is_correct"] is False


def test_q02_bare_string_remainder_still_rejected():
    payload = {
        "dividend_coefficients": [6, 4, 0],
        "divisor_coefficients": [2, 0, 0],
        "remainder": "4x",
        "quotient": 3,
    }
    verdict = evaluate_math_task_oracle(
        "polynomial_division_remainder_only", payload, "4x"
    )
    assert verdict["is_correct"] is False
    ok = evaluate_math_task_oracle(
        "polynomial_division_remainder_only",
        payload,
        {"remainder": "4x", "canonical_latex": "4x"},
    )
    assert ok["is_correct"] is True


def test_q10_compound_radical_signed_coeffs_no_regression():
    payload = {
        "larger_root": {
            "rational": 2,
            "radical_coefficient": 1,
            "radicand": 3,
            "canonical_latex": r"2+\sqrt{3}",
        },
        "smaller_root": {
            "rational": 2,
            "radical_coefficient": -1,
            "radicand": 3,
            "canonical_latex": r"2-\sqrt{3}",
        },
        "equation": "(x-2)^2=3",
        "order": "a>b",
        "target": "2a+b",
    }
    assert normalize_compound_radical(payload["larger_root"])[1] == 1
    assert normalize_compound_radical(payload["smaller_root"])[1] == -1
    good = {
        "result": {
            "rational": 6,
            "radical_coefficient": 1,
            "radicand": 3,
            "canonical_latex": r"6+\sqrt{3}",
        }
    }
    assert evaluate_math_task_oracle("compound_radical_result", payload, good)[
        "is_correct"
    ]
    bad_sign = {
        "result": {
            "rational": 6,
            "radical_coefficient": -1,
            "radicand": 3,
            "canonical_latex": r"6+\sqrt{3}",
        }
    }
    assert (
        evaluate_math_task_oracle("compound_radical_result", payload, bad_sign)[
            "is_correct"
        ]
        is False
    )
    roundtrip = json.loads(json.dumps(payload))
    assert evaluate_math_task_oracle("compound_radical_result", roundtrip, good)[
        "is_correct"
    ]


def test_json_roundtrip_poly_answers():
    submitted = {
        "quotient_coefficients": [6, 24],
        "remainder_coefficients": [102],
        "quotient_latex": "6x + 24",
        "remainder_latex": "102",
    }
    again = json.loads(json.dumps(submitted))
    assert evaluate_math16_polynomial_division_general(DIV_PAYLOAD, again)["is_correct"]
    roots = {
        "roots": [-6, 2],
        "factorization_latex": "(x + 6)(x - 2)",
        "roots_latex": "x = -6, 2",
    }
    assert evaluate_math16_polynomial_factor_roots(
        ROOTS_PAYLOAD, json.loads(json.dumps(roots))
    )["is_correct"]
