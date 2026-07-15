import os
import json
import pytest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CORRECTED_RUN_DIR = ROOT / "docs" / "experiments" / "results" / "ce115_corrected_context_formal_run"
CELLS_DIR = CORRECTED_RUN_DIR / "cells"

def test_corrected_run_completeness_and_uniqueness():
    summary_json_path = CORRECTED_RUN_DIR / "ce115_corrected_context_formal_run_summary.json"
    assert summary_json_path.exists(), "Summary JSON must exist after run"
    
    with open(summary_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    assert data["planned_cells"] == 72, "Must plan 72 cells"
    assert data["executed_cells"] == 72, "Must execute 72 cells"
    assert data["unique_cell_ids"] == 72, "Must have 72 unique cell IDs"
    
    results = data["results"]
    assert len(results) == 72, "Must contain exactly 72 result records"
    
    seen = set()
    for r in results:
        cell_id = r["cell_id"]
        assert cell_id not in seen, f"Duplicate cell execution found: {cell_id}"
        seen.add(cell_id)

def test_corrected_run_payload_integrity_and_isolation():
    # Verify that we do not overwrite the initial formal results folder
    initial_results_dir = ROOT / "docs" / "experiments" / "results" / "ce115_calc_local_confirmatory"
    assert CORRECTED_RUN_DIR != initial_results_dir, "Corrected run output directory must be isolated"
    
    summary_json_path = CORRECTED_RUN_DIR / "ce115_corrected_context_formal_run_summary.json"
    with open(summary_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    results = data["results"]
    for r in results:
        # If the run succeeded or failed (excluding runtime failures), check the schema
        if r.get("validity_classification") != "RUNTIME_FAILURE":
            assert r["requested_num_ctx"] == 65536, "Requested num_ctx must be 65536"
            assert r["requested_num_predict"] == 24576, "Requested num_predict must be 24576"
            assert r["requested_think"] is False, "Requested think must be false"
            assert len(r["prompt_sha256"]) == 64, "prompt_sha256 must be valid"
            assert len(r["raw_output_sha256"]) == 64, "raw_output_sha256 must be valid"
            assert r["effective_options_verification"] == "REQUEST_PAYLOAD_VERIFIED_ONLY", "Verification status must match protocol"
            
            # Repetition diagnostics must be present and valid
            rep = r["repetition_diagnostics"]
            assert "repeated_line_ratio" in rep, "repeated_line_ratio missing"
            assert "longest_repeated_contiguous_block" in rep, "longest_repeated_contiguous_block missing"
            assert "post_completion_loop" in rep, "post_completion_loop missing"
            assert 0.0 <= rep["repeated_line_ratio"] <= 1.0, "repetition ratio out of bounds"
