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
# Schema-normalization revision (post ORACLE_SCHEMA_AUDIT_V1_PRE_FIX): accept
# semantically equivalent packaging / types before compare.
EVALUATOR_SCHEMA_NORMALIZE_REVISION = "math16_oracle_schema_normalize_v1"


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
    """Extract (rational, radical_coefficient, radicand); latex is display-only.

    When ``result`` is a str (display latex), it must NOT shadow correct flat
    structural fields on the same dict (ORACLE_SCHEMA_AUDIT_V1 GAP_CONFIRMED q10).
    """
    if not isinstance(value, dict):
        raise ValueError("compound radical must be a dict")
    if "result" in value:
        nested = value["result"]
        if isinstance(nested, dict):
            payload = nested
        elif isinstance(nested, str):
            # Display-only result string: fall back to flat structural fields.
            payload = value
        else:
            raise ValueError("compound radical payload must be a dict")
    else:
        payload = value
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


def _coerce_answer_int(value: Any) -> int | None:
    """Normalize bare int or digit string (e.g. '-12') to int; else None."""
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        text = value.strip()
        if re.fullmatch(r"-?\d+", text):
            return int(text)
    return None


def normalize_remainder_poly_latex(value: Any) -> str | None:
    """Normalize remainder as API coeff list or latex/string to display-canonical form."""
    from core.prompts.domain_function_library import PolynomialOps

    if isinstance(value, str):
        return normalize_math16_display_latex(value)
    if isinstance(value, (list, tuple)):
        try:
            return normalize_math16_display_latex(PolynomialOps.format_latex(list(value)))
        except (TypeError, ValueError, ZeroDivisionError):
            return None
    return None


def _parse_ordered_int_roots_from_text(text: str) -> list[int] | None:
    """Extract an ordered integer root pair from packaging prose or short lists."""
    if not isinstance(text, str):
        return None
    section = re.search(
        r"Roots(?:\s*\([^)]*\))?\s*:\s*([^\n;]+)",
        text,
        flags=re.IGNORECASE,
    )
    if section:
        nums = [int(m) for m in re.findall(r"-?\d+", section.group(1))]
        if len(nums) >= 2:
            return nums[:2]
    nums = [int(m) for m in re.findall(r"-?\d+", text)]
    if len(nums) == 2:
        return nums
    return None


def normalize_factor_roots_list(submitted_answer: Any) -> list[int] | None:
    """Accept dict roots / bare list / digit strings / prose packaging with Roots:."""
    if isinstance(submitted_answer, list):
        out: list[int] = []
        for item in submitted_answer:
            coerced = _coerce_answer_int(item)
            if coerced is None:
                return None
            out.append(coerced)
        return out
    if isinstance(submitted_answer, dict):
        roots = submitted_answer.get("roots")
        if isinstance(roots, list):
            return normalize_factor_roots_list(roots)
        if isinstance(roots, str):
            return _parse_ordered_int_roots_from_text(roots)
        return None
    if isinstance(submitted_answer, str):
        return _parse_ordered_int_roots_from_text(submitted_answer)
    return None


def _as_rational_value(value: Any) -> Fraction | None:
    """Accept 'p/q' string, Fraction, or {numerator, denominator}."""
    try:
        if isinstance(value, Fraction):
            return value
        if isinstance(value, str):
            return Fraction(value.strip())
        if isinstance(value, dict):
            if "numerator" in value and "denominator" in value:
                return Fraction(
                    _integer(value["numerator"], "numerator"),
                    _integer(value["denominator"], "denominator"),
                )
            if "value" in value:
                return _as_rational_value(value["value"])
        return None
    except (ValueError, TypeError, ZeroDivisionError, KeyError):
        return None


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
    got_roots = normalize_factor_roots_list(submitted_answer)
    structural_ok = got_roots == list(structural["roots"])
    latex_ok = False
    if isinstance(submitted_answer, dict):
        latex_ok = _factorization_latex_equivalent(
            submitted_answer.get("factorization_latex"), expected["factorization_latex"]
        ) and _roots_latex_equivalent(
            submitted_answer.get("roots_latex"), list(structural["roots"])
        )
    # Roots list is the semantic judge; latex / packaging are presentation-only.
    return {
        "oracle_type": oracle_type,
        "is_correct": structural_ok,
        "expected_answer": expected,
        "submitted_answer": submitted_answer,
        "error": None if structural_ok else "structural_mismatch",
        "structural_ok": structural_ok,
        "latex_ok": latex_ok,
        "latex_presentation_ok": latex_ok,
        "normalized_roots": got_roots,
        "evaluator_revision": EVALUATOR_SCHEMA_NORMALIZE_REVISION,
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
    expected_frac = Fraction(structural["value"])
    submitted_value: Any = submitted_answer
    latex: Any = None
    if isinstance(submitted_answer, dict):
        if "value" in submitted_answer:
            submitted_value = submitted_answer.get("value")
        elif "numerator" in submitted_answer and "denominator" in submitted_answer:
            submitted_value = submitted_answer
        latex = submitted_answer.get("canonical_latex")
    got = _as_rational_value(submitted_value)
    structural_ok = got is not None and got == expected_frac
    latex_ok = latex is None or display_latex_equivalent(latex, expected["canonical_latex"])
    # Numeric value is semantic judge; latex is presentation-only (GAP_SUSPECTED).
    return {
        "oracle_type": oracle_type,
        "is_correct": structural_ok,
        "expected_answer": expected,
        "submitted_answer": submitted_answer,
        "error": None if structural_ok else "structural_mismatch",
        "structural_ok": structural_ok,
        "latex_ok": latex_ok,
        "latex_presentation_ok": latex_ok,
        "evaluator_revision": EVALUATOR_SCHEMA_NORMALIZE_REVISION,
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
    latex = submitted_answer.get("canonical_latex")
    latex_ok = latex is None or display_latex_equivalent(latex, expected["canonical_latex"])
    # Structure is semantic judge; latex presentation-only (GAP_SUSPECTED).
    return {
        "oracle_type": oracle_type,
        "is_correct": structural_ok,
        "expected_answer": expected,
        "submitted_answer": submitted_answer,
        "error": None if structural_ok else "structural_mismatch",
        "structural_ok": structural_ok,
        "latex_ok": latex_ok,
        "latex_presentation_ok": latex_ok,
        "evaluator_revision": EVALUATOR_SCHEMA_NORMALIZE_REVISION,
    }


def evaluate_polynomial_division_remainder_only(
    oracle_payload: dict[str, Any], submitted_answer: Any
) -> dict[str, Any]:
    oracle_type = "polynomial_division_remainder_only"
    expected = {"remainder": "4x", "canonical_latex": "4x"}
    expected_norm = normalize_math16_display_latex("4x")
    # Quotient is audit-only in oracle_payload and must not be required for scoring.
    if oracle_payload.get("remainder") not in ("4x", expected["remainder"]):
        # Still allow payload without remainder key if frozen params are coefficients.
        pass

    rem_norm: str | None = None
    latex_norm: str | None = None
    if isinstance(submitted_answer, str):
        rem_norm = normalize_remainder_poly_latex(submitted_answer)
    elif isinstance(submitted_answer, dict):
        # Reject scoring on quotient alone.
        if "quotient" in submitted_answer and set(submitted_answer) <= {"quotient"}:
            return {
                "oracle_type": oracle_type,
                "is_correct": False,
                "expected_answer": expected,
                "submitted_answer": submitted_answer,
                "error": "remainder_mismatch",
                "evaluator_revision": EVALUATOR_SCHEMA_NORMALIZE_REVISION,
            }
        rem_norm = normalize_remainder_poly_latex(submitted_answer.get("remainder"))
        latex_norm = normalize_remainder_poly_latex(submitted_answer.get("canonical_latex"))
    else:
        return _result(oracle_type, expected, submitted_answer)

    # Prefer remainder field; latex alone may carry the same math when remainder absent.
    if rem_norm is not None:
        ok = rem_norm == expected_norm
    elif latex_norm is not None:
        ok = latex_norm == expected_norm
    else:
        ok = False
    return {
        "oracle_type": oracle_type,
        "is_correct": ok,
        "expected_answer": expected,
        "submitted_answer": submitted_answer,
        "error": None if ok else "remainder_mismatch",
        "normalized_remainder": rem_norm if rem_norm is not None else latex_norm,
        "evaluator_revision": EVALUATOR_SCHEMA_NORMALIZE_REVISION,
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
        if submitted_answer.get("answer") == 12 or submitted_answer.get("answer") == "12":
            return _result(oracle_type, expected, submitted_answer, "legacy_wrong_answer")
        value = submitted_answer.get("answer", submitted_answer.get("value"))
        coerced = _coerce_answer_int(value)
        ok = coerced == expected
    else:
        coerced = _coerce_answer_int(submitted_answer)
        ok = coerced == expected
    return {
        "oracle_type": oracle_type,
        "is_correct": ok,
        "expected_answer": expected,
        "submitted_answer": submitted_answer,
        "error": None if ok else "answer_mismatch",
        "factor_order_policy": "strict_source_template",
        "evaluator_revision": EVALUATOR_SCHEMA_NORMALIZE_REVISION,
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
    latex_ok = latex is None or display_latex_equivalent(latex, expected["canonical_latex"])
    # Numeric fraction is semantic judge; latex presentation-only (GAP_SUSPECTED).
    return {
        "oracle_type": oracle_type,
        "is_correct": structural_ok,
        "expected_answer": expected,
        "submitted_answer": submitted_answer,
        "error": None if structural_ok else "fraction_mismatch",
        "structural_ok": structural_ok,
        "latex_ok": latex_ok,
        "latex_presentation_ok": latex_ok,
        "evaluator_revision": EVALUATOR_SCHEMA_NORMALIZE_REVISION,
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
    latex = submitted_answer.get("canonical_latex")
    latex_ok = latex is None or display_latex_equivalent(latex, expected["canonical_latex"])
    # Structure is semantic judge; latex presentation-only (GAP_SUSPECTED).
    return {
        "oracle_type": oracle_type,
        "is_correct": structural_ok,
        "expected_answer": expected,
        "submitted_answer": submitted_answer,
        "error": None if structural_ok else "radical_mismatch",
        "structural_ok": structural_ok,
        "latex_ok": latex_ok,
        "latex_presentation_ok": latex_ok,
        "evaluator_revision": EVALUATOR_SCHEMA_NORMALIZE_REVISION,
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
    latex = None
    if "result" in submitted_answer and isinstance(submitted_answer["result"], dict):
        latex = submitted_answer["result"].get("canonical_latex")
    else:
        latex = submitted_answer.get("canonical_latex")
    # Structure is the semantic judge; non-semantic whitespace must not veto.
    latex_ok = latex is None or display_latex_equivalent(
        latex, expected["result"]["canonical_latex"]
    )
    return {
        "oracle_type": oracle_type,
        "is_correct": structural_ok,
        "expected_answer": expected,
        "submitted_answer": submitted_answer,
        "error": None if structural_ok else "structural_mismatch",
        "structural_ok": structural_ok,
        "latex_ok": latex_ok,
        "latex_presentation_ok": latex_ok,
        "normalized": {"expected": expected_tuple, "submitted": got},
        "evaluator_revision": EVALUATOR_SCHEMA_NORMALIZE_REVISION,
    }


def classify_math16_oracle_failure(verdict: dict[str, Any]) -> str:
    """Map oracle verdict to failure taxonomy (not INTRINSIC_SAFETY for math mismatches)."""
    if verdict.get("is_correct"):
        return "passed"
    structural_ok = verdict.get("structural_ok")
    latex_ok = verdict.get("latex_ok")
    error = str(verdict.get("error") or "")
    # True safety / policy denials only (not ordinary oracle mismatches).
    safety_markers = (
        "safety",
        "policy_denied",
        "intrinsic_safety",
        "blocked_by_safety",
    )
    if any(marker in error.lower() for marker in safety_markers):
        return "intrinsic_safety"
    if structural_ok is True and latex_ok is False:
        return "latex_mismatch"
    if structural_ok is False:
        return "structural_mismatch"
    if error in {
        "structural_or_latex_mismatch",
        "compound_radical_mismatch",
        "radical_mismatch",
        "fraction_mismatch",
        "remainder_mismatch",
        "answer_mismatch",
    }:
        # Prefer finer labels when structural/latex flags exist; else math incorrect.
        if "latex" in error and structural_ok is not False:
            return "latex_mismatch"
        if "structural" in error:
            return "structural_mismatch"
        return "answer_incorrect"
    return "answer_incorrect"


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
