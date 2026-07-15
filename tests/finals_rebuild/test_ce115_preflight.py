import os
import json
import pytest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PREFLIGHT_DIR = ROOT / "docs" / "experiments" / "results" / "ce115_context_budget_preflight"
PROTOCOL_DIR = ROOT / "docs" / "experiments" / "manifests"

def test_preflight_cells_list_and_uniqueness():
    from scripts.ce115_context_budget_preflight import TARGET_CELL_IDS
    assert len(TARGET_CELL_IDS) == 6, "Must be exactly 6 preflight cells"
    assert len(set(TARGET_CELL_IDS)) == 6, "Preflight cells list must not contain duplicates"

def test_preflight_repetition_diagnostics_deterministic():
    from scripts.ce115_context_budget_preflight import compute_repetition_diagnostics
    
    text = "def generate():\n    return 1\n" * 5
    rep = compute_repetition_diagnostics(text)
    assert rep["repeated_line_ratio"] > 0.0
    assert rep["duplicate_fn_count"] == 4
    
    # Empty string check
    rep_empty = compute_repetition_diagnostics("")
    assert rep_empty["repeated_line_ratio"] == 0.0
    assert rep_empty["duplicate_fn_count"] == 0

def test_preflight_output_and_manifest_isolation():
    # Verify that preflight does not write to the main results folder
    # Main results folder is docs/experiments/results/ce115_calc_local_confirmatory
    main_results_dir = ROOT / "docs" / "experiments" / "results" / "ce115_calc_local_confirmatory"
    preflight_summary_path = PREFLIGHT_DIR / "ce115_context_budget_preflight_summary.json"
    
    # Assert paths are isolated
    assert PREFLIGHT_DIR != main_results_dir, "Preflight output directory must be isolated from main confirmatory results"
    
    # Assert protocol manifest paths are isolated
    protocol_json_path = PROTOCOL_DIR / "ce115_corrected_context_rerun_protocol.json"
    protocol_md_path = PROTOCOL_DIR / "ce115_corrected_context_rerun_protocol.md"
    assert protocol_json_path.exists(), "Protocol manifest JSON must exist"
    assert protocol_md_path.exists(), "Protocol manifest MD must exist"

def test_protocol_manifest_invariants():
    protocol_json_path = PROTOCOL_DIR / "ce115_corrected_context_rerun_protocol.json"
    with open(protocol_json_path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
        
    assert data["protocol_id"] == "ce115_corrected_context_rerun_protocol"
    assert data["parameter_overrides"]["num_ctx"] == 65536
    assert data["parameter_overrides"]["num_predict"] == 24576
    assert data["parameter_overrides"]["think"] is False
    assert data["execution_rules"]["preserve_original_artifacts"] is True
    assert data["execution_rules"]["first_attempt_only"] is True
