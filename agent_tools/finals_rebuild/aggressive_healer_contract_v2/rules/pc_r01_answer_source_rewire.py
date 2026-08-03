# -*- coding: utf-8 -*-
"""PC-R01 Answer Source Rewire: rewire answer fields to unique formatter sources."""
from __future__ import annotations

import ast
import re
from typing import Any

from agent_tools.finals_rebuild.aggressive_healer_contract_v2.ast_utils import (
    count_generate_defs,
    is_parseable,
    node_loc,
    parse_tree,
    replace_node_span,
    unparse,
)
from agent_tools.finals_rebuild.aggressive_healer_contract_v2.certificate import make_certificate
from agent_tools.finals_rebuild.aggressive_healer_contract_v2.types import RuleOutcome

RULE_ID = "PC-R01_ANSWER_SOURCE_REWIRE_V2"
RULE_VERSION = "v2.0.0"

# Discovery/dev cell registry (development-only; frozen into manifest, not used as special-case list at runtime)
DISCOVERY_CELLS = [
    "qwen_4b__ce111_q02_polynomial_division_remainder__ab2d_full_v2__seed_2026071301",
    "qwen_4b__ce111_q02_polynomial_division_remainder__ab2d_full_v2__seed_2026072001",
]
DEBUGGING_CELLS = DISCOVERY_CELLS
POSITIVE_EXAMPLES = DISCOVERY_CELLS
NEGATIVE_EXAMPLES = [
    "qwen_9b__ce115_calc_polynomial_factor_roots_l1__ab2d_full_v2__seed_2026071301",
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
        "single_generate_def",
        "ast_parseable",
        "contract_has_answer_source_rewire",
        "unique_candidate_only",
        "expected_answer_not_read",
        "evaluator_result_not_read",
    ]
    if not is_parseable(source):
        return _abstain(source, contract, cell_id, task_id, condition, model_key, "source_not_parseable", preconditions)
    tree = parse_tree(source)
    assert tree is not None
    if count_generate_defs(tree) != 1:
        return _abstain(source, contract, cell_id, task_id, condition, model_key, "generate_count_not_1", preconditions)

    specs = contract.get("answer_source_rewire") or []
    if not specs:
        return _abstain(source, contract, cell_id, task_id, condition, model_key, "no_rewire_clause", preconditions)

    candidates: list[tuple[ast.AST, str, str, dict[str, Any]]] = []
    for spec in specs:
        if spec.get("clause_id") != "REMAINDER_FROM_FORMAT_LATEX":
            continue
        # Find correct_answer dict assigns with remainder keyed wrongly.
        for node in ast.walk(tree):
            if not isinstance(node, ast.Dict):
                continue
            # Check if this looks like correct_answer payload
            keys = []
            for k in node.keys:
                if isinstance(k, ast.Constant) and isinstance(k.value, str):
                    keys.append(k.value)
            if "remainder" not in keys or "canonical_latex" not in keys:
                continue
            # Require r_latex assigned via format_latex somewhere
            if "format_latex" not in source or "r_latex" not in source:
                # also accept remainder_latex name
                if "remainder_latex" not in source:
                    continue
            rem_idx = keys.index("remainder")
            rem_val = node.values[rem_idx]
            rem_src = unparse(rem_val)
            # Wrong if uses str(...) of r or list/normalize or literal 0, and not r_latex/remainder_latex
            wrong = False
            if rem_src.startswith("str(") and (
                re.search(r"str\s*\(\s*r\s*\)", rem_src)
                or re.search(r"str\s*\(\s*0\s*\)", rem_src)
                or "normalize" in rem_src
                or re.search(r"str\s*\(\s*r_coeffs", rem_src)
                or re.search(r"str\s*\(\s*list", rem_src)
            ):
                wrong = True
            if rem_src in ("'0'", '"0"', "0"):
                wrong = True
            if rem_src in ("r_latex", "remainder_latex"):
                wrong = False
            if not wrong:
                continue
            # Prefer r_latex if exists, else remainder_latex
            target_name = "r_latex" if re.search(r"\br_latex\b", source) else (
                "remainder_latex" if re.search(r"\bremainder_latex\b", source) else None
            )
            if target_name is None:
                continue
            candidates.append((rem_val, rem_src, target_name, spec))

    if len(candidates) == 0:
        return _abstain(source, contract, cell_id, task_id, condition, model_key, "no_unique_rewire_target", preconditions)
    if len(candidates) != 1:
        return _abstain(
            source, contract, cell_id, task_id, condition, model_key, f"candidate_count_{len(candidates)}", preconditions
        )

    rem_val, rem_src, target_name, spec = candidates[0]
    new_source = replace_node_span(source, rem_val, target_name)
    if new_source is None or new_source == source:
        return _abstain(source, contract, cell_id, task_id, condition, model_key, "span_replace_failed", preconditions)
    if not is_parseable(new_source):
        return _abstain(source, contract, cell_id, task_id, condition, model_key, "post_not_parseable", preconditions)

    # Optionally rewire canonical_latex if it equals remainder value wrongly - only if unique
    # Keep single change for uniqueness (remainder only) when also_keys present and values differ
    postconditions = [
        "answer_key_remainder_equals_formatter_var",
        "parser_ok",
        "single_node_rewritten",
        "candidate_trial_count_1",
    ]
    cert = make_certificate(
        rule_id=RULE_ID,
        decision="ACCEPT",
        contract=contract,
        contract_clause=spec["clause_id"],
        cell_id=cell_id,
        task_id=task_id,
        condition=condition,
        model_key=model_key,
        ast_location=node_loc(rem_val),
        before_snippet=rem_src,
        after_snippet=target_name,
        before_source=source,
        after_source=new_source,
        candidate_count=1,
        preconditions=preconditions,
        postconditions=postconditions,
        changed_ast_nodes=["Dict.value[remainder]"],
        unrelated_ast_unchanged=True,
        extras={"rule_version": RULE_VERSION, "target_name": target_name},
    )
    return RuleOutcome(
        rule_id=RULE_ID,
        applied=True,
        abstained=False,
        source_out=new_source,
        certificate=cert,
        trigger_evidence=f"rewire remainder {rem_src} -> {target_name}",
    )


def _abstain(source, contract, cell_id, task_id, condition, model_key, reason, preconditions):
    cert = make_certificate(
        rule_id=RULE_ID,
        decision="ABSTAIN",
        contract=contract,
        contract_clause="answer_source_rewire",
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
        rule_id=RULE_ID,
        applied=False,
        abstained=True,
        source_out=source,
        certificate=cert,
        abstention_reason=reason,
    )
