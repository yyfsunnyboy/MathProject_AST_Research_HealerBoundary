# -*- coding: utf-8 -*-
"""Arithmetic / citation consistency for Pilot-02 final interpretation numbers."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

V4_REPORT = (
    ROOT
    / "docs/experiments/results/math16_pilot02_full_evaluation_v4_r001/math16_pilot02_full_v4_report.md"
)
V3_REPORT = (
    ROOT
    / "docs/experiments/results/math16_pilot02_full_evaluation_v3_r001/math16_pilot02_full_v3_report.md"
)
V2_EVAL = ROOT / "docs/experiments/results/math16_pilot02_ab2d_spec_v2_evaluation_r001/summary.json"
Q02_PATCH = (
    ROOT
    / "docs/experiments/results/math16_pilot02_ab2d_spec_v2_q02_patch_evaluation_r001/summary.json"
)
Q02_PURITY = (
    ROOT
    / "docs/experiments/results/math16_pilot02_ab2d_spec_v2_q02_purity_evaluation_r001/summary.json"
)
INTERP = ROOT / "docs/experiments/reports/math16_pilot02_final_result_interpretation.md"
AUDIT_MANIFEST = ROOT / "docs/experiments/audits/math16_pilot02_oracle_schema_audit_v1_manifest.json"


def test_primary_condition_and_family_sums():
    # Fixed primary numbers from v4
    conditions = (72, 76, 78, 63)
    families = (80, 74, 70, 65)
    assert sum(conditions) == 289
    assert sum(families) == 289


def test_v3_to_v4_delta():
    assert 265 + 24 == 289


def test_posthoc_deltas():
    assert 63 + 17 == 80
    assert 15 + 2 == 17
    assert 289 - 63 + 80 == 306
    assert 289 + 17 == 306
    assert 80 - 78 == 2


def test_artifacts_match_fixed_numbers():
    v4 = V4_REPORT.read_text(encoding="utf-8")
    assert "289/320" in v4
    assert "72/80" in v4 and "76/80" in v4 and "78/80" in v4 and "63/80" in v4
    assert "80/80" in v4 and "74/80" in v4 and "70/80" in v4 and "65/80" in v4

    v3 = V3_REPORT.read_text(encoding="utf-8")
    assert "265/320" in v3
    assert "58/80" in v3  # pre-fix Ab2d+spec historical

    v2 = json.loads(V2_EVAL.read_text(encoding="utf-8"))
    assert v2["global_recompute"]["ab2d_spec_v1_pass_per_80"] == 63
    assert v2["task_compare"]["ce111_q05_exact_fraction_expression"]["delta"] == 5
    assert v2["task_compare"]["ce112_q12_independent_probability_fraction"]["delta"] == 5
    assert v2["task_compare"]["ce113_q01_negative_fraction_subtraction"]["delta"] == 5

    patch = json.loads(Q02_PATCH.read_text(encoding="utf-8"))
    assert patch["global_recompute"]["ab2d_spec_hybrid_after_q02_pass_per_80"] == 80
    assert patch["global_recompute"]["overall_after_q02_per_320"] == 306
    assert patch["global_recompute"]["delta_from_q02_patch"] == 2

    purity = json.loads(Q02_PURITY.read_text(encoding="utf-8"))
    assert purity["q02_ab2d_spec_v2_pass"] == "5/5"
    assert purity["global_recompute"]["ab2d_spec_hybrid_pass_per_80"] == 80
    assert purity["global_recompute"]["overall_hybrid_pass_per_320"] == 306
    assert all(r["matches_frozen_v2"] for r in purity["all5_prompt_sha_table"])


def test_interpretation_doc_contains_required_layers():
    text = INTERP.read_text(encoding="utf-8")
    assert "MATH16_PILOT02_FINAL_INTERPRETATION_DOCUMENTED" in text
    assert "72/80" in text and "76/80" in text and "78/80" in text and "63/80" in text
    assert "289/320" in text
    assert "58/80" in text  # historical layer
    assert "80/80" in text and "306/320" in text
    assert "post-hoc" in text.lower() or "Post-hoc" in text
    assert "不得" in text and "Healer" in text
    assert "f9a51940b166e8613557d1490cf1a331467ffd95af8ca96617aeded15c78fb87" in text

    audit = json.loads(AUDIT_MANIFEST.read_text(encoding="utf-8"))
    assert audit["document_sha256"] == (
        "53906c5c3c8abb9412352a49c0e79f3ecda7b1f20183d9ec1084da1fe816fa73"
    )
    assert audit["summary"]["schema_false_negatives"] == 24
