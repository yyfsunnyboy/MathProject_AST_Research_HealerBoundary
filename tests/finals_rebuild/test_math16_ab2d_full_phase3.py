"""Math16 Ab2d+full Phase 3: API, scaffolds, prompts, isolation, zero-model preflight."""
from __future__ import annotations

import ast
import json
import re
from fractions import Fraction
from pathlib import Path

import pytest

from agent_tools.finals_rebuild.domain_api_ssot import validate_inventory
from agent_tools.finals_rebuild.math16_ab2d_full import (
    FORBIDDEN_ANSWER_KEYS,
    KIND,
    TASK_ALLOWED_APIS,
    assert_domain_isolation,
    build_ab2d_full_prompt,
    build_scaffold_map,
    estimate_tokens,
    extract_fenced_blocks,
    load_scaffold_map,
    markdown_fences_balanced,
    prompt_metrics,
    reference_assemble,
    run_zero_model_preflight,
    scaffold_for_task,
    validate_prompt_static,
    write_scaffold_artifacts,
)
from agent_tools.finals_rebuild.math16_pool import load_pool_manifest, tasks_by_id
from agent_tools.finals_rebuild.math_task_oracles import evaluate_math_task_oracle
from core.prompts.domain_function_library import IntegerOps, RadicalOps

ROOT = Path(__file__).resolve().parents[2]


def test_ssot_inventory_includes_new_apis():
    assert validate_inventory() == []
    assert hasattr(IntegerOps, "prime_factorization")
    assert hasattr(IntegerOps, "positive_divisors")
    assert hasattr(RadicalOps, "scale_linear_radical")
    assert hasattr(RadicalOps, "exact_integer")


def test_prime_factorization_happy_and_edges():
    assert IntegerOps.prime_factorization(12) == {2: 2, 3: 1}
    assert IntegerOps.prime_factorization(-12) == {2: 2, 3: 1}
    assert IntegerOps.prime_factorization(1) == {}
    assert IntegerOps.prime_factorization(-1) == {}
    with pytest.raises(ValueError):
        IntegerOps.prime_factorization(0)
    with pytest.raises(ValueError):
        IntegerOps.prime_factorization(True)  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        IntegerOps.prime_factorization(1.5)  # type: ignore[arg-type]


def test_positive_divisors_happy_and_edges():
    assert IntegerOps.positive_divisors(12) == [1, 2, 3, 4, 6, 12]
    assert IntegerOps.positive_divisors(7) == [1, 7]
    with pytest.raises(ValueError):
        IntegerOps.positive_divisors(0)
    with pytest.raises(ValueError):
        IntegerOps.positive_divisors(-3)
    with pytest.raises(ValueError):
        IntegerOps.positive_divisors(True)  # type: ignore[arg-type]


def test_linear_radical_scale_add_format_edges():
    term = {"rational": 1, "radical_coefficient": 1, "radicand": 2}
    assert RadicalOps.scale_linear_radical(term, 2) == {
        "rational": 2,
        "radical_coefficient": 2,
        "radicand": 2,
    }
    with pytest.raises(ValueError):
        RadicalOps.scale_linear_radical(term, 0)
    with pytest.raises(ValueError):
        RadicalOps.scale_linear_radical({"rational": 1, "radical_coefficient": 0, "radicand": 2}, 2)
    a = {"rational": 1, "radical_coefficient": 1, "radicand": 2}
    b = {"rational": 3, "radical_coefficient": -1, "radicand": 2}
    with pytest.raises(ValueError):
        RadicalOps.add_linear_radicals(a, b)
    added = RadicalOps.add_linear_radicals(
        {"rational": 1, "radical_coefficient": 2, "radicand": 2},
        {"rational": 3, "radical_coefficient": -1, "radicand": 2},
    )
    assert added == {"rational": 4, "radical_coefficient": 1, "radicand": 2}
    with pytest.raises(ValueError):
        RadicalOps.add_linear_radicals(a, {"rational": 1, "radical_coefficient": 1, "radicand": 3})
    assert RadicalOps.format_linear_radical({"rational": 1, "radical_coefficient": 1, "radicand": 2}) == r"1+\sqrt{2}"
    assert RadicalOps.format_linear_radical({"rational": 2, "radical_coefficient": -1, "radicand": 3}) == r"2-\sqrt{3}"


def test_exact_integer_only_int():
    assert RadicalOps.exact_integer(4) == 4
    assert RadicalOps.exact_integer(Fraction(4, 1)) == 4
    assert RadicalOps.exact_integer("4/1") == 4
    with pytest.raises(ValueError):
        RadicalOps.exact_integer(Fraction(3, 2))
    with pytest.raises(ValueError):
        RadicalOps.exact_integer("3/2")
    with pytest.raises(ValueError):
        RadicalOps.exact_integer(True)  # type: ignore[arg-type]


def test_scaffold_map_schema_and_no_answers():
    write_scaffold_artifacts(ROOT)
    data = load_scaffold_map(ROOT)
    assert data["kind"] == KIND
    assert set(data["tasks"]) == {
        "ce111_q05_exact_fraction_expression",
        "ce113_q01_negative_fraction_subtraction",
        "ce111_q10_ordered_quadratic_roots_radical",
        "ce113_q11_rationalize_denominator",
    }
    blob = json.dumps(data)
    json.loads(blob)
    for tid, row in data["tasks"].items():
        assert row["kind"] == KIND
        flat = json.dumps(row["structure"])
        for key in FORBIDDEN_ANSWER_KEYS:
            # structural keys like numerator in leaves are num/den, not forbidden names
            assert f'"{key}"' not in flat
        assert "no_answer_proof" in row


def test_scaffold_source_consistency_with_frozen():
    tasks = tasks_by_id(ROOT)
    t11 = tasks["ce111_q05_exact_fraction_expression"]
    assert "9/22" in t11["frozen_params"]["expression"]
    tree = scaffold_for_task("ce111_q05_exact_fraction_expression", ROOT)
    assert tree["left"]["left"] == {"num": 9, "den": 22}
    t16 = tasks["ce113_q11_rationalize_denominator"]
    assert t16["frozen_params"]["radicand"] == 7
    den = scaffold_for_task("ce113_q11_rationalize_denominator", ROOT)
    assert den == {"denom_rational": 4, "denom_radical_coeff": -1, "radicand": 7}
    t15 = scaffold_for_task("ce111_q10_ordered_quadratic_roots_radical", ROOT)
    assert t15["equation_form"] == "shifted_square"
    assert "result" not in t15


def test_prompts_unique_budget_isolation_and_payload_rule():
    write_scaffold_artifacts(ROOT)
    tasks = tasks_by_id(ROOT)
    hashes = set()
    for tid, task in tasks.items():
        prompt = build_ab2d_full_prompt(task, ROOT)
        hashes.add(prompt)
        metrics = prompt_metrics(prompt, task, ROOT)
        assert metrics["within_common_budget"]
        assert metrics["within_task_budget"]
        assert metrics["within_total_budget"]
        assert metrics["has_derived_scaffold"] is False
        assert metrics["has_processing_steps"] is True
        assert "derived_scaffold" not in prompt.lower()
        assert validate_prompt_static(prompt, task["domain_ops"]) == []
        assert_domain_isolation(prompt, task["domain_ops"])
        assert markdown_fences_balanced(prompt)
        for lang, body in extract_fenced_blocks(prompt):
            if lang == "python":
                ast.parse(body)
        # frozen echo contract text present; no audit payload dump
        assert '"oracle_payload"' in prompt or "oracle_payload" in prompt
        # key fields from frozen appear
        for key in task["frozen_params"]:
            assert key in prompt
        assert task["oracle_payload"] == task["oracle_payload"]
        # must not embed audit-only answer fields when they differ from frozen
        if task["frozen_params"] != task["oracle_payload"]:
            audit = json.dumps(task["oracle_payload"], ensure_ascii=False)
            assert audit not in prompt
        # Do not embed labeled manifest answers; bare ints may appear in stems.
        ca = task["correct_answer"]
        if isinstance(ca, dict):
            assert json.dumps(ca, ensure_ascii=False) not in prompt
        elif isinstance(ca, int):
            assert f'"correct_answer": {ca}' not in prompt
            assert f"correct_answer = {ca}" not in prompt
        for api in TASK_ALLOWED_APIS[tid]:
            assert api in prompt or tid == "ce112_q01_negative_integer_power"
    assert len(hashes) == 16


def test_full_plan_domain_api_block_matches_domain_menu():
    from agent_tools.finals_rebuild.math16_ab2d_domain_menu import (
        build_domain_menu_prompt,
        extract_domain_api_block,
        extract_task_specific_answer_contract_block,
        load_domain_template,
    )

    tasks = tasks_by_id(ROOT)
    for tid, task in tasks.items():
        domain = task["domain_ops"]
        menu = build_domain_menu_prompt(task, load_domain_template(domain, ROOT))
        full = build_ab2d_full_prompt(task, ROOT)
        assert extract_domain_api_block(menu) == extract_domain_api_block(full)
        assert extract_task_specific_answer_contract_block(menu) == (
            extract_task_specific_answer_contract_block(full)
        )
        # Sole prompt-level delta is Processing steps (and trailing content after base).
        assert full.startswith(menu.rstrip())
        assert "## Processing steps" in full[len(menu.rstrip()) :]
        assert "derived_scaffold" not in full.lower()
        steps = full[len(menu.rstrip()) :]
        assert "Assemble correct_answer exactly according to the Answer contract." in steps
        for banned in (
            'Return {"count"',
            'return {"k"',
            "Return bare int",
            "Pack coefficient/radicand",
            "Return numerator/denominator",
            "final bare answer",
            "nested or flat result dict",
        ):
            assert banned not in steps


def test_generic_example_marked_non_normative():
    from agent_tools.finals_rebuild.math16_ab2d_domain_menu import build_domain_template

    for domain in ("IntegerOps", "FractionOps", "RadicalOps", "PolynomialOps"):
        text = build_domain_template(domain)
        assert "ILLUSTRATIVE ONLY" in text
        assert "NOT the answer" in text or "NOT normative" in text or "NOT the answer contract" in text
        assert "to_exact serializes Fraction values" in text or domain != "FractionOps"


def test_reference_assembly_matches_evaluator_all_tasks():
    write_scaffold_artifacts(ROOT)
    tasks = tasks_by_id(ROOT)
    for tid, task in tasks.items():
        out = reference_assemble(task, ROOT)["output"]
        assert out["oracle_payload"] == task["frozen_params"]
        assert set(out) == {"question_text", "correct_answer", "oracle_payload"}
        verdict = evaluate_math_task_oracle(task["oracle_type"], task["oracle_payload"], out["correct_answer"])
        assert verdict["is_correct"], (tid, verdict)


def test_zero_model_preflight_overall_pass():
    summary = run_zero_model_preflight(ROOT)
    assert summary["n_tasks"] == 16
    assert summary["all_evaluator_pass"] is True
    assert summary["all_static_clean"] is True
    assert summary["all_budget_ok"] is True
    assert summary["overall_pass"] is True
    assert Path(ROOT / "docs/experiments/prompts/ab2d_full/derived_scaffolds_v1.json").is_file()
    assert Path(ROOT / "docs/experiments/results/math16_ab2d_full_phase3_preflight_v1/summary.json").is_file()


def test_token_estimate_method_documented():
    assert estimate_tokens("abcd") == 1
    assert estimate_tokens("a" * 8) == 2
