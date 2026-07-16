"""H1+H2 skeleton tests (protocol, empty-allowlist policy, cumulative manifest).

H3 registers a real L2 rule on the default allowlist; empty-allowlist behaviour
is still covered by explicitly passing ``allowlist=()``.
"""

from __future__ import annotations

import copy
import hashlib
import importlib
import inspect
import json
from pathlib import Path

import pytest

from agent_tools.finals_rebuild import math_healer_runner as mhr
from agent_tools.finals_rebuild.ce115_research_healer_protocol import (
    PROVENANCE_FIELDS,
    RULE_PROTOCOL_FIELDS,
    RuleOutcome,
    RuleProtocolError,
    assert_provenance_field_coverage,
    assert_protocol_field_coverage,
    make_parse_validation,
    research_result_to_dict,
    sha256_text,
    validate_provenance,
    validate_rule_outcome,
)
from agent_tools.finals_rebuild.ce115_research_healer_runner import (
    FORBIDDEN_LEGACY_IMPORTS,
    RULE_ALLOWLIST,
    RULE_REGISTRY,
    MathHealerRunner,
    _RegisteredRule,
    iter_manifest_cases,
    load_regression_manifest,
    run_research_healer,
    select_allowlisted_rules,
)

ROOT = Path(__file__).resolve().parents[2]
FIX = ROOT / "tests/finals_rebuild/fixtures/ce115_research_healer"
MANIFEST_PATH = FIX / "regression_manifest.json"


def _load_manifest() -> dict:
    return load_regression_manifest(MANIFEST_PATH)


def _case_ids() -> list[str]:
    return [c["case_id"] for c in iter_manifest_cases(_load_manifest())]


def _read_case(case: dict) -> tuple[str, dict, dict]:
    source = (FIX / case["source_artifact"]).read_text(encoding="utf-8")
    frozen = json.loads((FIX / case["frozen_artifact"]).read_text(encoding="utf-8"))
    meta_path = case.get("meta_artifact")
    meta = {}
    if meta_path:
        meta = json.loads((FIX / meta_path).read_text(encoding="utf-8"))
    return source, frozen, meta


def _protected_snapshot(case: dict, frozen: dict, source: str) -> dict:
    snap: dict = {"candidate_source": source, "frozen": copy.deepcopy(frozen)}
    for field in case["protected_fields"]:
        if field == "candidate_source":
            continue
        if field.startswith("frozen."):
            key = field.split(".", 1)[1]
            snap[field] = copy.deepcopy(frozen[key])
    return snap


def _assert_protected_unchanged(case: dict, before: dict, after_frozen: dict, after_source: str) -> None:
    for field in case["protected_fields"]:
        if field == "candidate_source":
            assert after_source == before["candidate_source"]
            continue
        if field.startswith("frozen."):
            key = field.split(".", 1)[1]
            assert after_frozen[key] == before[field]


# ---------------------------------------------------------------------------
# Protocol
# ---------------------------------------------------------------------------


def test_rule_protocol_required_fields():
    assert set(RULE_PROTOCOL_FIELDS) == {
        "rule_id",
        "layer",
        "priority",
        "applicable",
        "triggered",
        "changed",
        "guard_results",
        "reason",
        "before_hash",
        "after_hash",
        "validation",
        "stop_reason",
    }


def test_provenance_required_fields():
    assert set(PROVENANCE_FIELDS) == {
        "pass_index",
        "candidate_rules_checked",
        "selected_rule_id",
        "selection_priority",
        "stopped_after_change",
    }


def test_applicable_triggered_changed_semantics_distinguishable():
    h = sha256_text("x = 1\n")
    h2 = sha256_text("x = 2\n")

    applicable_only = RuleOutcome(
        rule_id="probe_applicable_only",
        layer="L2",
        priority=10,
        applicable=True,
        triggered=False,
        changed=False,
        guard_results={"pattern_seen": True},
        reason="guards pass but trigger gate closed",
        before_hash=h,
        after_hash=h,
        validation=make_parse_validation("x = 1\n"),
        stop_reason="not_triggered",
    )
    triggered_no_change = RuleOutcome(
        rule_id="probe_triggered_noop",
        layer="L2",
        priority=20,
        applicable=True,
        triggered=True,
        changed=False,
        guard_results={"pattern_seen": True},
        reason="triggered but apply was identity",
        before_hash=h,
        after_hash=h,
        validation=make_parse_validation("x = 1\n"),
        stop_reason="no_change",
    )
    changed = RuleOutcome(
        rule_id="probe_changed",
        layer="L2",
        priority=30,
        applicable=True,
        triggered=True,
        changed=True,
        guard_results={"pattern_seen": True},
        reason="source mutated",
        before_hash=h,
        after_hash=h2,
        validation=make_parse_validation("x = 2\n"),
        stop_reason="changed_stop_pass",
    )
    validate_rule_outcome(applicable_only)
    validate_rule_outcome(triggered_no_change)
    validate_rule_outcome(changed)

    assert (applicable_only.applicable, applicable_only.triggered, applicable_only.changed) == (
        True,
        False,
        False,
    )
    assert (triggered_no_change.applicable, triggered_no_change.triggered, triggered_no_change.changed) == (
        True,
        True,
        False,
    )
    assert (changed.applicable, changed.triggered, changed.changed) == (True, True, True)

    with pytest.raises(RuleProtocolError):
        validate_rule_outcome(
            RuleOutcome(
                rule_id="bad",
                layer="L1",
                priority=1,
                applicable=False,
                triggered=True,
                changed=False,
                guard_results={},
                reason="invalid ladder",
                before_hash=h,
                after_hash=h,
                validation={},
                stop_reason="not_triggered",
            )
        )


def test_math_healer_runner_exports_allowlist_surface():
    assert mhr.RULE_ALLOWLIST == RULE_ALLOWLIST
    assert "L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP" in RULE_ALLOWLIST
    assert "L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP" in RULE_REGISTRY
    assert callable(mhr.run_research_healer)
    assert mhr.MathHealerRunner is MathHealerRunner


def test_research_runner_does_not_import_legacy_pipelines():
    mod = importlib.import_module("agent_tools.finals_rebuild.ce115_research_healer_runner")
    src = inspect.getsource(mod)
    assert "from core.healers" not in src
    assert "import core.healers" not in src
    for banned in (
        "UnifiedCleanupHealer",
        "ASTHealer",
        "RegexHealer",
        "AntiDuplicationHealer",
    ):
        assert f"import {banned}" not in src
        assert f"{banned}(" not in src
    # Ban list is documentation of what must stay out; runner must still expose it.
    assert FORBIDDEN_LEGACY_IMPORTS
    assert "core.healers.unified_cleanup_healer" in FORBIDDEN_LEGACY_IMPORTS
    assert "UnifiedCleanupHealer" not in vars(mod)

# ---------------------------------------------------------------------------
# Runner policy (empty allowlist)
# ---------------------------------------------------------------------------


def test_empty_allowlist_is_noop():
    source = "def solve():\n    return 1\n"
    result = run_research_healer(source, allowlist=())
    assert result.final_status == "no_op"
    assert result.input_hash == result.output_hash == sha256_text(source)
    assert result.output_source == source
    assert result.rule_outcomes == ()
    assert result.real_model_calls == 0
    assert len(result.provenance) == 1
    prov = result.provenance[0]
    validate_provenance(prov)
    assert prov.pass_index == 0
    assert prov.candidate_rules_checked == ()
    assert prov.selected_rule_id is None
    assert prov.selection_priority is None
    assert prov.stopped_after_change is False


def test_math_healer_runner_class_empty_allowlist():
    runner = MathHealerRunner(allowlist=())
    assert runner.allowlist == ()
    result = runner.run("a = 1\n")
    assert result.final_status == "no_op"
    assert result.real_model_calls == 0


def test_runner_one_change_per_pass_and_priority_with_test_doubles():
    """Policy probe using ephemeral test doubles — not production rules."""

    def _reg(
        rule_id: str,
        priority: int,
        *,
        applicable: bool = True,
        triggered: bool = True,
        mutate: bool = False,
    ) -> _RegisteredRule:
        def is_applicable(source: str, context):
            return applicable, {"ok": True}, "applicable" if applicable else "skip"

        def is_triggered(source: str, context):
            return triggered, "triggered" if triggered else "not triggered"

        def apply(source: str, context):
            if mutate:
                return source + "# healed\n", {"mutated": True}, "mutated"
            return source, {"mutated": False}, "identity"

        return _RegisteredRule(
            rule_id=rule_id,
            layer="L1",
            priority=priority,
            is_applicable=is_applicable,
            is_triggered=is_triggered,
            apply=apply,
        )

    registry = {
        "low_prio_change": _reg("low_prio_change", 20, mutate=True),
        "high_prio_change": _reg("high_prio_change", 10, mutate=True),
        "mid_applicable_only": _reg("mid_applicable_only", 15, triggered=False, mutate=False),
    }
    source = "x = 1\n"
    result = run_research_healer(
        source,
        allowlist=("low_prio_change", "high_prio_change", "mid_applicable_only"),
        registry=registry,
        max_passes=1,
    )
    assert result.final_status == "changed"
    assert result.real_model_calls == 0
    # Fixed priority: priority 10 fires first and stops the pass.
    assert result.provenance[0].selected_rule_id == "high_prio_change"
    assert result.provenance[0].selection_priority == 10
    assert result.provenance[0].stopped_after_change is True
    changed_ids = [o.rule_id for o in result.rule_outcomes if o.changed]
    assert changed_ids == ["high_prio_change"]
    # Lower-priority mutate rule must not also run after first change.
    assert "low_prio_change" not in [o.rule_id for o in result.rule_outcomes]
    assert result.output_source.endswith("# healed\n")
    # Re-parse after change recorded.
    changed_outcome = next(o for o in result.rule_outcomes if o.changed)
    assert changed_outcome.validation["ast_parse_success"] is True
    assert changed_outcome.before_hash != changed_outcome.after_hash


# ---------------------------------------------------------------------------
# Manifest / corpus
# ---------------------------------------------------------------------------


def test_manifest_schema_and_required_case_fields():
    manifest = _load_manifest()
    assert manifest["manifest_id"] == "ce115_research_healer_regression_v1"
    assert manifest["allowlist_expected"] == ["L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP"]
    cases = iter_manifest_cases(manifest)
    assert len(cases) >= 5
    ids = {c["case_id"] for c in cases}
    assert {
        "pass_polydiv_ab2d",
        "pass_radical_ab2d",
        "fail_radical_ab1_l2",
        "noop_multikey_frozen",
        "noop_value_mismatch",
    } <= ids


@pytest.mark.parametrize("case_id", _case_ids())
def test_manifest_case_matches_expected_allowlist_behaviour(case_id: str):
    case = next(c for c in iter_manifest_cases(_load_manifest()) if c["case_id"] == case_id)
    source, frozen, _meta = _read_case(case)
    before_source = source
    before_frozen = copy.deepcopy(frozen)
    protected_before = _protected_snapshot(case, frozen, source)

    result = MathHealerRunner().run(
        source,
        context={"frozen": frozen, "case_id": case_id},
        protected_snapshot=protected_before,
    )

    assert result.final_status == case["expected_final_status"]
    assert result.real_model_calls == 0
    assert [o.rule_id for o in result.rule_outcomes if o.applicable] == case["expected_applicable_rules"]
    assert [o.rule_id for o in result.rule_outcomes if o.triggered] == case["expected_triggered_rules"]
    assert [o.rule_id for o in result.rule_outcomes if o.changed] == case["expected_changed_rules"]
    if case["expected_final_status"] == "no_op":
        assert result.input_hash == result.output_hash == sha256_text(before_source)
        assert result.output_source == before_source
    else:
        assert result.input_hash != result.output_hash
        assert result.output_source != before_source
    _assert_protected_unchanged(case, protected_before, frozen, result.output_source)
    assert frozen == before_frozen

    assert result.provenance
    for prov in result.provenance:
        assert_provenance_field_coverage(research_result_to_dict(result)["provenance"][0])
        validate_provenance(prov)


def test_manifest_parametrized_accumulation():
    """Adding a case to the in-memory manifest must be picked up by iter_manifest_cases."""
    manifest = _load_manifest()
    base_n = len(manifest["cases"])
    extra = {
        "case_id": "synthetic_accumulation_probe",
        "source_artifact": "cases/noop_value_mismatch/candidate.py",
        "frozen_artifact": "cases/noop_value_mismatch/frozen.json",
        "expected_applicable_rules": ["L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP"],
        "expected_triggered_rules": [],
        "expected_changed_rules": [],
        "expected_final_status": "no_op",
        "protected_fields": ["candidate_source", "frozen.x"],
    }
    extended = copy.deepcopy(manifest)
    extended["cases"].append(extra)
    ids = [c["case_id"] for c in iter_manifest_cases(extended)]
    assert len(ids) == base_n + 1
    assert ids[-1] == "synthetic_accumulation_probe"

    for case in iter_manifest_cases(extended):
        source, frozen, _ = _read_case(case)
        result = run_research_healer(source, context={"frozen": frozen})
        assert result.final_status == case["expected_final_status"]
        assert result.real_model_calls == 0
        if case["expected_final_status"] == "no_op":
            assert result.input_hash == result.output_hash


def test_original_pilot_artifacts_untouched():
    """Fixture copies exist; original pilot cell files keep prior byte identity."""
    pilot = ROOT / "docs/experiments/results/ce115_qwen_clean_incremental_pilot_01/cells"
    mapping = {
        "pass_polydiv_ab2d": "qwen3_5_4b__ce115_calc_polynomial_division_l1__ab2d__seed_2026071301",
        "pass_radical_ab2d": "qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d__seed_2026071301",
        "fail_radical_ab1_l2": "qwen3_5_4b__ce115_calc_radical_simplification_l1__ab1__seed_2026071301",
    }
    for case_id, cell_id in mapping.items():
        original = (pilot / cell_id / "extracted_candidate.py").read_bytes()
        fixture = (FIX / "cases" / case_id / "candidate.py").read_bytes()
        assert fixture == original
        # Touch runner must not rewrite original.
        before = hashlib.sha256(original).hexdigest()
        run_research_healer(fixture.decode("utf-8"))
        after = hashlib.sha256((pilot / cell_id / "extracted_candidate.py").read_bytes()).hexdigest()
        assert before == after


def test_select_allowlisted_rules_rejects_unknown():
    with pytest.raises(RuleProtocolError):
        select_allowlisted_rules(allowlist=("does_not_exist",), registry={})


def test_protocol_dict_coverage_helpers():
    h = sha256_text("ok")
    outcome = RuleOutcome(
        rule_id="r",
        layer="META",
        priority=0,
        applicable=False,
        triggered=False,
        changed=False,
        guard_results={},
        reason="n/a",
        before_hash=h,
        after_hash=h,
        validation={},
        stop_reason="not_applicable",
    )
    from agent_tools.finals_rebuild.ce115_research_healer_protocol import rule_outcome_to_dict

    d = rule_outcome_to_dict(outcome)
    assert_protocol_field_coverage(d)
    assert_provenance_field_coverage(
        {
            "pass_index": 0,
            "candidate_rules_checked": [],
            "selected_rule_id": None,
            "selection_priority": None,
            "stopped_after_change": False,
        }
    )
