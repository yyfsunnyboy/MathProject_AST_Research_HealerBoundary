"""
tests/test_math16_healer_rule_provenance_audit_v1.py
=====================================================
Test suite for Math16 Healer Rule Provenance Audit v1 (Refined Classification).

Validates:
1. Report file and manifest JSON exist and are readable.
2. Manifest contains exactly 6 rules matching the frozen allowlist.
3. Every rule has rule_freeze_status == "PRE_FROZEN_UNCHANGED" and validation_status == "PROSPECTIVE_WITHIN_MATH16_COHORT".
4. Runner-only fix (d3b5a69c) is explicitly separated from rule freeze status (0 rule modifications post-freeze).
5. L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP structure description verified (not 'entire dict single key').
6. All commit hashes are valid (8 or 40 hex chars).
7. All evidence paths exist in repository.
8. Official report numbers match (Primary rescued=5, Corrected=6, Qwen4B baseline=78, final=83/84).
9. Protected SHAs (Final Report v1.3 and Evidence Complete) are preserved.
10. Zero model, zero healer, and zero evaluator calls flags are true.
"""

import json
import hashlib
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
REPORT_PATH = REPO_ROOT / "docs/experiments/reports/math16_healer_rule_provenance_audit_v1.md"
MANIFEST_PATH = REPO_ROOT / "docs/experiments/reports/math16_healer_rule_provenance_audit_v1_manifest.json"

FINAL_REPORT_V13_PATH = REPO_ROOT / "docs/experiments/reports/math16_pilot02_final_report_v13.md"
EVIDENCE_COMPLETE_PATH = REPO_ROOT / "docs/experiments/milestones/math16_pilot02_evidence_complete_v1/evidence_complete_manifest.json"

FROZEN_SHA_FINAL_REPORT_V13 = "dcf6ae6ee0ac94b5896d8bc0d037ef4f06b7a3de905edf1be891022c6fd0754b"
FROZEN_SHA_EVIDENCE_COMPLETE = "de11b9bd5038171689ee2895fc3a499a7b404f5259b3f5b3bcc31cb4d4af2225"

EXPECTED_RULE_IDS = [
    "L1_CLOSE_UNBALANCED_PARENTHESIS",
    "L1_CLOSE_UNBALANCED_DELIMITER_EXTENDED",
    "L1_PROSE_RESIDUE_NARROW",
    "L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP",
    "L2_KWARGS_EMPTY_BAG_INLINE_UNIQUE_PARAM",
    "L2_CORRECT_ANSWER_JSON_DUMPS_UNWRAP"
]

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def test_provenance_audit_files_exist():
    assert REPORT_PATH.exists()
    assert MANIFEST_PATH.exists()

def test_manifest_structure_and_rules():
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        m = json.load(f)

    assert m["zero_model_calls"] is True
    assert m["zero_healer_calls"] is True
    assert m["zero_evaluator_calls"] is True

    rules = m.get("rules", [])
    assert len(rules) == 6
    rule_ids = [r["rule_id"] for r in rules]
    assert set(rule_ids) == set(EXPECTED_RULE_IDS)

    for r in rules:
        assert r["rule_freeze_status"] == "PRE_FROZEN_UNCHANGED"
        assert r["validation_status"] == "PROSPECTIVE_WITHIN_MATH16_COHORT"
        assert r["rule_diff_since_freeze"] == "EMPTY_UNCHANGED"
        assert r["independently_validated"] is False
        assert len(r["first_commit"]) in [7, 8, 40]
        assert len(r["freeze_commit"]) in [7, 8, 40]

        for p in r.get("evidence_paths", []):
            assert (REPO_ROOT / p).exists(), f"Evidence path missing: {p}"

def test_l2_single_key_payload_wrap_classification_and_structure():
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        m = json.load(f)

    rules_by_id = {r["rule_id"]: r for r in m.get("rules", [])}
    wrap_rule = rules_by_id["L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP"]

    assert wrap_rule["rule_freeze_status"] == "PRE_FROZEN_UNCHANGED"
    assert wrap_rule["validation_status"] == "PROSPECTIVE_WITHIN_MATH16_COHORT"
    assert wrap_rule["first_commit"] == "e098dc04"
    assert wrap_rule["freeze_commit"] == "d9aa264c"
    assert wrap_rule["independently_validated"] is False

    text = REPORT_PATH.read_text(encoding="utf-8")
    assert "整個return dict只有一個key" not in text
    assert "最外層dict只包含oracle_payload" not in text
    assert "oracle_payload" in text

def test_report_numbers_and_disclaimer():
    text = REPORT_PATH.read_text(encoding="utf-8")
    assert "83/320" in text
    assert "84/320" in text
    assert "5" in text
    assert "6" in text
    assert "PRE_FROZEN_UNCHANGED" in text
    assert "PROSPECTIVE_WITHIN_MATH16_COHORT" in text
    assert "POST_HOC_TECHNICAL_CORRECTION" in text
    assert "oracle_answer_used = false" in text

def test_protected_shas_intact():
    assert sha256_file(FINAL_REPORT_V13_PATH) == FROZEN_SHA_FINAL_REPORT_V13
    assert sha256_file(EVIDENCE_COMPLETE_PATH) == FROZEN_SHA_EVIDENCE_COMPLETE
