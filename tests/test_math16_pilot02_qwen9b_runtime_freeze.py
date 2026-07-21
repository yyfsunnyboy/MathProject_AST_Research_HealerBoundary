# -*- coding: utf-8 -*-
"""Targeted tests for Math16 Pilot-02 Qwen 9B runtime freeze."""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MANIFEST = ROOT / "docs/experiments/manifests/math16_pilot02_qwen9b_runtime_manifest.json"
PLAN = ROOT / "docs/experiments/manifests/math16_pilot02_qwen9b_cell_plan.json"
DESIGN = ROOT / "docs/experiments/design/math16_pilot02_qwen9b_runtime_preregistration.md"
QWEN4B_MANIFEST = ROOT / "docs/experiments/manifests/math16_pilot02_qwen4b_runtime_manifest.json"
QWEN4B_PLAN = ROOT / "docs/experiments/manifests/math16_pilot02_qwen4b_cell_plan.json"
HEALER_RUNNER = ROOT / "agent_tools/finals_rebuild/ce115_research_healer_runner.py"
HEALER_PROTOCOL = ROOT / "agent_tools/finals_rebuild/ce115_research_healer_protocol.py"

EXPECTED_RUNNER = "38453d1294382f061efe149484f5a3059a47d085d2aeef358874a954e37adebf"
EXPECTED_PROTO = "bdb4121ee266f91bfa116019a334cf4a528da0d71629b96540a5f763826aff39"

FINGERPRINT_KEYS = [
    "experiment_id",
    "model_provider",
    "model_tag",
    "model_digest",
    "model_version",
    "architecture",
    "parameter_count",
    "quantization",
    "runtime",
    "runtime_version",
    "thinking_mode",
    "temperature",
    "top_p",
    "top_k",
    "repeat_penalty",
    "seed_transport_supported",
    "context_window",
    "max_output_tokens",
    "timeout_seconds",
    "retry_policy",
    "seed_list",
    "prompt_manifest_hash",
    "evaluator_hash",
    "taxonomy_hash",
    "healer_allowlist_hash",
    "source_commit",
]


def _fp(manifest: dict) -> str:
    sub = {k: manifest[k] for k in FINGERPRINT_KEYS}
    return hashlib.sha256(
        json.dumps(sub, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_geometry_and_sampling_lock():
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    assert len(plan) == 320
    assert len({c["cell_id"] for c in plan}) == 320
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
    assert len(Counter(c["task_id"] for c in plan)) == 16
    assert all(v == 20 for v in Counter(c["task_id"] for c in plan).values())
    assert all(v == 64 for v in Counter(c["seed"] for c in plan).values())
    assert all(c["model_tag"] == "qwen3.5:9b" for c in plan)
    assert all(c["temperature"] == 0.2 for c in plan)
    assert all(c["top_p"] == 0.8 for c in plan)
    assert all(c["top_k"] == 20 for c in plan)
    assert all(c["think"] is False for c in plan)


def test_runtime_manifest_locks():
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert m["model_tag"] == "qwen3.5:9b"
    assert m["architecture"] == "qwen35"
    assert m["parameter_count"] == 9653104368
    assert m["parameter_count_label"] == "9.7B"
    assert m["quantization"] == "Q4_K_M"
    assert m["runtime_version"] == "0.32.1"
    assert m["thinking_mode"] is False
    assert m["temperature"] == 0.2
    assert m["top_p"] == 0.8
    assert m["top_k"] == 20
    assert m["context_window"] == 65536
    assert m["max_output_tokens"] == 24576
    assert m["timeout_seconds"] == 1800
    assert m["repeat_penalty"] == "ollama_default_unset"
    assert m["llm_generation_calls"] == 0
    assert m["formal_generation_started"] is False
    assert m["healer_execution_this_round"] is False
    assert "temperature=0.2" in m["sampling_rationale"]
    assert "Qwen 4B" in m["sampling_rationale"]


def test_fingerprint_and_healer_pins():
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert _fp(m) == m["runtime_config_fingerprint"]
    assert sha(HEALER_RUNNER) == EXPECTED_RUNNER
    assert sha(HEALER_PROTOCOL) == EXPECTED_PROTO
    assert m["corrected_chain_healer_runner_sha256"] == EXPECTED_RUNNER
    assert m["corrected_chain_healer_protocol_sha256"] == EXPECTED_PROTO


def test_prompt_sha_and_cell_alignment_with_qwen4b():
    m9 = json.loads(MANIFEST.read_text(encoding="utf-8"))
    m4 = json.loads(QWEN4B_MANIFEST.read_text(encoding="utf-8"))
    p9 = json.loads(PLAN.read_text(encoding="utf-8"))
    p4 = json.loads(QWEN4B_PLAN.read_text(encoding="utf-8"))

    assert m9["prompt_manifest_hash"] == m4["prompt_manifest_hash"]
    reg9 = {
        (r["task_id"], r["condition"]): r["prompt_sha256"]
        for r in m9["prompt_verification_registry"]
    }
    reg4 = {
        (r["task_id"], r["condition"]): r["prompt_sha256"]
        for r in m4["prompt_verification_registry"]
    }
    assert reg9 == reg4

    by4 = {(c["task_id"], c["condition"], c["seed"]): c for c in p4}
    for c in p9:
        q4 = by4[(c["task_id"], c["condition"], c["seed"])]
        assert c["prompt_sha256"] == q4["prompt_sha256"]
        assert c["family"] == q4["family"]
        assert (c.get("prompt_path") or None) == (q4.get("prompt_path") or None)
        assert c["model_tag"] != q4["model_tag"]
        assert c["cell_id"].startswith("qwen3_5_9b__")
        assert q4["cell_id"].startswith("qwen3_5_4b__")


def test_design_doc_and_preflight():
    text = DESIGN.read_text(encoding="utf-8")
    assert "QWEN9B_RUNTIME_PREREGISTRATION_FROZEN" in text
    assert "think=false" in text
    assert "temperature=0.2" in text
    assert EXPECTED_RUNNER in text
    assert EXPECTED_PROTO in text

    from scripts.preflight_math16_pilot02_qwen9b_runtime import do_preflight

    result = do_preflight()
    assert result["preflight"] == "PASS"
    assert result["llm_generation_calls"] == 0
    assert result["api_chat_calls"] == 0


def test_adapter_shared_sampling_contract():
    from scripts.math16_qwen_ollama_adapter import FROZEN_INFERENCE_CONFIG, build_math16_chat_payload

    assert FROZEN_INFERENCE_CONFIG["temperature"] == 0.2
    assert FROZEN_INFERENCE_CONFIG["top_p"] == 0.8
    assert FROZEN_INFERENCE_CONFIG["top_k"] == 20
    assert FROZEN_INFERENCE_CONFIG["think"] is False
    payload = build_math16_chat_payload("x", seed=2026072001, model="qwen3.5:9b")
    assert payload["model"] == "qwen3.5:9b"
    assert payload["think"] is False
    assert payload["options"]["seed"] == 2026072001
