"""L1_COMMENT_ONLY_IF_INSERT_PASS — paused experimental / exploratory parse-only.

Not on production RULE_ALLOWLIST. Tests opt in via explicit experimental allowlist.
"""

from __future__ import annotations

import ast
import json
from pathlib import Path

from agent_tools.finals_rebuild.ce115_research_healer_rules_l1 import (
    PRIORITY as L1_PRIORITY,
    PRODUCTION_APPROVED,
    RULE_ID as L1_ID,
    STATUS as L1_STATUS,
    analyze_l1_comment_only_if,
)
from agent_tools.finals_rebuild.ce115_research_healer_rules_l2 import (
    PRIORITY as L2_PRIORITY,
    RULE_ID as L2_ID,
)
from agent_tools.finals_rebuild.ce115_research_healer_runner import (
    EXPERIMENTAL_RULE_REGISTRY,
    RULE_ALLOWLIST,
    RULE_REGISTRY,
    MathHealerRunner,
    experimental_allowlist,
    iter_exploratory_cases,
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
EXPLORATORY_CASE = "fail_exact_ab2d_l1"


def _read_exploratory(case_id: str = EXPLORATORY_CASE) -> tuple[dict, str, dict]:
    case = next(
        c
        for c in iter_exploratory_cases(load_regression_manifest(MANIFEST_PATH))
        if c["case_id"] == case_id
    )
    source = (FIX / case["source_artifact"]).read_text(encoding="utf-8")
    frozen = json.loads((FIX / case["frozen_artifact"]).read_text(encoding="utf-8"))
    return case, source, frozen


def _read_production(case_id: str) -> tuple[dict, str, dict]:
    case = next(
        c for c in iter_manifest_cases(load_regression_manifest(MANIFEST_PATH)) if c["case_id"] == case_id
    )
    source = (FIX / case["source_artifact"]).read_text(encoding="utf-8")
    frozen = json.loads((FIX / case["frozen_artifact"]).read_text(encoding="utf-8"))
    return case, source, frozen


def _tasks():
    return {t["task_id"]: t for t in load_pilot_tasks(TASK_MANIFEST)}


def test_l1_paused_not_on_production_allowlist():
    assert L1_ID == "L1_COMMENT_ONLY_IF_INSERT_PASS"
    assert L1_PRIORITY == 50
    assert L2_PRIORITY == 100
    assert L1_PRIORITY < L2_PRIORITY
    assert PRODUCTION_APPROVED is False
    assert L1_STATUS == "paused_experimental_draft"
    assert RULE_ALLOWLIST == (L2_ID,)
    assert L1_ID not in RULE_ALLOWLIST
    assert L1_ID not in RULE_REGISTRY
    assert L1_ID in EXPERIMENTAL_RULE_REGISTRY
    ordered = select_allowlisted_rules(allowlist=experimental_allowlist())
    assert [r.rule_id for r in ordered] == [L1_ID, L2_ID]


def test_exact_ab2d_before_parse_failure_after_success_minimal_diff():
    _case, source, frozen = _read_exploratory()
    try:
        ast.parse(source)
        raise AssertionError("expected parse failure before heal")
    except SyntaxError:
        pass

    task = _tasks()["ce115_calc_exact_rational_expression_l1"]
    before = classify_response(source, {"oracle_payload": frozen}, task)[0]
    assert before == "parse_minor"

    result = MathHealerRunner(allowlist=experimental_allowlist()).run(
        source, context={"frozen": frozen, "task": task}
    )
    assert result.final_status == "changed"
    assert result.real_model_calls == 0
    changed = [o for o in result.rule_outcomes if o.changed]
    assert [o.rule_id for o in changed] == [L1_ID]
    assert changed[0].layer == "L1"
    assert changed[0].priority == 50
    assert changed[0].validation.get("full_repair_to_pass_claimed") is False
    assert changed[0].validation.get("repair_scope") in {
        "parse_only_l1",
        "exploratory_parse_only",
    }
    ast.parse(result.output_source)

    before_lines = source.splitlines()
    after_lines = result.output_source.splitlines()
    assert len(after_lines) == len(before_lines) + 1
    expected = []
    for line in before_lines:
        expected.append(line)
        if 'if frozen_params["products"][0]["sign"] == -1:' in line:
            expected.append("        pass")
    assert after_lines == expected

    after = classify_response(
        result.output_source, {"oracle_payload": frozen}, task
    )[0]
    assert after == "schema_failure"
    assert after != "passed"
    assert changed[0].validation.get("evaluator_outcome") == "schema_failure"
    assert changed[0].validation.get("next_layer_status") == "schema_failure"


def test_idempotent_second_pass():
    _case, source, frozen = _read_exploratory()
    first = run_research_healer(
        source, context={"frozen": frozen}, allowlist=experimental_allowlist()
    )
    assert first.final_status == "changed"
    second = run_research_healer(
        first.output_source,
        context={"frozen": frozen},
        allowlist=experimental_allowlist(),
    )
    assert second.final_status == "no_op"
    assert second.output_source == first.output_source
    assert [o.rule_id for o in second.rule_outcomes if o.changed] == []


def test_comment_only_for_while_try_do_not_trigger():
    samples = {
        "for": "def generate():\n    for x in [1]:\n        # only comment\n    return {}\n",
        "while": "def generate():\n    while False:\n        # only comment\n    return {}\n",
        "try": "def generate():\n    try:\n        # only comment\n    except Exception:\n        pass\n    return {}\n",
    }
    for kind, src in samples.items():
        analysis = analyze_l1_comment_only_if(src)
        assert analysis["triggered"] is False, kind
        result = run_research_healer(src, allowlist=(L1_ID,))
        assert result.final_status == "no_op", kind
        assert [o.rule_id for o in result.rule_outcomes if o.changed] == []


def test_non_comment_only_if_does_not_trigger():
    src = (
        "def generate():\n"
        "    if True:\n"
        "        x = 1\n"
        "    return {'question_text': 'q', 'correct_answer': {'v': 1}, 'oracle_payload': {'a': 1}}\n"
    )
    analysis = analyze_l1_comment_only_if(src)
    assert analysis["applicable"] is False
    result = run_research_healer(
        src, context={"frozen": {"a": 1}}, allowlist=experimental_allowlist()
    )
    assert L1_ID not in [o.rule_id for o in result.rule_outcomes if o.changed]


def test_production_runner_does_not_apply_l1_to_exploratory_fixture():
    _case, source, frozen = _read_exploratory()
    result = MathHealerRunner().run(source, context={"frozen": frozen})
    assert L1_ID not in [o.rule_id for o in result.rule_outcomes]
    assert result.final_status == "no_op"
    assert result.output_source == source


def test_l2_repair_to_pass_not_regressed():
    _case, source, frozen = _read_production("fail_radical_ab1_l2")
    task = _tasks()["ce115_calc_radical_simplification_l1"]
    before = classify_response(source, {"oracle_payload": frozen}, task)[0]
    assert before == "schema_failure"
    result = MathHealerRunner().run(source, context={"frozen": frozen, "task": task})
    assert result.final_status == "changed"
    assert [o.rule_id for o in result.rule_outcomes if o.changed] == [L2_ID]
    after = classify_response(
        result.output_source, {"oracle_payload": frozen}, task
    )[0]
    assert after == "passed"


def test_cumulative_manifest_production_only():
    manifest = load_regression_manifest(MANIFEST_PATH)
    assert manifest["allowlist_expected"] == [L2_ID]
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
            if prov.changed:
                assert prov.stopped_after_change is True


def test_original_pilot_artifact_untouched():
    pilot = (
        ROOT
        / "docs/experiments/results/ce115_qwen_clean_incremental_pilot_01/cells"
        / "qwen3_5_4b__ce115_calc_exact_rational_expression_l1__ab2d__seed_2026071301"
        / "extracted_candidate.py"
    )
    before = pilot.read_bytes()
    _case, source, frozen = _read_exploratory()
    run_research_healer(source, context={"frozen": frozen}, allowlist=experimental_allowlist())
    assert pilot.read_bytes() == before
