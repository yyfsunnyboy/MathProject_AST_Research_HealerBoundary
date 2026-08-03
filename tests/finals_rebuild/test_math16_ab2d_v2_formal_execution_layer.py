# -*- coding: utf-8 -*-
"""Zero-model tests for Math16 Ab2d V2 formal execution layer."""
from __future__ import annotations

from pathlib import Path

import pytest

from agent_tools.finals_rebuild.math16_ab2d_v2_formal_execution import (
    CONDITION_ORDER,
    CONDITIONS,
    EXPERIMENT_ID,
    MODEL_ORDER,
    V1_FORBIDDEN_WRITE_PREFIXES,
    V2_ARTIFACT_ROOT,
    assert_path_is_v2_write_target,
    audit_cell_plan,
    formal_root,
    load_cell_manifest,
    run_model_condition,
    runner_path_inventory,
    write_preregistration,
    zero_model_preflight_480,
)

ROOT = Path(__file__).resolve().parents[2]


def test_six_runners_point_to_v2_prompts_and_artifact_root():
    inv = runner_path_inventory()
    assert len(inv) == 6
    for row in inv:
        assert row["condition"] in CONDITION_ORDER
        assert row["model_key"] in MODEL_ORDER
        assert row["prompt_dir"].startswith("docs/experiments/prompts/")
        # Strict V2 prompt dirs only (exact match; never V1).
        assert row["prompt_dir"] in {
            "docs/experiments/prompts/ab2d_domain_menu_v2/prompts",
            "docs/experiments/prompts/ab2d_full_v2/prompts",
        }
        assert not row["prompt_dir"].endswith("ab2d_domain_menu/prompts")
        assert not row["prompt_dir"].endswith("ab2d_full/prompts")
        assert row["formal_root"].startswith(
            "artifacts/math16_ab2d_menu_vs_full_runtime_contract_v2/formal/"
        )
        assert "math16_ab2d_domain_menu_v1" not in row["formal_root"]
        assert "math16_ab2d_full_domain_assisted_v1" not in row["formal_root"]
        assert row["artifact_experiment_root"] == (
            "artifacts/math16_ab2d_menu_vs_full_runtime_contract_v2"
        )


def test_script_runners_bind_v2_conditions_only():
    scripts = [
        "scripts/run_math16_ab2d_domain_menu_v2_gemini_formal.py",
        "scripts/run_math16_ab2d_domain_menu_v2_qwen9b_formal.py",
        "scripts/run_math16_ab2d_domain_menu_v2_qwen4b_formal.py",
        "scripts/run_math16_ab2d_full_v2_gemini_formal.py",
        "scripts/run_math16_ab2d_full_v2_qwen9b_formal.py",
        "scripts/run_math16_ab2d_full_v2_qwen4b_formal.py",
    ]
    for rel in scripts:
        text = (ROOT / rel).read_text(encoding="utf-8")
        assert "math16_ab2d_v2_formal_cli" in text
        assert "ab2d_domain_menu_v2" in text or "ab2d_full_v2" in text
        assert 'run_cli("ab2d_full"' not in text
        assert 'run_cli("ab2d_domain_menu"' not in text
        assert "derived_scaffolds_v1" not in text


def test_v1_paths_cannot_be_write_targets():
    with pytest.raises(RuntimeError, match="V1 path|V2 formal write"):
        assert_path_is_v2_write_target(
            ROOT / "artifacts/math16_ab2d_domain_menu_v1/formal/gemini"
        )
    with pytest.raises(RuntimeError, match="V1 path|V2 formal write"):
        assert_path_is_v2_write_target(
            ROOT / "artifacts/math16_ab2d_full_domain_assisted_v1/formal/qwen_9b"
        )
    # V2 root ok
    assert_path_is_v2_write_target(V2_ARTIFACT_ROOT / "formal" / "gemini" / "ab2d_full_v2")


def test_conditions_map_to_v2_only():
    assert set(CONDITIONS) == {"ab2d_domain_menu_v2", "ab2d_full_v2"}
    for cond, cfg in CONDITIONS.items():
        assert cfg["experiment_id"] == EXPERIMENT_ID
        assert cfg["prompt_dir"].name == "prompts"
        assert "_v2" in str(cfg["prompt_dir"])
        assert "derived_scaffolds_v1" not in str(cfg)


def test_rebuild_and_480_plan_dry_run_zero_model_calls():
    full = write_preregistration("ab2d_full_v2")
    menu = write_preregistration("ab2d_domain_menu_v2")
    assert full["n_cells"] == 240
    assert menu["n_cells"] == 240
    plan = audit_cell_plan(both_conditions=True)
    assert plan["total_cells"] == 480
    assert plan["unique_cells"] == 480
    assert plan["duplicate"] == 0
    assert plan["missing"] == 0
    assert plan["ok"] is True
    assert plan["model_calls"] == 0
    for model_key in MODEL_ORDER:
        for condition in CONDITION_ORDER:
            summary = run_model_condition(
                condition=condition, model_key=model_key, dry_run=True, execute_api=False
            )
            assert summary["model_calls"] == 0
            assert summary["planned"] == 80
            assert summary["experiment_id"] == EXPERIMENT_ID
            assert "ab2d" in summary["prompt_dir"] and "_v2" in summary["prompt_dir"]
            assert summary["formal_root"].startswith(
                "artifacts/math16_ab2d_menu_vs_full_runtime_contract_v2/formal/"
            )


def test_zero_model_preflight_v2():
    result = zero_model_preflight_480()
    assert result["model_calls"] == 0
    assert result["overall_pass"] is True
    assert result["n_v2_prompts"] == 32
    assert result["gemini_160_planned"] == 160
    assert result["qwen9b_160_planned"] == 160
    assert result["qwen4b_160_planned"] == 160
    assert result["scaffold_ssot"]["uses_v1_derived_scaffolds"] is False
    assert not result["sha_inventory_mismatches"]


def test_cell_ids_use_v2_conditions():
    write_preregistration("ab2d_domain_menu_v2")
    write_preregistration("ab2d_full_v2")
    for condition in CONDITION_ORDER:
        for cell in load_cell_manifest(condition)[:5]:
            assert cell["condition"] == condition
            assert cell["experiment_id"] == EXPERIMENT_ID
            assert f"__{condition}__" in cell["cell_id"]
            assert "derived_scaffolds_v1" not in str(cell)


def test_formal_root_layering_model_condition():
    for condition in CONDITION_ORDER:
        for model_key in MODEL_ORDER:
            root = formal_root(condition, model_key)
            rel = str(root.relative_to(ROOT)).replace("\\", "/")
            assert rel == (
                f"artifacts/math16_ab2d_menu_vs_full_runtime_contract_v2/formal/"
                f"{model_key}/{condition}"
            )
