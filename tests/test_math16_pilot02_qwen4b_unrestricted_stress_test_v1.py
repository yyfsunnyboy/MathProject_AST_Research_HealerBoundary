"""
tests/test_math16_pilot02_qwen4b_unrestricted_stress_test_v1.py
==================================================================
Test suite for Math16 Qwen4B Unrestricted Healer Stress Test v1 Preregistration.

Validates target population (242 fail cells), frozen rules, inherited audit SHAs,
spec markdown, manifest JSON, preflight script execution, and governance rules.
"""

import hashlib
import json
import subprocess
from pathlib import Path
import sys
import pytest

REPO_ROOT = Path(__file__).parent.parent.resolve()
SPEC_PATH = REPO_ROOT / "docs/experiments/design/math16_pilot02_qwen4b_unrestricted_stress_test_v1_spec.md"
MANIFEST_PATH = REPO_ROOT / "docs/experiments/manifests/math16_pilot02_qwen4b_unrestricted_stress_test_v1_manifest.json"
PREFLIGHT_PATH = REPO_ROOT / "scripts/preflight_math16_pilot02_qwen4b_unrestricted_stress_test_v1.py"
BUILDER_PATH = REPO_ROOT / "scripts/build_math16_pilot02_qwen4b_unrestricted_stress_test_v1.py"
FINAL_REPORT_V13_PATH = REPO_ROOT / "docs/experiments/reports/math16_pilot02_final_report_v13.md"
EVIDENCE_COMPLETE_PATH = REPO_ROOT / "docs/experiments/milestones/math16_pilot02_evidence_complete_v1/evidence_complete_manifest.json"

FROZEN_SHA_FINAL_REPORT_V13 = "dcf6ae6ee0ac94b5896d8bc0d037ef4f06b7a3de905edf1be891022c6fd0754b"
FROZEN_SHA_EVIDENCE_COMPLETE = "de11b9bd5038171689ee2895fc3a499a7b404f5259b3f5b3bcc31cb4d4af2225"

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

# 1. Target population = 242 baseline FAIL cells
def test_target_population_fail_count():
    baseline_jsonl = REPO_ROOT / "docs/experiments/results/math16_pilot02_qwen4b_evaluation_v4_r001/cell_level_baseline.jsonl"
    assert baseline_jsonl.exists()
    fails = []
    passes = []
    with open(baseline_jsonl, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                r = json.loads(line)
                if r.get("final_status") == "PASSED":
                    passes.append(r)
                else:
                    fails.append(r)

    assert len(passes) + len(fails) == 320
    assert len(passes) == 78
    assert len(fails) == 242

# 2. Spec file exists and contains mandatory disclaimers and verdicts
def test_spec_file_contents():
    assert SPEC_PATH.exists()
    with open(SPEC_PATH, encoding="utf-8") as f:
        content = f.read()

    assert "MATH16_QWEN4B_UNRESTRICTED_STRESS_TEST_V1_PREREGISTERED" in content
    assert "ALL_BASELINE_FAIL_SET = 242 cells" in content
    assert "本實驗為 Evidence Complete 凍結後之 Post-hoc 補充 Stress Test" in content

# 3. Manifest file exists and matches target population
def test_manifest_file_contents():
    assert MANIFEST_PATH.exists()
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        manifest = json.load(f)

    pop = manifest.get("target_population", {})
    assert pop.get("total_cells") == 320
    assert pop.get("baseline_pass_cells") == 78
    assert pop.get("baseline_fail_cells") == 242
    assert "MATH16_QWEN4B_UNRESTRICTED_STRESS_TEST_V1_PREREGISTERED" in manifest.get("verdicts", [])

# 4. Builder runs in dry-run preflight mode cleanly
def test_builder_dry_run():
    assert BUILDER_PATH.exists()
    res = subprocess.run(
        [sys.executable, str(BUILDER_PATH), "--dry-run"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0
    assert "BUILDER RESULT: PREFLIGHT_PASS" in res.stdout

# 5. Preflight script runs and outputs PREFLIGHT_PASS
def test_preflight_script_pass():
    assert PREFLIGHT_PATH.exists()
    res = subprocess.run(
        [sys.executable, str(PREFLIGHT_PATH)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0
    assert "OVERALL: PREFLIGHT_PASS" in res.stdout

# 6. Official source SHAs remain unchanged
def test_official_shas_unchanged():
    assert sha256_file(FINAL_REPORT_V13_PATH) == FROZEN_SHA_FINAL_REPORT_V13
    assert sha256_file(EVIDENCE_COMPLETE_PATH) == FROZEN_SHA_EVIDENCE_COMPLETE
