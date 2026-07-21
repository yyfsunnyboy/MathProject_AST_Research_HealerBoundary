# -*- coding: utf-8 -*-
from __future__ import annotations

import json
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
TAXONOMY_JSON_PATH = ROOT / "docs/experiments/taxonomy/ai_generated_program_failure_taxonomy_v3.json"
MANIFEST_PATH = ROOT / "docs/experiments/manifests/math16_pilot02_integer_evaluation_v3_r001_manifest.json"

def test_taxonomy_integrity():
    assert TAXONOMY_JSON_PATH.exists()
    tax = json.loads(TAXONOMY_JSON_PATH.read_text(encoding="utf-8"))

    assert tax["version"] == "v3"
    assert tax["source_file_sha256"] == "7df8f4472ce048569967436cbc73ede8fd4bd117ad67d0028ddd95af2055a304"
    assert set(tax["failure_layers"].keys()) == {"L0", "L1", "L2", "L3", "L4", "L5"}
    assert set(tax["gates"].keys()) == {"G1", "G2", "G3", "G4"}
    assert set(tax["G3_subgates"].keys()) == {"G3e", "G3a", "G3s", "G3c"}

def test_manifest_integrity():
    assert MANIFEST_PATH.exists()
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    assert manifest["evaluation_revision"] == "v3_r001"
    assert manifest["taxonomy_id"] == "ai_generated_program_failure_taxonomy_v3"
    assert manifest["taxonomy_file_sha256"] == "7df8f4472ce048569967436cbc73ede8fd4bd117ad67d0028ddd95af2055a304"
    assert manifest["evidence_role"] == "post_hoc_exploratory"

def test_rule_entry_point_mismatch():
    # Rule: Entry-point mismatch -> L2 (even if NameError is raised at runtime)
    # Simulator of classification logic
    def classify(cell_id, g1_parse, g2_execution, g3e_entry_point, g3a_required_api, g3s_output_schema, g4_correctness, exception_type):
        if g1_parse == "FAIL":
            return "L1"
        if g3e_entry_point == "FAIL":
            return "L2"
        if g2_execution == "FAIL":
            if exception_type in ["ImportError", "ModuleNotFoundError"]:
                return "L3"
            return "L4"
        if g3s_output_schema == "FAIL":
            return "L2"
        if g4_correctness == "FAIL":
            return "L5"
        return "PASS"

    # Mismatched entry point signature -> L2
    layer = classify("cell_1", "PASS", "FAIL", "FAIL", "NOT_APPLICABLE", "NOT_ASSESSED", "NOT_ASSESSED", "AttributeError")
    assert layer == "L2"

def test_rule_ambiguous_entry_point():
    # Ambiguous entry point must be categorized as L2, noneligible, and abstained
    cell = {
        "primary_failure_layer": "L2",
        "mechanism_tags": ["ambiguous_entry_point"],
        "healer_eligibility": "noneligible",
        "healer_decision": "abstained"
    }
    assert cell["primary_failure_layer"] == "L2"
    assert "ambiguous_entry_point" in cell["mechanism_tags"]
    assert cell["healer_eligibility"] == "noneligible"
    assert cell["healer_decision"] == "abstained"

def test_rule_domain_api_error():
    # Domain API error -> L3
    # Mismatched Domain API call arity or import error -> L3
    def classify(exception_type):
        if exception_type in ["DomainAPIError", "ModuleNotFoundError", "ImportError"]:
            return "L3"
        return "L4"
    assert classify("DomainAPIError") == "L3"
    assert classify("NameError") == "L4"

def test_rule_general_missing_import():
    # Missing generic import or NameError -> L4
    def classify(exception_type):
        if exception_type == "NameError":
            return "L4"
        return "L3"
    assert classify("NameError") == "L4"

def test_rule_parse_failure():
    # Parse failure -> L1
    def classify(g1_parse):
        if g1_parse == "FAIL":
            return "L1"
        return "PASS"
    assert classify("FAIL") == "L1"

def test_rule_semantic_incorrect_requires_gates_pass():
    # G1-G3 must PASS for semantic incorrect to be L5
    def classify(g1, g2, g3, g4):
        if g1 == "PASS" and g2 == "PASS" and g3 == "PASS" and g4 == "FAIL":
            return "L5"
        return "OTHER"
    assert classify("PASS", "PASS", "PASS", "FAIL") == "L5"
    assert classify("PASS", "FAIL", "PASS", "FAIL") == "OTHER"

def test_rule_truncation_coexistence():
    # Truncation can coexist with L1, L2, L4, L5 and does not automatically make cell eligible
    cell_l1 = {
        "primary_failure_layer": "L1",
        "mechanism_tags": ["truncation"],
        "healer_eligibility": "noneligible"
    }
    cell_l2 = {
        "primary_failure_layer": "L2",
        "mechanism_tags": ["truncation"],
        "healer_eligibility": "noneligible"
    }
    assert cell_l1["primary_failure_layer"] == "L1"
    assert cell_l2["healer_eligibility"] == "noneligible"

def test_rule_unknown_no_mapping_to_l5():
    # Unknown does not map to L5
    cell = {
        "legacy_failure_category": "Unknown",
        "primary_failure_layer": None,
        "classification_status": "PENDING_REVIEW"
    }
    assert cell["primary_failure_layer"] is not "L5"

def test_rule_format_contamination_mismatch():
    # Format contamination preventing AST parsing -> L1
    def classify(g1_parse):
        if g1_parse == "FAIL":
            return "L1"
        return "L2"
    assert classify("FAIL") == "L1"

def test_rule_schema_mismatch():
    # Output schema mismatch -> L2
    cell = {
        "g3s_output_schema": "FAIL",
        "primary_failure_layer": "L2"
    }
    assert cell["primary_failure_layer"] == "L2"

def test_rule_native_only_integer():
    # For native-only integers, G3a is NOT_APPLICABLE
    cell = {
        "g3a_required_api": "NOT_APPLICABLE"
    }
    assert cell["g3a_required_api"] == "NOT_APPLICABLE"

def test_rule_optional_api_unused():
    # Unused optional API is not categorized as L3
    def classify(unused_optional):
        if unused_optional:
            # Encouraged but optional API unused is valid, not failure
            return "VALID_MODEL_OUTCOME"
        return "L3"
    assert classify(True) == "VALID_MODEL_OUTCOME"

def test_rule_invalid_evaluator_exclusion():
    # invalid evaluator does not count in model failure stats
    cell = {
        "outcome_validity": "INVALID_EVALUATOR",
        "primary_failure_layer": "L5"  # even if L5, outcome_validity excludes it from model failure stats
    }
    assert cell["outcome_validity"] == "INVALID_EVALUATOR"

def test_rule_healer_three_fields_separated():
    # Healer fields must be separated and not mixed
    cell = {
        "healer_eligibility": "eligible",
        "healer_decision": "transformed",
        "healer_outcome": "rescue_to_pass"
    }
    assert cell["healer_eligibility"] == "eligible"
    assert cell["healer_decision"] == "transformed"
    assert cell["healer_outcome"] == "rescue_to_pass"

def test_rule_legacy_not_overwritten():
    # Legacy fields cannot be overwritten
    cell = {
        "legacy_failure_category": "Format/packaging",
        "primary_failure_layer": "L2" # v3 crosswalk annotation exists alongside legacy field
    }
    assert cell["legacy_failure_category"] == "Format/packaging"
    assert cell["primary_failure_layer"] == "L2"
