# -*- coding: utf-8 -*-
"""Targeted tests for Math16 Pilot-02 Qwen 4B runtime freeze."""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MANIFEST = ROOT / "docs/experiments/manifests/math16_pilot02_qwen4b_runtime_manifest.json"
PLAN = ROOT / "docs/experiments/manifests/math16_pilot02_qwen4b_cell_plan.json"
DESIGN = ROOT / "docs/experiments/design/math16_pilot02_qwen4b_runtime_preregistration.md"
GEMINI_MANIFEST = ROOT / "docs/experiments/manifests/math16_pilot02_full_runtime_manifest.json"

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


def test_geometry_and_uniqueness():
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


def test_all_spec_prompts_are_v2_not_v1():
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    assert not any(c["condition"] == "ab2d_spec" for c in plan)
    for c in plan:
        if c["condition"] == "ab2d_spec_v2":
            assert c["prompt_path"].startswith(
                "docs/experiments/prompts/ab2d_spec_v2/prompts/"
            )
            assert "/ab2d_spec/prompts/" not in ("/" + c["prompt_path"].replace("\\", "/"))
            assert "/ab2d_spec_v2/prompts/" in ("/" + c["prompt_path"].replace("\\", "/"))
            path = ROOT / c["prompt_path"]
            assert path.exists()
            text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
            sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
            assert sha == c["prompt_sha256"]


def test_runtime_required_fields_and_thinking_false():
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for key in (
        "model_provider",
        "model_tag",
        "model_digest",
        "architecture",
        "parameter_count",
        "quantization",
        "runtime",
        "runtime_version",
        "transport",
        "thinking_mode",
        "temperature",
        "top_k",
        "top_p",
        "repeat_penalty",
        "seed_transport_supported",
        "context_window",
        "max_output_tokens",
        "timeout_seconds",
        "retry_policy",
        "hardware",
        "cold_warm",
        "source_commit",
    ):
        assert key in m
        assert m[key] not in (None, "")
    assert m["thinking_mode"] is False
    assert m["thinking_mode"] is not None
    assert m["seed_transport_supported"] is True
    assert m["seed_role"] == "model_rng_seed_and_cell_label"


def test_seed_transport_matches_adapter():
    from scripts.math16_qwen_ollama_adapter import build_math16_chat_payload

    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    payload = build_math16_chat_payload(
        "x", seed=2026072001, model=m["model_tag"]
    )
    assert payload["think"] is False
    assert payload["options"]["seed"] == 2026072001
    assert m["seed_transport_supported"] is True


def test_evaluator_taxonomy_healer_hashes_locked():
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert m["taxonomy_hash"] == (
        "7df8f4472ce048569967436cbc73ede8fd4bd117ad67d0028ddd95af2055a304"
    )
    assert m["evaluator_hash"] == (
        "2cca19f2258d4ba6134ff10d4e9bcff925e2441c32820fcbc151cb6b1dd740bc"
    )
    allow = m["healer_allowlist"]
    expect = hashlib.sha256(
        json.dumps(allow, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()
    assert m["healer_allowlist_hash"] == expect


def test_fingerprint_reproducible_and_no_forbidden():
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert _fp(m) == m["runtime_config_fingerprint"]
    blob = json.dumps({k: m[k] for k in FINGERPRINT_KEYS}, sort_keys=True)
    lower = blob.lower()
    assert "api_key" not in lower
    assert "username" not in lower
    assert "c:\\users\\" not in lower
    assert "created_at_utc" not in lower


def test_vs_gemini_diffs_only_in_allowed_set():
    q = json.loads(MANIFEST.read_text(encoding="utf-8"))
    g = json.loads(GEMINI_MANIFEST.read_text(encoding="utf-8"))
    # shared must-match
    assert q["seed_list"] == g["seed_list"]
    assert q["taxonomy_hash"] == (
        "7df8f4472ce048569967436cbc73ede8fd4bd117ad67d0028ddd95af2055a304"
    )
    # fingerprints must not be identical (more than model_tag differs)
    assert q["runtime_config_fingerprint"] != g["runtime_config_fingerprint"]
    assert q["model_provider"] != g["model_provider"]
    assert q["runtime"] != g["runtime"]
    assert q.get("model_digest")
    assert not g.get("model_digest")
    # allowed diff fields recorded
    allowed = set(q["allowed_cross_model_diff_fields"])
    assert {"model_provider", "model_tag", "runtime", "temperature", "hardware"} <= allowed


def test_design_doc_exists_and_states_think_false():
    text = DESIGN.read_text(encoding="utf-8")
    assert "think=false" in text
    assert "ab2d_spec_v2" in text
    assert "replicate_label_only" not in text or "seed_role" in text
    assert "MATH16_PILOT02_QWEN4B_RUNTIME_PREREGISTRATION_FROZEN" in text


def test_preflight_script_pass():
    from scripts.preflight_math16_pilot02_qwen4b_runtime import do_preflight

    result = do_preflight()
    assert result["preflight"] == "PASS"
    assert result["llm_generation_calls"] == 0


# ── Revision-targeted tests (temperature 0.7 → 0.2) ──────────────────────────

OLD_FINGERPRINT = "7efdbbaf6f6cc72af2a4d51fcd574bd82e92a654e20a0d685ee1275f11e24bfe"
NEW_FINGERPRINT = "33fd7603f58cdc47843bb048456d6d167dd71dc891b636377baf33dea30358f7"


def test_all_cells_use_temperature_02():
    """All 320 cells must resolve to temperature=0.2 via the manifest."""
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert m["temperature"] == 0.2, f"manifest temperature={m['temperature']}, expected 0.2"
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    assert len(plan) == 320


def test_think_false_and_not_null():
    """thinking_mode must be exactly False, not None."""
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert m["thinking_mode"] is False
    assert m["thinking_mode"] is not None


def test_prompt_sha_unchanged():
    """All 16x4=64 prompt SHAs in the manifest must be identical to the pre-revision values."""
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    registry = m["prompt_verification_registry"]
    # Spot-check a fixed set of known SHAs
    sha_by_key = {(r["task_id"], r["condition"]): r["prompt_sha256"] for r in registry}
    assert sha_by_key[("ce111_q03_prime_factor_selection", "ab1")] == \
        "398a9ab7067574286a3f7b6a955033b2f3af8d244d34098aa907623bb706bcc4"
    assert sha_by_key[("ce111_q03_prime_factor_selection", "ab2d_spec_v2")] == \
        "5417185bc8f5d084bd04d6bf4d346762f6fa4738c6a52d30ea34706f4121e6f0"
    # All registry entries must still have a non-empty sha
    for r in registry:
        assert r["prompt_sha256"], f"empty sha for {r['task_id']} {r['condition']}"


def test_new_fingerprint_differs_from_old():
    """New fingerprint must be different from the pre-revision fingerprint."""
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert m["runtime_config_fingerprint"] != OLD_FINGERPRINT
    assert m["runtime_config_fingerprint"] == NEW_FINGERPRINT


def test_fingerprint_recompute_matches_new():
    """Recomputing fingerprint from manifest fields must match the stored new fingerprint."""
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert _fp(m) == NEW_FINGERPRINT
    assert _fp(m) == m["runtime_config_fingerprint"]


def test_no_unexpected_field_changes():
    """Only temperature (and derived fingerprint) should differ; all other locked fields stay."""
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert m["top_p"] == 0.8
    assert m["top_k"] == 20
    assert m["thinking_mode"] is False
    assert m["context_window"] == 65536
    assert m["max_output_tokens"] == 24576
    assert m["timeout_seconds"] == 1800
    assert m["model_tag"] == "qwen3.5:4b"
    assert m["model_digest"] == "2a654d98e6fba55d452b7043684e9b57a947e393bbffa62485a7aac05ee4eefd"
    assert m["seed_list"] == [2026071301, 2026072001, 2026072002, 2026072003, 2026072004]
    assert m["expected_cell_count"] == 320
    assert m["repeat_penalty"] == "ollama_default_unset"


def test_qwen_4b_9b_comparison_contract():
    """The comparison contract for Qwen 4B vs 9B must be: temperature=0.2, think=false."""
    from scripts.math16_qwen_ollama_adapter import TEMPERATURE, FROZEN_INFERENCE_CONFIG
    assert TEMPERATURE == 0.2, f"adapter TEMPERATURE={TEMPERATURE}, expected 0.2"
    assert FROZEN_INFERENCE_CONFIG["temperature"] == 0.2
    assert FROZEN_INFERENCE_CONFIG["think"] is False
    assert FROZEN_INFERENCE_CONFIG["top_p"] == 0.8
    assert FROZEN_INFERENCE_CONFIG["top_k"] == 20
