"""A4: TIER_A_UNIQUE_IMPORT_BINDING_REPAIR_V1."""

from __future__ import annotations

import ast
from typing import Any, Optional

from agent_tools.finals_rebuild.aggressive_healer_tier_a.common import (
    builtin_names,
    is_parseable,
    newline_of,
    source_sha,
)
from agent_tools.finals_rebuild.aggressive_healer_tier_a.types import RuleResult

RULE_ID = "TIER_A_UNIQUE_IMPORT_BINDING_REPAIR_V1"
SEQUENCE_INDEX = 4

# Frozen unique stdlib bindings only. No domain Ops. No multi-form symbols.
_UNIQUE_IMPORT_MAP: dict[str, tuple[str, str]] = {
    "Fraction": ("from fractions import Fraction", "stdlib.fractions.Fraction"),
    "Decimal": ("from decimal import Decimal", "stdlib.decimal.Decimal"),
    "defaultdict": (
        "from collections import defaultdict",
        "stdlib.collections.defaultdict",
    ),
    "Counter": ("from collections import Counter", "stdlib.collections.Counter"),
    "deque": ("from collections import deque", "stdlib.collections.deque"),
}

_EXCLUDED_DOMAIN_NAMES = frozenset(
    {
        "IntegerOps",
        "FractionOps",
        "RadicalOps",
        "PolynomialOps",
        "CalculusOps",
        "DomainFunctionHelper",
        "fmt_num",
    }
)


def _collect_bound_names(tree: ast.AST) -> set[str]:
    bound: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
            bound.add(node.name)
            for arg in node.args.args + node.args.posonlyargs + node.args.kwonlyargs:
                bound.add(arg.arg)
            if node.args.vararg:
                bound.add(node.args.vararg.arg)
            if node.args.kwarg:
                bound.add(node.args.kwarg.arg)
        elif isinstance(node, ast.ClassDef):
            bound.add(node.name)
        elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            bound.add(node.id)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                bound.add(alias.asname or alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if alias.name == "*":
                    continue
                bound.add(alias.asname or alias.name)
        elif isinstance(node, ast.ExceptHandler) and node.name:
            bound.add(node.name)
        elif isinstance(node, (ast.Global, ast.Nonlocal)):
            bound.update(node.names)
    return bound


def _collect_load_names(tree: ast.AST) -> set[str]:
    used: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            used.add(node.id)
    return used


def _has_ops_shadowing(tree: ast.AST) -> bool:
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name in _EXCLUDED_DOMAIN_NAMES:
            return True
        if isinstance(node, ast.FunctionDef) and node.name in _EXCLUDED_DOMAIN_NAMES:
            return True
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            if node.id in _EXCLUDED_DOMAIN_NAMES:
                return True
    return False


def _module_docstring_end_lineno(tree: ast.Module) -> Optional[int]:
    if not tree.body:
        return None
    first = tree.body[0]
    if isinstance(first, ast.Expr):
        val = first.value
        if isinstance(val, ast.Constant) and isinstance(val.value, str):
            return getattr(first, "end_lineno", first.lineno)
    return None


def _insert_import_stmt(source: str, stmt: str) -> str:
    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)
    if not lines:
        return stmt + "\n"

    end_doc = _module_docstring_end_lineno(tree)
    insert_at = 0 if end_doc is None else int(end_doc)
    # insert_at is 1-based end line of docstring → index to insert after
    idx = insert_at
    nl = newline_of(lines[0]) if lines else "\n"
    import_line = stmt + nl
    new_lines = lines[:idx] + [import_line] + lines[idx:]
    return "".join(new_lines)


def apply_once(source: str) -> RuleResult:
    pre_sha = source_sha(source)
    pre_parse = is_parseable(source)
    result = RuleResult(
        rule_id=RULE_ID,
        sequence_index=SEQUENCE_INDEX,
        pre_source_sha=pre_sha,
        pre_parseable=pre_parse,
        source_out=source,
        post_source_sha=pre_sha,
        post_parseable=pre_parse,
    )

    if not pre_parse:
        result.abstained = True
        result.abstention_reason = "source_not_parseable"
        result.outcome_taxonomy = "abstain"
        return result

    tree = ast.parse(source)
    if _has_ops_shadowing(tree):
        result.abstained = True
        result.abstention_reason = "ops_class_shadowing"
        result.outcome_taxonomy = "abstain"
        return result

    bound = _collect_bound_names(tree) | builtin_names()
    used = _collect_load_names(tree)
    missing = sorted(used - bound)

    # Drop excluded domain names (runtime-injected / Tier B territory).
    repairable: list[tuple[str, str, str]] = []
    blocked_domain: list[str] = []
    unknown: list[str] = []
    for name in missing:
        if name in _EXCLUDED_DOMAIN_NAMES:
            blocked_domain.append(name)
            continue
        if name in _UNIQUE_IMPORT_MAP:
            stmt, evid = _UNIQUE_IMPORT_MAP[name]
            repairable.append((name, stmt, evid))
        else:
            unknown.append(name)

    if blocked_domain and not repairable:
        result.abstained = True
        result.abstention_reason = "domain_ops_or_excluded_binding"
        result.outcome_taxonomy = "abstain"
        result.trigger_evidence = ",".join(blocked_domain)
        return result

    if len(repairable) == 0:
        result.abstained = True
        result.abstention_reason = (
            "no_unique_stdlib_binding_gap"
            if not missing
            else "missing_names_not_uniquely_mappable"
        )
        result.outcome_taxonomy = "noop" if not missing else "abstain"
        result.trigger_evidence = ",".join(missing)
        return result

    if len(repairable) > 1:
        result.abstained = True
        result.abstention_reason = f"multiple_missing_bindings_count_{len(repairable)}"
        result.outcome_taxonomy = "abstain"
        result.trigger_evidence = ",".join(n for n, _, _ in repairable)
        return result

    # If other unknown missing names coexist, cannot claim single unique repair.
    if unknown or blocked_domain:
        result.abstained = True
        result.abstention_reason = "non_unique_or_unmapped_additional_gaps"
        result.outcome_taxonomy = "abstain"
        result.trigger_evidence = ",".join(missing)
        return result

    name, stmt, evid = repairable[0]
    fixed = _insert_import_stmt(source, stmt)
    if not is_parseable(fixed):
        result.abstained = True
        result.abstention_reason = "import_insert_unparseable"
        result.outcome_taxonomy = "abstain"
        return result

    # Idempotence guard: if binding already present equivalently, insert would
    # duplicate — detect by re-checking bound after a dry concept: if name was
    # missing, insert is needed. If stmt already in source text exactly, abstain.
    if stmt in source:
        result.abstained = True
        result.abstention_reason = "equivalent_binding_already_present"
        result.outcome_taxonomy = "noop"
        return result

    result.triggered = True
    result.applied = True
    result.edit_count = 1
    result.edit_scope = "single_import_binding_insert"
    result.source_out = fixed
    result.post_source_sha = source_sha(fixed)
    result.post_parseable = True
    result.trigger_evidence = f"missing_name={name}"
    result.extras.update(
        {
            "missing_name": name,
            "binding_stmt": stmt,
            "ssot_or_stdlib_evidence_id": evid,
        }
    )
    result.outcome_taxonomy = "repaired"
    return result
