"""
tests/test_math16_delivery_provenance_alignment.py
====================================================
Targeted test suite for the authoritative Math16 Teacher Delivery Package.

Validates:
1. 20260724_Math16 is the only authoritative delivery entry.
2. Its 04_math16_pilot02_jury_qa_final_v1.md contains Q20 provenance breakdown.
3. Its 05_math16_pilot02_appendices_v1.md contains Section 6 provenance breakdown.
4. Its README.md contains authority and provenance alignment summaries.
5. Preserves formal accounting (Primary rescued=5, Corrected=6, Qwen4B baseline=78, final=83/84).
6. Evidence Complete SHA & Final Report v1.3 SHA are unchanged.
7. No 'entire return dict single key' misdescriptions in delivery docs.
8. Zero model, zero healer, and zero evaluator calls.
"""

import hashlib
import json
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
DELIVERY_DIR = REPO_ROOT / "docs/決賽文件/實驗結果文件/20260724_Math16"

JURY_QA_DELIV = DELIVERY_DIR / "04_math16_pilot02_jury_qa_final_v1.md"
APPENDICES_DELIV = DELIVERY_DIR / "05_math16_pilot02_appendices_v1.md"
README_DELIV = DELIVERY_DIR / "README.md"
JURY_QA_REPORT = REPO_ROOT / "docs/experiments/reports/math16_pilot02_jury_qa_final_v1.md"
JURY_RISK_REVIEW = REPO_ROOT / "docs/experiments/reports/math16_jury_risk_review_v1.md"

PROV_REPORT_PATH = REPO_ROOT / "docs/experiments/reports/math16_healer_rule_provenance_audit_v1.md"
PROV_MANIFEST_PATH = REPO_ROOT / "docs/experiments/reports/math16_healer_rule_provenance_audit_v1_manifest.json"

FINAL_REPORT_V13_PATH = REPO_ROOT / "docs/experiments/reports/math16_pilot02_final_report_v13.md"
FINAL_REPORT_V13_DELIVERY = DELIVERY_DIR / "01_math16_pilot02_final_report_v13.md"
EVIDENCE_COMPLETE_PATH = REPO_ROOT / "docs/experiments/milestones/math16_pilot02_evidence_complete_v1/evidence_complete_manifest.json"

FROZEN_SHA_FINAL_REPORT_V13 = "d77eb8c4e1d7ccae03e276adb60bbe5f8a71ef38deef6246ae842ed840fe2fdd"
FROZEN_SHA_FINAL_REPORT_V13_DELIVERY = "30c318891b00d37275c9a95ab29bf4bcf18d154da6f9dd436b197aed0c47ecbe"
FROZEN_SHA_EVIDENCE_COMPLETE = "de11b9bd5038171689ee2895fc3a499a7b404f5259b3f5b3bcc31cb4d4af2225"
PREVIOUS_PROVENANCE_SHA = "663673eb8b0724813589dd7d9fbbf938e55e4bf51a24898165c71d604b77c5d3"

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def test_primary_delivery_files_exist():
    assert JURY_QA_DELIV.exists()
    assert APPENDICES_DELIV.exists()
    assert README_DELIV.exists()
    assert PROV_REPORT_PATH.exists()
    assert PROV_MANIFEST_PATH.exists()
    assert JURY_RISK_REVIEW.exists()


def test_20260724_is_the_only_authoritative_delivery_entry():
    readme = README_DELIV.read_text(encoding="utf-8")
    assert "唯一正式交付入口" in readme
    assert "20260724_Math16/" in readme
    assert "archived historical backup" in readme
    assert "20260722_Math16/" in readme


def test_submission_reading_order_and_rule_path():
    readme = README_DELIV.read_text(encoding="utf-8")
    entries = [
        "02_math16_pilot02_one_pager_v23.pdf",
        "03_math16_pilot02_poster_v11.pdf",
        "01_math16_pilot02_final_report_v13.md",
        "05_math16_pilot02_appendices_v1.md",
        "04_math16_pilot02_jury_qa_final_v1.md",
    ]
    assert [readme.index(entry) for entry in entries] == sorted(readme.index(entry) for entry in entries)
    assert "306 / 320" in readme
    assert "Ab2d+spec-v2 80" in readme

    appendix_delivery = APPENDICES_DELIV.read_text(encoding="utf-8")
    assert "\x07gent_tools/finals_rebuild/ce115_research_healer_rules_*.py" not in appendix_delivery
    assert "| agent_tools/finals_rebuild/ce115_research_healer_rules_*.py" in appendix_delivery
    assert list((REPO_ROOT / "agent_tools/finals_rebuild").glob("ce115_research_healer_rules_*.py"))

def test_eight_high_risk_questions_are_reviewed():
    qa = JURY_QA_REPORT.read_text(encoding="utf-8")
    review = JURY_RISK_REVIEW.read_text(encoding="utf-8")
    for question in ["R1:", "R2:", "R3:", "R4:", "R5:", "R6:", "R7:", "R8:"]:
        assert question in qa
    for evidence in [
        "PRE_FROZEN_UNCHANGED",
        "PROSPECTIVE_WITHIN_MATH16_COHORT",
        "POST_HOC_TECHNICAL_CORRECTION",
        "NO_RULE_CANDIDATE=231",
        "Observed Regression=0",
        "9B baseline/final 為 101/320",
        "獨立資料驗證",
    ]:
        assert evidence in review
    for prohibited in ["Healer 優於 Prompt", "Healer 保證安全", "六格證明可泛化"]:
        assert prohibited in review

def test_jury_qa_provenance_alignment():
    for path in [JURY_QA_DELIV]:
        text = path.read_text(encoding="utf-8")
        assert "Q20: Healer 規則的 Provenance" in text
        assert "PRE_FROZEN_UNCHANGED" in text
        assert "PROSPECTIVE_WITHIN_MATH16_COHORT" in text
        assert "POST_HOC_TECHNICAL_CORRECTION" in text
        assert "oracle_answer_used = false" in text

def test_appendices_provenance_alignment():
    for path in [APPENDICES_DELIV]:
        text = path.read_text(encoding="utf-8")
        assert "Healer 規則 Provenance Audit 與雙層學術定位" in text
        assert "PRE_FROZEN_UNCHANGED" in text
        assert "PROSPECTIVE_WITHIN_MATH16_COHORT" in text
        assert "POST_HOC_TECHNICAL_CORRECTION" in text

def test_no_payload_wrap_misdescription():
    for p in [JURY_QA_DELIV, APPENDICES_DELIV, README_DELIV]:
        text = p.read_text(encoding="utf-8")
        assert "整個return dict只有一個key" not in text
        assert "最外層dict只包含oracle_payload" not in text
        assert "不代表零副作用或一般語意安全保證" in text
        assert "尚未在完全獨立資料集驗證" in text

def test_provenance_version_references_are_unambiguous():
    manifest = json.loads(PROV_MANIFEST_PATH.read_text(encoding="utf-8"))
    report_sha = sha256_file(PROV_REPORT_PATH)
    manifest_sha = sha256_file(PROV_MANIFEST_PATH)

    assert manifest["previous_version_sha256"] == PREVIOUS_PROVENANCE_SHA
    assert manifest["current_version_sha256"] == report_sha
    assert manifest["report_sha256"] == report_sha
    assert manifest["previous_version_sha256"] != manifest["current_version_sha256"]

    for path in [JURY_QA_DELIV, APPENDICES_DELIV, README_DELIV]:
        text = path.read_text(encoding="utf-8")
        assert report_sha in text
        assert manifest_sha in text

def test_formal_accounting_is_preserved():
    text = FINAL_REPORT_V13_PATH.read_text(encoding="utf-8")
    for value in [
        "78/320",
        "10 格",
        "5 格",
        "83/320",
        "6 格",
        "84/320",
        "101 / 320",
        "NO_RULE_CANDIDATE",
        "UNIQUE_CANDIDATE_PRIMARY_ELIGIBLE",
        "AMBIGUOUS_MULTIPLE_CANDIDATES",
    ]:
        assert value in text or value in PROV_REPORT_PATH.read_text(encoding="utf-8")

def test_protected_shas_intact():
    assert sha256_file(FINAL_REPORT_V13_PATH) == FROZEN_SHA_FINAL_REPORT_V13
    assert sha256_file(FINAL_REPORT_V13_DELIVERY) == FROZEN_SHA_FINAL_REPORT_V13_DELIVERY
    assert sha256_file(EVIDENCE_COMPLETE_PATH) == FROZEN_SHA_EVIDENCE_COMPLETE

def test_delivery_final_report_reference_uses_current_sha():
    text = APPENDICES_DELIV.read_text(encoding="utf-8")
    assert "d77eb8c4e1d7ccae03e2..." in text
    assert "dcf6ae6ee0ac94b5896d..." not in text
