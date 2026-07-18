"""Math16-LaTeX-v1: contracts, oracles, LaTeX/G6, compound radical, no-model preflight."""
from __future__ import annotations

import json
from pathlib import Path

from agent_tools.finals_rebuild.ce115_clean_incremental_ablation import (
    DOMAIN_BUDGET,
    TASK_DOMAIN_APIS,
    assert_clean_ablation_invariants,
    build_condition_prompt,
    domain_section,
)
from agent_tools.finals_rebuild.generator_success import evaluate_math_notation
from agent_tools.finals_rebuild.math16_oracles import (
    normalize_compound_radical,
)
from agent_tools.finals_rebuild.math16_pool import (
    POOL_ID,
    SEED,
    build_pool_manifest,
    frozen_for_prompt,
    write_pool_manifest,
)
from agent_tools.finals_rebuild.math16_preflight import run_math16_preflight
from agent_tools.finals_rebuild.math_answer_contracts import CONTRACTS, render_answer_contract
from agent_tools.finals_rebuild.math_task_oracles import evaluate_math_task_oracle
from agent_tools.finals_rebuild.math_task_sampler import sample_task_parameters

ROOT = Path(__file__).resolve().parents[2]


def _tasks():
    return build_pool_manifest()["tasks"]


def test_pool_distribution_and_identities():
    manifest = build_pool_manifest()
    assert manifest["pool_id"] == POOL_ID
    assert len(manifest["tasks"]) == 16
    assert manifest["domain_ops_distribution"] == {
        "PolynomialOps": 4,
        "IntegerOps": 4,
        "FractionOps": 4,
        "RadicalOps": 4,
    }
    assert all(t.get("year_source") != "114" for t in manifest["tasks"])
    assert all(
        t["presentation_transform"]
        == {
            "type": "semantic_equivalent_latex_standardization",
            "changes_semantics": False,
        }
        for t in manifest["tasks"]
    )


def test_existing4_source_vs_math16_latex():
    by_id = {t["task_id"]: t for t in _tasks()}
    poly = by_id["ce115_calc_polynomial_division_l1"]
    assert "Divide (6x^2 + 6)" in poly["source_question_text"]
    assert r"\[" in poly["math16_question_text"]
    assert "6x^2+6" in poly["math16_question_text"]
    assert poly["correct_answer"]["quotient_coefficients"] == [6, 24]
    assert poly["correct_answer"]["quotient_latex"] == "6x+24"

    roots = by_id["ce115_calc_polynomial_factor_roots_l1"]
    assert "x^2 + 4x - 12" in roots["source_question_text"]
    assert r"x^2+4x-12=0" in roots["math16_question_text"]
    assert roots["correct_answer"]["roots"] == [-6, 2]

    rational = by_id["ce115_calc_exact_rational_expression_l1"]
    assert r"\times" in rational["math16_question_text"]
    assert rational["correct_answer"]["canonical_latex"] == r"\frac{2679}{10}"

    radical = by_id["ce115_calc_radical_simplification_l1"]
    assert r"\sqrt{27}" in radical["math16_question_text"]
    assert radical["correct_answer"]["canonical_latex"] == r"3\sqrt{3}"


def test_all_math16_stems_pass_g6_and_have_latex():
    for task in _tasks():
        text = task["math16_question_text"]
        assert r"\(" in text or r"\[" in text
        gate = evaluate_math_notation(text)
        assert gate["status"] == "PASS", (task["task_id"], gate)


def test_oracle_golden_and_contracts():
    for task in _tasks():
        assert task["oracle_type"] in CONTRACTS
        render_answer_contract(task, task["frozen_params"])
        sampled = sample_task_parameters(
            {
                "task_id": task["task_id"],
                "domain": task["domain"],
                "skill_id": task["skill_id"],
                "oracle_type": task["oracle_type"],
                "difficulty_level": 1,
                "parameter_ranges": task["parameter_ranges"],
            },
            SEED,
        )
        assert sampled["oracle_payload"] == task["frozen_params"]
        verdict = evaluate_math_task_oracle(
            task["oracle_type"], task["oracle_payload"], task["correct_answer"]
        )
        assert verdict["is_correct"] is True, (task["task_id"], verdict)


def test_q08_strict_order_and_rejects_legacy():
    task = next(t for t in _tasks() if t["task_id"] == "ce111_q08_polynomial_factor_parameter_recovery")
    assert task["factor_order_policy"] == "strict_source_template"
    assert task["oracle_payload"]["a"] == 2
    assert task["oracle_payload"]["b"] == 13
    assert task["oracle_payload"]["c"] == -7
    assert task["correct_answer"] == -12
    assert evaluate_math_task_oracle(
        task["oracle_type"], task["oracle_payload"], 12
    )["is_correct"] is False
    assert evaluate_math_task_oracle(
        task["oracle_type"],
        task["oracle_payload"],
        {"a": -2, "c": 7, "answer": 12},
    )["is_correct"] is False


def test_q12_substantial_abstraction_provenance():
    task = next(t for t in _tasks() if t["task_id"] == "ce112_q12_independent_probability_fraction")
    assert task["provenance"]["transformation_level"] == "substantial_abstraction"
    assert task["provenance"]["difficulty_equivalence_to_original_exam"] is False


def test_q11_rerun_policy():
    task = next(t for t in _tasks() if t["task_id"] == "ce113_q11_rationalize_denominator")
    assert task["reuse_policy"] == "rerun"
    assert task["provenance"]["historical_v2_reference_only"] is True


def test_compound_radical_pos_neg_nested_json_roundtrip():
    task = next(t for t in _tasks() if t["task_id"] == "ce111_q10_ordered_quadratic_roots_radical")
    assert normalize_compound_radical(task["oracle_payload"]["larger_root"])[1] == 1
    assert normalize_compound_radical(task["oracle_payload"]["smaller_root"])[1] == -1
    ok = evaluate_math_task_oracle(
        "compound_radical_result", task["oracle_payload"], task["correct_answer"]
    )
    assert ok["is_correct"] is True
    # Wrong sign must fail (not string-only compare).
    bad = evaluate_math_task_oracle(
        "compound_radical_result",
        task["oracle_payload"],
        {
            "result": {
                "rational": 6,
                "radical_coefficient": -1,
                "radicand": 3,
                "canonical_latex": r"6+\sqrt{3}",
            }
        },
    )
    assert bad["is_correct"] is False
    nested = json.loads(json.dumps(task["oracle_payload"]))
    assert evaluate_math_task_oracle(
        "compound_radical_result", nested, task["correct_answer"]
    )["is_correct"] is True
    # Structure-only acceptance when latex omitted.
    structural_only = {
        "result": {"rational": 6, "radical_coefficient": 1, "radicand": 3}
    }
    assert evaluate_math_task_oracle(
        "compound_radical_result", task["oracle_payload"], structural_only
    )["is_correct"] is True


def test_remainder_only_does_not_score_quotient():
    task = next(t for t in _tasks() if t["task_id"] == "ce111_q02_polynomial_division_remainder")
    assert "quotient" not in task["correct_answer"]
    assert "quotient" in task["oracle_payload"]
    assert evaluate_math_task_oracle(
        task["oracle_type"], task["oracle_payload"], {"remainder": "4x", "canonical_latex": "4x"}
    )["is_correct"] is True
    assert evaluate_math_task_oracle(
        task["oracle_type"], task["oracle_payload"], {"quotient": 3}
    )["is_correct"] is False


def test_prompt_freeze_has_no_answer_leak_for_q08():
    task = next(t for t in _tasks() if t["task_id"] == "ce111_q08_polynomial_factor_parameter_recovery")
    frozen = frozen_for_prompt(task)
    blob = json.dumps(frozen["oracle_payload"], sort_keys=True)
    assert '"a": 2' not in blob
    assert '"c": -7' not in blob
    assert "strict_source_template" in blob
    for condition in ("ab1", "ab2g", "ab2d"):
        prompt = build_condition_prompt(condition, task, frozen)
        assert "a+2c" in prompt or "a+2c" in task["math16_question_text"]
        assert '"a": 2' not in prompt
        assert "answer=-12" not in prompt


def test_domain_apis_and_ablation_invariants():
    for task in _tasks():
        tid = task["task_id"]
        assert tid in TASK_DOMAIN_APIS
        section = domain_section(tid)
        assert DOMAIN_BUDGET[0] <= len(section) <= DOMAIN_BUDGET[1]
        prompts = assert_clean_ablation_invariants(task, frozen_for_prompt(task))
        assert set(prompts) == {"ab1", "ab2g", "ab2d"}
        assert "PolynomialOps" not in prompts["ab1"]
        assert "## Clean-incremental GENERIC" in prompts["ab2g"]
        assert "## Clean-incremental DOMAIN" in prompts["ab2d"]


def test_frac_sqrt_exponent_coverage_in_stems():
    texts = "\n".join(t["math16_question_text"] for t in _tasks())
    assert r"\frac" in texts
    assert r"\sqrt" in texts
    assert "^" in texts or r"^" in texts
    assert "x^2" in texts or r"x^2" in texts


def test_json_escaping_roundtrip_manifest():
    manifest = write_pool_manifest(ROOT)
    path = ROOT / "docs/experiments/manifests/math16_latex_v1_pool_manifest.json"
    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert loaded["manifest_content_sha256"] == manifest["manifest_content_sha256"]
    for task in loaded["tasks"]:
        again = json.loads(json.dumps(task, ensure_ascii=False))
        assert again["math16_question_text"] == task["math16_question_text"]
        assert again["correct_answer"] == task["correct_answer"]


def test_no_model_preflight_passes():
    report = run_math16_preflight(write_manifest=True)
    assert report["passed"] is True, report
    assert report["checks"]["prompt_cells_48"] is True
    assert report["gemini_live_run"] == "blocked_until_explicit_go"
