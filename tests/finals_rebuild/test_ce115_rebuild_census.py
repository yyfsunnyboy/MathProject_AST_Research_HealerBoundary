import os
import json
import pytest

REBUILT_JSON_PATH = r"C:\Projects\MathProject_AST_Research_HealerBoundary\docs\experiments\reports\ce115_safe_generic_rule_matrix_rebuilt.json"
CENSUS_JSON_PATH = r"C:\Projects\MathProject_AST_Research_HealerBoundary\docs\experiments\reports\ce115_historical_output_budget_census.json"

def test_rebuilt_matrix_completeness_and_uniqueness():
    assert os.path.exists(REBUILT_JSON_PATH), "Rebuilt matrix JSON file must exist"
    with open(REBUILT_JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    assert data["unique_cells_count"] == 18, "Must contain exactly 18 unique cells"
    assert data["total_entries_count"] == 72, "Must contain exactly 72 entries (18 cells * 4 rules)"
    
    matrix = data["matrix"]
    assert len(matrix) == 72, "Matrix length must be 72"
    
    # Check uniqueness of entries (cell_id + rule_id)
    seen = set()
    for entry in matrix:
        key = (entry["cell_id"], entry["rule_id"])
        assert key not in seen, f"Duplicate matrix entry found: {key}"
        seen.add(key)
        
    assert len(seen) == 72, "Must have 72 distinct (cell_id, rule_id) pairs"

def test_rebuilt_matrix_hashes_and_negative_evidence():
    with open(REBUILT_JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    matrix = data["matrix"]
    for entry in matrix:
        # Each entry must have artifact relative path and hashes
        assert entry["artifact_relative_path"].startswith("docs/experiments/results/ce115_calc_local_confirmatory/"), "Path must be correct"
        assert len(entry["artifact_sha256"]) == 64, "Must have valid artifact_sha256"
        assert len(entry["raw_output_sha256"]) == 64, "Must have valid raw_output_sha256"
        
        # Negative evidence validation for NOT_APPLICABLE
        if entry["classification"] == "NOT_APPLICABLE":
            assert entry["scan_executed"] is True, "scan_executed must be True"
            assert entry["match_count"] == 0, "match_count must be 0 for NOT_APPLICABLE"
            assert "searched_pattern_classes" in entry, "NOT_APPLICABLE must document searched pattern classes"
            assert len(entry["searched_pattern_classes"]) > 0, "searched_pattern_classes must not be empty"
            assert len(entry["reason"]) > 0, "reason must be documented"

def test_rebuilt_matrix_lexical_scanners_verdict():
    with open(REBUILT_JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    matrix = data["matrix"]
    
    # 8 leakage cells must have UNSAFE_CORE_LOGIC for R03
    leakage_cells = {
        "qwen3_5_4b__ce115_calc_exact_rational_expression_l1__ab1__seed_2026071301",
        "qwen3_5_9b__ce115_calc_exact_rational_expression_l1__ab1__seed_2026071302",
        "qwen3_5_9b__ce115_calc_polynomial_division_l1__ab1__seed_2026071301",
        "qwen3_5_9b__ce115_calc_polynomial_division_l1__ab1__seed_2026071302",
        "qwen3_5_9b__ce115_calc_polynomial_division_l1__ab1__seed_2026071303",
        "qwen3_5_9b__ce115_calc_polynomial_division_l1__ab2d__seed_2026071302",
        "qwen3_5_9b__ce115_calc_polynomial_division_l1__ab2g__seed_2026071301",
        "qwen3_5_9b__ce115_calc_polynomial_factor_roots_l1__ab2d__seed_2026071301"
    }
    
    # 3 truncated cells must have UNSAFE_TRUNCATION for R02 and R03
    truncated_cells = {
        "qwen3_5_4b__ce115_calc_radical_simplification_l1__ab1__seed_2026071303",
        "qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2g__seed_2026071301",
        "qwen3_5_9b__ce115_calc_polynomial_division_l1__ab2g__seed_2026071302"
    }

    for entry in matrix:
        cell_id = entry["cell_id"]
        rule_id = entry["rule_id"]
        cls = entry["classification"]
        
        if cell_id in leakage_cells and rule_id == "R03_thinking_leakage_removal":
            assert cls == "UNSAFE_CORE_LOGIC", f"{cell_id} + R03 must be UNSAFE_CORE_LOGIC"
            assert entry["match_count"] > 0, "match_count must be > 0"
        elif cell_id in truncated_cells and rule_id in ("R02_trailing_artifact_removal", "R03_thinking_leakage_removal"):
            assert cls == "UNSAFE_TRUNCATION", f"{cell_id} + {rule_id} must be UNSAFE_TRUNCATION"
            assert entry["match_count"] == 0, "match_count must be 0 for truncated cell"
        elif cell_id == "qwen3_5_9b__ce115_calc_polynomial_factor_roots_l1__ab1__seed_2026071301" and rule_id == "R03_thinking_leakage_removal":
            assert cls == "INSUFFICIENT_EVIDENCE", "Must be INSUFFICIENT_EVIDENCE for English conversational leakage"

def test_historical_census_telemetry_integrity():
    assert os.path.exists(CENSUS_JSON_PATH), "Historical census JSON file must exist"
    with open(CENSUS_JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    records = data["records"]
    assert len(records) > 0, "Must have scanned historical records"
    
    # Check that bytes are not passed off as raw tokens
    for r in records:
        assert "level_b_metrics" in r, "Must have level_b_metrics"
        assert r["level_b_metrics"]["tag"] == "ESTIMATED_FROM_TEXT_SIZE_NOT_RUNTIME_TOKEN_COUNT", "Must tag estimated metrics"
        
        # Verify prompt_eval_count / eval_count are parsed telemetry or None, never file size
        if r["eval_count"] is not None:
            assert r["eval_count"] != r["file_size_bytes"], "eval_count must not equal file size bytes"

def test_historical_census_truncated_exclusion():
    with open(CENSUS_JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    records = data["records"]
    stats = data["level_a_statistics"]
    
    # Number of natural completions analyzed
    natural_count = data["natural_completions_analyzed"]
    
    # Verify that truncated files are excluded from natural statistics
    truncated_paths = [r["source_path"] for r in records if r["suspected_truncation"] is True]
    assert len(truncated_paths) >= 4, "Must have at least 4 truncated records (1 Qwen3 + 3 Qwen3.5)"
    
    overall_n = stats["overall"]["n"]
    assert overall_n == natural_count, "Overall statistic N must equal natural completions count"
    
    # Verify percentile logic
    p50 = stats["overall"]["median"]
    p90 = stats["overall"]["P90"]
    p95 = stats["overall"]["P95"]
    p99 = stats["overall"]["P99"]
    max_val = stats["overall"]["max"]
    
    assert p50 <= p90 <= p95 <= p99 <= max_val, "Percentiles must be monotonically increasing"
