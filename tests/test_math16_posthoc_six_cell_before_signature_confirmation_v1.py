"""
tests/test_math16_posthoc_six_cell_before_signature_confirmation_v1.py
========================================================================
Test suite for SIX_CELL_BEFORE_SIGNATURE_STATIC_CONFIRMATION.

Validates before-side AST precondition static confirmation, after search closure,
draft residue clearance, SHA protection, and zero-model execution constraints.
"""

import hashlib
import json
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).parent.parent.resolve()
CONFIRMATION_DIR = REPO_ROOT / "artifacts/math16_posthoc_six_cell_before_signature_confirmation_v1"
REPORT_PATH = REPO_ROOT / "docs/experiments/reports/math16_posthoc_six_cell_before_signature_confirmation_v1.md"
MANIFEST_PATH = REPO_ROOT / "docs/experiments/manifests/math16_posthoc_six_cell_before_signature_confirmation_v1_manifest.json"
FINAL_REPORT_V13_PATH = REPO_ROOT / "docs/experiments/reports/math16_pilot02_final_report_v13.md"
EVIDENCE_COMPLETE_PATH = REPO_ROOT / "docs/experiments/milestones/math16_pilot02_evidence_complete_v1/evidence_complete_manifest.json"

FROZEN_SHA_FINAL_REPORT_V13 = "dcf6ae6ee0ac94b5896d8bc0d037ef4f06b7a3de905edf1be891022c6fd0754b"
FROZEN_SHA_EVIDENCE_COMPLETE = "de11b9bd5038171689ee2895fc3a499a7b404f5259b3f5b3bcc31cb4d4af2225"

EXPECTED_CELL_IDS = [
    "qwen3_5_4b__ce112_q04_radical_simplification__ab2g__seed_2026072004",
    "qwen3_5_4b__ce113_q01_negative_fraction_subtraction__ab2d_spec_v2__seed_2026072002",
    "qwen3_5_4b__ce113_q01_negative_fraction_subtraction__ab2g__seed_2026072003",
    "qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d__seed_2026071301",
    "qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d__seed_2026072002",
    "qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d_spec_v2__seed_2026071301",
]

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

# 1. Records count = 6
def test_confirmation_records_count():
    rec_file = CONFIRMATION_DIR / "before_signature_records.jsonl"
    assert rec_file.exists()
    records = load_jsonl(rec_file)
    assert len(records) == 6

# 2. Canonical cell_ids match
def test_canonical_cell_ids_match():
    records = load_jsonl(CONFIRMATION_DIR / "before_signature_records.jsonl")
    actual_ids = [r["canonical_cell_id"] for r in records]
    assert sorted(actual_ids) == sorted(EXPECTED_CELL_IDS)

# 3. All 6 cells have verdict CONFIRMED based on AST analysis
def test_all_six_confirmed():
    records = load_jsonl(CONFIRMATION_DIR / "before_signature_records.jsonl")
    for r in records:
        assert r["source_parseable"] is True
        assert r["single_key_payload_wrapper_present"] is True
        assert r["return_dict_key_count"] == 3
        assert "oracle_payload" in r["return_dict_keys"]
        assert r["verdict"] == "CONFIRMED"
        assert r["safe_repair_candidate"] is True
        assert r["evidence_snippet"]

# 4. After search closure table
def test_after_search_closure_table():
    after_csv = CONFIRMATION_DIR / "after_search_closure_table.csv"
    assert after_csv.exists()
    with open(after_csv, encoding="utf-8") as f:
        content = f.read()
    assert "SEARCH_CLOSED" in content

# 5. Manifest verdicts
def test_confirmation_manifest_verdicts():
    assert MANIFEST_PATH.exists()
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        manifest = json.load(f)
    verdicts = manifest.get("verdicts", [])
    assert "MATH16_SIX_CELL_BEFORE_SIGNATURE_CONFIRMATION_V1_COMPLETED" in verdicts
    assert "SIX_OF_SIX_RULE_PRECONDITIONS_CONFIRMED" in verdicts
    assert "AFTER_SOURCE_SEARCH_CLOSED" in verdicts

# 6. Report contains closure declaration and verdict
def test_report_content_and_verdict():
    assert REPORT_PATH.exists()
    with open(REPORT_PATH, encoding="utf-8") as f:
        content = f.read()
    assert "AFTER_SOURCE_SEARCH_CLOSED" in content
    assert "SIX_OF_SIX_RULE_PRECONDITIONS_CONFIRMED" in content

# 7. Draft residue search
def test_no_draft_residues_in_formal_docs():
    terms = ["Let's present", "Search Evidence Recovery", "Find Sha", "Verify All Shas", "Test Extract"]
    docs = list(REPO_ROOT.glob("docs/experiments/reports/*.md")) + list(REPO_ROOT.glob("docs/experiments/manifests/*.json"))
    for d in docs:
        txt = d.read_text(encoding="utf-8", errors="ignore")
        for t in terms:
            assert t.lower() not in txt.lower(), f"Draft residue '{t}' found in {d}"

# 8. Official SHAs unchanged
def test_official_shas_unchanged():
    assert sha256_file(FINAL_REPORT_V13_PATH) == FROZEN_SHA_FINAL_REPORT_V13
    assert sha256_file(EVIDENCE_COMPLETE_PATH) == FROZEN_SHA_EVIDENCE_COMPLETE
