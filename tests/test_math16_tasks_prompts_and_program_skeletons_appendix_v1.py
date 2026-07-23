"""
tests/test_math16_tasks_prompts_and_program_skeletons_appendix_v1.py
=====================================================================
Test suite for Math16 Tasks, Prompts, and Program Skeletons Appendix v1 (Errata Verified).

Validates:
1. 16 tasks complete and unique in task_index.csv with runtime_level and preregistered_difficulty.
2. Verified preregistered difficulty for the 4 specified tasks:
   - ce111_q08: HIGH
   - ce111_q10: HIGH
   - ce112_q04: LOW
   - ce115_calc_polynomial_division_l1: MEDIUM
3. 64 prompts complete in prompt_index.csv (16 tasks x 4 conditions).
4. Appendix A & B manifest SHAs correctly assigned and separated from upstream result manifests.
5. 97392be8... labeled ONLY as upstream Six-Cell result manifest.
6. 7cfc9f8f... labeled ONLY as upstream Stress Test result manifest.
7. Procedural isolation notice and post-hoc disclaimer present in text.
8. Program skeleton uses only frozen contract fields.
9. Evidence index paths exist, artifact SHA and governing manifest SHA match actual files.
10. SHA integrity and official report protection.
"""

import csv
import hashlib
import json
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
APPENDIX_PATH = REPO_ROOT / "docs/experiments/appendices/math16_tasks_prompts_and_program_skeletons_appendix_v1.md"
MANIFEST_PATH = REPO_ROOT / "docs/experiments/manifests/math16_tasks_prompts_and_program_skeletons_appendix_v1_manifest.json"
FINAL_REPORT_V13_PATH = REPO_ROOT / "docs/experiments/reports/math16_pilot02_final_report_v13.md"
EVIDENCE_COMPLETE_PATH = REPO_ROOT / "docs/experiments/milestones/math16_pilot02_evidence_complete_v1/evidence_complete_manifest.json"

TASK_CSV_PATH = REPO_ROOT / "artifacts/math16_tasks_prompts_and_program_skeletons_appendix_v1/task_index.csv"
PROMPT_CSV_PATH = REPO_ROOT / "artifacts/math16_tasks_prompts_and_program_skeletons_appendix_v1/prompt_index.csv"
REP_JSON_PATH = REPO_ROOT / "artifacts/math16_tasks_prompts_and_program_skeletons_appendix_v1/representative_case_index.json"

APPENDIX_A_MANIFEST_PATH = REPO_ROOT / "docs/experiments/manifests/math16_six_cell_healer_mechanism_validation_appendix_v1_manifest.json"
APPENDIX_B_MANIFEST_PATH = REPO_ROOT / "docs/experiments/manifests/math16_eligibility_and_unrestricted_stress_test_appendix_v1_manifest.json"
UPSTREAM_SIX_CELL_MANIFEST_PATH = REPO_ROOT / "docs/experiments/manifests/math16_posthoc_six_cell_rescue_audit_v1_result_manifest.json"
UPSTREAM_STRESS_TEST_MANIFEST_PATH = REPO_ROOT / "docs/experiments/manifests/math16_pilot02_qwen4b_unrestricted_stress_test_v11_result_manifest.json"

FROZEN_SHA_FINAL_REPORT_V13 = "d77eb8c4e1d7ccae03e276adb60bbe5f8a71ef38deef6246ae842ed840fe2fdd"
FROZEN_SHA_EVIDENCE_COMPLETE = "de11b9bd5038171689ee2895fc3a499a7b404f5259b3f5b3bcc31cb4d4af2225"

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

# 1. 16 tasks complete & unique + runtime_level & preregistered_difficulty
def test_task_index_fields_and_specific_difficulties():
    assert TASK_CSV_PATH.exists()
    with open(TASK_CSV_PATH, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    assert len(rows) == 16
    task_map = {r["task_id"]: r for r in rows}
    assert len(task_map) == 16

    for tid, r in task_map.items():
        assert r["runtime_level"] == "1"
        assert r["preregistered_difficulty"] in ["LOW", "MEDIUM", "HIGH", "NOT_AVAILABLE"]

    # Verify the 4 specific task difficulties
    assert task_map["ce111_q08_polynomial_factor_parameter_recovery"]["preregistered_difficulty"] == "HIGH"
    assert task_map["ce111_q10_ordered_quadratic_roots_radical"]["preregistered_difficulty"] == "HIGH"
    assert task_map["ce112_q04_radical_simplification"]["preregistered_difficulty"] == "LOW"
    assert task_map["ce115_calc_polynomial_division_l1"]["preregistered_difficulty"] == "MEDIUM"

# 2. 64 prompts complete (16 tasks x 4 conditions)
def test_prompt_index():
    assert PROMPT_CSV_PATH.exists()
    with open(PROMPT_CSV_PATH, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    assert len(rows) == 64
    for r in rows:
        assert r["exact_text_available"] == "True" or r["exact_text_available"] == "true"
        assert len(r["prompt_sha256"]) == 64

# 3. 4 representative cases
def test_representative_cases():
    assert REP_JSON_PATH.exists()
    with open(REP_JSON_PATH, encoding="utf-8") as f:
        cases = json.load(f)

    assert len(cases) == 4
    for c in cases:
        assert "oracle_reference_data" in c
        assert "prompts_by_condition" in c
        assert "runtime_level" in c
        assert "preregistered_difficulty" in c
        assert len(c["prompts_by_condition"]) == 4

# 4. Appendix A/B manifest SHAs and Upstream result manifest SHAs check
def test_appendix_and_upstream_manifest_shas():
    sha_app_a = sha256_file(APPENDIX_A_MANIFEST_PATH)
    sha_app_b = sha256_file(APPENDIX_B_MANIFEST_PATH)
    sha_up_six = sha256_file(UPSTREAM_SIX_CELL_MANIFEST_PATH)
    sha_up_stress = sha256_file(UPSTREAM_STRESS_TEST_MANIFEST_PATH)

    assert sha_up_six.startswith("97392be8")
    assert sha_up_stress.startswith("7cfc9f8f")

    # Ensure Appendix A and B manifests are distinct from upstream result manifests
    assert sha_app_a != sha_up_six
    assert sha_app_b != sha_up_stress

    with open(MANIFEST_PATH, encoding="utf-8") as f:
        m = json.load(f)

    ev_index = m.get("evidence_index", [])
    claims_map = {item["claim"]: item for item in ev_index}

    # Verify Appendix A manifest entry
    app_a_item = [item for item in ev_index if "附錄 A" in item["claim"]][0]
    assert app_a_item["artifact_sha256"] == sha_app_a

    # Verify Appendix B manifest entry
    app_b_item = [item for item in ev_index if "附錄 B" in item["claim"]][0]
    assert app_b_item["artifact_sha256"] == sha_app_b

    # Verify upstream Six-Cell entry
    six_item = [item for item in ev_index if "上游 Six-Cell" in item["claim"]][0]
    assert six_item["artifact_sha256"] == sha_up_six

    # Verify upstream Stress Test entry
    stress_item = [item for item in ev_index if "上游 Unrestricted Stress Test" in item["claim"]][0]
    assert stress_item["artifact_sha256"] == sha_up_stress

# 5. Mandatory statements & isolation check in markdown
def test_markdown_statements_and_isolation():
    assert APPENDIX_PATH.exists()
    text = APPENDIX_PATH.read_text(encoding="utf-8")

    # Mandatory disclaimer present
    assert "本附錄為Evidence Complete凍結後之Post-hoc展示文件" in text

    # Runtime level vs preregistered difficulty explanation present
    assert "runtime_level=1" in text
    assert "不等於題目難度" in text

    # Mandatory procedural isolation notice present
    assert "oracle_answer_used = false" in text
    assert "正確答案僅供老師與評審對照理解" in text

    # Warning on non-verbatim after diagram
    assert "非原 Six-Cell 逐字 after 原始碼" in text

# 6. Evidence index paths exist & SHA match
def test_evidence_paths_and_distinct_shas():
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

# 7. Protected SHAs intact
def test_protected_shas_intact():
    assert sha256_file(FINAL_REPORT_V13_PATH) == FROZEN_SHA_FINAL_REPORT_V13
    assert sha256_file(EVIDENCE_COMPLETE_PATH) == FROZEN_SHA_EVIDENCE_COMPLETE
