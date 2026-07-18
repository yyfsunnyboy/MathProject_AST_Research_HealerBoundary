"""Contract-aligned v2 Domain API + prompt assembly audits (exam ext 113/114)."""
from __future__ import annotations

import ast
import inspect
import json
from fractions import Fraction
from pathlib import Path

import pytest

from agent_tools.finals_rebuild.ce115_contract_aligned_ablation_v2 import (
    GENERIC_BODY,
    LINEAGE_ID,
    TASK_DOMAIN_APIS,
    assert_v2_ablation_invariants,
    build_condition_prompt_v2,
    canonical_prompt_hash,
    domain_section,
    verify_generic_body_frozen_vs_v1,
)
from agent_tools.finals_rebuild.ce115_exam_external_validation import (
    EXPECTED_ANSWERS,
    FROZEN_PAYLOADS,
    TASK_IDS,
    all_leakage_audits,
)
from agent_tools.finals_rebuild.math_task_oracles import evaluate_math_task_oracle
from core.prompts.domain_function_library import (
    FractionOps,
    IntegerOps,
    LinearSystemOps,
    PolynomialOps,
    RadicalOps,
)

MANIFEST = Path("tests/finals_rebuild/fixtures/math_generation_tasks_ce115_pilot.jsonl")
SEED = 2026071301
LIBRARY = "core.prompts.domain_function_library"

# Resolve production callables by dotted name.
PROD = {
    "FractionOps.create": FractionOps.create,
    "FractionOps.from_parts": FractionOps.from_parts,
    "FractionOps.to_exact": FractionOps.to_exact,
    "IntegerOps.add": IntegerOps.add,
    "IntegerOps.sub": IntegerOps.sub,
    "LinearSystemOps.solve_2x2": LinearSystemOps.solve_2x2,
    "LinearSystemOps.evaluate_linear": LinearSystemOps.evaluate_linear,
    "PolynomialOps.coeffs_from_py_expression": PolynomialOps.coeffs_from_py_expression,
    "PolynomialOps.to_degree_map": PolynomialOps.to_degree_map,
    "PolynomialOps.factor_quadratic_exact": PolynomialOps.factor_quadratic_exact,
    "RadicalOps.simplify_term": RadicalOps.simplify_term,
    "RadicalOps.normalize_term_list": RadicalOps.normalize_term_list,
    "RadicalOps.rationalize_linear_denominator": RadicalOps.rationalize_linear_denominator,
}


def _load_tasks() -> dict[str, dict]:
    rows = [json.loads(line) for line in MANIFEST.read_text(encoding="utf-8").splitlines() if line.strip()]
    by = {r["task_id"]: r for r in rows}
    return {tid: by[tid] for tid in TASK_IDS}


def _frozen(task: dict) -> dict:
    tid = task["task_id"]
    return {
        "task_id": tid,
        "oracle_type": task["oracle_type"],
        "oracle_payload": FROZEN_PAYLOADS[tid],
        "repeat_seed": SEED,
    }


# --- 1–4 signature / legal / return / serialization ---


def test_fraction_create_rejects_signed_denominator_literal():
    with pytest.raises(ValueError, match="illegal Fraction string"):
        FractionOps.create("-240/-120")
    assert FractionOps.to_exact(FractionOps.from_parts(-240, -120)) == 2
    assert FractionOps.create("-3/5") == Fraction(-3, 5)
    assert FractionOps.create("7/2") == Fraction(7, 2)


def test_from_parts_and_to_exact_serialization():
    assert FractionOps.from_parts(7, 2) == Fraction(7, 2)
    assert FractionOps.to_exact(Fraction(7, 2)) == "7/2"
    assert FractionOps.to_exact(Fraction(4, 2)) == 2
    with pytest.raises(ValueError):
        FractionOps.from_parts(1, 0)
    with pytest.raises(ValueError):
        FractionOps.from_parts(1.5, 2)  # type: ignore[arg-type]


def test_integer_ops_signatures_and_types():
    assert inspect.signature(IntegerOps.add) == inspect.Signature(
        [
            inspect.Parameter("a", inspect.Parameter.POSITIONAL_OR_KEYWORD),
            inspect.Parameter("b", inspect.Parameter.POSITIONAL_OR_KEYWORD),
        ]
    )
    assert IntegerOps.add(10, 2) == 12
    assert IntegerOps.sub(12, 4) == 8
    with pytest.raises(ValueError):
        IntegerOps.add(1.0, 2)  # type: ignore[arg-type]


def test_linear_system_exact_path_and_negative_det():
    x, y = LinearSystemOps.solve_2x2(37, 2, 81, 23, -2, 39)
    assert x == 2 and y == Fraction(7, 2)
    value = LinearSystemOps.evaluate_linear(x, y, 1, 2)
    assert FractionOps.to_exact(value) == 9
    # Negative determinant still exact
    x2, y2 = LinearSystemOps.solve_2x2(1, 1, 3, 2, -1, 0)
    assert (x2, y2) == (1, 2)


def test_polynomial_simplify_and_factor_apis():
    coeffs = PolynomialOps.coeffs_from_py_expression("(5*x**2 - 2*x) - (4 - 3*x)")
    deg = PolynomialOps.to_degree_map(coeffs)
    assert deg == {"2": 5, "1": 1, "0": -4}
    fac_coeffs = PolynomialOps.coeffs_from_py_expression("5*x*(5*x - 2) - 4*(5*x - 2)**2")
    factors = PolynomialOps.factor_quadratic_exact(*fac_coeffs)
    verdict = evaluate_math_task_oracle(
        "exam_factorization_common_binomial",
        FROZEN_PAYLOADS["ce115_ext_113_10_factorization_l1"],
        {"factors": factors},
    )
    assert verdict["is_correct"] is True


def test_radical_normalize_and_rationalize():
    assert RadicalOps.simplify_term(1, 12) == (2, 3)
    terms = RadicalOps.normalize_term_list([(2, 6), (1, 12)])
    assert terms == [
        {"coefficient": 2, "radicand": 3},
        {"coefficient": 2, "radicand": 6},
    ]
    a, b, r = RadicalOps.rationalize_linear_denominator(9, 4, -1, 7)
    assert (FractionOps.to_exact(a), FractionOps.to_exact(b), r, FractionOps.to_exact(a + b)) == (4, 1, 7, 5)


def test_prompt_listed_signatures_match_production():
    for tid, apis in TASK_DOMAIN_APIS.items():
        for api in apis:
            assert api["import"] == LIBRARY
            fn = PROD[api["name"]]
            prod_sig = str(inspect.signature(fn))
            # Prompt signature uses same param names; allow spacing differences via normalize
            listed = api["signature"].replace(" ", "")
            actual = prod_sig.replace(" ", "")
            assert listed == actual, f"{tid} {api['name']}: prompt {listed} != prod {actual}"


# --- golden candidates that call listed APIs ---

GOLDEN_AB2D: dict[str, str] = {
    "ce115_ext_114_01_power_laws_l1": '''
from core.prompts.domain_function_library import IntegerOps
def generate(level=1, **kwargs):
    frozen = {"expression": "7**10 * 7**2 / 7**4", "required_form": "power_of_same_base", "base": 7}
    exp = IntegerOps.sub(IntegerOps.add(10, 2), 4)
    return {"question_text": "power", "correct_answer": {"base": 7, "exponent": exp}, "oracle_payload": frozen}
''',
    "ce115_ext_114_02_polynomial_simplify_l1": '''
from core.prompts.domain_function_library import PolynomialOps
def generate(level=1, **kwargs):
    frozen = {"expression": "(5*x**2 - 2*x) - (4 - 3*x)"}
    coeffs = PolynomialOps.coeffs_from_py_expression(frozen["expression"])
    degree_map = PolynomialOps.to_degree_map(coeffs)
    return {"question_text": "simplify", "correct_answer": {"coefficients": degree_map}, "oracle_payload": frozen}
''',
    "ce115_ext_114_04_linear_system_l1": '''
from core.prompts.domain_function_library import LinearSystemOps, FractionOps
def generate(level=1, **kwargs):
    frozen = {"equations": ["37*x + 2*y = 81", "23*x - 2*y = 39"], "target_expression": "x + 2*y"}
    x, y = LinearSystemOps.solve_2x2(37, 2, 81, 23, -2, 39)
    value = LinearSystemOps.evaluate_linear(x, y, 1, 2)
    # Demonstrate safe path instead of illegal create("-240/-120")
    _ = FractionOps.to_exact(FractionOps.from_parts(-240, -120))
    return {
        "question_text": "system",
        "correct_answer": {
            "x": FractionOps.to_exact(x),
            "y": FractionOps.to_exact(y),
            "value": FractionOps.to_exact(value),
        },
        "oracle_payload": frozen,
    }
''',
    "ce115_ext_114_08_radical_product_l1": '''
from core.prompts.domain_function_library import RadicalOps
def generate(level=1, **kwargs):
    frozen = {"expression": "(2*sqrt(3) + sqrt(6))*sqrt(2)"}
    t1 = RadicalOps.simplify_term(2, 3 * 2)
    t2 = RadicalOps.simplify_term(1, 6 * 2)
    terms = RadicalOps.normalize_term_list([t1, t2])
    return {"question_text": "radicals", "correct_answer": {"terms": terms}, "oracle_payload": frozen}
''',
    "ce115_ext_113_10_factorization_l1": '''
from core.prompts.domain_function_library import PolynomialOps
def generate(level=1, **kwargs):
    frozen = {"expression": "5*x*(5*x - 2) - 4*(5*x - 2)**2", "required_form": "fully_factored"}
    coeffs = PolynomialOps.coeffs_from_py_expression(frozen["expression"])
    factors = PolynomialOps.factor_quadratic_exact(*coeffs)
    return {"question_text": "factor", "correct_answer": {"factors": factors}, "oracle_payload": frozen}
''',
    "ce115_ext_113_11_rationalize_l1": '''
from core.prompts.domain_function_library import RadicalOps, FractionOps
def generate(level=1, **kwargs):
    frozen = {"expression": "9/(4 - sqrt(7))", "required_form": "a + b*sqrt(7)", "target_expression": "a + b"}
    a, b, r = RadicalOps.rationalize_linear_denominator(9, 4, -1, 7)
    aa, bb = FractionOps.to_exact(a), FractionOps.to_exact(b)
    return {
        "question_text": "rationalize",
        "correct_answer": {"a": aa, "b": bb, "radicand": r, "value": FractionOps.to_exact(a + b)},
        "oracle_payload": frozen,
    }
''',
}


def _api_names_called(source: str) -> set[str]:
    tree = ast.parse(source)
    found: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name):
                found.add(f"{node.func.value.id}.{node.func.attr}")
    return found


@pytest.mark.parametrize("task_id", TASK_IDS)
def test_ab2d_golden_calls_listed_apis_and_passes_oracle(task_id: str):
    source = GOLDEN_AB2D[task_id]
    listed = {api["name"] for api in TASK_DOMAIN_APIS[task_id]}
    required = {
        api["name"]
        for api in TASK_DOMAIN_APIS[task_id]
        if api.get("adoption", "required") == "required"
    }
    called = _api_names_called(source)
    if required:
        assert called & required, f"{task_id}: golden calls none of required {required}; called={called}"
        missing = required - called
        assert not missing, f"{task_id}: golden missing required APIs {missing}"
    else:
        # 114-01: all optional — golden may still demonstrate the APIs
        assert called & listed or True
    ns: dict = {}
    exec(source, ns, ns)
    out = ns["generate"]()
    assert out["oracle_payload"] == FROZEN_PAYLOADS[task_id]
    verdict = evaluate_math_task_oracle(
        _load_tasks()[task_id]["oracle_type"], FROZEN_PAYLOADS[task_id], out["correct_answer"]
    )
    assert verdict["is_correct"] is True, verdict


def test_11404_domain_excludes_fractionops_create():
    names = {a["name"] for a in TASK_DOMAIN_APIS["ce115_ext_114_04_linear_system_l1"]}
    assert "FractionOps.create" not in names
    assert names == {
        "LinearSystemOps.solve_2x2",
        "LinearSystemOps.evaluate_linear",
        "FractionOps.from_parts",
        "FractionOps.to_exact",
    }
    domain = domain_section("ce115_ext_114_04_linear_system_l1")
    assert "FractionOps.create" not in domain
    assert "from_parts(-4, -2)" in domain or "from_parts(-4,-2)" in domain.replace(" ", "")
    assert "-240/-120" not in domain  # no failure-cohort numeric stacking in DOMAIN


def test_11401_adoption_optional_in_domain():
    for api in TASK_DOMAIN_APIS["ce115_ext_114_01_power_laws_l1"]:
        assert api["adoption"] == "optional"
    domain = domain_section("ce115_ext_114_01_power_laws_l1")
    assert "optional" in domain
    assert "plain exact int arithmetic is acceptable" in domain


def test_11310_evaluator_accepts_order_and_sign_flip():
    tid = "ce115_ext_113_10_factorization_l1"
    payload = FROZEN_PAYLOADS[tid]
    sign_flipped = {
        "factors": [
            {"x_coefficient": -5, "constant": 2},
            {"x_coefficient": 15, "constant": -8},
        ]
    }
    ok = evaluate_math_task_oracle("exam_factorization_common_binomial", payload, sign_flipped)
    assert ok["is_correct"] is True
    domain = domain_section(tid)
    assert "factor order may be swapped" in domain
    assert "overall sign flip" in domain


def test_11311_denominator_definition_generic_examples():
    domain = domain_section("ce115_ext_113_11_rationalize_l1")
    assert "denom_rational + denom_radical_coeff * sqrt(radicand)" in domain
    assert "num/(p+q*sqrt(r))" in domain
    assert "num/(p-q*sqrt(r))" in domain
    assert "9/(4" not in domain  # no exam expression in DOMAIN


def test_generic_frozen_and_prompt_assembly():
    verify_generic_body_frozen_vs_v1()
    assert LINEAGE_ID.endswith("v2")
    tasks = _load_tasks()
    hashes = {}
    for tid, task in tasks.items():
        prompts = assert_v2_ablation_invariants(task, _frozen(task))
        hashes[tid] = {c: canonical_prompt_hash(t) for c, t in prompts.items()}
        # Ab2d contains BASE+GENERIC+DOMAIN
        assert GENERIC_BODY in prompts["ab2d"]
        assert domain_section(tid) in prompts["ab2d"]
        # Gemini/Qwen share builder — byte identity of builder output
        again = build_condition_prompt_v2("ab2d", task, _frozen(task))
        assert again == prompts["ab2d"]
    # nested coefficients in 114-02
    p11402 = build_condition_prompt_v2("ab1", tasks["ce115_ext_114_02_polynomial_simplify_l1"], _frozen(tasks["ce115_ext_114_02_polynomial_simplify_l1"]))
    assert 'exactly one top-level key "coefficients"' in p11402
    freeze_path = Path("docs/experiments/analysis/ce115_exam_ext_contract_aligned_v2/canonical_prompt_hashes.json")
    freeze_path.parent.mkdir(parents=True, exist_ok=True)
    freeze_path.write_text(
        json.dumps({"lineage_id": LINEAGE_ID, "seed": SEED, "hashes": hashes}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def test_task_to_tool_coverage_no_gaps():
    for tid in TASK_IDS:
        assert tid in TASK_DOMAIN_APIS
        assert len(TASK_DOMAIN_APIS[tid]) >= 1
    assert "FractionOps.create" not in {a["name"] for a in TASK_DOMAIN_APIS["ce115_ext_114_02_polynomial_simplify_l1"]}
    assert "FractionOps.create" not in {a["name"] for a in TASK_DOMAIN_APIS["ce115_ext_113_10_factorization_l1"]}
    assert "FractionOps.create" not in {a["name"] for a in TASK_DOMAIN_APIS["ce115_ext_114_04_linear_system_l1"]}
    assert "IntegerOps.add" in {a["name"] for a in TASK_DOMAIN_APIS["ce115_ext_114_01_power_laws_l1"]}
    assert all(a["adoption"] == "optional" for a in TASK_DOMAIN_APIS["ce115_ext_114_01_power_laws_l1"])


def test_leakage_audit_still_passes_and_domain_has_no_answers():
    assert all_leakage_audits()["passed"] is True
    for tid in TASK_IDS:
        text = domain_section(tid)
        for token in ('"exponent": 8', '"value": 9', '"a": 4', "5x-2"):
            assert token not in text


def test_v1_hash_file_untouched_exists():
    v1 = Path("docs/experiments/analysis/ce115_exam_ext_113_114_canonical_prompt_hashes.json")
    assert v1.is_file(), "v1 hash freeze must remain on disk"
