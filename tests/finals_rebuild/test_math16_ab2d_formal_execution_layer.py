# -*- coding: utf-8 -*-
"""Zero-model tests for Math16 Ab2d formal execution layer."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from agent_tools.finals_rebuild.math16_ab2d_formal_execution import (
    EXECUTION_FREEZE_COMMIT,
    MATH16_MODEL_SETTINGS_REL,
    MODEL_ORDER,
    SEEDS,
    assert_prior_model_audit_passed,
    audit_cell_plan,
    load_cell_manifest,
    load_math16_model_settings,
    run_model_condition,
    write_preregistration,
    zero_model_preflight_480,
)

ROOT = Path(__file__).resolve().parents[2]


def test_math16_settings_not_ce115_defaults():
    settings = load_math16_model_settings()
    assert settings["seed_list"] == SEEDS
    # Qwen Math16 freeze uses 0.2 / 0.8 / 20 — not CE115 TEMPERATURE=0.0
    assert settings["models"]["qwen_9b"]["temperature"] == 0.2
    assert settings["models"]["qwen_9b"]["top_p"] == 0.8
    assert settings["models"]["qwen_9b"]["top_k"] == 20
    assert settings["models"]["qwen_4b"]["temperature"] == 0.2
    assert settings["models"]["gemini"]["temperature"] == 0.0
    assert settings["models"]["gemini"]["max_output_tokens"] == 24576
    assert settings["models"]["gemini"]["top_p"] == 1.0
    assert settings["models"]["gemini"]["top_k"] == 1
    assert settings["models"]["gemini"]["timeout_seconds"] == 600
    from agent_tools.finals_rebuild.math16_ab2d_formal_execution import (
        math16_gemini_generation_config,
    )

    gen = math16_gemini_generation_config(settings["models"]["gemini"])
    assert gen == {
        "temperature": 0.0,
        "max_output_tokens": 24576,
        "top_p": 1.0,
        "top_k": 1,
    }
    src = (ROOT / "agent_tools/finals_rebuild/math16_ab2d_formal_execution.py").read_text(
        encoding="utf-8"
    )
    assert "ce115_v4_gemini_transport" not in src
    assert "ce115_qwen_ollama_transport" not in src
    assert MATH16_MODEL_SETTINGS_REL in src
    qual_src = (
        ROOT / "agent_tools/finals_rebuild/math16_ab2d_gemini_topk_qualification.py"
    ).read_text(encoding="utf-8")
    assert "ce115_v4_gemini_transport" not in qual_src
    assert "math16_ab2d_formal_execution" in qual_src
    assert "math16_gemini_generation_config" in qual_src


def test_rebuild_manifests_and_480_plan():
    full = write_preregistration("ab2d_full")
    menu = write_preregistration("ab2d_domain_menu")
    assert full["n_cells"] == 240
    assert menu["n_cells"] == 240
    plan = audit_cell_plan(both_conditions=True)
    assert plan["total_cells"] == 480
    assert plan["unique_cells"] == 480
    assert plan["duplicate"] == 0
    assert plan["missing"] == 0
    assert plan["by_model"] == {"gemini": 160, "qwen_9b": 160, "qwen_4b": 160}
    assert plan["ok"] is True
    assert plan["model_calls"] == 0


def test_prompt_sha_matches_disk():
    write_preregistration("ab2d_full")
    write_preregistration("ab2d_domain_menu")
    for condition in ("ab2d_full", "ab2d_domain_menu"):
        for cell in load_cell_manifest(condition):
            path = (
                ROOT
                / (
                    "docs/experiments/prompts/ab2d_full/prompts"
                    if condition == "ab2d_full"
                    else "docs/experiments/prompts/ab2d_domain_menu/prompts"
                )
                / f"{cell['task_id']}.txt"
            )
            import hashlib

            disk = hashlib.sha256(path.read_bytes()).hexdigest()
            assert cell["prompt_sha256"] == disk
            assert cell["execution_freeze_commit"] == EXECUTION_FREEZE_COMMIT


def test_dry_run_zero_model_calls():
    write_preregistration("ab2d_full")
    write_preregistration("ab2d_domain_menu")
    for model_key in MODEL_ORDER:
        for condition in ("ab2d_domain_menu", "ab2d_full"):
            summary = run_model_condition(
                condition=condition, model_key=model_key, dry_run=True, execute_api=False
            )
            assert summary["model_calls"] == 0
            assert summary["planned"] == 80
            assert summary["parameter_authority"] == MATH16_MODEL_SETTINGS_REL


def test_sequential_gate_blocks_qwen_without_gemini():
    write_preregistration("ab2d_full")
    write_preregistration("ab2d_domain_menu")
    with pytest.raises(RuntimeError, match="SEQUENTIAL_GATE_BLOCKED"):
        assert_prior_model_audit_passed("qwen_9b")


def test_zero_model_preflight_480():
    result = zero_model_preflight_480()
    assert result["model_calls"] == 0
    assert result["overall_pass"] is True
    assert result["gemini_160_planned"] == 160
    assert result["qwen9b_160_planned"] == 160
    assert result["qwen4b_160_planned"] == 160
    assert result["parameter_authority"] == MATH16_MODEL_SETTINGS_REL


def test_domain_menu_execute_api_fail_closed_without_flag(capsys):
    # Invoking CLI without flags should error; without --execute-api no live path.
    from scripts.math16_ab2d_formal_cli import run_cli

    with pytest.raises(SystemExit):
        run_cli("ab2d_domain_menu", "gemini", [])
