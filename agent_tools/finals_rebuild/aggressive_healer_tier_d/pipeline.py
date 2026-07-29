"""Minimal Tier D pipelines (Development slices).

Evaluator does not participate in repair selection.
"""

from __future__ import annotations

from typing import Any, Callable, Optional

from agent_tools.finals_rebuild.artifacts import sha256_text
from .common import is_parseable
from .types import PipelineResult, RuleResult
from . import rule_d1_ops_shadow_removal as d1
from . import rule_d2_duplicate_definition_selection as d2
from . import rule_d3_syntax_residue_quarantine as d3
from . import rule_d5_ranked_domain_method_binding as d5

# Frozen Development order for D3+D1 slice:
RULE_ORDER = (d3.RULE_ID, d1.RULE_ID)
_APPLY = {
    d3.RULE_ID: d3.apply_once,
    d1.RULE_ID: d1.apply_once,
}


def _run_single_rule_pipeline(
    source: str,
    *,
    apply_fn: Callable[..., RuleResult],
    apply_kwargs: Optional[dict[str, Any]] = None,
) -> PipelineResult:
    """Apply one rule at most once; single formal post-source; idempotent or rollback."""
    pre_sha = sha256_text(source)
    kwargs = apply_kwargs or {}
    step = apply_fn(source, **kwargs)
    logs = [step.to_audit_dict()]
    rule_id = step.rule_id

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
            outcome_taxonomy=step.outcome_taxonomy or ("abstain" if step.abstained else "noop"),
            abstention_reason=step.abstention_reason,
            rolled_back=False,
            selected_rule="",
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
            abstention_reason="mutation_count_exceeded_for_rule",
            rolled_back=True,
            selected_rule="",
        )

    healed = step.source_out
    if not is_parseable(healed):
        return PipelineResult(
            pre_source=source,
            post_source=source,
            pre_source_sha=pre_sha,
            post_source_sha=pre_sha,
            rule_logs=logs,
            rules_fired=[rule_id],
            mutation_count=1,
            pipeline_idempotent=False,
            outcome_taxonomy="rolled_back",
            abstention_reason="post_pipeline_unparseable_rollback",
            rolled_back=True,
            selected_rule="",
        )

    verify = apply_fn(healed, **kwargs)
    if verify.applied or verify.source_out != healed:
        return PipelineResult(
            pre_source=source,
            post_source=source,
            pre_source_sha=pre_sha,
            post_source_sha=pre_sha,
            rule_logs=logs + [verify.to_audit_dict()],
            rules_fired=[rule_id],
            mutation_count=1,
            pipeline_idempotent=False,
            outcome_taxonomy="non_idempotent_abort",
            abstention_reason="NON_IDEMPOTENT_ABORT",
            rolled_back=True,
            selected_rule="",
        )

    return PipelineResult(
        pre_source=source,
        post_source=healed,
        pre_source_sha=pre_sha,
        post_source_sha=sha256_text(healed),
        rule_logs=logs,
        rules_fired=[rule_id],
        mutation_count=1,
        pipeline_idempotent=True,
        outcome_taxonomy="repaired",
        rolled_back=False,
        selected_rule=rule_id,
    )


def run_tier_d_d5_pipeline(
    source: str,
    *,
    task_id: str = "",
    condition: str = "",
    exposed_symbols: Optional[list[str]] = None,
    domain: Optional[str] = None,
) -> PipelineResult:
    kwargs: dict[str, Any] = {}
    if exposed_symbols is not None:
        kwargs["exposed_symbols"] = exposed_symbols
    if task_id:
        kwargs["task_id"] = task_id
    if condition:
        kwargs["condition"] = condition
    if domain is not None:
        kwargs["domain"] = domain
    return _run_single_rule_pipeline(source, apply_fn=d5.apply_once, apply_kwargs=kwargs)


def run_tier_d_d2_pipeline(source: str) -> PipelineResult:
    return _run_single_rule_pipeline(source, apply_fn=d2.apply_once)


def run_tier_d_d3_d1_pipeline(source: str) -> PipelineResult:
    """Apply D3 then D1 at most once each; one formal post-source; idempotent or rollback."""
    pre_sha = sha256_text(source)
    current = source
    logs: list[dict] = []
    fired: list[str] = []
    mutations = 0

    for rule_id in RULE_ORDER:
        step = _APPLY[rule_id](current)
        logs.append(step.to_audit_dict())
        if not step.applied:
            continue
        if step.edit_count > 1:
            return PipelineResult(
                pre_source=source,
                post_source=source,
                pre_source_sha=pre_sha,
                post_source_sha=pre_sha,
                rule_logs=logs,
                rules_fired=fired,
                mutation_count=mutations + step.edit_count,
                pipeline_idempotent=False,
                outcome_taxonomy="budget_exceeded_abort",
                abstention_reason="mutation_count_exceeded_for_rule",
                rolled_back=True,
                selected_rule="",
            )
        current = step.source_out
        fired.append(rule_id)
        mutations += 1

    if mutations == 0:
        abstain_reason = ""
        taxonomy = "noop"
        for log in logs:
            if log.get("abstained") and log.get("abstention_reason"):
                abstain_reason = log["abstention_reason"]
                taxonomy = log.get("outcome_taxonomy") or "abstain"
        return PipelineResult(
            pre_source=source,
            post_source=source,
            pre_source_sha=pre_sha,
            post_source_sha=pre_sha,
            rule_logs=logs,
            rules_fired=[],
            mutation_count=0,
            pipeline_idempotent=True,
            outcome_taxonomy=taxonomy if abstain_reason else "noop",
            abstention_reason=abstain_reason,
            rolled_back=False,
            selected_rule="",
        )

    if not is_parseable(current):
        return PipelineResult(
            pre_source=source,
            post_source=source,
            pre_source_sha=pre_sha,
            post_source_sha=pre_sha,
            rule_logs=logs,
            rules_fired=fired,
            mutation_count=mutations,
            pipeline_idempotent=False,
            outcome_taxonomy="rolled_back",
            abstention_reason="post_pipeline_unparseable_rollback",
            rolled_back=True,
            selected_rule="",
        )

    verify = run_tier_d_d3_d1_pipeline_once_no_verify(current)
    if verify["mutation_count"] != 0 or verify["post_source"] != current:
        return PipelineResult(
            pre_source=source,
            post_source=source,
            pre_source_sha=pre_sha,
            post_source_sha=pre_sha,
            rule_logs=logs + verify["rule_logs"],
            rules_fired=fired,
            mutation_count=mutations,
            pipeline_idempotent=False,
            outcome_taxonomy="non_idempotent_abort",
            abstention_reason="NON_IDEMPOTENT_ABORT",
            rolled_back=True,
            selected_rule="",
        )

    selected = fired[-1] if len(fired) == 1 else "+".join(fired)
    return PipelineResult(
        pre_source=source,
        post_source=current,
        pre_source_sha=pre_sha,
        post_source_sha=sha256_text(current),
        rule_logs=logs,
        rules_fired=fired,
        mutation_count=mutations,
        pipeline_idempotent=True,
        outcome_taxonomy="repaired",
        rolled_back=False,
        selected_rule=selected,
    )


def run_tier_d_d3_d1_pipeline_once_no_verify(source: str) -> dict:
    """Single pass without recursive idempotence check (used by verify)."""
    current = source
    logs: list[dict] = []
    fired: list[str] = []
    mutations = 0
    for rule_id in RULE_ORDER:
        step = _APPLY[rule_id](current)
        logs.append(step.to_audit_dict())
        if step.applied:
            current = step.source_out
            fired.append(rule_id)
            mutations += 1
    return {
        "post_source": current,
        "mutation_count": mutations,
        "rule_logs": logs,
        "rules_fired": fired,
    }
