# -*- coding: utf-8 -*-
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "docs/experiments/manifests/math16_pilot02_full_evaluation_v3_r001_manifest.json"
INVENTORY_PATH = ROOT / "docs/experiments/manifests/math16_pilot02_full_analysis_inventory.json"
TAXONOMY_MD = ROOT / "docs/決賽文件/20260720_AI 生成程式共同失敗分類標準_實際使用版 v3.md"
EVAL_OUT = ROOT / "docs/experiments/results/math16_pilot02_full_evaluation_v3_r001"
INTEGER_BASELINE = (
    ROOT / "docs/experiments/results/math16_pilot02_integer_evaluation_v3_r001/cell_level_baseline.jsonl"
)
SCRIPT = ROOT / "scripts/evaluate_math16_pilot02_full_v3.py"


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_full_evaluation_manifest_integrity():
    assert MANIFEST_PATH.exists()
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    assert manifest["evaluation_id"] == "math16_pilot02_full_evaluation_v3_r001"
    assert manifest["evaluation_revision"] == "v3_r001"
    assert manifest["expected_cell_count"] == 320
    assert manifest["taxonomy_file_sha256"] == "7df8f4472ce048569967436cbc73ede8fd4bd117ad67d0028ddd95af2055a304"
    assert _sha(TAXONOMY_MD) == manifest["taxonomy_file_sha256"]
    assert _sha(INVENTORY_PATH) == manifest["inventory_file_sha256"]
    assert manifest["condition_display_map"]["ab2d"] == "Ab2d+api"
    assert manifest["condition_display_map"]["ab2d_spec"] == "Ab2d+spec"
    assert len(manifest["healer_allowlist"]) == 6


def test_inventory_geometry_320():
    inventory = json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))
    assert len(inventory) == 320
    assert len({c["cell_id"] for c in inventory}) == 320
    assert Counter(c["condition"] for c in inventory) == {
        "ab1": 80,
        "ab2g": 80,
        "ab2d": 80,
        "ab2d_spec": 80,
    }
    assert Counter(bool(c.get("reused")) for c in inventory) == {True: 80, False: 240}
    assert all(Counter(c["seed"] for c in inventory)[s] == 64 for s in {
        2026071301, 2026072001, 2026072002, 2026072003, 2026072004
    })


def test_preflight_offline():
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "--preflight-only"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stdout + "\n" + proc.stderr
    assert "Zero-Result Preflight PASS" in proc.stdout


@pytest.mark.slow
def test_execute_outputs_and_consistency():
    if not (EVAL_OUT / "cell_level_baseline.jsonl").exists():
        pytest.skip("full evaluation outputs not yet produced")

    required = [
        "execution_manifest.json",
        "evaluation_inventory.json",
        "cell_level_baseline.jsonl",
        "baseline_summary.json",
        "healer_results.jsonl",
        "post_healer_summary.json",
        "condition_summary.json",
        "family_summary.json",
        "task_summary.json",
        "seed_summary.json",
        "condition_family_task_tables.json",
        "failure_taxonomy_summary.json",
        "math16_pilot02_full_v3_report.md",
    ]
    for name in required:
        assert (EVAL_OUT / name).exists(), name

    baseline = [
        json.loads(line)
        for line in (EVAL_OUT / "cell_level_baseline.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    healer = [
        json.loads(line)
        for line in (EVAL_OUT / "healer_results.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    assert len(baseline) == 320
    assert len(healer) == 320
    assert len({r["cell_id"] for r in baseline}) == 320

    bp = sum(1 for r in baseline if r["final_status"] == "PASSED")
    bf = sum(1 for r in baseline if r["final_status"] != "PASSED")
    assert bp + bf == 320
    php = sum(1 for r in healer if r["final_status"] == "PASSED")
    phf = sum(1 for r in healer if r["final_status"] != "PASSED")
    assert php + phf == 320

    assert Counter(r["condition"] for r in baseline) == {
        "ab1": 80,
        "ab2g": 80,
        "ab2d": 80,
        "ab2d_spec": 80,
    }
    assert Counter(r["family"] for r in baseline) == {
        "integer": 80,
        "polynomial": 80,
        "radical": 80,
        "fraction": 80,
    }
    assert all(Counter(r["seed"] for r in baseline)[s] == 64 for s in {
        2026071301, 2026072001, 2026072002, 2026072003, 2026072004
    })

    for h in healer:
        assert not (h["rescued"] and h["regressed"])
        assert not (h["preserved_pass"] and h["rescued"])
        if h["healer_eligible"]:
            assert h["healer_ran"] is True
        if not h["healer_eligible"] and h["baseline_outcome"] == "PASSED":
            assert h["preserved_pass"] is True

    # Integer reproducibility vs prior revision
    prior = {
        json.loads(line)["cell_id"]: json.loads(line)
        for line in INTEGER_BASELINE.read_text(encoding="utf-8").splitlines()
        if line.strip()
    }
    integer_rows = [r for r in baseline if r["family"] == "integer"]
    assert len(integer_rows) == 80
    for row in integer_rows:
        assert prior[row["cell_id"]]["final_status"] == row["final_status"]

    report = (EVAL_OUT / "math16_pilot02_full_v3_report.md").read_text(encoding="utf-8")
    assert "MATH16_320_BLINDED_V3_EVALUATION_COMPLETE" in report
    assert "FROZEN_HEALER_EVALUATION_COMPLETE" in report
    assert "FULL_CONDITION_FAMILY_COMPARISON_READY" in report

    exec_manifest = json.loads((EVAL_OUT / "execution_manifest.json").read_text(encoding="utf-8"))
    assert exec_manifest["llm_calls"] == 0
    assert exec_manifest["api_cost_usd"] == 0.0


def test_unknown_not_mapped_to_l5_helper():
    from scripts.evaluate_math16_pilot02_full_v3 import classify_outcome_to_v3

    mapped = classify_outcome_to_v3("totally_unknown_outcome", {"detail": {}}, api_policy="native-only")
    assert mapped["primary_failure_layer"] is not "L5"
    assert mapped["classification_status"] == "PENDING_REVIEW"
    assert mapped["outcome_validity"] == "PENDING_REVIEW"
