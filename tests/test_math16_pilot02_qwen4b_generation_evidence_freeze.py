# -*- coding: utf-8 -*-
"""Evidence freeze / closeout tests for Qwen4B Pilot-02 generation corpus."""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs/experiments/results/math16_pilot02_qwen4b"
PLAN = ROOT / "docs/experiments/manifests/math16_pilot02_qwen4b_cell_plan.json"
FREEZE = ROOT / "docs/experiments/manifests/math16_pilot02_qwen4b_generation_evidence_freeze_v1.json"
RUNNER = ROOT / "scripts/run_math16_pilot02_qwen4b_generation.py"
EXPECTED_FP = "33fd7603f58cdc47843bb048456d6d167dd71dc891b636377baf33dea30358f7"
FROZEN_COMMIT = "7e30300be6db34190124f026314a011de6bfa124"


def sha_bytes(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha_lf(path: Path) -> str:
    return hashlib.sha256(
        path.read_text(encoding="utf-8").replace("\r\n", "\n").encode("utf-8")
    ).hexdigest()


def sha_json(obj) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()


def test_runner_is_generation_only():
    text = RUNNER.read_text(encoding="utf-8")
    assert "EXPECTED_FINGERPRINT" in text
    assert EXPECTED_FP in text
    assert "evaluate_math16" not in text
    assert "call_gemini" not in text
    assert "qwen3.5:9b" not in text
    assert '"scoring": False' in text
    assert "INCOMPATIBLE_EXISTING_CELL" in text
    assert "ab2d_spec_v2" in text


def test_corpus_file_counts_and_integrity():
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    assert len(plan) == 320
    assert len({c["cell_id"] for c in plan}) == 320
    for cell in plan:
        d = ROOT / "docs/experiments/results" / cell["output_relative_path"]
        assert (d / "artifact.json").exists()
        assert (d / "prompt.txt").exists()
        assert (d / "raw_response.txt").exists()
        art = json.loads((d / "artifact.json").read_text(encoding="utf-8"))
        assert art["runtime_config_fingerprint"] == EXPECTED_FP
        assert art["runtime_parameters"]["temperature"] == 0.2
        assert art["prompt_sha256"] == cell["prompt_sha256"]
        assert sha_lf(d / "prompt.txt") == cell["prompt_sha256"]
        raw = (d / "raw_response.txt").read_text(encoding="utf-8")
        assert raw.strip()
        assert art.get("scoring") is False
        assert art.get("healer") is False
        assert art.get("ab3") is False


def test_geometry_counts():
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    assert Counter(c["condition"] for c in plan) == {
        "ab1": 80,
        "ab2g": 80,
        "ab2d": 80,
        "ab2d_spec_v2": 80,
    }
    assert Counter(c["family"] for c in plan) == {
        "integer": 80,
        "polynomial": 80,
        "radical": 80,
        "fraction": 80,
    }


def test_journal_summary_audit_align():
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    journal = [
        json.loads(l)
        for l in (OUT / "cell_journal.jsonl").read_text(encoding="utf-8").splitlines()
        if l.strip()
    ]
    assert len(journal) == 320
    assert [r["cell_id"] for r in journal] == [c["cell_id"] for c in plan]
    summary = json.loads((OUT / "generation_summary.json").read_text(encoding="utf-8"))
    audit = json.loads(
        (OUT / "generation_completeness_audit.json").read_text(encoding="utf-8")
    )
    assert summary["stats"]["success"] == 320
    assert audit["passed"] is True
    assert audit["fingerprint"] == EXPECTED_FP


def test_evidence_freeze_manifest():
    freeze = json.loads(FREEZE.read_text(encoding="utf-8"))
    assert freeze["frozen_preregistration_commit"] == FROZEN_COMMIT
    assert freeze["runtime_config_fingerprint"] == EXPECTED_FP
    assert freeze["cell_count"] == 320
    assert freeze["scoring"] is False
    assert freeze["ab3"] is False
    assert freeze["healer"] is False
    assert freeze["other_model_calls"] is False
    assert freeze["llm_calls_during_freeze"] == 0
    assert freeze["integrity_checks"] == {
        "duplicate_cell_ids": 0,
        "missing": 0,
        "empty_success_raw": 0,
        "prompt_drift": 0,
        "fingerprint_mismatch": 0,
        "temperature_mismatch": 0,
    }
    # recompute corpus closure
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    records = []
    for cell in plan:
        d = ROOT / "docs/experiments/results" / cell["output_relative_path"]
        records.append(
            {
                "cell_id": cell["cell_id"],
                "artifact_sha256": sha_bytes(d / "artifact.json"),
                "prompt_sha256_file": sha_lf(d / "prompt.txt"),
                "raw_response_sha256": sha_bytes(d / "raw_response.txt"),
                "plan_prompt_sha256": cell["prompt_sha256"],
                "generation_status": json.loads(
                    (d / "artifact.json").read_text(encoding="utf-8")
                )["generation_status"],
            }
        )
    records = sorted(records, key=lambda r: r["cell_id"])
    assert sha_json(records) == freeze["corpus_sha_closure"]
    # key file SHAs still match
    for key, rel in {
        "runner": "scripts/run_math16_pilot02_qwen4b_generation.py",
        "cell_journal": "docs/experiments/results/math16_pilot02_qwen4b/cell_journal.jsonl",
        "generation_summary": "docs/experiments/results/math16_pilot02_qwen4b/generation_summary.json",
        "generation_completeness_audit": (
            "docs/experiments/results/math16_pilot02_qwen4b/generation_completeness_audit.json"
        ),
    }.items():
        assert freeze["key_file_sha256"][key] == sha_bytes(ROOT / rel)
