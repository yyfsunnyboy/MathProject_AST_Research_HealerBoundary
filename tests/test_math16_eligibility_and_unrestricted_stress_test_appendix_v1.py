"""
tests/test_math16_eligibility_and_unrestricted_stress_test_appendix_v1.py
===========================================================================
Test suite for Math16 Eligibility & Unrestricted Stress Test Validation Appendix v1 (Errata Verified).

Validates:
1. 242 baseline FAIL strata accounting (231/10/0/1/0).
2. Default arm and Forced exploratory arm outcome accounting.
3. Total absence of 'ambiguity_gate_prevented_harm = True' claim.
4. Presence of 3 new semantic fields in manifest (prevented_unsafe, prevented_ineffective, observed_harm_prevented).
5. Converged wording for Q7 and Q10 in markdown text.
6. Absence of exaggerated statements (證實Eligibility擋下是正確的 / 覆蓋全部可安全救回).
7. Separated Artifact SHA256 vs Governing Manifest SHA256 columns.
8. Distinct Artifact SHAs for disposition_summary.json and forced ambiguity .diff.
9. Mandatory post-hoc disclaimer statement.
10. SHA integrity and official report protection.
"""

import hashlib
import json
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
APPENDIX_PATH = REPO_ROOT / "docs/experiments/appendices/math16_eligibility_and_unrestricted_stress_test_appendix_v1.md"
MANIFEST_PATH = REPO_ROOT / "docs/experiments/manifests/math16_eligibility_and_unrestricted_stress_test_appendix_v1_manifest.json"
FINAL_REPORT_V13_PATH = REPO_ROOT / "docs/experiments/reports/math16_final_report_v13.md" if (REPO_ROOT / "docs/experiments/reports/math16_final_report_v13.md").exists() else REPO_ROOT / "docs/experiments/reports/math16_pilot02_final_report_v13.md"
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

# 1. 242-cell strata accounting check
def test_manifest_accounting():
    assert MANIFEST_PATH.exists()
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        m = json.load(f)

    acc = m.get("accounting", {})
    assert acc.get("total_baseline_fail_cells") == 242
    assert acc.get("no_rule_candidate_count") == 231
    assert acc.get("unique_candidate_primary_eligible_count") == 10
    assert acc.get("unique_candidate_primary_noneligible_count") == 0
    assert acc.get("ambiguous_multiple_candidates_count") == 1
    assert acc.get("detection_unresolved_count") == 0

# 2. Default and Forced arm accounting and semantic fields
def test_arms_accounting_and_semantic_fields():
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        m = json.load(f)

    d_arm = m.get("default_arm", {})
    f_arm = m.get("forced_exploratory_arm", {})

    assert d_arm.get("abstain_no_rule") == 231
    assert d_arm.get("planned_transform") == 10
    assert d_arm.get("abstain_ambiguous") == 1

    assert f_arm.get("target_cell_id") == AMBIGUOUS_CELL_ID
    assert f_arm.get("safety_classification") == "UNSAFE_MODIFICATION"
    assert f_arm.get("outcome_classification") == "MODIFIED_STILL_FAIL"

    # Three new semantic fields check
    assert f_arm.get("ambiguity_gate_prevented_unsafe_intervention") is True
    assert f_arm.get("ambiguity_gate_prevented_ineffective_intervention") is True
    assert f_arm.get("observed_harm_prevented") == "not_demonstrated"
    assert "ambiguity_gate_prevented_harm" not in f_arm

# 3. Appendix markdown Q&A questions & errata wording checks
def test_markdown_qa_and_errata_wording():
    assert APPENDIX_PATH.exists()
    text = APPENDIX_PATH.read_text(encoding="utf-8")

    # Q1 to Q10 present
    for i in range(1, 11):
        assert f"### Q{i}:" in text

    # Mandatory disclaimer present
    assert "本附錄為Evidence Complete凍結後之Post-hoc補充分析" in text

    # Check converged Q7 wording
    assert "此案例支持原本Abstain決策具有合理性" in text
    assert "證實Eligibility擋下是正確的" not in text

    # Check converged Q10 wording
    assert "Primary Eligibility涵蓋了所有已偵測到的唯一安全候選" in text
    assert "覆蓋全部可安全救回的潛在窗口" not in text

    # Check absence of prevented_harm claim
    assert "ambiguity_gate_prevented_harm = True" not in text

# 4. Evidence index paths exist & SHA verification
def test_evidence_paths_and_distinct_shas():
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        m = json.load(f)

    artifact_shas = []
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
        artifact_shas.append(item["artifact_sha256"])

    # Ensure disposition_summary SHA is distinct from forced diff SHA
    assert artifact_shas[1] != artifact_shas[2]

# 5. Protected SHAs intact
def test_protected_shas_intact():
    assert sha256_file(FINAL_REPORT_V13_PATH) == FROZEN_SHA_FINAL_REPORT_V13
    assert sha256_file(EVIDENCE_COMPLETE_PATH) == FROZEN_SHA_EVIDENCE_COMPLETE
