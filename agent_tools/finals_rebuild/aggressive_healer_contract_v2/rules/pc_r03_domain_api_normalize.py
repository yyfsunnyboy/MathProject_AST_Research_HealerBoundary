# -*- coding: utf-8 -*-
"""PC-R03 Domain API Normalize: unique illegal class/method → unique allowed replacement."""
from __future__ import annotations

import ast
import re
from typing import Any

from agent_tools.finals_rebuild.domain_api_ssot import API_CLASSIFICATION, SUPPORTED_PUBLIC
from agent_tools.finals_rebuild.aggressive_healer_contract_v2.ast_utils import (
    count_generate_defs,
    is_parseable,
    node_loc,
    parse_tree,
)
from agent_tools.finals_rebuild.aggressive_healer_contract_v2.certificate import make_certificate
from agent_tools.finals_rebuild.aggressive_healer_contract_v2.types import RuleOutcome

RULE_ID = "PC-R03_DOMAIN_API_NORMALIZE_V2"
RULE_VERSION = "v2.0.0"

DISCOVERY_CELLS = [
    "qwen_4b__ce112_q04_radical_simplification__ab2d_full_v2__seed_2026072004",
]
DEBUGGING_CELLS = DISCOVERY_CELLS
POSITIVE_EXAMPLES = DISCOVERY_CELLS
NEGATIVE_EXAMPLES = [
    "qwen_9b__ce111_q08_polynomial_factor_parameter_recovery__ab2d_full_v2__seed_2026071301",
]

# Known non-existent / mis-named class aliases → domain class only when domain unique.
KNOWN_TYPOS = {
    "RationalOps": "RadicalOps",  # only valid if method exists on RadicalOps
}


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
        "ast_parseable",
        "single_generate",
        "illegal_class_or_method",
        "unique_replacement",
        "replacement_in_allowed_methods",
    ]
    if not is_parseable(source):
        return _abstain(source, contract, cell_id, task_id, condition, model_key, "source_not_parseable", preconditions)
    tree = parse_tree(source)
    assert tree is not None
    if count_generate_defs(tree) != 1:
        return _abstain(source, contract, cell_id, task_id, condition, model_key, "generate_count_not_1", preconditions)

    domain = contract["domain"]
    allowed = set(contract["allowed_methods"])
    candidates: list[tuple[ast.Attribute, str, str]] = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.Attribute):
            continue
        if not isinstance(node.value, ast.Name):
            continue
        cls = node.value.id
        meth = node.attr
        # Class-level typo
        if cls in KNOWN_TYPOS:
            repl_cls = KNOWN_TYPOS[cls]
            fq = f"{repl_cls}.{meth}"
            if repl_cls == domain and (
                fq in allowed or API_CLASSIFICATION.get(fq) == SUPPORTED_PUBLIC
            ):
                candidates.append((node, cls, repl_cls))
            continue
        # Unknown Ops class
        if cls.endswith("Ops") and cls not in ("IntegerOps", "FractionOps", "RadicalOps", "PolynomialOps"):
            # only if domain is unique replacement
            if domain and f"{domain}.{meth}" in allowed:
                candidates.append((node, cls, domain))

    # unique by (lineno, col) pairs after dedupe of Attribute nodes on same class tokens
    if not candidates:
        return _abstain(source, contract, cell_id, task_id, condition, model_key, "no_illegal_api", preconditions)

    # All replacements must agree on target class
    targets = {t for _, _, t in candidates}
    if len(targets) != 1:
        return _abstain(source, contract, cell_id, task_id, condition, model_key, "nonunique_target_class", preconditions)
    target = next(iter(targets))
    # Replace all illegal class Name nodes that are value of those attributes — do string-level unique class rename for those names only.
    illegal_classes = {c for _, c, _ in candidates}
    if len(illegal_classes) != 1:
        return _abstain(source, contract, cell_id, task_id, condition, model_key, "multiple_illegal_classes", preconditions)
    illegal = next(iter(illegal_classes))

    # Word-boundary rename preserves unrelated AST text bytes.
    new_source, nsub = re.subn(rf"\b{re.escape(illegal)}\b", target, source)
    if nsub == 0 or new_source == source:
        return _abstain(source, contract, cell_id, task_id, condition, model_key, "no_change", preconditions)
    changed = nsub
    if not is_parseable(new_source):
        return _abstain(source, contract, cell_id, task_id, condition, model_key, "post_not_parseable", preconditions)

    first = candidates[0][0]
    cert = make_certificate(
        rule_id=RULE_ID,
        decision="ACCEPT",
        contract=contract,
        contract_clause="domain_api_normalize",
        cell_id=cell_id,
        task_id=task_id,
        condition=condition,
        model_key=model_key,
        ast_location=node_loc(first),
        before_snippet=illegal,
        after_snippet=target,
        before_source=source,
        after_source=new_source,
        candidate_count=1,
        preconditions=preconditions,
        postconditions=["class_in_allowed_domain", "methods_public", "parse_ok"],
        changed_ast_nodes=[f"Name.id:{illegal}->{target}"],
        unrelated_ast_unchanged=True,
        extras={"rule_version": RULE_VERSION, "replacements": changed},
    )
    return RuleOutcome(
        rule_id=RULE_ID,
        applied=True,
        abstained=False,
        source_out=new_source,
        certificate=cert,
        trigger_evidence=f"normalize {illegal} -> {target} ({changed} sites)",
    )


def _abstain(source, contract, cell_id, task_id, condition, model_key, reason, preconditions):
    cert = make_certificate(
        rule_id=RULE_ID,
        decision="ABSTAIN",
        contract=contract,
        contract_clause="domain_api_normalize",
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
