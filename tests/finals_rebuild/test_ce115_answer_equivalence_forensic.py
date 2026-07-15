"""Milestone 4C — exact answer-equivalence helpers (no model calls)."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from scripts.ce115_answer_incorrect_forensic import (
    exact_numbers_equal,
    exact_sequence_equal,
    independent_equivalence,
)

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "docs/experiments/results/ce115_calc_local_confirmatory"
SMOKE = (
    RESULTS
    / "qwen3_5_4b__ce115_calc_exact_rational_expression_l1__ab2g__seed_2026071301_git_908033d34863.jsonl"
)
SMOKE_SHA = "137f05c3ddf21af06c71e1cea0431b106bcdaf82b844f2a2c328b9d0afb44e4d"


def test_fraction_vs_decimal_exact_equality():
    assert exact_numbers_equal("1/4", "0.25")
    assert exact_numbers_equal("0.250", "1/4")
    assert exact_numbers_equal("2/8", "1/4")
    assert exact_numbers_equal("-1/2", "-0.5")
    assert not exact_numbers_equal("1/3", "0.33")


def test_radical_symbolic_pair_equality():
    exp = {"coefficient": 2, "radicand": 2}
    # Same numbers, different types should still be exact-equal via Fraction path
    sub = {"coefficient": "2", "radicand": 2}
    verdict = independent_equivalence("radical_simplification", exp, sub)
    assert verdict["equivalent"] is True


def test_polynomial_quotient_remainder_equality():
    exp = {"quotient_coefficients": [1, "1/2"], "remainder_coefficients": ["3/2"]}
    sub = {"quotient_coefficients": ["1", "0.5"], "remainder_coefficients": [1.5]}
    # 1.5 float rejected → not equal (no float tolerance)
    bad = independent_equivalence("polynomial_division_general", exp, sub)
    assert bad["equivalent"] is False
    good_sub = {"quotient_coefficients": [1, "0.5"], "remainder_coefficients": ["3/2"]}
    good = independent_equivalence("polynomial_division_general", exp, good_sub)
    assert good["equivalent"] is True


def test_root_set_order_independence_and_multiplicity():
    exp = {"roots": ["-1/2", 3]}
    sub = {"roots": [3, "-0.5"]}
    assert independent_equivalence("polynomial_factor_roots", exp, sub)["equivalent"] is True
    # Multiplicity preserved: duplicate roots must match counts
    exp2 = {"roots": [2, 2]}
    sub2 = {"roots": [2]}
    assert independent_equivalence("polynomial_factor_roots", exp2, sub2)["equivalent"] is False
    assert exact_sequence_equal([2, "2"], [2, 2], sorted_ok=True)


def test_rational_expression_dict_equivalence():
    exp = {"value": "1/4"}
    sub = {"value": "0.25"}
    assert independent_equivalence("exact_rational_expression", exp, sub)["equivalent"] is True
    assert independent_equivalence("exact_rational_expression", exp, {"value": "1/5"})["equivalent"] is False


def test_observed_smoke_artifact_unmodified():
    assert SMOKE.is_file()
    digest = hashlib.sha256(SMOKE.read_bytes()).hexdigest()
    assert digest == SMOKE_SHA
    row = json.loads(SMOKE.read_text(encoding="utf-8").splitlines()[0])
    assert row["record_state"] == "executed"
    assert row["outcome"] == "schema_failure"


def test_answer_incorrect_count_still_sixteen():
    n = 0
    for path in RESULTS.glob("*.jsonl"):
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip() and json.loads(line).get("outcome") == "answer_incorrect":
                n += 1
    assert n == 16
