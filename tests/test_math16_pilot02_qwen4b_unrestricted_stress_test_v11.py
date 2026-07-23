"""
tests/test_math16_pilot02_qwen4b_unrestricted_stress_test_v11.py
==================================================================
Test suite for Math16 Qwen4B Unrestricted Healer Stress Test v1.1 Preregistration.

Validates three-layer architecture reflection, Layer 2 gate removal, Layer 1 detector preservation,
NO_OP for no-candidate cells, dual classification (Outcome x Safety), and preflight execution.
"""

import hashlib
import json
import subprocess
import sys
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).parent.parent.resolve()
SPEC_V11_PATH = REPO_ROOT / "docs/experiments/design/math16_pilot02_qwen4b_unrestricted_stress_test_v11_spec.md"
MANIFEST_V11_PATH = REPO_ROOT / "docs/experiments/manifests/math16_pilot02_qwen4b_unrestricted_stress_test_v11_manifest.json"
CELL_PLAN_V11_PATH = REPO_ROOT / "docs/experiments/manifests/math16_pilot02_qwen4b_unrestricted_stress_test_v11_cell_plan.json"
PREFLIGHT_V11_PATH = REPO_ROOT / "scripts/preflight_math16_pilot02_qwen4b_unrestricted_stress_test_v11.py"
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

# 1. Spec v11 file exists and contains three-layer architecture and dual classification
def test_spec_v11_contents():
    assert SPEC_V11_PATH.exists()
    with open(SPEC_V11_PATH, encoding="utf-8") as f:
        content = f.read()

    assert "MATH16_QWEN4B_UNRESTRICTED_STRESS_TEST_V11_PREREGISTERED" in content
    assert "Layer 1: Rule Candidate Detection" in content
    assert "Layer 2: Primary Safety Eligibility Gate" in content
    assert "Layer 3: Transformation Execution" in content
    assert "ACCIDENTAL_RESCUE" in content

# 2. Manifest v11 file exists and matches strata allocation
def test_manifest_v11_contents():
    assert MANIFEST_V11_PATH.exists()
    with open(MANIFEST_V11_PATH, encoding="utf-8") as f:
        manifest = json.load(f)

    pop = manifest.get("target_population", {})
    assert pop.get("total_cells") == 320
    assert pop.get("baseline_fail_cells") == 242
    assert pop.get("no_rule_candidate_cells") == 231
    assert pop.get("unique_candidate_primary_eligible_cells") == 10
    assert pop.get("ambiguous_multiple_candidates_cells") == 1
    assert "MATH16_QWEN4B_UNRESTRICTED_STRESS_TEST_V11_PREREGISTERED" in manifest.get("verdicts", [])

# 3. Cell plan v11 file exists and matches 242 fail cells
def test_cell_plan_v11_contents():
    assert CELL_PLAN_V11_PATH.exists()
    with open(CELL_PLAN_V11_PATH, encoding="utf-8") as f:
        plan = json.load(f)

    assert plan.get("total_fail_cells") == 242
    strata = plan.get("strata_allocation", {})
    assert strata["NO_RULE_CANDIDATE"]["count"] == 231
    assert strata["UNIQUE_CANDIDATE_PRIMARY_ELIGIBLE"]["count"] == 10
    assert strata["AMBIGUOUS_MULTIPLE_CANDIDATES"]["count"] == 1

# 4. Preflight script v11 runs and outputs PREFLIGHT_PASS
def test_preflight_v11_pass():
    assert PREFLIGHT_V11_PATH.exists()
    res = subprocess.run(
        [sys.executable, str(PREFLIGHT_V11_PATH)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0
    assert "OVERALL: PREFLIGHT_PASS" in res.stdout

# 5. Official source SHAs remain unchanged
def test_official_shas_unchanged():
    assert sha256_file(FINAL_REPORT_V13_PATH) == FROZEN_SHA_FINAL_REPORT_V13
    assert sha256_file(EVIDENCE_COMPLETE_PATH) == FROZEN_SHA_EVIDENCE_COMPLETE
