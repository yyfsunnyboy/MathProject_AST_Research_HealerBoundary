"""Math16 Phase 1 Qwen multiseed completeness / aggregation / immutability tests."""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "docs/experiments/results"
REPORT_DATA = ROOT / "docs/experiments/reports/math16_qwen_five_seed_interim_report_data.json"
PREDICTIONS = ROOT / "docs/experiments/predictions/math16_qwen_multiseed_predictions.json"
AB3 = RESULTS / "math16_qwen_multiseed_ab3_phase1" / "ab3_report_data.json"

MODELS = ("qwen35_4b", "qwen35_9b")
NEW_SEEDS = (2026072001, 2026072002, 2026072003, 2026072004)
ALL_SEEDS = (2026071301, *NEW_SEEDS)
EXPECTED_DIGEST = {
    "qwen35_4b": "2a654d98e6fba55d452b7043684e9b57a947e393bbffa62485a7aac05ee4eefd",
    "qwen35_9b": "6488c96fa5faab64bb65cbd30d4289e20e6130ef535a93ef9a49f42eda893ea7",
}
PRED_SHA = "dd07fe894fd8289d9615f8871327354ef08c2f92c839a8e6ebc88faca6139e13"


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _seed_cells(model: str, seed: int) -> list[Path]:
    if seed == 2026071301:
        root = RESULTS / f"{model}_math16_ab123_run_002" / "cells"
    else:
        root = RESULTS / f"{model}_math16_ab123_run_003_multiseed" / f"seed_{seed}" / "cells"
    return sorted(root.glob("*/artifact.json"))


def test_generation_completeness_384():
    for model in MODELS:
        for seed in NEW_SEEDS:
            arts = _seed_cells(model, seed)
            assert len(arts) == 48
            ids = []
            for p in arts:
                a = _load(p)
                ids.append(a["cell_id"])
                assert a["seed"] == seed
                assert a.get("persisted_complete") is True
                assert (p.parent / "raw_response.txt").exists()
                assert a.get("hashes", {}).get("raw") is not None
                assert a.get("hashes", {}).get("prompt") is not None
                assert a.get("model_digest") == EXPECTED_DIGEST[model]
            assert len(set(ids)) == 48


def test_five_seed_totals_480():
    total = 0
    for model in MODELS:
        for seed in ALL_SEEDS:
            arts = _seed_cells(model, seed)
            assert len(arts) == 48
            total += len(arts)
    assert total == 480


def test_run_002_byte_immutability():
    snap = _load(RESULTS / "_phase1_immutability" / "run_002_pre_generation_fingerprint.json")
    for run, expected in snap.items():
        root = RESULTS / run
        arts = sorted((root / "cells").glob("*/artifact.json"))
        raws = sorted((root / "cells").glob("*/raw_response.txt"))
        ha = hashlib.sha256(b"".join(p.read_bytes() for p in arts)).hexdigest()
        hr = hashlib.sha256(b"".join(p.read_bytes() for p in raws)).hexdigest()
        assert ha == expected["artifact_concat_sha256"]
        assert hr == expected["raw_concat_sha256"]


def test_h0_new_immutable_vs_pre_ab3():
    pre = _load(RESULTS / "_phase1_immutability" / "h0_new_384_pre_ab3_fingerprint.json")
    arts = []
    for model in MODELS:
        for seed in NEW_SEEDS:
            arts.extend(_seed_cells(model, seed))
    h = hashlib.sha256(b"".join(p.read_bytes() for p in arts)).hexdigest()
    assert len(arts) == 384
    assert h == pre["concat_sha256"]


def test_ab3_outcome_closure():
    ab = _load(AB3)
    summary = ab["summary"]
    assert summary["cells"] == 384
    assert sum(summary["by_outcome"].values()) == 384
    assert summary["regression"] == 0
    assert summary["identity_reuse"] == summary["by_outcome"].get("identity_reuse", 0)
    # H1 independent
    h1 = RESULTS / "math16_qwen_multiseed_ab3_phase1" / "h1_cells"
    assert len(list(h1.iterdir())) == 384
    # no repaired files inside H0 trees
    for model in MODELS:
        for seed in NEW_SEEDS:
            root = RESULTS / f"{model}_math16_ab123_run_003_multiseed" / f"seed_{seed}" / "cells"
            assert list(root.glob("*/repaired_candidate.py")) == []


def test_prediction_lock_unchanged():
    preds = _load(PREDICTIONS)
    body = {k: v for k, v in preds.items() if k not in ("canonical_sha256", "canonical_sha256_basis")}
    h = hashlib.sha256(
        json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    ).hexdigest()
    assert h == PRED_SHA
    assert preds["canonical_sha256"] == PRED_SHA


def test_interim_report_assertions():
    data = _load(REPORT_DATA)
    for k, v in data["assertions"].items():
        assert v is True, k
    assert data["title"] == "Qwen Phase 1 interim report"


def test_allowlist_still_frozen():
    from agent_tools.finals_rebuild.ce115_research_healer_runner import RULE_ALLOWLIST

    assert len(RULE_ALLOWLIST) == 6
    assert sum(1 for r in RULE_ALLOWLIST if r.startswith("L1_")) == 3
    assert sum(1 for r in RULE_ALLOWLIST if r.startswith("L2_")) == 3
