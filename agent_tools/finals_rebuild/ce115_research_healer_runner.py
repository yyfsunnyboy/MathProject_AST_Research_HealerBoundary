"""Research-only allowlist Healer runner (H1+).

Execution policy (fixed):
- only rules present in RULE_ALLOWLIST are considered
- fixed priority ordering (ascending priority int)
- one change per pass; stop after the first changed rule
- after any change, re-parse / re-validate before finishing the pass
- H3 registers L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP; no L0/L1/L3/L4/L5/L6 rules
- must not call legacy Regex / AST / AntiDuplication / UnifiedCleanup pipelines

This module is intentionally separate from ``derive_ab3`` (legacy Ab2g→Ab3
path via UnifiedCleanupHealer). Research runs must go through
``run_research_healer`` / ``MathHealerRunner``.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Mapping, Protocol, Sequence

from agent_tools.finals_rebuild.ce115_research_healer_protocol import (
    PassProvenance,
    ResearchHealerResult,
    RuleOutcome,
    RuleProtocolError,
    make_parse_validation,
    sha256_text,
    validate_research_result,
    validate_rule_outcome,
)

# ---------------------------------------------------------------------------
# Allowlist — H3: first real transform rule (L2 single-key payload wrap)
# ---------------------------------------------------------------------------

from agent_tools.finals_rebuild.ce115_research_healer_rules_l2 import (
    LAYER as _L2_LAYER,
    PRIORITY as _L2_PRIORITY,
    RULE_ID as L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP,
    apply as _l2_apply,
    is_applicable as _l2_is_applicable,
    is_triggered as _l2_is_triggered,
)

RULE_ALLOWLIST: tuple[str, ...] = (L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP,)

FORBIDDEN_LEGACY_IMPORTS: frozenset[str] = frozenset(
    {
        "core.healers.unified_cleanup_healer",
        "core.healers.ast_healer",
        "core.healers.regex_healer",
        "core.healers.anti_duplication_healer",
        "UnifiedCleanupHealer",
        "ASTHealer",
        "RegexHealer",
        "AntiDuplicationHealer",
    }
)


class ResearchHealerRule(Protocol):
    """Contract for an allowlisted transform rule."""

    rule_id: str
    layer: str
    priority: int

    def is_applicable(self, source: str, context: Mapping[str, Any]) -> tuple[bool, Mapping[str, Any], str]:
        """Return (applicable, guard_results, reason)."""

    def is_triggered(self, source: str, context: Mapping[str, Any]) -> tuple[bool, str]:
        """Return (triggered, reason). Only called when applicable."""

    def apply(self, source: str, context: Mapping[str, Any]) -> tuple[str, Mapping[str, Any], str]:
        """Return (new_source, validation_extra, reason)."""


@dataclass(frozen=True)
class _RegisteredRule:
    rule_id: str
    layer: str
    priority: int
    is_applicable: Callable[[str, Mapping[str, Any]], tuple[bool, Mapping[str, Any], str]]
    is_triggered: Callable[[str, Mapping[str, Any]], tuple[bool, str]]
    apply: Callable[[str, Mapping[str, Any]], tuple[str, Mapping[str, Any], str]]


RULE_REGISTRY: dict[str, _RegisteredRule] = {
    L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP: _RegisteredRule(
        rule_id=L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP,
        layer=_L2_LAYER,
        priority=_L2_PRIORITY,
        is_applicable=_l2_is_applicable,
        is_triggered=_l2_is_triggered,
        apply=_l2_apply,
    ),
}

def _assert_no_legacy_pipeline() -> None:
    """Hard guard: research runner must not pull legacy healer pipelines."""
    import sys

    for name in FORBIDDEN_LEGACY_IMPORTS:
        if name in sys.modules and name.startswith("core.healers."):
            # Presence of the module object in sys.modules from *other* code paths
            # is tolerated only if this runner never imported it itself. We check
            # this module's own globals instead.
            pass
    for banned in (
        "UnifiedCleanupHealer",
        "ASTHealer",
        "RegexHealer",
        "AntiDuplicationHealer",
    ):
        if banned in globals():
            raise RuleProtocolError(f"research runner must not bind legacy healer {banned}")


def select_allowlisted_rules(
    allowlist: Sequence[str] = RULE_ALLOWLIST,
    registry: Mapping[str, _RegisteredRule] | None = None,
) -> list[_RegisteredRule]:
    """Return allowlisted rules sorted by fixed priority (then rule_id)."""
    reg = RULE_REGISTRY if registry is None else registry
    selected: list[_RegisteredRule] = []
    missing: list[str] = []
    for rule_id in allowlist:
        rule = reg.get(rule_id)
        if rule is None:
            missing.append(rule_id)
            continue
        selected.append(rule)
    if missing:
        raise RuleProtocolError(f"allowlist references unregistered rules: {missing}")
    selected.sort(key=lambda r: (r.priority, r.rule_id))
    return selected


def run_research_healer(
    source: str,
    *,
    context: Mapping[str, Any] | None = None,
    allowlist: Sequence[str] = RULE_ALLOWLIST,
    registry: Mapping[str, _RegisteredRule] | None = None,
    protected_snapshot: Mapping[str, Any] | None = None,
    max_passes: int = 1,
) -> ResearchHealerResult:
    """Run the research allowlist healer.

    With the default empty allowlist this always returns ``final_status='no_op'``
    and ``input_hash == output_hash``.
    """
    _assert_no_legacy_pipeline()
    if not isinstance(source, str):
        raise RuleProtocolError("source must be a str")
    ctx: dict[str, Any] = dict(context or {})
    protected = dict(protected_snapshot or {})

    input_hash = sha256_text(source)
    current = source
    outcomes: list[RuleOutcome] = []
    provenance: list[PassProvenance] = []
    notes: list[str] = []

    rules = select_allowlisted_rules(allowlist=allowlist, registry=registry)

    if not rules:
        provenance.append(
            PassProvenance(
                pass_index=0,
                candidate_rules_checked=(),
                selected_rule_id=None,
                selection_priority=None,
                stopped_after_change=False,
            )
        )
        notes.append("allowlist_empty" if not allowlist else "no_registered_allowlist_rules")
        result = ResearchHealerResult(
            input_source=source,
            output_source=current,
            input_hash=input_hash,
            output_hash=sha256_text(current),
            final_status="no_op",
            rule_outcomes=tuple(outcomes),
            provenance=tuple(provenance),
            real_model_calls=0,
            protected_snapshot=protected,
            notes=tuple(notes),
        )
        validate_research_result(result)
        return result

    changed_any = False
    for pass_index in range(max_passes):
        before = current
        before_hash = sha256_text(before)
        checked: list[str] = []
        selected_id: str | None = None
        selected_priority: int | None = None
        stopped_after_change = False
        pass_changed = False

        for rule in rules:
            checked.append(rule.rule_id)
            applicable, guards, app_reason = rule.is_applicable(before, ctx)
            if not applicable:
                outcome = RuleOutcome(
                    rule_id=rule.rule_id,
                    layer=rule.layer,
                    priority=rule.priority,
                    applicable=False,
                    triggered=False,
                    changed=False,
                    guard_results=dict(guards),
                    reason=app_reason,
                    before_hash=before_hash,
                    after_hash=before_hash,
                    validation=make_parse_validation(before),
                    stop_reason="not_applicable",
                )
                validate_rule_outcome(outcome)
                outcomes.append(outcome)
                continue

            triggered, trig_reason = rule.is_triggered(before, ctx)
            if not triggered:
                outcome = RuleOutcome(
                    rule_id=rule.rule_id,
                    layer=rule.layer,
                    priority=rule.priority,
                    applicable=True,
                    triggered=False,
                    changed=False,
                    guard_results=dict(guards),
                    reason=trig_reason,
                    before_hash=before_hash,
                    after_hash=before_hash,
                    validation=make_parse_validation(before),
                    stop_reason="not_triggered",
                )
                validate_rule_outcome(outcome)
                outcomes.append(outcome)
                continue

            # Attempt apply — still one-change-per-pass.
            new_source, extra_validation, apply_reason = rule.apply(before, ctx)
            after_hash = sha256_text(new_source)
            validation = make_parse_validation(new_source)
            validation.update(dict(extra_validation))
            did_change = new_source != before
            if did_change and not validation.get("ast_parse_success", False):
                outcome = RuleOutcome(
                    rule_id=rule.rule_id,
                    layer=rule.layer,
                    priority=rule.priority,
                    applicable=True,
                    triggered=True,
                    changed=False,
                    guard_results=dict(guards),
                    reason=f"validation_failed_after_apply: {apply_reason}",
                    before_hash=before_hash,
                    after_hash=before_hash,
                    validation=validation,
                    stop_reason="validation_failed",
                )
                validate_rule_outcome(outcome)
                outcomes.append(outcome)
                provenance.append(
                    PassProvenance(
                        pass_index=pass_index,
                        candidate_rules_checked=tuple(checked),
                        selected_rule_id=rule.rule_id,
                        selection_priority=rule.priority,
                        stopped_after_change=False,
                    )
                )
                result = ResearchHealerResult(
                    input_source=source,
                    output_source=current,
                    input_hash=input_hash,
                    output_hash=sha256_text(current),
                    final_status="validation_failed",
                    rule_outcomes=tuple(outcomes),
                    provenance=tuple(provenance),
                    real_model_calls=0,
                    protected_snapshot=protected,
                    notes=tuple(notes + ["reparse_required_after_change"]),
                )
                validate_research_result(result)
                return result

            if did_change:
                current = new_source
                pass_changed = True
                changed_any = True
                stopped_after_change = True
                selected_id = rule.rule_id
                selected_priority = rule.priority
                outcome = RuleOutcome(
                    rule_id=rule.rule_id,
                    layer=rule.layer,
                    priority=rule.priority,
                    applicable=True,
                    triggered=True,
                    changed=True,
                    guard_results=dict(guards),
                    reason=apply_reason,
                    before_hash=before_hash,
                    after_hash=after_hash,
                    validation=validation,
                    stop_reason="changed_stop_pass",
                )
                validate_rule_outcome(outcome)
                outcomes.append(outcome)
                break

            outcome = RuleOutcome(
                rule_id=rule.rule_id,
                layer=rule.layer,
                priority=rule.priority,
                applicable=True,
                triggered=True,
                changed=False,
                guard_results=dict(guards),
                reason=apply_reason,
                before_hash=before_hash,
                after_hash=before_hash,
                validation=validation,
                stop_reason="no_change",
            )
            validate_rule_outcome(outcome)
            outcomes.append(outcome)

        provenance.append(
            PassProvenance(
                pass_index=pass_index,
                candidate_rules_checked=tuple(checked),
                selected_rule_id=selected_id,
                selection_priority=selected_priority,
                stopped_after_change=stopped_after_change,
            )
        )
        if pass_changed:
            # Policy: stop after first changed rule (one change per pass, then halt).
            notes.append("stopped_after_first_changed_rule")
            break
        if selected_id is None and not any(o.triggered for o in outcomes):
            notes.append("no_candidate_selected")

    result = ResearchHealerResult(
        input_source=source,
        output_source=current,
        input_hash=input_hash,
        output_hash=sha256_text(current),
        final_status="changed" if changed_any else "no_op",
        rule_outcomes=tuple(outcomes),
        provenance=tuple(provenance),
        real_model_calls=0,
        protected_snapshot=protected,
        notes=tuple(notes),
    )
    validate_research_result(result)
    return result


class MathHealerRunner:
    """Allowlist-facing research runner entry point (H1).

    Legacy Ab2g→Ab3 derivation remains on ``derive_ab3`` in this package's
    ``math_healer_runner`` module and is intentionally not invoked here.
    """

    allowlist: tuple[str, ...] = RULE_ALLOWLIST

    def __init__(
        self,
        *,
        allowlist: Sequence[str] | None = None,
        registry: Mapping[str, _RegisteredRule] | None = None,
        max_passes: int = 1,
    ) -> None:
        self.allowlist = tuple(RULE_ALLOWLIST if allowlist is None else allowlist)
        self.registry = registry
        self.max_passes = max_passes

    def run(
        self,
        source: str,
        *,
        context: Mapping[str, Any] | None = None,
        protected_snapshot: Mapping[str, Any] | None = None,
    ) -> ResearchHealerResult:
        return run_research_healer(
            source,
            context=context,
            allowlist=self.allowlist,
            registry=self.registry,
            protected_snapshot=protected_snapshot,
            max_passes=self.max_passes,
        )


def load_regression_manifest(path: str | Path) -> dict[str, Any]:
    """Load cumulative regression manifest JSON."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise RuleProtocolError("manifest must be a JSON object")
    required = ("manifest_id", "schema_version", "cases")
    missing = [k for k in required if k not in data]
    if missing:
        raise RuleProtocolError(f"manifest missing keys: {missing}")
    if not isinstance(data["cases"], list):
        raise RuleProtocolError("manifest.cases must be a list")
    return data


def iter_manifest_cases(manifest: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Return cases in stable order; used by parametric tests for accumulation."""
    cases = list(manifest["cases"])
    case_fields = (
        "case_id",
        "source_artifact",
        "expected_applicable_rules",
        "expected_triggered_rules",
        "expected_changed_rules",
        "expected_final_status",
        "protected_fields",
    )
    for case in cases:
        missing = [k for k in case_fields if k not in case]
        if missing:
            raise RuleProtocolError(
                f"case {case.get('case_id')!r} missing fields: {missing}"
            )
    return cases
