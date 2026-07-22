"""
tests/test_math16_posthoc_six_cell_rescue_audit_v1_results.py
===============================================================
Comprehensive Result Test Suite for Math16 Post-hoc Six-Cell Rescue Mechanism Audit.

Validates all formal output artifacts, set relations, crosstabs, disclaimers,
SHA protection, and zero-model execution constraints.
"""

import csv
import hashlib
import json
import re
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).parent.parent.resolve()
FORMAL_DIR = REPO_ROOT / "artifacts/math16_posthoc_six_cell_rescue_audit_v1/formal"
REPORT_MD_PATH = REPO_ROOT / "docs/experiments/reports/math16_posthoc_six_cell_rescue_audit_v1.md"
RESULT_MANIFEST_PATH = REPO_ROOT / "docs/experiments/manifests/math16_posthoc_six_cell_rescue_audit_v1_result_manifest.json"
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

# 1. Formal records has exactly 6 cells
def test_formal_records_count():
    records_file = FORMAL_DIR / "six_cell_audit_records.jsonl"
    assert records_file.exists(), f"Missing {records_file}"
    records = load_jsonl(records_file)
    assert len(records) == 6, f"Expected 6 records, got {len(records)}"

# 2. Condition distribution is 2 / 2 / 2 / 0
def test_condition_distribution():
    records = load_jsonl(FORMAL_DIR / "six_cell_audit_records.jsonl")
    cond_counts = {}
    for r in records:
        cond = r["condition"]
        cond_counts[cond] = cond_counts.get(cond, 0) + 1

    assert cond_counts.get("Ab2g", 0) == 2
    assert cond_counts.get("Ab2d+api", 0) == 2
    assert cond_counts.get("Ab2d+spec", 0) == 2
    assert cond_counts.get("Ab1", 0) == 0
    assert sum(cond_counts.values()) == 6

# 3. Family distribution is 4 / 2 / 0 / 0
def test_family_distribution():
    records = load_jsonl(FORMAL_DIR / "six_cell_audit_records.jsonl")
    fam_counts = {}
    for r in records:
        fam = r["family"]
        fam_counts[fam] = fam_counts.get(fam, 0) + 1

    assert fam_counts.get("radical", 0) == 4
    assert fam_counts.get("fraction", 0) == 2
    assert fam_counts.get("integer", 0) == 0
    assert fam_counts.get("polynomial", 0) == 0
    assert sum(fam_counts.values()) == 6

# 4. Primary rescued = 5, Post-hoc rescued = 6, difference = 1
def test_rescue_set_relation():
    records = load_jsonl(FORMAL_DIR / "six_cell_audit_records.jsonl")
    primary_rescued = [r for r in records if r["primary_is_rescued"]]
    posthoc_rescued = [r for r in records if r["posthoc_is_rescued"]]
    incremental = [r for r in records if r["is_incremental_posthoc_pass"]]

    assert len(primary_rescued) == 5
    assert len(posthoc_rescued) == 6
    assert len(incremental) == 1
    assert incremental[0]["cell_id"] == "qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d__seed_2026071301"

# 5. Corrected-chain accounting = 10 / 8 / 2 / 1
def test_corrected_chain_accounting():
    comparison_path = REPO_ROOT / "docs/experiments/results/math16_pilot02_qwen4b_healer_v4_posthoc_corrected_chain_r001/primary_vs_corrected_chain_comparison.json"
    assert comparison_path.exists()
    with open(comparison_path, encoding="utf-8") as f:
        comp = json.load(f)

    assert comp.get("replayed") == 10
    assert comp.get("same_as_primary") == 8
    assert comp.get("changed_vs_primary") == 2
    assert (comp.get("corrected_rescued") - comp.get("primary_rescued")) == 1

# 6. All 6 cells have oracle_answer_used = false
def test_oracle_answer_used_false():
    records = load_jsonl(FORMAL_DIR / "six_cell_audit_records.jsonl")
    for r in records:
        assert r.get("oracle_answer_used") is False

# 7. Every cell has hashes and evidence path
def test_cell_hashes_and_evidence():
    records = load_jsonl(FORMAL_DIR / "six_cell_audit_records.jsonl")
    for r in records:
        assert r.get("before_snippet_hash")
        assert r.get("after_snippet_hash")
        assert r.get("evidence_citation")

# 8. Taxonomy values are valid
def test_taxonomy_validity():
    valid_conditions = {"Ab1", "Ab2g", "Ab2d+api", "Ab2d+spec"}
    valid_families = {"integer", "polynomial", "radical", "fraction"}
    valid_layers = {"L1_PARSE_SYNTAX", "L2_CONTRACT_SCHEMA_ENTRYPOINT", "L3_DOMAIN_API", "L4_RUNTIME_EXECUTION", "L5_SEMANTIC_ANSWER"}

    records = load_jsonl(FORMAL_DIR / "six_cell_audit_records.jsonl")
    for r in records:
        assert r["condition"] in valid_conditions
        assert r["family"] in valid_families
        assert r["root_mechanism_layer"] in valid_layers

# 9. All crosstabs sum back to 6
def test_crosstabs_sum_to_6():
    # condition_family_crosstab
    cf_file = FORMAL_DIR / "condition_family_crosstab.csv"
    assert cf_file.exists()
    with open(cf_file, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        totals = [int(row["Total"]) for row in reader]
        assert sum(totals) == 6

    # condition_failure_layer_crosstab
    cfl_file = FORMAL_DIR / "condition_failure_layer_crosstab.csv"
    assert cfl_file.exists()
    with open(cfl_file, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        totals = [int(row["Total"]) for row in reader]
        assert sum(totals) == 6

    # condition_rule_crosstab
    cr_file = FORMAL_DIR / "condition_rule_crosstab.csv"
    assert cr_file.exists()
    with open(cr_file, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        totals = [int(row["Total"]) for row in reader]
        assert sum(totals) == 6

# 10. Denominator table matches official artifacts
def test_denominator_table():
    cd_file = FORMAL_DIR / "condition_denominator_table.csv"
    assert cd_file.exists()
    with open(cd_file, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert len(rows) == 5  # 4 conditions + Total
        total_row = rows[-1]
        assert total_row["Condition"] == "Total (Qwen4B)"
        assert int(total_row["Total Cells"]) == 320
        assert int(total_row["Baseline PASS"]) == 78
        assert int(total_row["Baseline FAIL"]) == 242
        assert int(total_row["Eligible"]) == 10
        assert int(total_row["Primary Rescued"]) == 5
        assert int(total_row["Post-hoc Rescued"]) == 6

# 11. Report contains mandatory disclaimer and limitations
def test_report_disclaimer_and_limitations():
    assert REPORT_MD_PATH.exists()
    with open(REPORT_MD_PATH, encoding="utf-8") as f:
        content = f.read()

    assert "本分析為Evidence Complete凍結後之Post-hoc補充稽核，不修改、取代或重新解釋既有Primary與正式Post-hoc結果。" in content or "本分析為 Evidence Complete 凍結後之 Post-hoc 補充稽核，不修改、取代或重新解釋既有 Primary 與正式 Post-hoc 結果。" in content
    assert "解讀限制" in content or "Limitations" in content

# 12. Official source SHAs remain unchanged
def test_official_shas_unchanged():
    assert sha256_file(FINAL_REPORT_V13_PATH) == FROZEN_SHA_FINAL_REPORT_V13
    assert sha256_file(EVIDENCE_COMPLETE_PATH) == FROZEN_SHA_EVIDENCE_COMPLETE

# 13. Verdict strings present
def test_result_manifest_verdicts():
    assert RESULT_MANIFEST_PATH.exists()
    with open(RESULT_MANIFEST_PATH, encoding="utf-8") as f:
        manifest = json.load(f)

    verdicts = manifest.get("verdicts", [])
    assert "MATH16_SIX_CELL_RESCUE_MECHANISM_AUDIT_V1_COMPLETED" in verdicts
    assert "READY_FOR_UNRESTRICTED_STRESS_TEST_PREREGISTRATION" in verdicts
