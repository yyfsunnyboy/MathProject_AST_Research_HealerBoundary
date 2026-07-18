"""Math16-LaTeX-v1 frozen pool: 16 tasks, semantic-equivalent LaTeX standardization.

All 16 items are fully frozen fixed identities for this pool. Existing CE115 L1
source stems are preserved as provenance only; model-facing stems are LaTeX.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

POOL_ID = "Math16-LaTeX-v1"
POOL_MANIFEST_VERSION = "math16_latex_v1.pool_manifest"
MANIFEST_REL = Path("docs/experiments/manifests/math16_latex_v1_pool_manifest.json")
EXISTING4_FREEZE_REL = Path("docs/experiments/manifests/math16_existing4_formal_freeze.json")
SEED = 2026071301
GIT_HEAD_AT_FREEZE = "6107ac7a3cc46d7d41d6e373ef191ac278f2fe98"

PRESENTATION_TRANSFORM = {
    "type": "semantic_equivalent_latex_standardization",
    "changes_semantics": False,
}

DOMAIN_OPS = ("PolynomialOps", "IntegerOps", "FractionOps", "RadicalOps")


def _sha(obj: Any) -> str:
    return hashlib.sha256(
        json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _task(
    *,
    task_id: str,
    domain: str,
    domain_ops: str,
    skill_id: str,
    oracle_type: str,
    source_question_text: str,
    math16_question_text: str,
    frozen_params: dict[str, Any],
    oracle_payload: dict[str, Any],
    correct_answer: Any,
    source: str,
    pool_role: str,
    year_source: str | None = None,
    canonical_latex: str | None = None,
    reuse_policy: str = "math16_latex_v1_rerun",
    provenance: dict[str, Any] | None = None,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    row: dict[str, Any] = {
        "task_id": task_id,
        "domain": domain,
        "domain_ops": domain_ops,
        "skill_id": skill_id,
        "oracle_type": oracle_type,
        "difficulty_level": 1,
        "difficulty_label": "basic",
        "pool_role": pool_role,
        "reuse_policy": reuse_policy,
        "source_question_text": source_question_text,
        "math16_question_text": math16_question_text,
        "actual_question_text": math16_question_text,
        "presentation_transform": dict(PRESENTATION_TRANSFORM),
        "frozen_params": frozen_params,
        "oracle_payload": oracle_payload,
        "correct_answer": correct_answer,
        "canonical_latex": canonical_latex,
        "source": source,
        "version": POOL_MANIFEST_VERSION,
        "seed": SEED if pool_role == "existing_formal_ce115_l1" else None,
        "year_source": year_source,
        "held_out": False,
        "required_entry_point": "generate",
        "required_output_keys": ["question_text", "correct_answer", "oracle_payload"],
        "parameter_ranges": {
            key: {"allowed_values": [value]} for key, value in frozen_params.items()
        },
        "provenance": provenance or {},
    }
    if extra:
        row.update(extra)
    row["freeze_record_sha256"] = _sha(
        {
            "task_id": task_id,
            "source_question_text": source_question_text,
            "math16_question_text": math16_question_text,
            "frozen_params": frozen_params,
            "oracle_payload": oracle_payload,
            "correct_answer": correct_answer,
            "canonical_latex": canonical_latex,
            "presentation_transform": PRESENTATION_TRANSFORM,
        }
    )
    return row


def build_pool_tasks() -> list[dict[str, Any]]:
    existing = [
        _task(
            task_id="ce115_calc_polynomial_division_l1",
            domain="polynomials",
            domain_ops="PolynomialOps",
            skill_id="math16_polynomial_division_general",
            oracle_type="math16_polynomial_division_general",
            source_question_text=(
                "Divide (6x^2 + 6) by (x - 4). Report the quotient and remainder polynomials."
            ),
            math16_question_text=(
                "將多項式\n\\[\n6x^2+6\n\\]\n除以\n\\[\nx-4,\n\\]\n求商式與餘式。"
            ),
            frozen_params={
                "dividend_coefficients": [6, 0, 6],
                "divisor_coefficients": [1, -4],
            },
            oracle_payload={
                "dividend_coefficients": [6, 0, 6],
                "divisor_coefficients": [1, -4],
            },
            correct_answer={
                "quotient_coefficients": [6, 24],
                "remainder_coefficients": [102],
                "quotient_latex": "6x+24",
                "remainder_latex": "102",
            },
            canonical_latex=None,
            source="FORMAL_L1 / ce115_calc_main_experiment_manifest.v1",
            pool_role="existing_formal_ce115_l1",
            provenance={
                "source_identity": "ce115_calc_polynomial_division_l1",
                "source_experiment_manifest": (
                    "docs/experiments/manifests/ce115_calc_main_experiment_manifest.json"
                ),
                "source_task_manifest": (
                    "tests/finals_rebuild/fixtures/math_generation_tasks_ce115_pilot.jsonl"
                ),
            },
        ),
        _task(
            task_id="ce115_calc_polynomial_factor_roots_l1",
            domain="polynomials",
            domain_ops="PolynomialOps",
            skill_id="math16_polynomial_factor_roots",
            oracle_type="math16_polynomial_factor_roots",
            source_question_text=(
                "Factor the quadratic x^2 + 4x - 12 = 0 over the rationals and find both "
                "distinct roots in ascending numeric order."
            ),
            math16_question_text=(
                "將一元二次方程式\n\\[\nx^2+4x-12=0\n\\]\n"
                "的左式在有理數範圍內因式分解，並依數值由小到大列出兩個相異實根。"
            ),
            frozen_params={"quadratic_coefficients": [1, 4, -12]},
            oracle_payload={"quadratic_coefficients": [1, 4, -12]},
            correct_answer={
                "roots": [-6, 2],
                "factorization_latex": "(x+6)(x-2)=0",
                "roots_latex": r"[-6,\,2]",
            },
            source="FORMAL_L1 / ce115_calc_main_experiment_manifest.v1",
            pool_role="existing_formal_ce115_l1",
            provenance={
                "source_identity": "ce115_calc_polynomial_factor_roots_l1",
                "source_experiment_manifest": (
                    "docs/experiments/manifests/ce115_calc_main_experiment_manifest.json"
                ),
            },
        ),
        _task(
            task_id="ce115_calc_exact_rational_expression_l1",
            domain="rational_arithmetic",
            domain_ops="FractionOps",
            skill_id="math16_exact_rational_expression",
            oracle_type="math16_exact_rational_expression",
            source_question_text="Evaluate the exact value of 2.79×89.3 − (-0.21×89.3).",
            math16_question_text=(
                "精確計算\n\\[\n"
                r"2.79\times 89.3-\left(-0.21\times 89.3\right)."
                "\n\\]\n答案不得使用近似值。"
            ),
            frozen_params={
                "products": [
                    {"sign": 1, "left": "2.79", "right": "89.3"},
                    {"sign": -1, "left": "-0.21", "right": "89.3"},
                ]
            },
            oracle_payload={
                "products": [
                    {"sign": 1, "left": "2.79", "right": "89.3"},
                    {"sign": -1, "left": "-0.21", "right": "89.3"},
                ]
            },
            correct_answer={
                "value": "2679/10",
                "canonical_latex": r"\frac{2679}{10}",
            },
            canonical_latex=r"\frac{2679}{10}",
            source="FORMAL_L1 / ce115_calc_main_experiment_manifest.v1",
            pool_role="existing_formal_ce115_l1",
            provenance={"source_identity": "ce115_calc_exact_rational_expression_l1"},
        ),
        _task(
            task_id="ce115_calc_radical_simplification_l1",
            domain="radicals",
            domain_ops="RadicalOps",
            skill_id="math16_radical_simplification",
            oracle_type="math16_radical_simplification",
            source_question_text=(
                "Rewrite √27 in simplest radical form a√b, where b is square-free "
                "and a is a positive integer."
            ),
            math16_question_text=(
                "將\n\\[\n\\sqrt{27}\n\\]\n"
                "化為最簡根式 \\(a\\sqrt{b}\\)，其中 \\(a\\) 為正整數，"
                "且 \\(b\\) 不含大於 \\(1\\) 的完全平方因數。"
            ),
            frozen_params={"radicand": 27},
            oracle_payload={"radicand": 27},
            correct_answer={
                "coefficient": 3,
                "radicand": 3,
                "canonical_latex": r"3\sqrt{3}",
            },
            canonical_latex=r"3\sqrt{3}",
            source="FORMAL_L1 / ce115_calc_main_experiment_manifest.v1",
            pool_role="existing_formal_ce115_l1",
            provenance={"source_identity": "ce115_calc_radical_simplification_l1"},
        ),
    ]

    new12 = [
        _task(
            task_id="ce111_q02_polynomial_division_remainder",
            domain="polynomials",
            domain_ops="PolynomialOps",
            skill_id="math16_polynomial_division_remainder_only",
            oracle_type="polynomial_division_remainder_only",
            source_question_text=r"計算多項式 \(6x^2+4x\) 除以 \(2x^2\) 所得的餘式。",
            math16_question_text=r"計算多項式 \(6x^2+4x\) 除以 \(2x^2\) 所得的餘式。",
            frozen_params={
                "dividend_coefficients": [6, 4, 0],
                "divisor_coefficients": [2, 0, 0],
            },
            oracle_payload={
                "quotient": 3,
                "remainder": "4x",
                "remainder_canonical_latex": "4x",
            },
            correct_answer={"remainder": "4x", "canonical_latex": "4x"},
            canonical_latex="4x",
            source="111年國中教育會考數學試題第2題（formalized fixed item）",
            pool_role="math16_new_fixed_item",
            year_source="111",
            provenance={"item": "2", "exam_year": "111"},
        ),
        _task(
            task_id="ce111_q08_polynomial_factor_parameter_recovery",
            domain="polynomials",
            domain_ops="PolynomialOps",
            skill_id="math16_polynomial_factor_parameter_recovery",
            oracle_type="polynomial_factor_parameter_recovery",
            source_question_text=(
                "已知\n\\[\n39x^2+5x-14=(3x+a)(bx+c),\n\\]\n"
                "其中 \\(a,b,c\\) 均為整數，求 \\(a+2c\\)。"
            ),
            math16_question_text=(
                "已知\n\\[\n39x^2+5x-14=(3x+a)(bx+c),\n\\]\n"
                "其中 \\(a,b,c\\) 均為整數，求 \\(a+2c\\)。"
            ),
            frozen_params={
                "quadratic_coefficients": [39, 5, -14],
                "template_left_x_coefficient": 3,
                "factor_order_policy": "strict_source_template",
            },
            oracle_payload={
                "a": 2,
                "b": 13,
                "c": -7,
                "expanded_check": [39, 5, -14],
            },
            correct_answer=-12,
            source="111年國中教育會考數學試題第8題（formalized fixed item）",
            pool_role="math16_new_fixed_item",
            year_source="111",
            extra={"factor_order_policy": "strict_source_template"},
            provenance={
                "item": "8",
                "exam_year": "111",
                "correct_parameters": {"a": 2, "b": 13, "c": -7, "answer": -12},
                "forbidden_legacy_wrong_values": {"a": -2, "c": 7, "answer": 12},
                "factor_order_policy": "strict_source_template",
            },
        ),
        _task(
            task_id="ce111_q03_prime_factor_selection",
            domain="integers",
            domain_ops="IntegerOps",
            skill_id="math16_prime_factor_selection",
            oracle_type="integer_exact",
            source_question_text=(
                r"下列整數 \(11,12,13,14\) 中，哪一個是 \(156\) 的質因數？"
            ),
            math16_question_text=(
                r"下列整數 \(11,12,13,14\) 中，哪一個是 \(156\) 的質因數？"
            ),
            frozen_params={"candidates": [11, 12, 13, 14], "n": 156},
            oracle_payload={"prime_factors_of_n": [2, 3, 13], "selected": 13},
            correct_answer=13,
            source="111年國中教育會考數學試題第3題（easy positive control）",
            pool_role="math16_new_fixed_item",
            year_source="111",
            provenance={"item": "3", "exam_year": "111", "role": "easy_positive_control"},
        ),
        _task(
            task_id="ce112_q01_negative_integer_power",
            domain="integers",
            domain_ops="IntegerOps",
            skill_id="math16_negative_integer_power",
            oracle_type="integer_exact",
            source_question_text="計算\n\\[\n(-3)^3.\n\\]",
            math16_question_text="計算\n\\[\n(-3)^3.\n\\]",
            frozen_params={"base": -3, "exponent": 3},
            oracle_payload={"base": -3, "exponent": 3, "value": -27},
            correct_answer=-27,
            source="112年國中教育會考數學試題第1題（easy positive control）",
            pool_role="math16_new_fixed_item",
            year_source="112",
            provenance={"item": "1", "exam_year": "112", "role": "easy_positive_control"},
        ),
        _task(
            task_id="ce112_q09_divisor_multiple_intersection",
            domain="integers",
            domain_ops="IntegerOps",
            skill_id="math16_divisor_multiple_intersection",
            oracle_type="integer_count",
            source_question_text=(
                r"有多少個正整數同時是 \(18\) 的倍數，也是 \(216\) 的因數？"
            ),
            math16_question_text=(
                r"有多少個正整數同時是 \(18\) 的倍數，也是 \(216\) 的因數？"
            ),
            frozen_params={"multiple_of": 18, "divisor_of": 216},
            oracle_payload={"valid_values": [18, 36, 54, 72, 108, 216]},
            correct_answer={"count": 6},
            source="112年國中教育會考數學試題第9題（formalized fixed item）",
            pool_role="math16_new_fixed_item",
            year_source="112",
            provenance={"item": "9", "exam_year": "112"},
        ),
        _task(
            task_id="ce111_nonchoice_q01_part1_exponential_growth",
            domain="integers",
            domain_ops="IntegerOps",
            skill_id="math16_exponential_growth_generation_count",
            oracle_type="integer_exact_k",
            source_question_text=(
                r"從 \(1\) 個細胞開始培養。每經過 \(20\) 小時，每個細胞分裂成 \(4\) 個，"
                r"且新細胞仍依相同規則繼續分裂。經過 \(15\) 天後，細胞總數可寫成 \(4^k\)，求 \(k\)。"
            ),
            math16_question_text=(
                r"從 \(1\) 個細胞開始培養。每經過 \(20\) 小時，每個細胞分裂成 \(4\) 個，"
                r"且新細胞仍依相同規則繼續分裂。經過 \(15\) 天後，細胞總數可寫成 \(4^k\)，求 \(k\)。"
            ),
            frozen_params={
                "initial": 1,
                "split_factor": 4,
                "hours_per_generation": 20,
                "days": 15,
            },
            oracle_payload={"total_hours": 360, "generation_count": 18},
            correct_answer={"k": 18},
            source="111年非選擇題第1題第1小題（formalized fixed item）",
            pool_role="math16_new_fixed_item",
            year_source="111",
            provenance={"item": "nonchoice_01_part1", "exam_year": "111"},
        ),
        _task(
            task_id="ce111_q05_exact_fraction_expression",
            domain="rational_arithmetic",
            domain_ops="FractionOps",
            skill_id="math16_exact_fraction_expression",
            oracle_type="exact_fraction_canonical",
            source_question_text=(
                "精確計算\n\\[\n"
                "\\frac{9}{22}+\\frac{11}{18}\n"
                "-\\left(\\frac{23}{22}-\\frac{7}{18}\\right).\n"
                "\\]\n答案須化為最簡分數。"
            ),
            math16_question_text=(
                "精確計算\n\\[\n"
                "\\frac{9}{22}+\\frac{11}{18}\n"
                "-\\left(\\frac{23}{22}-\\frac{7}{18}\\right).\n"
                "\\]\n答案須化為最簡分數。"
            ),
            frozen_params={"expression": "9/22 + 11/18 - (23/22 - 7/18)"},
            oracle_payload={"expression": "9/22 + 11/18 - (23/22 - 7/18)"},
            correct_answer={
                "numerator": 4,
                "denominator": 11,
                "canonical_latex": r"\frac{4}{11}",
            },
            canonical_latex=r"\frac{4}{11}",
            source="111年國中教育會考數學試題第5題（formalized fixed item）",
            pool_role="math16_new_fixed_item",
            year_source="111",
            provenance={"item": "5", "exam_year": "111"},
        ),
        _task(
            task_id="ce113_q01_negative_fraction_subtraction",
            domain="rational_arithmetic",
            domain_ops="FractionOps",
            skill_id="math16_negative_fraction_subtraction",
            oracle_type="exact_fraction_canonical",
            source_question_text=(
                "精確計算\n\\[\n"
                "\\frac{3}{7}-\\left(-\\frac{1}{4}\\right).\n"
                "\\]\n答案須化為最簡分數。"
            ),
            math16_question_text=(
                "精確計算\n\\[\n"
                "\\frac{3}{7}-\\left(-\\frac{1}{4}\\right).\n"
                "\\]\n答案須化為最簡分數。"
            ),
            frozen_params={"expression": "3/7 - (-1/4)"},
            oracle_payload={"expression": "3/7 - (-1/4)"},
            correct_answer={
                "numerator": 19,
                "denominator": 28,
                "canonical_latex": r"\frac{19}{28}",
            },
            canonical_latex=r"\frac{19}{28}",
            source="113年國中教育會考數學試題第1題（fraction easy control）",
            pool_role="math16_new_fixed_item",
            year_source="113",
            provenance={
                "item": "1",
                "exam_year": "113",
                "role": "fraction_easy_control",
            },
        ),
        _task(
            task_id="ce112_q12_independent_probability_fraction",
            domain="rational_arithmetic",
            domain_ops="FractionOps",
            skill_id="math16_independent_probability_fraction",
            oracle_type="exact_fraction_canonical",
            source_question_text=(
                r"第一組有 \(6\) 個等可能結果，其中 \(2\) 個符合條件；"
                r"第二組有 \(5\) 個等可能結果，其中 \(1\) 個符合條件。"
                r"若兩次選擇彼此獨立，求兩組皆符合條件的機率，並以最簡分數表示。"
            ),
            math16_question_text=(
                r"第一組有 \(6\) 個等可能結果，其中 \(2\) 個符合條件；"
                r"第二組有 \(5\) 個等可能結果，其中 \(1\) 個符合條件。"
                r"若兩次選擇彼此獨立，求兩組皆符合條件的機率，並以最簡分數表示。"
            ),
            frozen_params={"p1": [2, 6], "p2": [1, 5]},
            oracle_payload={"p1": "2/6", "p2": "1/5", "product": "1/15"},
            correct_answer={
                "numerator": 1,
                "denominator": 15,
                "canonical_latex": r"\frac{1}{15}",
            },
            canonical_latex=r"\frac{1}{15}",
            source="112年國中教育會考數學試題第12題（substantial abstraction）",
            pool_role="math16_new_fixed_item",
            year_source="112",
            provenance={
                "item": "12",
                "exam_year": "112",
                "transformation_level": "substantial_abstraction",
                "original_context": "盒玩情境機率建模",
                "retained_core": "精確分數乘法",
                "not_tested": ["情境建模", "獨立性辨識", "有利結果擷取"],
                "difficulty_equivalence_to_original_exam": False,
                "note": "難度不得直接等同原會考題",
            },
        ),
        _task(
            task_id="ce112_q04_radical_simplification",
            domain="radicals",
            domain_ops="RadicalOps",
            skill_id="math16_radical_simplification_fixed",
            oracle_type="radical_simplification_canonical",
            source_question_text="將\n\\[\n\\sqrt{135}\n\\]\n化為最簡根式。",
            math16_question_text="將\n\\[\n\\sqrt{135}\n\\]\n化為最簡根式。",
            frozen_params={"radicand": 135},
            oracle_payload={"radicand": 135},
            correct_answer={
                "coefficient": 3,
                "radicand": 15,
                "canonical_latex": r"3\sqrt{15}",
            },
            canonical_latex=r"3\sqrt{15}",
            source="112年國中教育會考數學試題第4題（formalized fixed item）",
            pool_role="math16_new_fixed_item",
            year_source="112",
            provenance={"item": "4", "exam_year": "112"},
        ),
        _task(
            task_id="ce111_q10_ordered_quadratic_roots_radical",
            domain="radicals",
            domain_ops="RadicalOps",
            skill_id="math16_ordered_quadratic_roots_radical",
            oracle_type="compound_radical_result",
            source_question_text=(
                "一元二次方程式\n\\[\n(x-2)^2=3\n\\]\n"
                "的兩根為 \\(a,b\\)，且 \\(a>b\\)。求 \\(2a+b\\)，答案須保持精確根式形式。"
            ),
            math16_question_text=(
                "一元二次方程式\n\\[\n(x-2)^2=3\n\\]\n"
                "的兩根為 \\(a,b\\)，且 \\(a>b\\)。求 \\(2a+b\\)，答案須保持精確根式形式。"
            ),
            frozen_params={
                "equation": "(x-2)^2=3",
                "order": "a>b",
                "target": "2a+b",
            },
            oracle_payload={
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
            },
            correct_answer={
                "result": {
                    "rational": 6,
                    "radical_coefficient": 1,
                    "radicand": 3,
                    "canonical_latex": r"6+\sqrt{3}",
                }
            },
            canonical_latex=r"6+\sqrt{3}",
            source="111年國中教育會考數學試題第10題（formalized fixed item）",
            pool_role="math16_new_fixed_item",
            year_source="111",
            provenance={
                "item": "10",
                "exam_year": "111",
                "requires_compound_radical_schema": True,
            },
        ),
        _task(
            task_id="ce113_q11_rationalize_denominator",
            domain="radicals",
            domain_ops="RadicalOps",
            skill_id="math16_rationalize_denominator_ab_sum",
            oracle_type="integer_exact",
            source_question_text=(
                "將\n\\[\n\\frac{9}{4-\\sqrt{7}}\n\\]\n"
                "化為 \\(a+b\\sqrt{7}\\)，其中 \\(a,b\\) 為整數，求 \\(a+b\\)。"
            ),
            math16_question_text=(
                "將\n\\[\n\\frac{9}{4-\\sqrt{7}}\n\\]\n"
                "化為 \\(a+b\\sqrt{7}\\)，其中 \\(a,b\\) 為整數，求 \\(a+b\\)。"
            ),
            frozen_params={
                "numerator": 9,
                "denominator": "4-sqrt(7)",
                "radicand": 7,
            },
            oracle_payload={
                "a": 4,
                "b": 1,
                "radicand": 7,
                "canonical_latex": r"4+\sqrt{7}",
            },
            correct_answer=5,
            source="113年國中教育會考數學試題第11題（Math16 rerun; historical_v2_reference_only）",
            pool_role="math16_new_fixed_item",
            year_source="113",
            reuse_policy="rerun",
            provenance={
                "item": "11",
                "exam_year": "113",
                "reuse_policy": "rerun",
                "historical_v2_reference_only": True,
                "note": "舊 v2 結果不得混入本輪 primary/confirmatory analysis；本輪一律 rerun",
                "related_held_out_exam_task_id": "ce115_ext_113_11_rationalize_l1",
            },
            extra={"historical_v2_policy": "historical_v2_reference_only"},
        ),
    ]
    return existing + new12


def domain_ops_distribution(tasks: list[dict[str, Any]]) -> dict[str, int]:
    dist = {name: 0 for name in DOMAIN_OPS}
    for task in tasks:
        dist[task["domain_ops"]] += 1
    return dist


def build_pool_manifest() -> dict[str, Any]:
    tasks = build_pool_tasks()
    dist = domain_ops_distribution(tasks)
    if dist != {name: 4 for name in DOMAIN_OPS}:
        raise ValueError(f"Math16 domain_ops must be 4/4/4/4, got {dist}")
    if any(task.get("year_source") == "114" for task in tasks):
        raise ValueError("114 held-out year leaked into Math16 pool")
    if len(tasks) != 16:
        raise ValueError(f"expected 16 tasks, got {len(tasks)}")

    existing = [t for t in tasks if t["pool_role"] == "existing_formal_ce115_l1"]
    new_tasks = [t for t in tasks if t["pool_role"] == "math16_new_fixed_item"]
    task_freeze = {
        t["task_id"]: {
            "freeze_record_sha256": t["freeze_record_sha256"],
            "oracle_payload": t["oracle_payload"],
            "correct_answer": t["correct_answer"],
            "math16_question_text": t["math16_question_text"],
        }
        for t in tasks
    }
    body = {
        "pool_id": POOL_ID,
        "manifest_id": "math16_latex_v1_pool_manifest",
        "manifest_version": POOL_MANIFEST_VERSION,
        "git_head_at_freeze": GIT_HEAD_AT_FREEZE,
        "run_id_planned": "gemini35flash_math16_ab123_run_001",
        "model_planned": "gemini-3.5-flash",
        "conditions": ["ab1", "ab2g", "ab2d"],
        "cells_planned": 48,
        "presentation_transform_default": PRESENTATION_TRANSFORM,
        "itt_policy": (
            "first_valid_model_response_fixed_to_treatment; "
            "healer/pipeline/retry accounted separately"
        ),
        "held_out_policy": {
            "exclude_years": ["114"],
            "note": "114年維持 held-out，不得納入本輪",
        },
        "analysis_policy": {
            "old_results_mixing": "forbidden",
            "historical_v2_reference_only_task_ids": ["ce113_q11_rationalize_denominator"],
        },
        "domain_ops_distribution": dist,
        "domain_ops_distribution_verified": True,
        "task_ids": [t["task_id"] for t in tasks],
        "existing_task_ids": [t["task_id"] for t in existing],
        "new_task_ids": [t["task_id"] for t in new_tasks],
        "task_freeze": task_freeze,
        "tasks": tasks,
    }
    body["task_freeze_hash"] = _sha(task_freeze)
    body["pool_identity_hash"] = _sha(
        {
            "pool_id": POOL_ID,
            "task_ids": body["task_ids"],
            "domain_ops_distribution": dist,
            "presentation_transform_default": PRESENTATION_TRANSFORM,
            "task_freeze_hash": body["task_freeze_hash"],
        }
    )
    body["manifest_content_sha256"] = _sha({k: v for k, v in body.items()})
    return body


def write_pool_manifest(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[2]
    manifest = build_pool_manifest()
    path = root / MANIFEST_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    # Keep existing4 freeze as provenance companion (source stems only).
    existing = [t for t in manifest["tasks"] if t["pool_role"] == "existing_formal_ce115_l1"]
    existing_doc = {
        "manifest_id": "math16_existing4_formal_freeze.v2_latex_source_identity",
        "pool_id": POOL_ID,
        "git_head": GIT_HEAD_AT_FREEZE,
        "note": (
            "source_question_text is provenance/audit only; "
            "model-facing stems are math16_question_text in the pool manifest"
        ),
        "tasks": [
            {
                "task_id": t["task_id"],
                "domain_ops": t["domain_ops"],
                "source_question_text": t["source_question_text"],
                "math16_question_text": t["math16_question_text"],
                "presentation_transform": t["presentation_transform"],
                "frozen_params": t["frozen_params"],
                "oracle_payload": t["oracle_payload"],
                "correct_answer": t["correct_answer"],
                "freeze_record_sha256": t["freeze_record_sha256"],
            }
            for t in existing
        ],
    }
    (root / EXISTING4_FREEZE_REL).write_text(
        json.dumps(existing_doc, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest


def load_pool_manifest(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[2]
    path = root / MANIFEST_REL
    return json.loads(path.read_text(encoding="utf-8"))


def tasks_by_id(root: Path | None = None) -> dict[str, dict[str, Any]]:
    manifest = load_pool_manifest(root)
    return {row["task_id"]: row for row in manifest["tasks"]}


def task_specs_for_sampler(root: Path | None = None) -> dict[str, dict[str, Any]]:
    """Minimal task_spec dicts compatible with sample_task_parameters."""
    return {
        tid: {
            "task_id": row["task_id"],
            "domain": row["domain"],
            "skill_id": row["skill_id"],
            "oracle_type": row["oracle_type"],
            "difficulty_level": row["difficulty_level"],
            "parameter_ranges": row["parameter_ranges"],
        }
        for tid, row in tasks_by_id(root).items()
    }


def frozen_for_prompt(task: dict[str, Any]) -> dict[str, Any]:
    """Frozen prompt identity is stem params only (no answer leakage).

    Evaluator-side audit fields remain in task['oracle_payload'] and are not
    what the model must echo; generate() oracle_payload must equal frozen_params.
    """
    return {
        "task_id": task["task_id"],
        "oracle_type": task["oracle_type"],
        "oracle_payload": task["frozen_params"],
        "repeat_seed": task.get("seed") or SEED,
    }
