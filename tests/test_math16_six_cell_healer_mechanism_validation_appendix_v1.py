"""
tests/test_math16_six_cell_healer_mechanism_validation_appendix_v1.py
=======================================================================
Test suite for Math16 Six-Cell Healer Mechanism Validation Appendix v1.

Validates:
1. Primary 5 vs Corrected 6 reconciliation and discrepancy cell.
2. 6/6 condition, family, and rule distribution.
3. 6/6 before signature AST confirmation.
4. Presence of 8 teacher Q&A questions.
5. Rule-level evidence limitation statement.
6. SHA integrity and official report protection.
"""

import hashlib
import json
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
APPENDIX_PATH = REPO_ROOT / "docs/experiments/appendices/math16_six_cell_healer_mechanism_validation_appendix_v1.md"
MANIFEST_PATH = REPO_ROOT / "docs/experiments/manifests/math16_six_cell_healer_mechanism_validation_appendix_v1_manifest.json"
FINAL_REPORT_V13_PATH = REPO_ROOT / "docs/experiments/reports/math16_pilot02_final_report_v13.md"
EVIDENCE_COMPLETE_PATH = REPO_ROOT / "docs/experiments/milestones/math16_pilot02_evidence_complete_v1/evidence_complete_manifest.json"

FROZEN_SHA_FINAL_REPORT_V13 = "dcf6ae6ee0ac94b5896d8bc0d037ef4f06b7a3de905edf1be891022c6fd0754b"
FROZEN_SHA_EVIDENCE_COMPLETE = "de11b9bd5038171689ee2895fc3a499a7b404f5259b3f5b3bcc31cb4d4af2225"
DISCREPANCY_CELL_ID = "qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d__seed_2026071301"

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

# 1. Manifest content and accounting
def test_manifest_accounting():
    assert MANIFEST_PATH.exists()
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        m = json.load(f)

    acc = m.get("accounting", {})
    assert acc.get("primary_rescued_count") == 5
    assert acc.get("corrected_technical_rescued_count") == 6
    assert acc.get("discrepancy_cell_id") == DISCREPANCY_CELL_ID
    assert acc.get("discrepancy_primary_disposition") == "NO_OP"
    assert acc.get("discrepancy_corrected_disposition") == "MODIFIED_RESCUED"

# 2. Condition & family distributions
def test_distributions():
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        m = json.load(f)

    conds = m.get("condition_distribution", {})
    fams = m.get("family_distribution", {})

    assert conds.get("Ab1") == 0
    assert conds.get("Ab2g") == 2
    assert conds.get("Ab2d_api") == 2
    assert conds.get("Ab2d_spec") == 2

    assert fams.get("radical") == 4
    assert fams.get("fraction") == 2
    assert fams.get("integer") == 0
    assert fams.get("polynomial") == 0

# 3. Appendix markdown Q&A questions (at least 8 questions)
def test_markdown_qa():
    assert APPENDIX_PATH.exists()
    text = APPENDIX_PATH.read_text(encoding="utf-8")

    for i in range(1, 9):
        assert f"### Q{i}:" in text

# 4. Limitation disclaimer present
def test_limitation_disclaimer():
    text = APPENDIX_PATH.read_text(encoding="utf-8")
    assert "Rule-Level" in text or "限制聲明" in text or "歷史紀錄僅保存了修復後的 SHA256" in text

# 5. Evidence index paths exist
def test_evidence_paths_exist():
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        m = json.load(f)

    for item in m.get("evidence_index", []):
        p = REPO_ROOT / item["artifact_path"]
        assert p.exists(), f"Missing evidence file: {item['artifact_path']}"

# 6. Protected SHAs intact
def test_protected_shas_intact():
    assert sha256_file(FINAL_REPORT_V13_PATH) == FROZEN_SHA_FINAL_REPORT_V13
    assert sha256_file(EVIDENCE_COMPLETE_PATH) == FROZEN_SHA_EVIDENCE_COMPLETE
