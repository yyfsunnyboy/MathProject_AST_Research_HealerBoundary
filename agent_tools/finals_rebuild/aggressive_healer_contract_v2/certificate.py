# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Any, Optional

from agent_tools.finals_rebuild.artifacts import sha256_text
from agent_tools.finals_rebuild.aggressive_healer_contract_v2.types import PatchCertificate


def make_certificate(
    *,
    rule_id: str,
    decision: str,
    contract: dict[str, Any],
    contract_clause: str,
    cell_id: str,
    task_id: str,
    condition: str,
    model_key: str,
    ast_location: dict[str, Any],
    before_snippet: str,
    after_snippet: str,
    before_source: str,
    after_source: str,
    candidate_count: int,
    preconditions: list[str],
    postconditions: list[str],
    changed_ast_nodes: list[str],
    unrelated_ast_unchanged: bool,
    abstention_reason: str = "",
    extras: Optional[dict[str, Any]] = None,
) -> PatchCertificate:
    return PatchCertificate(
        rule_id=rule_id,
        decision=decision,
        contract_id=contract["contract_id"],
        contract_sha256=contract["contract_sha256"],
        contract_clause=contract_clause,
        cell_id=cell_id,
        task_id=task_id,
        condition=condition,
        model_key=model_key,
        ast_location=ast_location,
        before_snippet=before_snippet[:2000],
        after_snippet=after_snippet[:2000],
        before_source_sha256=sha256_text(before_source),
        after_source_sha256=sha256_text(after_source),
        candidate_count=candidate_count,
        preconditions=preconditions,
        postconditions=postconditions,
        changed_ast_nodes=changed_ast_nodes,
        unrelated_ast_unchanged=unrelated_ast_unchanged,
        expected_answer_not_read=True,
        evaluator_result_not_read=True,
        candidate_trial_count=1 if decision == "ACCEPT" else 0,
        abstention_reason=abstention_reason,
        extras=extras or {},
    )
