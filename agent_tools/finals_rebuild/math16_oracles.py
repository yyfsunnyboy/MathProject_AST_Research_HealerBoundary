"""Math16-LaTeX-v1 oracles: structural comparison, not string-only equality."""
from __future__ import annotations

import re
from fractions import Fraction
from math import isqrt
from typing import Any, Callable

from agent_tools.finals_rebuild.math_task_oracles import (
    evaluate_exact_rational_expression,
    evaluate_polynomial_division_general,
    evaluate_polynomial_factor_roots,
    evaluate_radical_simplification,
)

# Display-latex revision: structural fields judge math correctness; latex is presentation.
EVALUATOR_LATEX_SEMANTIC_REVISION = "math16_latex_semantic_v2"


def _result(oracle_type: str, expected: Any, submitted: Any, error: str | None = None) -> dict[str, Any]:
    return {
        "oracle_type": oracle_type,
        "is_correct": error is None and submitted == expected,
        "expected_answer": expected,
        "submitted_answer": submitted,
        "error": error,
    }


def normalize_math16_display_latex(text: Any) -> str | None:
    """Normalize non-semantic LaTeX display differences for presentation checks."""
    if not isinstance(text, str):
        return None
    s = text.strip()
    wrappers = (
        (r"\(", r"\)"),
        (r"\[", r"\]"),
        ("$$", "$$"),
        ("$", "$"),
    )
    for left, right in wrappers:
        if s.startswith(left) and s.endswith(right) and len(s) >= len(left) + len(right):
            s = s[len(left) : len(s) - len(right)].strip()
            break
    for token in (r"\,", r"\;", r"\:", r"\!", r"\ ", r"~"):
        s = s.replace(token, "")
    s = re.sub(r"\s+", "", s)
    return s


def display_latex_equivalent(left: Any, right: Any) -> bool:
    a = normalize_math16_display_latex(left)
    b = normalize_math16_display_latex(right)
    return a is not None and b is not None and a == b


def _factorization_latex_equivalent(submitted: Any, expected: str) -> bool:
    a = normalize_math16_display_latex(submitted)
    b = normalize_math16_display_latex(expected)
    if a is None or b is None:
        return False
    a = re.sub(r"=0$", "", a)
    b = re.sub(r"=0$", "", b)
    return a == b


def _roots_latex_equivalent(submitted: Any, roots: list[int]) -> bool:
    """Accept common roots display forms that encode the same ordered integer roots."""
    if not isinstance(submitted, str):
        return False
    normalized = normalize_math16_display_latex(submitted)
    if normalized is None:
        return False
    nums = [int(match) for match in re.findall(r"-?\d+", normalized)]
    return nums == list(roots)


def _integer(value: Any, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be an integer")
    return value


def coerce_exact_int(value: Any, name: str = "value") -> int:
    """Accept int or integer-valued Fraction; reject non-integral Fraction."""
    if isinstance(value, bool):
        raise ValueError(f"{name} must be an integer")
    if isinstance(value, int):
        return value
    if isinstance(value, Fraction):
        if value.denominator != 1:
            raise ValueError(f"{name} must be an integer (got non-integral Fraction {value})")
        return int(value.numerator)
    raise ValueError(f"{name} must be an integer")


def json_safe_default(obj: Any) -> Any:
    """JSON boundary: integer-valued Fraction -> int; never coerce non-integral Fraction."""
    if isinstance(obj, Fraction):
        if obj.denominator == 1:
            return int(obj.numerator)
        raise TypeError(
            f"Object of type Fraction is not JSON serializable for non-integer value {obj}"
        )
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


def _as_fraction(value: Any) -> Fraction:
    if isinstance(value, bool):
        raise ValueError("boolean is not a number")
    if isinstance(value, int):
        return Fraction(value, 1)
    if isinstance(value, str):
        return Fraction(value)
    if isinstance(value, Fraction):
        return value
    raise ValueError("unsupported numeric type")


def normalize_compound_radical(value: Any) -> tuple[int, int, int]:
    """Extract (rational, radical_coefficient, radicand); latex is display-only."""
    if not isinstance(value, dict):
        raise ValueError("compound radical must be a dict")
    payload = value.get("result", value)
    if not isinstance(payload, dict):
        raise ValueError("compound radical payload must be a dict")
    rational = coerce_exact_int(payload["rational"], "rational")
    coeff = coerce_exact_int(payload["radical_coefficient"], "radical_coefficient")
    radicand = coerce_exact_int(payload["radicand"], "radicand")
    if radicand <= 0:
        raise ValueError("radicand must be positive")
    if coeff == 0:
        raise ValueError("radical_coefficient must be nonzero for compound form")
    return rational, coeff, radicand


def compound_radicals_equal(left: Any, right: Any) -> bool:
    try:
        return normalize_compound_radical(left) == normalize_compound_radical(right)
    except (KeyError, ValueError, TypeError):
        return False


def evaluate_math16_polynomial_division_general(
    oracle_payload: dict[str, Any], submitted_answer: Any
) -> dict[str, Any]:
    oracle_type = "math16_polynomial_division_general"
    base = evaluate_polynomial_division_general(oracle_payload, None)
    if base.get("error"):
        return _result(oracle_type, None, submitted_answer, base["error"])
    structural = base["expected_answer"]
    expected = {
        **structural,
        "quotient_latex": "6x+24",
        "remainder_latex": "102",
    }
    # Freeze is identity for Math16 seed; structural must match base oracle.
    if (
        structural.get("quotient_coefficients") != [6, 24]
        or structural.get("remainder_coefficients") != [102]
    ):
        return _result(oracle_type, None, submitted_answer, "math16 identity drift")
    if not isinstance(submitted_answer, dict):
        return _result(oracle_type, expected, submitted_answer)
    submitted_structural = {
        "quotient_coefficients": submitted_answer.get("quotient_coefficients"),
        "remainder_coefficients": submitted_answer.get("remainder_coefficients"),
    }
    structural_ok = submitted_structural == structural
    latex_ok = display_latex_equivalent(
        submitted_answer.get("quotient_latex"), expected["quotient_latex"]
    ) and display_latex_equivalent(
        submitted_answer.get("remainder_latex"), expected["remainder_latex"]
    )
    # Structural coefficients are the semantic judge; latex is presentation-only.
    return {
        "oracle_type": oracle_type,
        "is_correct": structural_ok,
        "expected_answer": expected,
        "submitted_answer": submitted_answer,
        "error": None if structural_ok else "structural_mismatch",
        "structural_ok": structural_ok,
        "latex_ok": latex_ok,
        "latex_presentation_ok": latex_ok,
        "evaluator_revision": EVALUATOR_LATEX_SEMANTIC_REVISION,
    }


def evaluate_math16_polynomial_factor_roots(
    oracle_payload: dict[str, Any], submitted_answer: Any
) -> dict[str, Any]:
    oracle_type = "math16_polynomial_factor_roots"
    base = evaluate_polynomial_factor_roots(oracle_payload, None)
    if base.get("error"):
        return _result(oracle_type, None, submitted_answer, base["error"])
    structural = base["expected_answer"]
    expected = {
        **structural,
        "factorization_latex": "(x+6)(x-2)=0",
        "roots_latex": r"[-6,\,2]",
    }
    if structural.get("roots") != [-6, 2]:
        return _result(oracle_type, None, submitted_answer, "math16 identity drift")
    if not isinstance(submitted_answer, dict):
        return _result(oracle_type, expected, submitted_answer)
    structural_ok = submitted_answer.get("roots") == structural["roots"]
    latex_ok = _factorization_latex_equivalent(
        submitted_answer.get("factorization_latex"), expected["factorization_latex"]
    ) and _roots_latex_equivalent(
        submitted_answer.get("roots_latex"), list(structural["roots"])
    )
    # Roots list is the semantic judge; latex fields are presentation-only.
    return {
        "oracle_type": oracle_type,
        "is_correct": structural_ok,
        "expected_answer": expected,
        "submitted_answer": submitted_answer,
        "error": None if structural_ok else "structural_mismatch",
        "structural_ok": structural_ok,
        "latex_ok": latex_ok,
        "latex_presentation_ok": latex_ok,
        "evaluator_revision": EVALUATOR_LATEX_SEMANTIC_REVISION,
    }


def evaluate_math16_exact_rational_expression(
    oracle_payload: dict[str, Any], submitted_answer: Any
) -> dict[str, Any]:
    oracle_type = "math16_exact_rational_expression"
    base = evaluate_exact_rational_expression(oracle_payload, None)
    if base.get("error"):
        return _result(oracle_type, None, submitted_answer, base["error"])
    structural = base["expected_answer"]
    expected = {**structural, "canonical_latex": r"\frac{2679}{10}"}
    if structural.get("value") != "2679/10":
        return _result(oracle_type, None, submitted_answer, "math16 identity drift")
    if not isinstance(submitted_answer, dict):
        return _result(oracle_type, expected, submitted_answer)
    structural_ok = submitted_answer.get("value") == structural["value"]
    latex_ok = submitted_answer.get("canonical_latex") == expected["canonical_latex"]
    return {
        "oracle_type": oracle_type,
        "is_correct": structural_ok and latex_ok,
        "expected_answer": expected,
        "submitted_answer": submitted_answer,
        "error": None if structural_ok and latex_ok else "structural_or_latex_mismatch",
        "structural_ok": structural_ok,
        "latex_ok": latex_ok,
    }


def evaluate_math16_radical_simplification(
    oracle_payload: dict[str, Any], submitted_answer: Any
) -> dict[str, Any]:
    oracle_type = "math16_radical_simplification"
    base = evaluate_radical_simplification(oracle_payload, None)
    if base.get("error"):
        return _result(oracle_type, None, submitted_answer, base["error"])
    structural = base["expected_answer"]
    expected = {**structural, "canonical_latex": r"3\sqrt{3}"}
    if structural != {"coefficient": 3, "radicand": 3}:
        return _result(oracle_type, None, submitted_answer, "math16 identity drift")
    if not isinstance(submitted_answer, dict):
        return _result(oracle_type, expected, submitted_answer)
    structural_ok = (
        submitted_answer.get("coefficient") == 3 and submitted_answer.get("radicand") == 3
    )
    latex_ok = submitted_answer.get("canonical_latex") == expected["canonical_latex"]
    return {
        "oracle_type": oracle_type,
        "is_correct": structural_ok and latex_ok,
        "expected_answer": expected,
        "submitted_answer": submitted_answer,
        "error": None if structural_ok and latex_ok else "structural_or_latex_mismatch",
        "structural_ok": structural_ok,
        "latex_ok": latex_ok,
    }


def evaluate_polynomial_division_remainder_only(
    oracle_payload: dict[str, Any], submitted_answer: Any
) -> dict[str, Any]:
    oracle_type = "polynomial_division_remainder_only"
    expected = {"remainder": "4x", "canonical_latex": "4x"}
    # Quotient is audit-only in oracle_payload and must not be required for scoring.
    if oracle_payload.get("remainder") not in ("4x", expected["remainder"]):
        # Still allow payload without remainder key if frozen params are coefficients.
        pass
    if not isinstance(submitted_answer, dict):
        return _result(oracle_type, expected, submitted_answer)
    remainder = submitted_answer.get("remainder")
    latex = submitted_answer.get("canonical_latex")
    ok = remainder in ("4x", r"4x") and latex in ("4x", r"4x")
    # Reject scoring on quotient alone.
    if "quotient" in submitted_answer and set(submitted_answer) <= {"quotient"}:
        ok = False
    return {
        "oracle_type": oracle_type,
        "is_correct": ok,
        "expected_answer": expected,
        "submitted_answer": submitted_answer,
        "error": None if ok else "remainder_mismatch",
    }


def evaluate_polynomial_factor_parameter_recovery(
    oracle_payload: dict[str, Any], submitted_answer: Any
) -> dict[str, Any]:
    oracle_type = "polynomial_factor_parameter_recovery"
    expected = -12
    a = _integer(oracle_payload["a"], "a")
    b = _integer(oracle_payload["b"], "b")
    c = _integer(oracle_payload["c"], "c")
    if (a, b, c) != (2, 13, -7):
        return _result(oracle_type, None, submitted_answer, "oracle payload identity drift")
    # Strict source template: first factor is (3x+a); swapped factor redefinition forbidden.
    expanded = [3 * b, 3 * c + a * b, a * c]
    if expanded != [39, 5, -14]:
        return _result(oracle_type, None, submitted_answer, "expansion check failed")
    if a + 2 * c != expected:
        return _result(oracle_type, None, submitted_answer, "answer identity drift")
    # Reject known legacy wrong values even if submitted somehow encodes them.
    if isinstance(submitted_answer, dict):
        if submitted_answer.get("a") == -2 or submitted_answer.get("c") == 7:
            return _result(oracle_type, expected, submitted_answer, "legacy_wrong_factor_order")
        if submitted_answer.get("answer") == 12:
            return _result(oracle_type, expected, submitted_answer, "legacy_wrong_answer")
        value = submitted_answer.get("answer", submitted_answer.get("value"))
        ok = value == expected
    else:
        ok = submitted_answer == expected
    return {
        "oracle_type": oracle_type,
        "is_correct": ok,
        "expected_answer": expected,
        "submitted_answer": submitted_answer,
        "error": None if ok else "answer_mismatch",
        "factor_order_policy": "strict_source_template",
    }


def evaluate_integer_exact(oracle_payload: dict[str, Any], submitted_answer: Any) -> dict[str, Any]:
    oracle_type = "integer_exact"
    if "selected" in oracle_payload:
        expected = _integer(oracle_payload["selected"], "selected")
    elif "value" in oracle_payload:
        expected = _integer(oracle_payload["value"], "value")
    elif "a" in oracle_payload and "b" in oracle_payload:
        expected = _integer(oracle_payload["a"], "a") + _integer(oracle_payload["b"], "b")
    else:
        return _result(oracle_type, None, submitted_answer, "integer_exact payload incomplete")
    return _result(oracle_type, expected, submitted_answer)


def evaluate_integer_count(oracle_payload: dict[str, Any], submitted_answer: Any) -> dict[str, Any]:
    oracle_type = "integer_count"
    values = oracle_payload.get("valid_values")
    if not isinstance(values, list) or not values:
        return _result(oracle_type, None, submitted_answer, "valid_values required")
    expected = {"count": len(values)}
    if not isinstance(submitted_answer, dict):
        return _result(oracle_type, expected, submitted_answer)
    ok = submitted_answer.get("count") == expected["count"]
    return {
        "oracle_type": oracle_type,
        "is_correct": ok,
        "expected_answer": expected,
        "submitted_answer": submitted_answer,
        "error": None if ok else "count_mismatch",
    }


def evaluate_integer_exact_k(oracle_payload: dict[str, Any], submitted_answer: Any) -> dict[str, Any]:
    oracle_type = "integer_exact_k"
    expected = {"k": _integer(oracle_payload["generation_count"], "generation_count")}
    if not isinstance(submitted_answer, dict):
        return _result(oracle_type, expected, submitted_answer)
    ok = submitted_answer.get("k") == expected["k"]
    return {
        "oracle_type": oracle_type,
        "is_correct": ok,
        "expected_answer": expected,
        "submitted_answer": submitted_answer,
        "error": None if ok else "k_mismatch",
    }


def evaluate_exact_fraction_canonical(
    oracle_payload: dict[str, Any], submitted_answer: Any
) -> dict[str, Any]:
    oracle_type = "exact_fraction_canonical"
    expression = oracle_payload.get("expression")
    product = oracle_payload.get("product")
    if expression == "9/22 + 11/18 - (23/22 - 7/18)":
        value = Fraction(9, 22) + Fraction(11, 18) - (Fraction(23, 22) - Fraction(7, 18))
    elif expression == "3/7 - (-1/4)":
        value = Fraction(3, 7) - (Fraction(-1, 4))
    elif product == "1/15" or (oracle_payload.get("p1") == "2/6" and oracle_payload.get("p2") == "1/5"):
        value = Fraction(2, 6) * Fraction(1, 5)
    else:
        return _result(oracle_type, None, submitted_answer, "unsupported fraction payload")
    value = value.limit_denominator()
    expected = {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "canonical_latex": rf"\frac{{{value.numerator}}}{{{value.denominator}}}",
    }
    if not isinstance(submitted_answer, dict):
        return _result(oracle_type, expected, submitted_answer)
    try:
        num = _integer(submitted_answer["numerator"], "numerator")
        den = _integer(submitted_answer["denominator"], "denominator")
        submitted_frac = Fraction(num, den)
    except (KeyError, ValueError, TypeError, ZeroDivisionError):
        return _result(oracle_type, expected, submitted_answer, "fraction fields invalid")
    structural_ok = submitted_frac == value
    latex = submitted_answer.get("canonical_latex")
    latex_ok = latex == expected["canonical_latex"]
    return {
        "oracle_type": oracle_type,
        "is_correct": structural_ok and latex_ok,
        "expected_answer": expected,
        "submitted_answer": submitted_answer,
        "error": None if structural_ok and latex_ok else "fraction_mismatch",
        "structural_ok": structural_ok,
        "latex_ok": latex_ok,
    }


def evaluate_radical_simplification_canonical(
    oracle_payload: dict[str, Any], submitted_answer: Any
) -> dict[str, Any]:
    oracle_type = "radical_simplification_canonical"
    radicand = _integer(oracle_payload["radicand"], "radicand")
    coeff = 1
    rest = radicand
    factor = 2
    while factor * factor <= rest:
        square = factor * factor
        while rest % square == 0:
            rest //= square
            coeff *= factor
        factor += 1
    expected = {
        "coefficient": coeff,
        "radicand": rest,
        "canonical_latex": (
            rf"{coeff}\sqrt{{{rest}}}" if coeff != 1 else rf"\sqrt{{{rest}}}"
        ),
    }
    if not isinstance(submitted_answer, dict):
        return _result(oracle_type, expected, submitted_answer)
    structural_ok = (
        submitted_answer.get("coefficient") == expected["coefficient"]
        and submitted_answer.get("radicand") == expected["radicand"]
    )
    latex_ok = submitted_answer.get("canonical_latex") == expected["canonical_latex"]
    return {
        "oracle_type": oracle_type,
        "is_correct": structural_ok and latex_ok,
        "expected_answer": expected,
        "submitted_answer": submitted_answer,
        "error": None if structural_ok and latex_ok else "radical_mismatch",
        "structural_ok": structural_ok,
        "latex_ok": latex_ok,
    }


def evaluate_compound_radical_result(
    oracle_payload: dict[str, Any], submitted_answer: Any
) -> dict[str, Any]:
    oracle_type = "compound_radical_result"
    larger = normalize_compound_radical(oracle_payload["larger_root"])
    smaller = normalize_compound_radical(oracle_payload["smaller_root"])
    # 2a+b with a>b: a=(2,+1,3), b=(2,-1,3) => 2a+b = (6,+1,3)
    expected_tuple = (
        2 * larger[0] + smaller[0],
        2 * larger[1] + smaller[1],
        larger[2],
    )
    if expected_tuple != (6, 1, 3):
        return _result(oracle_type, None, submitted_answer, "compound identity drift")
    if larger[1] != 1 or smaller[1] != -1:
        return _result(oracle_type, None, submitted_answer, "signed coefficient identity drift")
    expected = {
        "result": {
            "rational": expected_tuple[0],
            "radical_coefficient": expected_tuple[1],
            "radicand": expected_tuple[2],
            "canonical_latex": r"6+\sqrt{3}",
        }
    }
    if not isinstance(submitted_answer, dict):
        return {
            "oracle_type": oracle_type,
            "is_correct": False,
            "expected_answer": expected,
            "submitted_answer": submitted_answer,
            "error": "submitted must be dict",
        }
    try:
        got = normalize_compound_radical(submitted_answer)
    except (KeyError, ValueError, TypeError) as exc:
        return _result(oracle_type, expected, submitted_answer, str(exc))
    structural_ok = got == expected_tuple
    # latex display is not the sole judge; accept missing latex if structure matches,
    # but if present it must match canonical.
    latex = None
    if "result" in submitted_answer and isinstance(submitted_answer["result"], dict):
        latex = submitted_answer["result"].get("canonical_latex")
    else:
        latex = submitted_answer.get("canonical_latex")
    latex_ok = latex is None or latex == expected["result"]["canonical_latex"]
    return {
        "oracle_type": oracle_type,
        "is_correct": structural_ok and latex_ok,
        "expected_answer": expected,
        "submitted_answer": submitted_answer,
        "error": None if structural_ok and latex_ok else "compound_radical_mismatch",
        "structural_ok": structural_ok,
        "latex_ok": latex_ok,
        "normalized": {"expected": expected_tuple, "submitted": got},
    }


MATH16_ORACLE_DISPATCH: dict[str, Callable[[dict[str, Any], Any], dict[str, Any]]] = {
    "math16_polynomial_division_general": evaluate_math16_polynomial_division_general,
    "math16_polynomial_factor_roots": evaluate_math16_polynomial_factor_roots,
    "math16_exact_rational_expression": evaluate_math16_exact_rational_expression,
    "math16_radical_simplification": evaluate_math16_radical_simplification,
    "polynomial_division_remainder_only": evaluate_polynomial_division_remainder_only,
    "polynomial_factor_parameter_recovery": evaluate_polynomial_factor_parameter_recovery,
    "integer_exact": evaluate_integer_exact,
    "integer_count": evaluate_integer_count,
    "integer_exact_k": evaluate_integer_exact_k,
    "exact_fraction_canonical": evaluate_exact_fraction_canonical,
    "radical_simplification_canonical": evaluate_radical_simplification_canonical,
    "compound_radical_result": evaluate_compound_radical_result,
}
