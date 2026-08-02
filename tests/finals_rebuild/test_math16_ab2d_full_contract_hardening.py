"""Ab2d+full domain API contract hardening: runtime ↔ SSOT ↔ return shapes."""
from __future__ import annotations

from fractions import Fraction

import pytest

from agent_tools.finals_rebuild.domain_api_ssot import validate_inventory
from agent_tools.finals_rebuild.math16_ab2d_full import TASK_ALLOWED_APIS
from core.prompts.domain_function_library import FractionOps, IntegerOps, PolynomialOps, RadicalOps


def test_inventory_still_valid():
    assert validate_inventory() == []


def test_fraction_create_rejects_bool_and_accepts_numeric():
    assert FractionOps.create(3) == Fraction(3, 1)
    assert FractionOps.create(-0.6) == Fraction(-3, 5)
    assert FractionOps.create("3/5") == Fraction(3, 5)
    with pytest.raises(ValueError, match="bool"):
        FractionOps.create(True)
    with pytest.raises(ValueError, match="bool"):
        FractionOps.create(False)
    with pytest.raises(ValueError):
        FractionOps.create([1, 2])  # type: ignore[arg-type]


def test_fraction_div_zero_and_to_exact_types():
    with pytest.raises(ValueError, match="Division by zero"):
        FractionOps.div(Fraction(1, 2), 0)
    with pytest.raises(ValueError, match="Division by zero"):
        FractionOps.div(Fraction(1, 2), Fraction(0))
    assert FractionOps.to_exact(Fraction(4, 2)) == 2
    assert FractionOps.to_exact(Fraction(3, 2)) == "3/2"
    assert isinstance(FractionOps.to_latex(Fraction(3, 5)), str)


def test_integer_is_divisible_policy():
    assert IntegerOps.is_divisible(156, 13) is True
    assert IntegerOps.is_divisible(10, 3) is False
    assert IntegerOps.is_divisible(5, 0) is False
    assert type(IntegerOps.is_divisible(5, 0)) is bool
    with pytest.raises(ValueError, match="non-bool int|int operands"):
        IntegerOps.is_divisible(True, 1)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="non-bool int|int operands"):
        IntegerOps.is_divisible(5, False)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="int operands"):
        IntegerOps.is_divisible(5.5, 1)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="int operands"):
        IntegerOps.is_divisible(5, 1.0)  # type: ignore[arg-type]


def test_simplify_term_rejects_negative_and_bool_radicand():
    assert RadicalOps.simplify_term(1, 12) == (2, 3)
    assert RadicalOps.simplify_term(1, 0) == (0, 1)
    assert RadicalOps.simplify_term(Fraction(1, 2), 12) == (Fraction(1), 3)
    with pytest.raises(ValueError, match="non-negative"):
        RadicalOps.simplify_term(1, -12)
    with pytest.raises(ValueError, match="non-bool int"):
        RadicalOps.simplify_term(1, True)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="non-bool int"):
        RadicalOps.simplify_term(1, 1.5)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="non-negative"):
        RadicalOps.simplify_term(1, Fraction(-1, 2))


def test_div_terms_zero_division_is_value_error():
    assert RadicalOps.div_terms(1, 35, 1, 5)[1] == 7
    with pytest.raises(ValueError, match="Division by zero"):
        RadicalOps.div_terms(1, 2, 0, 3)
    with pytest.raises(ValueError, match="Division by zero"):
        RadicalOps.div_terms(1, 2, 1, 0)


def test_formatters_return_str_and_predicates_return_bool():
    assert type(RadicalOps.format_term(3, 15)) is str
    assert type(RadicalOps.format_expression({1: 6, 3: -1})) is str
    assert type(
        RadicalOps.format_linear_radical(
            {"rational": 1, "radical_coefficient": 1, "radicand": 2}
        )
    ) is str
    assert type(PolynomialOps.format_latex([3, -2, 1])) is str
    assert type(FractionOps.to_latex(Fraction(1, 2))) is str
    assert type(IntegerOps.is_divisible(4, 2)) is bool


def test_polynomial_bool_and_empty_policy():
    assert PolynomialOps.normalize([]) == [0]
    assert PolynomialOps.normalize([0, 0]) == [0]
    assert PolynomialOps.mul([], [1, 2]) == [0]
    assert PolynomialOps.add([1, 2], [3]) == [1, 5]
    with pytest.raises(ValueError, match="bool"):
        PolynomialOps.mul([True, 1], [1, 1])  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="bool"):
        PolynomialOps.add([1], [False])  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="bool"):
        PolynomialOps.normalize([True, 1])  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="zero polynomial"):
        PolynomialOps.div_qr([1, 0], [0])


def test_exact_integer_and_linear_radical_shapes():
    assert RadicalOps.exact_integer(Fraction(4, 1)) == 4
    with pytest.raises(ValueError):
        RadicalOps.exact_integer(Fraction(3, 2))
    scaled = RadicalOps.scale_linear_radical(
        {"rational": 1, "radical_coefficient": 1, "radicand": 2}, 2
    )
    assert scaled == {"rational": 2, "radical_coefficient": 2, "radicand": 2}
    assert set(scaled) == {"rational", "radical_coefficient", "radicand"}


def test_ab2d_full_prompt_visible_apis_are_callable():
    """Every Ab2d+full routed API remains importable and returns documented core types."""
    visible = sorted({name for names in TASK_ALLOWED_APIS.values() for name in names})
    assert "FractionOps.create" in visible
    assert "IntegerOps.is_divisible" in visible
    assert "RadicalOps.simplify_term" in visible
    # Smoke: create + simplify_term + is_divisible still usable together for assembly.
    assert FractionOps.create("2/3") == Fraction(2, 3)
    assert RadicalOps.simplify_term(1, 8) == (2, 2)
    assert IntegerOps.is_divisible(12, 3) is True
