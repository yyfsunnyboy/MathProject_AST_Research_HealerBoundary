"""
tests/test_math16_posthoc_six_cell_before_after_recovery_v1.py
================================================================
Test suite for SIX_CELL_BEFORE_AFTER_EVIDENCE_RECOVERY_AUDIT.

Validates evidence recovery counts, cell identities, confidence classifications,
SHA integrity, and zero-model execution constraints.
"""

import hashlib
import json
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).parent.parent.resolve()
RECOVERY_DIR = REPO_ROOT / "artifacts/math16_posthoc_six_cell_before_after_recovery_v1"
REPORT_PATH = REPO_ROOT / "docs/experiments/reports/math16_posthoc_six_cell_before_after_recovery_v1.md"
MANIFEST_PATH = REPO_ROOT / "docs/experiments/manifests/math16_posthoc_six_cell_before_after_recovery_v1_manifest.json"
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

# 1. Recovery records count = 6
def test_recovery_records_count():
    rec_file = RECOVERY_DIR / "recovery_records.jsonl"
    assert rec_file.exists()
    records = load_jsonl(rec_file)
    assert len(records) == 6

# 2. Canonical cell_ids match Six-Cell Audit
def test_canonical_cell_ids_match():
    records = load_jsonl(RECOVERY_DIR / "recovery_records.jsonl")
    actual_ids = [r["canonical_cell_id"] for r in records]
    assert sorted(actual_ids) == sorted(EXPECTED_CELL_IDS)

# 3. Clear recovery status per cell
def test_recovery_status_per_cell():
    records = load_jsonl(RECOVERY_DIR / "recovery_records.jsonl")
    for r in records:
        assert r["before_source_recovered"] is True
        assert r["after_source_recovered"] is False
        assert r["reconstruct_unified_diff_possible"] is False

# 4. No cell marked as EXACT
def test_no_exact_confidence():
    records = load_jsonl(RECOVERY_DIR / "recovery_records.jsonl")
    for r in records:
        assert r["evidence_confidence"] != "EXACT"

# 5. Recovered source files exist and SHAs match
def test_recovered_sources_files():
    sources_dir = RECOVERY_DIR / "recovered_sources"
    assert sources_dir.exists()
    records = load_jsonl(RECOVERY_DIR / "recovery_records.jsonl")
    for r in records:
        cid = r["canonical_cell_id"]
        src_file = sources_dir / f"{cid}__before.py"
        assert src_file.exists(), f"Missing recovered source file for {cid}"
        sha = sha256_file(src_file)
        assert sha == r["source_sha"]

# 6. Incremental Post-hoc cell separately identified
def test_incremental_cell_identification():
    records = load_jsonl(RECOVERY_DIR / "recovery_records.jsonl")
    incremental = [r for r in records if r.get("is_incremental_posthoc_pass")]
    assert len(incremental) == 1
    assert incremental[0]["canonical_cell_id"] == "qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d__seed_2026071301"
    assert incremental[0]["before_source_recovered"] is True

# 7. Manifest verdicts and no-exact status
def test_recovery_manifest_verdicts():
    assert MANIFEST_PATH.exists()
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        manifest = json.load(f)
    verdicts = manifest.get("verdicts", [])
    assert "MATH16_SIX_CELL_BEFORE_AFTER_RECOVERY_V1_COMPLETED" in verdicts
    assert "NO_EXACT_SOURCE_DIFF_RECOVERED" in verdicts
    assert "RULE_LEVEL_MECHANISM_ONLY" in verdicts

# 8. Report includes mandatory teacher-facing disclaimer tag
def test_report_teacher_facing_disclaimer():
    assert REPORT_PATH.exists()
    with open(REPORT_PATH, encoding="utf-8") as f:
        content = f.read()
    assert "機制示意，非逐字還原之原始程式碼。" in content

# 9. Official source SHAs unchanged
def test_official_shas_unchanged():
    assert sha256_file(FINAL_REPORT_V13_PATH) == FROZEN_SHA_FINAL_REPORT_V13
    assert sha256_file(EVIDENCE_COMPLETE_PATH) == FROZEN_SHA_EVIDENCE_COMPLETE
