"""Math16 Domain API SSOT: registry ↔ runtime ↔ model-facing prompt."""
from __future__ import annotations

import json
import re
from fractions import Fraction

import pytest

from agent_tools.finals_rebuild.ce115_clean_incremental_ablation import (
    TASK_DOMAIN_APIS,
    build_condition_prompt,
    domain_section,
    extract_domain_section,
)
from agent_tools.finals_rebuild.domain_api_ssot import DOMAIN_API_SSOT, render_api_prompt_line
from agent_tools.finals_rebuild.math16_pool import frozen_for_prompt, load_pool_manifest
from core.prompts.domain_function_library import PolynomialOps

API_LINE = re.compile(
    r"^- `([^`]+)` \| import: `([^`]+)` \| signature: `([^`]+)` \| returns: (.+)$",
    re.M,
)


def _math16_tasks():
    return {t["task_id"]: t for t in load_pool_manifest()["tasks"]}


def test_factor_quadratic_exact_runtime_length_2_factor_dicts():
    factors = PolynomialOps.factor_quadratic_exact(1, 4, -12)
    assert isinstance(factors, list)
    assert len(factors) == 2
    for factor in factors:
        assert set(factor) == {"x_coefficient", "constant"}
        assert isinstance(factor["x_coefficient"], (int, str))
        assert isinstance(factor["constant"], (int, str))


def test_factor_quadratic_exact_correct_usage_yields_roots():
    factors = PolynomialOps.factor_quadratic_exact(1, 4, -12)
    roots = sorted(
        -Fraction(f["constant"]) / Fraction(f["x_coefficient"]) for f in factors
    )
    assert [int(r) for r in roots] == [-6, 2]


def test_wrong_3_value_unpack_is_impossible_against_runtime_contract():
    factors = PolynomialOps.factor_quadratic_exact(1, 4, -12)
    with pytest.raises(ValueError, match="not enough values to unpack"):
        _a, _b, _c = factors  # type: ignore[misc]


def test_prompt_factor_roots_matches_ssot_not_ambiguous_prose():
    tasks = _math16_tasks()
    task = tasks["ce115_calc_polynomial_factor_roots_l1"]
    prompt = build_condition_prompt("ab2d", task, frozen_for_prompt(task))
    domain = extract_domain_section(prompt)
    ssot_line = render_api_prompt_line("PolynomialOps.factor_quadratic_exact")
    assert ssot_line in domain
    assert "tuple of exact linear factors / roots" not in domain
    assert "list[dict, dict]" in domain
    assert "NOT a 3-tuple" in domain


def test_all_math16_ab2d_domain_apis_have_ssot_and_prompt_match():
    tasks = _math16_tasks()
    for tid, task in tasks.items():
        apis = TASK_DOMAIN_APIS[tid]
        for api in apis:
            assert api["name"] in DOMAIN_API_SSOT
        prompt = build_condition_prompt("ab2d", task, frozen_for_prompt(task))
        for name, _imp, sig, ret in API_LINE.findall(prompt):
            contract = DOMAIN_API_SSOT[name]
            assert sig == contract["signature"]
            assert ret.strip() == contract["returns_model_facing"]
            assert render_api_prompt_line(name) in prompt


def test_domain_section_equals_ssot_render():
    for tid in _math16_tasks():
        section = domain_section(tid)
        for api in TASK_DOMAIN_APIS[tid]:
            assert render_api_prompt_line(api["name"]) in section


def test_factor_return_json_roundtrip():
    factors = PolynomialOps.factor_quadratic_exact(1, 4, -12)
    again = json.loads(json.dumps(factors))
    assert again == factors
