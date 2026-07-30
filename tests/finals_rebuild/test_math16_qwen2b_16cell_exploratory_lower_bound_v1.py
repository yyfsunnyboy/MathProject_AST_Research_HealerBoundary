# -*- coding: utf-8 -*-
"""Focused checks for Qwen2B 16-cell exploratory lower-bound Healer replay."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NS = "qwen2b_16cell_exploratory_lower_bound_v1"


def _load(rel: str) -> dict:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def _load_jsonl(rel: str) -> list[dict]:
    path = ROOT / rel
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def test_namespace_and_cell_identity():
    c0 = _load(f"docs/experiments/manifests/math16_c0_baseline_closure_{NS}.json")
    lineage = _load(f"docs/experiments/manifests/math16_16cell_lineage_{NS}.json")
    assert c0["namespace"] == NS
    assert c0["authority_status"] == "EXPLORATORY_LOWER_BOUND_FAIL_GATED_V1"
    assert c0["validation"]["n_cells"] == 16
    assert c0["validation"]["pass_n"] == 0
    assert c0["validation"]["fail_n"] == 16
    ids = [c["cell_id"] for c in c0["cells"]]
    assert len(ids) == 16
    assert len(set(ids)) == 16
    assert lineage["n_cells"] == 16
    assert lineage["timeout_fill_cells"] == 3


def test_raw_source_aligned_to_smoke_manifest():
    plan = _load(
        "docs/experiments/manifests/math16_qwen35_2b_four_condition_smoke_20260725_v1.json"
    )
    c0 = _load(f"docs/experiments/manifests/math16_c0_baseline_closure_{NS}.json")
    plan_ids = {c["cell_id"] for c in plan["cells"]}
    c0_ids = {c["cell_id"] for c in c0["cells"]}
    assert plan_ids == c0_ids
    fills = [c for c in c0["cells"] if c["source_lineage"] != "SMOKE_PRIMARY"]
    assert len(fills) == 3
    for c in c0["cells"]:
        raw = ROOT / c["raw_response_path"]
        assert raw.exists() and raw.stat().st_size > 0


def test_cumulative_zero_rescue_zero_regression():
    summary = _load(
        f"docs/experiments/results/math16_cumulative_{NS}/summary.json"
    )
    assert summary["baseline_pass"] == 0
    assert summary["final_pass"] == 0
    assert summary["total_verified_rescue"] == 0
    assert summary["total_regression"] == 0
    assert summary["model_calls"] == 0
    assert len(summary["pass_curve"]) == 9  # C0 + 8 layers


def test_per_layer_journals_parse_and_second_replay():
    layers = [
        "tier_a",
        "tier_b",
        "tier_c1",
        "tier_c2",
        "tier_d3",
        "tier_d1",
        "tier_d5",
        "tier_d2",
    ]
    for tag in layers:
        rows = _load_jsonl(
            f"docs/experiments/results/math16_{tag}_reproducibility_{NS}/"
            "transition_journal.jsonl"
        )
        census = _load_jsonl(
            f"docs/experiments/results/math16_{tag}_reproducibility_{NS}/"
            "census_journal.jsonl"
        )
        summary = _load(
            f"docs/experiments/results/math16_{tag}_reproducibility_{NS}/summary.json"
        )
        second = _load(
            f"docs/experiments/results/math16_{tag}_reproducibility_{NS}/"
            "deterministic_second_replay.json"
        )
        assert len(rows) == 16
        assert len(census) == 16
        assert summary["gated_fail_count"] == 16 or summary["preserved_pass_count"] + summary[
            "gated_fail_count"
        ] == 16
        assert second["zero_diff"] is True
        assert summary["transitions"]["regression"] == 0
        assert summary["model_calls"] == 0


def test_protocol_freeze_and_not_primary():
    protocol = _load(f"docs/experiments/manifests/math16_protocol_{NS}.json")
    assert protocol["namespace"] == NS
    assert protocol["freeze_checks"]["tier_b_order_matches"] is True
    assert protocol["freeze_checks"]["d5_thresholds_unchanged"] is True
    assert "no_round_2" in protocol["declarations"]
    assert "not_mixed_into_three_model_primary" in protocol["declarations"]
