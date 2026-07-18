"""Compound-radical integer boundary: int and integer-valued Fraction."""
from __future__ import annotations

import json
from fractions import Fraction

import pytest

from agent_tools.finals_rebuild.math_task_oracles import evaluate_math_task_oracle
from agent_tools.finals_rebuild.math16_oracles import (
    coerce_exact_int,
    json_safe_default,
    normalize_compound_radical,
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


def test_fraction_integer_valued_coerces_positive_and_negative():
    assert coerce_exact_int(Fraction(6, 1), "rational") == 6
    assert coerce_exact_int(Fraction(-6, 1), "rational") == -6
    assert normalize_compound_radical(
        {"rational": Fraction(6, 1), "radical_coefficient": 1, "radicand": 3}
    ) == (6, 1, 3)
    assert normalize_compound_radical(
        {"rational": Fraction(-6, 1), "radical_coefficient": -1, "radicand": 3}
    ) == (-6, -1, 3)


def test_non_integral_fraction_rejected():
    with pytest.raises(ValueError, match="non-integral Fraction"):
        coerce_exact_int(Fraction(3, 2), "rational")
    with pytest.raises(ValueError):
        normalize_compound_radical(
            {"rational": Fraction(3, 2), "radical_coefficient": 1, "radicand": 3}
        )


def test_q10_payload_json_roundtrip_with_fraction_fields():
    answer = {
        "result": {
            "rational": Fraction(6, 1),
            "radical_coefficient": Fraction(1, 1),
            "radicand": 3,
            "canonical_latex": r"6+\sqrt{3}",
        }
    }
    encoded = json.dumps(answer, ensure_ascii=False, default=json_safe_default)
    loaded = json.loads(encoded)
    assert loaded["result"]["rational"] == 6
    assert loaded["result"]["radical_coefficient"] == 1
    assert isinstance(loaded["result"]["rational"], int)
    assert evaluate_math_task_oracle("compound_radical_result", Q10_PAYLOAD, loaded)[
        "is_correct"
    ]


def test_q10_correct_answer_still_passes():
    good = {
        "result": {
            "rational": 6,
            "radical_coefficient": 1,
            "radicand": 3,
            "canonical_latex": r"6+\sqrt{3}",
        }
    }
    assert evaluate_math_task_oracle("compound_radical_result", Q10_PAYLOAD, good)[
        "is_correct"
    ]
    via_fraction = {
        "result": {
            "rational": Fraction(6, 1),
            "radical_coefficient": 1,
            "radicand": 3,
            "canonical_latex": r"6+\sqrt{3}",
        }
    }
    assert evaluate_math_task_oracle(
        "compound_radical_result", Q10_PAYLOAD, via_fraction
    )["is_correct"]


def test_wrong_radicand_or_coefficient_still_fails():
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
    assert (
        evaluate_math_task_oracle("compound_radical_result", Q10_PAYLOAD, bad_rad)[
            "is_correct"
        ]
        is False
    )
    assert (
        evaluate_math_task_oracle("compound_radical_result", Q10_PAYLOAD, bad_coeff)[
            "is_correct"
        ]
        is False
    )


def test_json_safe_default_rejects_non_integral_fraction():
    with pytest.raises(TypeError, match="non-integer value"):
        json.dumps({"x": Fraction(3, 2)}, default=json_safe_default)
