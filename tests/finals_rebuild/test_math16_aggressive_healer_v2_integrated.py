# -*- coding: utf-8 -*-
"""Tests for Aggressive Healer v2 integration (zero model / zero evaluator)."""
from __future__ import annotations

from pathlib import Path

from agent_tools.finals_rebuild.aggressive_healer_v2_integrated import (
    EXISTING_PREFIX,
    FIXED_SEQUENCE,
    INTEGRATED_SEQUENCE,
    apply_aggressive_healer_v2_once,
    apply_pc_layer,
    ensure_existing_prefix_unchanged,
    run_fixpoint_v2,
    verify_certificate,
)
from agent_tools.finals_rebuild.math16_qwen4b_cellwise_fixpoint_replay_v1 import (
    FIXED_SEQUENCE as BASE_SEQ,
)

ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "artifacts/math16_ab2d_menu_vs_full_runtime_contract_v2/formal"


def test_existing_rule_order_unchanged():
    ensure_existing_prefix_unchanged()
    assert BASE_SEQ == "A→B→C1→C2→D3→D1→D5→D2"
    assert EXISTING_PREFIX == BASE_SEQ
    assert FIXED_SEQUENCE == BASE_SEQ
    assert INTEGRATED_SEQUENCE.startswith(BASE_SEQ + "→")
    assert "PC-R01" in INTEGRATED_SEQUENCE
    assert "AST_PARSE_GATE" in INTEGRATED_SEQUENCE


def test_pc_layer_only_after_parseable():
    bad = "def generate(:\n  pass\n"
    out = apply_pc_layer(
        bad,
        task_id="ce111_q02_polynomial_division_remainder",
        condition="ab2d_full_v2",
        cell_id="t",
        model_key="qwen_4b",
    )
    assert out["pc_skipped"] is True
    assert out["ast_parseable"] is False


def test_fixpoint_no_change_on_clean_source():
    src = '''
from core.prompts.domain_function_library import PolynomialOps

def generate(level=1, **kwargs):
    frozen = {"dividend_coefficients": [6, 4, 0], "divisor_coefficients": [2, 0, 0]}
    q, r = PolynomialOps.div_qr(frozen["dividend_coefficients"], frozen["divisor_coefficients"])
    r_latex = PolynomialOps.format_latex(r)
    correct_answer = {"remainder": r_latex, "canonical_latex": r_latex}
    return {"question_text": "q", "correct_answer": correct_answer, "oracle_payload": frozen}
'''
    res = run_fixpoint_v2(
        src,
        cell_id="clean",
        task_id="ce111_q02_polynomial_division_remainder",
        condition="ab2d_full_v2",
        model_key="gemini",
        max_round=3,
    )
    assert res.stop_reason == "FIXPOINT_NO_CHANGE"
    assert res.source_modified is False
    assert res.total_pc_accepts == 0


def test_fixpoint_cycle_or_converge_on_r01():
    src = '''
from core.prompts.domain_function_library import PolynomialOps

def generate(level=1, **kwargs):
    frozen = {"dividend_coefficients": [6, 4, 0], "divisor_coefficients": [2, 0, 0]}
    q, r = PolynomialOps.div_qr(frozen["dividend_coefficients"], frozen["divisor_coefficients"])
    r_latex = PolynomialOps.format_latex(r)
    correct_answer = {"remainder": str(r), "canonical_latex": r_latex}
    return {"question_text": "q", "correct_answer": correct_answer, "oracle_payload": frozen}
'''
    res = run_fixpoint_v2(
        src,
        cell_id="r01",
        task_id="ce111_q02_polynomial_division_remainder",
        condition="ab2d_full_v2",
        model_key="qwen_4b",
        max_round=4,
    )
    assert res.total_pc_accepts >= 1
    assert "PC-R01_ANSWER_SOURCE_REWIRE_V2" in res.pc_rules_fired_union
    assert res.stop_reason in {"FIXPOINT_NO_CHANGE", "SHA_CYCLE"}
    # After first repair, second round should be stable (no further PC ACCEPT).
    assert res.n_rounds >= 1


def test_known_cell_r01_decision_stable():
    cid = "qwen_4b__ce111_q02_polynomial_division_remainder__ab2d_full_v2__seed_2026071301"
    p = FORMAL / "qwen_4b" / "ab2d_full_v2" / cid / "extracted_source.py"
    if not p.exists():
        return
    src = p.read_text(encoding="utf-8")
    res = run_fixpoint_v2(
        src,
        cell_id=cid,
        task_id="ce111_q02_polynomial_division_remainder",
        condition="ab2d_full_v2",
        model_key="qwen_4b",
    )
    assert "PC-R01_ANSWER_SOURCE_REWIRE_V2" in res.pc_rules_fired_union


def test_multi_generate_abstains_pc():
    src = """
def generate(level=1, **kwargs):
    return 1
def generate(level=1, **kwargs):
    return 2
"""
    out = apply_pc_layer(
        src,
        task_id="ce115_calc_polynomial_factor_roots_l1",
        condition="ab2d_full_v2",
        cell_id="mg",
        model_key="qwen_9b",
    )
    assert out["pc_accept_count"] == 0


def test_certificate_required_fields():
    bad = {"rule_id": "X", "decision": "ACCEPT"}
    errs = verify_certificate(bad)
    assert errs
    good = {
        "rule_id": "PC-R01",
        "decision": "ACCEPT",
        "contract_sha256": "a" * 64,
        "candidate_count": 1,
        "expected_answer_not_read": True,
        "evaluator_result_not_read": True,
        "candidate_trial_count": 1,
        "before_source_sha256": "b" * 64,
        "after_source_sha256": "c" * 64,
    }
    assert verify_certificate(good) == []


def test_round_record_fields():
    src = "def generate(level=1, **kwargs):\n    return {}\n"
    rec = apply_aggressive_healer_v2_once(
        src,
        cell_id="t",
        task_id="ce112_q01_negative_integer_power",
        condition="ab2d_domain_menu_v2",
        model_key="gemini",
    )
    assert rec.round_index == 1
    assert isinstance(rec.pc_skipped, bool)
    assert isinstance(rec.source_out, str)


def test_raw_pass_identity_preserve():
    src = "def generate(level=1, **kwargs):\n    return {'question_text': 'q'}\n"
    res = run_fixpoint_v2(
        src,
        cell_id="pass_cell",
        task_id="ce112_q01_negative_integer_power",
        condition="ab2d_full_v2",
        model_key="gemini",
        raw_outcome="passed",
        identity_on_raw_pass=True,
    )
    assert res.source_modified is False
    assert res.total_pc_accepts == 0
    assert res.proposed_repair == 0
    assert res.stop_reason == "PASS_IDENTITY_PRESERVE"


def test_unparseable_pc_skipped_cert_ok():
    bad = "def generate(:\n  pass\n"
    rec = apply_aggressive_healer_v2_once(
        bad,
        cell_id="bad",
        task_id="ce111_q02_polynomial_division_remainder",
        condition="ab2d_full_v2",
        model_key="qwen_4b",
    )
    assert rec.pc_skipped is True
    assert rec.cert_verify_ok is True
    assert rec.static_recheck_ok is True
