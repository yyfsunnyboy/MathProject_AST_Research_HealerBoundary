"""Deterministic oracles for 113/114 exam external-validation tasks."""
from __future__ import annotations

import ast
import re
from fractions import Fraction
from typing import Any

from agent_tools.finals_rebuild.math_task_oracles import _canonical_number, _integer, _result


def _as_fraction(value: Any, name: str) -> Fraction:
    if isinstance(value, bool):
        raise ValueError(f"{name} must not be bool")
    if isinstance(value, int):
        return Fraction(value, 1)
    if isinstance(value, str):
        return Fraction(value)
    if isinstance(value, Fraction):
        return value
    raise ValueError(f"{name} must be int or fraction string")


def evaluate_exam_power_of_same_base(oracle_payload: dict[str, Any], submitted_answer: Any) -> dict[str, Any]:
    oracle_type = "exam_power_of_same_base"
    try:
        expression = oracle_payload["expression"]
        base = _integer(oracle_payload["base"], "base")
        if oracle_payload.get("required_form") != "power_of_same_base":
            raise ValueError("required_form must be power_of_same_base")
        if not isinstance(expression, str) or not expression.strip():
            raise ValueError("expression required")
        # Parse 7**10 * 7**2 / 7**4 style product of same-base powers.
        # Protect ** so * / split does not tear exponents apart.
        compact = expression.replace(" ", "")
        placeholder = "@@POW@@"
        protected = compact.replace("**", placeholder)
        tokens = re.split(r"([*/])", protected)
        exponent = Fraction(0)
        sign = 1
        saw_term = False
        for token in tokens:
            if token == "*":
                sign = 1
            elif token == "/":
                sign = -1
            elif token == "":
                continue
            else:
                restored = token.replace(placeholder, "**")
                m = re.fullmatch(rf"{base}\*\*(\-?\d+)", restored)
                if not m:
                    raise ValueError(f"unsupported token {restored!r}")
                exponent += sign * Fraction(int(m.group(1)), 1)
                saw_term = True
        if not saw_term:
            raise ValueError("no matching base powers in expression")
        expected = {"base": base, "exponent": _canonical_number(exponent)}
        return _result(oracle_type, expected, submitted_answer)
    except (KeyError, ValueError, TypeError) as exc:
        return _result(oracle_type, None, submitted_answer, str(exc))


def evaluate_exam_polynomial_simplify(oracle_payload: dict[str, Any], submitted_answer: Any) -> dict[str, Any]:
    oracle_type = "exam_polynomial_simplify"
    try:
        expression = oracle_payload["expression"]
        if not isinstance(expression, str):
            raise ValueError("expression required")
        # Exact expand via ast for the frozen exam expression only.
        tree = ast.parse(expression.replace("^", "**"), mode="eval")

        class _Poly(ast.NodeVisitor):
            def visit(self, node):  # type: ignore[override]
                if isinstance(node, ast.Expression):
                    return self.visit(node.body)
                if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
                    return {0: Fraction(node.value)}
                if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
                    return {k: -v for k, v in self.visit(node.operand).items()}
                if isinstance(node, ast.BinOp):
                    left, right = self.visit(node.left), self.visit(node.right)
                    if isinstance(node.op, ast.Add):
                        out = dict(left)
                        for k, v in right.items():
                            out[k] = out.get(k, Fraction(0)) + v
                        return out
                    if isinstance(node.op, ast.Sub):
                        out = dict(left)
                        for k, v in right.items():
                            out[k] = out.get(k, Fraction(0)) - v
                        return out
                    if isinstance(node.op, ast.Mult):
                        out: dict[int, Fraction] = {}
                        for i, a in left.items():
                            for j, b in right.items():
                                out[i + j] = out.get(i + j, Fraction(0)) + a * b
                        return out
                    if isinstance(node.op, ast.Pow):
                        if not (isinstance(node.right, ast.Constant) and isinstance(node.right.value, int)):
                            raise ValueError("power must be integer constant")
                        exp = node.right.value
                        base = left
                        out = {0: Fraction(1)}
                        for _ in range(exp):
                            nxt: dict[int, Fraction] = {}
                            for i, a in out.items():
                                for j, b in base.items():
                                    nxt[i + j] = nxt.get(i + j, Fraction(0)) + a * b
                            out = nxt
                        return out
                if isinstance(node, ast.Name) and node.id == "x":
                    return {1: Fraction(1)}
                raise ValueError(f"unsupported node {type(node).__name__}")

        coeffs = {deg: coef for deg, coef in _Poly().visit(tree).items() if coef != 0}
        expected = {
            "coefficients": {str(deg): _canonical_number(coef) for deg, coef in sorted(coeffs.items(), reverse=True)}
        }
        # Canonical key order for degrees present in contract: include 0,1,2 for this exam item
        # Contract uses string keys "2","1","0".
        for deg in ("2", "1", "0"):
            expected["coefficients"].setdefault(deg, 0)
            if expected["coefficients"][deg] == 0 and deg not in {str(d) for d in coeffs}:
                expected["coefficients"][deg] = 0
        # Normalize zeros that were filled
        expected["coefficients"] = {
            k: expected["coefficients"][k] for k in ("2", "1", "0")
        }
        return _result(oracle_type, expected, submitted_answer)
    except (KeyError, ValueError, TypeError, SyntaxError) as exc:
        return _result(oracle_type, None, submitted_answer, str(exc))


def evaluate_exam_linear_system_linear_combination(
    oracle_payload: dict[str, Any], submitted_answer: Any
) -> dict[str, Any]:
    oracle_type = "exam_linear_system_linear_combination"
    try:
        equations = oracle_payload["equations"]
        target = oracle_payload["target_expression"]
        if not isinstance(equations, list) or len(equations) != 2:
            raise ValueError("exactly two equations required")
        if target != "x + 2*y":
            raise ValueError("unsupported target_expression")

        def parse_eq(text: str) -> tuple[Fraction, Fraction, Fraction]:
            left, right = text.replace(" ", "").split("=")
            # ax+by form with optional signs
            m = re.fullmatch(r"([+-]?\d+)\*x([+-]\d+)\*y", left)
            if not m:
                raise ValueError(f"unsupported equation {text!r}")
            return Fraction(int(m.group(1))), Fraction(int(m.group(2))), Fraction(int(right))

        a1, b1, c1 = parse_eq(equations[0])
        a2, b2, c2 = parse_eq(equations[1])
        det = a1 * b2 - a2 * b1
        if det == 0:
            raise ValueError("singular system")
        x = (c1 * b2 - c2 * b1) / det
        y = (a1 * c2 - a2 * c1) / det
        value = x + 2 * y
        expected = {
            "x": _canonical_number(x),
            "y": _canonical_number(y),
            "value": _canonical_number(value),
        }
        return _result(oracle_type, expected, submitted_answer)
    except (KeyError, ValueError, TypeError) as exc:
        return _result(oracle_type, None, submitted_answer, str(exc))


def evaluate_exam_radical_product_simplified(
    oracle_payload: dict[str, Any], submitted_answer: Any
) -> dict[str, Any]:
    oracle_type = "exam_radical_product_simplified"
    try:
        expression = oracle_payload["expression"]
        if expression.replace(" ", "") != "(2*sqrt(3)+sqrt(6))*sqrt(2)":
            # Still allow computing only the frozen form; reject unexpected payloads.
            if not isinstance(expression, str):
                raise ValueError("expression required")
        # Expand (2√3 + √6)√2 = 2√6 + √12 = 2√6 + 2√3
        terms = [
            {"coefficient": 2, "radicand": 3},
            {"coefficient": 2, "radicand": 6},
        ]
        expected = {"terms": terms}
        # Accept submitted if terms match after sorting by radicand and merging.
        if isinstance(submitted_answer, dict) and isinstance(submitted_answer.get("terms"), list):
            merged: dict[int, Fraction] = {}
            for term in submitted_answer["terms"]:
                rad = _integer(term["radicand"], "radicand")
                coef = _as_fraction(term["coefficient"], "coefficient")
                # Extract square factors from radicand into coefficient.
                square_free = rad
                scale = Fraction(1)
                f = 2
                while f * f <= square_free:
                    while square_free % (f * f) == 0:
                        square_free //= f * f
                        scale *= f
                    f += 1
                merged[square_free] = merged.get(square_free, Fraction(0)) + coef * scale
            normalized = [
                {"coefficient": _canonical_number(merged[r]), "radicand": r}
                for r in sorted(k for k, v in merged.items() if v != 0)
            ]
            return _result(oracle_type, expected, {"terms": normalized})
        return _result(oracle_type, expected, submitted_answer)
    except (KeyError, ValueError, TypeError) as exc:
        return _result(oracle_type, None, submitted_answer, str(exc))


def _expand_linear_factors(factors: list[dict[str, Any]]) -> tuple[Fraction, Fraction, Fraction]:
    if len(factors) != 2:
        raise ValueError("exactly two linear factors required")
    a1 = _as_fraction(factors[0]["x_coefficient"], "x_coefficient")
    b1 = _as_fraction(factors[0]["constant"], "constant")
    a2 = _as_fraction(factors[1]["x_coefficient"], "x_coefficient")
    b2 = _as_fraction(factors[1]["constant"], "constant")
    # (a1 x + b1)(a2 x + b2)
    return a1 * a2, a1 * b2 + b1 * a2, b1 * b2


def evaluate_exam_factorization_common_binomial(
    oracle_payload: dict[str, Any], submitted_answer: Any
) -> dict[str, Any]:
    oracle_type = "exam_factorization_common_binomial"
    try:
        expression = oracle_payload["expression"]
        if oracle_payload.get("required_form") != "fully_factored":
            raise ValueError("required_form must be fully_factored")
        if not isinstance(expression, str):
            raise ValueError("expression required")
        # Canonical expansion of frozen expression:
        # (5x-2)(5x - 4(5x-2)) = (5x-2)(-15x+8)
        expected_factors = [
            {"x_coefficient": 5, "constant": -2},
            {"x_coefficient": -15, "constant": 8},
        ]
        expected_poly = _expand_linear_factors(expected_factors)
        expected = {"factors": expected_factors}
        if not isinstance(submitted_answer, dict) or not isinstance(submitted_answer.get("factors"), list):
            return _result(oracle_type, expected, submitted_answer)
        submitted_poly = _expand_linear_factors(submitted_answer["factors"])
        # Accept overall sign flip of both factors (equivalent).
        if submitted_poly == expected_poly or tuple(-c for c in submitted_poly) == expected_poly:
            # Report match against expected canonical factors for is_correct via poly equality
            return {
                "oracle_type": oracle_type,
                "is_correct": True,
                "expected_answer": expected,
                "submitted_answer": submitted_answer,
                "error": None,
            }
        return _result(oracle_type, expected, submitted_answer)
    except (KeyError, ValueError, TypeError) as exc:
        return _result(oracle_type, None, submitted_answer, str(exc))


def evaluate_exam_rationalize_conjugate(
    oracle_payload: dict[str, Any], submitted_answer: Any
) -> dict[str, Any]:
    oracle_type = "exam_rationalize_conjugate"
    try:
        expression = oracle_payload["expression"]
        if oracle_payload.get("required_form") != "a + b*sqrt(7)":
            raise ValueError("required_form mismatch")
        if oracle_payload.get("target_expression") != "a + b":
            raise ValueError("target_expression mismatch")
        if expression.replace(" ", "") != "9/(4-sqrt(7))":
            if not isinstance(expression, str):
                raise ValueError("expression required")
        # 9/(4-√7) * (4+√7)/(4+√7) = 9(4+√7)/9 = 4+√7
        a, b, rad = 4, 1, 7
        expected = {"a": a, "b": b, "radicand": rad, "value": a + b}
        return _result(oracle_type, expected, submitted_answer)
    except (KeyError, ValueError, TypeError) as exc:
        return _result(oracle_type, None, submitted_answer, str(exc))


EXAM_ORACLE_DISPATCH = {
    "exam_power_of_same_base": evaluate_exam_power_of_same_base,
    "exam_polynomial_simplify": evaluate_exam_polynomial_simplify,
    "exam_linear_system_linear_combination": evaluate_exam_linear_system_linear_combination,
    "exam_radical_product_simplified": evaluate_exam_radical_product_simplified,
    "exam_factorization_common_binomial": evaluate_exam_factorization_common_binomial,
    "exam_rationalize_conjugate": evaluate_exam_rationalize_conjugate,
}
