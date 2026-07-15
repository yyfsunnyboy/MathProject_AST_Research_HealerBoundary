import os
import json
import pytest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CORRECTED_DIR = ROOT / "docs" / "experiments" / "results" / "ce115_corrected_context_formal_run"

def test_census_counts():
    census_path = CORRECTED_DIR / "ce115_corrected_census.json"
    assert census_path.exists(), "ce115_corrected_census.json does not exist"
    
    with open(census_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    assert data["total_records_analyzed"] == 72
    assert data["natural_completions_analyzed"] == 50
    assert data["degeneration_completions_analyzed"] == 22

def test_taxonomy_exclusions_and_families():
    taxonomy_path = CORRECTED_DIR / "ce115_corrected_taxonomy.json"
    assert taxonomy_path.exists(), "ce115_corrected_taxonomy.json does not exist"
    
    with open(taxonomy_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    failures = data["failures"]
    assert len(failures) == 63, "Should be exactly 63 failures (72 total - 9 passed)"
    
    primary_counts = data["primary_counts"]
    assert primary_counts["MODEL_DEGENERATIVE_NONTERMINATION"] == 22, "Exactly 22 degenerative failures"
    
    # Assert every failed cell has exactly one primary failure family
    for f in failures:
        assert f["primary_failure_family"] is not None
        assert f["primary_failure_family"] in primary_counts
        
        # Verify passed cells are not present in taxonomy failures list
        assert "evaluator outcome: passed" not in f["evidence_references"]

def test_healer_candidate_pool_governance():
    pool_path = CORRECTED_DIR / "ce115_corrected_healer_candidate_pool.json"
    assert pool_path.exists(), "ce115_corrected_healer_candidate_pool.json does not exist"
    
    with open(pool_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    assert data["total_candidates_analyzed"] == 63
    counts = data["governance_tier_counts"]
    assert counts["SAFE_HISTORICAL_CANDIDATE"] == 11
    assert counts["ABSTAIN"] == 52
    assert counts["MINIMAL_CORE_CANDIDATE"] == 0
    assert counts["EXPLORATORY_ONLY"] == 0
    assert counts["INSUFFICIENT_EVIDENCE"] == 0
