# -*- coding: utf-8 -*-
"""Zero-model preflight for Math16 Pilot-02 Qwen 4B runtime freeze."""
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

MANIFEST_PATH = ROOT / "docs/experiments/manifests/math16_pilot02_qwen4b_runtime_manifest.json"
PLAN_PATH = ROOT / "docs/experiments/manifests/math16_pilot02_qwen4b_cell_plan.json"
V1_SPEC_DIR = ROOT / "docs/experiments/prompts/ab2d_spec/prompts"

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

REQUIRED_RUNTIME_FIELDS = [
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
    "stop_sequences",
    "timeout_seconds",
    "retry_policy",
    "hardware",
    "cold_warm",
    "source_commit",
]


def sha_text(text: str) -> str:
    return hashlib.sha256(text.replace("\r\n", "\n").encode("utf-8")).hexdigest()


def sha_file_lf(path: Path) -> str:
    return sha_text(path.read_text(encoding="utf-8"))


def sha_json(obj: Any) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()


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

    for field in REQUIRED_RUNTIME_FIELDS:
        if field not in manifest or manifest[field] in (None, ""):
            raise RuntimeError(f"missing required runtime field: {field}")
    if manifest["thinking_mode"] is not False:
        raise RuntimeError("thinking_mode must be false")
    if manifest.get("thinking_mode") is None:
        raise RuntimeError("thinking_mode must not be null")

    # seed transport declaration vs adapter
    from scripts.math16_qwen_ollama_adapter import build_math16_chat_payload

    payload = build_math16_chat_payload(
        "preflight", seed=int(manifest["seed_list"][0]), model=manifest["model_tag"]
    )
    seed_in_options = "seed" in (payload.get("options") or {})
    if bool(manifest["seed_transport_supported"]) != seed_in_options:
        raise RuntimeError("seed_transport_supported disagrees with adapter payload")
    if payload.get("think") is not False:
        raise RuntimeError("adapter think must be false")

    fp = compute_fingerprint(manifest)
    if fp != manifest["runtime_config_fingerprint"]:
        raise RuntimeError(
            f"fingerprint mismatch: stored={manifest['runtime_config_fingerprint']} got={fp}"
        )

    if len(plan) != 320:
        raise RuntimeError(f"expected 320 cells, got {len(plan)}")
    ids = [c["cell_id"] for c in plan]
    if len(set(ids)) != 320:
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

    # prompt SHA verification
    from agent_tools.finals_rebuild.ce115_clean_incremental_ablation import (
        build_condition_prompt,
    )
    from agent_tools.finals_rebuild.math16_pool import frozen_for_prompt, tasks_by_id

    tasks = tasks_by_id()
    registry = {
        (r["task_id"], r["condition"]): r
        for r in manifest["prompt_verification_registry"]
    }
    for cell in plan:
        key = (cell["task_id"], cell["condition"])
        reg = registry[key]
        if cell["prompt_sha256"] != reg["prompt_sha256"]:
            raise RuntimeError(f"plan/registry sha mismatch {cell['cell_id']}")
        if cell["condition"] == "ab2d_spec_v2":
            path = ROOT / cell["prompt_path"]
            if "ab2d_spec_v2" not in str(cell["prompt_path"]).replace("\\", "/"):
                raise RuntimeError(f"spec path not v2: {cell['prompt_path']}")
            if "ab2d_spec/" in str(cell["prompt_path"]).replace("\\", "/") and "ab2d_spec_v2" not in str(cell["prompt_path"]):
                raise RuntimeError(f"v1 path leaked: {cell['prompt_path']}")
            if not path.exists():
                raise RuntimeError(f"missing prompt file {path}")
            if sha_file_lf(path) != cell["prompt_sha256"]:
                raise RuntimeError(f"file sha mismatch {path}")
        else:
            task = tasks[cell["task_id"]]
            frozen = frozen_for_prompt(task)
            built = build_condition_prompt(cell["condition"], task, frozen)
            if sha_text(built) != cell["prompt_sha256"]:
                raise RuntimeError(f"builder sha mismatch {cell['cell_id']}")

    # no v1 condition id
    if any(c["condition"] == "ab2d_spec" for c in plan):
        raise RuntimeError("ab2d_spec v1 condition leaked into plan")

    # hashes locked
    if manifest["taxonomy_hash"] != (
        "7df8f4472ce048569967436cbc73ede8fd4bd117ad67d0028ddd95af2055a304"
    ):
        raise RuntimeError("taxonomy hash drift")
    if manifest["evaluator_hash"] != (
        "2cca19f2258d4ba6134ff10d4e9bcff925e2441c32820fcbc151cb6b1dd740bc"
    ):
        raise RuntimeError("evaluator hash drift")

    # API cards present in patched prompts
    for tid in (
        "ce111_q05_exact_fraction_expression",
        "ce112_q12_independent_probability_fraction",
        "ce113_q01_negative_fraction_subtraction",
    ):
        text = (ROOT / f"docs/experiments/prompts/ab2d_spec_v2/prompts/{tid}.txt").read_text(
            encoding="utf-8"
        )
        if "`FractionOps.create`" not in text or "signature: `(value)`" not in text:
            raise RuntimeError(f"missing create(value) card in {tid}")
        if "`FractionOps.from_parts`" not in text or "(numerator, denominator)" not in text:
            raise RuntimeError(f"missing from_parts card in {tid}")
    q02 = (
        ROOT
        / "docs/experiments/prompts/ab2d_spec_v2/prompts/ce111_q02_polynomial_division_remainder.txt"
    ).read_text(encoding="utf-8")
    if "PolynomialOps.format_latex" not in q02 or "var='x'" not in q02:
        raise RuntimeError("missing format_latex(coeffs, var='x') in q02 v2")

    # compare shared prompt SHAs vs Gemini inventory for ab1/ab2g/ab2d
    gemini_inv = json.loads(
        (
            ROOT
            / "docs/experiments/manifests/math16_pilot02_full_analysis_inventory.json"
        ).read_text(encoding="utf-8")
    )
    gemini_sha = {}
    for row in gemini_inv:
        if row["condition"] in ("ab1", "ab2g", "ab2d") and int(row["seed"]) == 2026071301:
            gemini_sha[(row["task_id"], row["condition"])] = row["prompt_sha256"]
    for (tid, cond), sha in gemini_sha.items():
        qsha = registry[(tid, cond)]["prompt_sha256"]
        if qsha != sha:
            raise RuntimeError(
                f"shared prompt SHA drift vs Gemini inventory: {tid}/{cond}"
            )

    # ensure v1 prompt dir not referenced by plan paths
    for cell in plan:
        p = cell.get("prompt_path") or ""
        if p.startswith("docs/experiments/prompts/ab2d_spec/") and "ab2d_spec_v2" not in p:
            raise RuntimeError(f"plan references v1 path: {p}")

    result = {
        "preflight": "PASS",
        "cells": 320,
        "fingerprint": fp,
        "thinking_mode": False,
        "seed_transport_supported": True,
        "llm_generation_calls": 0,
        "model_calls": 0,
    }
    print(json.dumps(result, indent=2))
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preflight-only", action="store_true", required=True)
    parser.parse_args()
    do_preflight()
    print("MATH16_PILOT02_QWEN4B_RUNTIME_PREFLIGHT_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
