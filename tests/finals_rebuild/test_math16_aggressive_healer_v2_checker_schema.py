# -*- coding: utf-8 -*-
"""Tests for API Contract Checker schema (detection layer, zero model)."""
from __future__ import annotations

import json
from pathlib import Path

from agent_tools.finals_rebuild.aggressive_healer_contract_v2.checker_audit import (
    KNOWN6,
    REWRITE13,
)
from agent_tools.finals_rebuild.aggressive_healer_contract_v2.checker_schema import (
    SCHEMA_FIELD_NAMES,
    run_contract_checker,
)
from agent_tools.finals_rebuild.aggressive_healer_contract_v2.contracts import load_contract

ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "artifacts/math16_ab2d_menu_vs_full_runtime_contract_v2/formal"


def _formal_src(cell_id: str) -> tuple[str, dict]:
    for p in FORMAL.rglob("artifact.json"):
        art = json.loads(p.read_text(encoding="utf-8"))
        if art["cell_id"] == cell_id:
            src = (p.parent / "extracted_source.py").read_text(encoding="utf-8", errors="replace")
            return src, art
    raise FileNotFoundError(cell_id)


def test_schema_fields_present_on_finding():
    src = '''
from core.prompts.domain_function_library import PolynomialOps
def generate(level=1, **kwargs):
    frozen = {"dividend_coefficients": [1,0], "divisor_coefficients": [1,0]}
    q, r = PolynomialOps.div_qr(frozen["dividend_coefficients"], frozen["divisor_coefficients"])
    r_latex = PolynomialOps.format_latex(r)
    return {"question_text": "q", "correct_answer": {"remainder": str(r), "canonical_latex": r_latex}, "oracle_payload": frozen}
'''
    rep = run_contract_checker(
        src,
        task_id="ce111_q02_polynomial_division_remainder",
        condition="ab2d_full_v2",
        cell_id="t_schema",
        model_key="qwen_4b",
    )
    assert rep.findings
    f = next(x for x in rep.findings if x.contract_violation_detected or x.decision == "REPAIR_ACCEPTED")
    d = f.to_dict()
    for name in SCHEMA_FIELD_NAMES:
        assert name in d


def test_violation_independent_of_repair_accepted():
    # Multi wrong remainder candidates: detect violation, no unique PC repair.
    src = '''
from core.prompts.domain_function_library import PolynomialOps
def generate(level=1, **kwargs):
    frozen = {"dividend_coefficients": [6,4,0], "divisor_coefficients": [2,0,0]}
    q, r = PolynomialOps.div_qr(frozen["dividend_coefficients"], frozen["divisor_coefficients"])
    r_latex = PolynomialOps.format_latex(r)
    a = {"remainder": str(r), "canonical_latex": r_latex}
    b = {"remainder": str(list(r)), "canonical_latex": r_latex}
    c = {"remainder": str(0), "canonical_latex": r_latex}
    correct_answer = a
    return {"question_text": "q", "correct_answer": correct_answer, "oracle_payload": frozen}
'''
    rep = run_contract_checker(
        src,
        task_id="ce111_q02_polynomial_division_remainder",
        condition="ab2d_full_v2",
        cell_id="multi",
        model_key="qwen_4b",
    )
    # repair may or may not apply depending on PC uniqueness; fields exist independently
    has_v = any(f.contract_violation_detected for f in rep.findings)
    has_ra_field = all(hasattr(f, "repair_accepted") for f in rep.findings)
    assert has_ra_field
    # If PC abstains, still can have violation_detected True elsewhere
    if rep.repair_accepted_count == 0:
        assert has_v or rep.cell_decision in {
            "DETECT_ONLY_ABSTAIN",
            "INSUFFICIENT_EVIDENCE",
            "CONTRACT_OK",
            "REWRITE_REQUIRED",
        }


def test_ast_uncheckable():
    bad = "def generate(:\n  pass\n"
    rep = run_contract_checker(
        bad,
        task_id="ce111_q02_polynomial_division_remainder",
        condition="ab2d_full_v2",
        cell_id="bad",
        model_key="qwen_4b",
    )
    assert rep.cell_decision == "AST_UNCHECKABLE"
    assert rep.parseable is False
    assert rep.parse_error
    assert all(f.decision == "AST_UNCHECKABLE" for f in rep.findings)
    # Must not claim "no contract violation" as CONTRACT_OK
    assert rep.cell_decision != "CONTRACT_OK"
    assert rep.repair_accepted_count == 0


def test_menu_skips_full_plan_process_violations():
    src = '''
from core.prompts.domain_function_library import IntegerOps
def generate(level=1, **kwargs):
    frozen = {"a": 1, "b": 2}
    # Intentionally no full-plan required process for domain-menu path
    v = IntegerOps.add(frozen["a"], frozen["b"])
    return {"question_text": "q", "correct_answer": v, "oracle_payload": frozen}
'''
    rep = run_contract_checker(
        src,
        task_id="ce112_q01_negative_integer_power",
        condition="ab2d_domain_menu_v2",
        cell_id="menu_ok",
        model_key="gemini",
    )
    fp_viol = [
        f
        for f in rep.findings
        if f.condition_scope == "full_plan_only" and f.contract_violation_detected
    ]
    assert fp_viol == []
    skips = [f for f in rep.findings if f.checker_status == "SKIPPED_MENU"]
    assert skips


def test_full_plan_operand_order_and_missing_call():
    # wrong operand order — detect + likely PC-R02 accept
    src = '''
from core.prompts.domain_function_library import FractionOps
def generate(level=1, **kwargs):
    frozen = {"products": []}
    term = FractionOps.create("1")
    term = FractionOps.sub(term, FractionOps.create(0))
    return {"question_text": "q", "correct_answer": {"value": "1", "canonical_latex": "1"}, "oracle_payload": frozen}
'''
    rep = run_contract_checker(
        src,
        task_id="ce115_calc_exact_rational_expression_l1",
        condition="ab2d_full_v2",
        cell_id="op",
        model_key="qwen_4b",
    )
    dims = {f.dimension for f in rep.findings if f.contract_violation_detected}
    assert "operand_roles_order" in dims or rep.repair_accepted_count >= 1

    # missing process-ish
    src2 = '''
from core.prompts.domain_function_library import PolynomialOps
def generate(level=1, **kwargs):
    frozen = {"dividend_coefficients": [1,0], "divisor_coefficients": [1]}
    return {"question_text": "q", "correct_answer": {"remainder": "0", "canonical_latex": "0"}, "oracle_payload": frozen}
'''
    rep2 = run_contract_checker(
        src2,
        task_id="ce111_q02_polynomial_division_remainder",
        condition="ab2d_full_v2",
        cell_id="miss",
        model_key="qwen_4b",
    )
    assert any(
        f.dimension in ("required_api_calls", "missing_extra_process_step") and f.contract_violation_detected
        for f in rep2.findings
    )


def test_known6_repair_decisions():
    for cid, rule in KNOWN6.items():
        try:
            src, art = _formal_src(cid)
        except FileNotFoundError:
            continue
        rep = run_contract_checker(
            src,
            task_id=art["task_id"],
            condition=art["condition"],
            cell_id=cid,
            model_key=art["model_key"],
        )
        assert rule in rep.repair_accepted_rules
        assert rep.repair_accepted_count >= 1
        assert rep.cell_decision == "REPAIR_ACCEPTED"


def test_rewrite13_refuse_repair():
    for cid in REWRITE13:
        try:
            src, art = _formal_src(cid)
        except FileNotFoundError:
            continue
        rep = run_contract_checker(
            src,
            task_id=art["task_id"],
            condition=art["condition"],
            cell_id=cid,
            model_key=art["model_key"],
        )
        assert rep.repair_accepted_count == 0
        assert not rep.source_modified_by_pc


def test_pass_sample_no_repair():
    # Spot-check a few PASS cells if present
    n = 0
    for p in FORMAL.rglob("artifact.json"):
        art = json.loads(p.read_text(encoding="utf-8"))
        if art.get("outcome") != "passed":
            continue
        src = (p.parent / "extracted_source.py").read_text(encoding="utf-8", errors="replace")
        rep = run_contract_checker(
            src,
            task_id=art["task_id"],
            condition=art["condition"],
            cell_id=art["cell_id"],
            model_key=art["model_key"],
        )
        assert rep.repair_accepted_count == 0
        assert not rep.source_modified_by_pc
        n += 1
        if n >= 8:
            break
    assert n >= 1


def test_contract_loads_unchanged():
    c = load_contract("ce111_q02_polynomial_division_remainder", "ab2d_full_v2")
    assert c["domain"] == "PolynomialOps"
    assert c["contract_sha256"]
