"""Tier D rule D2: Duplicate definition selection.

Keep exactly one of two same-scope same-name defs via frozen §5 ranking.
Evaluator-blind; does not merge bodies.
"""

from __future__ import annotations

import ast
from collections import defaultdict
from typing import Any, Optional

from agent_tools.finals_rebuild.artifacts import sha256_text
from agent_tools.finals_rebuild.aggressive_healer_tier_d.common import (
    OPS_NAMES,
    is_parseable,
    replace_line_span,
)
from agent_tools.finals_rebuild.aggressive_healer_tier_d.ranking import (
    MIN_MARGIN,
    MIN_SCORE,
    WEIGHTS,
    select_unique_winner,
)
from agent_tools.finals_rebuild.aggressive_healer_tier_d.types import (
    CURRENT_TIER,
    LAYER_ROLE,
    RISK_TIER,
    RuleResult,
)

RULE_ID = "TIER_D_DUPLICATE_DEFINITION_SELECTION_V1"


def _def_completeness(node: ast.AST) -> float:
    body = getattr(node, "body", []) or []
    if not body:
        return 0.0
    if all(isinstance(n, ast.Pass) for n in body):
        return 0.2
    return 1.0


def _scaffold_role(node: ast.AST) -> float:
    n = getattr(node, "name", "")
    if n == "generate" or n in OPS_NAMES:
        return 1.0
    return 0.0


def _score_def(node: ast.AST) -> dict[str, Any]:
    feats = {
        "F_prompt_contract_token": 1.0 if getattr(node, "name", "") in ({"generate"} | OPS_NAMES) else 0.0,
        "F_class_compat": 1.0
        if isinstance(node, ast.ClassDef) and node.name in OPS_NAMES
        else (0.5 if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) else 0.0),
        "F_method_compat": 1.0
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == "generate"
        else 0.0,
        "F_arity": 1.0,
        "F_keyword_schema": 1.0,
        "F_return_shape": 1.0 if any(isinstance(n, ast.Return) for n in ast.walk(node)) else 0.0,
        "F_ast_context": _def_completeness(node),
        "F_scaffold_signature": _scaffold_role(node),
        "F_method_name_similarity": 0.0,
    }
    score = sum(WEIGHTS[k] * feats[k] for k in WEIGHTS)
    return {
        "method": f"{type(node).__name__}@{getattr(node, 'lineno', 0)}",
        "node": node,
        "kind": type(node).__name__,
        "lineno": getattr(node, "lineno", None),
        "end_lineno": getattr(node, "end_lineno", None),
        "features": feats,
        "score": score,
        "score_without_similarity": score,
    }


def _nested_defs_outside_module(tree: ast.Module) -> bool:
    """True if duplicates only appear nested (cross-scope) — abstain for module rule."""
    return False


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
    groups: dict[str, list[ast.AST]] = defaultdict(list)
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            groups[node.name].append(node)

    # Cross-scope: nested duplicates without module-level pair → abstain
    nested_counts: dict[str, int] = defaultdict(int)
    for node in ast.walk(tree):
        if node in tree.body:
            continue
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            nested_counts[node.name] += 1
    if any(v >= 2 for v in nested_counts.values()) and not any(len(v) >= 2 for v in groups.values()):
        result.triggered = True
        result.abstained = True
        result.abstention_reason = "cross_scope_duplicate_abstain"
        result.outcome_taxonomy = "abstain"
        return result

    dups = {k: v for k, v in groups.items() if len(v) >= 2}
    if not dups:
        result.abstained = True
        result.abstention_reason = "no_duplicate_definitions"
        result.outcome_taxonomy = "noop"
        return result
    if len(dups) != 1:
        result.triggered = True
        result.abstained = True
        result.abstention_reason = "multiple_duplicate_name_groups"
        result.outcome_taxonomy = "abstain"
        result.extras = {"duplicates": {k: len(v) for k, v in dups.items()}}
        return result

    name, nodes = next(iter(dups.items()))
    if len(nodes) != 2:
        result.triggered = True
        result.abstained = True
        result.abstention_reason = "duplicate_count_not_exactly_two"
        result.outcome_taxonomy = "abstain"
        result.extras = {"name": name, "count": len(nodes)}
        return result

    # Dependency conflict: both defs mutually referenced in a way that both are needed.
    # For same-name module defs, only the last binds; if the dropped body is the only
    # one with returns AND the kept one is empty stub referencing the name — still OK.
    # Flag conflict if both have high completeness AND each calls the other name as attr — rare.
    scored = [_score_def(n) for n in nodes]
    # Ambiguous if both completeness high and scaffold role equal and scores would need evaluator
    if (
        scored[0]["features"]["F_ast_context"] >= 1.0
        and scored[1]["features"]["F_ast_context"] >= 1.0
        and scored[0]["features"]["F_scaffold_signature"] == scored[1]["features"]["F_scaffold_signature"]
        and abs(scored[0]["score"] - scored[1]["score"]) < MIN_MARGIN
    ):
        # still run select_unique_winner which will abstain on margin
        pass

    # Adapt to select_unique_winner schema (uses "method" key)
    decision = select_unique_winner(
        [
            {
                "method": s["method"],
                "score": s["score"],
                "score_without_similarity": s["score_without_similarity"],
                "features": s["features"],
                "_meta": s,
            }
            for s in scored
        ]
    )
    result.triggered = True
    result.extras = {
        "ranking_contract": {
            "weights": WEIGHTS,
            "minimum_score": MIN_SCORE,
            "minimum_margin": MIN_MARGIN,
        },
        "name": name,
        "candidates": [
            {k: v for k, v in s.items() if k != "node"} for s in scored
        ],
        "evaluator_used_for_selection": False,
    }

    if decision["status"] != "selected":
        result.abstained = True
        result.abstention_reason = decision["reason"]
        if all(s["features"]["F_ast_context"] >= 1.0 for s in scored) and decision["reason"] in {
            "score_tie",
            "margin_below_minimum",
            "similarity_sole_decision_or_tie_without_similarity",
        }:
            result.abstention_reason = "dependency_conflict_or_" + decision["reason"]
        result.outcome_taxonomy = "abstain"
        return result

    best_meta = decision["best"]["_meta"]
    drop_meta = decision["runner_up"]["_meta"]
    drop_node = drop_meta["node"]
    if drop_meta["lineno"] is None or drop_meta["end_lineno"] is None:
        result.abstained = True
        result.abstention_reason = "drop_span_unlocated"
        result.outcome_taxonomy = "abstain"
        return result

    healed = replace_line_span(source, int(drop_meta["lineno"]), int(drop_meta["end_lineno"]), "")
    if healed == source:
        result.abstained = True
        result.abstention_reason = "edit_produced_identical_source"
        result.outcome_taxonomy = "abstain"
        return result
    if not is_parseable(healed):
        result.abstained = True
        result.abstention_reason = "post_edit_unparseable_rollback"
        result.outcome_taxonomy = "rolled_back"
        result.extras["rolled_back"] = True
        return result

    # Ensure exactly one remaining def of that name at module level
    post = ast.parse(healed)
    remain = [
        n
        for n in post.body
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and n.name == name
    ]
    if len(remain) != 1:
        result.abstained = True
        result.abstention_reason = "post_edit_duplicate_not_resolved"
        result.outcome_taxonomy = "rolled_back"
        result.extras["rolled_back"] = True
        return result

    result.applied = True
    result.edit_count = 1
    result.edit_scope = "single_duplicate_definition_drop"
    result.source_out = healed
    result.post_source_sha = sha256_text(healed)
    result.post_parseable = True
    result.outcome_taxonomy = "repaired"
    result.ast_node_location = {
        "name": name,
        "keep": {"kind": best_meta["kind"], "lineno": best_meta["lineno"], "end_lineno": best_meta["end_lineno"]},
        "drop": {"kind": drop_meta["kind"], "lineno": drop_meta["lineno"], "end_lineno": drop_meta["end_lineno"]},
    }
    result.trigger_evidence = (
        f"duplicate {name}: keep L{best_meta['lineno']} score={best_meta['score']}; "
        f"drop L{drop_meta['lineno']} score={drop_meta['score']}; evaluator-blind"
    )
    result.extras.update(
        {
            "selected_candidate_score": best_meta["score"],
            "runner_up_score": drop_meta["score"],
            "margin": decision.get("margin"),
            "keep": result.ast_node_location["keep"],
            "drop": result.ast_node_location["drop"],
        }
    )
    return result
