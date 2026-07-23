"""
scripts/build_math16_appendix_c.py
===================================
Builder script for Appendix C:
《Math16 實驗題目、Prompt 與程式骨架展示附錄 v1》 (Errata v1.1)

Generates:
1. artifacts/math16_tasks_prompts_and_program_skeletons_appendix_v1/task_index.csv
2. artifacts/math16_tasks_prompts_and_program_skeletons_appendix_v1/prompt_index.csv
3. artifacts/math16_tasks_prompts_and_program_skeletons_appendix_v1/representative_case_index.json
4. artifacts/math16_tasks_prompts_and_program_skeletons_appendix_v1/evidence_index.json
5. docs/experiments/appendices/math16_tasks_prompts_and_program_skeletons_appendix_v1.md
6. docs/experiments/manifests/math16_tasks_prompts_and_program_skeletons_appendix_v1_manifest.json
7. docs/experiments/appendices/math16_tasks_prompts_and_program_skeletons_appendix_v1_build_report.md
"""

import csv
import hashlib
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(REPO_ROOT))

ARTIFACT_DIR = REPO_ROOT / "artifacts/math16_tasks_prompts_and_program_skeletons_appendix_v1"
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

# Load tasks
from agent_tools.finals_rebuild.math16_pool import tasks_by_id
from scripts.evaluate_math16_pilot02_full_v4 import _load_family_and_api_policy

tasks = tasks_by_id()
family_map, api_policy_map = _load_family_and_api_policy()

plan_path = REPO_ROOT / "docs/experiments/manifests/math16_pilot02_qwen4b_cell_plan.json"
with open(plan_path, encoding="utf-8") as f:
    cell_plan = json.load(f)

# Load preregistered difficulty from ab2d_spec manifest
spec_manifest_path = REPO_ROOT / "docs/experiments/prompts/ab2d_spec/manifest.json"
spec_manifest_data = json.loads(spec_manifest_path.read_text(encoding="utf-8"))
preregistered_diff_map = {}
for item in spec_manifest_data.get("tasks", []):
    tid = item.get("task_id")
    ass = item.get("assessment", {})
    diff = ass.get("difficulty", "NOT_AVAILABLE")
    preregistered_diff_map[tid] = diff

SIX_CELL_TASKS = {
    "ce112_q04_radical_simplification",
    "ce113_q01_negative_fraction_subtraction",
    "ce113_q11_rationalize_denominator",
    "ce115_calc_exact_rational_expression_l1",
    "ce115_calc_radical_simplification_l1"
}
FORCED_TASK = "ce111_q08_polynomial_factor_parameter_recovery"

# Build Task Index CSV
task_rows = []
sorted_tids = sorted(tasks.keys())
for tid in sorted_tids:
    t = tasks[tid]
    fam = family_map.get(tid, "unknown")
    api_policy = api_policy_map.get(tid, "unknown")
    otype = t.get("oracle_type", "unknown")

    in_six_cell = tid in SIX_CELL_TASKS
    in_forced = tid == FORCED_TASK
    special_role = "Six-Cell Rescued" if in_six_cell else ("Forced Ambiguity" if in_forced else "Standard Benchmark")

    prereg_diff = preregistered_diff_map.get(tid, "NOT_AVAILABLE")

    task_rows.append({
        "task_id": tid,
        "family": fam,
        "runtime_level": 1,
        "preregistered_difficulty": prereg_diff,
        "api_policy": api_policy,
        "expected_output_type": otype,
        "frozen_source_path": "agent_tools/finals_rebuild/math16_pool.py",
        "source_sha256": sha256_file(REPO_ROOT / "agent_tools/finals_rebuild/math16_pool.py"),
        "special_case_role": special_role
    })

task_csv_path = ARTIFACT_DIR / "task_index.csv"
with open(task_csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(task_rows[0].keys()))
    writer.writeheader()
    writer.writerows(task_rows)

print(f"Wrote {len(task_rows)} rows to {task_csv_path}")

# Build Prompt Index CSV (64 rows for seed 2026071301)
prompt_cells = {}
for cell in cell_plan:
    if cell["seed"] == 2026071301:
        key = (cell["task_id"], cell["condition"])
        prompt_cells[key] = cell

prompt_rows = []
for tid in sorted_tids:
    for cond in ["ab1", "ab2g", "ab2d", "ab2d_spec_v2"]:
        cell = prompt_cells[(tid, cond)]
        rel_p = cell["output_relative_path"]
        p_path = REPO_ROOT / "docs/experiments/results" / rel_p / "prompt.txt"

        if p_path.exists():
            p_text = p_path.read_text(encoding="utf-8")
            p_sha = sha256_bytes(p_text.encode("utf-8"))
            p_len = len(p_text)
            p_avail = True
            fingerprint = f"{tid}__{cond}__seed_2026071301"
        else:
            p_sha = "NOT_AVAILABLE"
            p_len = 0
            p_avail = False
            fingerprint = "NOT_AVAILABLE"

        prompt_rows.append({
            "task_id": tid,
            "condition": cond,
            "prompt_artifact_path": f"docs/experiments/results/{rel_p}/prompt.txt",
            "prompt_sha256": p_sha,
            "prompt_length": p_len,
            "frozen_fingerprint": fingerprint,
            "exact_text_available": p_avail
        })

prompt_csv_path = ARTIFACT_DIR / "prompt_index.csv"
with open(prompt_csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(prompt_rows[0].keys()))
    writer.writeheader()
    writer.writerows(prompt_rows)

print(f"Wrote {len(prompt_rows)} rows to {prompt_csv_path}")

# Build Representative Cases JSON
rep_tids = [
    "ce112_q04_radical_simplification",
    "ce113_q01_negative_fraction_subtraction",
    "ce115_calc_radical_simplification_l1",
    "ce111_q08_polynomial_factor_parameter_recovery"
]

rep_cases = []
for tid in rep_tids:
    t = tasks[tid]
    fam = family_map.get(tid)

    cond_prompts = {}
    for cond in ["ab1", "ab2g", "ab2d", "ab2d_spec_v2"]:
        cell = prompt_cells[(tid, cond)]
        rel_p = cell["output_relative_path"]
        p_path = REPO_ROOT / "docs/experiments/results" / rel_p / "prompt.txt"
        text = p_path.read_text(encoding="utf-8")
        cond_prompts[cond] = {
            "path": f"docs/experiments/results/{rel_p}/prompt.txt",
            "sha256": sha256_bytes(text.encode("utf-8")),
            "length": len(text),
            "sample_text": text[:300] + "..."
        }

    oracle_payload = t.get("oracle_payload")
    oracle_type = t.get("oracle_type")

    in_six_cell = tid in SIX_CELL_TASKS
    in_forced = tid == FORCED_TASK
    relation = "Post-hoc Rescued Cell" if in_six_cell else ("Forced Ambiguity Cell" if in_forced else "Standard Benchmark Case")

    rep_cases.append({
        "task_id": tid,
        "family": fam,
        "runtime_level": 1,
        "preregistered_difficulty": preregistered_diff_map.get(tid, "NOT_AVAILABLE"),
        "api_policy": api_policy_map.get(tid),
        "question_text": t.get("question_text", ""),
        "oracle_reference_data": {
            "oracle_payload": oracle_payload,
            "oracle_type": oracle_type,
            "isolation_notice": "評審對照資料：不進入 LLM Prompt，亦不進入 Healer 判斷輸入"
        },
        "prompts_by_condition": cond_prompts,
        "relation_to_audit_cases": relation
    })

rep_json_path = ARTIFACT_DIR / "representative_case_index.json"
with open(rep_json_path, "w", encoding="utf-8") as f:
    json.dump(rep_cases, f, ensure_ascii=False, indent=2)

print(f"Wrote representative cases to {rep_json_path}")

# Build Evidence Index JSON
evidence_items = [
    {
        "claim": "16 題任務之 runtime_level=1 來源自執行介面預設參數",
        "artifact_path": "scripts/evaluate_math16_pilot02_full_v4.py",
        "artifact_sha256": sha256_file(REPO_ROOT / "scripts/evaluate_math16_pilot02_full_v4.py"),
        "governing_manifest_path": "docs/experiments/manifests/math16_pilot02_qwen4b_cell_plan.json",
        "governing_manifest_sha256": sha256_file(REPO_ROOT / "docs/experiments/manifests/math16_pilot02_qwen4b_cell_plan.json"),
        "supports": "generate(level=1) 介面參數定義"
    },
    {
        "claim": "16 題任務之 preregistered_difficulty 來源自預註冊 Spec Manifest",
        "artifact_path": "docs/experiments/prompts/ab2d_spec/manifest.json",
        "artifact_sha256": sha256_file(REPO_ROOT / "docs/experiments/prompts/ab2d_spec/manifest.json"),
        "governing_manifest_path": "docs/experiments/manifests/math16_pilot02_qwen4b_cell_plan.json",
        "governing_manifest_sha256": sha256_file(REPO_ROOT / "docs/experiments/manifests/math16_pilot02_qwen4b_cell_plan.json"),
        "supports": "預註冊難度 (LOW / MEDIUM / HIGH) 評估來源"
    },
    {
        "claim": "附錄 A (六格 Healer 救援機制驗證附錄) 權威 Manifest 檔案與 SHA256",
        "artifact_path": "docs/experiments/manifests/math16_six_cell_healer_mechanism_validation_appendix_v1_manifest.json",
        "artifact_sha256": sha256_file(REPO_ROOT / "docs/experiments/manifests/math16_six_cell_healer_mechanism_validation_appendix_v1_manifest.json"),
        "governing_manifest_path": "docs/experiments/manifests/math16_posthoc_six_cell_rescue_audit_v1_result_manifest.json",
        "governing_manifest_sha256": sha256_file(REPO_ROOT / "docs/experiments/manifests/math16_posthoc_six_cell_rescue_audit_v1_result_manifest.json"),
        "supports": "附錄 A 權威 Manifest 索引"
    },
    {
        "claim": "附錄 B (Eligibility 與 Stress Test 驗證附錄) 權威 Manifest 檔案與 SHA256",
        "artifact_path": "docs/experiments/manifests/math16_eligibility_and_unrestricted_stress_test_appendix_v1_manifest.json",
        "artifact_sha256": sha256_file(REPO_ROOT / "docs/experiments/manifests/math16_eligibility_and_unrestricted_stress_test_appendix_v1_manifest.json"),
        "governing_manifest_path": "docs/experiments/manifests/math16_pilot02_qwen4b_unrestricted_stress_test_v11_result_manifest.json",
        "governing_manifest_sha256": sha256_file(REPO_ROOT / "docs/experiments/manifests/math16_pilot02_qwen4b_unrestricted_stress_test_v11_result_manifest.json"),
        "supports": "附錄 B 權威 Manifest 索引"
    },
    {
        "claim": "上游 Six-Cell 救援稽核正式結果 Manifest 檔案與 SHA256",
        "artifact_path": "docs/experiments/manifests/math16_posthoc_six_cell_rescue_audit_v1_result_manifest.json",
        "artifact_sha256": sha256_file(REPO_ROOT / "docs/experiments/manifests/math16_posthoc_six_cell_rescue_audit_v1_result_manifest.json"),
        "governing_manifest_path": "docs/experiments/milestones/math16_pilot02_evidence_complete_v1/evidence_complete_manifest.json",
        "governing_manifest_sha256": sha256_file(REPO_ROOT / "docs/experiments/milestones/math16_pilot02_evidence_complete_v1/evidence_complete_manifest.json"),
        "supports": "上游 Six-Cell 正式結果 Manifest"
    },
    {
        "claim": "上游 Unrestricted Stress Test v1.1 正式結果 Manifest 檔案與 SHA256",
        "artifact_path": "docs/experiments/manifests/math16_pilot02_qwen4b_unrestricted_stress_test_v11_result_manifest.json",
        "artifact_sha256": sha256_file(REPO_ROOT / "docs/experiments/manifests/math16_pilot02_qwen4b_unrestricted_stress_test_v11_result_manifest.json"),
        "governing_manifest_path": "docs/experiments/milestones/math16_pilot02_evidence_complete_v1/evidence_complete_manifest.json",
        "governing_manifest_sha256": sha256_file(REPO_ROOT / "docs/experiments/milestones/math16_pilot02_evidence_complete_v1/evidence_complete_manifest.json"),
        "supports": "上游 Stress Test v1.1 正式結果 Manifest"
    }
]

evidence_json_path = ARTIFACT_DIR / "evidence_index.json"
with open(evidence_json_path, "w", encoding="utf-8") as f:
    json.dump(evidence_items, f, ensure_ascii=False, indent=2)

print(f"Wrote evidence index to {evidence_json_path}")
