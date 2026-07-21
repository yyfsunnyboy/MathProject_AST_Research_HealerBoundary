"""Compound-radical LaTeX presentation + Math16 failure taxonomy regressions."""
from __future__ import annotations

import json
from fractions import Fraction

from agent_tools.finals_rebuild.math_task_oracles import evaluate_math_task_oracle
from agent_tools.finals_rebuild.math16_oracles import (
    classify_math16_oracle_failure,
    display_latex_equivalent,
    evaluate_compound_radical_result,
)


Q10_PAYLOAD = {
    "larger_root": {
        "rational": 2,
        "radical_coefficient": 1,
        "radicand": 3,
        "canonical_latex": r"2+\sqrt{3}",
    },
    "smaller_root": {
        "rational": 2,
        "radical_coefficient": -1,
        "radicand": 3,
        "canonical_latex": r"2-\sqrt{3}",
    },
    "equation": "(x-2)^2=3",
    "order": "a>b",
    "target": "2a+b",
}


def test_compound_latex_whitespace_equivalent_does_not_veto():
    assert display_latex_equivalent(r"6+\sqrt{3}", r"6 + \sqrt{3}")
    assert display_latex_equivalent(r"6-\sqrt{3}", r"6 - \sqrt{3}")
    spaced = {
        "result": {
            "rational": 6,
            "radical_coefficient": 1,
            "radicand": 3,
            "canonical_latex": r"6 + \sqrt{3}",
        }
    }
    v = evaluate_compound_radical_result(Q10_PAYLOAD, spaced)
    assert v["structural_ok"] is True
    assert v["latex_ok"] is True
    assert v["is_correct"] is True


def test_wrong_radicand_and_coefficient_still_fail():
    bad_rad = {
        "result": {
            "rational": 6,
            "radical_coefficient": 1,
            "radicand": 5,
            "canonical_latex": r"6+\sqrt{3}",
        }
    }
    bad_coeff = {
        "result": {
            "rational": 6,
            "radical_coefficient": -1,
            "radicand": 3,
            "canonical_latex": r"6+\sqrt{3}",
        }
    }
    assert evaluate_compound_radical_result(Q10_PAYLOAD, bad_rad)["is_correct"] is False
    assert evaluate_compound_radical_result(Q10_PAYLOAD, bad_coeff)["is_correct"] is False


def test_tuple_like_wrong_radical_latex_is_presentation_only_q04_style():
    # After schema normalize: structure judges is_correct; wrong latex is presentation-only.
    payload = {"radicand": 135}
    submitted = {
        "coefficient": 3,
        "radicand": 15,
        "canonical_latex": r"\sqrt{(3, 15)}",
    }
    v = evaluate_math_task_oracle("radical_simplification_canonical", payload, submitted)
    assert v["structural_ok"] is True
    assert v["latex_ok"] is False
    assert v["is_correct"] is True
    assert classify_math16_oracle_failure(v) == "passed"


def test_positive_negative_coefficient_and_json_roundtrip():
    assert display_latex_equivalent(r"2+\sqrt{3}", r"2 + \sqrt{3}")
    assert display_latex_equivalent(r"2-\sqrt{3}", r"2 - \sqrt{3}")
    good = {
        "result": {
            "rational": Fraction(6, 1),
            "radical_coefficient": 1,
            "radicand": 3,
            "canonical_latex": r"6 + \sqrt{3}",
        }
    }
    # Oracle accepts Fraction rational; JSON channel normalizes separately.
    assert evaluate_math_task_oracle("compound_radical_result", Q10_PAYLOAD, good)[
        "is_correct"
    ]
    encoded = json.dumps(
        {
            "result": {
                "rational": 6,
                "radical_coefficient": 1,
                "radicand": 3,
                "canonical_latex": r"6 + \sqrt{3}",
            }
        },
        ensure_ascii=False,
    )
    loaded = json.loads(encoded)
    assert evaluate_math_task_oracle("compound_radical_result", Q10_PAYLOAD, loaded)[
        "is_correct"
    ]


def test_taxonomy_no_longer_maps_oracle_mismatch_to_intrinsic_safety():
    structural_fail = {
        "is_correct": False,
        "structural_ok": False,
        "latex_ok": True,
        "error": "structural_mismatch",
    }
    latex_fail = {
        "is_correct": False,
        "structural_ok": True,
        "latex_ok": False,
        "error": "radical_mismatch",
    }
    answer_fail = {
        "is_correct": False,
        "error": "answer_mismatch",
    }
    safety = {
        "is_correct": False,
        "error": "blocked_by_safety_policy",
    }
    assert classify_math16_oracle_failure(structural_fail) == "structural_mismatch"
    assert classify_math16_oracle_failure(latex_fail) == "latex_mismatch"
    assert classify_math16_oracle_failure(answer_fail) == "answer_incorrect"
    assert classify_math16_oracle_failure(safety) == "intrinsic_safety"
    assert classify_math16_oracle_failure({"is_correct": True}) == "passed"


def test_mislabel_cases_q08_style_answer_mismatch_not_intrinsic():
    # Historical mislabel: answer_mismatch was recorded as INTRINSIC_SAFETY.
    assert (
        classify_math16_oracle_failure(
            {"is_correct": False, "error": "answer_mismatch"}
        )
        == "answer_incorrect"
    )
    assert (
        classify_math16_oracle_failure(
            {
                "is_correct": False,
                "structural_ok": True,
                "latex_ok": False,
                "error": "structural_or_latex_mismatch",
            }
        )
        == "latex_mismatch"
    )
