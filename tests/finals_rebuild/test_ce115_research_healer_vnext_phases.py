"""Deterministic synthetic coverage for the frozen vNext runner phases."""

from __future__ import annotations

import ast

from agent_tools.finals_rebuild.ce115_research_healer_runner import (
    _RegisteredRule,
    run_research_healer,
)


def _replacement_rule(rule_id: str, layer: str, priority: int, old: str, new: str):
    def is_applicable(source, context):
        return True, {"synthetic": True}, "synthetic"

    def is_triggered(source, context):
        return old in source, "marker present" if old in source else "marker absent"

    def apply(source, context):
        changed = source.replace(old, new, 1)
        return changed, {"synthetic": True}, "replace marker"

    return _RegisteredRule(
        rule_id=rule_id,
        layer=layer,
        priority=priority,
        is_applicable=is_applicable,
        is_triggered=is_triggered,
        apply=apply,
    )


def test_two_l1_errors_repair_sequentially_across_passes():
    source = "x = (1\ny = (2\n"
    registry = {
        "L1_SYNTH_FIRST": _replacement_rule(
            "L1_SYNTH_FIRST", "L1", 10, "x = (1\n", "x = (1)\n"
        ),
        "L1_SYNTH_SECOND": _replacement_rule(
            "L1_SYNTH_SECOND", "L1", 20, "y = (2\n", "y = (2)\n"
        ),
    }
    result = run_research_healer(
        source,
        allowlist=tuple(registry),
        registry=registry,
        max_passes=3,
    )
    ast.parse(result.output_source)
    assert result.final_status == "changed"
    assert [p.selected_rule_id for p in result.provenance if p.changed] == [
        "L1_SYNTH_FIRST",
        "L1_SYNTH_SECOND",
    ]
    assert [p.validation["phase"] for p in result.provenance[:2]] == [
        "Phase_A",
        "Phase_A",
    ]


def test_l1_to_l2_phase_transition_across_passes():
    source = "x = (1\nFLAG = 0\n"
    registry = {
        "L1_SYNTH_CLOSE": _replacement_rule(
            "L1_SYNTH_CLOSE", "L1", 10, "x = (1\n", "x = (1)\n"
        ),
        "L2_SYNTH_REWRITE": _replacement_rule(
            "L2_SYNTH_REWRITE", "L2", 20, "FLAG = 0", "FLAG = 1"
        ),
    }
    result = run_research_healer(
        source,
        allowlist=tuple(registry),
        registry=registry,
        max_passes=3,
    )
    assert result.final_status == "changed"
    assert [p.selected_rule_id for p in result.provenance if p.changed] == [
        "L1_SYNTH_CLOSE",
        "L2_SYNTH_REWRITE",
    ]
    assert [p.validation["phase"] for p in result.provenance[:2]] == [
        "Phase_A",
        "Phase_B",
    ]
    assert "FLAG = 1" in result.output_source
