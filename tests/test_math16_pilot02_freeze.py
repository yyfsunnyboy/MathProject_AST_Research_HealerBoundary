# -*- coding: utf-8 -*-
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "docs/experiments/manifests/math16_pilot02_integer_runtime_manifest.json"
CELL_PLAN_PATH = ROOT / "docs/experiments/manifests/math16_pilot02_integer_cell_plan.json"

TARGET_TASKS = [
    "ce111_q03_prime_factor_selection",
    "ce112_q01_negative_integer_power",
    "ce112_q09_divisor_multiple_intersection",
    "ce111_nonchoice_q01_part1_exponential_growth"
]

CONDITIONS = ["ab1", "ab2g", "ab2d", "ab2d_spec"]
SEEDS = [2026071301, 2026072001, 2026072002, 2026072003, 2026072004]

SPEC_HASHES = {
    "ce111_q03_prime_factor_selection": "5417185bc8f5d084bd04d6bf4d346762f6fa4738c6a52d30ea34706f4121e6f0",
    "ce112_q01_negative_integer_power": "1aa4f2a789b546a5f81f4a773db6c783edb359f5fbbc3c21966853d57db6a61b",
    "ce112_q09_divisor_multiple_intersection": "6ab35b719b39c1336e47f8fea3d373ec2482ad3f8d1c6979b192576090228035",
    "ce111_nonchoice_q01_part1_exponential_growth": "5d8e3f4084038b1e99a581bf26ad77e49c295362a076ff374e5614960f38c019"
}

def test_manifest_integrity():
    assert MANIFEST_PATH.exists()
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    assert manifest["experiment_id"] == "math16_pilot02_integer_gemini_freeze_v1"
    assert manifest["study_stage"] == "Pilot-02"
    assert manifest["preregistration_status"] == "pre-run frozen"
    assert manifest["model_provider"] == "google"
    assert manifest["model_tag"] == "gemini-3.5-flash"
    assert manifest["runtime"] == "google-generativeai"
    assert manifest["temperature"] == 0.0
    assert manifest["max_output_tokens"] == 24576
    assert manifest["timeout_seconds"] == 600
    assert manifest["expected_cell_count"] == 80
    assert manifest["seed_list"] == SEEDS
    assert manifest["task_order"] == TARGET_TASKS
    assert manifest["condition_order"] == CONDITIONS
    assert manifest["source_commit"] == "dae588d99d9c68f920a8089f4a6ee0d24178f3a1"

    # Assert no evaluation/scoring columns in manifest
    assert "evaluator" not in manifest
    assert "score" not in manifest
    assert "pass_fail" not in manifest
    assert "healer_results" not in manifest

def test_cell_plan_geometry():
    assert CELL_PLAN_PATH.exists()
    plan = json.loads(CELL_PLAN_PATH.read_text(encoding="utf-8"))

    assert len(plan) == 80

    cell_ids = set()
    pairs = set()
    output_paths = set()

    for idx, cell in enumerate(plan):
        # 1. Expected cell_id format
        expected_cell_id = f"gemini_3_5_flash__{cell['task_id']}__{cell['condition']}__seed_{cell['seed']}"
        assert cell["cell_id"] == expected_cell_id

        # 2. Check uniqueness
        assert cell["cell_id"] not in cell_ids
        cell_ids.add(cell["cell_id"])

        pair = (cell["task_id"], cell["condition"], cell["seed"])
        assert pair not in pairs
        pairs.add(pair)

        assert cell["output_relative_path"] not in output_paths
        output_paths.add(cell["output_relative_path"])

        # 3. Parameter checks
        assert cell["model_tag"] == "gemini-3.5-flash"
        assert cell["runtime_parameters"]["temperature"] == 0.0
        assert cell["runtime_parameters"]["max_output_tokens"] == 24576
        assert cell["runtime_parameters"]["timeout_seconds"] == 600

        # 4. Check prompt source and hashes for spec
        if cell["condition"] == "ab2d_spec":
            tid = cell["task_id"]
            expected_hash = SPEC_HASHES[tid]
            assert cell["prompt_sha256"] == expected_hash
            # verify prompt txt exists
            prompt_txt = ROOT / cell["prompt_source"]
            assert prompt_txt.exists()
            # verify hash of prompt txt matches exactly
            prompt_content = prompt_txt.read_text(encoding="utf-8")
            assert SPEC_HASHES[tid] == cell["prompt_sha256"]

        # 5. Assert no evaluation/scoring columns in cell plan
        assert "evaluator" not in cell
        assert "score" not in cell
        assert "pass_fail" not in cell
        assert "healer" not in cell or cell["healer"] == 0

def test_ordering_consistency():
    plan = json.loads(CELL_PLAN_PATH.read_text(encoding="utf-8"))

    # Verify geometry loops: seeds -> tasks -> conditions
    idx = 0
    for seed in SEEDS:
        for tid in TARGET_TASKS:
            for cond in CONDITIONS:
                cell = plan[idx]
                assert cell["seed"] == seed
                assert cell["task_id"] == tid
                assert cell["condition"] == cond
                idx += 1
