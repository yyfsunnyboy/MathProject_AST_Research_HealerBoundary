"""H3: L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP — first allowlisted repair-to-pass rule."""

from __future__ import annotations

import ast
import copy
import json
from pathlib import Path

import pytest

from agent_tools.finals_rebuild.ce115_research_healer_protocol import sha256_text
from agent_tools.finals_rebuild.ce115_research_healer_rules_l2 import (
    PRIORITY,
    RULE_ID,
    _correct_answer_fingerprint,
    analyze_l2_payload_wrap,
)
from agent_tools.finals_rebuild.ce115_research_healer_runner import (
    MathHealerRunner,
    RULE_ALLOWLIST,
    iter_manifest_cases,
    load_regression_manifest,
    run_research_healer,
)
from agent_tools.finals_rebuild.math_boundary_pilot import (
    classify_response,
    load_pilot_tasks,
)

ROOT = Path(__file__).resolve().parents[2]
FIX = ROOT / "tests/finals_rebuild/fixtures/ce115_research_healer"
MANIFEST_PATH = FIX / "regression_manifest.json"
TASK_MANIFEST = ROOT / "tests/finals_rebuild/fixtures/math_generation_tasks_ce115_pilot.jsonl"
RULE = "L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP"


def _tasks() -> dict[str, dict]:
    return {t["task_id"]: t for t in load_pilot_tasks(TASK_MANIFEST)}


def _read(case_id: str) -> tuple[dict, str, dict]:
    manifest = load_regression_manifest(MANIFEST_PATH)
    case = next(c for c in iter_manifest_cases(manifest) if c["case_id"] == case_id)
    source = (FIX / case["source_artifact"]).read_text(encoding="utf-8")
    frozen = json.loads((FIX / case["frozen_artifact"]).read_text(encoding="utf-8"))
    return case, source, frozen


def _normalize_oracle_payload_value(source: str) -> str:
    """AST-dump fingerprint with oracle_payload value replaced by a sentinel."""
    tree = ast.parse(source)

    class _Norm(ast.NodeTransformer):
        def visit_Return(self, node: ast.Return):
            self.generic_visit(node)
            if isinstance(node.value, ast.Dict):
                new_keys = []
                new_vals = []
                for k, v in zip(node.value.keys, node.value.values):
                    new_keys.append(k)
                    if isinstance(k, ast.Constant) and k.value == "oracle_payload":
                        new_vals.append(ast.Constant(value="__ORACLE_PAYLOAD__"))
                    else:
                        new_vals.append(v)
                node.value = ast.Dict(keys=new_keys, values=new_vals)
            return node

    return ast.dump(_Norm().visit(copy.deepcopy(tree)), include_attributes=False)


def test_rule_id_and_priority():
    assert RULE_ID == RULE
    assert PRIORITY == 100
    assert RULE in RULE_ALLOWLIST
    assert RULE_ALLOWLIST[0] == RULE


def test_radical_ab1_evaluator_before_failure_after_pass():
    case, source, frozen = _read("fail_radical_ab1_l2")
    task = _tasks()["ce115_calc_radical_simplification_l1"]
    before_outcome, _, _ = classify_response(
        source, {"oracle_payload": frozen}, task
    )
    assert before_outcome == "schema_failure"

    result = MathHealerRunner().run(
        source,
        context={"frozen": frozen, "task": task, "case_id": case["case_id"]},
    )
    assert result.final_status == "changed"
    assert result.real_model_calls == 0
    outcome = next(o for o in result.rule_outcomes if o.rule_id == RULE)
    assert outcome.applicable is True
    assert outcome.triggered is True
    assert outcome.changed is True
    assert outcome.layer == "L2"
    assert outcome.priority == 100
    assert outcome.before_hash != outcome.after_hash
    assert outcome.validation.get("ast_parse_success") is True
    assert outcome.validation.get("evaluator_outcome") == "passed"
    assert outcome.validation.get("correct_answer_guard") is True

    after_outcome, _, _ = classify_response(
        result.output_source, {"oracle_payload": frozen}, task
    )
    assert after_outcome == "passed"


def test_correct_answer_and_non_payload_ast_unchanged():
    _case, source, frozen = _read("fail_radical_ab1_l2")
    before_fp = _correct_answer_fingerprint(source)
    before_norm = _normalize_oracle_payload_value(source)
    result = run_research_healer(source, context={"frozen": frozen})
    after_fp = _correct_answer_fingerprint(result.output_source)
    after_norm = _normalize_oracle_payload_value(result.output_source)
    assert before_fp == after_fp
    assert before_fp[0] is not None
    assert before_norm == after_norm
    assert '{"radicand": 27}' in result.output_source or "{'radicand': 27}" in result.output_source


def test_minimal_source_diff_is_oracle_payload_only():
    _case, source, frozen = _read("fail_radical_ab1_l2")
    result = run_research_healer(source, context={"frozen": frozen})
    # Exact surgical expectation for this fixture.
    assert '"oracle_payload": oracle_payload' in source
    assert '"oracle_payload": oracle_payload' not in result.output_source
    assert '"oracle_payload": {\'radicand\': 27}' in result.output_source
    # Everything else byte-identical outside that replacement.
    old = '"oracle_payload": oracle_payload'
    new = '"oracle_payload": {\'radicand\': 27}'
    assert source.replace(old, new, 1) == result.output_source


def test_idempotent_second_pass_noop():
    _case, source, frozen = _read("fail_radical_ab1_l2")
    first = run_research_healer(source, context={"frozen": frozen})
    assert first.final_status == "changed"
    second = run_research_healer(first.output_source, context={"frozen": frozen})
    assert second.final_status == "no_op"
    assert second.input_hash == second.output_hash
    assert second.output_source == first.output_source
    assert [o.rule_id for o in second.rule_outcomes if o.changed] == []
    assert second.real_model_calls == 0


def test_deterministic():
    _case, source, frozen = _read("fail_radical_ab1_l2")
    a = run_research_healer(source, context={"frozen": frozen})
    b = run_research_healer(source, context={"frozen": frozen})
    assert a.output_source == b.output_source
    assert a.output_hash == b.output_hash == sha256_text(a.output_source)


@pytest.mark.parametrize(
    "case_id,expect_applicable,expect_triggered,expect_changed",
    [
        ("fail_radical_ab1_l2", True, True, True),
        ("pass_radical_ab2d", True, False, False),
        ("pass_polydiv_ab2d", True, False, False),
        ("noop_multikey_frozen", True, False, False),
        ("noop_value_mismatch", True, False, False),
    ],
)
def test_case_guard_semantics(
    case_id: str,
    expect_applicable: bool,
    expect_triggered: bool,
    expect_changed: bool,
):
    _case, source, frozen = _read(case_id)
    analysis = analyze_l2_payload_wrap(source, frozen)
    assert analysis["applicable"] is expect_applicable
    assert analysis["triggered"] is expect_triggered
    result = run_research_healer(source, context={"frozen": frozen})
    changed_ids = [o.rule_id for o in result.rule_outcomes if o.changed]
    assert (RULE in changed_ids) is expect_changed
    assert result.real_model_calls == 0


def test_pass_cells_not_harmed_still_evaluate_passed():
    task = _tasks()["ce115_calc_radical_simplification_l1"]
    _case, source, frozen = _read("pass_radical_ab2d")
    before, _, _ = classify_response(source, {"oracle_payload": frozen}, task)
    result = run_research_healer(source, context={"frozen": frozen, "task": task})
    after, _, _ = classify_response(
        result.output_source, {"oracle_payload": frozen}, task
    )
    assert before == "passed"
    assert result.final_status == "no_op"
    assert after == "passed"
    assert result.output_source == source

    poly_task = _tasks()["ce115_calc_polynomial_division_l1"]
    _c2, poly_src, poly_frozen = _read("pass_polydiv_ab2d")
    before_p, _, _ = classify_response(
        poly_src, {"oracle_payload": poly_frozen}, poly_task
    )
    result_p = run_research_healer(
        poly_src, context={"frozen": poly_frozen, "task": poly_task}
    )
    after_p, _, _ = classify_response(
        result_p.output_source, {"oracle_payload": poly_frozen}, poly_task
    )
    assert before_p == "passed"
    assert result_p.final_status == "no_op"
    assert after_p == "passed"


def test_original_pilot_artifact_untouched_after_heal():
    pilot = (
        ROOT
        / "docs/experiments/results/ce115_qwen_clean_incremental_pilot_01/cells"
        / "qwen3_5_4b__ce115_calc_radical_simplification_l1__ab1__seed_2026071301"
        / "extracted_candidate.py"
    )
    before = pilot.read_bytes()
    fixture = (FIX / "cases/fail_radical_ab1_l2/candidate.py").read_text(encoding="utf-8")
    frozen = json.loads(
        (FIX / "cases/fail_radical_ab1_l2/frozen.json").read_text(encoding="utf-8")
    )
    run_research_healer(fixture, context={"frozen": frozen})
    assert pilot.read_bytes() == before
