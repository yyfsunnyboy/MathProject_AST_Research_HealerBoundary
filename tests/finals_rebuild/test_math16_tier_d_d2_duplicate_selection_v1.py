"""Focused tests for Tier D D2 duplicate definition selection."""

from __future__ import annotations

import ast
from unittest import mock

from agent_tools.finals_rebuild.aggressive_healer_tier_d import d2, run_tier_d_d2_pipeline
from agent_tools.finals_rebuild.aggressive_healer_tier_d.rule_d2_duplicate_definition_selection import (
    RULE_ID,
    apply_once as raw_apply,
)
from agent_tools.finals_rebuild.aggressive_healer_tier_d.types import RuleResult


def _unique_keepable() -> str:
    return (
        "def generate(level=1, **kwargs):\n"
        "    pass\n"
        "\n"
        "def generate(level=1, **kwargs):\n"
        "    return {'question_text': 'q', 'correct_answer': 1, 'oracle_payload': {}}\n"
    )


def _already_correct() -> str:
    return (
        "def generate(level=1, **kwargs):\n"
        "    return {'question_text': 'q', 'correct_answer': 1, 'oracle_payload': {}}\n"
    )


class TestUniqueKeepable:
    def test_keeps_complete_generate(self):
        src = _unique_keepable()
        r = d2.apply_once(src)
        assert r.applied and r.triggered
        assert r.rule_id == RULE_ID
        tree = ast.parse(r.source_out)
        gens = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "generate"]
        assert len(gens) == 1
        assert any(isinstance(n, ast.Return) for n in gens[0].body)


class TestAmbiguousDuplicate:
    def test_three_duplicates_abstain(self):
        src = (
            "def generate():\n"
            "    return 1\n"
            "def generate():\n"
            "    return 2\n"
            "def generate():\n"
            "    return 3\n"
        )
        r = d2.apply_once(src)
        assert not r.applied
        assert r.triggered
        assert r.abstention_reason == "duplicate_count_not_exactly_two"


class TestCrossScopeAbstain:
    def test_nested_duplicate_abstain(self):
        src = (
            "def outer():\n"
            "    def helper():\n"
            "        return 1\n"
            "    def helper():\n"
            "        return 2\n"
            "    return helper()\n"
        )
        r = d2.apply_once(src)
        assert not r.applied
        assert r.triggered
        assert r.abstention_reason == "cross_scope_duplicate_abstain"


class TestDependencyConflictAbstain:
    def test_two_complete_generates_close_scores_abstain_or_select(self):
        # Two non-trivial bodies with similar ranking features → margin/tie abstain
        src = (
            "def generate(level=1, **kwargs):\n"
            "    x = 1\n"
            "    return {'question_text': 'q', 'correct_answer': x, 'oracle_payload': {}}\n"
            "\n"
            "def generate(level=1, **kwargs):\n"
            "    y = 2\n"
            "    return {'question_text': 'q', 'correct_answer': y, 'oracle_payload': {}}\n"
        )
        r = d2.apply_once(src)
        # Either selects later by lineno tie-break after equal scores, or abstains
        if not r.applied:
            assert "dependency_conflict" in r.abstention_reason or r.abstention_reason in {
                "score_tie",
                "margin_below_minimum",
                "similarity_sole_decision_or_tie_without_similarity",
            }
        else:
            # deterministic keep of one is acceptable if margin exists via lineno sort key on method id
            tree = ast.parse(r.source_out)
            gens = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "generate"]
            assert len(gens) == 1


class TestAlreadyCorrect:
    def test_no_duplicate_noop(self):
        src = _already_correct()
        r = d2.apply_once(src)
        assert not r.applied
        assert r.source_out == src
        assert r.abstention_reason == "no_duplicate_definitions"


class TestIdempotence:
    def test_second_apply_zero_diff(self):
        src = _unique_keepable()
        r1 = d2.apply_once(src)
        assert r1.applied
        r2 = d2.apply_once(r1.source_out)
        assert not r2.applied
        assert r2.source_out == r1.source_out
        pipe = run_tier_d_d2_pipeline(src)
        assert pipe.pipeline_idempotent and not pipe.rolled_back
        again = run_tier_d_d2_pipeline(pipe.post_source)
        assert again.mutation_count == 0


class TestRollback:
    def test_pipeline_rollback_on_non_idempotent(self):
        src = _unique_keepable()
        real = raw_apply
        calls = {"n": 0}

        def flaky(source: str) -> RuleResult:
            calls["n"] += 1
            r = real(source)
            if calls["n"] >= 2 and not r.applied:
                r.applied = True
                r.triggered = True
                r.source_out = source + "\n"
                r.edit_count = 1
            return r

        with mock.patch(
            "agent_tools.finals_rebuild.aggressive_healer_tier_d.pipeline.d2.apply_once",
            side_effect=flaky,
        ):
            pipe = run_tier_d_d2_pipeline(src)
        assert pipe.rolled_back
        assert pipe.post_source == src
        assert pipe.abstention_reason == "NON_IDEMPOTENT_ABORT"
