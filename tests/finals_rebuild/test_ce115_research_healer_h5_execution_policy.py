"""H5: freeze multi-rule execution policy and complete provenance."""

from __future__ import annotations

import json
from pathlib import Path

from agent_tools.finals_rebuild.ce115_research_healer_protocol import (
    DEFAULT_MAX_PASSES,
    FROZEN_EXECUTION_POLICY,
    PROVENANCE_FIELDS,
    assert_provenance_field_coverage,
    provenance_to_dict,
    research_result_to_dict,
    sha256_text,
)
from agent_tools.finals_rebuild.ce115_research_healer_runner import (
    MathHealerRunner,
    RULE_ALLOWLIST,
    _RegisteredRule,
    iter_manifest_cases,
    load_regression_manifest,
    run_research_healer,
    select_allowlisted_rules,
)
from agent_tools.finals_rebuild.math_boundary_pilot import (
    classify_response,
    load_pilot_tasks,
)

ROOT = Path(__file__).resolve().parents[2]
FIX = ROOT / "tests/finals_rebuild/fixtures/ce115_research_healer"
MANIFEST_PATH = FIX / "regression_manifest.json"
TASK_MANIFEST = ROOT / "tests/finals_rebuild/fixtures/math_generation_tasks_ce115_pilot.jsonl"
L2 = "L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP"


def _reg(
    rule_id: str,
    priority: int,
    *,
    applicable: bool = True,
    triggered: bool = True,
    mutate: bool = False,
    marker: str = "# healed\n",
) -> _RegisteredRule:
    def is_applicable(source: str, context):
        return applicable, {"ok": True}, "applicable" if applicable else "skip"

    def is_triggered(source: str, context):
        if mutate and marker in source:
            return False, "already healed"
        return triggered, "triggered" if triggered else "not triggered"

    def apply(source: str, context):
        if mutate and marker not in source:
            return source + marker, {"mutated": True}, "mutated"
        return source, {"mutated": False}, "identity"

    return _RegisteredRule(
        rule_id=rule_id,
        layer="META",
        priority=priority,
        is_applicable=is_applicable,
        is_triggered=is_triggered,
        apply=apply,
    )


def test_frozen_execution_policy_constants():
    assert DEFAULT_MAX_PASSES == 1
    assert FROZEN_EXECUTION_POLICY["allowlist_only"] is True
    assert FROZEN_EXECUTION_POLICY["fixed_priority"] is True
    assert FROZEN_EXECUTION_POLICY["one_change_per_pass"] is True
    assert FROZEN_EXECUTION_POLICY["stop_pass_after_first_changed"] is True
    assert FROZEN_EXECUTION_POLICY["fail_closed_on_max_passes_exceeded"] is True
    assert FROZEN_EXECUTION_POLICY["rollback_on_max_passes_exceeded"] is True
    assert FROZEN_EXECUTION_POLICY["max_passes_semantics"] == "transactional_rollback"
    assert FROZEN_EXECUTION_POLICY["consumer_may_use_output_when_max_passes_exceeded"] is False
    assert FROZEN_EXECUTION_POLICY["repair_attempt_requires_changed"] is True
    assert FROZEN_EXECUTION_POLICY["forbid_legacy_pipelines"] is True
    assert set(PROVENANCE_FIELDS) == {
        "pass_index",
        "candidate_rules_checked",
        "selected_rule_id",
        "selection_priority",
        "applicable",
        "triggered",
        "changed",
        "guard_results",
        "before_hash",
        "after_hash",
        "validation",
        "stop_reason",
        "stopped_after_change",
        "final_status",
    }


def test_single_rule_changed_stops_pass():
    source = "x = 1\n"
    registry = {
        "first_change": _reg("first_change", 10, mutate=True, marker="# A\n"),
        "second_change": _reg("second_change", 20, mutate=True, marker="# B\n"),
    }
    result = run_research_healer(
        source,
        allowlist=("first_change", "second_change"),
        registry=registry,
        max_passes=1,
    )
    assert result.final_status == "max_passes_exceeded" or result.final_status == "changed"
    # With max_passes=1 and second rule still wanting to change ⇒ fail closed.
    assert result.final_status == "max_passes_exceeded"
    assert result.max_passes == 1
    assert result.rolled_back is True
    assert result.consumer_may_use_output is False
    assert result.output_source == source
    changed = [o for o in result.rule_outcomes if o.changed]
    assert len(changed) == 1
    assert changed[0].rule_id == "first_change"
    assert "second_change" not in [o.rule_id for o in result.rule_outcomes if o.changed]
    assert result.provenance[0].stopped_after_change is True
    assert result.provenance[0].selected_rule_id == "first_change"
    assert result.real_model_calls == 0


def test_noop_rule_continues_to_next():
    registry = {
        "noop_high": _reg("noop_high", 10, triggered=False, mutate=False),
        "change_low": _reg("change_low", 20, mutate=True, marker="# C\n"),
    }
    result = run_research_healer(
        "x = 1\n",
        allowlist=("noop_high", "change_low"),
        registry=registry,
        max_passes=1,
    )
    assert result.final_status == "changed"
    assert [o.rule_id for o in result.rule_outcomes] == ["noop_high", "change_low"]
    assert result.rule_outcomes[0].triggered is False
    assert result.rule_outcomes[0].changed is False
    assert result.rule_outcomes[0].validation.get("repair_attempted") is False
    assert result.rule_outcomes[1].changed is True
    assert result.output_source.endswith("# C\n")


def test_fixed_priority_ignores_registry_insertion_order():
    # Insert lower priority first in registry and allowlist; higher priority must win.
    registry = {
        "late_low": _reg("late_low", 50, mutate=True, marker="# LOW\n"),
        "early_high": _reg("early_high", 5, mutate=True, marker="# HIGH\n"),
    }
    ordered = select_allowlisted_rules(
        allowlist=("late_low", "early_high"),
        registry=registry,
    )
    assert [r.rule_id for r in ordered] == ["early_high", "late_low"]
    result = run_research_healer(
        "x = 1\n",
        allowlist=("late_low", "early_high"),
        registry=registry,
        max_passes=2,
    )
    assert result.provenance[0].selected_rule_id == "early_high"
    assert result.provenance[0].selection_priority == 5
    assert "# HIGH\n" in result.output_source
    # With max_passes=2 the lower-priority rule may apply on pass 1.
    assert result.final_status == "changed"
    assert result.output_source.endswith("# LOW\n")
    assert [p.selected_rule_id for p in result.provenance if p.changed] == [
        "early_high",
        "late_low",
    ]


def test_at_most_one_changed_rule_per_pass():
    registry = {
        "a": _reg("a", 1, mutate=True, marker="#1\n"),
        "b": _reg("b", 2, mutate=True, marker="#2\n"),
        "c": _reg("c", 3, mutate=True, marker="#3\n"),
    }
    result = run_research_healer(
        "x = 1\n",
        allowlist=("a", "b", "c"),
        registry=registry,
        max_passes=2,
    )
    # Pass 0: only a changes; pass 1: only b changes (c may remain ⇒ exceeded or applied).
    by_pass: dict[int, list[str]] = {}
    pass_idx = 0
    for o in result.rule_outcomes:
        if o.changed:
            by_pass.setdefault(pass_idx, []).append(o.rule_id)
            # After a changed outcome, next outcomes belong to later passes conceptually;
            # count changed per provenance pass instead.
    for prov in result.provenance:
        changed_in_pass = [
            o.rule_id
            for o in result.rule_outcomes
            if o.changed and o.rule_id == prov.selected_rule_id and prov.changed
        ]
        assert len(changed_in_pass) <= 1
        if prov.changed:
            assert prov.stopped_after_change is True


def test_change_requires_reparse_and_evaluate():
    case = next(
        c
        for c in iter_manifest_cases(load_regression_manifest(MANIFEST_PATH))
        if c["case_id"] == "fail_radical_ab1_l2"
    )
    source = (FIX / case["source_artifact"]).read_text(encoding="utf-8")
    frozen = json.loads((FIX / case["frozen_artifact"]).read_text(encoding="utf-8"))
    task = {
        t["task_id"]: t
        for t in load_pilot_tasks(TASK_MANIFEST)
    }["ce115_calc_radical_simplification_l1"]
    result = MathHealerRunner(max_passes=1).run(
        source,
        context={"frozen": frozen, "task": task},
    )
    assert result.final_status == "changed"
    changed = next(o for o in result.rule_outcomes if o.changed)
    assert changed.validation.get("ast_parse_success") is True
    assert changed.validation.get("reparsed_after_change") is True
    assert changed.validation.get("evaluator_rerun") is True
    assert changed.validation.get("evaluator_outcome") == "passed"
    assert changed.validation.get("repair_attempted") is True
    assert result.provenance[0].validation.get("evaluator_outcome") == "passed"


def test_max_passes_fail_closed():
    source = "x = 1\n"
    registry = {
        "r1": _reg("r1", 10, mutate=True, marker="#1\n"),
        "r2": _reg("r2", 20, mutate=True, marker="#2\n"),
    }
    result = run_research_healer(
        source,
        allowlist=("r1", "r2"),
        registry=registry,
        max_passes=1,
    )
    assert result.final_status == "max_passes_exceeded"
    assert result.max_passes == 1
    assert result.provenance[-1].final_status == "max_passes_exceeded"
    assert any("fail_closed_max_passes_exceeded" in n for n in result.notes)
    assert any("transaction_rollback_to_input" in n for n in result.notes)
    # Option A: transactional rollback — no partial output for consumers.
    assert result.rolled_back is True
    assert result.consumer_may_use_output is False
    assert result.output_source == source
    assert result.output_hash == result.input_hash
    assert FROZEN_EXECUTION_POLICY["max_passes_semantics"] == "transactional_rollback"


def test_empty_allowlist_all_noop():
    result = run_research_healer("a = 1\n", allowlist=(), max_passes=3)
    assert result.final_status == "no_op"
    assert result.input_hash == result.output_hash
    assert result.rule_outcomes == ()
    assert result.real_model_calls == 0
    assert result.max_passes == 3
    prov = result.provenance[0]
    assert_provenance_field_coverage(provenance_to_dict(prov))
    assert prov.changed is False
    assert prov.stopped_after_change is False
    assert prov.final_status == "no_op"
    assert prov.stop_reason == "allowlist_empty"


def test_h3_l2_repair_to_pass_not_regressed():
    case = next(
        c
        for c in iter_manifest_cases(load_regression_manifest(MANIFEST_PATH))
        if c["case_id"] == "fail_radical_ab1_l2"
    )
    source = (FIX / case["source_artifact"]).read_text(encoding="utf-8")
    frozen = json.loads((FIX / case["frozen_artifact"]).read_text(encoding="utf-8"))
    task = {
        t["task_id"]: t
        for t in load_pilot_tasks(TASK_MANIFEST)
    }["ce115_calc_radical_simplification_l1"]
    before, _, _ = classify_response(source, {"oracle_payload": frozen}, task)
    assert before == "schema_failure"
    result = run_research_healer(
        source,
        context={"frozen": frozen, "task": task},
        max_passes=DEFAULT_MAX_PASSES,
    )
    assert L2 in RULE_ALLOWLIST
    assert RULE_ALLOWLIST == (L2,)
    assert result.final_status == "changed"
    assert result.real_model_calls == 0
    after, _, _ = classify_response(
        result.output_source, {"oracle_payload": frozen}, task
    )
    assert after == "passed"
    # Idempotent second run.
    second = run_research_healer(
        result.output_source,
        context={"frozen": frozen, "task": task},
    )
    assert second.final_status == "no_op"
    assert second.output_source == result.output_source


def test_cumulative_manifest_still_passes():
    manifest = load_regression_manifest(MANIFEST_PATH)
    for case in iter_manifest_cases(manifest):
        source = (FIX / case["source_artifact"]).read_text(encoding="utf-8")
        frozen = json.loads((FIX / case["frozen_artifact"]).read_text(encoding="utf-8"))
        result = MathHealerRunner().run(source, context={"frozen": frozen})
        assert result.final_status == case["expected_final_status"]
        assert result.real_model_calls == 0
        assert [
            o.rule_id for o in result.rule_outcomes if o.applicable
        ] == case["expected_applicable_rules"]
        assert [
            o.rule_id for o in result.rule_outcomes if o.triggered
        ] == case["expected_triggered_rules"]
        assert [
            o.rule_id for o in result.rule_outcomes if o.changed
        ] == case["expected_changed_rules"]
        for prov in result.provenance:
            assert_provenance_field_coverage(provenance_to_dict(prov))


def test_no_repair_claim_without_change():
    registry = {
        "trig_noop": _reg("trig_noop", 1, triggered=True, mutate=False),
    }
    result = run_research_healer(
        "x = 1\n",
        allowlist=("trig_noop",),
        registry=registry,
        max_passes=1,
    )
    assert result.final_status == "no_op"
    outcome = result.rule_outcomes[0]
    assert outcome.triggered is True
    assert outcome.changed is False
    assert outcome.validation.get("repair_attempted") is False
    payload = research_result_to_dict(result)
    assert payload["max_passes"] == 1
    assert payload["execution_policy"]["policy_id"] == FROZEN_EXECUTION_POLICY["policy_id"]
