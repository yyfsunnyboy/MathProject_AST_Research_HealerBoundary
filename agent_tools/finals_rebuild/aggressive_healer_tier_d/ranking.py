"""Frozen Tier D §5 ranking contract (spec-provisional weights).

Evaluator / answer / post-repair outcomes are forbidden as features.
"""

from __future__ import annotations

import inspect
from difflib import SequenceMatcher
from typing import Any, Optional

from agent_tools.finals_rebuild.domain_api_ssot import DOMAIN_API_SSOT
from core.prompts.domain_function_library import (
    FractionOps,
    IntegerOps,
    PolynomialOps,
    RadicalOps,
)

WEIGHTS: dict[str, float] = {
    "F_prompt_contract_token": 5,
    "F_class_compat": 4,
    "F_method_compat": 4,
    "F_arity": 3,
    "F_keyword_schema": 3,
    "F_return_shape": 2,
    "F_ast_context": 2,
    "F_scaffold_signature": 3,
    "F_method_name_similarity": 1,
}
MIN_SCORE = 8
MIN_MARGIN = 2

OPS_CLASSES = {
    "IntegerOps": IntegerOps,
    "FractionOps": FractionOps,
    "RadicalOps": RadicalOps,
    "PolynomialOps": PolynomialOps,
}


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def method_sig(ops_class: str, method: str) -> Optional[inspect.Signature]:
    cls = OPS_CLASSES.get(ops_class)
    if cls is None or not hasattr(cls, method):
        return None
    fn = getattr(cls, method)
    if not callable(fn):
        return None
    try:
        return inspect.signature(fn)
    except (TypeError, ValueError):
        return None


def arity_ok(sig: inspect.Signature, n_pos: int, kw_names: set[str]) -> bool:
    params = [
        p
        for p in sig.parameters.values()
        if p.kind
        in (
            inspect.Parameter.POSITIONAL_ONLY,
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
            inspect.Parameter.KEYWORD_ONLY,
        )
    ]
    required = [
        p
        for p in params
        if p.default is inspect.Parameter.empty and p.kind != inspect.Parameter.KEYWORD_ONLY
    ]
    allowed_names = {p.name for p in params}
    if any(k not in allowed_names for k in kw_names):
        return False
    pos_capable = [
        p
        for p in params
        if p.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
    ]
    if n_pos > len(pos_capable):
        return False
    for p in required[n_pos:]:
        if p.name not in kw_names:
            return False
    return True


def keyword_schema_ok(sig: inspect.Signature, kw_names: set[str]) -> bool:
    allowed = {
        p.name
        for p in sig.parameters.values()
        if p.kind
        in (
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
            inspect.Parameter.KEYWORD_ONLY,
        )
    }
    return all(k in allowed for k in kw_names)


def score_method_candidate(
    *,
    ops_class: str,
    current_method: str,
    candidate: str,
    exposed_methods: set[str],
    domain_class: Optional[str],
    n_pos: int,
    kw_names: set[str],
    ast_context: str,
) -> dict[str, Any]:
    feats: dict[str, float] = {}
    feats["F_prompt_contract_token"] = 1.0 if candidate in exposed_methods else 0.0
    if domain_class and ops_class == domain_class:
        feats["F_class_compat"] = 1.0
    elif domain_class and ops_class != domain_class:
        feats["F_class_compat"] = 0.0
    else:
        feats["F_class_compat"] = 1.0 if ops_class in OPS_CLASSES else 0.0

    fq = f"{ops_class}.{candidate}"
    feats["F_method_compat"] = 1.0 if (candidate in exposed_methods or fq in DOMAIN_API_SSOT) else 0.0

    sig = method_sig(ops_class, candidate)
    if sig is None:
        feats["F_arity"] = 0.0
        feats["F_keyword_schema"] = 0.0
        feats["F_scaffold_signature"] = 0.0
    else:
        feats["F_arity"] = 1.0 if arity_ok(sig, n_pos, kw_names) else 0.0
        feats["F_keyword_schema"] = 1.0 if keyword_schema_ok(sig, kw_names) else 0.0
        feats["F_scaffold_signature"] = 1.0 if candidate in exposed_methods else 0.0

    feats["F_return_shape"] = (
        1.0 if ast_context in {"return", "assign"} and feats["F_method_compat"] else 0.0
    )
    feats["F_ast_context"] = 1.0 if ast_context in {"return", "assign", "expr"} else 0.0
    feats["F_method_name_similarity"] = similarity(current_method, candidate)

    score = sum(WEIGHTS[k] * feats[k] for k in WEIGHTS)
    score_wo_sim = sum(
        WEIGHTS[k] * feats[k] for k in WEIGHTS if k != "F_method_name_similarity"
    )
    return {
        "method": candidate,
        "features": feats,
        "score": score,
        "score_without_similarity": score_wo_sim,
    }


def select_unique_winner(scored: list[dict[str, Any]]) -> dict[str, Any]:
    """Apply §5 thresholds. Returns {status, reason, ...}."""
    if not scored:
        return {"status": "abstain", "reason": "empty_candidate_set"}

    ranked = sorted(scored, key=lambda x: (-x["score"], x["method"]))
    best = ranked[0]
    runner = ranked[1] if len(ranked) > 1 else None

    order_full = [s["method"] for s in ranked]
    ranked_wo = sorted(scored, key=lambda x: (-x["score_without_similarity"], x["method"]))
    if order_full[0] != ranked_wo[0]["method"] or (
        len(ranked_wo) > 1
        and ranked_wo[0]["score_without_similarity"] == ranked_wo[1]["score_without_similarity"]
    ):
        return {
            "status": "abstain",
            "reason": "similarity_sole_decision_or_tie_without_similarity",
            "candidates": ranked,
            "best": best,
            "runner_up": runner,
        }

    if best["score"] < MIN_SCORE:
        return {
            "status": "abstain",
            "reason": "best_score_below_minimum",
            "candidates": ranked,
            "best": best,
            "runner_up": runner,
            "minimum_score": MIN_SCORE,
        }

    if runner is not None:
        if best["score"] == runner["score"]:
            return {
                "status": "abstain",
                "reason": "score_tie",
                "candidates": ranked,
                "best": best,
                "runner_up": runner,
            }
        margin = best["score"] - runner["score"]
        if margin < MIN_MARGIN:
            return {
                "status": "abstain",
                "reason": "margin_below_minimum",
                "candidates": ranked,
                "best": best,
                "runner_up": runner,
                "margin": margin,
                "minimum_margin": MIN_MARGIN,
            }

    return {
        "status": "selected",
        "reason": "unique_highest_meets_thresholds",
        "candidates": ranked,
        "best": best,
        "runner_up": runner,
        "margin": None if runner is None else best["score"] - runner["score"],
        "similarity_sole_decision": False,
    }
