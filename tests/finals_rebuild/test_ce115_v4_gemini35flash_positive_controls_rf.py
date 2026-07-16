"""Targeted tests for Gemini radical/fraction positive-control runner."""
from __future__ import annotations

import hashlib
from pathlib import Path

from scripts.ce115_v4_formal_cohort import _render_formal_prompt
from scripts.ce115_v4_gemini_transport import MODEL_ID
from scripts.ce115_v4_gemini35flash_positive_controls_rf import (
    DEFAULT_OUT,
    FIXED_CELLS,
    _source_edge,
    _transport_is_flask_free,
    build_run_plan,
)


def test_fixed_identities_match_formal_plan():
    for spec in FIXED_CELLS:
        edge, art = _source_edge(spec)
        assert edge["cell_id"] == spec["expected_cell_id"]
        assert edge["task_family"] == spec["task_family"]
        assert int(edge["seed"]) == 2026071301
        assert art["evaluator_verdict"] == "EXECUTION_FAILURE"


def test_run_plan_two_cells_budget_two():
    plan = build_run_plan(DEFAULT_OUT)
    assert plan["planned_cells"] == 2
    assert plan["model_calls_planned"] == 2
    assert {c["key"] for c in plan["cells"]} == {"radical", "fraction"}
    assert all(c["model"] == MODEL_ID for c in plan["cells"])
    assert all(c["max_model_calls"] == 1 for c in plan["cells"])
    assert all(
        all(int(c[k]) == 0 for k in ("retry", "resume", "replacement", "replay", "repair", "healer"))
        for c in plan["cells"]
    )


def test_prompts_match_source_artifacts_and_contract():
    root = Path(__file__).resolve().parents[2]
    for spec in FIXED_CELLS:
        edge, art = _source_edge(spec)
        prompt, frozen = _render_formal_prompt(edge["task"], int(edge["seed"]))
        assert frozen == art["frozen_parameters"]
        assert prompt == art["exact_rendered_prompt"]
        assert hashlib.sha256(prompt.encode()).hexdigest() == art["hashes"]["prompt"]
        assert "Available Domain APIs" in prompt
        assert "Required APIs" not in prompt
        assert "MUST_CALL" not in prompt
        assert art["raw_model_response"] not in prompt
        assert (root / "docs/experiments/results/ce115_ab2d_assembly_v4_formal_run").is_dir()


def test_transport_flask_free():
    assert _transport_is_flask_free() is True
