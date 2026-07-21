"""Unit tests for ORACLE_SCHEMA_AUDIT_V1 gap fixes (semantic normalize)."""
from __future__ import annotations

from fractions import Fraction

from agent_tools.finals_rebuild.math_task_oracles import evaluate_math_task_oracle
from agent_tools.finals_rebuild.math16_oracles import (
    evaluate_math16_exact_rational_expression,
    evaluate_math16_polynomial_factor_roots,
    evaluate_math16_radical_simplification,
    evaluate_polynomial_division_remainder_only,
    evaluate_polynomial_factor_parameter_recovery,
    normalize_compound_radical,
)


Q02_PAYLOAD = {
    "dividend_coefficients": [6, 4, 0],
    "divisor_coefficients": [2, 0, 0],
    "remainder": "4x",
    "quotient": 3,
}
Q08_PAYLOAD = {"a": 2, "b": 13, "c": -7, "strict_source_template": True}
ROOTS_PAYLOAD = {"quadratic_coefficients": [1, 4, -12]}
Q10_PAYLOAD = {
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


def test_q02_accepts_bare_string_and_api_list_remainder():
    assert evaluate_polynomial_division_remainder_only(Q02_PAYLOAD, "4x")["is_correct"]
    assert evaluate_polynomial_division_remainder_only(
        Q02_PAYLOAD, {"remainder": [4, 0], "canonical_latex": "4x"}
    )["is_correct"]
    assert evaluate_polynomial_division_remainder_only(
        Q02_PAYLOAD, {"remainder": [4, 0]}
    )["is_correct"]
    assert evaluate_polynomial_division_remainder_only(
        Q02_PAYLOAD, {"remainder": "4x", "canonical_latex": "4x"}
    )["is_correct"]


def test_q02_still_rejects_wrong_remainder_and_quotient_only():
    assert (
        evaluate_polynomial_division_remainder_only(
            Q02_PAYLOAD, {"remainder": "3x", "canonical_latex": "3x"}
        )["is_correct"]
        is False
    )
    assert (
        evaluate_polynomial_division_remainder_only(Q02_PAYLOAD, {"quotient": 3})[
            "is_correct"
        ]
        is False
    )
    assert evaluate_polynomial_division_remainder_only(Q02_PAYLOAD, "3x")["is_correct"] is False


def test_q08_accepts_digit_string_and_rejects_true_wrong():
    assert evaluate_polynomial_factor_parameter_recovery(Q08_PAYLOAD, -12)["is_correct"]
    assert evaluate_polynomial_factor_parameter_recovery(Q08_PAYLOAD, "-12")["is_correct"]
    assert evaluate_polynomial_factor_parameter_recovery(
        Q08_PAYLOAD, {"answer": "-12"}
    )["is_correct"]
    assert evaluate_polynomial_factor_parameter_recovery(Q08_PAYLOAD, "28")["is_correct"] is False
    assert evaluate_polynomial_factor_parameter_recovery(Q08_PAYLOAD, 28)["is_correct"] is False
    assert (
        evaluate_polynomial_factor_parameter_recovery(Q08_PAYLOAD, {"answer": 28})[
            "is_correct"
        ]
        is False
    )


def test_factor_roots_accepts_bare_list_strings_and_prose():
    assert evaluate_math16_polynomial_factor_roots(ROOTS_PAYLOAD, [-6, 2])["is_correct"]
    assert evaluate_math16_polynomial_factor_roots(
        ROOTS_PAYLOAD, ["-6", "2"]
    )["is_correct"]
    assert evaluate_math16_polynomial_factor_roots(
        ROOTS_PAYLOAD, {"roots": [-6, 2]}
    )["is_correct"]
    prose = "Factorization: (x - 2)(x + 6), Roots: -6, 2"
    assert evaluate_math16_polynomial_factor_roots(ROOTS_PAYLOAD, prose)["is_correct"]
    prose2 = (
        "Factorization: $(x + 6)(x - 2)$\n"
        "Roots (ascending): -6, 2\n"
        "Roots LaTeX: $x = -6, x = 2$"
    )
    assert evaluate_math16_polynomial_factor_roots(ROOTS_PAYLOAD, prose2)["is_correct"]


def test_factor_roots_still_rejects_wrong_roots():
    assert (
        evaluate_math16_polynomial_factor_roots(ROOTS_PAYLOAD, {"roots": [6, -2]})[
            "is_correct"
        ]
        is False
    )
    assert (
        evaluate_math16_polynomial_factor_roots(ROOTS_PAYLOAD, "Roots: 1, 2")[
            "is_correct"
        ]
        is False
    )
    assert evaluate_math16_polynomial_factor_roots(ROOTS_PAYLOAD, [2, -6])["is_correct"] is False


def test_q10_result_str_does_not_shadow_flat_fields():
    submitted = {
        "rational": 6,
        "radical_coefficient": 1,
        "radicand": 3,
        "canonical_latex": r"6 + \sqrt{3}",
        "result": r"6 + \sqrt{3}",
    }
    assert normalize_compound_radical(submitted) == (6, 1, 3)
    assert evaluate_math_task_oracle("compound_radical_result", Q10_PAYLOAD, submitted)[
        "is_correct"
    ]
    bad = {**submitted, "rational": 5}
    assert (
        evaluate_math_task_oracle("compound_radical_result", Q10_PAYLOAD, bad)[
            "is_correct"
        ]
        is False
    )


def test_gap_suspected_radical_structural_without_latex_passes():
    payload = {"radicand": 135}
    submitted = {"coefficient": 3, "radicand": 15}
    v = evaluate_math_task_oracle("radical_simplification_canonical", payload, submitted)
    assert v["structural_ok"] is True
    assert v["is_correct"] is True
    assert v["latex_ok"] is True  # missing latex treated as presentation-ok
    wrong = {"coefficient": 1, "radicand": 135, "canonical_latex": r"\sqrt{135}"}
    assert (
        evaluate_math_task_oracle("radical_simplification_canonical", payload, wrong)[
            "is_correct"
        ]
        is False
    )


def test_gap_suspected_fraction_structural_without_exact_latex_passes():
    payload = {"expression": "3/7 - (-1/4)"}
    submitted = {"numerator": 19, "denominator": 28, "canonical_latex": r"\dfrac{19}{28}"}
    v = evaluate_math_task_oracle("exact_fraction_canonical", payload, submitted)
    assert v["structural_ok"] is True
    assert v["is_correct"] is True
    wrong = {"numerator": 1, "denominator": 2, "canonical_latex": r"\frac{19}{28}"}
    assert (
        evaluate_math_task_oracle("exact_fraction_canonical", payload, wrong)[
            "is_correct"
        ]
        is False
    )


def test_gap_suspected_exact_rational_accepts_fraction_shapes():
    from agent_tools.finals_rebuild.math16_pool import tasks_by_id

    task = tasks_by_id()["ce115_calc_exact_rational_expression_l1"]
    payload = task["oracle_payload"]
    assert evaluate_math16_exact_rational_expression(
        payload, {"value": "2679/10", "canonical_latex": r"\frac{2679}{10}"}
    )["is_correct"]
    assert evaluate_math16_exact_rational_expression(
        payload, {"value": Fraction(2679, 10)}
    )["is_correct"]
    assert evaluate_math16_exact_rational_expression(
        payload, {"numerator": 2679, "denominator": 10}
    )["is_correct"]
    assert (
        evaluate_math16_exact_rational_expression(
            payload, {"value": "2678/10"}
        )["is_correct"]
        is False
    )


def test_gap_suspected_calc_radical_structural_only():
    from agent_tools.finals_rebuild.math16_pool import tasks_by_id

    task = tasks_by_id()["ce115_calc_radical_simplification_l1"]
    payload = task["oracle_payload"]
    assert evaluate_math16_radical_simplification(
        payload, {"coefficient": 3, "radicand": 3}
    )["is_correct"]
    assert (
        evaluate_math16_radical_simplification(
            payload, {"coefficient": 1, "radicand": 27}
        )["is_correct"]
        is False
    )
