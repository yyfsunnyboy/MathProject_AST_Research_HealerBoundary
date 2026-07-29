"""Pipeline wrapper for Tier C2 default_optional_pure_form_cleanup."""

from __future__ import annotations

from agent_tools.finals_rebuild.aggressive_healer_tier_c2.rule_default_optional_cleanup import (
    RULE_ID,
    apply_once,
)
from agent_tools.finals_rebuild.aggressive_healer_tier_c2.types import PipelineResult
from agent_tools.finals_rebuild.artifacts import sha256_text


def run_tier_c2_default_optional_cleanup(source: str) -> PipelineResult:
    """Run the narrow Tier C2 rule once with idempotence + rollback guards.

    Decision path is answer-blind and evaluator-blind.
    """
    pre_sha = sha256_text(source)
    step = apply_once(source)
    logs = [step.to_audit_dict()]

    if not step.applied:
        return PipelineResult(
            pre_source=source,
            post_source=source,
            pre_source_sha=pre_sha,
            post_source_sha=pre_sha,
            rule_logs=logs,
            rules_fired=[],
            mutation_count=0,
            pipeline_idempotent=True,
            outcome_taxonomy=step.outcome_taxonomy,
            abstention_reason=step.abstention_reason,
            rolled_back=False,
        )

    if step.edit_count > 1:
        return PipelineResult(
            pre_source=source,
            post_source=source,
            pre_source_sha=pre_sha,
            post_source_sha=pre_sha,
            rule_logs=logs,
            rules_fired=[],
            mutation_count=step.edit_count,
            pipeline_idempotent=False,
            outcome_taxonomy="budget_exceeded_abort",
            abstention_reason="mutation_count_exceeded",
            rolled_back=True,
        )

    healed = step.source_out
    verify = apply_once(healed)
    if verify.applied or verify.source_out != healed:
        return PipelineResult(
            pre_source=source,
            post_source=source,
            pre_source_sha=pre_sha,
            post_source_sha=pre_sha,
            rule_logs=logs + [verify.to_audit_dict()],
            rules_fired=[RULE_ID],
            mutation_count=1,
            pipeline_idempotent=False,
            outcome_taxonomy="non_idempotent_abort",
            abstention_reason="NON_IDEMPOTENT_ABORT",
            rolled_back=True,
        )

    return PipelineResult(
        pre_source=source,
        post_source=healed,
        pre_source_sha=pre_sha,
        post_source_sha=sha256_text(healed),
        rule_logs=logs,
        rules_fired=[RULE_ID],
        mutation_count=1,
        pipeline_idempotent=True,
        outcome_taxonomy="repaired",
        rolled_back=False,
    )
