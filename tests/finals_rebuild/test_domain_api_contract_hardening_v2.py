from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

import pytest

from agent_tools.finals_rebuild.ce115_clean_incremental_ablation import TASK_DOMAIN_APIS, domain_section
from agent_tools.finals_rebuild.domain_answer_assembly import (
    TASK_OUTPUT_ASSEMBLY, compound_radical, exact_fraction, exact_int,
    polynomial_coefficients, radical_term,
)
from agent_tools.finals_rebuild.domain_api_ssot import (
    API_CLASSIFICATION, DOMAIN_API_SSOT, SUPPORTED_PUBLIC,
    render_api_prompt_line, render_supported_api_reference, runtime_public_inventory,
    validate_inventory,
)
from agent_tools.finals_rebuild.math16_pool import load_pool_manifest
from core.prompts.domain_function_library import FractionOps, IntegerOps, PolynomialOps, RadicalOps


def test_inventory_has_exactly_49_classified_public_apis():
    assert len(runtime_public_inventory()) == 49
    assert len(API_CLASSIFICATION) == 49
    assert validate_inventory() == []
    assert set(DOMAIN_API_SSOT) == {n for n, c in API_CLASSIFICATION.items() if c == SUPPORTED_PUBLIC}


def test_every_routed_api_is_supported_and_rendered_from_ssot():
    for task_id, apis in TASK_DOMAIN_APIS.items():
        for api in apis:
            name = api["name"]
            assert API_CLASSIFICATION[name] == SUPPORTED_PUBLIC
            assert render_api_prompt_line(name) in domain_section(task_id)


def test_safe_eval_supported_return_domain_and_exact_int_boundary():
    assert IntegerOps.safe_eval("2+3") == 5
    assert type(IntegerOps.safe_eval("5/2")) is float
    with pytest.raises(ValueError, match="int or float"):
        IntegerOps.safe_eval("1 == 1")
    with pytest.raises(ValueError, match="int or float"):
        IntegerOps.safe_eval("(1, 2)")
    assert exact_int(5) == 5
    for bad in (True, 5.0, Fraction(5, 1)):
        with pytest.raises(TypeError):
            exact_int(bad)


def test_fraction_pipeline_and_json_adapters():
    values = [
        FractionOps.create("1/2"),
        FractionOps.add(Fraction(1, 2), Fraction(1, 3)),
        FractionOps.sub(Fraction(1, 2), Fraction(1, 3)),
        FractionOps.mul(Fraction(1, 2), Fraction(1, 3)),
        FractionOps.div(Fraction(1, 2), Fraction(1, 3)),
        FractionOps.from_parts(6, 3),
    ]
    assert all(isinstance(v, Fraction) for v in values)
    assert FractionOps.to_exact(Fraction(6, 3)) == 2
    assert FractionOps.to_exact(Fraction(3, 2)) == "3/2"
    with pytest.raises(TypeError):
        json.dumps(Fraction(1, 2))
    payload = exact_fraction(Fraction(3, 2))
    assert json.loads(json.dumps(payload)) == payload


def test_polynomial_mul_operand_dependent_types_and_normalization():
    ints = PolynomialOps.mul([3, 2], [13, -7])
    floats = PolynomialOps.mul([0.5, 1.0], [2.0])
    fractions = PolynomialOps.mul([Fraction(1, 2), 1], [2])
    assert ints == [39, 5, -14] and all(type(x) is int for x in ints)
    assert floats == [1.0, 2.0] and all(type(x) is float for x in floats)
    assert fractions == [Fraction(1), 2]
    assert polynomial_coefficients(fractions) == [1, 2]
    assert json.loads(json.dumps(polynomial_coefficients(fractions))) == [1, 2]


def test_polynomial_exact_structures_and_ordering():
    q, r = PolynomialOps.div_qr([6, 0, 6], [1, -4])
    assert (q, r) == ([6, 24], [102])
    factors = PolynomialOps.factor_quadratic_exact(1, 4, -12)
    assert len(factors) == 2
    assert all(list(f) == ["x_coefficient", "constant"] for f in factors)
    assert json.loads(json.dumps(factors)) == factors
    coeffs = PolynomialOps.coeffs_from_py_expression("(x+1)*(x-1)")
    assert coeffs == [Fraction(1), Fraction(0), Fraction(-1)]
    assert list(PolynomialOps.to_degree_map(coeffs)) == ["2", "1", "0"]


def test_radical_semantics_are_separate_from_presentation():
    assert RadicalOps.simplify_term(Fraction(1, 2), 12) == (Fraction(1), 3)
    assert radical_term(3, 15) == {"coefficient": 3, "radicand": 15, "canonical_latex": r"3\sqrt{15}"}
    result = compound_radical(6, -1, 3)
    assert result == {"rational": 6, "radical_coefficient": -1, "radicand": 3, "canonical_latex": r"6 - \sqrt{3}"}
    assert r"\sqrt{(3,15)}" not in RadicalOps.format_term(3, 15)
    with pytest.raises((TypeError, ValueError)):
        radical_term(1, (3, 15))  # type: ignore[arg-type]


def test_all_math16_tasks_have_explicit_output_assembly_and_json_roundtrip():
    manifest = load_pool_manifest()
    ids = {t["task_id"] for t in manifest["tasks"]}
    assert set(TASK_OUTPUT_ASSEMBLY) == ids
    for task in manifest["tasks"]:
        assert json.loads(json.dumps(task["correct_answer"], ensure_ascii=False)) == task["correct_answer"]


def test_generated_reference_contains_exact_prompt_lines():
    doc = render_supported_api_reference()
    assert "Generated from domain_api_ssot.py" in doc
    for name in DOMAIN_API_SSOT:
        assert render_api_prompt_line(name) in doc
    skill = (Path(__file__).resolve().parents[2] / "agent_skills/domain_api_contract_v2/SKILL.md").read_text(encoding="utf-8")
    assert doc in skill
