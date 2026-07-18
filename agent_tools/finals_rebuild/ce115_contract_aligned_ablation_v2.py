"""CE115 contract-aligned ablation v2 (exam external-validation lineage).

Preserves v1 clean-incremental GENERIC_BODY byte-identity and does not mutate
v1 TASK_DOMAIN_APIS / hashes. v2 adds contract-aligned BASE wording (esp. 114-02
nested coefficients) and production-matched DOMAIN APIs.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Mapping

from agent_tools.finals_rebuild.ce115_clean_incremental_ablation import (
    GENERIC_BODY,
    GENERIC_SECTION_MARKER,
    LIBRARY,
)
from agent_tools.finals_rebuild.math_boundary_pilot import build_ab1_prompt

LINEAGE_ID = "ce115_contract_aligned_ablation_v2"

DOMAIN_SECTION_MARKER = "## Clean-incremental DOMAIN"
GENERIC_SECTION_MARKER_V2 = GENERIC_SECTION_MARKER  # identical marker text

# Frozen GENERIC — must stay byte-identical to v1 GENERIC_BODY.
assert GENERIC_BODY.startswith("Output complete Python source only.")

ADOPTION_RULE_REQUIRED = (
    "Use the listed domain API for each supported core operation, and ensure the returned value "
    "contributes to correct_answer. Do not invent APIs. Do not call unrelated APIs unless listed."
)

ADOPTION_RULE_OPTIONAL_INTEGER = (
    "Adoption of listed IntegerOps is optional: plain exact int arithmetic is acceptable. "
    "If you call a listed API, its return must contribute to correct_answer. Do not invent APIs."
)

GENERIC_BUDGET = (250, 400)
DOMAIN_BUDGET = (350, 2200)

# Per-task DOMAIN: name/import/signature/returns must match production.
# adoption: "required" | "optional"
TASK_DOMAIN_APIS: dict[str, tuple[dict[str, str], ...]] = {
    "ce115_ext_114_01_power_laws_l1": (
        {
            "name": "IntegerOps.add",
            "import": LIBRARY,
            "signature": "(a, b)",
            "returns": "int",
            "notes": "Legal: int (not bool). Illegal: float/str/Fraction.",
            "necessity": "Optional helper to add exponents for same-base multiplication.",
            "adoption": "optional",
        },
        {
            "name": "IntegerOps.sub",
            "import": LIBRARY,
            "signature": "(a, b)",
            "returns": "int",
            "notes": "Legal: int (not bool). Illegal: float/str/Fraction.",
            "necessity": "Optional helper to subtract exponents for same-base division.",
            "adoption": "optional",
        },
    ),
    "ce115_ext_114_02_polynomial_simplify_l1": (
        {
            "name": "PolynomialOps.coeffs_from_py_expression",
            "import": LIBRARY,
            "signature": "(expression, var='x')",
            "returns": "list  # highest-degree-first coeffs (int or Fraction)",
            "notes": "Legal: restricted Python poly str with int/+-*/**/(). Illegal: float, calls.",
            "necessity": "Expand/simplify frozen polynomial expression to coefficient list.",
            "adoption": "required",
        },
        {
            "name": "PolynomialOps.to_degree_map",
            "import": LIBRARY,
            "signature": "(coeffs)",
            "returns": "dict[str, int|'p/q']  # degree-string keys",
            "notes": "Serialize coeffs for the nested coefficients map.",
            "necessity": "Build the degree map placed under correct_answer['coefficients'].",
            "adoption": "required",
        },
    ),
    "ce115_ext_114_04_linear_system_l1": (
        {
            "name": "LinearSystemOps.solve_2x2",
            "import": LIBRARY,
            "signature": "(a1, b1, c1, a2, b2, c2)",
            "returns": "tuple[Fraction, Fraction]  # (x, y)",
            "notes": (
                "Legal coeffs: int, Fraction, or 'p/q' with positive denominator literal only. "
                "Raises on singular systems. Do not invent alternate solvers."
            ),
            "necessity": "Exact 2x2 solver (supports negative determinants without illegal string literals).",
            "adoption": "required",
        },
        {
            "name": "LinearSystemOps.evaluate_linear",
            "import": LIBRARY,
            "signature": "(x, y, cx=1, cy=0)",
            "returns": "Fraction",
            "notes": "Computes cx*x + cy*y exactly.",
            "necessity": "Evaluate the required linear combination of the solution.",
            "adoption": "required",
        },
        {
            "name": "FractionOps.from_parts",
            "import": LIBRARY,
            "signature": "(numerator, denominator=1)",
            "returns": "Fraction  # denominator normalized positive",
            "notes": (
                "Legal: int numerator/denominator. Illegal: str/float/bool. "
                "Generic example: from_parts(-4, -2) -> Fraction(2, 1). "
                "Prefer this over any signed-denominator string literal."
            ),
            "necessity": "Safe signed-int Fraction construction for exact leaves.",
            "adoption": "required",
        },
        {
            "name": "FractionOps.to_exact",
            "import": LIBRARY,
            "signature": "(value)",
            "returns": "int | 'p/q'",
            "notes": "JSON-compatible serialization; 'p/q' always has a positive denominator.",
            "necessity": "Serialize x, y, and value into contract leaves.",
            "adoption": "required",
        },
    ),
    "ce115_ext_114_08_radical_product_l1": (
        {
            "name": "RadicalOps.simplify_term",
            "import": LIBRARY,
            "signature": "(coeff, radicand)",
            "returns": "tuple[exact coefficient, int]  # (outer coeff, square-free radicand)",
            "notes": "Pulls square factors from radicand into coeff.",
            "necessity": "Simplify each product term after distributing.",
            "adoption": "required",
        },
        {
            "name": "RadicalOps.normalize_term_list",
            "import": LIBRARY,
            "signature": "(terms)",
            "returns": "list[{coefficient, radicand}]  # merged, sorted by radicand asc",
            "notes": "Accepts (c,r) pairs or dicts; coefficients JSON-exact via to_exact.",
            "necessity": "Merge like radicands and emit contract terms list.",
            "adoption": "required",
        },
    ),
    "ce115_ext_113_10_factorization_l1": (
        {
            "name": "PolynomialOps.coeffs_from_py_expression",
            "import": LIBRARY,
            "signature": "(expression, var='x')",
            "returns": "list  # highest-degree-first",
            "notes": "Expand frozen expression to quadratic coeffs.",
            "necessity": "Obtain a,b,c for factorization without hardcoding factors.",
            "adoption": "required",
        },
        {
            "name": "PolynomialOps.factor_quadratic_exact",
            "import": LIBRARY,
            "signature": "(a, b, c)",
            "returns": "list[2] of {x_coefficient, constant} as int|'p/q'",
            "notes": (
                "Raises if discriminant is not a perfect square over Q. "
                "Evaluator accepts mathematical equivalence: factor order may be swapped; "
                "multiplying both factors by -1 (overall sign flip) is equivalent."
            ),
            "necessity": "Reusable exact linear-factor factorization.",
            "adoption": "required",
        },
    ),
    "ce115_ext_113_11_rationalize_l1": (
        {
            "name": "RadicalOps.rationalize_linear_denominator",
            "import": LIBRARY,
            "signature": "(numerator, denom_rational, denom_radical_coeff, radicand)",
            "returns": "tuple[Fraction, Fraction, int]  # (a, b, r) for a + b*sqrt(r)",
            "notes": (
                "Denominator is defined as "
                "(denom_rational + denom_radical_coeff * sqrt(radicand)). "
                "Generic non-task examples: "
                "num/(p+q*sqrt(r)) -> (num, p, q, r); "
                "num/(p-q*sqrt(r)) -> (num, p, -q, r)."
            ),
            "necessity": "Reusable conjugate rationalization.",
            "adoption": "required",
        },
        {
            "name": "FractionOps.to_exact",
            "import": LIBRARY,
            "signature": "(value)",
            "returns": "int | 'p/q'",
            "notes": "Serialize a, b and a+b for JSON contract.",
            "necessity": "Exact JSON leaves for a, b, value.",
            "adoption": "required",
        },
    ),
}

# Backward-compatible alias used by older call sites in this module.
ADOPTION_RULE = ADOPTION_RULE_REQUIRED


FORBIDDEN_BASELINE_MARKERS = (
    "Generic Safety-and-Format Scaffold",
    "Clean-incremental GENERIC",
    "Clean-incremental DOMAIN",
    "Domain API",
    "Available Domain APIs",
    "PolynomialOps",
    "FractionOps",
    "RadicalOps",
    "LinearSystemOps",
    "IntegerOps",
    "RadicalLogicEngine",
    "Ab1 answer-contract wording",
    "Ab2g scaffold",
    "CE115 Ab2d-Assembly domain contract",
)

FORBIDDEN_AB2G_DOMAIN_MARKERS = (
    "PolynomialOps",
    "FractionOps",
    "RadicalOps",
    "LinearSystemOps",
    "IntegerOps",
    "RadicalLogicEngine",
    "domain_function_library",
    "Available Domain APIs",
    "Clean-incremental DOMAIN",
)

# Answer tokens that must not appear as solution leakage in DOMAIN text.
LEAKAGE_FORBIDDEN_IN_DOMAIN = (
    '"exponent": 8',
    '"2": 5',
    '"0": -4',
    '"x": 2',
    '"y": "7/2"',
    '"value": 9',
    "x_coefficient\": 5",
    "constant\": -2",
    '"a": 4',
    '"b": 1',
    "common factor",
    "5x-2",
)


def prompt_sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def universal_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def canonical_prompt_hash(text: str) -> str:
    return prompt_sha256(universal_newlines(text))


def generic_section() -> str:
    return f"{GENERIC_SECTION_MARKER}\n{GENERIC_BODY}"


def domain_section(task_id: str) -> str:
    apis = TASK_DOMAIN_APIS.get(task_id)
    if not apis:
        raise KeyError(f"no v2 DOMAIN mapping for task_id={task_id!r}")
    lines = [
        DOMAIN_SECTION_MARKER,
        "Task-local domain APIs (use only these; signatures match production):",
    ]
    for api in apis:
        adoption = api.get("adoption", "required")
        lines.append(
            f"- `{api['name']}` | import: `{api['import']}` | signature: `{api['signature']}` "
            f"| returns: {api['returns']} | adoption: {adoption}"
        )
        if api.get("notes"):
            lines.append(f"  notes: {api['notes']}")
    if task_id == "ce115_ext_114_01_power_laws_l1":
        lines.append(ADOPTION_RULE_OPTIONAL_INTEGER)
    else:
        lines.append(ADOPTION_RULE_REQUIRED)
    section = "\n".join(lines)
    n = len(section)
    if n > DOMAIN_BUDGET[1]:
        raise RuntimeError(
            f"DOMAIN_BUDGET_EXCEEDED: task={task_id} domain_chars={n} budget_max={DOMAIN_BUDGET[1]}"
        )
    if n < DOMAIN_BUDGET[0]:
        raise RuntimeError(
            f"DOMAIN_BUDGET_UNDERFLOW: task={task_id} domain_chars={n} budget_min={DOMAIN_BUDGET[0]}"
        )
    return section


def _v2_answer_contract_override(task: Mapping[str, Any]) -> str | None:
    """Contract-aligned BASE addenda that supersede ambiguous v1 wording."""
    oid = task.get("oracle_type")
    if oid == "exam_polynomial_simplify":
        return (
            "correct_answer must be a JSON-compatible dict with exactly one top-level key "
            "\"coefficients\"; its value is the degree-string map with keys '2','1','0' "
            "mapping to exact ints or irreducible p/q strings. Do not return a flat degree map "
            "as the top-level correct_answer. Exact arithmetic; no floats. "
        )
    if oid == "exam_linear_system_linear_combination":
        return (
            "correct_answer must be a JSON-compatible dict with exactly x, y, and value "
            "(ints or irreducible p/q strings with positive denominators). "
            "Never encode rationals as signed-denominator strings such as '-240/-120'. Exact arithmetic; no floats. "
        )
    if oid == "exam_power_of_same_base":
        return (
            "correct_answer must be a JSON-compatible dict with exactly base (int) and exponent "
            "(int or irreducible p/q string). Exact arithmetic; no floats. "
        )
    return None


def build_base_prompt_v2(task: Mapping[str, Any], frozen: Mapping[str, Any]) -> str:
    """Ab1-v2 BASE: start from compact builder, then apply contract-aligned overrides."""
    base = build_ab1_prompt(dict(task), dict(frozen))
    override = _v2_answer_contract_override(task)
    if not override:
        return base
    # Replace the first correct_answer contract sentence block for this oracle.
    pattern = r"correct_answer must be a JSON-compatible dict with exactly .+?Exact arithmetic; no floats\. "
    replaced, n = re.subn(pattern, override, base, count=1, flags=re.DOTALL)
    if n != 1:
        # Fallback: append override after generate() sentence if pattern drift.
        return base + "\n" + override
    return replaced


def build_ab2g_v2_prompt(task: Mapping[str, Any], frozen: Mapping[str, Any]) -> str:
    base = build_base_prompt_v2(task, frozen)
    generic = generic_section()
    if not (GENERIC_BUDGET[0] <= len(generic) <= GENERIC_BUDGET[1]):
        raise RuntimeError(f"GENERIC budget miss: chars={len(generic)} allowed={GENERIC_BUDGET}")
    return f"{base}\n\n{generic}"


def build_ab2d_v2_prompt(task: Mapping[str, Any], frozen: Mapping[str, Any]) -> str:
    ab2g = build_ab2g_v2_prompt(task, frozen)
    domain = domain_section(str(task["task_id"]))
    return f"{ab2g}\n\n{domain}"


def build_condition_prompt_v2(
    condition: str,
    task: Mapping[str, Any],
    frozen: Mapping[str, Any],
) -> str:
    key = condition.lower().replace("-", "")
    if key in {"ab1", "ab1v2"}:
        return build_base_prompt_v2(task, frozen)
    if key in {"ab2g", "ab2gv2"}:
        return build_ab2g_v2_prompt(task, frozen)
    if key in {"ab2d", "ab2dv2"}:
        return build_ab2d_v2_prompt(task, frozen)
    raise ValueError(f"unknown v2 condition: {condition}")


def assert_v2_ablation_invariants(task: Mapping[str, Any], frozen: Mapping[str, Any]) -> dict[str, str]:
    ab1 = build_base_prompt_v2(task, frozen)
    ab2g = build_ab2g_v2_prompt(task, frozen)
    ab2d = build_ab2d_v2_prompt(task, frozen)
    for marker in (
        "Clean-incremental GENERIC",
        "Clean-incremental DOMAIN",
        "PolynomialOps",
        "FractionOps",
        "RadicalOps",
        "LinearSystemOps",
        "IntegerOps",
        "domain_function_library",
        "Available Domain APIs",
    ):
        assert marker not in ab1, f"marker leaked into Ab1-v2: {marker}"
    for marker in FORBIDDEN_AB2G_DOMAIN_MARKERS:
        assert marker not in ab2g, f"DOMAIN marker in Ab2g-v2: {marker}"
    assert GENERIC_SECTION_MARKER in ab2g
    assert DOMAIN_SECTION_MARKER in ab2d
    assert GENERIC_BODY in ab2g and GENERIC_BODY in ab2d
    assert ab2d.startswith(ab2g)
    if task.get("oracle_type") == "exam_polynomial_simplify":
        assert 'exactly one top-level key "coefficients"' in ab1
        assert "flat degree map" in ab1
    domain = domain_section(str(task["task_id"]))
    for leak in LEAKAGE_FORBIDDEN_IN_DOMAIN:
        assert leak not in domain, f"leakage token in DOMAIN: {leak}"
    return {"ab1": ab1, "ab2g": ab2g, "ab2d": ab2d}


def freeze_prompt_hashes(tasks: Mapping[str, Mapping[str, Any]], seed: int = 2026071301) -> dict[str, Any]:
    from agent_tools.finals_rebuild.ce115_exam_external_validation import FROZEN_PAYLOADS

    out: dict[str, Any] = {"lineage_id": LINEAGE_ID, "seed": seed, "hashes": {}}
    for tid, task in tasks.items():
        frozen = {
            "task_id": tid,
            "oracle_type": task["oracle_type"],
            "oracle_payload": FROZEN_PAYLOADS[tid],
            "repeat_seed": seed,
        }
        prompts = assert_v2_ablation_invariants(task, frozen)
        out["hashes"][tid] = {
            cond: canonical_prompt_hash(text) for cond, text in prompts.items()
        }
    return out


def verify_generic_body_frozen_vs_v1() -> None:
    from agent_tools.finals_rebuild import ce115_clean_incremental_ablation as v1

    assert GENERIC_BODY == v1.GENERIC_BODY, "GENERIC_BODY drifted from v1"
    assert prompt_sha256(GENERIC_BODY) == prompt_sha256(v1.GENERIC_BODY)


def scan_v2_domain_adoption(source: str, task_id: str) -> dict[str, Any]:
    """AST adoption scan against v2 TASK_DOMAIN_APIS (does not use v1 assembly toolbox)."""
    import ast as _ast

    listed = [api["name"] for api in TASK_DOMAIN_APIS[task_id]]
    required = [
        api["name"]
        for api in TASK_DOMAIN_APIS[task_id]
        if api.get("adoption", "required") == "required"
    ]
    listed_set = set(listed)
    families = {name.split(".")[0] for name in listed}
    try:
        tree = _ast.parse(source)
    except SyntaxError as exc:
        return {
            "classification": "INSUFFICIENT_EVIDENCE",
            "listed_apis": listed,
            "required_apis": required,
            "called_apis": [],
            "missing_listed_apis": required,
            "domain_library_adopted": False,
            "errors": [str(exc)],
        }
    aliases: dict[str, str] = {}
    for node in _ast.walk(tree):
        if isinstance(node, (_ast.Import, _ast.ImportFrom)):
            for alias in node.names:
                if alias.name in families:
                    aliases[alias.asname or alias.name] = alias.name
    called: list[str] = []
    for node in _ast.walk(tree):
        if isinstance(node, _ast.Call):
            if isinstance(node.func, _ast.Attribute) and isinstance(node.func.value, _ast.Name):
                base = aliases.get(node.func.value.id, node.func.value.id)
                qual = f"{base}.{node.func.attr}"
                if qual in listed_set or base in families:
                    called.append(qual)
    called_u = sorted(set(called))
    missing = [name for name in required if name not in called_u]
    if not required:
        # All optional (e.g. 114-01): compliance does not require API calls.
        adopted = True
        classification = "OPTIONAL_ADOPTION" if called_u else "OPTIONAL_NOT_USED"
    else:
        adopted = len(missing) == 0
        classification = "ADOPTED" if adopted else ("PARTIAL" if called_u else "NOT_ADOPTED")
    return {
        "classification": classification,
        "listed_apis": listed,
        "required_apis": required,
        "called_apis": called_u,
        "missing_listed_apis": missing,
        "domain_library_adopted": adopted,
        "errors": [],
    }
