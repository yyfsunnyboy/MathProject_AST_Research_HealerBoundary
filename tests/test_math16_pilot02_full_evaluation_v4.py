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
MANIFEST_PATH = ROOT / "docs/experiments/manifests/math16_pilot02_full_evaluation_v4_r001_manifest.json"
V3_MANIFEST_PATH = ROOT / "docs/experiments/manifests/math16_pilot02_full_evaluation_v3_r001_manifest.json"
INVENTORY_PATH = ROOT / "docs/experiments/manifests/math16_pilot02_full_analysis_inventory.json"
TAXONOMY_MD = ROOT / "docs/決賽文件/20260720_AI 生成程式共同失敗分類標準_實際使用版 v3.md"
EVAL_OUT = ROOT / "docs/experiments/results/math16_pilot02_full_evaluation_v4_r001"
V3_OUT = ROOT / "docs/experiments/results/math16_pilot02_full_evaluation_v3_r001"
SCRIPT = ROOT / "scripts/evaluate_math16_pilot02_full_v4.py"
AUDIT_V1 = ROOT / "docs/experiments/audits/math16_pilot02_oracle_schema_audit_v1.md"


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_v4_manifest_integrity_and_does_not_overwrite_v3():
    assert MANIFEST_PATH.exists()
    assert V3_MANIFEST_PATH.exists()
    assert AUDIT_V1.exists()
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    assert manifest["evaluation_id"] == "math16_pilot02_full_evaluation_v4_r001"
    assert manifest["evaluation_revision"] == "v4_r001"
    assert manifest["prior_evaluation_revision"] == "v3_r001"
    assert manifest["expected_cell_count"] == 320
    assert _sha(TAXONOMY_MD) == manifest["taxonomy_file_sha256"]
    assert _sha(INVENTORY_PATH) == manifest["inventory_file_sha256"]
    assert "never overwrite v3_r001" in manifest["overwrite_policy"]
    # v3 outputs must still exist unchanged as sibling revision
    assert (V3_OUT / "cell_level_baseline.jsonl").exists()


def test_v4_preflight_offline():
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
def test_v4_outputs_geometry_and_v3_comparison_fields():
    if not (EVAL_OUT / "cell_level_baseline.jsonl").exists():
        pytest.skip("v4 evaluation outputs not yet produced")

    required = [
        "execution_manifest.json",
        "evaluation_inventory.json",
        "cell_level_baseline.jsonl",
        "baseline_summary.json",
        "v3_v4_comparison_summary.json",
        "math16_pilot02_full_v4_report.md",
    ]
    for name in required:
        assert (EVAL_OUT / name).exists(), name

    rows = [
        json.loads(line)
        for line in (EVAL_OUT / "cell_level_baseline.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    assert len(rows) == 320
    assert len({r["cell_id"] for r in rows}) == 320
    assert Counter(r["condition"] for r in rows) == {
        "ab1": 80,
        "ab2g": 80,
        "ab2d": 80,
        "ab2d_spec": 80,
    }
    assert Counter(r["family"] for r in rows) == {
        "integer": 80,
        "polynomial": 80,
        "radical": 80,
        "fraction": 80,
    }
    for row in rows:
        assert "v3_final_status" in row
        assert "v4_final_status" in row
        assert "changed_by_evaluator_fix" in row
        assert isinstance(row["changed_by_evaluator_fix"], bool)

    # v3 artifacts untouched
    v3_rows = [
        json.loads(line)
        for line in (V3_OUT / "cell_level_baseline.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    assert len(v3_rows) == 320
    cmp = json.loads((EVAL_OUT / "v3_v4_comparison_summary.json").read_text(encoding="utf-8"))
    assert cmp["v3_baseline_pass"] == "265/320"
