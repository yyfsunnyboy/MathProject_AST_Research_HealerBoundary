# -*- coding: utf-8 -*-
"""PC-R02 Operand Order Restore: only when full-plan specifies unique arg roles."""
from __future__ import annotations

import ast
from typing import Any

from agent_tools.finals_rebuild.aggressive_healer_contract_v2.ast_utils import (
    count_generate_defs,
    is_call_ops,
    is_parseable,
    node_loc,
    parse_tree,
    replace_node_span,
    unparse,
)
from agent_tools.finals_rebuild.aggressive_healer_contract_v2.certificate import make_certificate
from agent_tools.finals_rebuild.aggressive_healer_contract_v2.types import RuleOutcome

RULE_ID = "PC-R02_OPERAND_ORDER_RESTORE_V2"
RULE_VERSION = "v2.0.0"

DISCOVERY_CELLS = [
    "qwen_4b__ce115_calc_exact_rational_expression_l1__ab2d_full_v2__seed_2026072003",
    "qwen_4b__ce115_calc_exact_rational_expression_l1__ab2d_full_v2__seed_2026072004",
]
DEBUGGING_CELLS = DISCOVERY_CELLS
POSITIVE_EXAMPLES = DISCOVERY_CELLS
NEGATIVE_EXAMPLES = [
    "qwen_4b__ce111_q02_polynomial_division_remainder__ab2d_full_v2__seed_2026071301",
]


def _is_create_zero(node: ast.AST) -> bool:
    if not isinstance(node, ast.Call):
        return False
    f = node.func
    if not (isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name)):
        return False
    if f.value.id != "FractionOps" or f.attr != "create":
        return False
    if len(node.args) != 1:
        return False
    a0 = node.args[0]
    return isinstance(a0, ast.Constant) and a0.value == 0


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
        "operand_order_clause_present",
        "ast_parseable",
        "single_generate",
        "unique_swapped_call",
    ]
    if condition != "ab2d_full_v2":
        return _abstain(source, contract, cell_id, task_id, condition, model_key, "not_full_plan", preconditions)
    constraints = contract.get("operand_order_constraints") or []
    if not constraints:
        return _abstain(source, contract, cell_id, task_id, condition, model_key, "no_operand_clause", preconditions)
    if not is_parseable(source):
        return _abstain(source, contract, cell_id, task_id, condition, model_key, "source_not_parseable", preconditions)
    tree = parse_tree(source)
    assert tree is not None
    if count_generate_defs(tree) != 1:
        return _abstain(source, contract, cell_id, task_id, condition, model_key, "generate_count_not_1", preconditions)

    clause = constraints[0]
    # Find FractionOps.sub(term, create(0)) that should be sub(create(0), term)
    swapped: list[ast.Call] = []
    for node in ast.walk(tree):
        if not is_call_ops(node, "FractionOps", "sub"):
            continue
        assert isinstance(node, ast.Call)
        if len(node.args) != 2:
            continue
        a0, a1 = node.args[0], node.args[1]
        if _is_create_zero(a1) and not _is_create_zero(a0):
            swapped.append(node)

    if len(swapped) == 0:
        return _abstain(source, contract, cell_id, task_id, condition, model_key, "no_swapped_call", preconditions)
    if len(swapped) != 1:
        return _abstain(
            source, contract, cell_id, task_id, condition, model_key, f"candidate_count_{len(swapped)}", preconditions
        )

    call = swapped[0]
    a0, a1 = call.args[0], call.args[1]
    new_call = ast.Call(
        func=call.func,
        args=[a1, a0],
        keywords=list(call.keywords),
    )
    ast.copy_location(new_call, call)
    end = getattr(call, "end_lineno", None)
    if end is not None:
        new_call.end_lineno = call.end_lineno  # type: ignore[attr-defined]
        new_call.end_col_offset = call.end_col_offset  # type: ignore[attr-defined]
    new_text = unparse(new_call)
    new_source = replace_node_span(source, call, new_text)
    if new_source is None or new_source == source:
        return _abstain(source, contract, cell_id, task_id, condition, model_key, "span_replace_failed", preconditions)
    if not is_parseable(new_source):
        return _abstain(source, contract, cell_id, task_id, condition, model_key, "post_not_parseable", preconditions)

    cert = make_certificate(
        rule_id=RULE_ID,
        decision="ACCEPT",
        contract=contract,
        contract_clause=clause["clause_id"],
        cell_id=cell_id,
        task_id=task_id,
        condition=condition,
        model_key=model_key,
        ast_location=node_loc(call),
        before_snippet=unparse(call),
        after_snippet=new_text,
        before_source=source,
        after_source=new_source,
        candidate_count=1,
        preconditions=preconditions,
        postconditions=["arg0_is_zero", "arg1_is_term", "parse_ok"],
        changed_ast_nodes=["Call.FractionOps.sub.args_swap"],
        unrelated_ast_unchanged=True,
        extras={"rule_version": RULE_VERSION},
    )
    return RuleOutcome(
        rule_id=RULE_ID,
        applied=True,
        abstained=False,
        source_out=new_source,
        certificate=cert,
        trigger_evidence="swapped FractionOps.sub operands to match scaffold",
    )


def _abstain(source, contract, cell_id, task_id, condition, model_key, reason, preconditions):
    cert = make_certificate(
        rule_id=RULE_ID,
        decision="ABSTAIN",
        contract=contract,
        contract_clause="operand_order",
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
