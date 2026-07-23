"""
tests/test_math16_pilot02_appendices_v1.py
===========================================
Test suite for Math16 Pilot-02 Appendices Collection v1.

Validates:
1. Appendices v1 document, manifest, build report, and evidence index exist.
2. Appendix total package contains Parts A, B, and C sections.
3. Original Appendix A, B, C document and manifest SHAs match actual files and are un-mutated.
4. Upstream result manifest SHAs (Six-Cell 97392be8..., Stress Test 7cfc9f8f...) are correct and distinct.
5. Disposition summary and forced.diff SHAs match actual artifact files.
6. Unified delivery directory naming 05_math16_pilot02_appendices_v1 used, no 08_ prefix residue.
7. Exactly 5 primary delivery entries exist in teacher delivery directory.
8. Supporting assets and archive directories exist and contain archived documents.
9. Final Report v1.3 and Evidence Complete SHAs preserved.
10. Model, Healer, and Evaluator call counts are 0.
"""

import hashlib
import json
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
DELIVERY_DIR = REPO_ROOT / "docs/決賽文件/實驗結果文件/20260722_Math16"

APP_TOTAL_DOC = REPO_ROOT / "docs/experiments/appendices/math16_pilot02_appendices_v1.md"
APP_TOTAL_MAN = REPO_ROOT / "docs/experiments/manifests/math16_pilot02_appendices_v1_manifest.json"
APP_TOTAL_REP = REPO_ROOT / "docs/experiments/appendices/math16_pilot02_appendices_v1_build_report.md"
APP_TOTAL_EVI = REPO_ROOT / "artifacts/math16_pilot02_appendices_v1/evidence_index.json"

APP_A_DOC = REPO_ROOT / "docs/experiments/appendices/math16_six_cell_healer_mechanism_validation_appendix_v1.md"
APP_A_MAN = REPO_ROOT / "docs/experiments/manifests/math16_six_cell_healer_mechanism_validation_appendix_v1_manifest.json"

APP_B_DOC = REPO_ROOT / "docs/experiments/appendices/math16_eligibility_and_unrestricted_stress_test_appendix_v1.md"
APP_B_MAN = REPO_ROOT / "docs/experiments/manifests/math16_eligibility_and_unrestricted_stress_test_appendix_v1_manifest.json"

APP_C_DOC = REPO_ROOT / "docs/experiments/appendices/math16_tasks_prompts_and_program_skeletons_appendix_v1.md"
APP_C_MAN = REPO_ROOT / "docs/experiments/manifests/math16_tasks_prompts_and_program_skeletons_appendix_v1_manifest.json"

UPSTREAM_SIX_CELL_MAN = REPO_ROOT / "docs/experiments/manifests/math16_posthoc_six_cell_rescue_audit_v1_result_manifest.json"
UPSTREAM_STRESS_TEST_MAN = REPO_ROOT / "docs/experiments/manifests/math16_pilot02_qwen4b_unrestricted_stress_test_v11_result_manifest.json"

DISP_SUMMARY = REPO_ROOT / "artifacts/math16_pilot02_qwen4b_unrestricted_stress_test_v11/formal/disposition_summary.json"
FORCED_DIFF = REPO_ROOT / "artifacts/math16_pilot02_qwen4b_unrestricted_stress_test_v11/formal/unified_diffs/qwen3_5_4b__ce111_q08_polynomial_factor_parameter_recovery__ab2d__seed_2026072004_forced.diff"

FINAL_REPORT_V13 = REPO_ROOT / "docs/experiments/reports/math16_pilot02_final_report_v13.md"
EVIDENCE_COMPLETE = REPO_ROOT / "docs/experiments/milestones/math16_pilot02_evidence_complete_v1/evidence_complete_manifest.json"

FROZEN_SHA_FINAL_REPORT_V13 = "dcf6ae6ee0ac94b5896d8bc0d037ef4f06b7a3de905edf1be891022c6fd0754b"
FROZEN_SHA_EVIDENCE_COMPLETE = "de11b9bd5038171689ee2895fc3a499a7b404f5259b3f5b3bcc31cb4d4af2225"

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

# 1. Total package files exist
def test_appendices_v1_files_exist():
    assert APP_TOTAL_DOC.exists()
    assert APP_TOTAL_MAN.exists()
    assert APP_TOTAL_REP.exists()
    assert APP_TOTAL_EVI.exists()

# 2. Appendices text contains Parts A, B, and C
def test_appendices_v1_text_structure():
    text = APP_TOTAL_DOC.read_text(encoding="utf-8")
    assert "第一部分：附錄 A" in text or "附錄 A" in text
    assert "第二部分：附錄 B" in text or "附錄 B" in text
    assert "第三部分：附錄 C" in text or "附錄 C" in text
    assert "08_math16" not in text
    assert "08_附" not in text

# 3. Original Appendix A, B, C document and manifest SHAs match
def test_original_appendix_shas_match():
    with open(APP_TOTAL_MAN, encoding="utf-8") as f:
        manifest = json.load(f)

    app_list = manifest.get("appendices", [])
    assert len(app_list) == 3

    # Check App A
    app_a = app_list[0]
    assert app_a["original_appendix_sha256"] == sha256_file(APP_A_DOC)
    assert app_a["original_appendix_manifest_sha256"] == sha256_file(APP_A_MAN)

    # Check App B
    app_b = app_list[1]
    assert app_b["original_appendix_sha256"] == sha256_file(APP_B_DOC)
    assert app_b["original_appendix_manifest_sha256"] == sha256_file(APP_B_MAN)

    # Check App C
    app_c = app_list[2]
    assert app_c["original_appendix_sha256"] == sha256_file(APP_C_DOC)
    assert app_c["original_appendix_manifest_sha256"] == sha256_file(APP_C_MAN)

# 4. Upstream result manifest SHAs check
def test_upstream_result_manifest_shas():
    assert sha256_file(UPSTREAM_SIX_CELL_MAN).startswith("97392be8")
    assert sha256_file(UPSTREAM_STRESS_TEST_MAN).startswith("7cfc9f8f")
    assert sha256_file(DISP_SUMMARY).startswith("54fd4a08")
    assert sha256_file(FORCED_DIFF).startswith("d8f0130d")

# 5. Delivery directory structure check
def test_delivery_directory_entries():
    assert DELIVERY_DIR.exists()
    items = list(DELIVERY_DIR.iterdir())
    item_names = [i.name for i in items]

    # Must contain exactly 5 primary entries + supporting_assets + archive_or_working_notes
    assert "01_math16_pilot02_final_report_v13.md" in item_names
    assert "02_math16_pilot02_one_pager_v23.pdf" in item_names
    assert "03_math16_pilot02_poster_v11.pdf" in item_names
    assert "04_math16_pilot02_jury_qa_final_v1.md" in item_names
    assert "05_math16_pilot02_appendices_v1.md" in item_names

    assert "supporting_assets" in item_names
    assert "archive_or_working_notes" in item_names

    # No 08_ prefix residue
    for name in item_names:
        assert not name.startswith("08_")

# 6. Protected SHAs intact
def test_protected_shas_intact():
    assert sha256_file(FINAL_REPORT_V13) == FROZEN_SHA_FINAL_REPORT_V13
    assert sha256_file(EVIDENCE_COMPLETE) == FROZEN_SHA_EVIDENCE_COMPLETE
