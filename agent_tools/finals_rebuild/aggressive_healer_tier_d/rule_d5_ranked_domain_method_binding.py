"""Tier D rule D5: Ranked domain method binding.

Only renames a unique wrong Ops method attribute; arguments preserved.
Ranking uses frozen §5 contract — evaluator-blind.
"""

from __future__ import annotations

import ast
import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Optional

from agent_tools.finals_rebuild.artifacts import sha256_text
from agent_tools.finals_rebuild.aggressive_healer_tier_d.common import (
    OPS_NAMES,
    is_parseable,
)
from agent_tools.finals_rebuild.aggressive_healer_tier_d.ranking import (
    MIN_MARGIN,
    MIN_SCORE,
    WEIGHTS,
    score_method_candidate,
    select_unique_winner,
)
from agent_tools.finals_rebuild.aggressive_healer_tier_d.types import (
    CURRENT_TIER,
    LAYER_ROLE,
    RISK_TIER,
    RuleResult,
)

RULE_ID = "TIER_D_RANKED_DOMAIN_METHOD_BINDING_V1"
_CONTRACT_MATRIX = (
    Path(__file__).resolve().parents[3]
    / "docs/experiments/manifests/math16_ab2d_task_contract_matrix_v1.json"
)

_DOMAIN_TO_CLASS = {
    "Integer": "IntegerOps",
    "Fraction": "FractionOps",
    "Radical": "RadicalOps",
    "Polynomial": "PolynomialOps",
}


def _load_contract(task_id: str, condition: str) -> Optional[dict[str, Any]]:
    if condition not in {"ab2d", "ab2d_spec_v2"}:
        return None
    data = json.loads(_CONTRACT_MATRIX.read_text(encoding="utf-8"))
    for c in data["contracts"]:
        if c["task_id"] == task_id and c["condition_code"] == condition:
            return c
    return None


def _offset(lines: list[str], lineno: int, col: int) -> int:
    pos = 0
    for i in range(lineno - 1):
        pos += len(lines[i])
    return pos + col


def _call_ast_context(tree: ast.AST, call: ast.Call) -> str:
    for node in ast.walk(tree):
        if isinstance(node, ast.Return) and node.value is call:
            return "return"
        if isinstance(node, ast.Assign) and node.value is call:
            return "assign"
        if isinstance(node, ast.Expr) and node.value is call:
            return "expr"
    return "other"


def _replace_attr_name(source: str, attr: ast.Attribute, new_name: str) -> Optional[str]:
    if (
        getattr(attr, "end_lineno", None) is None
        or getattr(attr, "end_col_offset", None) is None
        or getattr(attr, "lineno", None) is None
        or getattr(attr, "col_offset", None) is None
    ):
        return None
    # Replace only the attribute identifier span: from last '.'+1 to end of Attribute
    lines = source.splitlines(keepends=True)
    # Find the attr name start: end of value node + optional dots/spaces
    val = attr.value
    if getattr(val, "end_lineno", None) is None or getattr(val, "end_col_offset", None) is None:
        return None
    after_val = _offset(lines, val.end_lineno, val.end_col_offset)  # type: ignore[arg-type]
    end = _offset(lines, attr.end_lineno, attr.end_col_offset)  # type: ignore[arg-type]
    # skip '.' and whitespace between value and attr name
    i = after_val
    while i < end and source[i] in " \t\r\n":
        i += 1
    if i >= end or source[i] != ".":
        # fallback: replace trailing identifier matching old attr
        old = attr.attr
        # search backward from end for old name
        chunk = source[after_val:end]
        idx = chunk.rfind(old)
        if idx < 0:
            return None
        start = after_val + idx
        healed = source[:start] + new_name + source[start + len(old) :]
    else:
        i += 1
        while i < end and source[i] in " \t":
            i += 1
        start = i
        healed = source[:start] + new_name + source[end:]
    if not is_parseable(healed):
        return None
    return healed


def apply_once(
    source: str,
    *,
    task_id: str = "",
    condition: str = "",
    exposed_symbols: Optional[list[str]] = None,
    domain: Optional[str] = None,
) -> RuleResult:
    pre_sha = sha256_text(source)
    pre_parse = is_parseable(source)
    result = RuleResult(
        rule_id=RULE_ID,
        risk_tier=RISK_TIER,
        current_tier=CURRENT_TIER,
        layer_role=LAYER_ROLE,
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

    if exposed_symbols is None:
        contract = _load_contract(task_id, condition)
        if contract is None:
            result.abstained = True
            result.abstention_reason = "condition_has_no_domain_api_contract"
            result.outcome_taxonomy = "ineligible"
            return result
        if contract.get("system_status") in {"SYSTEM_CONTRACT_DEFECT", "UNRESOLVED"}:
            result.abstained = True
            result.abstention_reason = f"system_contract_{contract.get('system_status')}"
            result.outcome_taxonomy = "ineligible"
            return result
        exposed_symbols = list(contract.get("exposed_symbols") or [])
        domain = domain or contract.get("domain")

    by_cls: dict[str, set[str]] = defaultdict(set)
    for sym in exposed_symbols:
        if "." in sym:
            c, m = sym.split(".", 1)
            by_cls[c].add(m)
    domain_class = _DOMAIN_TO_CLASS.get(domain or "")

    tree = ast.parse(source)
    sites: list[dict[str, Any]] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        f = node.func
        if not (isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name)):
            continue
        if f.value.id not in OPS_NAMES:
            continue
        methods = by_cls.get(f.value.id)
        if not methods or f.attr in methods:
            continue
        if len(methods) < 2:
            continue
        sites.append(
            {
                "call": node,
                "attr": f,
                "ops_class": f.value.id,
                "method": f.attr,
                "lineno": getattr(node, "lineno", None),
                "n_pos": len(node.args),
                "kw_names": {k.arg for k in node.keywords if k.arg},
            }
        )

    if not sites:
        result.abstained = True
        result.abstention_reason = "no_ranked_wrong_method_site"
        result.outcome_taxonomy = "noop"
        return result
    if len(sites) > 1:
        result.triggered = True
        result.abstained = True
        result.abstention_reason = "multiple_ranked_binding_sites"
        result.outcome_taxonomy = "abstain"
        result.extras = {"site_count": len(sites)}
        return result

    site = sites[0]
    candidates = sorted(m for m in by_cls[site["ops_class"]] if m != site["method"])
    if len(candidates) < 2:
        result.abstained = True
        result.abstention_reason = "fewer_than_2_replacement_candidates"
        result.outcome_taxonomy = "noop"
        return result

    ast_ctx = _call_ast_context(tree, site["call"])
    scored = [
        score_method_candidate(
            ops_class=site["ops_class"],
            current_method=site["method"],
            candidate=m,
            exposed_methods=by_cls[site["ops_class"]],
            domain_class=domain_class,
            n_pos=site["n_pos"],
            kw_names=site["kw_names"],
            ast_context=ast_ctx,
        )
        for m in candidates
    ]
    decision = select_unique_winner(scored)
    result.triggered = True
    result.extras = {
        "ranking_contract": {
            "weights": WEIGHTS,
            "minimum_score": MIN_SCORE,
            "minimum_margin": MIN_MARGIN,
        },
        "candidates": decision.get("candidates"),
        "evaluator_used_for_selection": False,
    }

    if decision["status"] != "selected":
        result.abstained = True
        result.abstention_reason = decision["reason"]
        result.outcome_taxonomy = "abstain"
        return result

    best = decision["best"]
    new_method = best["method"]
    healed = _replace_attr_name(source, site["attr"], new_method)
    if healed is None:
        result.abstained = True
        result.abstention_reason = "surgical_attr_rename_failed_or_unparseable"
        result.outcome_taxonomy = "rolled_back"
        result.extras["rolled_back"] = True
        return result
    if healed == source:
        result.abstained = True
        result.abstention_reason = "edit_produced_identical_source"
        result.outcome_taxonomy = "abstain"
        return result

    result.applied = True
    result.edit_count = 1
    result.edit_scope = "single_domain_method_attribute_rename"
    result.source_out = healed
    result.post_source_sha = sha256_text(healed)
    result.post_parseable = True
    result.outcome_taxonomy = "repaired"
    result.ast_node_location = {
        "ops_class": site["ops_class"],
        "from_method": site["method"],
        "to_method": new_method,
        "lineno": site["lineno"],
    }
    result.trigger_evidence = (
        f"unique wrong binding {site['ops_class']}.{site['method']} -> {new_method}; "
        f"score={best['score']} margin={decision.get('margin')}; "
        "arguments preserved; evaluator-blind"
    )
    result.extras.update(
        {
            "selected_method": new_method,
            "selected_candidate_score": best["score"],
            "runner_up_score": None
            if decision.get("runner_up") is None
            else decision["runner_up"]["score"],
            "margin": decision.get("margin"),
            "similarity_sole_decision": False,
            "arguments_preserved": True,
        }
    )
    return result
