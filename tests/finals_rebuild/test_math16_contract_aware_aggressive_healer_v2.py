# -*- coding: utf-8 -*-
"""Minimal tests for Contract-Aware Aggressive Healer v2 (zero model calls)."""
from __future__ import annotations

from pathlib import Path

from agent_tools.finals_rebuild.aggressive_healer_contract_v2.contracts import (
    CONDITIONS,
    build_all_contracts,
    load_contract,
)
from agent_tools.finals_rebuild.aggressive_healer_contract_v2.pipeline import (
    apply_contract_aware_v2,
)
from agent_tools.finals_rebuild.aggressive_healer_contract_v2.rules import (
    pc_r01_answer_source_rewire as r01,
    pc_r02_operand_order as r02,
    pc_r03_domain_api_normalize as r03,
)
from agent_tools.finals_rebuild.math16_ab2d_v2_scaffolds import TASK_SCAFFOLDS_V2

ROOT = Path(__file__).resolve().parents[2]


def test_build_32_contracts():
    built = build_all_contracts(write=True)
    assert built["index"]["n_contracts"] == 32
    assert len(built["contracts"]) == 32
    for tid in TASK_SCAFFOLDS_V2:
        for cond in CONDITIONS:
            c = load_contract(tid, cond)
            assert c["task_id"] == tid
            assert c["condition"] == cond
            assert c["domain"]
            assert c["allowed_methods"]
            assert c["contract_sha256"]


def test_pc_r01_rewires_remainder_str_r():
    src = '''
from core.prompts.domain_function_library import PolynomialOps

def generate(level=1, **kwargs):
    frozen = {"dividend_coefficients": [6, 4, 0], "divisor_coefficients": [2, 0, 0]}
    question_text = "q"
    q, r = PolynomialOps.div_qr(frozen["dividend_coefficients"], frozen["divisor_coefficients"])
    r_latex = PolynomialOps.format_latex(r)
    correct_answer = {
        "remainder": str(r),
        "canonical_latex": r_latex,
    }
    return {"question_text": question_text, "correct_answer": correct_answer, "oracle_payload": frozen}
'''
    contract = load_contract("ce111_q02_polynomial_division_remainder", "ab2d_full_v2")
    out = r01.apply_once(
        src,
        contract=contract,
        cell_id="test",
        task_id="ce111_q02_polynomial_division_remainder",
        condition="ab2d_full_v2",
        model_key="qwen_4b",
    )
    assert out.applied is True
    assert "remainder\": r_latex" in out.source_out.replace(" ", "") or 'remainder": r_latex' in out.source_out
    assert out.certificate is not None and out.certificate.decision == "ACCEPT"
    assert out.certificate.candidate_trial_count == 1
    assert out.certificate.expected_answer_not_read is True


def test_pc_r02_swaps_sub_operands():
    src = '''
from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    frozen = {"products": []}
    term = FractionOps.create("1")
    term = FractionOps.sub(term, FractionOps.create(0))
    return {"question_text": "q", "correct_answer": {"value": "1", "canonical_latex": "1"}, "oracle_payload": frozen}
'''
    contract = load_contract("ce115_calc_exact_rational_expression_l1", "ab2d_full_v2")
    out = r02.apply_once(
        src,
        contract=contract,
        cell_id="test",
        task_id="ce115_calc_exact_rational_expression_l1",
        condition="ab2d_full_v2",
        model_key="qwen_4b",
    )
    assert out.applied is True
    assert "FractionOps.sub(FractionOps.create(0), term)" in out.source_out.replace(" ", "").replace(
        "FractionOps.create(0)", "FractionOps.create(0)"
    ) or "create(0), term" in out.source_out


def test_pc_r02_abstain_on_domain_menu():
    src = "def generate(level=1, **kwargs):\n    return {}\n"
    contract = load_contract("ce115_calc_exact_rational_expression_l1", "ab2d_domain_menu_v2")
    out = r02.apply_once(
        src,
        contract=contract,
        cell_id="t",
        task_id="ce115_calc_exact_rational_expression_l1",
        condition="ab2d_domain_menu_v2",
        model_key="qwen_4b",
    )
    assert out.abstained is True
    assert out.applied is False


def test_pc_r03_normalizes_rational_ops():
    src = '''
from core.prompts.domain_function_library import RadicalOps

def generate(level=1, **kwargs):
    frozen = {"radicand": 135}
    coeff, rest = RationalOps.simplify_term(1, frozen["radicand"])
    return {"question_text": "q", "correct_answer": {"coefficient": 1, "radicand": 1, "canonical_latex": "x"}, "oracle_payload": frozen}
'''
    contract = load_contract("ce112_q04_radical_simplification", "ab2d_full_v2")
    out = r03.apply_once(
        src,
        contract=contract,
        cell_id="t",
        task_id="ce112_q04_radical_simplification",
        condition="ab2d_full_v2",
        model_key="qwen_4b",
    )
    assert out.applied is True
    assert "RationalOps" not in out.source_out
    assert "RadicalOps.simplify_term" in out.source_out


def test_pass_cell_noop_no_false_positive():
    # Synthetic clean remainder scaffold-shaped PASS path
    src = '''
from core.prompts.domain_function_library import PolynomialOps

def generate(level=1, **kwargs):
    frozen = {"dividend_coefficients": [6, 4, 0], "divisor_coefficients": [2, 0, 0]}
    q, r = PolynomialOps.div_qr(frozen["dividend_coefficients"], frozen["divisor_coefficients"])
    r_latex = PolynomialOps.format_latex(r)
    correct_answer = {"remainder": r_latex, "canonical_latex": r_latex}
    return {"question_text": "q", "correct_answer": correct_answer, "oracle_payload": frozen}
'''
    out = apply_contract_aware_v2(
        src,
        task_id="ce111_q02_polynomial_division_remainder",
        condition="ab2d_full_v2",
        cell_id="pass_synth",
        model_key="gemini",
    )
    assert out.source_modified is False
    assert out.proposed_repair_count == 0


def test_rewrite_messy_source_abstains():
    src = '''
def generate(level=1, **kwargs):
    frozen = {"quadratic_coefficients": [1,4,-12]}
    if True:
        
    elif False:
        pass
    return 1

def generate(level=1, **kwargs):
    return 2
'''
    out = apply_contract_aware_v2(
        src,
        task_id="ce115_calc_polynomial_factor_roots_l1",
        condition="ab2d_full_v2",
        cell_id="messy",
        model_key="qwen_9b",
    )
    # either not parseable path: all rules abstain; or parse fails per rule
    assert out.proposed_repair_count == 0
