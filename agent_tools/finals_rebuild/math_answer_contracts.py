# -*- coding: utf-8 -*-
import json
from typing import Any, Mapping

GENERATION_INSTRUCTIONS = """Write only complete Python source code.
Do not use Markdown fences, prose, explanations, or prompt echoes.
Implement exactly one function:

def generate(level=1, **kwargs):

`generate()` must return exactly the three-key dictionary specified below."""

OVERRIDE_STATEMENT = """Return exactly these three top-level keys and no others:
`question_text`, `correct_answer`, and `oracle_payload`.
Do not return `answer`, `mode`, or any additional key.
The task-specific `correct_answer` schema below supersedes any earlier generic `correct_answer: str` instruction."""

NEUTRAL_TASK_STATEMENTS = {
    "polynomial_division_exact": """# Task Specification: Polynomial Division
- Task Name: Polynomial Division
- Input Parameters: `dividend_coefficients` (coefficients of the dividend polynomial) and `divisor_root` (the root of the linear divisor).
- Output: `question_text` must ask the user to divide the dividend polynomial by the linear divisor (i.e. x - divisor_root) to find the quotient and remainder.
- Calculation: `correct_answer` must calculate and return the quotient coefficients and remainder.
- Data Contract: `oracle_payload` must return exactly the input parameters.""",

    "rpm_circumference_kph": """# Task Specification: Rotation Speed Conversion
- Task Name: Rotation Speed Conversion
- Input Parameters: `circumference_cm` (wheel circumference in cm), `rpm_symbol` (symbol for rpm), and `requested_unit` ("km/h").
- Output: `question_text` must ask to calculate the linear speed in km/h for 1 RPM.
- Calculation: `correct_answer` must calculate the speed coefficient for 1 RPM as a reduced fraction string, and the unit "km/h".
- Data Contract: `oracle_payload` must return exactly the input parameters.""",

    "largest_proper_divisor_logic": """# Task Specification: Largest Proper Divisor Logic Reasoning
- Task Name: Largest Proper Divisor Logic Reasoning
- Input Parameters: `largest_proper_divisors` (mapping from labels to largest proper divisors) and `claims` (list of necessity claims).
- Output: `question_text` must present the claims and ask whether each necessity claim is logically true or false.
- Calculation: `correct_answer` must evaluate and return the boolean truth value (True or False) of each claim in the exact frozen order.
- Data Contract: `oracle_payload` must return exactly the input parameters.""",

    "radical_simplification": """# Task Specification: Radical Simplification
- Task Name: Radical Simplification
- Input Parameters: `radicand` (positive integer under the square root) and optional `outer_coefficient` (positive integer multiplier outside the root; treat as 1 when absent).
- Output: `question_text` must ask to rewrite outer_coefficient * sqrt(radicand) in simplest radical form coefficient * sqrt(square_free_radicand).
- Calculation: `correct_answer` must return the simplified integer coefficient and the square-free radicand.
- Data Contract: `oracle_payload` must return exactly the input parameters.""",

    "exact_rational_expression": """# Task Specification: Exact Rational Expression Evaluation
- Task Name: Exact Rational Expression Evaluation
- Input Parameters: `products` (ordered list of terms; each term has `sign` (1 or -1), `left` and `right` exact decimal strings). The expression value is the sum over terms of sign * left * right.
- Output: `question_text` must present the arithmetic expression built from these terms.
- Calculation: `correct_answer` must evaluate the expression with exact rational arithmetic (no floats) and return the canonical value string.
- Data Contract: `oracle_payload` must return exactly the input parameters.""",

    "polynomial_division_general": """# Task Specification: Polynomial Division (General Linear Divisor)
- Task Name: Polynomial Division with Quotient and Remainder
- Input Parameters: `dividend_coefficients` (highest degree first) and `divisor_coefficients` (two values: leading and constant of the linear divisor).
- Output: `question_text` must ask to divide the dividend polynomial by the linear divisor and report the quotient and the remainder.
- Calculation: `correct_answer` must return the quotient coefficients (highest degree first) and the remainder coefficients computed with exact arithmetic.
- Data Contract: `oracle_payload` must return exactly the input parameters.""",

    "polynomial_factor_roots": """# Task Specification: Polynomial Factorization and Roots
- Task Name: Quadratic Factorization and Roots
- Input Parameters: `quadratic_coefficients` (three integers a, b, c of a x^2 + b x + c, highest degree first).
- Output: `question_text` must ask to factor the quadratic (for example by extracting a common factor) and find both roots.
- Calculation: `correct_answer` must return the two distinct exact roots in ascending numeric order.
- Data Contract: `oracle_payload` must return exactly the input parameters.""",

    "common_factor_quadratic_root_ordering": """# Task Specification: Common-Factor Quadratic Root Ordering
- Task Name: Common-Factor Quadratic Root Ordering
- Input Parameters: `shared_shift`, `leading_factor`, `subtracted_factor`, `root_order`, and `linear_combination`.
- Output: `question_text` must ask to solve (leading_factor*x - subtracted_factor) * (x + shared_shift) = 0, name the roots according to root_order, and evaluate the requested linear combination.
- Calculation: factor the shared binomial, solve both linear factors, order the roots as a>b, and return roots, labeled a/b, and the exact linear combination value.
- Data Contract: `oracle_payload` must return exactly the input parameters.""",

    "exam_power_of_same_base": """# Task Specification: Power of the Same Base
- Input Parameters: `expression` (product/quotient of powers), `required_form` ("power_of_same_base"), `base`.
- Output: ask to rewrite the expression as a single power of the given base.
- Calculation: return base and exponent.
- Data Contract: `oracle_payload` must equal the frozen parameters.""",

    "exam_polynomial_simplify": """# Task Specification: Polynomial Simplification
- Input Parameters: `expression` (difference of polynomials in x).
- Output: ask to simplify the expression.
- Calculation: return simplified coefficients keyed by degree strings "2","1","0".
- Data Contract: `oracle_payload` must equal the frozen parameters.""",

    "exam_linear_system_linear_combination": """# Task Specification: Linear System Linear Combination
- Input Parameters: `equations` (two linear equations) and `target_expression`.
- Output: ask to solve for x and y and evaluate the target expression.
- Calculation: return x, y, and value of the target expression.
- Data Contract: `oracle_payload` must equal the frozen parameters.""",

    "exam_radical_product_simplified": """# Task Specification: Radical Product Simplification
- Input Parameters: `expression` (product involving square roots).
- Output: ask to rewrite as a simplified sum of radical terms.
- Calculation: return terms [{coefficient, radicand}, ...] sorted by increasing radicand after simplifying squares.
- Data Contract: `oracle_payload` must equal the frozen parameters.""",

    "exam_factorization_common_binomial": """# Task Specification: Factorization
- Input Parameters: `expression` and `required_form` ("fully_factored").
- Output: ask to factor the expression completely.
- Calculation: return two linear factors as {x_coefficient, constant} pairs (order may vary; equivalent forms accepted by oracle).
- Data Contract: `oracle_payload` must equal the frozen parameters.""",

    "exam_rationalize_conjugate": """# Task Specification: Rationalize Denominator
- Input Parameters: `expression`, `required_form` ("a + b*sqrt(7)"), `target_expression` ("a + b").
- Output: ask to rewrite in the required form and report a+b.
- Calculation: return a, b, radicand, and value=a+b.
- Data Contract: `oracle_payload` must equal the frozen parameters.""",

    "math16_polynomial_division_general": """# Task Specification: Math16 Polynomial Division
- Input Parameters: `dividend_coefficients`, `divisor_coefficients`.
- Output: `question_text` must use formal LaTeX delimiters and ask for quotient and remainder.
- Calculation: return quotient_coefficients, remainder_coefficients, quotient_latex, remainder_latex.
- Data Contract: `oracle_payload` must equal the frozen parameters.""",

    "math16_polynomial_factor_roots": """# Task Specification: Math16 Quadratic Factor Roots
- Input Parameters: `quadratic_coefficients`.
- Output: LaTeX question asking for factorization and ascending roots.
- Calculation: return roots, factorization_latex, roots_latex.
- Data Contract: `oracle_payload` must equal the frozen parameters.""",

    "math16_exact_rational_expression": """# Task Specification: Math16 Exact Rational Expression
- Input Parameters: `products` of exact decimal strings.
- Output: LaTeX question; exact value with no approximation.
- Calculation: return value and canonical_latex.
- Data Contract: `oracle_payload` must equal the frozen parameters.""",

    "math16_radical_simplification": """# Task Specification: Math16 Radical Simplification
- Input Parameters: `radicand`.
- Output: LaTeX question asking for simplest radical form.
- Calculation: return coefficient, radicand, canonical_latex.
- Data Contract: `oracle_payload` must equal the frozen parameters.""",

    "polynomial_division_remainder_only": """# Task Specification: Polynomial Division Remainder Only
- Input Parameters: dividend/divisor coefficients.
- Output: ask only for the remainder polynomial in LaTeX-capable form.
- Calculation: return remainder and canonical_latex only (quotient is not scored).
- Data Contract: `oracle_payload` may include quotient for audit only.""",

    "polynomial_factor_parameter_recovery": """# Task Specification: Strict Factor Parameter Recovery
- Input Parameters: quadratic coefficients and factor_order_policy=strict_source_template.
- Output: ask for a+2c with first factor fixed as (3x+a).
- Calculation: return the integer a+2c. Factor order may not be swapped to redefine parameters.
- Data Contract: `oracle_payload` holds a,b,c and expansion check.""",

    "integer_exact": """# Task Specification: Integer Exact Answer
- Output: ask for a single integer answer.
- Calculation: return the exact integer.
- Data Contract: `oracle_payload` must equal the frozen parameters.""",

    "integer_count": """# Task Specification: Integer Count
- Output: ask how many positive integers satisfy the stated conditions.
- Calculation: return {count: int}.
- Data Contract: `oracle_payload` may list valid_values for audit.""",

    "integer_exact_k": """# Task Specification: Integer Exact k
- Output: ask for exponent/generation count k.
- Calculation: return {k: int}.
- Data Contract: `oracle_payload` must equal the frozen parameters.""",

    "exact_fraction_canonical": """# Task Specification: Exact Fraction Canonical
- Output: ask for an irreducible fraction in LaTeX-capable form.
- Calculation: return numerator, denominator, canonical_latex.
- Data Contract: `oracle_payload` must equal the frozen parameters.""",

    "radical_simplification_canonical": """# Task Specification: Radical Simplification Canonical
- Output: ask for simplest radical form with canonical_latex.
- Calculation: return coefficient, radicand, canonical_latex.
- Data Contract: `oracle_payload` must equal the frozen parameters.""",

    "compound_radical_result": """# Task Specification: Compound Radical Result
- Output: ask for an exact compound radical value.
- Calculation: return result={rational, radical_coefficient, radicand, canonical_latex}.
- Comparison uses structured fields; latex is not the sole judge.
- Data Contract: `oracle_payload` may nest larger_root/smaller_root compounds."""
}

POLYNOMIAL_DIVISION_CONTRACT = """Required return schema:
{
  "question_text": str,
  "correct_answer": {
      "quotient_coefficients": list[int | str],  # coefficients of the quotient (integers or fraction strings "p/q")
      "remainder": int | str                    # remainder of the division (integer or fraction string "p/q")
  },
  "oracle_payload": dict
}
- Formatting rules: Output integers directly, or irreducible fraction strings in the format "p/q" if fractional. Do not use float values.
- Equality: Exact matching via dictionary structure. No tolerance."""

RPM_CIRCUMFERENCE_CONTRACT = """Required return schema:
{
  "question_text": str,
  "correct_answer": {
      "coefficient": str,  # speed coefficient for 1 rpm in the format "p/q" (reduced fraction string, or "n" if denominator is 1)
      "unit": str          # must be exactly "km/h"
  },
  "oracle_payload": dict
}
- Formatting rules: Reduce the fraction completely. Output integer if the denominator is 1.
- Equality: Exact dictionary match. No tolerance."""

LARGEST_PROPER_DIVISOR_CONTRACT = """Required return schema:
{
  "question_text": str,
  "correct_answer": {
      "claims": list[bool]  # boolean list indicating the truth value of the necessity claims in the frozen order
  },
  "oracle_payload": dict
}
- Formatting rules: boolean values (True or False) only.
- Equality: Exact dictionary match. No tolerance."""

ALTERNATING_SEQUENCE_CONTRACT = """Required return schema:
{
  "question_text": str,
  "correct_answer": {
      "specified_session_laps": int,  # laps completed in the specified week and day
      "first_exceed_week": int,        # 1-indexed week number when the total distance first exceeds threshold_km
      "first_exceed_day": str         # day label of the first exceed session
  },
  "oracle_payload": dict
}
- Formatting rules: match day label strings exactly from the list provided.
- Equality: Exact dictionary match. No tolerance."""

COMMON_FACTOR_QUADRATIC_ROOT_ORDERING_CONTRACT = """Required return schema:
{
  "question_text": str,
  "correct_answer": {
      "roots": list[int | str],  # the two distinct roots ordered as a>b (a first, then b)
      "a": int | str,            # larger root under root_order a>b
      "b": int | str,            # smaller root under root_order a>b
      "value": int | str         # exact linear combination coeff_a*a + coeff_b*b; irreducible "p/q" if fractional
  },
  "oracle_payload": dict
}
- Formatting rules: exact arithmetic only; integers directly, irreducible "p/q" strings when fractional; no float values.
- Ordering: a must be strictly greater than b; roots must equal [a, b].
- Equality: Exact dictionary match. No tolerance."""

RADICAL_SIMPLIFICATION_CONTRACT = """Required return schema:
{
  "question_text": str,
  "correct_answer": {
      "coefficient": int,  # simplified positive integer coefficient outside the square root
      "radicand": int      # square-free integer remaining under the square root (> 1)
  },
  "oracle_payload": dict
}
- Formatting rules: integers only; the radicand must be square-free; do not use float values.
- Equality: Exact dictionary match. No tolerance."""

EXACT_RATIONAL_EXPRESSION_CONTRACT = """Required return schema:
{
  "question_text": str,
  "correct_answer": {
      "value": str  # canonical exact value: integer string, or irreducible "p/q" with positive denominator
  },
  "oracle_payload": dict
}
- Formatting rules: reduce completely; output the integer string if the denominator is 1; never use decimal or float approximations.
- Equality: Exact dictionary match. No tolerance."""

POLYNOMIAL_DIVISION_GENERAL_CONTRACT = """Required return schema:
{
  "question_text": str,
  "correct_answer": {
      "quotient_coefficients": list[int | str],   # highest degree first; integers, or irreducible fraction strings "p/q"
      "remainder_coefficients": list[int | str]   # coefficients of the remainder (degree < divisor degree; one value for a linear divisor)
  },
  "oracle_payload": dict
}
- Formatting rules: exact arithmetic only; integers directly, irreducible "p/q" strings when fractional; no float values.
- Equality: Exact dictionary match. No tolerance."""

POLYNOMIAL_FACTOR_ROOTS_CONTRACT = """Required return schema:
{
  "question_text": str,
  "correct_answer": {
      "roots": list[int | str]  # the two distinct roots in ascending numeric order; integers, or irreducible fraction strings "p/q"
  },
  "oracle_payload": dict
}
- Formatting rules: ascending order; exact values only; irreducible "p/q" with positive denominator when fractional; no float values.
- Equality: Exact dictionary match. No tolerance."""

EXAM_POWER_CONTRACT = """Required return schema:
{
  "question_text": str,
  "correct_answer": {"base": int, "exponent": int | str},
  "oracle_payload": dict
}
- Equality: Exact dictionary match."""

EXAM_POLY_SIMPLIFY_CONTRACT = """Required return schema:
{
  "question_text": str,
  "correct_answer": {"coefficients": {"2": int|str, "1": int|str, "0": int|str}},
  "oracle_payload": dict
}
- Degree keys are strings. Exact arithmetic only. Exact dictionary match."""

EXAM_LINEAR_SYSTEM_CONTRACT = """Required return schema:
{
  "question_text": str,
  "correct_answer": {"x": int|str, "y": int|str, "value": int|str},
  "oracle_payload": dict
}
- Exact rationals as int or irreducible "p/q". Exact dictionary match."""

EXAM_RADICAL_PRODUCT_CONTRACT = """Required return schema:
{
  "question_text": str,
  "correct_answer": {"terms": [{"coefficient": int|str, "radicand": int}, ...]},
  "oracle_payload": dict
}
- Simplify square factors; merge like radicands; sort by increasing radicand. Exact match on normalized terms."""

EXAM_FACTORIZATION_CONTRACT = """Required return schema:
{
  "question_text": str,
  "correct_answer": {"factors": [{"x_coefficient": int|str, "constant": int|str}, {"x_coefficient": int|str, "constant": int|str}]},
  "oracle_payload": dict
}
- Factor order may vary; oracle accepts algebraically equivalent linear-factor pairs (not string-only)."""

EXAM_RATIONALIZE_CONTRACT = """Required return schema:
{
  "question_text": str,
  "correct_answer": {"a": int, "b": int, "radicand": int, "value": int},
  "oracle_payload": dict
}
- Exact dictionary match."""

MATH16_POLY_DIV_CONTRACT = """Required return schema:
{
  "question_text": str,
  "correct_answer": {
    "quotient_coefficients": list,
    "remainder_coefficients": list,
    "quotient_latex": str,
    "remainder_latex": str
  },
  "oracle_payload": dict
}
- question_text must use formal LaTeX (\\( \\) / \\[ \\]). Structural fields are scored; latex fields required."""

MATH16_FACTOR_ROOTS_CONTRACT = """Required return schema:
{
  "question_text": str,
  "correct_answer": {
    "roots": list,
    "factorization_latex": str,
    "roots_latex": str
  },
  "oracle_payload": dict
}
- question_text must use formal LaTeX. roots ordered ascending."""

MATH16_EXACT_RATIONAL_CONTRACT = """Required return schema:
{
  "question_text": str,
  "correct_answer": {"value": str, "canonical_latex": str},
  "oracle_payload": dict
}
- Exact rational value plus canonical_latex. No floats."""

MATH16_RADICAL_CONTRACT = """Required return schema:
{
  "question_text": str,
  "correct_answer": {"coefficient": int, "radicand": int, "canonical_latex": str},
  "oracle_payload": dict
}
- Simplest radical form with canonical_latex."""

POLY_REMAINDER_ONLY_CONTRACT = """Required return schema:
{
  "question_text": str,
  "correct_answer": {"remainder": str, "canonical_latex": str},
  "oracle_payload": dict
}
- Score remainder only; do not require quotient in correct_answer."""

FACTOR_PARAM_RECOVERY_CONTRACT = """Required return schema:
{
  "question_text": str,
  "correct_answer": int,
  "oracle_payload": dict
}
- factor_order_policy=strict_source_template; first factor fixed as (3x+a). Return integer a+2c."""

INTEGER_EXACT_CONTRACT = """Required return schema:
{
  "question_text": str,
  "correct_answer": int,
  "oracle_payload": dict
}
- Exact integer match."""

INTEGER_COUNT_CONTRACT = """Required return schema:
{
  "question_text": str,
  "correct_answer": {"count": int},
  "oracle_payload": dict
}
- Exact count match."""

INTEGER_EXACT_K_CONTRACT = """Required return schema:
{
  "question_text": str,
  "correct_answer": {"k": int},
  "oracle_payload": dict
}
- Exact k match."""

EXACT_FRACTION_CANONICAL_CONTRACT = """Required return schema:
{
  "question_text": str,
  "correct_answer": {"numerator": int, "denominator": int, "canonical_latex": str},
  "oracle_payload": dict
}
- Irreducible fraction; structural Fraction equality plus canonical_latex."""

RADICAL_CANONICAL_CONTRACT = """Required return schema:
{
  "question_text": str,
  "correct_answer": {"coefficient": int, "radicand": int, "canonical_latex": str},
  "oracle_payload": dict
}
- Square-free radicand; structural match plus canonical_latex."""

COMPOUND_RADICAL_CONTRACT = """Required return schema:
{
  "question_text": str,
  "correct_answer": {
    "result": {
      "rational": int,
      "radical_coefficient": int,
      "radicand": int,
      "canonical_latex": str
    }
  },
  "oracle_payload": dict
}
- Structured comparison on (rational, radical_coefficient, radicand). Accepts +1/-1 coefficients. Not string-only."""

CONTRACTS: Mapping[str, str] = {
    "radical_simplification": RADICAL_SIMPLIFICATION_CONTRACT,
    "exact_rational_expression": EXACT_RATIONAL_EXPRESSION_CONTRACT,
    "polynomial_division_general": POLYNOMIAL_DIVISION_GENERAL_CONTRACT,
    "polynomial_factor_roots": POLYNOMIAL_FACTOR_ROOTS_CONTRACT,
    "polynomial_division_exact": POLYNOMIAL_DIVISION_CONTRACT,
    "rpm_circumference_kph": RPM_CIRCUMFERENCE_CONTRACT,
    "largest_proper_divisor_logic": LARGEST_PROPER_DIVISOR_CONTRACT,
    "alternating_sequence_threshold": ALTERNATING_SEQUENCE_CONTRACT,
    "common_factor_quadratic_root_ordering": COMMON_FACTOR_QUADRATIC_ROOT_ORDERING_CONTRACT,
    "exam_power_of_same_base": EXAM_POWER_CONTRACT,
    "exam_polynomial_simplify": EXAM_POLY_SIMPLIFY_CONTRACT,
    "exam_linear_system_linear_combination": EXAM_LINEAR_SYSTEM_CONTRACT,
    "exam_radical_product_simplified": EXAM_RADICAL_PRODUCT_CONTRACT,
    "exam_factorization_common_binomial": EXAM_FACTORIZATION_CONTRACT,
    "exam_rationalize_conjugate": EXAM_RATIONALIZE_CONTRACT,
    "math16_polynomial_division_general": MATH16_POLY_DIV_CONTRACT,
    "math16_polynomial_factor_roots": MATH16_FACTOR_ROOTS_CONTRACT,
    "math16_exact_rational_expression": MATH16_EXACT_RATIONAL_CONTRACT,
    "math16_radical_simplification": MATH16_RADICAL_CONTRACT,
    "polynomial_division_remainder_only": POLY_REMAINDER_ONLY_CONTRACT,
    "polynomial_factor_parameter_recovery": FACTOR_PARAM_RECOVERY_CONTRACT,
    "integer_exact": INTEGER_EXACT_CONTRACT,
    "integer_count": INTEGER_COUNT_CONTRACT,
    "integer_exact_k": INTEGER_EXACT_K_CONTRACT,
    "exact_fraction_canonical": EXACT_FRACTION_CANONICAL_CONTRACT,
    "radical_simplification_canonical": RADICAL_CANONICAL_CONTRACT,
    "compound_radical_result": COMPOUND_RADICAL_CONTRACT,
}


def render_answer_contract(task_metadata: Mapping[str, Any], frozen_payload: Mapping[str, Any] | None = None) -> str:
    if not isinstance(task_metadata, Mapping):
        raise ValueError("ANSWER_CONTRACT_NOT_FOUND")
    oracle_type = task_metadata.get("oracle_type")
    if not oracle_type or oracle_type not in CONTRACTS:
        raise ValueError("ANSWER_CONTRACT_NOT_FOUND")

    parts = []

    # 1. Neutral task statement
    parts.append(NEUTRAL_TASK_STATEMENTS[oracle_type])

    # 2. Frozen sampled parameters
    if frozen_payload is not None:
        parts.append(f"Frozen sampled parameters:\n{json.dumps(frozen_payload, sort_keys=True)}\n\n`oracle_payload` must exactly equal the frozen sampled parameters above.")

    # 3. Generation output instructions (entry point + output format)
    parts.append(GENERATION_INSTRUCTIONS)

    # 4. Override statement (B1)
    parts.append(OVERRIDE_STATEMENT)

    # 5. Task-specific contract
    parts.append(CONTRACTS[oracle_type])

    return "\n\n" + "\n\n".join(parts) + "\n"
