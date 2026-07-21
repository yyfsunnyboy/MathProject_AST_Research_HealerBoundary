# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import hashlib
from pathlib import Path
import pytest
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

MANIFEST_SPEC_PATH = ROOT / "docs/experiments/prompts/ab2d_spec/manifest.json"
MANIFEST_PATH = ROOT / "docs/experiments/manifests/math16_pilot02_full_runtime_manifest.json"
CELL_PLAN_PATH = ROOT / "docs/experiments/manifests/math16_pilot02_full_generation_plan.json"
INVENTORY_PATH = ROOT / "docs/experiments/manifests/math16_pilot02_full_analysis_inventory.json"

def get_file_sha256(path: Path) -> str:
    content = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    return hashlib.sha256(content.encode("utf-8")).hexdigest()

def test_manifest_spec_integrity():
    assert MANIFEST_SPEC_PATH.exists()
    manifest = json.loads(MANIFEST_SPEC_PATH.read_text(encoding="utf-8"))
    assert manifest["manifest_id"] == "math16_ab2d_spec_pilot02_freeze_v1"
    assert len(manifest["tasks"]) == 16

    for task in manifest["tasks"]:
        p_path = ROOT / task["prompt_path"]
        assert p_path.exists()
        assert "family" in task
        assert "assessment" in task

        ass = task["assessment"]
        assert ass["assessment_timing"] in {"PRE_RUN", "POST_RUN_RETROSPECTIVE"}
        assert ass["difficulty"] in {"LOW", "MEDIUM", "HIGH"}
        assert ass["discrimination"] in {"LOW", "MEDIUM", "HIGH"}
        assert ass["ceiling_risk"] in {"LOW", "MODERATE", "HIGH"}
        assert isinstance(ass["result_known"], bool)
        assert ass["evidence_basis"] in {"HISTORICAL_FROZEN_ONLY", "SAME_RUN_EVIDENCE"}

        # Verify SHA, char count, byte count
        content = p_path.read_text(encoding="utf-8").replace("\r\n", "\n")
        calculated_sha = hashlib.sha256(content.encode("utf-8")).hexdigest()
        assert calculated_sha == task["exact_prompt_sha256"]
        assert len(content) == task["char_count"]
        assert len(content.encode("utf-8")) == task["utf8_byte_count"]

def test_integer_sha_no_drift():
    manifest = json.loads(MANIFEST_SPEC_PATH.read_text(encoding="utf-8"))
    expected_integer_hashes = {
        "ce111_q03_prime_factor_selection": "5417185bc8f5d084bd04d6bf4d346762f6fa4738c6a52d30ea34706f4121e6f0",
        "ce112_q01_negative_integer_power": "1aa4f2a789b546a5f81f4a773db6c783edb359f5fbbc3c21966853d57db6a61b",
        "ce112_q09_divisor_multiple_intersection": "6ab35b719b39c1336e47f8fea3d373ec2482ad3f8d1c6979b192576090228035",
        "ce111_nonchoice_q01_part1_exponential_growth": "5d8e3f4084038b1e99a581bf26ad77e49c295362a076ff374e5614960f38c019"
    }

    for task in manifest["tasks"]:
        tid = task["task_id"]
        if tid in expected_integer_hashes:
            assert task["exact_prompt_sha256"] == expected_integer_hashes[tid]

def test_guardrails_isolation_and_no_leak():
    manifest = json.loads(MANIFEST_SPEC_PATH.read_text(encoding="utf-8"))

    # Non-integer tasks from pool
    from agent_tools.finals_rebuild.math16_pool import build_pool_tasks
    pool_tasks = {t["task_id"]: t for t in build_pool_tasks()}

    for task in manifest["tasks"]:
        tid = task["task_id"]
        g_path = ROOT / task["task_guardrail_source"]
        assert g_path.exists()

        # Guardrail content checks
        g_content = g_path.read_text(encoding="utf-8")

        # Verify no hardcoded correct answers are in the guardrail md files
        pool_task = pool_tasks[tid]
        ans = pool_task["correct_answer"]
        if isinstance(ans, dict):
            for k, v in ans.items():
                if isinstance(v, (int, str)) and len(str(v)) > 2:
                    assert str(v) not in g_content
        elif isinstance(ans, (int, str)) and len(str(ans)) > 2:
            assert str(ans) not in g_content

def test_api_policy_rules():
    manifest = json.loads(MANIFEST_SPEC_PATH.read_text(encoding="utf-8"))

    # 12 non-integer policies:
    # 8 API-only, 1 mixed, 3 native-only
    policies = {t["task_id"]: t["api_policy"] for t in manifest["tasks"]}

    # Check mixed
    assert policies["ce111_q10_ordered_quadratic_roots_radical"] == "mixed"

    # Check native-only
    for tid in ["ce111_q08_polynomial_factor_parameter_recovery",
                "ce115_calc_polynomial_factor_roots_l1",
                "ce113_q11_rationalize_denominator"]:
        assert policies[tid] == "native-only"

    # Check that native-only prompts do not expose domain APIs
    for task in manifest["tasks"]:
        if task["api_policy"] == "native-only":
            p_path = ROOT / task["prompt_path"]
            prompt_text = p_path.read_text(encoding="utf-8")
            assert "PolynomialOps" not in prompt_text
            assert "RadicalOps" not in prompt_text
            assert "FractionOps" not in prompt_text
            assert "IntegerOps" not in prompt_text

def test_plans_geometry():
    assert CELL_PLAN_PATH.exists()
    assert INVENTORY_PATH.exists()

    plan = json.loads(CELL_PLAN_PATH.read_text(encoding="utf-8"))
    inventory = json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))

    assert len(plan) == 240
    assert len(inventory) == 320

    reused = [c for c in inventory if c.get("reused") is True]
    new_cells = [c for c in inventory if c.get("reused") is False]
    assert len(reused) == 80
    assert len(new_cells) == 240

def test_runner_execute_disallowed():
    # Calling python runner with --execute must fail with RuntimeError
    res = subprocess.run([sys.executable, "scripts/run_math16_pilot02_full_generation.py", "--execute"], capture_output=True, text=True)
    assert res.returncode != 0
    assert "EXECUTE_DISALLOWED" in res.stderr or "EXECUTE_DISALLOWED" in res.stdout
