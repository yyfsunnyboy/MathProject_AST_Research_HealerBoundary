"""CE115 clean incremental ablation prompt composition (Edge-AI compact).

Lineage
-------
Ab1  = BASE          (unchanged compact baseline from math_boundary_pilot)
Ab2g = BASE + GENERIC
Ab2d = BASE + GENERIC + DOMAIN

This is the single shared builder for Gemini and Qwen three-condition pilots.
Legacy assembly-v4 / freeze scaffolds are not used here; keep their artifacts
untouched as historical lineage.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any, Mapping

from agent_tools.finals_rebuild.math_boundary_pilot import build_ab1_prompt

LINEAGE_ID = "ce115_clean_incremental_ablation_v1"

GENERIC_SECTION_MARKER = "## Clean-incremental GENERIC"
DOMAIN_SECTION_MARKER = "## Clean-incremental DOMAIN"

# Domain-agnostic; identical for every task and for Ab2g/Ab2d.
GENERIC_BODY = (
    "Output complete Python source only. Do not use Markdown fences or explanatory prose. "
    "Preserve frozen parameters exactly. Verify that generate() exists. "
    "Verify that the return value has exactly the three required top-level keys. "
    "Verify field types match the stated contract and that oracle_payload equals the frozen parameters."
)

ADOPTION_RULE = (
    "Use the listed domain API for each supported core operation, and ensure the returned value "
    "contributes to correct_answer."
)

LIBRARY = "core.prompts.domain_function_library"

# Minimal sufficient APIs per task_id. No unrelated toolbox entries.
TASK_DOMAIN_APIS: dict[str, tuple[dict[str, str], ...]] = {
    "ce115_calc_polynomial_division_l1": (
        {
            "name": "PolynomialOps.div_qr",
            "import": LIBRARY,
            "signature": "(dividend_coefficients, divisor_coefficients)",
            "returns": "tuple[list, list]  # (quotient_coefficients, remainder_coefficients)",
            "necessity": "Sole supported primitive for exact polynomial quotient/remainder.",
        },
    ),
    "ce115_calc_radical_simplification_l1": (
        {
            "name": "RadicalOps.simplify_term",
            "import": LIBRARY,
            "signature": "(coeff, radicand)",
            "returns": "tuple[exact coefficient, int]  # (outer coefficient, square-free radicand)",
            "necessity": "Sole supported primitive for extracting square factors into coefficient/radicand.",
        },
    ),
    "ce115_calc_exact_rational_expression_l1": (
        {
            "name": "FractionOps.create",
            "import": LIBRARY,
            "signature": "(value)",
            "returns": "Fraction",
            "necessity": "Construct exact rationals from frozen decimal-string operands.",
        },
        {
            "name": "FractionOps.mul",
            "import": LIBRARY,
            "signature": "(a, b)",
            "returns": "Fraction",
            "necessity": "Form each term as sign * left * right with exact arithmetic.",
        },
        {
            "name": "FractionOps.add",
            "import": LIBRARY,
            "signature": "(a, b)",
            "returns": "Fraction",
            "necessity": "Accumulate the sum of product terms into the final exact value.",
        },
    ),
    "ce115_calc_polynomial_factor_roots_l1": (
        {
            "name": "PolynomialOps.factor_quadratic_exact",
            "import": LIBRARY,
            "signature": "(a, b, c)",
            "returns": "tuple of exact linear factors / roots",
            "necessity": "Sole supported primitive for exact quadratic factorization and roots.",
        },
        {
            "name": "FractionOps.create",
            "import": LIBRARY,
            "signature": "(value)",
            "returns": "Fraction",
            "necessity": "Represent exact root values without floating-point drift.",
        },
    ),
    "ce111_q02_polynomial_division_remainder": (
        {
            "name": "PolynomialOps.div_qr",
            "import": LIBRARY,
            "signature": "(dividend_coefficients, divisor_coefficients)",
            "returns": "tuple[list, list]  # (quotient_coefficients, remainder_coefficients)",
            "necessity": "Compute exact remainder; quotient is audit-only and not scored.",
        },
        {
            "name": "PolynomialOps.format_latex",
            "import": LIBRARY,
            "signature": "(coeffs, var='x')",
            "returns": "str",
            "necessity": "Render remainder polynomial into canonical_latex.",
        },
    ),
    "ce111_q08_polynomial_factor_parameter_recovery": (
        {
            "name": "PolynomialOps.mul",
            "import": LIBRARY,
            "signature": "(c1, c2)",
            "returns": "list",
            "necessity": "Expand (3x+a)(bx+c) under strict_source_template factor order.",
        },
        {
            "name": "FractionOps.create",
            "import": LIBRARY,
            "signature": "(value)",
            "returns": "Fraction",
            "necessity": "Exact integer/rational parameter recovery without float drift.",
        },
    ),
    "ce111_q03_prime_factor_selection": (
        {
            "name": "IntegerOps.is_divisible",
            "import": LIBRARY,
            "signature": "(a, b)",
            "returns": "bool",
            "necessity": "Test which candidate divides 156 as a prime factor.",
        },
        {
            "name": "IntegerOps.safe_eval",
            "import": LIBRARY,
            "signature": "(expr)",
            "returns": "exact numeric value",
            "necessity": "Evaluate integer checks without unsafe builtins.",
        },
    ),
    "ce112_q01_negative_integer_power": (
        {
            "name": "IntegerOps.safe_eval",
            "import": LIBRARY,
            "signature": "(expr)",
            "returns": "exact numeric value",
            "necessity": "Evaluate (-3)**3 exactly with safe integer arithmetic.",
        },
        {
            "name": "IntegerOps.fmt_num",
            "import": LIBRARY,
            "signature": "(n)",
            "returns": "str",
            "necessity": "Preserve signed-base formatting for negative integer powers.",
        },
    ),
    "ce112_q09_divisor_multiple_intersection": (
        {
            "name": "IntegerOps.is_divisible",
            "import": LIBRARY,
            "signature": "(a, b)",
            "returns": "bool",
            "necessity": "Identify positive integers that are multiples of 18 and divisors of 216.",
        },
        {
            "name": "IntegerOps.safe_eval",
            "import": LIBRARY,
            "signature": "(expr)",
            "returns": "exact numeric value",
            "necessity": "Count qualifying integers with exact arithmetic only.",
        },
    ),
    "ce111_nonchoice_q01_part1_exponential_growth": (
        {
            "name": "IntegerOps.safe_eval",
            "import": LIBRARY,
            "signature": "(expr)",
            "returns": "exact numeric value",
            "necessity": "Compute generation count k from 20-hour splits over 15 days.",
        },
        {
            "name": "IntegerOps.fmt_num",
            "import": LIBRARY,
            "signature": "(n)",
            "returns": "str",
            "necessity": "Format exact integer exponent k without float coercion.",
        },
    ),
    "ce111_q05_exact_fraction_expression": (
        {
            "name": "FractionOps.create",
            "import": LIBRARY,
            "signature": "(value)",
            "returns": "Fraction",
            "necessity": "Construct exact fraction operands from the frozen expression.",
        },
        {
            "name": "FractionOps.add",
            "import": LIBRARY,
            "signature": "(a, b)",
            "returns": "Fraction",
            "necessity": "Accumulate the exact signed fraction expression.",
        },
        {
            "name": "FractionOps.to_latex",
            "import": LIBRARY,
            "signature": "(val, mixed=False)",
            "returns": "str",
            "necessity": "Emit canonical_latex for the irreducible result.",
        },
    ),
    "ce113_q01_negative_fraction_subtraction": (
        {
            "name": "FractionOps.create",
            "import": LIBRARY,
            "signature": "(value)",
            "returns": "Fraction",
            "necessity": "Construct exact operands including negative fractions.",
        },
        {
            "name": "FractionOps.sub",
            "import": LIBRARY,
            "signature": "(a, b)",
            "returns": "Fraction",
            "necessity": "Evaluate 3/7 - (-1/4) with exact arithmetic.",
        },
        {
            "name": "FractionOps.to_latex",
            "import": LIBRARY,
            "signature": "(val, mixed=False)",
            "returns": "str",
            "necessity": "Emit canonical_latex for the irreducible result.",
        },
    ),
    "ce112_q12_independent_probability_fraction": (
        {
            "name": "FractionOps.create",
            "import": LIBRARY,
            "signature": "(value)",
            "returns": "Fraction",
            "necessity": "Construct exact probability factors 2/6 and 1/5.",
        },
        {
            "name": "FractionOps.mul",
            "import": LIBRARY,
            "signature": "(a, b)",
            "returns": "Fraction",
            "necessity": "Multiply independent probabilities into an irreducible fraction.",
        },
        {
            "name": "FractionOps.to_latex",
            "import": LIBRARY,
            "signature": "(val, mixed=False)",
            "returns": "str",
            "necessity": "Emit canonical_latex for the probability product.",
        },
    ),
    "ce112_q04_radical_simplification": (
        {
            "name": "RadicalOps.simplify_term",
            "import": LIBRARY,
            "signature": "(coeff, radicand)",
            "returns": "tuple[exact coefficient, int]",
            "necessity": "Extract square factors from sqrt(135) into coefficient/radicand.",
        },
        {
            "name": "RadicalOps.to_latex",
            "import": LIBRARY,
            "signature": "(expr)",
            "returns": "str",
            "necessity": "Emit canonical_latex for the simplified radical.",
        },
    ),
    "ce111_q10_ordered_quadratic_roots_radical": (
        {
            "name": "RadicalOps.simplify_term",
            "import": LIBRARY,
            "signature": "(coeff, radicand)",
            "returns": "tuple[exact coefficient, int]",
            "necessity": "Keep exact ±sqrt(3) coefficients for ordered roots.",
        },
        {
            "name": "FractionOps.create",
            "import": LIBRARY,
            "signature": "(value)",
            "returns": "Fraction",
            "necessity": "Combine rational parts when forming 2a+b as a compound radical.",
        },
        {
            "name": "RadicalOps.to_latex",
            "import": LIBRARY,
            "signature": "(expr)",
            "returns": "str",
            "necessity": "Emit canonical_latex for the compound radical result.",
        },
    ),
    "ce113_q11_rationalize_denominator": (
        {
            "name": "FractionOps.create",
            "import": LIBRARY,
            "signature": "(value)",
            "returns": "Fraction",
            "necessity": "Exact rational arithmetic while rationalizing.",
        },
        {
            "name": "FractionOps.mul",
            "import": LIBRARY,
            "signature": "(a, b)",
            "returns": "Fraction",
            "necessity": "Multiply by the conjugate numerator/denominator.",
        },
        {
            "name": "FractionOps.add",
            "import": LIBRARY,
            "signature": "(a, b)",
            "returns": "Fraction",
            "necessity": "Form a+b from the simplified a + b*sqrt(7).",
        },
    ),
    "ce115_calc_common_factor_quadratic_root_ordering_l1": (
        {
            "name": "FractionOps.create",
            "import": LIBRARY,
            "signature": "(value)",
            "returns": "Fraction",
            "necessity": "Construct exact root values from the two linear factors.",
        },
        {
            "name": "FractionOps.mul",
            "import": LIBRARY,
            "signature": "(a, b)",
            "returns": "Fraction",
            "necessity": "Scale ordered roots by the frozen linear-combination coefficients.",
        },
        {
            "name": "FractionOps.add",
            "import": LIBRARY,
            "signature": "(a, b)",
            "returns": "Fraction",
            "necessity": "Accumulate the exact linear combination into correct_answer.value.",
        },
    ),
    # 113/114 exam external validation (minimal DOMAIN; GENERIC unchanged).
    "ce115_ext_114_01_power_laws_l1": (
        {
            "name": "FractionOps.create",
            "import": LIBRARY,
            "signature": "(value)",
            "returns": "Fraction",
            "necessity": "Construct exact exponent contributions from each same-base power.",
        },
        {
            "name": "FractionOps.add",
            "import": LIBRARY,
            "signature": "(a, b)",
            "returns": "Fraction",
            "necessity": "Combine exponents for multiply (+) and divide (−) of same-base powers.",
        },
    ),
    "ce115_ext_114_02_polynomial_simplify_l1": (
        {
            "name": "FractionOps.create",
            "import": LIBRARY,
            "signature": "(value)",
            "returns": "Fraction",
            "necessity": "Exact coefficient arithmetic while expanding/combining like terms.",
        },
        {
            "name": "FractionOps.add",
            "import": LIBRARY,
            "signature": "(a, b)",
            "returns": "Fraction",
            "necessity": "Accumulate like-term coefficients into the simplified polynomial.",
        },
    ),
    "ce115_ext_114_04_linear_system_l1": (
        {
            "name": "FractionOps.create",
            "import": LIBRARY,
            "signature": "(value)",
            "returns": "Fraction",
            "necessity": "Exact rational coefficients for elimination/substitution.",
        },
        {
            "name": "FractionOps.mul",
            "import": LIBRARY,
            "signature": "(a, b)",
            "returns": "Fraction",
            "necessity": "Scale equations and evaluate the linear combination.",
        },
        {
            "name": "FractionOps.add",
            "import": LIBRARY,
            "signature": "(a, b)",
            "returns": "Fraction",
            "necessity": "Combine equation sides and accumulate x+2y.",
        },
    ),
    "ce115_ext_114_08_radical_product_l1": (
        {
            "name": "RadicalOps.simplify_term",
            "import": LIBRARY,
            "signature": "(coeff, radicand)",
            "returns": "tuple[exact coefficient, int]  # (outer coefficient, square-free radicand)",
            "necessity": "Extract square factors after multiplying/distributing radicals.",
        },
    ),
    "ce115_ext_113_10_factorization_l1": (
        {
            "name": "FractionOps.create",
            "import": LIBRARY,
            "signature": "(value)",
            "returns": "Fraction",
            "necessity": "Exact arithmetic for factor coefficients.",
        },
        {
            "name": "FractionOps.mul",
            "import": LIBRARY,
            "signature": "(a, b)",
            "returns": "Fraction",
            "necessity": "Scale binomial coefficients while completing factorization.",
        },
    ),
    "ce115_ext_113_11_rationalize_l1": (
        {
            "name": "FractionOps.create",
            "import": LIBRARY,
            "signature": "(value)",
            "returns": "Fraction",
            "necessity": "Exact rational arithmetic while rationalizing.",
        },
        {
            "name": "FractionOps.mul",
            "import": LIBRARY,
            "signature": "(a, b)",
            "returns": "Fraction",
            "necessity": "Multiply by the conjugate numerator/denominator.",
        },
        {
            "name": "FractionOps.add",
            "import": LIBRARY,
            "signature": "(a, b)",
            "returns": "Fraction",
            "necessity": "Form a+b from the simplified a + b*sqrt(7).",
        },
    ),
}

GENERIC_BUDGET = (250, 400)
# Floor ~350 allows a single necessary API; ceiling 900 is hard (DOMAIN_BUDGET_EXCEEDED).
DOMAIN_BUDGET = (350, 900)

FORBIDDEN_BASELINE_MARKERS = (
    "Generic Safety-and-Format Scaffold",
    "Clean-incremental GENERIC",
    "Clean-incremental DOMAIN",
    "Domain API",
    "Available Domain APIs",
    "PolynomialOps",
    "FractionOps",
    "RadicalOps",
    "RadicalLogicEngine",
    "Ab1 answer-contract wording",
    "Ab2g scaffold",
    "CE115 Ab2d-Assembly domain contract",
)

FORBIDDEN_AB2G_DOMAIN_MARKERS = (
    "PolynomialOps",
    "FractionOps",
    "RadicalOps",
    "RadicalLogicEngine",
    "domain_function_library",
    "Available Domain APIs",
    "Clean-incremental DOMAIN",
)


def prompt_sha256(text: str) -> str:
    """SHA-256 of a canonical in-memory prompt string (UTF-8)."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def universal_newlines(text: str) -> str:
    """Normalize CRLF/CR to LF. Does not claim byte-identity with on-disk files."""
    return text.replace("\r\n", "\n").replace("\r", "\n")


def file_byte_hash(path: str | Path) -> str:
    """SHA-256 of on-disk raw bytes (no newline normalization)."""
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def canonical_text_hash(text: str) -> str:
    """SHA-256 of UTF-8 text after universal-newline normalization."""
    return hashlib.sha256(universal_newlines(text).encode("utf-8")).hexdigest()


def canonical_file_text_hash(path: str | Path) -> str:
    """SHA-256 of on-disk file decoded as UTF-8 then universal-newline normalized."""
    return canonical_text_hash(Path(path).read_bytes().decode("utf-8"))


def canonical_prompt_hash(text: str) -> str:
    """Preferred name for the hash of the builder-emitted prompt string.

    Builder strings already use LF; for on-disk prompt.txt prefer
    ``canonical_file_text_hash`` (universal-newline) vs ``prompt_file_byte_hash``.
    """
    return prompt_sha256(text)


def prompt_file_byte_hash(path: str | Path) -> str:
    """SHA-256 of on-disk prompt file bytes (may differ from canonical string hash)."""
    return file_byte_hash(path)


CANONICALIZATION_DEFINITION = (
    "SHA-256 of UTF-8 text after universal-newline normalization "
    "(CRLF/CR -> LF); does not claim byte-identity with on-disk files."
)


def generic_section() -> str:
    """Single shared GENERIC block (marker + body). Identical for all tasks."""
    return f"{GENERIC_SECTION_MARKER}\n{GENERIC_BODY}"


def domain_section(task_id: str) -> str:
    """Task-local DOMAIN block only. Raises DOMAIN_BUDGET_EXCEEDED if too large."""
    apis = TASK_DOMAIN_APIS.get(task_id)
    if not apis:
        raise KeyError(f"no clean-incremental DOMAIN mapping for task_id={task_id!r}")
    lines = [
        DOMAIN_SECTION_MARKER,
        "Task-local domain APIs (use only these):",
    ]
    for api in apis:
        lines.append(
            f"- `{api['name']}` | import: `{api['import']}` | signature: `{api['signature']}` "
            f"| returns: {api['returns']}"
        )
    lines.append(ADOPTION_RULE)
    section = "\n".join(lines)
    n = len(section)
    if n > DOMAIN_BUDGET[1]:
        raise RuntimeError(
            f"DOMAIN_BUDGET_EXCEEDED: task={task_id} domain_chars={n} "
            f"budget_max={DOMAIN_BUDGET[1]} (necessary APIs not trimmed)"
        )
    return section


def build_base_prompt(task: Mapping[str, Any], frozen: Mapping[str, Any]) -> str:
    """Ab1 BASE — delegates to unchanged compact builder."""
    return build_ab1_prompt(dict(task), dict(frozen))


def build_ab2g_clean_prompt(task: Mapping[str, Any], frozen: Mapping[str, Any]) -> str:
    base = build_base_prompt(task, frozen)
    generic = generic_section()
    if not (GENERIC_BUDGET[0] <= len(generic) <= GENERIC_BUDGET[1]):
        raise RuntimeError(
            f"GENERIC budget miss: chars={len(generic)} allowed={GENERIC_BUDGET}"
        )
    return f"{base}\n\n{generic}"


def build_ab2d_clean_prompt(task: Mapping[str, Any], frozen: Mapping[str, Any]) -> str:
    ab2g = build_ab2g_clean_prompt(task, frozen)
    domain = domain_section(str(task["task_id"]))
    return f"{ab2g}\n\n{domain}"


def build_condition_prompt(
    condition: str,
    task: Mapping[str, Any],
    frozen: Mapping[str, Any],
) -> str:
    if condition == "ab1":
        return build_base_prompt(task, frozen)
    if condition == "ab2g":
        return build_ab2g_clean_prompt(task, frozen)
    if condition == "ab2d":
        return build_ab2d_clean_prompt(task, frozen)
    raise ValueError(f"unsupported condition: {condition!r}")


def strip_generic_section(prompt: str) -> str:
    marker = f"\n\n{GENERIC_SECTION_MARKER}"
    if marker not in prompt:
        raise ValueError("GENERIC section marker missing")
    head, _, _ = prompt.partition(marker)
    return head


def strip_domain_section(prompt: str) -> str:
    marker = f"\n\n{DOMAIN_SECTION_MARKER}"
    if marker not in prompt:
        raise ValueError("DOMAIN section marker missing")
    head, _, _ = prompt.partition(marker)
    return head


def extract_generic_section(prompt: str) -> str:
    marker = f"\n\n{GENERIC_SECTION_MARKER}"
    if marker not in prompt:
        raise ValueError("GENERIC section marker missing")
    _, _, rest = prompt.partition(marker)
    # rest starts with body after marker line already consumed? partition keeps marker out of rest
    # Actually partition(marker) where marker is "\n\n## Clean-incremental GENERIC"
    # rest is "\n{BODY}\n\n## DOMAIN..." or "\n{BODY}"
    section = GENERIC_SECTION_MARKER + rest
    domain_marker = f"\n\n{DOMAIN_SECTION_MARKER}"
    if domain_marker in section:
        section, _, _ = section.partition(domain_marker)
    return section


def extract_domain_section(prompt: str) -> str:
    marker = f"\n\n{DOMAIN_SECTION_MARKER}"
    if marker not in prompt:
        raise ValueError("DOMAIN section marker missing")
    _, _, rest = prompt.partition(marker)
    return DOMAIN_SECTION_MARKER + rest


def section_identity(prompt: str, condition: str) -> dict[str, Any]:
    base_end = prompt.find(f"\n\n{GENERIC_SECTION_MARKER}")
    if condition == "ab1":
        return {
            "lineage": LINEAGE_ID,
            "condition": condition,
            "has_generic": False,
            "has_domain": False,
            "base_chars": len(prompt),
            "generic_chars": 0,
            "domain_chars": 0,
            "total_chars": len(prompt),
            "total_lines": prompt.count("\n") + 1,
            "canonical_prompt_hash": prompt_sha256(prompt),
            # Deprecated alias — same value as canonical_prompt_hash.
            "prompt_hash": prompt_sha256(prompt),
        }
    if base_end < 0:
        raise ValueError("expected GENERIC marker for non-Ab1 prompt")
    base = prompt[:base_end]
    generic = extract_generic_section(prompt)
    domain = extract_domain_section(prompt) if condition == "ab2d" else ""
    return {
        "lineage": LINEAGE_ID,
        "condition": condition,
        "has_generic": True,
        "has_domain": condition == "ab2d",
        "base_chars": len(base),
        "generic_chars": len(generic),
        "domain_chars": len(domain),
        "total_chars": len(prompt),
        "total_lines": prompt.count("\n") + 1,
        "canonical_prompt_hash": prompt_sha256(prompt),
        "prompt_hash": prompt_sha256(prompt),
        "generic_hash": prompt_sha256(generic),
        "domain_hash": prompt_sha256(domain) if domain else None,
    }


def assert_clean_ablation_invariants(
    task: Mapping[str, Any],
    frozen: Mapping[str, Any],
) -> dict[str, str]:
    """Raise AssertionError on any clean-ablation violation; return prompts."""
    ab1 = build_condition_prompt("ab1", task, frozen)
    ab2g = build_condition_prompt("ab2g", task, frozen)
    ab2d = build_condition_prompt("ab2d", task, frozen)

    assert strip_generic_section(ab2g) == ab1
    assert strip_domain_section(ab2d) == ab2g
    assert extract_generic_section(ab2g) == extract_generic_section(ab2d)
    assert extract_generic_section(ab2g) == generic_section()
    assert ab2g.startswith(ab1)
    assert ab2d.startswith(ab2g)

    for marker in FORBIDDEN_BASELINE_MARKERS:
        assert marker not in ab1, f"Ab1 contaminated by {marker!r}"

    for marker in FORBIDDEN_AB2G_DOMAIN_MARKERS:
        assert marker not in ab2g, f"Ab2g contaminated by {marker!r}"

    assert "Ab1 answer-contract wording" not in ab2d
    assert "Ab2g scaffold" not in ab2d
    assert "CE115 Ab2d-Assembly domain contract" not in ab2d
    assert "Available Domain APIs" not in ab2d  # full-toolbox label
    # Only task-local names may appear
    allowed_names = {api["name"].split(".")[0] for api in TASK_DOMAIN_APIS[str(task["task_id"])]}
    for name in ("PolynomialOps", "FractionOps", "RadicalOps", "RadicalLogicEngine"):
        if name not in allowed_names:
            assert name not in ab2d, f"unrelated API family {name} in DOMAIN"

    generic = extract_generic_section(ab2g)
    domain = extract_domain_section(ab2d)
    assert GENERIC_BUDGET[0] <= len(generic) <= GENERIC_BUDGET[1]
    assert DOMAIN_BUDGET[0] <= len(domain) <= DOMAIN_BUDGET[1]

    return {"ab1": ab1, "ab2g": ab2g, "ab2d": ab2d}
