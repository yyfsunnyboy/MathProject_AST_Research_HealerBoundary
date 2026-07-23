"""
tests/test_math16_six_cell_healer_mechanism_validation_appendix_v1.py
=======================================================================
Test suite for Math16 Six-Cell Healer Mechanism Validation Appendix v1 (Errata Verified).

Validates:
1. Primary 5 vs Corrected 6 reconciliation and discrepancy cell.
2. 6/6 condition, family, and rule distribution.
3. Complete absence of '8B' in Appendix A text; Ab1 labeled as 原始契約條件.
4. Correct three-column return structure description in text.
5. Converged SAFE_REPAIR_CANDIDATE wording in Q6.
6. Separated Artifact SHA256 vs Governing Manifest SHA256 columns in evidence index.
7. Mandatory post-hoc disclaimer statement.
8. SHA integrity and official report protection.
"""

import hashlib
import json
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
APPENDIX_PATH = REPO_ROOT / "docs/experiments/appendices/math16_six_cell_healer_mechanism_validation_appendix_v1.md"
MANIFEST_PATH = REPO_ROOT / "docs/experiments/manifests/math16_six_cell_healer_mechanism_validation_appendix_v1_manifest.json"
FINAL_REPORT_V13_PATH = REPO_ROOT / "docs/experiments/reports/math16_final_report_v13.md" if (REPO_ROOT / "docs/experiments/reports/math16_final_report_v13.md").exists() else REPO_ROOT / "docs/experiments/reports/math16_pilot02_final_report_v13.md"
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

# 2. Condition & family distributions
def test_distributions():
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        m = json.load(f)

    conds = m.get("condition_distribution", {})
    fams = m.get("family_distribution", {})

    assert conds.get("Ab1_original_contract") == 0
    assert conds.get("Ab2g") == 2
    assert conds.get("Ab2d_api") == 2
    assert conds.get("Ab2d_spec") == 2

    assert fams.get("radical") == 4
    assert fams.get("fraction") == 2

# 3. Text errata checks
def test_text_errata():
    assert APPENDIX_PATH.exists()
    text = APPENDIX_PATH.read_text(encoding="utf-8")

    # Complete absence of 8B
    assert "8B" not in text
    # Ab1 is labeled as 原始契約條件
    assert "Ab1（原始契約條件）" in text
    # Three-column return structure wording is present
    assert "question_text" in text and "correct_answer" in text and "oracle_payload" in text
    # Q6 converged wording present
    assert "SAFE_REPAIR_CANDIDATE表示修改前具備不看答案" in text
    # Mandatory disclaimer present
    assert "本附錄為Evidence Complete凍結後之Post-hoc補充分析" in text

# 4. Appendix markdown Q&A questions (8 questions)
def test_markdown_qa():
    text = APPENDIX_PATH.read_text(encoding="utf-8")
    for i in range(1, 9):
        assert f"### Q{i}:" in text

# 5. Evidence index paths exist & SHA match
def test_evidence_paths_and_shas():
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        m = json.load(f)

    for item in m.get("evidence_index", []):
        art_p = REPO_ROOT / item["artifact_path"]
        assert art_p.exists(), f"Missing artifact: {item['artifact_path']}"
        actual_art_sha = sha256_file(art_p)
        assert actual_art_sha == item["artifact_sha256"], f"Artifact SHA mismatch for {item['artifact_path']}: expected {item['artifact_sha256']}, got {actual_art_sha}"

        gov_p = REPO_ROOT / item["governing_manifest_path"]
        assert gov_p.exists(), f"Missing governing manifest: {item['governing_manifest_path']}"
        actual_gov_sha = sha256_file(gov_p)
        assert actual_gov_sha == item["governing_manifest_sha256"], f"Governing manifest SHA mismatch for {item['governing_manifest_path']}: expected {item['governing_manifest_sha256']}, got {actual_gov_sha}"

        # Ensure artifact SHA is distinct from governing manifest SHA
        assert item["artifact_sha256"] != item["governing_manifest_sha256"]

# 6. Protected SHAs intact
def test_protected_shas_intact():
    assert sha256_file(FINAL_REPORT_V13_PATH) == FROZEN_SHA_FINAL_REPORT_V13
    assert sha256_file(EVIDENCE_COMPLETE_PATH) == FROZEN_SHA_EVIDENCE_COMPLETE
