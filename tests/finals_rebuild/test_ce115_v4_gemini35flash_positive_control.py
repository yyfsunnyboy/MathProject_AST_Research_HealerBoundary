"""Targeted tests for Gemini 3.5 Flash positive-control transport/redaction."""
from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from scripts.ce115_v4_formal_cohort import _render_formal_prompt, formal_plan
from scripts.ce115_v4_gemini_transport import (
    MODEL_ID,
    api_key_status,
    assert_no_key_leak,
    build_redacted_request,
)
from scripts.ce115_v4_gemini35flash_positive_control import (
    DEFAULT_OUT,
    EXPECTED_PROMPT_HASH,
    SOURCE_SEQUENCE,
    _transport_is_flask_free,
    build_run_plan,
    _source_edge_cell,
)


def test_model_id_is_exact():
    assert MODEL_ID == "gemini-3.5-flash"


def test_redacted_request_has_no_key_fields(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "super-secret-test-key-value-xyz")
    req = build_redacted_request("hello prompt", model=MODEL_ID)
    blob = json.dumps(req)
    assert "super-secret-test-key-value-xyz" not in blob
    assert "api_key" not in req
    assert req["api_key_source"] == "environment"
    assert req["api_key_present"] is True
    assert req["tools"] is None
    assert req["code_execution"] is False
    assert req["function_calling"] is False
    assert_no_key_leak(req)


def test_assert_no_key_leak_detects_value(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "leak-me-now-12345")
    with pytest.raises(AssertionError):
        assert_no_key_leak({"x": "leak-me-now-12345"})


def test_api_key_status_presence_only(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    st = api_key_status()
    assert st == {"api_key_source": "environment", "api_key_present": False}
    monkeypatch.setenv("GEMINI_API_KEY", "abc")
    st2 = api_key_status()
    assert st2["api_key_present"] is True
    assert "abc" not in json.dumps(st2)


def test_source_seq13_identity_matches_formal_plan():
    edge = _source_edge_cell()
    plan = formal_plan()
    expected = [c for c in plan["cells"] if c["sequence"] == SOURCE_SEQUENCE][0]
    assert edge["cell_id"] == expected["cell_id"]
    assert edge["task"] == "ce115_calc_polynomial_division_l1"
    assert edge["task_family"] == "polynomial"
    assert edge["seed"] == 2026071301
    assert edge["model"] == "qwen3.5:9b"


def test_positive_control_plan_is_single_cell_budget_one():
    plan = build_run_plan(DEFAULT_OUT)
    assert plan["run_id"].endswith("positive_control_02")
    assert plan["planned_cells"] == 1
    assert len(plan["cells"]) == 1
    cell = plan["cells"][0]
    assert cell["max_model_calls"] == 1
    assert cell["model"] == MODEL_ID
    assert "positive_control_02" in cell["cell_id"]
    assert all(int(cell[k]) == 0 for k in ("retry", "resume", "replacement", "replay", "repair", "healer"))
    assert cell["source_sequence"] == 13


def test_transport_does_not_import_flask():
    assert _transport_is_flask_free() is True
    src = Path(__file__).resolve().parents[2] / "scripts/ce115_v4_gemini_transport.py"
    text = src.read_text(encoding="utf8")
    assert "import flask" not in text
    assert "from flask" not in text
    assert "GoogleAIClient" not in text


def test_prompt_matches_source_artifact_contract():
    root = Path(__file__).resolve().parents[2]
    edge = _source_edge_cell()
    art = json.loads(
        (
            root
            / "docs/experiments/results/ce115_ab2d_assembly_v4_formal_run"
            / f"{edge['cell_id']}.artifact.json"
        ).read_text(encoding="utf8")
    )
    prompt, frozen = _render_formal_prompt(edge["task"], int(edge["seed"]))
    assert frozen == art["frozen_parameters"]
    assert prompt == art["exact_rendered_prompt"]
    import hashlib

    assert hashlib.sha256(prompt.encode()).hexdigest() == EXPECTED_PROMPT_HASH
    assert "Available Domain APIs" in prompt
    assert "Required APIs" not in prompt
    assert "MUST_CALL" not in prompt
    assert art["raw_model_response"] not in prompt
