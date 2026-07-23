"""
tests/test_math16_pilot02_qwen4b_unrestricted_stress_test_v11_dry_run.py
==========================================================================
Test suite for Math16 Qwen4B Unrestricted Stress Test v1.1 Zero-Model Dry Run.

Validates 242-cell accounting, default arm plan, forced exploratory arm plan,
ambiguity N=1 specification, deterministic selection policy, safety pre-classification,
output isolation, and zero-model execution constraints.
"""

import hashlib
import json
import subprocess
import sys
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).parent.parent.resolve()
DRY_RUN_DIR = REPO_ROOT / "artifacts/math16_pilot02_qwen4b_unrestricted_stress_test_v11/dry_run"
FORMAL_DIR = REPO_ROOT / "artifacts/math16_pilot02_qwen4b_unrestricted_stress_test_v11/formal"
REPORT_PATH = REPO_ROOT / "docs/experiments/reports/math16_pilot02_qwen4b_unrestricted_stress_test_v11_dry_run_report.md"
MANIFEST_PATH = REPO_ROOT / "docs/experiments/manifests/math16_pilot02_qwen4b_unrestricted_stress_test_v11_runtime_manifest.json"
BUILDER_PATH = REPO_ROOT / "scripts/build_math16_pilot02_qwen4b_unrestricted_stress_test_v11_dry_run.py"
PREFLIGHT_PATH = REPO_ROOT / "scripts/preflight_math16_pilot02_qwen4b_unrestricted_stress_test_v11_runtime.py"
FINAL_REPORT_V13_PATH = REPO_ROOT / "docs/experiments/reports/math16_pilot02_final_report_v13.md"
EVIDENCE_COMPLETE_PATH = REPO_ROOT / "docs/experiments/milestones/math16_pilot02_evidence_complete_v1/evidence_complete_manifest.json"

FROZEN_SHA_FINAL_REPORT_V13 = "dcf6ae6ee0ac94b5896d8bc0d037ef4f06b7a3de905edf1be891022c6fd0754b"
FROZEN_SHA_EVIDENCE_COMPLETE = "de11b9bd5038171689ee2895fc3a499a7b404f5259b3f5b3bcc31cb4d4af2225"
AMBIGUOUS_CELL_ID = "qwen3_5_4b__ce111_q08_polynomial_factor_parameter_recovery__ab2d__seed_2026072004"

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def load_jsonl(path: Path) -> list:
    records = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records

# 1. 242-cell plan accounting matches exactly
def test_dry_run_plan_accounting():
    rec_file = DRY_RUN_DIR / "dry_run_cell_plan.jsonl"
    assert rec_file.exists()
    records = load_jsonl(rec_file)
    assert len(records) == 242

    strata_counts = {}
    for r in records:
        s = r["stratum"]
        strata_counts[s] = strata_counts.get(s, 0) + 1

    assert strata_counts.get("NO_RULE_CANDIDATE") == 231
    assert strata_counts.get("UNIQUE_CANDIDATE_PRIMARY_ELIGIBLE") == 10
    assert strata_counts.get("UNIQUE_CANDIDATE_PRIMARY_NONELIGIBLE", 0) == 0
    assert strata_counts.get("AMBIGUOUS_MULTIPLE_CANDIDATES") == 1
    assert strata_counts.get("DETECTION_UNRESOLVED", 0) == 0
    assert sum(strata_counts.values()) == 242

# 2. Default arm plan CSV has 242 rows
def test_default_arm_plan_csv():
    csv_file = DRY_RUN_DIR / "default_arm_plan.csv"
    assert csv_file.exists()
    with open(csv_file, encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]
    assert len(lines) == 243  # Header + 242 rows

# 3. Forced exploratory arm plan specifies canonical cell_id and UNSAFE pre-classification
def test_forced_exploratory_arm_plan():
    forced_file = DRY_RUN_DIR / "forced_exploratory_arm_plan.json"
    assert forced_file.exists()
    with open(forced_file, encoding="utf-8") as f:
        plan = json.load(f)

    assert plan.get("target_cell_id") == AMBIGUOUS_CELL_ID
    assert plan.get("safety_pre_classification") == "UNSAFE_MODIFICATION"
    assert plan.get("safety_pre_classification") != "SAFE_REPAIR_CANDIDATE"
    assert plan.get("transform_executed_in_dry_run") is False

# 4. Zero executions in dry run
def test_zero_transform_executions():
    records = load_jsonl(DRY_RUN_DIR / "dry_run_cell_plan.jsonl")
    for r in records:
        assert r.get("transform_executed_in_dry_run") is False

# 5. Output directory isolation check record
def test_output_isolation():
    isolation_file = DRY_RUN_DIR / "output_isolation_check.json"
    assert isolation_file.exists()
    with open(isolation_file, encoding="utf-8") as f:
        iso = json.load(f)
    assert iso.get("status") == "ISOLATED_PASS"

# 6. Builder script runs cleanly
def test_builder_runs():
    assert BUILDER_PATH.exists()
    res = subprocess.run(
        [sys.executable, str(BUILDER_PATH)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0
    assert "All dry run artifacts successfully generated" in res.stdout

# 7. Preflight script runs and outputs PREFLIGHT_PASS
def test_preflight_script():
    assert PREFLIGHT_PATH.exists()
    res = subprocess.run(
        [sys.executable, str(PREFLIGHT_PATH)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0
    assert "OVERALL: PREFLIGHT_PASS" in res.stdout

# 8. Report and Manifest content checks
def test_report_and_manifest_verdicts():
    assert REPORT_PATH.exists()
    assert MANIFEST_PATH.exists()
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        manifest = json.load(f)
    verdicts = manifest.get("verdicts", [])
    assert "MATH16_QWEN4B_UNRESTRICTED_STRESS_TEST_V11_ZERO_MODEL_DRY_RUN_COMPLETED" in verdicts
    assert "DEFAULT_ARM_242_CELL_PLAN_VALIDATED" in verdicts

# 9. Official source SHAs remain unchanged
def test_official_shas_unchanged():
    assert sha256_file(FINAL_REPORT_V13_PATH) == FROZEN_SHA_FINAL_REPORT_V13
    assert sha256_file(EVIDENCE_COMPLETE_PATH) == FROZEN_SHA_EVIDENCE_COMPLETE
