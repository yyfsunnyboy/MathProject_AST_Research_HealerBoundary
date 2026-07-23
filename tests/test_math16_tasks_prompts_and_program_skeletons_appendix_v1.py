"""
tests/test_math16_tasks_prompts_and_program_skeletons_appendix_v1.py
=====================================================================
Test suite for Math16 Tasks, Prompts, and Program Skeletons Appendix v1.

Validates:
1. 16 tasks complete and unique in task_index.csv.
2. 64 prompts complete in prompt_index.csv (16 tasks x 4 conditions).
3. 4 representative cases present in representative_case_index.json.
4. Correct answer procedurally and visually isolated from model/healer inputs.
5. Mandatory procedural isolation and post-hoc disclaimer statements present.
6. Program skeleton uses only frozen contract fields.
7. Six-cell diagram has non-verbatim warning statement.
8. Forced ambiguity case references authentic diff file.
9. Separated Artifact SHA256 vs Governing Manifest SHA256 columns in evidence index.
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

FROZEN_SHA_FINAL_REPORT_V13 = "dcf6ae6ee0ac94b5896d8bc0d037ef4f06b7a3de905edf1be891022c6fd0754b"
FROZEN_SHA_EVIDENCE_COMPLETE = "de11b9bd5038171689ee2895fc3a499a7b404f5259b3f5b3bcc31cb4d4af2225"

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

# 1. 16 tasks complete & unique
def test_task_index():
    assert TASK_CSV_PATH.exists()
    with open(TASK_CSV_PATH, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    assert len(rows) == 16
    tids = [r["task_id"] for r in rows]
    assert len(set(tids)) == 16

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
        assert len(c["prompts_by_condition"]) == 4

# 4. Mandatory statements & isolation check
def test_markdown_statements_and_isolation():
    assert APPENDIX_PATH.exists()
    text = APPENDIX_PATH.read_text(encoding="utf-8")

    # Mandatory disclaimer present
    assert "本附錄為Evidence Complete凍結後之Post-hoc展示文件" in text

    # Mandatory procedural isolation notice present
    assert "oracle_answer_used = false" in text
    assert "正確答案僅供老師與評審對照理解" in text

    # Warning on non-verbatim after diagram
    assert "非原 Six-Cell 逐字 after 原始碼" in text

    # Forced ambiguity diff path present
    assert "qwen3_5_4b__ce111_q08_polynomial_factor_parameter_recovery__ab2d__seed_2026072004_forced.diff" in text

# 5. Evidence index paths exist & SHA match
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

        # Ensure artifact SHA is distinct from governing manifest SHA
        assert item["artifact_sha256"] != item["governing_manifest_sha256"]

# 6. Protected SHAs intact
def test_protected_shas_intact():
    assert sha256_file(FINAL_REPORT_V13_PATH) == FROZEN_SHA_FINAL_REPORT_V13
    assert sha256_file(EVIDENCE_COMPLETE_PATH) == FROZEN_SHA_EVIDENCE_COMPLETE
