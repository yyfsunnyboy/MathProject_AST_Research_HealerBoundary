"""Research-only allowlist Healer runner (H1+) / frozen multi-rule policy (H5).

Frozen execution policy (H5):
- allowlist only
- fixed priority (ascending)
- one change per pass; stop that pass after the first changed rule
- after any change: re-parse / re-validate / re-evaluate (when task present)
- never claim repair_attempted unless changed=True
- max_passes is mandatory and explicit; exceed ⇒ fail closed
- must not call legacy Regex / AST / AntiDuplication / UnifiedCleanup pipelines

H3 registers L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP only; H5 adds no new repair rules.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Mapping, Protocol, Sequence

from agent_tools.finals_rebuild.ce115_research_healer_protocol import (
    DEFAULT_MAX_PASSES,
    FROZEN_EXECUTION_POLICY,
    PassProvenance,
    ResearchHealerResult,
    RuleOutcome,
    RuleProtocolError,
    make_parse_validation,
    sha256_text,
    validate_research_result,
    validate_rule_outcome,
)
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


def _maybe_reevaluate(source: str, context: Mapping[str, Any]) -> dict[str, Any]:
    """Re-run existing evaluator when task+frozen are present; never mutate evaluator."""
    task = context.get("task")
    frozen = context.get("frozen")
    if not isinstance(task, Mapping) or not isinstance(frozen, Mapping):
        return {"evaluator_rerun": False}
    from agent_tools.finals_rebuild.math_boundary_pilot import classify_response

    outcome, _code, details = classify_response(
        source,
        {"oracle_payload": dict(frozen)},
        dict(task),
    )
    return {
        "evaluator_rerun": True,
        "evaluator_outcome": outcome,
        "evaluator_details_keys": sorted(details.keys()),
    }


def _rule_would_change(
    source: str,
    rule: _RegisteredRule,
    context: Mapping[str, Any],
) -> bool:
    applicable, _guards, _reason = rule.is_applicable(source, context)
    if not applicable:
        return False
    triggered, _trig = rule.is_triggered(source, context)
    if not triggered:
        return False
    new_source, _extra, _apply_reason = rule.apply(source, context)
    return new_source != source


def _any_rule_would_change(
    source: str,
    rules: Sequence[_RegisteredRule],
    context: Mapping[str, Any],
) -> bool:
    return any(_rule_would_change(source, rule, context) for rule in rules)


def _build_pass_provenance(
    *,
    pass_index: int,
    checked: Sequence[str],
    selected_id: str | None,
    selected_priority: int | None,
    selected_outcome: RuleOutcome | None,
    before_hash: str,
    after_hash: str,
    validation: Mapping[str, Any],
    stopped_after_change: bool,
    stop_reason: str | None,
    final_status: str,
) -> PassProvenance:
    if selected_outcome is not None:
        return PassProvenance(
            pass_index=pass_index,
            candidate_rules_checked=tuple(checked),
            selected_rule_id=selected_id,
            selection_priority=selected_priority,
            applicable=selected_outcome.applicable,
            triggered=selected_outcome.triggered,
            changed=selected_outcome.changed,
            guard_results=dict(selected_outcome.guard_results),
            before_hash=before_hash,
            after_hash=after_hash,
            validation=dict(validation),
            stop_reason=stop_reason if stop_reason is not None else selected_outcome.stop_reason,
            stopped_after_change=stopped_after_change,
            final_status=final_status,
        )
    return PassProvenance(
        pass_index=pass_index,
        candidate_rules_checked=tuple(checked),
        selected_rule_id=None,
        selection_priority=None,
        applicable=False,
        triggered=False,
        changed=False,
        guard_results={},
        before_hash=before_hash,
        after_hash=after_hash,
        validation=dict(validation),
        stop_reason=stop_reason,
        stopped_after_change=False,
        final_status=final_status,
    )


def _finish(
    *,
    source: str,
    current: str,
    input_hash: str,
    final_status: str,
    outcomes: list[RuleOutcome],
    provenance: list[PassProvenance],
    notes: list[str],
    protected: Mapping[str, Any],
    max_passes: int,
) -> ResearchHealerResult:
    # Stamp last provenance final_status to match run result.
    if provenance:
        last = provenance[-1]
        if last.final_status != final_status:
            provenance[-1] = PassProvenance(
                pass_index=last.pass_index,
                candidate_rules_checked=last.candidate_rules_checked,
                selected_rule_id=last.selected_rule_id,
                selection_priority=last.selection_priority,
                applicable=last.applicable,
                triggered=last.triggered,
                changed=last.changed,
                guard_results=dict(last.guard_results),
                before_hash=last.before_hash,
                after_hash=last.after_hash,
                validation=dict(last.validation),
                stop_reason=last.stop_reason,
                stopped_after_change=last.stopped_after_change,
                final_status=final_status,
            )
    result = ResearchHealerResult(
        input_source=source,
        output_source=current,
        input_hash=input_hash,
        output_hash=sha256_text(current),
        final_status=final_status,
        rule_outcomes=tuple(outcomes),
        provenance=tuple(provenance),
        real_model_calls=0,
        protected_snapshot=dict(protected),
        notes=tuple(notes),
        max_passes=max_passes,
        execution_policy=dict(FROZEN_EXECUTION_POLICY),
    )
    validate_research_result(result)
    return result


def run_research_healer(
    source: str,
    *,
    context: Mapping[str, Any] | None = None,
    allowlist: Sequence[str] = RULE_ALLOWLIST,
    registry: Mapping[str, _RegisteredRule] | None = None,
    protected_snapshot: Mapping[str, Any] | None = None,
    max_passes: int = DEFAULT_MAX_PASSES,
) -> ResearchHealerResult:
    """Run the research allowlist healer under the frozen H5 execution policy."""
    _assert_no_legacy_pipeline()
    if not isinstance(source, str):
        raise RuleProtocolError("source must be a str")
    if not isinstance(max_passes, int) or max_passes < 1:
        raise RuleProtocolError("max_passes must be an explicit int >= 1")

    ctx: dict[str, Any] = dict(context or {})
    protected = dict(protected_snapshot or {})
    input_hash = sha256_text(source)
    current = source
    outcomes: list[RuleOutcome] = []
    provenance: list[PassProvenance] = []
    notes: list[str] = [f"max_passes={max_passes}"]

    rules = select_allowlisted_rules(allowlist=allowlist, registry=registry)

    if not rules:
        empty_hash = sha256_text(current)
        empty_validation = make_parse_validation(current)
        provenance.append(
            _build_pass_provenance(
                pass_index=0,
                checked=(),
                selected_id=None,
                selected_priority=None,
                selected_outcome=None,
                before_hash=empty_hash,
                after_hash=empty_hash,
                validation=empty_validation,
                stopped_after_change=False,
                stop_reason="allowlist_empty" if not allowlist else "no_candidate_selected",
                final_status="no_op",
            )
        )
        notes.append("allowlist_empty" if not allowlist else "no_registered_allowlist_rules")
        return _finish(
            source=source,
            current=current,
            input_hash=input_hash,
            final_status="no_op",
            outcomes=outcomes,
            provenance=provenance,
            notes=notes,
            protected=protected,
            max_passes=max_passes,
        )

    changed_any = False
    for pass_index in range(max_passes):
        before = current
        before_hash = sha256_text(before)
        checked: list[str] = []
        selected_id: str | None = None
        selected_priority: int | None = None
        selected_outcome: RuleOutcome | None = None
        stopped_after_change = False
        pass_changed = False
        pass_stop_reason: str | None = "no_candidate_selected"
        pass_validation: dict[str, Any] = make_parse_validation(before)

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
                    validation={
                        **make_parse_validation(before),
                        "repair_attempted": False,
                    },
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
                    validation={
                        **make_parse_validation(before),
                        "repair_attempted": False,
                    },
                    stop_reason="not_triggered",
                )
                validate_rule_outcome(outcome)
                outcomes.append(outcome)
                continue

            # Triggered ⇒ attempt apply. repair_attempted only if source changes.
            new_source, extra_validation, apply_reason = rule.apply(before, ctx)
            after_hash = sha256_text(new_source)
            validation = make_parse_validation(new_source)
            validation.update(dict(extra_validation))
            did_change = new_source != before
            validation["repair_attempted"] = did_change
            # Always re-parse after a potential change; re-evaluate when task present.
            if did_change:
                validation.update(_maybe_reevaluate(new_source, ctx))
                validation["reparsed_after_change"] = True
            else:
                validation["reparsed_after_change"] = False

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
                    validation={**validation, "repair_attempted": False},
                    stop_reason="validation_failed",
                )
                validate_rule_outcome(outcome)
                outcomes.append(outcome)
                selected_outcome = outcome
                selected_id = rule.rule_id
                selected_priority = rule.priority
                pass_stop_reason = "validation_failed"
                pass_validation = dict(outcome.validation)
                provenance.append(
                    _build_pass_provenance(
                        pass_index=pass_index,
                        checked=checked,
                        selected_id=selected_id,
                        selected_priority=selected_priority,
                        selected_outcome=selected_outcome,
                        before_hash=before_hash,
                        after_hash=before_hash,
                        validation=pass_validation,
                        stopped_after_change=False,
                        stop_reason=pass_stop_reason,
                        final_status="validation_failed",
                    )
                )
                notes.append("fail_closed_validation")
                return _finish(
                    source=source,
                    current=current,
                    input_hash=input_hash,
                    final_status="validation_failed",
                    outcomes=outcomes,
                    provenance=provenance,
                    notes=notes,
                    protected=protected,
                    max_passes=max_passes,
                )

            if did_change:
                current = new_source
                pass_changed = True
                changed_any = True
                stopped_after_change = True
                selected_id = rule.rule_id
                selected_priority = rule.priority
                pass_stop_reason = "changed_stop_pass"
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
                selected_outcome = outcome
                pass_validation = dict(validation)
                # One change per pass — stop checking further rules this pass.
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
            # Triggered but identity apply: keep scanning lower-priority rules.
            pass_stop_reason = "stable_no_further_change"

        after_hash = sha256_text(current)
        if not pass_changed and selected_outcome is None:
            # No triggered selection; keep last checked state in provenance.
            pass_stop_reason = (
                "no_candidate_selected" if checked else "allowlist_empty"
            )
            pass_validation = make_parse_validation(current)

        provisional_status = "changed" if changed_any else "no_op"
        provenance.append(
            _build_pass_provenance(
                pass_index=pass_index,
                checked=checked,
                selected_id=selected_id,
                selected_priority=selected_priority,
                selected_outcome=selected_outcome,
                before_hash=before_hash,
                after_hash=after_hash,
                validation=pass_validation,
                stopped_after_change=stopped_after_change,
                stop_reason=pass_stop_reason,
                final_status=provisional_status,
            )
        )

        if pass_changed:
            notes.append(f"pass_{pass_index}_stopped_after_first_changed_rule")
            # Continue to next pass only while budget remains.
            if pass_index + 1 >= max_passes:
                if _any_rule_would_change(current, rules, ctx):
                    notes.append("fail_closed_max_passes_exceeded")
                    return _finish(
                        source=source,
                        current=current,
                        input_hash=input_hash,
                        final_status="max_passes_exceeded",
                        outcomes=outcomes,
                        provenance=provenance,
                        notes=notes,
                        protected=protected,
                        max_passes=max_passes,
                    )
                # Budget exhausted but stable — success if we changed, else no_op.
                return _finish(
                    source=source,
                    current=current,
                    input_hash=input_hash,
                    final_status="changed" if changed_any else "no_op",
                    outcomes=outcomes,
                    provenance=provenance,
                    notes=notes,
                    protected=protected,
                    max_passes=max_passes,
                )
            # More passes available: re-scan on updated source next iteration.
            continue

        # No change this pass ⇒ stable; stop without consuming further passes.
        notes.append(f"pass_{pass_index}_stable_no_change")
        return _finish(
            source=source,
            current=current,
            input_hash=input_hash,
            final_status="changed" if changed_any else "no_op",
            outcomes=outcomes,
            provenance=provenance,
            notes=notes,
            protected=protected,
            max_passes=max_passes,
        )

    # All passes consumed without early return.
    if changed_any and _any_rule_would_change(current, rules, ctx):
        notes.append("fail_closed_max_passes_exceeded")
        return _finish(
            source=source,
            current=current,
            input_hash=input_hash,
            final_status="max_passes_exceeded",
            outcomes=outcomes,
            provenance=provenance,
            notes=notes,
            protected=protected,
            max_passes=max_passes,
        )
    return _finish(
        source=source,
        current=current,
        input_hash=input_hash,
        final_status="changed" if changed_any else "no_op",
        outcomes=outcomes,
        provenance=provenance,
        notes=notes,
        protected=protected,
        max_passes=max_passes,
    )


class MathHealerRunner:
    """Allowlist-facing research runner entry point (H5 frozen policy)."""

    allowlist: tuple[str, ...] = RULE_ALLOWLIST

    def __init__(
        self,
        *,
        allowlist: Sequence[str] | None = None,
        registry: Mapping[str, _RegisteredRule] | None = None,
        max_passes: int = DEFAULT_MAX_PASSES,
    ) -> None:
        if not isinstance(max_passes, int) or max_passes < 1:
            raise RuleProtocolError("max_passes must be an explicit int >= 1")
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
