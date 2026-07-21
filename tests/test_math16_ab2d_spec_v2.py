# -*- coding: utf-8 -*-
"""Completeness / freeze tests for Math16 ab2d_spec_v2."""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FROZEN_FIRST4 = {
    "ce111_q05_exact_fraction_expression": "927977168ad6a72c644641fed7ef653495e55279689dc0beb06253033242926d",
    "ce112_q12_independent_probability_fraction": "183c3a708e2a1361e9ccd41de1cb33c51bb169b1f6b7cd99d874f98aa23ada51",
    "ce113_q01_negative_fraction_subtraction": "319926943ccbc9ca260979e04cf024cc1d896f00bc3e6be23e7b9632170ca54a",
    "ce111_q08_polynomial_factor_parameter_recovery": "4e8f345ad99e87317c2bb38ce741268ce4f57d9e2ca98518eea4f37fb36fb477",
}


def _sha_lf(path: Path) -> str:
    return hashlib.sha256(path.read_text(encoding="utf-8").replace("\r\n", "\n").encode()).hexdigest()


def test_first4_prompts_immutable():
    for tid, expected in FROZEN_FIRST4.items():
        path = ROOT / "docs/experiments/prompts/ab2d_spec_v2/prompts" / f"{tid}.txt"
        assert path.exists()
        assert _sha_lf(path) == expected


def test_q02_v2_has_format_latex_not_to_latex_helper():
    path = ROOT / "docs/experiments/prompts/ab2d_spec_v2/prompts/ce111_q02_polynomial_division_remainder.txt"
    text = path.read_text(encoding="utf-8")
    assert "PolynomialOps.format_latex" in text
    assert "(coeffs, var='x')" in text or '(coeffs, var="x")' in text or "var='x'" in text
    assert "to_latex" in text  # prohibition text
    assert "API-only" in text or "Only import the specified Domain API" in text


def test_v2_manifest_includes_five_tasks_and_policies():
    manifest = json.loads(
        (ROOT / "docs/experiments/prompts/ab2d_spec_v2/manifest.json").read_text(encoding="utf-8")
    )
    ids = [t["task_id"] for t in manifest["tasks"]]
    assert set(FROZEN_FIRST4) <= set(ids)
    assert "ce111_q02_polynomial_division_remainder" in ids
    by = {t["task_id"]: t for t in manifest["tasks"]}
    assert by["ce111_q02_polynomial_division_remainder"]["api_policy"] == "API-only"
    assert by["ce111_q08_polynomial_factor_parameter_recovery"]["api_policy"] == "native-only"
    for tid in (
        "ce111_q05_exact_fraction_expression",
        "ce112_q12_independent_probability_fraction",
        "ce113_q01_negative_fraction_subtraction",
    ):
        assert by[tid]["api_policy"] == "API-only"


def test_original_20cell_plan_geometry():
    plan = json.loads(
        (ROOT / "docs/experiments/manifests/math16_pilot02_ab2d_spec_v2_generation_plan.json").read_text(
            encoding="utf-8"
        )
    )
    assert len(plan) == 20
    assert len({c["cell_id"] for c in plan}) == 20
    assert Counter(c["task_id"] for c in plan) == {tid: 5 for tid in FROZEN_FIRST4}


def test_q02_patch_plan_two_seeds():
    plan = json.loads(
        (ROOT / "docs/experiments/manifests/math16_pilot02_ab2d_spec_v2_q02_patch_plan.json").read_text(
            encoding="utf-8"
        )
    )
    assert len(plan) == 2
    assert {c["seed"] for c in plan} == {2026071301, 2026072003}
    assert all(c["task_id"] == "ce111_q02_polynomial_division_remainder" for c in plan)


def test_q02_patch_eval_both_pass():
    summary = json.loads(
        (
            ROOT
            / "docs/experiments/results/math16_pilot02_ab2d_spec_v2_q02_patch_evaluation_r001/summary.json"
        ).read_text(encoding="utf-8")
    )
    assert summary["q02_v2_patched2_pass"] == "2/2"
    assert summary["global_recompute"]["ab2d_spec_hybrid_after_q02_pass_per_80"] == 80
    assert summary["global_recompute"]["overall_after_q02_per_320"] == 306
