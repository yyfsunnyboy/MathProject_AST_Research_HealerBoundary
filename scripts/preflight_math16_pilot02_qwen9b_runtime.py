# -*- coding: utf-8 -*-
"""Zero-model preflight for Math16 Pilot-02 Qwen 9B runtime freeze.

Must not call Ollama /api/chat.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

MANIFEST_PATH = ROOT / "docs/experiments/manifests/math16_pilot02_qwen9b_runtime_manifest.json"
PLAN_PATH = ROOT / "docs/experiments/manifests/math16_pilot02_qwen9b_cell_plan.json"
QWEN4B_PLAN = ROOT / "docs/experiments/manifests/math16_pilot02_qwen4b_cell_plan.json"
QWEN4B_MANIFEST = ROOT / "docs/experiments/manifests/math16_pilot02_qwen4b_runtime_manifest.json"
HEALER_RUNNER = ROOT / "agent_tools/finals_rebuild/ce115_research_healer_runner.py"
HEALER_PROTOCOL = ROOT / "agent_tools/finals_rebuild/ce115_research_healer_protocol.py"

EXPECTED_HEALER_RUNNER_HASH = (
    "38453d1294382f061efe149484f5a3059a47d085d2aeef358874a954e37adebf"
)
EXPECTED_HEALER_PROTOCOL_HASH = (
    "bdb4121ee266f91bfa116019a334cf4a528da0d71629b96540a5f763826aff39"
)

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


def sha_json(obj: Any) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()


def sha_bytes(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compute_fingerprint(manifest: dict[str, Any]) -> str:
    sub = {k: manifest[k] for k in FINGERPRINT_KEYS}
    blob = json.dumps(sub, sort_keys=True, ensure_ascii=False)
    lower = blob.lower()
    for bad in ("api_key", "username", "c:\\users\\", "/users/", "created_at_utc"):
        if bad in lower:
            raise RuntimeError(f"forbidden content in fingerprint payload: {bad}")
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def do_preflight() -> dict[str, Any]:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    q4_plan = json.loads(QWEN4B_PLAN.read_text(encoding="utf-8"))
    q4_man = json.loads(QWEN4B_MANIFEST.read_text(encoding="utf-8"))

    if manifest["model_tag"] != "qwen3.5:9b":
        raise RuntimeError("model_tag must be qwen3.5:9b")
    if manifest["thinking_mode"] is not False:
        raise RuntimeError("thinking_mode must be false")
    if manifest["temperature"] != 0.2:
        raise RuntimeError("temperature must be 0.2")
    if manifest["top_p"] != 0.8 or manifest["top_k"] != 20:
        raise RuntimeError("top_p/top_k must be 0.8/20")
    if manifest["context_window"] != 65536:
        raise RuntimeError("num_ctx/context_window must be 65536")
    if manifest["max_output_tokens"] != 24576:
        raise RuntimeError("num_predict must be 24576")
    if manifest["timeout_seconds"] != 1800:
        raise RuntimeError("timeout must be 1800")
    if manifest.get("formal_generation_started") is not False:
        raise RuntimeError("formal generation must remain false")
    if manifest.get("llm_generation_calls") != 0:
        raise RuntimeError("llm_generation_calls must be 0")

    # Adapter payload checks without calling /api/chat.
    from scripts.math16_qwen_ollama_adapter import build_math16_chat_payload

    payload = build_math16_chat_payload(
        "preflight", seed=int(manifest["seed_list"][0]), model=manifest["model_tag"]
    )
    if payload.get("think") is not False:
        raise RuntimeError("adapter think must be false")
    if "seed" not in (payload.get("options") or {}):
        raise RuntimeError("options.seed missing")
    if payload["options"]["temperature"] != 0.2:
        raise RuntimeError("payload temperature != 0.2")
    if payload["model"] != "qwen3.5:9b":
        raise RuntimeError("payload model != qwen3.5:9b")

    fp = compute_fingerprint(manifest)
    if fp != manifest["runtime_config_fingerprint"]:
        raise RuntimeError(
            f"fingerprint mismatch: stored={manifest['runtime_config_fingerprint']} got={fp}"
        )

    if len(plan) != 320:
        raise RuntimeError(f"expected 320 cells, got {len(plan)}")
    if len({c["cell_id"] for c in plan}) != 320:
        raise RuntimeError("duplicate cell_id")

    cond_c = Counter(c["condition"] for c in plan)
    fam_c = Counter(c["family"] for c in plan)
    task_c = Counter(c["task_id"] for c in plan)
    seed_c = Counter(c["seed"] for c in plan)
    if cond_c != {c: 80 for c in ("ab1", "ab2g", "ab2d", "ab2d_spec_v2")}:
        raise RuntimeError(f"condition counts bad: {cond_c}")
    if fam_c != {"integer": 80, "polynomial": 80, "radical": 80, "fraction": 80}:
        raise RuntimeError(f"family counts bad: {fam_c}")
    if any(v != 20 for v in task_c.values()) or len(task_c) != 16:
        raise RuntimeError(f"task counts bad: {task_c}")
    if seed_c != {s: 64 for s in manifest["seed_list"]}:
        raise RuntimeError(f"seed counts bad: {seed_c}")

    for cell in plan:
        if cell["model_tag"] != "qwen3.5:9b":
            raise RuntimeError(f"bad model_tag on {cell['cell_id']}")
        if cell.get("temperature") != 0.2:
            raise RuntimeError(f"bad temperature on {cell['cell_id']}")
        if cell.get("top_p") != 0.8 or cell.get("top_k") != 20:
            raise RuntimeError(f"bad top_p/k on {cell['cell_id']}")
        if cell.get("think") is not False:
            raise RuntimeError(f"bad think on {cell['cell_id']}")

    # Prompt SHA + cell alignment vs Qwen4B.
    q4_reg = {
        (r["task_id"], r["condition"]): r["prompt_sha256"]
        for r in q4_man["prompt_verification_registry"]
    }
    q9_reg = {
        (r["task_id"], r["condition"]): r["prompt_sha256"]
        for r in manifest["prompt_verification_registry"]
    }
    if q4_reg != q9_reg:
        raise RuntimeError("prompt SHA registry drift vs Qwen4B")
    if manifest["prompt_manifest_hash"] != q4_man["prompt_manifest_hash"]:
        raise RuntimeError("prompt_manifest_hash drift vs Qwen4B")

    q4_by = {(c["task_id"], c["condition"], c["seed"]): c for c in q4_plan}
    for c in plan:
        key = (c["task_id"], c["condition"], c["seed"])
        q4 = q4_by[key]
        if c["prompt_sha256"] != q4["prompt_sha256"]:
            raise RuntimeError(f"prompt SHA cell drift: {key}")
        if c["family"] != q4["family"]:
            raise RuntimeError(f"family drift: {key}")
        if (c.get("prompt_path") or None) != (q4.get("prompt_path") or None):
            raise RuntimeError(f"prompt_path drift: {key}")

    # Corrected-chain Healer pins.
    if sha_bytes(HEALER_RUNNER) != EXPECTED_HEALER_RUNNER_HASH:
        raise RuntimeError("healer runner pin drift")
    if sha_bytes(HEALER_PROTOCOL) != EXPECTED_HEALER_PROTOCOL_HASH:
        raise RuntimeError("healer protocol pin drift")
    if manifest["corrected_chain_healer_runner_sha256"] != EXPECTED_HEALER_RUNNER_HASH:
        raise RuntimeError("manifest runner pin mismatch")
    if manifest["corrected_chain_healer_protocol_sha256"] != EXPECTED_HEALER_PROTOCOL_HASH:
        raise RuntimeError("manifest protocol pin mismatch")

    if manifest["taxonomy_hash"] != (
        "7df8f4472ce048569967436cbc73ede8fd4bd117ad67d0028ddd95af2055a304"
    ):
        raise RuntimeError("taxonomy hash drift")
    if manifest["evaluator_hash"] != (
        "2cca19f2258d4ba6134ff10d4e9bcff925e2441c32820fcbc151cb6b1dd740bc"
    ):
        raise RuntimeError("evaluator hash drift")

    result = {
        "preflight": "PASS",
        "cells": 320,
        "fingerprint": fp,
        "model_tag": manifest["model_tag"],
        "model_digest": manifest["model_digest"],
        "thinking_mode": False,
        "temperature": 0.2,
        "aligned_with_qwen4b_prompt_sha": True,
        "llm_generation_calls": 0,
        "model_calls": 0,
        "api_chat_calls": 0,
    }
    print(json.dumps(result, indent=2))
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preflight-only", action="store_true", required=True)
    parser.parse_args()
    do_preflight()
    print("QWEN9B_ZERO_MODEL_PREFLIGHT_PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
