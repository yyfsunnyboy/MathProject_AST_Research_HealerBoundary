"""Math16 Ab2d+full-plan: domain-menu API surface + task-specific Processing steps.

Fairness alignment with Ab2d+domain-menu: prompts share the same domain API menu
(byte-identical), stem, frozen_params, generic example, and output contract.
The sole prompt-level addition is ``## Processing steps``.

Derived scaffolds remain available for zero-model reference assembly only and are
NOT injected into model-facing prompts.
"""
from __future__ import annotations

import ast
import hashlib
import json
import re
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable

from agent_tools.finals_rebuild.domain_api_ssot import render_api_prompt_line, require_ssot
from agent_tools.finals_rebuild.math16_ab2d_domain_menu import (
    DOMAIN_BLOCK_BEGIN,
    DOMAIN_BLOCK_END,
    build_domain_menu_prompt,
    extract_domain_api_block,
    load_domain_template,
)
from agent_tools.finals_rebuild.math16_pool import frozen_for_prompt, load_pool_manifest, tasks_by_id
from agent_tools.finals_rebuild.math_task_oracles import evaluate_math_task_oracle
from core.prompts.domain_function_library import (
    FractionOps,
    IntegerOps,
    PolynomialOps,
    RadicalOps,
)

ROOT = Path(__file__).resolve().parents[2]
SCAFFOLD_REL = Path("docs/experiments/prompts/ab2d_full/derived_scaffolds_v1.json")
SCAFFOLD_MANIFEST_REL = Path("docs/experiments/prompts/ab2d_full/derived_scaffolds_v1_manifest.json")
PROMPT_DIR_REL = Path("docs/experiments/prompts/ab2d_full/prompts")
PREFLIGHT_REL = Path("docs/experiments/results/math16_ab2d_full_phase3_preflight_v1")

KIND = "DERIVED_NON_ORACLE_STRUCTURAL_SCAFFOLD"
TOKEN_ESTIMATE_METHOD = "chars_div_4_ceil"
# Full-domain menus (~1.8k tokens) + processing steps; budgets raised for fairness rebuild.
COMMON_TOKEN_BUDGET = 500
TASK_TOKEN_BUDGET = 3500
TOTAL_TOKEN_BUDGET = 4000

FORBIDDEN_ANSWER_KEYS = frozenset(
    {
        "correct_answer",
        "expected_answer",
        "selected",
        "value",
        "product",
        "valid_values",
        "generation_count",
        "prime_factors_of_n",
        "a",
        "b",
        "c",
        "quotient",
        "remainder",
        "larger_root",
        "smaller_root",
        "roots",
        "numerator",
        "denominator",
        "coefficient",
        "result",
    }
)

# Per-task allowed public APIs for Ab2d+full (domain-isolated).
TASK_ALLOWED_APIS: dict[str, tuple[str, ...]] = {
    "ce115_calc_polynomial_division_l1": (
        "PolynomialOps.div_qr",
        "PolynomialOps.format_latex",
    ),
    "ce115_calc_polynomial_factor_roots_l1": (
        "PolynomialOps.factor_quadratic_exact",
        "PolynomialOps.mul",
    ),
    "ce115_calc_exact_rational_expression_l1": (
        "FractionOps.create",
        "FractionOps.mul",
        "FractionOps.add",
        "FractionOps.sub",
        "FractionOps.to_exact",
        "FractionOps.to_latex",
    ),
    "ce115_calc_radical_simplification_l1": (
        "RadicalOps.simplify_term",
        "RadicalOps.format_term",
    ),
    "ce111_q02_polynomial_division_remainder": (
        "PolynomialOps.div_qr",
        "PolynomialOps.format_latex",
    ),
    "ce111_q08_polynomial_factor_parameter_recovery": (
        "PolynomialOps.factor_quadratic_exact",
        "PolynomialOps.mul",
    ),
    "ce111_q03_prime_factor_selection": ("IntegerOps.prime_factorization",),
    "ce112_q01_negative_integer_power": (),
    "ce112_q09_divisor_multiple_intersection": (
        "IntegerOps.positive_divisors",
        "IntegerOps.is_divisible",
    ),
    "ce111_nonchoice_q01_part1_exponential_growth": ("IntegerOps.is_divisible",),
    "ce111_q05_exact_fraction_expression": (
        "FractionOps.from_parts",
        "FractionOps.add",
        "FractionOps.sub",
        "FractionOps.to_latex",
    ),
    "ce113_q01_negative_fraction_subtraction": (
        "FractionOps.from_parts",
        "FractionOps.add",
        "FractionOps.sub",
        "FractionOps.to_latex",
    ),
    "ce112_q12_independent_probability_fraction": (
        "FractionOps.from_parts",
        "FractionOps.mul",
        "FractionOps.to_latex",
    ),
    "ce112_q04_radical_simplification": (
        "RadicalOps.simplify_term",
        "RadicalOps.format_term",
    ),
    "ce111_q10_ordered_quadratic_roots_radical": (
        "RadicalOps.scale_linear_radical",
        "RadicalOps.add_linear_radicals",
        "RadicalOps.format_linear_radical",
    ),
    "ce113_q11_rationalize_denominator": (
        "RadicalOps.rationalize_linear_denominator",
        "RadicalOps.exact_integer",
        "RadicalOps.format_linear_radical",
    ),
}

DOMAIN_EXAMPLES: dict[str, str] = {
    "PolynomialOps": '''```python
from core.prompts.domain_function_library import PolynomialOps

def generate(level=1, **kwargs):
    frozen = {"dividend_coefficients": [2, 0, 2], "divisor_coefficients": [1, 1]}
    q, r = PolynomialOps.div_qr(
        frozen["dividend_coefficients"], frozen["divisor_coefficients"]
    )
    return {
        "question_text": "example stem",
        "correct_answer": {
            "quotient_coefficients": q,
            "remainder_coefficients": r,
            "quotient_latex": PolynomialOps.format_latex(q),
            "remainder_latex": PolynomialOps.format_latex(r),
        },
        "oracle_payload": frozen,
    }
```''',
    "IntegerOps": '''```python
from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    frozen = {"n": 12, "candidates": [2, 5, 7]}
    factors = IntegerOps.prime_factorization(frozen["n"])
    chosen = [c for c in frozen["candidates"] if c in factors][0]
    return {
        "question_text": "example stem",
        "correct_answer": chosen,
        "oracle_payload": frozen,
    }
```''',
    "FractionOps": '''```python
from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    frozen = {"p1": [1, 6], "p2": [1, 3]}
    a = FractionOps.from_parts(frozen["p1"][0], frozen["p1"][1])
    b = FractionOps.from_parts(frozen["p2"][0], frozen["p2"][1])
    value = FractionOps.mul(a, b)
    return {
        "question_text": "example stem",
        "correct_answer": {
            "numerator": value.numerator,
            "denominator": value.denominator,
            "canonical_latex": FractionOps.to_latex(value),
        },
        "oracle_payload": frozen,
    }
```''',
    "RadicalOps": '''```python
from core.prompts.domain_function_library import RadicalOps

def generate(level=1, **kwargs):
    frozen = {"radicand": 50}
    coeff, rest = RadicalOps.simplify_term(1, frozen["radicand"])
    return {
        "question_text": "example stem",
        "correct_answer": {
            "coefficient": coeff,
            "radicand": rest,
            "canonical_latex": RadicalOps.format_term(coeff, rest),
        },
        "oracle_payload": frozen,
    }
```''',
}


def estimate_tokens(text: str) -> int:
    """Conservative token estimate when no tokenizer is available."""
    return (len(text) + 3) // 4


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_text(text: str) -> str:
    return _sha256_bytes(text.encode("utf-8"))


def _sha256_obj(obj: Any) -> str:
    return _sha256_text(json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")))


def build_scaffold_map() -> dict[str, Any]:
    """Deterministic non-oracle scaffolds derived from frozen stem structure only."""
    return {
        "kind": KIND,
        "pool_id": "Math16-LaTeX-v1",
        "version": "ab2d_full_derived_scaffolds_v1",
        "tasks": {
            "ce111_q05_exact_fraction_expression": {
                "kind": KIND,
                "scaffold_type": "fraction_expression_tree",
                "source_frozen_fields": ["expression"],
                "structure": {
                    "op": "sub",
                    "left": {
                        "op": "add",
                        "left": {"num": 9, "den": 22},
                        "right": {"num": 11, "den": 18},
                    },
                    "right": {
                        "op": "sub",
                        "left": {"num": 23, "den": 22},
                        "right": {"num": 7, "den": 18},
                    },
                },
                "no_answer_proof": "Leaves are stem coefficients only; no reduced value.",
            },
            "ce113_q01_negative_fraction_subtraction": {
                "kind": KIND,
                "scaffold_type": "fraction_expression_tree",
                "source_frozen_fields": ["expression"],
                "structure": {
                    "op": "sub",
                    "left": {"num": 3, "den": 7},
                    "right": {"num": -1, "den": 4},
                },
                "no_answer_proof": "Leaves are stem coefficients only; no reduced value.",
            },
            "ce111_q10_ordered_quadratic_roots_radical": {
                "kind": KIND,
                "scaffold_type": "shifted_square_structure",
                "source_frozen_fields": ["equation", "order", "target"],
                "structure": {
                    "equation_form": "shifted_square",
                    "center": 2,
                    "squared_distance": 3,
                    "order": "larger_first",
                    "target_weights": {"larger": 2, "smaller": 1},
                },
                "no_answer_proof": "No roots and no final LinearRadical result.",
            },
            "ce113_q11_rationalize_denominator": {
                "kind": KIND,
                "scaffold_type": "structured_denominator",
                "source_frozen_fields": ["denominator", "radicand", "numerator"],
                "structure": {
                    "denom_rational": 4,
                    "denom_radical_coeff": -1,
                    "radicand": 7,
                },
                "no_answer_proof": "Denominator structure only; no rationalized a,b or a+b.",
            },
        },
    }


def write_scaffold_artifacts(root: Path | None = None) -> dict[str, Any]:
    root = root or ROOT
    scaffold_map = build_scaffold_map()
    body = json.dumps(scaffold_map, ensure_ascii=False, indent=2) + "\n"
    path = root / SCAFFOLD_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    file_sha = _sha256_bytes(path.read_bytes())
    content_sha = _sha256_obj(scaffold_map)
    manifest = {
        "manifest_id": "math16_ab2d_full_derived_scaffolds_v1",
        "kind": KIND,
        "scaffold_map_rel": str(SCAFFOLD_REL).replace("\\", "/"),
        "scaffold_map_sha256": file_sha,
        "scaffold_content_sha256": content_sha,
        "pool_identity_untouched": True,
        "derivation_rules": {
            "ce111_q05_exact_fraction_expression": (
                "Parse frozen expression string into binary op tree with num/den leaves."
            ),
            "ce113_q01_negative_fraction_subtraction": (
                "Parse frozen expression string into binary sub tree with num/den leaves."
            ),
            "ce111_q10_ordered_quadratic_roots_radical": (
                "Project equation/order/target into shifted-square structural fields."
            ),
            "ce113_q11_rationalize_denominator": (
                "Project denominator string and radicand into rational/radical coeff parts."
            ),
        },
        "forbidden_fields": sorted(FORBIDDEN_ANSWER_KEYS),
        "tasks": {
            tid: {
                "scaffold_type": row["scaffold_type"],
                "source_frozen_fields": row["source_frozen_fields"],
                "no_answer_proof": row["no_answer_proof"],
            }
            for tid, row in scaffold_map["tasks"].items()
        },
    }
    mpath = root / SCAFFOLD_MANIFEST_REL
    mpath.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"scaffold_map": scaffold_map, "manifest": manifest, "file_sha256": file_sha}


def load_scaffold_map(root: Path | None = None) -> dict[str, Any]:
    root = root or ROOT
    path = root / SCAFFOLD_REL
    return json.loads(path.read_text(encoding="utf-8"))


def scaffold_for_task(task_id: str, root: Path | None = None) -> dict[str, Any] | None:
    data = load_scaffold_map(root)
    row = data.get("tasks", {}).get(task_id)
    if row is None:
        return None
    return row["structure"]


def common_system_block(domain_ops: str) -> str:
    lines = [
        "# Math16 Ab2d+full system",
        "Write only Python source implementing `def generate(level=1, **kwargs):`.",
        "Return a dict with exactly three keys: question_text, correct_answer, oracle_payload.",
        "question_text must be the provided stem string (do not rebuild LaTeX).",
        "oracle_payload must exactly equal the frozen_params object.",
        "correct_answer must be JSON-compatible and match the task answer shape.",
        "Use only the listed Domain API methods from this prompt.",
        f"Domain for this task: {domain_ops}.",
        "Allowed native ops: arithmetic, comparisons, if/else, loops, list/dict, unpacking, sorting.",
        "Forbidden: other domain public APIs; task-specific solvers; reading audit payloads;",
        "manifest answers; evaluator expected answers; answer lookup by task_id.",
        "Do not use Markdown fences or explanations outside the Python source.",
        "Import Domain API from `core.prompts.domain_function_library` only as needed.",
    ]
    return "\n".join(lines) + "\n"


def _api_card(api_name: str) -> str:
    c = require_ssot(api_name)
    return "\n".join(
        [
            render_api_prompt_line(api_name),
            f"  inputs: {c['input_constraints']}",
            f"  notes: {c['normalization_responsibility']}",
        ]
    )


def _steps_for_task(task_id: str) -> str:
    steps = {
        "ce115_calc_polynomial_division_l1": (
            "1) Call PolynomialOps.div_qr on frozen coefficients.\n"
            "2) Optionally format latex.\n"
            "3) Assemble coefficient lists into correct_answer."
        ),
        "ce115_calc_polynomial_factor_roots_l1": (
            "1) factor_quadratic_exact(a,b,c).\n"
            "2) Convert factors to roots and sort ascending.\n"
            "3) Return roots (latex optional)."
        ),
        "ce115_calc_exact_rational_expression_l1": (
            "1) FractionOps.create each operand string.\n"
            "2) Multiply and accumulate with signs.\n"
            "3) FractionOps.to_exact for value."
        ),
        "ce115_calc_radical_simplification_l1": (
            "1) simplify_term(1, radicand).\n"
            "2) Pack coefficient/radicand; optional format_term."
        ),
        "ce111_q02_polynomial_division_remainder": (
            "1) div_qr frozen coefficients.\n"
            "2) Keep remainder only; format_latex if needed."
        ),
        "ce111_q08_polynomial_factor_parameter_recovery": (
            "1) factor_quadratic_exact.\n"
            "2) Swap so left x_coefficient equals template_left_x_coefficient.\n"
            "3) Extract a,b,c and compute a+2*c with native arithmetic."
        ),
        "ce111_q03_prime_factor_selection": (
            "1) IntegerOps.prime_factorization(n).\n"
            "2) Choose the candidate that appears as a prime key."
        ),
        "ce112_q01_negative_integer_power": (
            "1) Compute base ** exponent with native arithmetic.\n"
            "2) Return bare int."
        ),
        "ce112_q09_divisor_multiple_intersection": (
            "1) positive_divisors(divisor_of).\n"
            "2) Keep values divisible by multiple_of.\n"
            "3) Return {\"count\": len(valid)}."
        ),
        "ce111_nonchoice_q01_part1_exponential_growth": (
            "1) total_hours = days * 24.\n"
            "2) Ensure divisible by hours_per_generation.\n"
            "3) k = total_hours // hours_per_generation; return {\"k\": k}."
        ),
        "ce111_q05_exact_fraction_expression": (
            "1) From the frozen expression, construct each fraction leaf with "
            "FractionOps.from_parts.\n"
            "2) Evaluate the expression tree with FractionOps.add and FractionOps.sub "
            "(outer subtraction of the parenthesized difference).\n"
            "3) Return numerator/denominator (+ optional FractionOps.to_latex)."
        ),
        "ce113_q01_negative_fraction_subtraction": (
            "1) Construct both operands from the frozen expression with "
            "FractionOps.from_parts (preserve the negative numerator).\n"
            "2) Compute FractionOps.sub(left, right).\n"
            "3) Return numerator/denominator (+ optional FractionOps.to_latex)."
        ),
        "ce112_q12_independent_probability_fraction": (
            "1) from_parts for p1 and p2.\n"
            "2) mul; return numerator/denominator."
        ),
        "ce112_q04_radical_simplification": (
            "1) simplify_term(1, radicand).\n"
            "2) Pack coefficient/radicand."
        ),
        "ce111_q10_ordered_quadratic_roots_radical": (
            "1) From the frozen shifted-square equation, form the two LinearRadical "
            "roots with native arithmetic; order them so the larger root is first "
            "(a > b).\n"
            "2) Call RadicalOps.scale_linear_radical on the larger root with weight 2; "
            "then RadicalOps.add_linear_radicals with the smaller root.\n"
            "3) Assemble the nested or flat result dict "
            "(optional RadicalOps.format_linear_radical)."
        ),
        "ce113_q11_rationalize_denominator": (
            "1) Interpret the frozen denominator as "
            "(denom_rational) + (denom_radical_coeff)*sqrt(radicand); call "
            "RadicalOps.rationalize_linear_denominator("
            "numerator, denom_rational, denom_radical_coeff, radicand).\n"
            "2) RadicalOps.exact_integer on both returned coefficients.\n"
            "3) Native int add for final bare answer."
        ),
    }
    return steps[task_id]


def build_task_block(task: dict[str, Any], scaffold_structure: dict[str, Any] | None = None) -> str:
    """Legacy helper retained for tests; prompts no longer inject scaffolds.

    Prefer ``build_ab2d_full_prompt``, which shares the domain-menu base and only
    appends Processing steps.
    """
    del scaffold_structure  # intentionally unused in model-facing prompts
    frozen = task["frozen_params"]
    domain = task["domain_ops"]
    parts = [
        f"# Task `{task['task_id']}`",
        f"domain_ops: {domain}",
        "",
        "## Question stem (use verbatim as question_text)",
        task["math16_question_text"],
        "",
        "## frozen_params (oracle_payload must equal this object)",
        json.dumps(frozen, ensure_ascii=False, indent=2, sort_keys=True),
        "",
        "## Processing steps",
        _steps_for_task(task["task_id"]),
    ]
    return "\n".join(parts) + "\n"


def build_ab2d_full_prompt(task: dict[str, Any], root: Path | None = None) -> str:
    """Ab2d+full-plan = domain-menu prompt + task-specific Processing steps only."""
    root = root or ROOT
    template = load_domain_template(task["domain_ops"], root)
    base = build_domain_menu_prompt(task, template)
    steps = _steps_for_task(task["task_id"])
    return base.rstrip() + "\n\n## Processing steps\n" + steps + "\n"


def prompt_metrics(prompt: str, task: dict[str, Any], root: Path | None = None) -> dict[str, Any]:
    root = root or ROOT
    template = load_domain_template(task["domain_ops"], root)
    base = build_domain_menu_prompt(task, template)
    steps = "## Processing steps\n" + _steps_for_task(task["task_id"]) + "\n"
    return {
        "task_id": task["task_id"],
        "domain_ops": task["domain_ops"],
        "common_chars": len(base),
        "task_chars": len(steps),
        "total_chars": len(prompt),
        "common_tokens_est": estimate_tokens(base),
        "task_tokens_est": estimate_tokens(steps),
        "total_tokens_est": estimate_tokens(prompt),
        "token_estimate_method": TOKEN_ESTIMATE_METHOD,
        "prompt_sha256": _sha256_text(prompt),
        "within_common_budget": estimate_tokens(base) <= TOTAL_TOKEN_BUDGET,
        "within_task_budget": estimate_tokens(steps) <= TASK_TOKEN_BUDGET,
        "within_total_budget": estimate_tokens(prompt) <= TOTAL_TOKEN_BUDGET,
        "domain_api_block_sha256": _sha256_text(extract_domain_api_block(prompt)),
        "has_derived_scaffold": "derived_scaffold" in prompt.lower(),
        "has_processing_steps": "## Processing steps" in prompt,
    }


def assert_domain_isolation(prompt: str, domain_ops: str) -> None:
    foreign = [name for name in ("PolynomialOps", "IntegerOps", "FractionOps", "RadicalOps") if name != domain_ops]
    for name in foreign:
        if re.search(rf"\b{name}\.", prompt):
            raise AssertionError(f"foreign domain API leaked: {name}")
        if f"domain_ops: {name}" in prompt:
            raise AssertionError(f"foreign domain_ops label leaked: {name}")


def markdown_fences_balanced(text: str) -> bool:
    return text.count("```") % 2 == 0


def extract_fenced_blocks(text: str) -> list[tuple[str, str]]:
    pattern = re.compile(r"```([a-zA-Z0-9_-]*)\n(.*?)```", re.S)
    return [(m.group(1), m.group(2)) for m in pattern.finditer(text)]


def validate_prompt_static(prompt: str, domain_ops: str) -> list[str]:
    errors: list[str] = []
    if not markdown_fences_balanced(prompt):
        errors.append("unbalanced_markdown_fences")
    if "derived_scaffold" in prompt.lower():
        errors.append("derived_scaffold_injected")
    if DOMAIN_BLOCK_BEGIN not in prompt or DOMAIN_BLOCK_END not in prompt:
        errors.append("missing_domain_menu_api_block_markers")
    if "## Processing steps" not in prompt:
        errors.append("missing_processing_steps")
    try:
        assert_domain_isolation(prompt, domain_ops)
    except AssertionError as exc:
        errors.append(str(exc))
    for lang, body in extract_fenced_blocks(prompt):
        if lang == "python":
            try:
                ast.parse(body)
            except SyntaxError as exc:
                errors.append(f"python_ast:{exc}")
            if re.search(r"^\|", body, re.M) or "|---" in body:
                errors.append("markdown_table_inside_code_fence")
    # Audit/answer leakage heuristics (field names that must not appear as data).
    for marker in ('"selected"', '"valid_values"', '"generation_count"', '"prime_factors_of_n"', '"larger_root"', '"smaller_root"'):
        if marker in prompt:
            errors.append(f"audit_field_leakage:{marker}")
    if "expected_answer" in prompt:
        errors.append("expected_answer_leakage")
    return errors


def _eval_fraction_tree(node: dict[str, Any]) -> Fraction:
    if "num" in node and "den" in node:
        return FractionOps.from_parts(node["num"], node["den"])
    op = node["op"]
    left = _eval_fraction_tree(node["left"])
    right = _eval_fraction_tree(node["right"])
    if op == "add":
        return FractionOps.add(left, right)
    if op == "sub":
        return FractionOps.sub(left, right)
    raise ValueError(f"unsupported tree op: {op}")


def reference_assemble(task: dict[str, Any], root: Path | None = None) -> dict[str, Any]:
    """Deterministic reference assembly for zero-model preflight (NOT for prompts)."""
    tid = task["task_id"]
    frozen = dict(task["frozen_params"])
    stem = task["math16_question_text"]
    scaffold = scaffold_for_task(tid, root)
    trace: list[dict[str, Any]] = []

    def rec(op: str, call: str, result: Any) -> Any:
        trace.append({"op": op, "call": call, "return_type": type(result).__name__, "return": _jsonable(result)})
        return result

    if tid == "ce115_calc_polynomial_division_l1":
        q, r = rec("div_qr", "PolynomialOps.div_qr(...)", PolynomialOps.div_qr(frozen["dividend_coefficients"], frozen["divisor_coefficients"]))
        ca = {
            "quotient_coefficients": q,
            "remainder_coefficients": r,
            "quotient_latex": PolynomialOps.format_latex(q),
            "remainder_latex": PolynomialOps.format_latex(r),
        }
    elif tid == "ce115_calc_polynomial_factor_roots_l1":
        a, b, c = frozen["quadratic_coefficients"]
        factors = rec("factor", "factor_quadratic_exact", PolynomialOps.factor_quadratic_exact(a, b, c))

        def _root_of(factor: dict[str, Any]) -> int:
            return int(-Fraction(factor["constant"]) / Fraction(factor["x_coefficient"]))

        roots = sorted(_root_of(f) for f in factors)
        # Presentation only: assemble latex from API factors / computed roots (no frozen answer strings).
        factors_by_root = sorted(factors, key=_root_of)
        factor_parts = []
        for factor in factors_by_root:
            inner = PolynomialOps.format_latex(
                [factor["x_coefficient"], factor["constant"]]
            ).replace(" ", "")
            factor_parts.append(f"({inner})")
        factorization_latex = "".join(factor_parts) + "=0"
        roots_latex = "[" + r",\,".join(str(root) for root in roots) + "]"
        ca = {
            "roots": roots,
            "factorization_latex": factorization_latex,
            "roots_latex": roots_latex,
        }
    elif tid == "ce115_calc_exact_rational_expression_l1":
        total = Fraction(0)
        for product in frozen["products"]:
            left = FractionOps.create(product["left"])
            right = FractionOps.create(product["right"])
            term = FractionOps.mul(left, right)
            if product["sign"] == 1:
                total = FractionOps.add(total, term)
            else:
                total = FractionOps.add(total, FractionOps.mul(Fraction(-1), term))
        rec("rational", "create/mul/add", total)
        ca = {"value": FractionOps.to_exact(total), "canonical_latex": FractionOps.to_latex(total)}
    elif tid == "ce115_calc_radical_simplification_l1":
        coeff, rest = rec("simp", "simplify_term", RadicalOps.simplify_term(1, frozen["radicand"]))
        ca = {"coefficient": coeff, "radicand": rest, "canonical_latex": RadicalOps.format_term(coeff, rest)}
    elif tid == "ce111_q02_polynomial_division_remainder":
        _q, r = rec("div_qr", "div_qr", PolynomialOps.div_qr(frozen["dividend_coefficients"], frozen["divisor_coefficients"]))
        rem = PolynomialOps.format_latex(r)
        ca = {"remainder": rem, "canonical_latex": rem}
    elif tid == "ce111_q08_polynomial_factor_parameter_recovery":
        a0, b0, c0 = frozen["quadratic_coefficients"]
        factors = rec("factor", "factor_quadratic_exact", PolynomialOps.factor_quadratic_exact(a0, b0, c0))
        tx = frozen["template_left_x_coefficient"]
        f1, f2 = factors[0], factors[1]
        if f1["x_coefficient"] != tx:
            f1, f2 = f2, f1
        a, b, c = f1["constant"], f2["x_coefficient"], f2["constant"]
        ca = a + 2 * c
    elif tid == "ce111_q03_prime_factor_selection":
        pf = rec("pf", "prime_factorization", IntegerOps.prime_factorization(frozen["n"]))
        hits = [c for c in frozen["candidates"] if c in pf]
        ca = hits[0]
    elif tid == "ce112_q01_negative_integer_power":
        ca = frozen["base"] ** frozen["exponent"]
        rec("pow", "native **", ca)
    elif tid == "ce112_q09_divisor_multiple_intersection":
        divs = rec("divisors", "positive_divisors", IntegerOps.positive_divisors(frozen["divisor_of"]))
        valid = [d for d in divs if IntegerOps.is_divisible(d, frozen["multiple_of"])]
        ca = {"count": len(valid)}
    elif tid == "ce111_nonchoice_q01_part1_exponential_growth":
        hours = frozen["days"] * 24
        assert IntegerOps.is_divisible(hours, frozen["hours_per_generation"])
        ca = {"k": hours // frozen["hours_per_generation"]}
        rec("growth", "native hours//", ca)
    elif tid in ("ce111_q05_exact_fraction_expression", "ce113_q01_negative_fraction_subtraction"):
        assert scaffold is not None
        value = rec("tree", "from_parts/add/sub", _eval_fraction_tree(scaffold))
        ca = {
            "numerator": value.numerator,
            "denominator": value.denominator,
            "canonical_latex": FractionOps.to_latex(value),
        }
    elif tid == "ce112_q12_independent_probability_fraction":
        p1 = FractionOps.from_parts(frozen["p1"][0], frozen["p1"][1])
        p2 = FractionOps.from_parts(frozen["p2"][0], frozen["p2"][1])
        value = rec("mul", "mul", FractionOps.mul(p1, p2))
        ca = {
            "numerator": value.numerator,
            "denominator": value.denominator,
            "canonical_latex": FractionOps.to_latex(value),
        }
    elif tid == "ce112_q04_radical_simplification":
        coeff, rest = rec("simp", "simplify_term", RadicalOps.simplify_term(1, frozen["radicand"]))
        ca = {"coefficient": coeff, "radicand": rest, "canonical_latex": RadicalOps.format_term(coeff, rest)}
    elif tid == "ce111_q10_ordered_quadratic_roots_radical":
        assert scaffold is not None
        center = scaffold["center"]
        dist = scaffold["squared_distance"]
        larger = {"rational": center, "radical_coefficient": 1, "radicand": dist}
        smaller = {"rational": center, "radical_coefficient": -1, "radicand": dist}
        scaled = rec("scale", "scale_linear_radical", RadicalOps.scale_linear_radical(larger, scaffold["target_weights"]["larger"]))
        result = rec("add", "add_linear_radicals", RadicalOps.add_linear_radicals(scaled, smaller))
        latex = RadicalOps.format_linear_radical(result)
        ca = {"result": {**result, "canonical_latex": latex}}
    elif tid == "ce113_q11_rationalize_denominator":
        assert scaffold is not None
        a_out, b_out, _r = rec(
            "rat",
            "rationalize_linear_denominator",
            RadicalOps.rationalize_linear_denominator(
                frozen["numerator"],
                scaffold["denom_rational"],
                scaffold["denom_radical_coeff"],
                scaffold["radicand"],
            ),
        )
        a_i = RadicalOps.exact_integer(a_out)
        b_i = RadicalOps.exact_integer(b_out)
        ca = a_i + b_i
    else:
        raise KeyError(tid)

    output = {
        "question_text": stem,
        "correct_answer": ca,
        "oracle_payload": frozen,
    }
    return {"output": output, "trace": trace}


def _jsonable(value: Any) -> Any:
    if isinstance(value, Fraction):
        return {"Fraction": f"{value.numerator}/{value.denominator}"}
    if isinstance(value, (list, tuple)):
        return [_jsonable(v) for v in value]
    if isinstance(value, dict):
        return {str(k): _jsonable(v) for k, v in value.items()}
    return value


def run_zero_model_preflight(root: Path | None = None) -> dict[str, Any]:
    root = root or ROOT
    write_scaffold_artifacts(root)
    tasks = tasks_by_id(root)
    manifest = load_pool_manifest(root)
    out_dir = root / PREFLIGHT_REL
    out_dir.mkdir(parents=True, exist_ok=True)
    prompt_dir = root / PROMPT_DIR_REL
    prompt_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    prompt_metrics_rows = []
    all_pass = True
    for tid in manifest["task_ids"]:
        task = tasks[tid]
        prompt = build_ab2d_full_prompt(task, root)
        (prompt_dir / f"{tid}.txt").write_text(prompt, encoding="utf-8")
        metrics = prompt_metrics(prompt, task, root)
        static_errors = validate_prompt_static(prompt, task["domain_ops"])
        metrics["static_errors"] = static_errors
        prompt_metrics_rows.append(metrics)

        assembled = reference_assemble(task, root)
        output = assembled["output"]
        assert set(output) == {"question_text", "correct_answer", "oracle_payload"}
        assert output["oracle_payload"] == task["frozen_params"]
        assert output["question_text"] == task["math16_question_text"]
        verdict = evaluate_math_task_oracle(task["oracle_type"], task["oracle_payload"], output["correct_answer"])
        ok = bool(verdict.get("is_correct"))
        all_pass = all_pass and ok and not static_errors and metrics["within_total_budget"]
        row = {
            "task_id": tid,
            "domain_ops": task["domain_ops"],
            "oracle_type": task["oracle_type"],
            "api_trace": assembled["trace"],
            "final_schema_keys": sorted(output),
            "correct_answer": _jsonable(output["correct_answer"]),
            "evaluator_is_correct": ok,
            "evaluator_error": verdict.get("error"),
            "static_errors": static_errors,
            "prompt_sha256": metrics["prompt_sha256"],
            "total_tokens_est": metrics["total_tokens_est"],
        }
        rows.append(row)
        (out_dir / f"{tid}.json").write_text(json.dumps(row, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    summary = {
        "preflight_id": "math16_ab2d_full_phase3_preflight_v1",
        "n_tasks": len(rows),
        "all_evaluator_pass": all(r["evaluator_is_correct"] for r in rows),
        "all_static_clean": all(not r["static_errors"] for r in rows),
        "all_budget_ok": all(m["within_total_budget"] for m in prompt_metrics_rows),
        "overall_pass": all_pass,
        "scaffold_map_sha256": (root / SCAFFOLD_MANIFEST_REL and json.loads((root / SCAFFOLD_MANIFEST_REL).read_text(encoding="utf-8"))["scaffold_map_sha256"]),
        "prompt_metrics": prompt_metrics_rows,
        "tasks": rows,
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return summary


if __name__ == "__main__":
    result = run_zero_model_preflight()
    print(json.dumps({k: result[k] for k in ("n_tasks", "overall_pass", "all_evaluator_pass", "all_static_clean", "all_budget_ok", "scaffold_map_sha256")}, ensure_ascii=False, indent=2))
