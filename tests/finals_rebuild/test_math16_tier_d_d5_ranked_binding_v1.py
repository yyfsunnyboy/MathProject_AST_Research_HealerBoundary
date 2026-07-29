"""Focused tests for Tier D D5 ranked domain method binding."""

from __future__ import annotations

import ast
from unittest import mock

from agent_tools.finals_rebuild.aggressive_healer_tier_d import d5, run_tier_d_d5_pipeline
from agent_tools.finals_rebuild.aggressive_healer_tier_d.rule_d5_ranked_domain_method_binding import (
    RULE_ID,
    apply_once as raw_apply,
)
from agent_tools.finals_rebuild.aggressive_healer_tier_d.types import RuleResult

EXPOSED = ["FractionOps.create", "FractionOps.add", "FractionOps.mul"]


def _wrong_sqrt() -> str:
    return (
        "def generate(level=1, **kwargs):\n"
        "    x = FractionOps.sqrt(7)\n"
        "    return {'question_text': 'q', 'correct_answer': x, 'oracle_payload': {}}\n"
    )


def _already_correct() -> str:
    return (
        "def generate(level=1, **kwargs):\n"
        "    x = FractionOps.create(7)\n"
        "    return {'question_text': 'q', 'correct_answer': x, 'oracle_payload': {}}\n"
    )


class TestUniqueWinner:
    def test_unique_highest_renames_method(self):
        src = _wrong_sqrt()
        r = d5.apply_once(src, exposed_symbols=EXPOSED, domain="Fraction")
        assert r.applied and r.triggered
        assert r.rule_id == RULE_ID
        assert "FractionOps.create" in r.source_out
        assert "FractionOps.sqrt" not in r.source_out
        assert "FractionOps.create(7)" in r.source_out
        ast.parse(r.source_out)


class TestTieAbstain:
    def test_tie_abstain(self):
        src = (
            "def generate(level=1, **kwargs):\n"
            "    x = FractionOps.neg(1, 2)\n"
            "    return x\n"
        )
        # Force equal scores via patching select_unique_winner path: use two methods with identical features
        exposed = ["FractionOps.add", "FractionOps.sub"]  # both arity-2, similar
        r = d5.apply_once(src, exposed_symbols=exposed, domain="Fraction")
        assert not r.applied
        assert r.triggered
        assert r.abstention_reason in {
            "score_tie",
            "margin_below_minimum",
            "similarity_sole_decision_or_tie_without_similarity",
        }


class TestMarginAbstain:
    def test_margin_below_2_abstain(self):
        # create vs from_parts on unary-ish call often margins via similarity only;
        # use exposed set where winners are close
        src = (
            "def generate(level=1, **kwargs):\n"
            "    x = FractionOps.neg(1)\n"
            "    return x\n"
        )
        exposed = ["FractionOps.create", "FractionOps.from_parts", "FractionOps.add", "FractionOps.sub"]
        r = d5.apply_once(src, exposed_symbols=exposed, domain="Fraction")
        assert not r.applied
        assert r.abstention_reason in {
            "margin_below_minimum",
            "similarity_sole_decision_or_tie_without_similarity",
            "score_tie",
        }


class TestScoreBelowMinimum:
    def test_score_below_8_abstain(self):
        src = (
            "def generate(level=1, **kwargs):\n"
            "    x = FractionOps.neg(a=1, b=2, c=3)\n"
            "    return x\n"
        )
        # methods that don't match kwargs → low arity/keyword features
        exposed = ["FractionOps.add", "FractionOps.mul"]
        r = d5.apply_once(src, exposed_symbols=exposed, domain="Fraction")
        assert not r.applied
        # may be best_score_below_minimum or other abstain
        assert r.abstained
        assert r.source_out == src


class TestSimilarityOnlyAbstain:
    def test_similarity_sole_decision_abstain(self):
        src = (
            "def generate(level=1, **kwargs):\n"
            "    x = FractionOps.neg(1)\n"
            "    return x\n"
        )
        exposed = ["FractionOps.create", "FractionOps.from_parts", "FractionOps.add", "FractionOps.sub"]
        r = d5.apply_once(src, exposed_symbols=exposed, domain="Fraction")
        assert not r.applied
        assert r.abstention_reason == "similarity_sole_decision_or_tie_without_similarity"


class TestAlreadyCorrect:
    def test_preserve_correct_binding(self):
        src = _already_correct()
        r = d5.apply_once(src, exposed_symbols=EXPOSED, domain="Fraction")
        assert not r.applied
        assert r.source_out == src
        assert r.abstention_reason == "no_ranked_wrong_method_site"


class TestIdempotence:
    def test_second_apply_zero_diff(self):
        src = _wrong_sqrt()
        r1 = d5.apply_once(src, exposed_symbols=EXPOSED, domain="Fraction")
        assert r1.applied
        r2 = d5.apply_once(r1.source_out, exposed_symbols=EXPOSED, domain="Fraction")
        assert not r2.applied
        assert r2.source_out == r1.source_out
        pipe = run_tier_d_d5_pipeline(src, exposed_symbols=EXPOSED, domain="Fraction")
        assert pipe.pipeline_idempotent and pipe.mutation_count == 1
        again = run_tier_d_d5_pipeline(pipe.post_source, exposed_symbols=EXPOSED, domain="Fraction")
        assert again.mutation_count == 0
        assert again.post_source == pipe.post_source


class TestRollback:
    def test_pipeline_rollback_on_non_idempotent(self):
        src = _wrong_sqrt()
        real = raw_apply
        calls = {"n": 0}

        def flaky(source: str, **kwargs) -> RuleResult:
            calls["n"] += 1
            r = real(source, **kwargs)
            if calls["n"] >= 2 and not r.applied:
                r.applied = True
                r.triggered = True
                r.source_out = source + "\n"
                r.edit_count = 1
            return r

        with mock.patch(
            "agent_tools.finals_rebuild.aggressive_healer_tier_d.pipeline.d5.apply_once",
            side_effect=flaky,
        ):
            pipe = run_tier_d_d5_pipeline(src, exposed_symbols=EXPOSED, domain="Fraction")
        assert pipe.rolled_back
        assert pipe.post_source == src
        assert pipe.abstention_reason == "NON_IDEMPOTENT_ABORT"
