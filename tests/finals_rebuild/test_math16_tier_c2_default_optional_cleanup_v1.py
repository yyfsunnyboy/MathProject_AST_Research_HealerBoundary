"""Focused tests for Tier C2 default_optional_pure_form_cleanup.

Synthetic fixtures only — no formal 320-cell bulk run here.
"""

from __future__ import annotations

import ast
from unittest import mock

import pytest

from agent_tools.finals_rebuild.aggressive_healer_tier_c2 import (
    CURRENT_TIER,
    LAYER_ROLE,
    RULE_ID,
    SUBTYPE,
    apply_once,
    run_tier_c2_default_optional_cleanup,
)
from agent_tools.finals_rebuild.aggressive_healer_tier_c2.rule_default_optional_cleanup import (
    apply_once as raw_apply,
)
from agent_tools.finals_rebuild.aggressive_healer_tier_c2.types import RuleResult


def _fmt_with_default_var() -> str:
    return (
        "def generate(oracle_payload):\n"
        "    coeffs = [1, 2]\n"
        "    return PolynomialOps.format_latex(coeffs, var='x')\n"
    )


def _fmt_already_clean() -> str:
    return (
        "def generate(oracle_payload):\n"
        "    coeffs = [1, 2]\n"
        "    return PolynomialOps.format_latex(coeffs)\n"
    )


class TestFixable:
    def test_fix_format_latex_var_x_single_quotes(self):
        src = _fmt_with_default_var()
        r = apply_once(src)
        assert r.applied
        assert r.triggered
        assert r.rule_id == RULE_ID
        assert r.current_tier == CURRENT_TIER
        assert r.layer_role == LAYER_ROLE
        assert r.repair_subtype == SUBTYPE
        assert r.ssot_entry_id == "PolynomialOps.format_latex"
        assert "var=" not in r.source_out
        assert "PolynomialOps.format_latex(coeffs)" in r.source_out
        ast.parse(r.source_out)

    def test_fix_format_latex_var_x_double_quotes(self):
        src = (
            "def generate(oracle_payload):\n"
            '    return PolynomialOps.format_latex([0, 1], var="x")\n'
        )
        r = apply_once(src)
        assert r.applied
        assert 'var=' not in r.source_out
        assert "PolynomialOps.format_latex([0, 1])" in r.source_out
        ast.parse(r.source_out)


class TestAlreadyCorrect:
    def test_preserve_format_latex_without_var(self):
        src = _fmt_already_clean()
        r = apply_once(src)
        assert not r.applied
        assert r.abstained
        assert r.source_out == src
        assert r.abstention_reason == "no_redundant_optional_default_literal"

    def test_preserve_to_latex_without_mixed(self):
        src = "y = FractionOps.to_latex(val)\n"
        r = apply_once(src)
        assert not r.applied
        assert r.source_out == src


class TestWrongDefaultValueAbstain:
    def test_abstain_var_y_not_default(self):
        src = "PolynomialOps.format_latex(coeffs, var='y')\n"
        r = apply_once(src)
        assert not r.applied
        assert r.source_out == src
        assert r.abstention_reason == "no_redundant_optional_default_literal"

    def test_abstain_mixed_true_not_default(self):
        src = "FractionOps.to_latex(val, mixed=True)\n"
        r = apply_once(src)
        assert not r.applied
        assert r.source_out == src
        assert r.abstention_reason == "no_redundant_optional_default_literal"


class TestNonLiteralAmbiguousAbstain:
    def test_abstain_non_literal_var_name(self):
        src = "v = 'x'\nPolynomialOps.format_latex(coeffs, var=v)\n"
        r = apply_once(src)
        assert not r.applied
        assert r.source_out == src
        assert r.abstention_reason == "no_redundant_optional_default_literal"

    def test_abstain_multiple_redundant_defaults_on_one_call(self):
        # format_term(coeff, radicand, is_first=True) — only one optional default usually
        # Use RadicalOps.format_expression(terms_dict, denominator=1) alone is one.
        # For multi on one call: FractionOps.to_latex(val, mixed=False) only one optional.
        # Construct with two optionals that both equal defaults if any API has two:
        # PolynomialOps.coeffs_from_py_expression(expression, var='x') — one optional.
        # RadicalOps.format_term(c, r, is_first=True) — one optional.
        # Use a synthetic double by calling format_latex with var='x' AND a fake — can't.
        # Instead: two separate optional-default kwargs on format_term if we add is_first=True
        # only one. Skip — use two calls for multi-call test; for this test use
        # coeffs_from_py_expression(expr, var='x') is single.
        # Force ambiguity via two keywords both matching defaults on format_expression:
        # signature (terms_dict, denominator=1) — only one optional.
        #
        # Practical approach: monkeypatch defaults to expose two optionals on a call,
        # OR use source with two known defaults: 
        # `RadicalOps.format_term(1, 2, is_first=True)` is one site.
        #
        # Dual defaults: manually craft Call that our finder sees as two sites by
        # temporarily patching _method_defaults.
        src = "PolynomialOps.format_latex(coeffs, var='x')\n"

        def fake_defaults(fqname: str):
            if fqname == "PolynomialOps.format_latex":
                return {"var": "x", "unused": 0}
            return {}

        with mock.patch(
            "agent_tools.finals_rebuild.aggressive_healer_tier_c2."
            "rule_default_optional_cleanup._method_defaults",
            side_effect=fake_defaults,
        ):
            # Still only one keyword in source — need source with unused=0 too
            src2 = "PolynomialOps.format_latex(coeffs, var='x', unused=0)\n"
            # unused is not a real param — inspect won't list it unless we fake defaults
            # and the keyword is present; finder checks kw.arg in defaults
            r = apply_once(src2)
        assert not r.applied
        assert "ambiguous_multiple_redundant_defaults_on_one_call" in r.abstention_reason


class TestMultiCallAbstain:
    def test_abstain_two_format_latex_default_vars(self):
        src = (
            "a = PolynomialOps.format_latex(c1, var='x')\n"
            "b = PolynomialOps.format_latex(c2, var='x')\n"
        )
        r = apply_once(src)
        assert not r.applied
        assert r.source_out == src
        assert "ambiguous_multiple_call_sites" in r.abstention_reason


class TestIdempotence:
    def test_second_apply_zero_diff(self):
        src = _fmt_with_default_var()
        r1 = apply_once(src)
        assert r1.applied
        r2 = apply_once(r1.source_out)
        assert not r2.applied
        assert r2.source_out == r1.source_out
        pipe = run_tier_c2_default_optional_cleanup(src)
        assert pipe.pipeline_idempotent
        assert not pipe.rolled_back
        assert pipe.mutation_count == 1
        again = run_tier_c2_default_optional_cleanup(pipe.post_source)
        assert again.mutation_count == 0
        assert again.post_source == pipe.post_source


class TestRollbackSchemaFailure:
    def test_pipeline_rollback_on_non_idempotent_second_pass(self):
        src = _fmt_with_default_var()
        real_apply = raw_apply
        calls = {"n": 0}

        def flaky(source: str) -> RuleResult:
            calls["n"] += 1
            result = real_apply(source)
            if calls["n"] >= 2 and not result.applied:
                # Force a false-positive second mutation signal
                result.applied = True
                result.triggered = True
                result.source_out = source + "\n"
                result.edit_count = 1
            return result

        with mock.patch(
            "agent_tools.finals_rebuild.aggressive_healer_tier_c2.pipeline.apply_once",
            side_effect=flaky,
        ):
            pipe = run_tier_c2_default_optional_cleanup(src)
        assert pipe.rolled_back
        assert pipe.post_source == src
        assert pipe.abstention_reason == "NON_IDEMPOTENT_ABORT"
        assert pipe.outcome_taxonomy == "non_idempotent_abort"
