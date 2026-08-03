"""V2 content model for the Math16 Ab2d menu-vs-full runtime-contract prompt rewrite.

Single source of truth for both `ab2d_domain_menu_v2` and `ab2d_full_v2` builders.
Every entry's `full_plan_body` was mined from an already-frozen, already-PASSING V1 cell
(preferring gemini/ab2d_full; falling back to gemini/ab2d_domain_menu for
ce113_q11_rationalize_denominator, whose gemini ab2d_full cells all failed on a model
misread of RadicalOps.rationalize_linear_denominator's return tuple -- see
docs/experiments/results/Math16/math16_gemini_full_rationalize_5cell_forensic_v1.md),
then independently re-verified against agent_tools/finals_rebuild/domain_api_ssot.py and
agent_tools/finals_rebuild/math_answer_contracts.py, and locally re-executed (see
scripts/preflight_math16_ab2d_v2.py) before being used to render any prompt text.

This module does not modify, import-shadow, or replace any V1 prompt/builder module.
"""

from __future__ import annotations

from typing import Any, Mapping

# answer_schema: either a dict of {key: type_name} for a dict-shaped correct_answer,
# or the literal string "int" for a bare-scalar-int correct_answer contract.
# Used only to render the domain-menu runtime skeleton's placeholder shape -- values are
# always `...` (ellipsis) there; the real computation only appears in full_plan_body.

TASK_SCAFFOLDS_V2: dict[str, dict[str, Any]] = {
    "ce115_calc_polynomial_division_l1": {
        "domain": "PolynomialOps",
        "oracle_type": "math16_polynomial_division_general",
        "frozen_literal": {"dividend_coefficients": [6, 0, 6], "divisor_coefficients": [1, -4]},
        "answer_schema": {
            "quotient_coefficients": "list",
            "remainder_coefficients": "list",
            "quotient_latex": "str",
            "remainder_latex": "str",
        },
        "full_plan_steps": [
            "1) dividend = frozen[\"dividend_coefficients\"]; divisor = frozen[\"divisor_coefficients\"].",
            "2) q, r = PolynomialOps.div_qr(dividend, divisor).",
            "3) q_latex = PolynomialOps.format_latex(q); r_latex = PolynomialOps.format_latex(r).",
            "4) Assemble correct_answer exactly according to the Answer contract.",
        ],
        "full_plan_body": '''    dividend = frozen["dividend_coefficients"]
    divisor = frozen["divisor_coefficients"]
    q, r = PolynomialOps.div_qr(dividend, divisor)
    q_latex = PolynomialOps.format_latex(q)
    r_latex = PolynomialOps.format_latex(r)
    correct_answer = {
        "quotient_coefficients": q,
        "remainder_coefficients": r,
        "quotient_latex": q_latex,
        "remainder_latex": r_latex,
    }''',
    },
    "ce115_calc_polynomial_factor_roots_l1": {
        "domain": "PolynomialOps",
        "oracle_type": "math16_polynomial_factor_roots",
        "frozen_literal": {"quadratic_coefficients": [1, 4, -12]},
        "answer_schema": {"roots": "list", "factorization_latex": "str", "roots_latex": "str"},
        "full_plan_steps": [
            "1) a, b, c = frozen[\"quadratic_coefficients\"].",
            "2) factors = PolynomialOps.factor_quadratic_exact(a, b, c) -> list of 2 dicts with x_coefficient/constant.",
            "3) For each factor dict, root = -constant / x_coefficient (as Fraction); sort factors ascending by root.",
            "4) roots = [int or float root per factor]; build factorization_latex by concatenating each factor's LaTeX term; roots_latex = \"x_1 = ..., x_2 = ...\".",
            "5) Assemble correct_answer exactly according to the Answer contract.",
        ],
        "full_plan_body": '''    a, b, c = frozen["quadratic_coefficients"]
    factors = PolynomialOps.factor_quadratic_exact(a, b, c)

    def _frac(v):
        if isinstance(v, str):
            if "/" in v:
                num, den = v.split("/")
                return Fraction(int(num), int(den))
            return Fraction(int(v))
        return Fraction(v)

    parsed = []
    for f in factors:
        coeff = _frac(f["x_coefficient"])
        const = _frac(f["constant"])
        root = -const / coeff
        parsed.append({"coeff": coeff, "const": const, "root": root})
    parsed.sort(key=lambda item: item["root"])

    def _fmt_frac(fr):
        if fr.denominator == 1:
            return str(fr.numerator)
        sign = "-" if fr < 0 else ""
        return f"{sign}\\\\frac{{{abs(fr.numerator)}}}{{{fr.denominator}}}"

    roots = [p["root"].numerator if p["root"].denominator == 1 else float(p["root"]) for p in parsed]
    roots_latex = f"x_1 = {_fmt_frac(parsed[0]['root'])}, x_2 = {_fmt_frac(parsed[1]['root'])}"

    factor_strings = []
    for p in parsed:
        coeff, const = p["coeff"], p["const"]
        term = "x" if coeff == 1 else ("-x" if coeff == -1 else f"{_fmt_frac(coeff)}x")
        if const == 0:
            factor_strings.append(term)
        elif const > 0:
            factor_strings.append(f"({term}+{_fmt_frac(const)})")
        else:
            factor_strings.append(f"({term}-{_fmt_frac(-const)})")
    factorization_latex = "".join(factor_strings)

    correct_answer = {
        "roots": roots,
        "factorization_latex": factorization_latex,
        "roots_latex": roots_latex,
    }''',
        "extra_imports": ["from fractions import Fraction"],
    },
    "ce115_calc_exact_rational_expression_l1": {
        "domain": "FractionOps",
        "oracle_type": "math16_exact_rational_expression",
        "frozen_literal": {
            "products": [
                {"sign": 1, "left": "2.79", "right": "89.3"},
                {"sign": -1, "left": "-0.21", "right": "89.3"},
            ]
        },
        "answer_schema": {"value": "str", "canonical_latex": "str"},
        "full_plan_steps": [
            "1) For each entry in frozen[\"products\"]: term = FractionOps.mul(FractionOps.create(left), FractionOps.create(right)); negate with FractionOps.sub(FractionOps.create(0), term) if sign == -1.",
            "2) result = FractionOps.add(term1, term2).",
            "3) value = FractionOps.to_exact(result); canonical_latex = FractionOps.to_latex(result).",
            "4) Assemble correct_answer exactly according to the Answer contract.",
        ],
        "full_plan_body": '''    p1, p2 = frozen["products"]

    def _signed_product(p):
        term = FractionOps.mul(FractionOps.create(p["left"]), FractionOps.create(p["right"]))
        if p["sign"] == -1:
            term = FractionOps.sub(FractionOps.create(0), term)
        return term

    result = FractionOps.add(_signed_product(p1), _signed_product(p2))
    correct_answer = {
        "value": str(FractionOps.to_exact(result)),
        "canonical_latex": FractionOps.to_latex(result),
    }''',
    },
    "ce115_calc_radical_simplification_l1": {
        "domain": "RadicalOps",
        "oracle_type": "math16_radical_simplification",
        "frozen_literal": {"radicand": 27},
        "answer_schema": {"coefficient": "int", "radicand": "int", "canonical_latex": "str"},
        "full_plan_steps": [
            "1) coeff, rest = RadicalOps.simplify_term(1, frozen[\"radicand\"]).",
            "2) coeff_int = RadicalOps.exact_integer(coeff); rest_int = RadicalOps.exact_integer(rest).",
            "3) canonical_latex = RadicalOps.format_term(coeff_int, rest_int).",
            "4) Assemble correct_answer exactly according to the Answer contract.",
        ],
        "full_plan_body": '''    coeff, rest = RadicalOps.simplify_term(1, frozen["radicand"])
    coeff_int = RadicalOps.exact_integer(coeff)
    rest_int = RadicalOps.exact_integer(rest)
    canonical_latex = RadicalOps.format_term(coeff_int, rest_int)
    correct_answer = {
        "coefficient": coeff_int,
        "radicand": rest_int,
        "canonical_latex": canonical_latex,
    }''',
    },
    "ce111_q02_polynomial_division_remainder": {
        "domain": "PolynomialOps",
        "oracle_type": "polynomial_division_remainder_only",
        "frozen_literal": {"dividend_coefficients": [6, 4, 0], "divisor_coefficients": [2, 0, 0]},
        "answer_schema": {"remainder": "str", "canonical_latex": "str"},
        "full_plan_steps": [
            "1) dividend = frozen[\"dividend_coefficients\"]; divisor = frozen[\"divisor_coefficients\"].",
            "2) q, r = PolynomialOps.div_qr(dividend, divisor) (q is unused; only r is scored).",
            "3) r_latex = PolynomialOps.format_latex(r).",
            "4) Assemble correct_answer exactly according to the Answer contract.",
        ],
        "full_plan_body": '''    dividend = frozen["dividend_coefficients"]
    divisor = frozen["divisor_coefficients"]
    q, r = PolynomialOps.div_qr(dividend, divisor)
    r_latex = PolynomialOps.format_latex(r)
    correct_answer = {
        "remainder": r_latex,
        "canonical_latex": r_latex,
    }''',
    },
    "ce111_q08_polynomial_factor_parameter_recovery": {
        "domain": "PolynomialOps",
        "oracle_type": "polynomial_factor_parameter_recovery",
        "frozen_literal": {
            "quadratic_coefficients": [39, 5, -14],
            "template_left_x_coefficient": 3,
            "factor_order_policy": "strict_source_template",
        },
        "answer_schema": "int",
        "full_plan_steps": [
            "1) a0, b0, c0 = frozen[\"quadratic_coefficients\"]; factors = PolynomialOps.factor_quadratic_exact(a0, b0, c0) -> 2 dicts with x_coefficient/constant.",
            "2) target = frozen[\"template_left_x_coefficient\"]; find the factor (or its sign-flip) whose x_coefficient matches target, label it (a*x+b), the other (c*x+d).",
            "3) correct_answer = a + 2*c (per factor_order_policy=strict_source_template contract).",
            "4) Return correct_answer as a bare int exactly according to the Answer contract.",
        ],
        "full_plan_body": '''    a0, b0, c0 = frozen["quadratic_coefficients"]
    target = frozen["template_left_x_coefficient"]
    f1, f2 = PolynomialOps.factor_quadratic_exact(a0, b0, c0)
    p1, q1 = int(f1["x_coefficient"]), int(f1["constant"])
    p2, q2 = int(f2["x_coefficient"]), int(f2["constant"])

    if p1 == target:
        a, b, c = q1, p2, q2
    elif p1 == -target:
        a, b, c = -q1, -p2, -q2
    elif p2 == target:
        a, b, c = q2, p1, q1
    else:
        a, b, c = -q2, -p1, -q1

    correct_answer = a + 2 * c''',
    },
    "ce111_q03_prime_factor_selection": {
        "domain": "IntegerOps",
        "oracle_type": "integer_exact",
        "frozen_literal": {"candidates": [11, 12, 13, 14], "n": 156},
        "answer_schema": "int",
        "full_plan_steps": [
            "1) factors = IntegerOps.prime_factorization(frozen[\"n\"]) -> dict[int prime, int exponent].",
            "2) correct_answer = the first value in frozen[\"candidates\"] that is a key of factors (i.e. a prime factor of n).",
            "3) Return correct_answer as a bare int exactly according to the Answer contract.",
        ],
        "full_plan_body": '''    n = frozen["n"]
    candidates = frozen["candidates"]
    factors = IntegerOps.prime_factorization(n)
    correct_answer = next(c for c in candidates if c in factors)''',
    },
    "ce112_q01_negative_integer_power": {
        "domain": "IntegerOps",
        "oracle_type": "integer_exact",
        "frozen_literal": {"base": -3, "exponent": 3},
        "answer_schema": "int",
        "full_plan_steps": [
            "1) base = frozen[\"base\"]; exponent = frozen[\"exponent\"].",
            "2) correct_answer = int(IntegerOps.safe_eval(f\"{base}**{exponent}\")).",
            "3) Return correct_answer as a bare int exactly according to the Answer contract.",
        ],
        "full_plan_body": '''    base = frozen["base"]
    exponent = frozen["exponent"]
    correct_answer = int(IntegerOps.safe_eval(f"({base})**{exponent}"))''',
    },
    "ce112_q09_divisor_multiple_intersection": {
        "domain": "IntegerOps",
        "oracle_type": "integer_count",
        "frozen_literal": {"multiple_of": 18, "divisor_of": 216},
        "answer_schema": {"count": "int"},
        "full_plan_steps": [
            "1) divisors = IntegerOps.positive_divisors(frozen[\"divisor_of\"]).",
            "2) valid = [d for d in divisors if IntegerOps.is_divisible(d, frozen[\"multiple_of\"])].",
            "3) count = len(valid).",
            "4) Assemble correct_answer exactly according to the Answer contract.",
        ],
        "full_plan_body": '''    divisors = IntegerOps.positive_divisors(frozen["divisor_of"])
    valid = [d for d in divisors if IntegerOps.is_divisible(d, frozen["multiple_of"])]
    correct_answer = {"count": len(valid)}''',
    },
    "ce111_nonchoice_q01_part1_exponential_growth": {
        "domain": "IntegerOps",
        "oracle_type": "integer_exact_k",
        "frozen_literal": {"initial": 1, "split_factor": 4, "hours_per_generation": 20, "days": 15},
        "answer_schema": {"k": "int"},
        "full_plan_steps": [
            "1) total_hours = IntegerOps.safe_eval(f\"{frozen['days']} * 24\").",
            "2) k = IntegerOps.safe_eval(f\"{total_hours} // {frozen['hours_per_generation']}\") (requires IntegerOps.is_divisible(total_hours, hours_per_generation)).",
            "3) Assemble correct_answer exactly according to the Answer contract.",
        ],
        "full_plan_body": '''    days = frozen["days"]
    hours_per_generation = frozen["hours_per_generation"]
    total_hours = IntegerOps.safe_eval(f"{days} * 24")
    if not IntegerOps.is_divisible(total_hours, hours_per_generation):
        raise ValueError("total_hours not divisible by hours_per_generation")
    k = IntegerOps.safe_eval(f"{total_hours} // {hours_per_generation}")
    correct_answer = {"k": int(k)}''',
    },
    "ce111_q05_exact_fraction_expression": {
        "domain": "FractionOps",
        "oracle_type": "exact_fraction_canonical",
        "frozen_literal": {"expression": "9/22 + 11/18 - (23/22 - 7/18)"},
        "answer_schema": {"numerator": "int", "denominator": "int", "canonical_latex": "str"},
        "full_plan_steps": [
            "1) This task's frozen \"expression\" is fixed text \"9/22 + 11/18 - (23/22 - 7/18)\"; "
            "build it from FractionOps.from_parts(9,22), from_parts(11,18), from_parts(23,22), from_parts(7,18).",
            "2) result = FractionOps.sub(FractionOps.add(f1, f2), FractionOps.sub(f3, f4)).",
            "3) numerator = result.numerator; denominator = result.denominator; canonical_latex = FractionOps.to_latex(result).",
            "4) Assemble correct_answer exactly according to the Answer contract.",
        ],
        "full_plan_body": '''    f1 = FractionOps.from_parts(9, 22)
    f2 = FractionOps.from_parts(11, 18)
    f3 = FractionOps.from_parts(23, 22)
    f4 = FractionOps.from_parts(7, 18)
    result = FractionOps.sub(FractionOps.add(f1, f2), FractionOps.sub(f3, f4))
    correct_answer = {
        "numerator": result.numerator,
        "denominator": result.denominator,
        "canonical_latex": FractionOps.to_latex(result),
    }''',
    },
    "ce113_q01_negative_fraction_subtraction": {
        "domain": "FractionOps",
        "oracle_type": "exact_fraction_canonical",
        "frozen_literal": {"expression": "3/7 - (-1/4)"},
        "answer_schema": {"numerator": "int", "denominator": "int", "canonical_latex": "str"},
        "full_plan_steps": [
            "1) This task's frozen \"expression\" is fixed text \"3/7 - (-1/4)\"; "
            "build it from FractionOps.from_parts(3,7) and FractionOps.from_parts(-1,4).",
            "2) result = FractionOps.sub(left, right).",
            "3) numerator = result.numerator; denominator = result.denominator; canonical_latex = FractionOps.to_latex(result).",
            "4) Assemble correct_answer exactly according to the Answer contract.",
        ],
        "full_plan_body": '''    left = FractionOps.from_parts(3, 7)
    right = FractionOps.from_parts(-1, 4)
    result = FractionOps.sub(left, right)
    correct_answer = {
        "numerator": result.numerator,
        "denominator": result.denominator,
        "canonical_latex": FractionOps.to_latex(result),
    }''',
    },
    "ce112_q12_independent_probability_fraction": {
        "domain": "FractionOps",
        "oracle_type": "exact_fraction_canonical",
        "frozen_literal": {"p1": [2, 6], "p2": [1, 5]},
        "answer_schema": {"numerator": "int", "denominator": "int", "canonical_latex": "str"},
        "full_plan_steps": [
            "1) p1_num, p1_den = frozen[\"p1\"]; p2_num, p2_den = frozen[\"p2\"].",
            "2) a = FractionOps.from_parts(p1_num, p1_den); b = FractionOps.from_parts(p2_num, p2_den).",
            "3) value = FractionOps.mul(a, b).",
            "4) Assemble correct_answer exactly according to the Answer contract.",
        ],
        "full_plan_body": '''    p1_num, p1_den = frozen["p1"]
    p2_num, p2_den = frozen["p2"]
    a = FractionOps.from_parts(p1_num, p1_den)
    b = FractionOps.from_parts(p2_num, p2_den)
    value = FractionOps.mul(a, b)
    correct_answer = {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "canonical_latex": FractionOps.to_latex(value),
    }''',
    },
    "ce112_q04_radical_simplification": {
        "domain": "RadicalOps",
        "oracle_type": "radical_simplification_canonical",
        "frozen_literal": {"radicand": 135},
        "answer_schema": {"coefficient": "int", "radicand": "int", "canonical_latex": "str"},
        "full_plan_steps": [
            "1) coeff, rest = RadicalOps.simplify_term(1, frozen[\"radicand\"]).",
            "2) coeff_int = RadicalOps.exact_integer(coeff); rest_int = RadicalOps.exact_integer(rest).",
            "3) canonical_latex = RadicalOps.format_term(coeff_int, rest_int).",
            "4) Assemble correct_answer exactly according to the Answer contract.",
        ],
        "full_plan_body": '''    coeff, rest = RadicalOps.simplify_term(1, frozen["radicand"])
    coeff_int = RadicalOps.exact_integer(coeff)
    rest_int = RadicalOps.exact_integer(rest)
    canonical_latex = RadicalOps.format_term(coeff_int, rest_int)
    correct_answer = {
        "coefficient": coeff_int,
        "radicand": rest_int,
        "canonical_latex": canonical_latex,
    }''',
    },
    "ce111_q10_ordered_quadratic_roots_radical": {
        "domain": "RadicalOps",
        "oracle_type": "compound_radical_result",
        "frozen_literal": {"equation": "(x-2)^2=3", "order": "a>b", "target": "2a+b"},
        "answer_schema": {
            "result": {"rational": "int", "radical_coefficient": "int", "radicand": "int", "canonical_latex": "str"}
        },
        "full_plan_steps": [
            "1) frozen[\"equation\"] is the fixed equation (x-2)^2=3, with roots 2+sqrt(3) and 2-sqrt(3); "
            "per frozen[\"order\"]=\"a>b\": a = {rational:2, radical_coefficient:1, radicand:3}, "
            "b = {rational:2, radical_coefficient:-1, radicand:3}.",
            "2) frozen[\"target\"]=\"2a+b\": term_2a = RadicalOps.scale_linear_radical(a, 2); "
            "result = RadicalOps.add_linear_radicals(term_2a, b).",
            "3) canonical_latex = RadicalOps.format_linear_radical(result); "
            "apply RadicalOps.exact_integer to each of result's rational/radical_coefficient/radicand.",
            "4) Assemble correct_answer exactly according to the Answer contract (nested under \"result\").",
        ],
        "full_plan_body": '''    a = {"rational": 2, "radical_coefficient": 1, "radicand": 3}
    b = {"rational": 2, "radical_coefficient": -1, "radicand": 3}
    term_2a = RadicalOps.scale_linear_radical(a, 2)
    result = RadicalOps.add_linear_radicals(term_2a, b)
    canonical_latex = RadicalOps.format_linear_radical(result)
    correct_answer = {
        "result": {
            "rational": RadicalOps.exact_integer(result["rational"]),
            "radical_coefficient": RadicalOps.exact_integer(result["radical_coefficient"]),
            "radicand": RadicalOps.exact_integer(result["radicand"]),
            "canonical_latex": canonical_latex,
        }
    }''',
    },
    "ce113_q11_rationalize_denominator": {
        "domain": "RadicalOps",
        "oracle_type": "integer_exact",
        "frozen_literal": {"numerator": 9, "denominator": "4-sqrt(7)", "radicand": 7},
        "answer_schema": "int",
        "full_plan_steps": [
            "1) frozen[\"denominator\"]=\"4-sqrt(7)\" means denom_rational=4, denom_radical_coeff=-1; "
            "radicand = frozen[\"radicand\"]; numerator = frozen[\"numerator\"].",
            "2) a_out, b_out, r = RadicalOps.rationalize_linear_denominator(numerator, denom_rational, denom_radical_coeff, radicand) "
            "-- r is always the (possibly re-simplified) radicand, per its docstring contract; a_out/b_out are the final coefficients, no further division.",
            "3) a = RadicalOps.exact_integer(a_out); b = RadicalOps.exact_integer(b_out).",
            "4) correct_answer = a + b (bare int, per the Answer contract).",
        ],
        "full_plan_body": '''    numerator = frozen["numerator"]
    radicand = frozen["radicand"]
    denom_rational, denom_radical_coeff = 4, -1  # parsed from frozen["denominator"] == "4-sqrt(7)"
    a_out, b_out, r = RadicalOps.rationalize_linear_denominator(
        numerator, denom_rational, denom_radical_coeff, radicand
    )
    a = RadicalOps.exact_integer(a_out)
    b = RadicalOps.exact_integer(b_out)
    correct_answer = a + b''',
    },
}


def task_scaffold(task_id: str) -> Mapping[str, Any]:
    return TASK_SCAFFOLDS_V2[task_id]
