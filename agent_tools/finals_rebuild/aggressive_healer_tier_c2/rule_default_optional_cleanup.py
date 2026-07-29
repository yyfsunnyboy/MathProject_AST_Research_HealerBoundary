"""Tier C2 narrow rule: default_optional_pure_form_cleanup only.

legacy_rule_id: TIER_B_DOMAIN_SIGNATURE_FORM_REPAIR_V1
"""

from __future__ import annotations

import ast
import inspect
from typing import Any, Optional

from agent_tools.finals_rebuild.artifacts import sha256_text
from agent_tools.finals_rebuild.domain_api_ssot import DOMAIN_API_SSOT
from core.prompts.domain_function_library import (
    FractionOps,
    IntegerOps,
    PolynomialOps,
    RadicalOps,
)
from agent_tools.finals_rebuild.aggressive_healer_tier_c2.types import (
    CURRENT_TIER,
    LAYER_ROLE,
    RISK_TIER,
    RuleResult,
)

RULE_ID = "TIER_B_DOMAIN_SIGNATURE_FORM_REPAIR_V1"
SUBTYPE = "default_optional_pure_form_cleanup"
SEQUENCE_INDEX = 1

OPS_CLASSES = {
    "IntegerOps": IntegerOps,
    "FractionOps": FractionOps,
    "RadicalOps": RadicalOps,
    "PolynomialOps": PolynomialOps,
}


def _is_parseable(source: str) -> bool:
    try:
        ast.parse(source)
    except SyntaxError:
        return False
    return True


def _method_defaults(fqname: str) -> dict[str, Any]:
    cls_name, meth = fqname.split(".", 1)
    fn = getattr(OPS_CLASSES[cls_name], meth)
    defaults: dict[str, Any] = {}
    for name, param in inspect.signature(fn).parameters.items():
        if param.kind in (
            inspect.Parameter.VAR_POSITIONAL,
            inspect.Parameter.VAR_KEYWORD,
        ):
            continue
        if param.default is not inspect.Parameter.empty:
            defaults[name] = param.default
    return defaults


def _const_literal(node: ast.AST) -> tuple[bool, Any]:
    if isinstance(node, ast.Constant):
        return True, node.value
    return False, None


def _iter_ops_calls(tree: ast.AST) -> list[ast.Call]:
    calls: list[ast.Call] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if not isinstance(func, ast.Attribute):
            continue
        if not isinstance(func.value, ast.Name):
            continue
        if func.value.id not in OPS_CLASSES:
            continue
        calls.append(node)
    return calls


def _fqname(call: ast.Call) -> str:
    assert isinstance(call.func, ast.Attribute)
    assert isinstance(call.func.value, ast.Name)
    return f"{call.func.value.id}.{call.func.attr}"


def _has_end_pos(node: ast.AST) -> bool:
    return (
        getattr(node, "lineno", None) is not None
        and getattr(node, "col_offset", None) is not None
        and getattr(node, "end_lineno", None) is not None
        and getattr(node, "end_col_offset", None) is not None
    )


def _offset(lines: list[str], lineno: int, col: int) -> int:
    # 1-based lineno
    pos = 0
    for i in range(lineno - 1):
        pos += len(lines[i])
    return pos + col


def _remove_keyword_from_source(source: str, call: ast.Call, kw: ast.keyword) -> Optional[str]:
    """Surgically remove one keyword (and its comma) from a Call in source text."""
    if not _has_end_pos(kw) or not _has_end_pos(call):
        return None
    if kw.arg is None:
        return None

    lines = source.splitlines(keepends=True)
    kw_start = _offset(lines, kw.lineno, kw.col_offset)  # type: ignore[arg-type]
    kw_end = _offset(lines, kw.end_lineno, kw.end_col_offset)  # type: ignore[arg-type]

    # Expand start leftward to include a preceding comma and whitespace when present.
    start = kw_start
    i = start - 1
    while i >= 0 and source[i] in " \t":
        i -= 1
    if i >= 0 and source[i] == ",":
        start = i
        # also swallow spaces before comma? keep comma removal only from comma
    else:
        # Keyword may be the first argument: remove trailing comma after keyword instead.
        j = kw_end
        while j < len(source) and source[j] in " \t":
            j += 1
        if j < len(source) and source[j] == ",":
            kw_end = j + 1
            while kw_end < len(source) and source[kw_end] in " \t":
                kw_end += 1
        start = kw_start

    cleaned = source[:start] + source[kw_end:]
    # Normalize odd spaces inside empty-arg calls: f( ) → leave as-is if parseable
    if not _is_parseable(cleaned):
        return None
    return cleaned


def _find_redundant_default_sites(tree: ast.AST) -> list[dict[str, Any]]:
    sites: list[dict[str, Any]] = []
    for call in _iter_ops_calls(tree):
        fq = _fqname(call)
        if fq not in DOMAIN_API_SSOT:
            continue
        defaults = _method_defaults(fq)
        if not defaults:
            continue
        for kw in call.keywords:
            if kw.arg is None or kw.arg not in defaults:
                continue
            ok, lit = _const_literal(kw.value)
            if not ok:
                # non-literal → not a cleanup site (may contribute to ambiguity elsewhere)
                continue
            if lit != defaults[kw.arg]:
                continue
            sites.append(
                {
                    "call": call,
                    "keyword": kw,
                    "fqname": fq,
                    "keyword_name": kw.arg,
                    "default_value": defaults[kw.arg],
                    "lineno": getattr(call, "lineno", None),
                    "col_offset": getattr(call, "col_offset", None),
                }
            )
    return sites


def apply_once(source: str) -> RuleResult:
    """Apply at most one default_optional_pure_form_cleanup edit, else abstain."""
    pre_sha = sha256_text(source)
    pre_parse = _is_parseable(source)
    result = RuleResult(
        rule_id=RULE_ID,
        risk_tier=RISK_TIER,
        current_tier=CURRENT_TIER,
        layer_role=LAYER_ROLE,
        repair_subtype=SUBTYPE,
        sequence_index=SEQUENCE_INDEX,
        pre_source_sha=pre_sha,
        pre_parseable=pre_parse,
        source_out=source,
        post_source_sha=pre_sha,
        post_parseable=pre_parse,
    )

    if not pre_parse:
        result.abstained = True
        result.abstention_reason = "candidate_not_parseable"
        result.outcome_taxonomy = "abstain"
        return result

    tree = ast.parse(source)
    sites = _find_redundant_default_sites(tree)

    if not sites:
        # Distinguish already-correct vs no ops calls for audit clarity
        ops_calls = _iter_ops_calls(tree)
        result.abstained = True
        if not ops_calls:
            result.abstention_reason = "no_domain_api_call_present"
        else:
            result.abstention_reason = "no_redundant_optional_default_literal"
        result.outcome_taxonomy = "noop"
        return result

    # Group by call identity (lineno/col)
    by_call: dict[tuple[Any, Any], list[dict[str, Any]]] = {}
    for site in sites:
        key = (site["lineno"], site["col_offset"])
        by_call.setdefault(key, []).append(site)

    if len(by_call) > 1:
        result.abstained = True
        result.abstention_reason = f"ambiguous_multiple_call_sites_{len(by_call)}"
        result.outcome_taxonomy = "abstain"
        result.extras["candidate_site_count"] = len(sites)
        result.extras["call_site_count"] = len(by_call)
        return result

    call_sites = next(iter(by_call.values()))
    if len(call_sites) > 1:
        result.abstained = True
        result.abstention_reason = f"ambiguous_multiple_redundant_defaults_on_one_call_{len(call_sites)}"
        result.outcome_taxonomy = "abstain"
        result.extras["candidate_site_count"] = len(call_sites)
        return result

    site = call_sites[0]
    call: ast.Call = site["call"]
    kw: ast.keyword = site["keyword"]
    fq = site["fqname"]

    # Wrong-default literals are not in sites; non-literals excluded above.
    cleaned = _remove_keyword_from_source(source, call, kw)
    if cleaned is None:
        result.abstained = True
        result.abstention_reason = "surgical_keyword_removal_failed_or_unparseable"
        result.outcome_taxonomy = "abstain"
        return result

    if cleaned == source:
        result.abstained = True
        result.abstention_reason = "edit_produced_identical_source"
        result.outcome_taxonomy = "abstain"
        return result

    if not _is_parseable(cleaned):
        # rollback guard at rule level
        result.abstained = True
        result.abstention_reason = "post_edit_unparseable_rollback"
        result.outcome_taxonomy = "abstain"
        result.extras["rolled_back"] = True
        return result

    result.triggered = True
    result.applied = True
    result.edit_count = 1
    result.edit_scope = "single_optional_keyword_default_cleanup"
    result.ssot_entry_id = fq
    result.source_out = cleaned
    result.post_source_sha = sha256_text(cleaned)
    result.post_parseable = True
    result.ast_node_location = {
        "lineno": site["lineno"],
        "col_offset": site["col_offset"],
        "fqname": fq,
        "keyword": site["keyword_name"],
        "default_value": site["default_value"],
        "repair_subtype": SUBTYPE,
    }
    result.trigger_evidence = (
        f"SSOT/runtime default for {fq}.{site['keyword_name']} "
        f"is {site['default_value']!r}; candidate passes identical Constant literal; "
        f"removing keyword is mechanically binding-equivalent; single local call site"
    )
    result.outcome_taxonomy = "repaired"
    result.extras = {
        "repair_subtype": SUBTYPE,
        "keyword_removed": site["keyword_name"],
        "default_value": site["default_value"],
        "ssot_entry_id": fq,
        "name_similarity_used": False,
        "argument_expressions_preserved": True,
    }
    return result
