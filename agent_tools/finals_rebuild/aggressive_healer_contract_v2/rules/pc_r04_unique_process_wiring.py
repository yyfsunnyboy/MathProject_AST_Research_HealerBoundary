# -*- coding: utf-8 -*-
"""PC-R04 Unique Process Wiring: insert unique missing full-plan API step only.

Fail-closed: requires full-plan, single generate, complete AST, uniquely missing
required call with unique insertion site and unique output binding. Almost all
complex failures abstain.
"""
from __future__ import annotations

import ast
from typing import Any

from agent_tools.finals_rebuild.aggressive_healer_contract_v2.ast_utils import (
    count_generate_defs,
    fqname,
    is_parseable,
    iter_ops_calls,
    parse_tree,
)
from agent_tools.finals_rebuild.aggressive_healer_contract_v2.certificate import make_certificate
from agent_tools.finals_rebuild.aggressive_healer_contract_v2.types import RuleOutcome

RULE_ID = "PC-R04_UNIQUE_PROCESS_WIRING_V2"
RULE_VERSION = "v2.0.0"

# Development registry intentionally empty of ACCEPT examples in freeze v2.0.0;
# rule is fail-closed scaffolding + certificates for ABSTAIN dominance.
DISCOVERY_CELLS: list[str] = []
DEBUGGING_CELLS: list[str] = []
POSITIVE_EXAMPLES: list[str] = []
NEGATIVE_EXAMPLES = [
    "qwen_9b__ce115_calc_polynomial_factor_roots_l1__ab2d_full_v2__seed_2026071301",
    "qwen_9b__ce111_q08_polynomial_factor_parameter_recovery__ab2d_full_v2__seed_2026071301",
    "qwen_4b__ce115_calc_polynomial_factor_roots_l1__ab2d_full_v2__seed_2026072001",
]


def apply_once(
    source: str,
    *,
    contract: dict[str, Any],
    cell_id: str,
    task_id: str,
    condition: str,
    model_key: str,
) -> RuleOutcome:
    preconditions = [
        "condition_is_full_plan",
        "required_calls_present_in_contract",
        "ast_parseable",
        "single_generate",
        "no_contradictory_branches",
        "exactly_one_missing_required_call",
        "unique_insertion_point",
        "unique_output_binding",
    ]
    if condition != "ab2d_full_v2":
        return _abstain(source, contract, cell_id, task_id, condition, model_key, "not_full_plan", preconditions)
    fp = contract.get("full_plan_constraints") or {}
    required = fp.get("required_calls") or []
    if not required:
        return _abstain(source, contract, cell_id, task_id, condition, model_key, "no_required_calls", preconditions)
    if not is_parseable(source):
        return _abstain(source, contract, cell_id, task_id, condition, model_key, "source_not_parseable", preconditions)
    tree = parse_tree(source)
    assert tree is not None
    if count_generate_defs(tree) != 1:
        return _abstain(source, contract, cell_id, task_id, condition, model_key, "generate_count_not_1", preconditions)

    # Contradictory: multiple near-duplicate generate fragments already filtered;
    # refuse if both if/else incomplete bodies (placeholder: many bare Pass with comments only not tracked)
    present = {fqname(c) for c in iter_ops_calls(tree)}
    required_names = [c["fqname"] for c in required]
    missing = [n for n in required_names if n not in present]
    if len(missing) != 1:
        return _abstain(
            source,
            contract,
            cell_id,
            task_id,
            condition,
            model_key,
            f"missing_count_{len(missing)}_not_unique",
            preconditions,
        )
    # Even with one missing call, insertion site is rarely unique without evaluator — abstain fail-closed.
    return _abstain(
        source,
        contract,
        cell_id,
        task_id,
        condition,
        model_key,
        "insertion_point_not_uniquely_provable",
        preconditions,
    )


def _abstain(source, contract, cell_id, task_id, condition, model_key, reason, preconditions):
    cert = make_certificate(
        rule_id=RULE_ID,
        decision="ABSTAIN",
        contract=contract,
        contract_clause="unique_process_wiring",
        cell_id=cell_id,
        task_id=task_id,
        condition=condition,
        model_key=model_key,
        ast_location={},
        before_snippet="",
        after_snippet="",
        before_source=source,
        after_source=source,
        candidate_count=0,
        preconditions=preconditions,
        postconditions=[],
        changed_ast_nodes=[],
        unrelated_ast_unchanged=True,
        abstention_reason=reason,
        extras={"rule_version": RULE_VERSION},
    )
    return RuleOutcome(
        rule_id=RULE_ID, applied=False, abstained=True, source_out=source, certificate=cert, abstention_reason=reason
    )
