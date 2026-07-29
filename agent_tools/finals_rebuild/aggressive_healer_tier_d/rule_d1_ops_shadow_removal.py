"""Tier D rule D1: Ops Shadow Removal.

Remove a unique model-defined Ops class/binding that shadows the runtime-injected Ops.
Budget: one shadow site per cell per pass.
"""

from __future__ import annotations

import ast
from typing import Any, Optional

from agent_tools.finals_rebuild.artifacts import sha256_text
from agent_tools.finals_rebuild.aggressive_healer_tier_d.common import (
    OPS_NAMES,
    is_parseable,
    replace_line_span,
)
from agent_tools.finals_rebuild.aggressive_healer_tier_d.types import (
    CURRENT_TIER,
    LAYER_ROLE,
    RISK_TIER,
    RuleResult,
)

RULE_ID = "TIER_D_OPS_SHADOW_REMOVAL_V1"
SEQUENCE_INDEX = 2


def _shadow_nodes(tree: ast.Module) -> list[dict[str, Any]]:
    """Collect unique shadow definition nodes at any nesting (ClassDef / Assign / AnnAssign / FunctionDef)."""
    found: list[dict[str, Any]] = []

    class Visitor(ast.NodeVisitor):
        def visit_ClassDef(self, node: ast.ClassDef) -> None:
            if node.name in OPS_NAMES:
                found.append(
                    {
                        "kind": "ClassDef",
                        "name": node.name,
                        "node": node,
                        "lineno": node.lineno,
                        "end_lineno": node.end_lineno,
                    }
                )
            self.generic_visit(node)

        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            if node.name in OPS_NAMES:
                found.append(
                    {
                        "kind": "FunctionDef",
                        "name": node.name,
                        "node": node,
                        "lineno": node.lineno,
                        "end_lineno": node.end_lineno,
                    }
                )
            self.generic_visit(node)

        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
            if node.name in OPS_NAMES:
                found.append(
                    {
                        "kind": "AsyncFunctionDef",
                        "name": node.name,
                        "node": node,
                        "lineno": node.lineno,
                        "end_lineno": node.end_lineno,
                    }
                )
            self.generic_visit(node)

        def visit_Assign(self, node: ast.Assign) -> None:
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id in OPS_NAMES:
                    found.append(
                        {
                            "kind": "Assign",
                            "name": t.id,
                            "node": node,
                            "lineno": node.lineno,
                            "end_lineno": node.end_lineno,
                        }
                    )
            self.generic_visit(node)

        def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
            if isinstance(node.target, ast.Name) and node.target.id in OPS_NAMES:
                found.append(
                    {
                        "kind": "AnnAssign",
                        "name": node.target.id,
                        "node": node,
                        "lineno": node.lineno,
                        "end_lineno": node.end_lineno,
                    }
                )
            self.generic_visit(node)

    Visitor().visit(tree)
    return found


def _parent_map(tree: ast.AST) -> dict[int, ast.AST]:
    parents: dict[int, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parents[id(child)] = parent
    return parents


def _suite_list(parent: ast.AST, node: ast.AST) -> Optional[list]:
    for attr in ("body", "orelse", "finalbody", "handlers"):
        val = getattr(parent, attr, None)
        if isinstance(val, list) and node in val:
            return val
        if attr == "handlers" and isinstance(val, list):
            for h in val:
                if isinstance(h, ast.ExceptHandler) and node in h.body:
                    return h.body
    return None


def apply_once(source: str) -> RuleResult:
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

    tree = ast.parse(source)
    shadows = _shadow_nodes(tree)
    names = sorted({s["name"] for s in shadows})

    if not shadows:
        result.abstained = True
        result.abstention_reason = "no_ops_shadow"
        result.outcome_taxonomy = "noop"
        return result

    if len(names) > 1 or len(shadows) > 1:
        result.triggered = True
        result.abstained = True
        result.abstention_reason = "multiple_ops_shadows"
        result.outcome_taxonomy = "abstain"
        result.extras = {"shadow_names": names, "shadow_site_count": len(shadows)}
        return result

    site = shadows[0]
    node = site["node"]
    if getattr(node, "lineno", None) is None or getattr(node, "end_lineno", None) is None:
        result.triggered = True
        result.abstained = True
        result.abstention_reason = "shadow_span_unlocated"
        result.outcome_taxonomy = "abstain"
        return result

    parents = _parent_map(tree)
    parent = parents.get(id(node))
    # If removing the only statement in a suite, replace with `pass` to keep parseable.
    replacement = ""
    if parent is not None:
        suite = _suite_list(parent, node)
        if suite is not None and len(suite) == 1:
            indent = " " * getattr(node, "col_offset", 0)
            replacement = f"{indent}pass\n"

    start = int(node.lineno)
    end = int(node.end_lineno)
    healed = replace_line_span(source, start, end, replacement)
    if healed == source:
        result.triggered = True
        result.abstained = True
        result.abstention_reason = "edit_produced_identical_source"
        result.outcome_taxonomy = "abstain"
        return result

    if not is_parseable(healed):
        result.triggered = True
        result.abstained = True
        result.abstention_reason = "post_edit_unparseable_rollback"
        result.outcome_taxonomy = "rolled_back"
        result.extras["rolled_back"] = True
        return result

    # Post-condition: no remaining shadow of that Ops name
    post_tree = ast.parse(healed)
    remaining = [s for s in _shadow_nodes(post_tree) if s["name"] == site["name"]]
    if remaining:
        result.triggered = True
        result.abstained = True
        result.abstention_reason = "shadow_still_present_after_edit"
        result.outcome_taxonomy = "rolled_back"
        result.extras["rolled_back"] = True
        return result

    result.triggered = True
    result.applied = True
    result.edit_count = 1
    result.edit_scope = "single_ops_shadow_removal"
    result.source_out = healed
    result.post_source_sha = sha256_text(healed)
    result.post_parseable = True
    result.outcome_taxonomy = "repaired"
    result.ast_node_location = {
        "kind": site["kind"],
        "name": site["name"],
        "lineno": start,
        "end_lineno": end,
        "removed_span": {"start_lineno": start, "end_lineno": end},
    }
    result.trigger_evidence = (
        f"unique Ops shadow {site['kind']} {site['name']} at L{start}-{end}; "
        "scaffold provides injected same-name Ops; calls resolve to injected version after removal"
    )
    result.extras = {
        "shadow_names": [site["name"]],
        "removed_span": {"start_lineno": start, "end_lineno": end},
        "replaced_with_pass": bool(replacement.strip()),
    }
    return result
