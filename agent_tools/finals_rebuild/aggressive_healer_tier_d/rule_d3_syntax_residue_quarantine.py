"""Tier D rule D3: Syntax Residue Quarantine.

Frozen strategy: comment-out (quarantine_mode=comment_out).
Budget: one contiguous trailing residue span after unique generate.
"""

from __future__ import annotations

import ast
from typing import Any, Optional

from agent_tools.finals_rebuild.artifacts import sha256_text
from agent_tools.finals_rebuild.aggressive_healer_tier_d.common import (
    comment_out_lines,
    is_parseable,
    names_bound_in_module_fragment,
    names_loaded_in,
    replace_line_span,
    unique_generate,
)
from agent_tools.finals_rebuild.aggressive_healer_tier_d.types import (
    CURRENT_TIER,
    LAYER_ROLE,
    RISK_TIER,
    RuleResult,
)

RULE_ID = "TIER_D_SYNTAX_RESIDUE_QUARANTINE_V1"
QUARANTINE_MODE = "comment_out"
SEQUENCE_INDEX = 1


def _classify_residue(source: str, tree: ast.Module) -> dict[str, Any]:
    gen = unique_generate(tree)
    if gen is None or getattr(gen, "end_lineno", None) is None:
        return {"status": "ineligible", "reason": "no_unique_generate_or_end_lineno"}

    lines = source.splitlines(keepends=True)
    start = gen.end_lineno + 1
    if start > len(lines):
        return {"status": "ineligible", "reason": "no_trailing_residue"}

    after = "".join(lines[gen.end_lineno :])
    if not after.strip():
        return {"status": "ineligible", "reason": "no_trailing_residue"}

    end = len(lines)
    # Drop trailing blank lines from span end for cleaner quarantine
    while end >= start and lines[end - 1].strip() == "":
        end -= 1
    if end < start:
        return {"status": "ineligible", "reason": "no_trailing_residue"}

    residue_text = "".join(lines[start - 1 : end])
    try:
        trailing_mod = ast.parse(after)
    except SyntaxError:
        return {
            "status": "eligible",
            "reason": "unparseable_trailing_residue_unique_span",
            "start_lineno": start,
            "end_lineno": end,
            "residue_text": residue_text,
            "generate_end_lineno": gen.end_lineno,
        }

    if any(
        isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
        for n in trailing_mod.body
    ):
        return {
            "status": "abstain",
            "reason": "trailing_contains_definitions",
            "start_lineno": start,
            "end_lineno": end,
        }

    if not trailing_mod.body:
        return {"status": "ineligible", "reason": "no_trailing_residue"}

    # Dependency: names bound in residue used by generate → abstain
    bound = names_bound_in_module_fragment(trailing_mod)
    used = names_loaded_in(gen)
    overlap = sorted(bound & used)
    if overlap:
        return {
            "status": "abstain",
            "reason": "residue_name_dependency_on_generate",
            "dependency_names": overlap,
            "start_lineno": start,
            "end_lineno": end,
        }

    return {
        "status": "eligible",
        "reason": "parseable_trailing_non_def_residue",
        "start_lineno": start,
        "end_lineno": end,
        "residue_text": residue_text,
        "generate_end_lineno": gen.end_lineno,
        "trailing_stmt_kinds": [type(n).__name__ for n in trailing_mod.body],
    }


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
        # Still allow quarantine when unique generate can be located via partial recovery?
        # Spec: prefer mechanical unique span. Without full parse we cannot locate generate safely.
        result.abstained = True
        result.abstention_reason = "candidate_not_parseable"
        result.outcome_taxonomy = "abstain"
        return result

    tree = ast.parse(source)
    info = _classify_residue(source, tree)

    if info["status"] == "ineligible":
        result.abstained = True
        result.abstention_reason = info["reason"]
        result.outcome_taxonomy = "noop"
        return result

    if info["status"] == "abstain":
        result.triggered = True
        result.abstained = True
        result.abstention_reason = info["reason"]
        result.outcome_taxonomy = "abstain"
        result.extras = {k: v for k, v in info.items() if k != "residue_text"}
        return result

    start = int(info["start_lineno"])
    end = int(info["end_lineno"])
    residue = info["residue_text"]
    quarantined = comment_out_lines(residue)
    if quarantined == residue:
        result.triggered = True
        result.abstained = True
        result.abstention_reason = "residue_already_commented"
        result.outcome_taxonomy = "noop"
        return result

    # Ensure quarantined block ends with newline if original span did not leave one for join
    if not quarantined.endswith("\n") and end < len(source.splitlines()):
        quarantined = quarantined + "\n"

    healed = replace_line_span(source, start, end, quarantined)
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

    result.triggered = True
    result.applied = True
    result.edit_count = 1
    result.edit_scope = "single_trailing_residue_quarantine"
    result.source_out = healed
    result.post_source_sha = sha256_text(healed)
    result.post_parseable = True
    result.outcome_taxonomy = "repaired"
    result.ast_node_location = {
        "residue_span": {"start_lineno": start, "end_lineno": end},
        "quarantine_mode": QUARANTINE_MODE,
        "generate_end_lineno": info.get("generate_end_lineno"),
    }
    result.trigger_evidence = (
        f"unique trailing residue after generate (reason={info['reason']}); "
        f"quarantine_mode={QUARANTINE_MODE}; span={start}-{end}"
    )
    result.extras = {
        "quarantine_mode": QUARANTINE_MODE,
        "residue_span": {"start_lineno": start, "end_lineno": end},
        "reason": info["reason"],
        "trailing_stmt_kinds": info.get("trailing_stmt_kinds"),
    }
    return result
