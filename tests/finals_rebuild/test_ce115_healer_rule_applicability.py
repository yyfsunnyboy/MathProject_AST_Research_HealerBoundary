"""Milestone 5A.1 — frozen-rule applicability unit tests (no model / no replay)."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from scripts.ce115_healer_rule_applicability import (
    RULE_ID,
    character_diff,
    classify_applicability,
    main as applicability_main,
)

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "docs/experiments/results/ce115_calc_local_confirmatory"
SMOKE = (
    RESULTS
    / "qwen3_5_4b__ce115_calc_exact_rational_expression_l1__ab2g__seed_2026071301_git_908033d34863.jsonl"
)
SMOKE_SHA = "137f05c3ddf21af06c71e1cea0431b106bcdaf82b844f2a2c328b9d0afb44e4d"
OUT_JSON = ROOT / "docs/experiments/analysis/ce115_healer_rule_applicability.json"


def test_supported_fullwidth_changes_and_parses():
    code = "def generate(level=1， **kwargs)：\n    return {}\n"
    out = classify_applicability(code=code, raw=code)
    assert out["applicability_verdict"] == "RULE_APPLICABLE"
    assert out["normalization_changed_content"] is True
    assert out["non_rule_changes"] == 0
    assert out["parse_after"]["ok"] is True


def test_normalization_noop_not_applicable():
    code = "def generate(level=1, **kwargs):\n    return {'a': 1}\n"
    out = classify_applicability(code=code, raw=code)
    assert out["applicability_verdict"] == "RULE_NOT_APPLICABLE"
    assert out["normalization_changed_content"] is False


def test_markdown_fence_not_applicable():
    code = "```python\ndef generate(level=1， **kwargs)：\n    return {}\n```\n"
    out = classify_applicability(code=code, raw=code)
    assert out["applicability_verdict"] == "RULE_NOT_APPLICABLE"
    assert "markdown_fence" in out["gap_tags"] or "markdown_fence" in out["exclusion_signals"]


def test_unmatched_bracket_without_fullwidth_not_applicable():
    code = "def generate(level=1, **kwargs):\n    return {\n"
    out = classify_applicability(code=code, raw=code)
    assert out["applicability_verdict"] == "RULE_NOT_APPLICABLE"


def test_truncated_code_not_applicable():
    code = "def generate(level=1, **kwargs):\n    x = 1 +\n"
    out = classify_applicability(code=code, raw=code)
    assert out["applicability_verdict"] == "RULE_NOT_APPLICABLE"


def test_still_parse_fail_after_normalization_not_applicable():
    # Fullwidth colon fixed would still leave unfinished body / bad structure.
    code = "def generate(level=1， **kwargs)：\n    return {\n"
    out = classify_applicability(code=code, raw=code)
    assert out["applicability_verdict"] == "RULE_NOT_APPLICABLE"
    assert out.get("normalization_changed_content") in {True, False}


def test_non_rule_character_change_blocked_via_diff_helper():
    # Simulate illicit length-preserving non-rule edit detection.
    before = "abc"
    after = "aXc"
    diff = character_diff(before, after)
    assert diff["non_rule_changes"] == 1


def test_observed_artifact_hashes_unchanged_and_deterministic():
    assert hashlib.sha256(SMOKE.read_bytes()).hexdigest() == SMOKE_SHA
    before = hashlib.sha256(SMOKE.read_bytes()).hexdigest()
    assert applicability_main() == 0
    assert hashlib.sha256(SMOKE.read_bytes()).hexdigest() == before
    a = json.loads(OUT_JSON.read_text(encoding="utf-8"))
    assert applicability_main() == 0
    b = json.loads(OUT_JSON.read_text(encoding="utf-8"))
    assert a["verdict_counts"] == b["verdict_counts"]
    assert a["windows"] == b["windows"]
    assert a["cases"] == b["cases"]
    assert a["rule_id"] == RULE_ID
    assert a["taxonomy_candidate_count"] == 18
