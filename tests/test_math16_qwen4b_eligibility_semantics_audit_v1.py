"""
tests/test_math16_qwen4b_eligibility_semantics_audit_v1.py
===========================================================
Test suite for Math16 Qwen4B Eligibility Semantics Audit v1.

Validates 242 baseline FAIL records classification into 5 mutually exclusive strata,
three-layer Healer architecture documentation, SHA integrity, and zero-model execution constraints.
"""

import hashlib
import json
import subprocess
import sys
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).parent.parent.resolve()
AUDIT_DIR = REPO_ROOT / "artifacts/math16_qwen4b_eligibility_semantics_audit_v1"
REPORT_PATH = REPO_ROOT / "docs/experiments/reports/math16_qwen4b_eligibility_semantics_audit_v1.md"
MANIFEST_PATH = REPO_ROOT / "docs/experiments/manifests/math16_qwen4b_eligibility_semantics_audit_v1_manifest.json"
BUILDER_PATH = REPO_ROOT / "scripts/build_math16_qwen4b_eligibility_semantics_audit_v1.py"
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

def load_jsonl(path: Path) -> list:
    records = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records

# 1. Audit records count = 242
def test_records_count():
    rec_file = AUDIT_DIR / "eligibility_semantics_records.jsonl"
    assert rec_file.exists()
    records = load_jsonl(rec_file)
    assert len(records) == 242

# 2. 5 strata mutually exclusive and sum to 242
def test_strata_breakdown_and_sum():
    records = load_jsonl(AUDIT_DIR / "eligibility_semantics_records.jsonl")
    strata_counts = {}
    for r in records:
        c = r["classification"]
        strata_counts[c] = strata_counts.get(c, 0) + 1

    assert strata_counts.get("NO_RULE_CANDIDATE") == 231
    assert strata_counts.get("UNIQUE_CANDIDATE_PRIMARY_ELIGIBLE") == 10
    assert strata_counts.get("UNIQUE_CANDIDATE_PRIMARY_NONELIGIBLE", 0) == 0
    assert strata_counts.get("AMBIGUOUS_MULTIPLE_CANDIDATES") == 1
    assert strata_counts.get("DETECTION_UNRESOLVED", 0) == 0
    assert sum(strata_counts.values()) == 242

# 3. Builder runs cleanly
def test_builder_runs():
    res = subprocess.run(
        [sys.executable, str(BUILDER_PATH)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0
    assert "All audit artifacts successfully generated" in res.stdout

# 4. Manifest verdicts match expected
def test_manifest_verdicts():
    assert MANIFEST_PATH.exists()
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        manifest = json.load(f)
    verdicts = manifest.get("verdicts", [])
    assert "MATH16_QWEN4B_ELIGIBILITY_SEMANTICS_AUDIT_V1_COMPLETED" in verdicts
    assert "STRESS_TEST_INTERVENTION_CONTRAST_CONFIRMED" in verdicts

# 5. Report contains three-layer architecture and disclaimers
def test_report_contents():
    assert REPORT_PATH.exists()
    with open(REPORT_PATH, encoding="utf-8") as f:
        content = f.read()
    assert "Layer 1: Rule Candidate Detection" in content
    assert "Layer 2: Primary Eligibility Gate" in content
    assert "Layer 3: Transformation Execution" in content
    assert "ACCIDENTAL_RESCUE" in content

# 6. Official source SHAs remain unchanged
def test_official_shas_unchanged():
    assert sha256_file(FINAL_REPORT_V13_PATH) == FROZEN_SHA_FINAL_REPORT_V13
    assert sha256_file(EVIDENCE_COMPLETE_PATH) == FROZEN_SHA_EVIDENCE_COMPLETE
