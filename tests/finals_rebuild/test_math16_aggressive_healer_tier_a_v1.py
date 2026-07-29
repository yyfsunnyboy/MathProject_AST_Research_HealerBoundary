"""Focused tests for Aggressive Healer v1 Tier A rules + pipeline.

Synthetic fixtures only — no formal 320/422 cells.
"""

from __future__ import annotations

import ast

from agent_tools.finals_rebuild.aggressive_healer_tier_a import (
    RULE_ORDER,
    run_tier_a_pipeline,
)
from agent_tools.finals_rebuild.aggressive_healer_tier_a import (
    rule_a1_fullwidth as a1,
    rule_a2_delimiter as a2,
    rule_a3_empty_suite as a3,
    rule_a4_import_binding as a4,
)
from agent_tools.finals_rebuild.aggressive_healer_tier_a.types import RuleResult


# ---------------------------------------------------------------------------
# A1 — fullwidth normalization
# ---------------------------------------------------------------------------


class TestA1Fullwidth:
    def test_fix_paren_call(self):
        src = "def f():\n    return g（1，2）\n"
        r = a1.apply_once(src)
        assert r.applied
        assert r.rule_id == "core.normalize_fullwidth_python_punctuation"
        ast.parse(r.source_out)
        assert "（" not in r.source_out and "，" not in r.source_out

    def test_fix_colon_if(self):
        src = "if True：\n    pass\n"
        r = a1.apply_once(src)
        assert r.applied
        assert "：" not in r.source_out
        ast.parse(r.source_out)

    def test_no_change_string_content(self):
        src = 'x = "全形：，（）"\n'
        r = a1.apply_once(src)
        assert not r.applied
        assert r.source_out == src

    def test_no_change_comment(self):
        src = "x = 1  # 全形：（）\n"
        r = a1.apply_once(src)
        assert not r.applied
        assert r.source_out == src

    def test_abstain_unmapped_fullwidth_operator_fail_closed(self):
        # ＞ not in map; mixed with mapped ： → fail-closed identical
        src = "if x＞0：\n    pass\n"
        r = a1.apply_once(src)
        assert not r.applied
        assert r.source_out == src

    def test_abstain_only_unmapped_symbol(self):
        src = "x = 1 ＃ comment-like but hash is ascii; y＝2\n"
        # ＝ not in map; source may still parse or not — rule must not rewrite ＝
        r = a1.apply_once(src)
        assert "＝" in r.source_out
        assert r.source_out == src or "＝" in r.source_out

    def test_already_correct_preservation(self):
        src = "def f(x, y):\n    return x + y\n"
        r = a1.apply_once(src)
        assert not r.applied
        assert r.source_out == src

    def test_idempotence(self):
        src = "f(x，y)\n"
        r1 = a1.apply_once(src)
        assert r1.applied
        r2 = a1.apply_once(r1.source_out)
        assert not r2.applied
        assert r2.source_out == r1.source_out


# ---------------------------------------------------------------------------
# A2 — unique missing delimiter
# ---------------------------------------------------------------------------


class TestA2Delimiter:
    def test_fix_missing_paren(self):
        src = "def f():\n    return g(\n"
        r = a2.apply_once(src)
        assert r.applied
        assert r.extras["delimiter_char"] == ")"
        assert r.extras["uniqueness_proof"] is True
        ast.parse(r.source_out)

    def test_fix_missing_bracket(self):
        src = "xs = [1\n"
        r = a2.apply_once(src)
        assert r.applied
        assert r.extras["delimiter_char"] == "]"
        ast.parse(r.source_out)

    def test_fix_missing_brace_unique(self):
        src = "d = {1\n"
        r = a2.apply_once(src)
        assert r.applied
        assert r.extras["delimiter_char"] == "}"
        ast.parse(r.source_out)

    def test_no_change_non_delimiter_syntax_error(self):
        src = "def f(:\n    pass\n"
        r = a2.apply_once(src)
        assert not r.applied
        assert r.abstained
        assert r.source_out == src

    def test_no_change_empty_suite_error(self):
        src = "def f():\n"
        r = a2.apply_once(src)
        assert not r.applied
        assert r.source_out == src

    def test_abstain_ambiguous_bracket_positions(self):
        src = "xs = [1, 2, 3\n"
        r = a2.apply_once(src)
        assert not r.applied
        assert r.abstained
        assert "ambiguous" in r.abstention_reason
        assert r.source_out == src

    def test_abstain_already_parses(self):
        src = "def f():\n    return (1 + 2)\n"
        r = a2.apply_once(src)
        assert not r.applied
        assert r.abstention_reason == "source_already_parses"

    def test_already_correct_preservation(self):
        src = "x = [1, 2, 3]\n"
        r = a2.apply_once(src)
        assert r.source_out == src
        assert not r.applied

    def test_idempotence(self):
        src = "def f():\n    return g(\n"
        r1 = a2.apply_once(src)
        assert r1.applied
        r2 = a2.apply_once(r1.source_out)
        assert not r2.applied
        assert r2.source_out == r1.source_out


# ---------------------------------------------------------------------------
# A3 — empty suite insert pass
# ---------------------------------------------------------------------------


class TestA3EmptySuite:
    def test_fix_empty_if(self):
        src = "if True:\n"
        r = a3.apply_once(src)
        assert r.applied
        assert "pass" in r.source_out
        ast.parse(r.source_out)
        assert r.extras["suite_owner_kind"] == "if"

    def test_fix_empty_def(self):
        src = "def f():\n"
        r = a3.apply_once(src)
        assert r.applied
        ast.parse(r.source_out)
        assert r.extras["suite_owner_kind"] == "def"

    def test_fix_empty_while(self):
        src = "while False:\n"
        r = a3.apply_once(src)
        assert r.applied
        assert r.extras["suite_owner_kind"] == "while"
        ast.parse(r.source_out)

    def test_fix_empty_for_with_comment_preserved(self):
        src = "for i in range(1):\n    # keep\n"
        r = a3.apply_once(src)
        assert r.applied
        assert "# keep" in r.source_out
        ast.parse(r.source_out)

    def test_no_change_non_empty_suite(self):
        src = "if True:\n    x = 1\n"
        r = a3.apply_once(src)
        assert not r.applied
        assert r.source_out == src

    def test_no_change_delimiter_error(self):
        src = "def f():\n    return (1 + 2\n"
        r = a3.apply_once(src)
        assert not r.applied
        assert r.source_out == src

    def test_abstain_two_empty_suites(self):
        src = "if True:\n\nif False:\n"
        r = a3.apply_once(src)
        assert not r.applied
        assert r.abstained
        assert "ambiguous" in r.abstention_reason
        assert r.source_out == src

    def test_abstain_already_parses(self):
        src = "while False:\n    pass\n"
        r = a3.apply_once(src)
        assert not r.applied
        assert r.abstention_reason == "source_already_parses"

    def test_already_correct_preservation(self):
        src = "def f():\n    return 1\n"
        r = a3.apply_once(src)
        assert r.source_out == src

    def test_idempotence(self):
        src = "if True:\n"
        r1 = a3.apply_once(src)
        assert r1.applied
        r2 = a3.apply_once(r1.source_out)
        assert not r2.applied
        assert r2.source_out == r1.source_out


# ---------------------------------------------------------------------------
# A4 — unique import binding
# ---------------------------------------------------------------------------


class TestA4ImportBinding:
    def test_fix_fraction(self):
        src = "def f():\n    return Fraction(1, 2)\n"
        r = a4.apply_once(src)
        assert r.applied
        assert "from fractions import Fraction" in r.source_out
        ast.parse(r.source_out)
        assert r.extras["missing_name"] == "Fraction"

    def test_fix_defaultdict(self):
        src = "def f():\n    return defaultdict(int)\n"
        r = a4.apply_once(src)
        assert r.applied
        assert "from collections import defaultdict" in r.source_out
        ast.parse(r.source_out)

    def test_no_change_local_definition(self):
        src = "class Fraction:\n    pass\n\ndef f():\n    return Fraction()\n"
        r = a4.apply_once(src)
        assert not r.applied
        assert r.source_out == src

    def test_no_change_domain_ops_name(self):
        src = "def f():\n    return IntegerOps.gcd(4, 6)\n"
        r = a4.apply_once(src)
        assert not r.applied
        assert r.abstained
        assert r.source_out == src

    def test_abstain_multiple_missing_stdlib(self):
        src = "def f():\n    return Fraction(1, 2) + Decimal(3)\n"
        r = a4.apply_once(src)
        assert not r.applied
        assert "multiple_missing" in r.abstention_reason
        assert r.source_out == src

    def test_abstain_unknown_name(self):
        src = "def f():\n    return not_a_real_symbol(1)\n"
        r = a4.apply_once(src)
        assert not r.applied
        assert r.source_out == src

    def test_already_correct_preservation(self):
        src = "from fractions import Fraction\n\ndef f():\n    return Fraction(1, 2)\n"
        r = a4.apply_once(src)
        assert not r.applied
        assert r.source_out == src

    def test_idempotence(self):
        src = "def f():\n    return Counter()\n"
        r1 = a4.apply_once(src)
        assert r1.applied
        r2 = a4.apply_once(r1.source_out)
        assert not r2.applied
        assert r2.source_out == r1.source_out

    def test_ops_shadowing_abstain(self):
        src = (
            "class IntegerOps:\n    pass\n\n"
            "def f():\n    return Fraction(1, 1)\n"
        )
        r = a4.apply_once(src)
        assert not r.applied
        assert r.abstention_reason == "ops_class_shadowing"


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------


class TestTierAPipeline:
    def test_rule_order_constant(self):
        assert RULE_ORDER == (
            "core.normalize_fullwidth_python_punctuation",
            "TIER_A_UNIQUE_MISSING_DELIMITER_REPAIR_V1",
            "TIER_A_EMPTY_SUITE_INSERT_PASS_V1",
            "TIER_A_UNIQUE_IMPORT_BINDING_REPAIR_V1",
        )

    def test_pipeline_runs_four_rules_in_order(self):
        src = "def f():\n    return 1\n"
        out = run_tier_a_pipeline(src)
        assert len(out.rule_logs) == 4
        ids = [log["rule_id"] for log in out.rule_logs]
        assert ids == list(RULE_ORDER)
        assert out.mutation_count == 0
        assert out.pipeline_idempotent
        assert out.post_source == src

    def test_pipeline_normalization_then_import(self):
        # Fullwidth in a parseable-after-A1 program that needs Fraction
        src = "def f（）：\n    return Fraction(1, 2)\n"
        out = run_tier_a_pipeline(src)
        assert out.pipeline_idempotent
        assert not out.rolled_back
        assert "core.normalize_fullwidth_python_punctuation" in out.rules_fired
        assert "TIER_A_UNIQUE_IMPORT_BINDING_REPAIR_V1" in out.rules_fired
        assert out.mutation_count <= 4
        ast.parse(out.post_source)
        # Each rule at most once
        assert out.rules_fired.count("core.normalize_fullwidth_python_punctuation") <= 1

    def test_pipeline_empty_suite_only(self):
        src = "def f():\n"
        out = run_tier_a_pipeline(src)
        assert "TIER_A_EMPTY_SUITE_INSERT_PASS_V1" in out.rules_fired
        assert out.mutation_count <= 4
        ast.parse(out.post_source)
        assert out.pipeline_idempotent

    def test_pipeline_second_run_zero_diff(self):
        src = "def f():\n    return g(\n"
        out1 = run_tier_a_pipeline(src)
        assert out1.pipeline_idempotent
        out2 = run_tier_a_pipeline(out1.post_source)
        assert out2.mutation_count == 0
        assert out2.post_source == out1.post_source

    def test_pipeline_idempotence_failure_rolls_back(self):
        def flaky_a1(source: str) -> RuleResult:
            # Always append a space — non-idempotent
            healed = source + " "
            return RuleResult(
                rule_id=a1.RULE_ID,
                sequence_index=1,
                triggered=True,
                applied=True,
                edit_count=1,
                edit_scope="test_flaky",
                source_out=healed,
                outcome_taxonomy="repaired",
            )

        src = "x = 1\n"
        out = run_tier_a_pipeline(
            src,
            rules=(
                flaky_a1,
                a2.apply_once,
                a3.apply_once,
                a4.apply_once,
            ),
        )
        assert out.rolled_back
        assert out.outcome_taxonomy == "non_idempotent_abort"
        assert out.post_source == src
        assert out.abstention_reason == "NON_IDEMPOTENT_ABORT"

    def test_pipeline_does_not_read_pass_fail_or_answer(self):
        # Guarding API: kwargs must not include answer/pass_fail decision hooks.
        src = "x = 1\n"
        out = run_tier_a_pipeline(src)
        # Ensure audit may omit pass_fail and still succeed
        for log in out.rule_logs:
            assert log.get("pre_pass_fail") is None
            assert log.get("post_pass_fail") is None

    def test_mutation_budget_at_most_four(self):
        src = "def f（）：\n"
        # After A1 may become def f(): empty suite → A3; no import
        out = run_tier_a_pipeline(src)
        assert out.mutation_count <= 4
