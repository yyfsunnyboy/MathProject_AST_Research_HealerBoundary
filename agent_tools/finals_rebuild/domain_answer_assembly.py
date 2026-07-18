"""Typed, no-model adapters from Domain API values to Math16 answer leaves."""
from __future__ import annotations

from fractions import Fraction
from typing import Any

from core.prompts.domain_function_library import FractionOps, PolynomialOps, RadicalOps


def exact_int(value: Any) -> int:
    """Accept a real int only; never silently accept bool or coerce float."""
    if type(value) is not int:
        raise TypeError(f"exact-int answer requires int, got {type(value).__name__}")
    return value


def exact_fraction(value: Fraction) -> dict[str, int | str]:
    """Return JSON-safe structural and presentation leaves for a Fraction."""
    if not isinstance(value, Fraction):
        raise TypeError("exact_fraction requires Fraction")
    exact = FractionOps.to_exact(value)
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "value": exact,
        "canonical_latex": FractionOps.to_latex(value),
    }


def polynomial_coefficients(coeffs: list[Any]) -> list[int | float | str]:
    """Serialize coefficient leaves without converting floats to exact values."""
    out: list[int | float | str] = []
    for value in coeffs:
        if isinstance(value, bool):
            raise TypeError("bool is not a polynomial coefficient")
        if isinstance(value, Fraction):
            out.append(FractionOps.to_exact(value))
        elif isinstance(value, (int, float)):
            out.append(value)
        else:
            raise TypeError(f"unsupported coefficient: {type(value).__name__}")
    return out


def radical_term(coeff: int | Fraction, radicand: int) -> dict[str, Any]:
    """Normalize a semantic radical term into JSON leaves plus complete LaTeX."""
    c, r = RadicalOps.simplify_term(coeff, radicand)
    return {
        "coefficient": FractionOps.to_exact(c),
        "radicand": exact_int(r),
        "canonical_latex": RadicalOps.format_term(c, r),
    }


def compound_radical(rational: int | Fraction, radical_coefficient: int | Fraction,
                     radicand: int) -> dict[str, Any]:
    """Normalize a+b*sqrt(r) without passing tuples to RadicalOps.to_latex."""
    a = FractionOps.create(rational)
    b, r = RadicalOps.simplify_term(radical_coefficient, radicand)
    if a.denominator != 1 or isinstance(b, Fraction) and b.denominator != 1:
        raise ValueError("Math16 compound-radical answer requires integer coefficients")
    ai, bi = int(a), int(b)
    return {
        "rational": ai,
        "radical_coefficient": bi,
        "radicand": exact_int(r),
        "canonical_latex": RadicalOps.format_expression({1: ai, r: bi}),
    }


# Declarative boundary used by preflight.  It documents responsibility without
# changing frozen questions or oracle answers.
TASK_OUTPUT_ASSEMBLY: dict[str, dict[str, str]] = {
    "ce115_calc_polynomial_division_l1": {"normalization":"polynomial_coefficients for q/r", "answer":"quotient_coefficients,remainder_coefficients,quotient_latex,remainder_latex"},
    "ce115_calc_polynomial_factor_roots_l1": {"normalization":"factor dict leaves -> Fraction -> sorted exact roots", "answer":"roots,factorization_latex,roots_latex"},
    "ce115_calc_exact_rational_expression_l1": {"normalization":"exact_fraction", "answer":"value,canonical_latex"},
    "ce115_calc_radical_simplification_l1": {"normalization":"radical_term", "answer":"coefficient,radicand,canonical_latex"},
    "ce111_q02_polynomial_division_remainder": {"normalization":"remainder -> PolynomialOps.format_latex", "answer":"remainder,canonical_latex"},
    "ce111_q08_polynomial_factor_parameter_recovery": {"normalization":"strict (3x+a)(dx+c) binding; exact_int", "answer":"int a+2c"},
    "ce111_q03_prime_factor_selection": {"normalization":"exact_int", "answer":"int"},
    "ce112_q01_negative_integer_power": {"normalization":"exact_int", "answer":"int"},
    "ce112_q09_divisor_multiple_intersection": {"normalization":"exact_int", "answer":"{count:int}"},
    "ce111_nonchoice_q01_part1_exponential_growth": {"normalization":"exact_int generation count only", "answer":"{k:int}"},
    "ce111_q05_exact_fraction_expression": {"normalization":"exact_fraction", "answer":"numerator,denominator,canonical_latex"},
    "ce113_q01_negative_fraction_subtraction": {"normalization":"exact_fraction", "answer":"numerator,denominator,canonical_latex"},
    "ce112_q12_independent_probability_fraction": {"normalization":"exact_fraction", "answer":"numerator,denominator,canonical_latex"},
    "ce112_q04_radical_simplification": {"normalization":"radical_term", "answer":"coefficient,radicand,canonical_latex"},
    "ce111_q10_ordered_quadratic_roots_radical": {"normalization":"compound_radical", "answer":"{result:{rational,radical_coefficient,radicand,canonical_latex}}"},
    "ce113_q11_rationalize_denominator": {"normalization":"rationalize then exact_int(a+b)", "answer":"int"},
}
