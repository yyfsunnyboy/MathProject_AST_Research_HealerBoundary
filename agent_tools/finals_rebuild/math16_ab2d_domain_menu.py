# -*- coding: utf-8 -*-
"""Math16 Ab2d+domain-menu: domain-level API menus (zero-model freeze).

Each of the four domains exposes its full SUPPORTED_PUBLIC API surface.
Per-task rendered prompts add only frozen stem + frozen_params.
No task-specific guardrails, API-order plans, or answer/oracle leakage.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from agent_tools.finals_rebuild.domain_api_ssot import (
    API_CLASSIFICATION,
    DOMAIN_API_SSOT,
    SUPPORTED_PUBLIC,
    render_api_prompt_line,
    require_ssot,
    validate_inventory,
)
from agent_tools.finals_rebuild.math16_pool import (
    load_pool_manifest,
    tasks_by_id,
)

ROOT = Path(__file__).resolve().parents[2]

CONDITION = "ab2d_domain_menu"
CONDITION_LABEL = "Ab2d+domain-menu"
MANIFEST_ID = "math16_ab2d_domain_menu_freeze_v1"
EXPERIMENT_ID = "math16_ab2d_domain_menu_v1"

TEMPLATE_DIR_REL = "docs/experiments/templates/ab2d_domain_menu"
PROMPT_DIR_REL = "docs/experiments/prompts/ab2d_domain_menu/prompts"
MANIFEST_REL = "docs/experiments/prompts/ab2d_domain_menu/manifest.json"
PREFLIGHT_REL = "docs/experiments/results/math16_ab2d_domain_menu_preflight_v1"
ARTIFACT_ROOT_REL = f"artifacts/{EXPERIMENT_ID}"

DOMAIN_OPS = ("IntegerOps", "FractionOps", "RadicalOps", "PolynomialOps")

DOMAIN_TEMPLATE_FILES: dict[str, str] = {
    "IntegerOps": "integer_domain_menu.md",
    "FractionOps": "fraction_domain_menu.md",
    "RadicalOps": "radical_domain_menu.md",
    "PolynomialOps": "polynomial_domain_menu.md",
}

# Generic examples only — must not reuse Math16 formal frozen instances / answers.
GENERIC_USAGE_EXAMPLES: dict[str, str] = {
    "IntegerOps.add": "IntegerOps.add(10, 20)  # 30",
    "IntegerOps.sub": "IntegerOps.sub(30, 8)  # 22",
    "IntegerOps.fmt_num": 'IntegerOps.fmt_num(-2)  # "(-2)"',
    "IntegerOps.is_divisible": "IntegerOps.is_divisible(21, 7)  # True",
    "IntegerOps.prime_factorization": "IntegerOps.prime_factorization(12)  # {2: 2, 3: 1}",
    "IntegerOps.positive_divisors": "IntegerOps.positive_divisors(12)  # [1, 2, 3, 4, 6, 12]",
    "IntegerOps.safe_eval": 'IntegerOps.safe_eval("2**4")  # 16',
    "FractionOps.create": 'FractionOps.create("2/7")  # Fraction(2, 7)',
    "FractionOps.to_latex": r"FractionOps.to_latex(Fraction(2, 7))  # '\frac{2}{7}'",
    "FractionOps.add": "FractionOps.add(Fraction(1, 2), Fraction(1, 3))",
    "FractionOps.sub": "FractionOps.sub(Fraction(1, 2), Fraction(1, 6))",
    "FractionOps.mul": "FractionOps.mul(Fraction(1, 2), Fraction(1, 3))",
    "FractionOps.div": "FractionOps.div(Fraction(1, 2), Fraction(1, 3))",
    "FractionOps.from_parts": "FractionOps.from_parts(6, 3)  # Fraction(2, 1)",
    "FractionOps.to_exact": "FractionOps.to_exact(Fraction(3, 2))  # '3/2'",
    "RadicalOps.simplify_term": "RadicalOps.simplify_term(1, 12)  # (2, 3)",
    "RadicalOps.format_term": r"RadicalOps.format_term(2, 3)  # '2\sqrt{3}'",
    "RadicalOps.format_expression": r"RadicalOps.format_expression({1: 6, 3: -1})  # '6 - \sqrt{3}'",
    "RadicalOps.normalize_term_list": "RadicalOps.normalize_term_list([(1, 12)])",
    "RadicalOps.rationalize_linear_denominator": (
        "RadicalOps.rationalize_linear_denominator(1, 2, 1, 3)"
    ),
    "RadicalOps.scale_linear_radical": (
        'RadicalOps.scale_linear_radical('
        '{"rational": 1, "radical_coefficient": 1, "radicand": 2}, 2)'
    ),
    "RadicalOps.add_linear_radicals": (
        'RadicalOps.add_linear_radicals('
        '{"rational": 1, "radical_coefficient": 1, "radicand": 2},'
        '{"rational": 3, "radical_coefficient": 1, "radicand": 2})'
    ),
    "RadicalOps.format_linear_radical": (
        r'RadicalOps.format_linear_radical('
        r'{"rational": 1, "radical_coefficient": 1, "radicand": 2})  # "1+\sqrt{2}"'
    ),
    "RadicalOps.exact_integer": "RadicalOps.exact_integer(Fraction(4, 1))  # 4",
    "PolynomialOps.normalize": "PolynomialOps.normalize([0, 2, 1])  # [2, 1]",
    "PolynomialOps.format_latex": "PolynomialOps.format_latex([2, 0])  # '2x'",
    "PolynomialOps.add": "PolynomialOps.add([1, 2], [3, 4])  # [4, 6]",
    "PolynomialOps.sub": "PolynomialOps.sub([1, 2], [3, 4])  # [-2, -2]",
    "PolynomialOps.mul": "PolynomialOps.mul([1, 1], [1, -1])  # [1, 0, -1]",
    "PolynomialOps.div_qr": "PolynomialOps.div_qr([2, 0, 2], [1, 1])",
    "PolynomialOps.coeffs_from_py_expression": (
        "PolynomialOps.coeffs_from_py_expression('(x+1)*(x-1)')"
    ),
    "PolynomialOps.to_degree_map": "PolynomialOps.to_degree_map([1, 0, -1])",
    "PolynomialOps.factor_quadratic_exact": (
        "PolynomialOps.factor_quadratic_exact(1, -5, 6)"
    ),
}

DOMAIN_CODE_EXAMPLES: dict[str, str] = {
    "IntegerOps": '''```python
from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    # Generic illustration only — not a Math16 formal item.
    frozen = {"n": 12, "candidates": [2, 7, 11]}
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
    # Generic illustration only — not a Math16 formal item.
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
    # Generic illustration only — not a Math16 formal item.
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
    "PolynomialOps": '''```python
from core.prompts.domain_function_library import PolynomialOps

def generate(level=1, **kwargs):
    # Generic illustration only — not a Math16 formal item.
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
}

SHARED_OUTPUT_CONTRACT = """## Shared output contract
Return a dict with exactly three keys: question_text, correct_answer, oracle_payload.
- question_text: the provided stem string (do not rebuild from scratch unless required).
- correct_answer: JSON-compatible value matching the task answer shape.
- oracle_payload: must exactly equal the frozen_params object provided in the task block.
Do not read audit payloads, evaluator expected answers, or answer tables."""

SYSTEM_HEADER = """# Math16 Ab2d+domain-menu
Write only Python source implementing `def generate(level=1, **kwargs):`.
Use only the Domain API methods listed in the Domain API menu below for this domain.
Allowed native ops: arithmetic, comparisons, if/else, loops, list/dict, unpacking, sorting.
Forbidden: other domain public APIs; task-specific solvers; reading audit payloads;
manifest answers; evaluator expected answers; answer lookup by task_id;
prescribed per-item API sequences (none are provided — choose APIs yourself).
Do not use Markdown fences or explanations outside the Python source.
Import Domain API from `core.prompts.domain_function_library` only as needed.
"""

# Markers for byte-identical domain API block extraction.
DOMAIN_BLOCK_BEGIN = "<!-- DOMAIN_API_BLOCK_BEGIN -->"
DOMAIN_BLOCK_END = "<!-- DOMAIN_API_BLOCK_END -->"

SOLUTION_PLAN_PATTERNS = [
    re.compile(r"(?i)processing steps"),
    re.compile(r"(?i)task guardrails?"),
    re.compile(r"(?i)\bAPI call order\b"),
    re.compile(r"(?i)first call\b"),
    re.compile(r"(?i)then call\b"),
    re.compile(r"(?i)use \w+Ops\.\w+ (?:and|then) \w+Ops\.\w+"),
    re.compile(r"(?i)extract (?:the )?(?:quotient|remainder|roots)"),
    re.compile(r"(?i)order the roots"),
    re.compile(r"(?i)^\s*1\)\s*.+\n\s*2\)\s*.+\n\s*3\)", re.M),
    re.compile(r"(?i)for this (?:exact )?task[,:]?\s*use"),
    re.compile(r"(?i)evaluate the exact expression:"),
    re.compile(r"(?i)perform polynomial division of \("),
]


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.replace("\r\n", "\n").encode("utf-8")).hexdigest()


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def supported_apis_for_domain(domain_ops: str) -> list[str]:
    if domain_ops not in DOMAIN_OPS:
        raise KeyError(domain_ops)
    return sorted(
        name
        for name, cls in API_CLASSIFICATION.items()
        if cls == SUPPORTED_PUBLIC and name.startswith(domain_ops + ".")
    )


def render_api_card(api_name: str) -> str:
    contract = require_ssot(api_name)
    example = GENERIC_USAGE_EXAMPLES[api_name]
    return "\n".join(
        [
            render_api_prompt_line(api_name),
            f"  inputs: {contract['input_constraints']}",
            f"  returns_shape: `{json.dumps(contract['return_contract'], ensure_ascii=False, sort_keys=True)}`",
            f"  boundary: {contract['normalization_responsibility']}",
            f"  example: `{example}`",
        ]
    )


def build_domain_api_block(domain_ops: str) -> str:
    """Byte-stable domain API menu body (between markers)."""
    apis = supported_apis_for_domain(domain_ops)
    lines = [
        f"# Domain API menu: {domain_ops}",
        "",
        f"This menu lists every SUPPORTED_PUBLIC method on `{domain_ops}`.",
        "It is domain-general: it does not name a Math16 task, prescribe which",
        "APIs a specific item must call, or give call order / solution steps.",
        "",
        "## Public APIs",
    ]
    for name in apis:
        lines.append(render_api_card(name))
        lines.append("")
    lines.append("## Generic domain code example (non-formal numbers)")
    lines.append(DOMAIN_CODE_EXAMPLES[domain_ops].rstrip())
    lines.append("")
    lines.append(SHARED_OUTPUT_CONTRACT.rstrip())
    lines.append("")
    return "\n".join(lines)


def build_domain_template(domain_ops: str) -> str:
    block = build_domain_api_block(domain_ops)
    return (
        f"{DOMAIN_BLOCK_BEGIN}\n"
        f"{block.rstrip()}\n"
        f"{DOMAIN_BLOCK_END}\n"
    )


def extract_domain_api_block(text: str) -> str:
    begin = text.find(DOMAIN_BLOCK_BEGIN)
    end = text.find(DOMAIN_BLOCK_END)
    if begin < 0 or end < 0 or end <= begin:
        raise ValueError("domain API block markers missing")
    inner = text[begin + len(DOMAIN_BLOCK_BEGIN) : end]
    return inner.strip("\n") + "\n"


def build_task_block(task: dict[str, Any]) -> str:
    frozen = task["frozen_params"]
    return "\n".join(
        [
            "## Task",
            f"task_id: `{task['task_id']}`",
            f"domain_ops: `{task['domain_ops']}`",
            f"skill_id: `{task.get('skill_id', '')}`",
            "",
            "## Frozen task description (use as question_text)",
            task["math16_question_text"],
            "",
            "## frozen_params (oracle_payload must equal this object)",
            json.dumps(frozen, ensure_ascii=False, indent=2, sort_keys=True),
            "",
        ]
    )


def build_domain_menu_prompt(task: dict[str, Any], template_text: str | None = None) -> str:
    domain = task["domain_ops"]
    if template_text is None:
        template_text = build_domain_template(domain)
    # Ensure we only inject the marked domain block once.
    block = extract_domain_api_block(template_text)
    wrapped = f"{DOMAIN_BLOCK_BEGIN}\n{block.rstrip()}\n{DOMAIN_BLOCK_END}"
    parts = [
        SYSTEM_HEADER.rstrip(),
        "",
        f"Domain for this task: {domain}.",
        "",
        wrapped,
        "",
        build_task_block(task).rstrip(),
        "",
    ]
    return "\n".join(parts).replace("\r\n", "\n")


def write_domain_templates(root: Path | None = None) -> dict[str, str]:
    root = root or ROOT
    out_dir = root / TEMPLATE_DIR_REL
    out_dir.mkdir(parents=True, exist_ok=True)
    hashes: dict[str, str] = {}
    for domain, filename in DOMAIN_TEMPLATE_FILES.items():
        text = build_domain_template(domain)
        path = out_dir / filename
        path.write_text(text, encoding="utf-8", newline="\n")
        hashes[domain] = _sha256_text(text)
    return hashes


def load_domain_template(domain_ops: str, root: Path | None = None) -> str:
    root = root or ROOT
    path = root / TEMPLATE_DIR_REL / DOMAIN_TEMPLATE_FILES[domain_ops]
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def other_domain_ops(domain_ops: str) -> list[str]:
    return [d for d in DOMAIN_OPS if d != domain_ops]


def validate_prompt_static(prompt: str, domain_ops: str) -> list[str]:
    errors: list[str] = []
    if DOMAIN_BLOCK_BEGIN not in prompt or DOMAIN_BLOCK_END not in prompt:
        errors.append("missing_domain_block_markers")
    for other in other_domain_ops(domain_ops):
        if other in prompt:
            errors.append(f"cross_domain_exposure:{other}")
    for pat in SOLUTION_PLAN_PATTERNS:
        if pat.search(prompt):
            errors.append(f"solution_plan_pattern:{pat.pattern}")
    # Forbid embedding labeled formal answers.
    if re.search(r"(?i)expected[_ ]answer\s*[:=]", prompt):
        errors.append("expected_answer_label")
    if "task_id →" in prompt or "task_id->" in prompt:
        errors.append("task_id_lookup_arrow")
    return errors


def _flatten_leaves(obj: Any, prefix: str = "") -> list[tuple[str, Any]]:
    out: list[tuple[str, Any]] = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            out.extend(_flatten_leaves(v, f"{prefix}.{k}" if prefix else str(k)))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out.extend(_flatten_leaves(v, f"{prefix}[{i}]"))
    else:
        out.append((prefix, obj))
    return out


def distinctive_answer_tokens(correct_answer: Any) -> list[tuple[str, str]]:
    """High-signal answer tokens for leakage scanning (avoid tiny shared ints)."""
    tokens: list[tuple[str, str]] = []
    if isinstance(correct_answer, bool):
        return tokens
    if isinstance(correct_answer, int):
        if abs(correct_answer) > 4:
            tokens.append(("bounded", str(correct_answer)))
        return tokens
    if isinstance(correct_answer, str):
        if len(correct_answer) >= 2:
            tokens.append(("exact", correct_answer))
        return tokens
    # Structured answers: full dump + distinctive string leaves only (not nested ints).
    dumped = json.dumps(correct_answer, ensure_ascii=False, sort_keys=True)
    if len(dumped) >= 8:
        tokens.append(("exact", dumped))
    for _path, val in _flatten_leaves(correct_answer):
        if isinstance(val, str) and len(val) >= 3:
            tokens.append(("exact", val))
    return tokens


def _token_present(text: str, kind: str, token: str) -> bool:
    if kind == "exact":
        return token in text
    return re.search(rf"(?<![0-9A-Za-z_-]){re.escape(token)}(?![0-9A-Za-z_-])", text) is not None


def scan_answer_leakage(
    text: str,
    tasks: list[dict[str, Any]],
    *,
    allow_frozen_overlap: bool = False,
    frozen_params: dict[str, Any] | None = None,
) -> list[str]:
    hits: list[str] = []
    frozen_blob = (
        json.dumps(frozen_params, ensure_ascii=False) if frozen_params is not None else ""
    )
    for task in tasks:
        tid = task["task_id"]
        for kind, token in distinctive_answer_tokens(task["correct_answer"]):
            if not _token_present(text, kind, token):
                continue
            if allow_frozen_overlap and token in frozen_blob:
                continue
            if allow_frozen_overlap:
                fp_idx = text.find("## frozen_params")
                if fp_idx >= 0:
                    domain_part = text[: text.find("## Task")] if "## Task" in text else text
                    if _token_present(domain_part, kind, token):
                        hits.append(f"{tid}:{token[:60]}")
                    continue
            hits.append(f"{tid}:{token[:60]}")
    return sorted(set(hits))


def scan_solution_plan(text: str) -> list[str]:
    return [f"solution_plan_pattern:{p.pattern}" for p in SOLUTION_PLAN_PATTERNS if p.search(text)]


def domain_block_hashes_from_prompts(
    prompts_by_task: dict[str, str],
    tasks: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Verify same-domain API blocks are byte-identical."""
    by_domain: dict[str, dict[str, str]] = {d: {} for d in DOMAIN_OPS}
    for tid, prompt in prompts_by_task.items():
        domain = tasks[tid]["domain_ops"]
        block = extract_domain_api_block(prompt)
        by_domain[domain][tid] = _sha256_text(block)
    report: dict[str, dict[str, Any]] = {}
    for domain, mapping in by_domain.items():
        unique = sorted(set(mapping.values()))
        report[domain] = {
            "n_tasks": len(mapping),
            "unique_block_hashes": unique,
            "byte_identical": len(unique) == 1 and len(mapping) > 0,
            "block_sha256": unique[0] if len(unique) == 1 else None,
            "per_task": mapping,
        }
    return report


def evaluator_identity(root: Path | None = None) -> dict[str, str]:
    root = root or ROOT
    oracle_path = root / "agent_tools/finals_rebuild/math_task_oracles.py"
    success_path = root / "agent_tools/finals_rebuild/generator_success.py"
    return {
        "math_task_oracles_rel": "agent_tools/finals_rebuild/math_task_oracles.py",
        "math_task_oracles_sha256": _sha256_file(oracle_path),
        "generator_success_rel": "agent_tools/finals_rebuild/generator_success.py",
        "generator_success_sha256": _sha256_file(success_path),
    }


def build_all_prompts(root: Path | None = None) -> dict[str, Any]:
    root = root or ROOT
    inv_errors = validate_inventory()
    if inv_errors:
        raise RuntimeError(f"SSOT inventory invalid: {inv_errors}")

    template_hashes = write_domain_templates(root)
    templates = {d: load_domain_template(d, root) for d in DOMAIN_OPS}
    prompt_dir = root / PROMPT_DIR_REL
    prompt_dir.mkdir(parents=True, exist_ok=True)

    pool = load_pool_manifest(root)
    tasks = tasks_by_id(root)
    prompts: dict[str, str] = {}
    task_records: list[dict[str, Any]] = []

    for tid in pool["task_ids"]:
        task = tasks[tid]
        domain = task["domain_ops"]
        prompt = build_domain_menu_prompt(task, templates[domain])
        static_errors = validate_prompt_static(prompt, domain)
        if static_errors:
            raise RuntimeError(f"static validation failed for {tid}: {static_errors}")
        path = prompt_dir / f"{tid}.txt"
        path.write_text(prompt, encoding="utf-8", newline="\n")
        prompts[tid] = prompt
        task_records.append(
            {
                "condition": CONDITION,
                "task_id": tid,
                "domain_ops": domain,
                "prompt_path": f"{PROMPT_DIR_REL}/{tid}.txt".replace("\\", "/"),
                "prompt_sha256": _sha256_text(prompt),
                "template_rel": f"{TEMPLATE_DIR_REL}/{DOMAIN_TEMPLATE_FILES[domain]}",
                "template_sha256": template_hashes[domain],
                "domain_block_sha256": _sha256_text(extract_domain_api_block(prompt)),
                "char_count": len(prompt),
                "utf8_byte_count": len(prompt.encode("utf-8")),
                "model_called": False,
                "prompt_frozen": True,
            }
        )

    block_report = domain_block_hashes_from_prompts(prompts, tasks)
    if not all(v["byte_identical"] for v in block_report.values()):
        raise RuntimeError(f"domain block hash mismatch: {block_report}")

    # Template-level leakage scan (domain menus must not contain formal answers).
    template_leak_hits: list[str] = []
    task_list = [tasks[tid] for tid in pool["task_ids"]]
    for domain, text in templates.items():
        hits = scan_answer_leakage(text, task_list, allow_frozen_overlap=False)
        for h in hits:
            template_leak_hits.append(f"{domain}:{h}")
    if template_leak_hits:
        raise RuntimeError(f"answer leakage in domain templates: {template_leak_hits}")

    solution_hits: list[str] = []
    for tid, prompt in prompts.items():
        for h in scan_solution_plan(prompt):
            solution_hits.append(f"{tid}:{h}")
    if solution_hits:
        raise RuntimeError(f"solution-plan patterns in prompts: {solution_hits}")

    # Prompt leakage: answers must not appear in domain block / system header.
    prompt_leak_hits: list[str] = []
    for tid, prompt in prompts.items():
        domain_part = prompt.split("## Task", 1)[0]
        hits = scan_answer_leakage(domain_part, task_list, allow_frozen_overlap=False)
        for h in hits:
            prompt_leak_hits.append(f"{tid}:{h}")
    if prompt_leak_hits:
        raise RuntimeError(f"answer leakage in domain/system sections: {prompt_leak_hits}")

    eval_id = evaluator_identity(root)
    manifest = {
        "manifest_id": MANIFEST_ID,
        "condition": CONDITION,
        "condition_label": CONDITION_LABEL,
        "experiment_id": EXPERIMENT_ID,
        "prompt_revision": "ab2d_domain_menu_v1",
        "n_tasks": len(task_records),
        "n_domains": 4,
        "llm_policy": "freeze_only; zero model calls",
        "pool_id": pool["pool_id"],
        "pool_identity_hash": pool["pool_identity_hash"],
        "task_freeze_hash": pool["task_freeze_hash"],
        "evaluator_identity": eval_id,
        "ssot_inventory_ok": True,
        "domain_template_sha256": template_hashes,
        "domain_block_hashes": {
            d: block_report[d]["block_sha256"] for d in DOMAIN_OPS
        },
        "domain_blocks_byte_identical": {
            d: block_report[d]["byte_identical"] for d in DOMAIN_OPS
        },
        "template_dir": TEMPLATE_DIR_REL,
        "prompt_dir": PROMPT_DIR_REL,
        "artifact_root": ARTIFACT_ROOT_REL,
        "forbidden_content": [
            "task-specific guardrail",
            "prescribed API set for a task",
            "API call order / solution steps",
            "formal intermediate or final answers",
            "oracle/audit answer payloads",
            "task_id→solution lookup",
        ],
        "allowed_per_task_additions": [
            "frozen task description (stem)",
            "frozen_params",
        ],
        "tasks": task_records,
        "audits": {
            "template_answer_leakage_hits": template_leak_hits,
            "prompt_domain_section_answer_leakage_hits": prompt_leak_hits,
            "solution_plan_hits": solution_hits,
        },
    }
    manifest_path = root / MANIFEST_REL
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return {
        "manifest": manifest,
        "prompts": prompts,
        "block_report": block_report,
        "template_hashes": template_hashes,
    }


def run_zero_model_preflight(root: Path | None = None) -> dict[str, Any]:
    """Build 16 prompts, verify isolation/hashes, load evaluator — no model calls."""
    root = root or ROOT
    built = build_all_prompts(root)
    manifest = built["manifest"]
    pool = load_pool_manifest(root)
    tasks = tasks_by_id(root)

    # Confirm evaluator import works without calling a model.
    from agent_tools.finals_rebuild.math_task_oracles import evaluate_math_task_oracle
    from agent_tools.finals_rebuild.generator_success import REQUIRED_RETURN_KEYS

    eval_smoke = []
    for tid in pool["task_ids"]:
        task = tasks[tid]
        # Smoke: evaluator accepts the known correct answer (local, not LLM).
        verdict = evaluate_math_task_oracle(
            task["oracle_type"], task["oracle_payload"], task["correct_answer"]
        )
        eval_smoke.append(
            {
                "task_id": tid,
                "evaluator_accepts_reference_answer": bool(verdict.get("is_correct")),
                "error": verdict.get("error"),
            }
        )

    cross = []
    for tid in pool["task_ids"]:
        prompt = built["prompts"][tid]
        domain = tasks[tid]["domain_ops"]
        errs = validate_prompt_static(prompt, domain)
        cross.append({"task_id": tid, "static_errors": errs, "ok": not errs})

    artifact_root = root / ARTIFACT_ROOT_REL
    artifact_root.mkdir(parents=True, exist_ok=True)
    (artifact_root / "qualification").mkdir(exist_ok=True)
    (artifact_root / "formal").mkdir(exist_ok=True)
    (artifact_root / "preregistration").mkdir(exist_ok=True)

    preflight_dir = root / PREFLIGHT_REL
    preflight_dir.mkdir(parents=True, exist_ok=True)

    summary = {
        "preflight_id": "math16_ab2d_domain_menu_preflight_v1",
        "condition": CONDITION,
        "model_calls": 0,
        "n_prompts": len(built["prompts"]),
        "n_prompts_expected": 16,
        "prompts_complete": len(built["prompts"]) == 16,
        "domain_blocks_byte_identical": all(
            built["block_report"][d]["byte_identical"] for d in DOMAIN_OPS
        ),
        "domain_block_hashes": {
            d: built["block_report"][d]["block_sha256"] for d in DOMAIN_OPS
        },
        "cross_domain_isolation_ok": all(r["ok"] for r in cross),
        "cross_domain_rows": cross,
        "solution_plan_clean": len(manifest["audits"]["solution_plan_hits"]) == 0,
        "answer_leakage_clean": (
            len(manifest["audits"]["template_answer_leakage_hits"]) == 0
            and len(manifest["audits"]["prompt_domain_section_answer_leakage_hits"]) == 0
        ),
        "evaluator_loaded": True,
        "required_return_keys": list(REQUIRED_RETURN_KEYS),
        "evaluator_reference_smoke_all_pass": all(
            r["evaluator_accepts_reference_answer"] for r in eval_smoke
        ),
        "evaluator_smoke": eval_smoke,
        "namespace": {
            "experiment_id": EXPERIMENT_ID,
            "artifact_root": ARTIFACT_ROOT_REL,
            "prompt_dir": PROMPT_DIR_REL,
            "template_dir": TEMPLATE_DIR_REL,
            "manifest": MANIFEST_REL,
        },
        "pool_identity_hash": pool["pool_identity_hash"],
        "task_freeze_hash": pool["task_freeze_hash"],
        "manifest_id": manifest["manifest_id"],
    }
    summary["overall_pass"] = (
        summary["prompts_complete"]
        and summary["domain_blocks_byte_identical"]
        and summary["cross_domain_isolation_ok"]
        and summary["solution_plan_clean"]
        and summary["answer_leakage_clean"]
        and summary["evaluator_reference_smoke_all_pass"]
        and summary["model_calls"] == 0
    )
    (preflight_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return summary


if __name__ == "__main__":
    result = run_zero_model_preflight()
    print(
        json.dumps(
            {
                k: result[k]
                for k in (
                    "preflight_id",
                    "n_prompts",
                    "prompts_complete",
                    "domain_blocks_byte_identical",
                    "cross_domain_isolation_ok",
                    "solution_plan_clean",
                    "answer_leakage_clean",
                    "evaluator_reference_smoke_all_pass",
                    "model_calls",
                    "overall_pass",
                    "domain_block_hashes",
                )
            },
            ensure_ascii=False,
            indent=2,
        )
    )
