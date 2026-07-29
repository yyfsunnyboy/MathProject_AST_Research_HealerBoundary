"""A1: core.normalize_fullwidth_python_punctuation (delegate to Minimal Core)."""

from __future__ import annotations

from agent_tools.finals_rebuild.aggressive_healer_tier_a.common import (
    is_parseable,
    source_sha,
)
from agent_tools.finals_rebuild.aggressive_healer_tier_a.types import RuleResult
from agent_tools.finals_rebuild.core_adapter import (
    normalize_fullwidth_python_punctuation,
)

RULE_ID = "core.normalize_fullwidth_python_punctuation"
SEQUENCE_INDEX = 1


def apply_once(source: str) -> RuleResult:
    pre_sha = source_sha(source)
    pre_parse = is_parseable(source)
    result = RuleResult(
        rule_id=RULE_ID,
        sequence_index=SEQUENCE_INDEX,
        pre_source_sha=pre_sha,
        pre_parseable=pre_parse,
        source_out=source,
        extras={"protected_span_policy": "tokenize_mask"},
    )

    if source == "":
        result.abstained = True
        result.abstention_reason = "empty_source_noop"
        result.outcome_taxonomy = "noop"
        result.post_source_sha = pre_sha
        result.post_parseable = pre_parse
        return result

    healed = normalize_fullwidth_python_punctuation(source)
    post_sha = source_sha(healed)
    post_parse = is_parseable(healed)
    result.post_source_sha = post_sha
    result.post_parseable = post_parse
    result.source_out = healed

    if healed == source:
        # Distinguish "nothing to do" vs fail-closed (still has mapped chars but
        # re-parse failed). Fail-closed leaves original; count unprotected mapped
        # only via change detection — no change means abstain/noop.
        result.abstained = True
        result.abstention_reason = "no_unprotected_mapped_or_fail_closed"
        result.outcome_taxonomy = "noop"
        result.trigger_evidence = "normalize_fullwidth_returned_identical"
        return result

    mapped = sum(
        1
        for a, b in zip(source, healed)
        if a != b
    )
    # Length-preserving replacements only under this rule.
    if len(source) != len(healed):
        # Spec forbids non-replacement edits; treat as abstain + restore.
        result.abstained = True
        result.abstention_reason = "unexpected_length_change"
        result.outcome_taxonomy = "abstain"
        result.source_out = source
        result.post_source_sha = pre_sha
        result.post_parseable = pre_parse
        return result

    result.triggered = True
    result.applied = True
    result.edit_count = 1
    result.edit_scope = "fullwidth_syntax_punctuation"
    result.trigger_evidence = f"mapped_char_replacements={mapped}"
    result.extras["mapped_char_count"] = mapped
    result.outcome_taxonomy = "repaired"
    return result
