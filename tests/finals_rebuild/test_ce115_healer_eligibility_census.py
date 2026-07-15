"""Milestone 5A — Healer eligibility census tests (no model / no repair)."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from scripts.ce115_healer_eligibility_census import (
    ELIGIBLE_TAXONOMY_TO_REPAIR_FAMILY,
    OUTCOME_TAXONOMY,
    classify_cell,
    dataset_hash,
    main as census_main,
)

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "docs/experiments/results/ce115_calc_local_confirmatory"
SMOKE = (
    RESULTS
    / "qwen3_5_4b__ce115_calc_exact_rational_expression_l1__ab2g__seed_2026071301_git_908033d34863.jsonl"
)
SMOKE_SHA = "137f05c3ddf21af06c71e1cea0431b106bcdaf82b844f2a2c328b9d0afb44e4d"
OUT_JSON = ROOT / "docs/experiments/analysis/ce115_healer_eligibility_census.json"


def test_passed_not_eligible():
    row = {
        "cell_id": "x",
        "model_tag": "qwen3.5:4b",
        "prompt_condition": "ab1",
        "task_id": "t",
        "seed": 1,
        "outcome": "passed",
        "candidate_extracted": "def generate():\n pass\n",
        "raw_first_attempt_output": "def generate():\n pass\n",
    }
    out = classify_cell(row, artifact_hash="abc")
    assert out["healer_eligible"] is False
    assert out["census_status"] == "ALREADY_PASSED"


def test_answer_incorrect_excluded():
    row = {
        "cell_id": "y",
        "model_tag": "qwen3.5:4b",
        "prompt_condition": "ab1",
        "task_id": "t",
        "seed": 1,
        "outcome": "answer_incorrect",
        "candidate_extracted": "def generate():\n pass\n",
        "raw_first_attempt_output": "code",
    }
    out = classify_cell(row, artifact_hash="abc")
    assert out["healer_eligible"] is False
    assert out["failure_taxonomy"] == "oracle_mismatch"
    assert out["failure_gate"] == "G4"
    assert "g4_semantic" in (out["exclusion_reason"] or "")


def test_parse_minor_eligible_mapping():
    assert OUTCOME_TAXONOMY["parse_minor"][0] == "parse_failure"
    assert "parse_failure" in ELIGIBLE_TAXONOMY_TO_REPAIR_FAMILY
    row = {
        "cell_id": "z",
        "model_tag": "qwen3.5:9b",
        "prompt_condition": "ab2g",
        "task_id": "t",
        "seed": 1,
        "outcome": "parse_minor",
        "candidate_extracted": "x = 1",
        "raw_first_attempt_output": "```\nx=1",
    }
    out = classify_cell(row, artifact_hash="abc")
    assert out["healer_eligible"] is True
    assert out["applicable_deterministic_repair_family"] == "tier1_core_syntax_or_format"


def test_unknown_outcome_blocked():
    row = {
        "cell_id": "u",
        "model_tag": "qwen3.5:4b",
        "prompt_condition": "ab1",
        "task_id": "t",
        "seed": 1,
        "outcome": "made_up_outcome",
        "candidate_extracted": "x",
        "raw_first_attempt_output": "x",
    }
    out = classify_cell(row, artifact_hash="abc")
    assert out["healer_eligible"] is False
    assert out["census_status"] == "BLOCKED_UNCLASSIFIED"
    assert out["failure_taxonomy"] == "unknown"


def test_census_72_unique_and_artifacts_unmodified(tmp_path=None):
    assert SMOKE.is_file()
    assert hashlib.sha256(SMOKE.read_bytes()).hexdigest() == SMOKE_SHA
    before = dataset_hash(RESULTS)
    assert census_main() == 0
    after = dataset_hash(RESULTS)
    assert before == after
    report = json.loads(OUT_JSON.read_text(encoding="utf-8"))
    assert report["census_kind"] == "taxonomy-level eligibility candidate census"
    assert report["n_cells"] == 72
    assert report["unique_cell_ids"] == 72
    assert report["blocked_unclassified_count"] == 0
    assert report["blocked_unclassified_cell_ids"] == []
    assert report["window_metrics"]["taxonomy_candidate_prevalence"] == "18 / 72"
    assert report["window_metrics"]["taxonomy_candidate_width_among_failures"] == "18 / 63"
    assert "PENDING" in report["window_metrics"]["rule_applicable_window"]
    assert report["call_counts"] == {"model": 0, "healer": 0, "retry": 0, "external_api": 0}
    # answer_incorrect all excluded
    ai = [c for c in report["cells"] if c["observed_outcome"] == "answer_incorrect"]
    assert len(ai) == 16
    assert all(c["healer_eligible"] is False for c in ai)


def test_deterministic_census_rebuild():
    assert census_main() == 0
    a = json.loads(OUT_JSON.read_text(encoding="utf-8"))
    assert census_main() == 0
    b = json.loads(OUT_JSON.read_text(encoding="utf-8"))
    for key in (
        "observed_dataset_hash",
        "script_sha256",
        "stats",
        "cells",
        "eligible_taxonomy_to_repair_family",
        "n_cells",
    ):
        assert a[key] == b[key]
