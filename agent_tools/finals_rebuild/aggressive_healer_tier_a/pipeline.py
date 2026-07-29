"""Aggressive Healer v1 Tier A pipeline orchestration."""

from __future__ import annotations

from typing import Callable, Optional

from agent_tools.finals_rebuild.aggressive_healer_tier_a import (
    rule_a1_fullwidth,
    rule_a2_delimiter,
    rule_a3_empty_suite,
    rule_a4_import_binding,
)
from agent_tools.finals_rebuild.aggressive_healer_tier_a.common import source_sha
from agent_tools.finals_rebuild.aggressive_healer_tier_a.types import (
    PipelineResult,
    RuleResult,
)

RULE_ORDER: tuple[str, ...] = (
    rule_a1_fullwidth.RULE_ID,
    rule_a2_delimiter.RULE_ID,
    rule_a3_empty_suite.RULE_ID,
    rule_a4_import_binding.RULE_ID,
)

_MAX_MUTATIONS = 4

RuleFn = Callable[[str], RuleResult]

_DEFAULT_RULES: tuple[RuleFn, ...] = (
    rule_a1_fullwidth.apply_once,
    rule_a2_delimiter.apply_once,
    rule_a3_empty_suite.apply_once,
    rule_a4_import_binding.apply_once,
)


def _run_once(
    source: str,
    rules: tuple[RuleFn, ...],
) -> tuple[str, list[RuleResult], list[str], int]:
    current = source
    logs: list[RuleResult] = []
    fired: list[str] = []
    mutations = 0
    for fn in rules:
        # Each rule at most once by construction (single forward pass).
        step = fn(current)
        logs.append(step)
        if step.applied:
            mutations += 1
            fired.append(step.rule_id)
            current = step.source_out
            if mutations > _MAX_MUTATIONS:
                break
    return current, logs, fired, mutations


def run_tier_a_pipeline(
    source: str,
    *,
    rules: Optional[tuple[RuleFn, ...]] = None,
    skip_idempotence_check: bool = False,
) -> PipelineResult:
    """Run Tier A rules in frozen order; rollback on non-idempotent output.

    Decision path is answer-blind and evaluator-blind: ``pass_fail`` / answer
    fields are never read.
    """
    rule_fns = rules if rules is not None else _DEFAULT_RULES
    pre_sha = source_sha(source)

    healed, logs, fired, mutations = _run_once(source, rule_fns)

    if mutations > _MAX_MUTATIONS:
        return PipelineResult(
            pre_source=source,
            post_source=source,
            pre_source_sha=pre_sha,
            post_source_sha=pre_sha,
            rule_logs=[r.to_audit_dict() for r in logs],
            rules_fired=fired,
            mutation_count=mutations,
            pipeline_idempotent=False,
            outcome_taxonomy="budget_exceeded_abort",
            abstention_reason="mutation_count_exceeded",
            rolled_back=True,
        )

    if skip_idempotence_check:
        return PipelineResult(
            pre_source=source,
            post_source=healed,
            pre_source_sha=pre_sha,
            post_source_sha=source_sha(healed),
            rule_logs=[r.to_audit_dict() for r in logs],
            rules_fired=fired,
            mutation_count=mutations,
            pipeline_idempotent=True,
            outcome_taxonomy="repaired" if mutations else "noop",
            rolled_back=False,
        )

    # Idempotence verification pass: must be zero-diff.
    verify, _vlogs, _vfired, verify_mutations = _run_once(healed, rule_fns)
    if verify != healed or verify_mutations != 0:
        return PipelineResult(
            pre_source=source,
            post_source=source,
            pre_source_sha=pre_sha,
            post_source_sha=pre_sha,
            rule_logs=[r.to_audit_dict() for r in logs],
            rules_fired=fired,
            mutation_count=mutations,
            pipeline_idempotent=False,
            outcome_taxonomy="non_idempotent_abort",
            abstention_reason="NON_IDEMPOTENT_ABORT",
            rolled_back=True,
        )

    outcome = "repaired" if mutations else "noop"
    if mutations and any(
        (not r.applied) and r.abstained and r.outcome_taxonomy == "abstain" for r in logs
    ):
        # Partial path still counts as repaired if any mutation landed.
        outcome = "repaired"

    return PipelineResult(
        pre_source=source,
        post_source=healed,
        pre_source_sha=pre_sha,
        post_source_sha=source_sha(healed),
        rule_logs=[r.to_audit_dict() for r in logs],
        rules_fired=fired,
        mutation_count=mutations,
        pipeline_idempotent=True,
        outcome_taxonomy=outcome,
        rolled_back=False,
    )
