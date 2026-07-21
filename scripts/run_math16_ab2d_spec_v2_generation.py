# -*- coding: utf-8 -*-
"""Generate Math16 Ab2d+spec-v2 patch cells (4 tasks × 5 seeds = 20).

Never overwrites ab2d_spec v1 prompts, full_gemini cells, v3/v4 evaluations,
or ORACLE_SCHEMA_AUDIT_V1.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

SPEC_V2_MANIFEST = ROOT / "docs/experiments/prompts/ab2d_spec_v2/manifest.json"
SPEC_V1_MANIFEST = ROOT / "docs/experiments/prompts/ab2d_spec/manifest.json"
FULL_RUNTIME_MANIFEST = ROOT / "docs/experiments/manifests/math16_pilot02_full_runtime_manifest.json"
PLAN_PATH = ROOT / "docs/experiments/manifests/math16_pilot02_ab2d_spec_v2_generation_plan.json"
RUNTIME_MANIFEST_PATH = ROOT / "docs/experiments/manifests/math16_pilot02_ab2d_spec_v2_runtime_manifest.json"
OUTPUT_ROOT = ROOT / "docs/experiments/results/math16_pilot02_ab2d_spec_v2_gemini"
V1_PROMPT_DIR = ROOT / "docs/experiments/prompts/ab2d_spec/prompts"
AUDIT_V1 = ROOT / "docs/experiments/audits/math16_pilot02_oracle_schema_audit_v1.md"
V3_OUT = ROOT / "docs/experiments/results/math16_pilot02_full_evaluation_v3_r001"
V4_OUT = ROOT / "docs/experiments/results/math16_pilot02_full_evaluation_v4_r001"

EXPECTED_FINGERPRINT = "8bcb0d7177bc35216410108bda88b014848181a95b12bc09bf171866749f3057"
EXPECTED_AUDIT_SHA = "53906c5c3c8abb9412352a49c0e79f3ecda7b1f20183d9ec1084da1fe816fa73"
MODEL_TAG = "gemini-3.5-flash"
CONDITION = "ab2d_spec_v2"


def get_file_sha256(path: Path) -> str:
    content = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def _raw_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    import tempfile

    fd, tmp_name = tempfile.mkstemp(prefix=path.name + ".", dir=str(path.parent))
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_path, path)
    finally:
        if tmp_path.exists():
            try:
                tmp_path.unlink()
            except OSError:
                pass


def build_plan_and_runtime() -> tuple[dict, list[dict]]:
    full = json.loads(FULL_RUNTIME_MANIFEST.read_text(encoding="utf-8"))
    spec_v2 = json.loads(SPEC_V2_MANIFEST.read_text(encoding="utf-8"))
    seeds = list(full["seed_list"])
    assert seeds == [2026071301, 2026072001, 2026072002, 2026072003, 2026072004]

    runtime = {
        "experiment_id": "math16_pilot02_ab2d_spec_v2_gemini_freeze_v1",
        "model_provider": full["model_provider"],
        "model_tag": full["model_tag"],
        "model_version": full["model_version"],
        "runtime": full["runtime"],
        "runtime_version": full["runtime_version"],
        "thinking_mode": full["thinking_mode"],
        "temperature": full["temperature"],
        "top_p": full["top_p"],
        "top_k": full["top_k"],
        "max_output_tokens": full["max_output_tokens"],
        "timeout_seconds": full["timeout_seconds"],
        "retry_policy": full["retry_policy"],
        "seed_list": seeds,
        "source_commit": full.get("source_commit"),
        "parent_experiment_id": full["experiment_id"],
        "prompt_revision": "ab2d_spec_v2",
        "created_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "runtime_config_fingerprint": EXPECTED_FINGERPRINT,
        "scope": "ab2d_spec_v2_api_gap_patch_20_cells",
        "llm_policy": "gemini live; exactly one successful call per cell after retries",
    }
    # Fingerprint must match full freeze keys subset
    keys = [
        "experiment_id",
        "model_provider",
        "model_tag",
        "model_version",
        "runtime",
        "runtime_version",
        "thinking_mode",
        "temperature",
        "top_p",
        "top_k",
        "max_output_tokens",
        "timeout_seconds",
        "retry_policy",
        "seed_list",
        "source_commit",
    ]
    # Use parent fingerprint identity: verify parent full manifest fingerprint still matches.
    parent_sub = {k: full[k] for k in keys}
    parent_fp = hashlib.sha256(
        json.dumps(parent_sub, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()
    if parent_fp != EXPECTED_FINGERPRINT:
        raise ValueError(f"Parent runtime fingerprint drift: {parent_fp}")

    plan: list[dict] = []
    for task in spec_v2["tasks"]:
        tid = task["task_id"]
        for seed in seeds:
            cell_id = f"{MODEL_TAG.replace('.', '_').replace('-', '_')}__{tid}__{CONDITION}__seed_{seed}"
            # Keep gemini_3_5_flash style used elsewhere
            cell_id = f"gemini_3_5_flash__{tid}__{CONDITION}__seed_{seed}"
            rel = f"math16_pilot02_ab2d_spec_v2_gemini/cells/{cell_id}"
            plan.append(
                {
                    "cell_id": cell_id,
                    "task_id": tid,
                    "family": task["family"],
                    "condition": CONDITION,
                    "seed": seed,
                    "model_tag": MODEL_TAG,
                    "prompt_sha256": task["exact_prompt_sha256"],
                    "prompt_path": task["prompt_path"],
                    "api_policy": task["api_policy"],
                    "output_relative_path": rel,
                }
            )

    if len(plan) != 20:
        raise ValueError(f"Expected 20-cell plan, got {len(plan)}")

    RUNTIME_MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    RUNTIME_MANIFEST_PATH.write_text(
        json.dumps(runtime, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    PLAN_PATH.write_text(
        json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    return runtime, plan


def do_preflight() -> dict:
    print("=== Ab2d+spec-v2 zero-model preflight ===")
    runtime, plan = build_plan_and_runtime()
    spec_v2 = json.loads(SPEC_V2_MANIFEST.read_text(encoding="utf-8"))
    spec_v1 = json.loads(SPEC_V1_MANIFEST.read_text(encoding="utf-8"))

    # 1. v2 prompt SHA consistency
    for task in spec_v2["tasks"]:
        path = ROOT / task["prompt_path"]
        actual = get_file_sha256(path)
        if actual != task["exact_prompt_sha256"]:
            raise ValueError(f"v2 prompt SHA mismatch for {task['task_id']}")
        text = path.read_text(encoding="utf-8")
        if task["family"] == "fraction":
            if "FractionOps.create" not in text or "FractionOps.from_parts" not in text:
                raise ValueError(f"Missing FractionOps cards in {task['task_id']}")
            if "(value)" not in text or "(numerator, denominator)" not in text:
                raise ValueError(f"Incomplete FractionOps signatures in {task['task_id']}")
        else:
            if "PolynomialOps.format_latex" not in text:
                raise ValueError(f"Missing format_latex in {task['task_id']}")
            if "to_latex" not in text:
                raise ValueError(f"Missing to_latex prohibition in {task['task_id']}")

        # Answer non-leak: frozen answers must not appear as explicit answer dumps
        if "answer=-12" in text or '"remainder": "4x"' in text:
            raise ValueError(f"Possible answer leak in {task['task_id']}")

    # 2. API policy consistency vs v1 for same task ids
    v1_by_id = {t["task_id"]: t for t in spec_v1["tasks"]}
    for task in spec_v2["tasks"]:
        v1 = v1_by_id[task["task_id"]]
        if task["api_policy"] != v1["api_policy"]:
            raise ValueError(
                f"api_policy drift for {task['task_id']}: v2={task['api_policy']} v1={v1['api_policy']}"
            )

    # 3. Guardrail isolation: v2 guardrail sha == v1 guardrail sha
    for task in spec_v2["tasks"]:
        v2g = ROOT / task["task_guardrail_source"]
        v1g = (
            ROOT
            / "docs/experiments/prompts/ab2d_spec/task_guardrails"
            / Path(task["task_guardrail_source"]).parts[-2]
            / Path(task["task_guardrail_source"]).name
        )
        if get_file_sha256(v2g) != get_file_sha256(v1g):
            raise ValueError(f"Guardrail isolation failed for {task['task_id']}")

    # 4. v1 prompts / evaluations / audit untouched
    snapshot = spec_v2.get("prior_v1_prompt_sha256_snapshot") or {}
    for name, sha in snapshot.items():
        if get_file_sha256(V1_PROMPT_DIR / name) != sha:
            raise ValueError(f"v1 prompt changed: {name}")
    if get_file_sha256(SPEC_V1_MANIFEST) != spec_v2["prior_manifest_sha256"]:
        raise ValueError("v1 spec manifest changed")
    if not (V3_OUT / "cell_level_baseline.jsonl").exists():
        raise FileNotFoundError("v3_r001 missing")
    if not (V4_OUT / "cell_level_baseline.jsonl").exists():
        raise FileNotFoundError("v4_r001 missing")
    if _raw_sha256(AUDIT_V1) != EXPECTED_AUDIT_SHA:
        raise ValueError(
            f"ORACLE_SCHEMA_AUDIT_V1 mutated: expected {EXPECTED_AUDIT_SHA}, got {_raw_sha256(AUDIT_V1)}"
        )

    # 5. Plan geometry
    if len(plan) != 20:
        raise ValueError("plan size != 20")
    if len({c["cell_id"] for c in plan}) != 20:
        raise ValueError("duplicate cell ids")
    from collections import Counter

    if Counter(c["task_id"] for c in plan) != {
        t["task_id"]: 5 for t in spec_v2["tasks"]
    }:
        raise ValueError("task×seed geometry mismatch")
    if any(c["condition"] != CONDITION for c in plan):
        raise ValueError("condition must be ab2d_spec_v2")

    report = {
        "preflight": "PASS",
        "cells": 20,
        "fingerprint_parent": EXPECTED_FINGERPRINT,
        "tasks": [t["task_id"] for t in spec_v2["tasks"]],
        "v1_untouched": True,
        "v3_present": True,
        "v4_present": True,
        "audit_v1_sha256": EXPECTED_AUDIT_SHA,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("AB2D_SPEC_V2_PREFLIGHT_PASS")
    return {"runtime": runtime, "plan": plan, "spec_v2": spec_v2}


def quarantine_cell(cell_id: str, cell_dir: Path, output_root: Path) -> None:
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    quarantine_dir = output_root / "_quarantine" / f"{cell_id}__{ts}"
    quarantine_dir.mkdir(parents=True, exist_ok=True)
    if cell_dir.exists():
        for item in list(cell_dir.iterdir()):
            item.rename(quarantine_dir / item.name)
        if cell_dir.exists():
            try:
                cell_dir.rmdir()
            except OSError:
                pass
    print(f"Quarantined incomplete cell {cell_id} → {quarantine_dir}")


def run_cell_with_retries(prompt: str, cell_id: str, execute_fn, retry_policy: dict) -> dict:
    delays = list(retry_policy.get("retry_delays_seconds") or [5, 20])
    max_attempts = int(retry_policy.get("max_attempts") or 3)
    api_attempts = []
    last_err = None
    for attempt in range(1, max_attempts + 1):
        try:
            resp = execute_fn(prompt)
            raw = resp.get("raw_text") if isinstance(resp, dict) else None
            if raw is None and isinstance(resp, dict):
                raw = resp.get("text")
            if not isinstance(raw, str) or not raw.strip():
                raise RuntimeError("empty model response")
            meta = dict(resp.get("metadata") or {})
            meta["attempt_count"] = attempt
            api_attempts.append({"attempt": attempt, "ok": True})
            return {
                "raw_text": raw,
                "metadata": meta,
                "api_attempts": api_attempts,
                "response": resp,
            }
        except Exception as exc:  # noqa: BLE001
            last_err = exc
            api_attempts.append({"attempt": attempt, "ok": False, "error": str(exc)})
            if attempt < max_attempts:
                delay = delays[min(attempt - 1, len(delays) - 1)]
                print(f"Retry {attempt}/{max_attempts} for {cell_id} after {delay}s: {exc}")
                time.sleep(delay)
    raise RuntimeError(f"All retries failed for {cell_id}: {last_err}")


def execute_generations(runtime: dict, plan: list[dict]) -> dict:
    from scripts.ce115_v4_gemini_transport import api_key_status, call_gemini_once

    status = api_key_status()
    if not status.get("api_key_present"):
        raise RuntimeError("GEMINI_API_KEY missing")

    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    _atomic_write_text(
        OUTPUT_ROOT / "manifest.json",
        json.dumps(runtime, ensure_ascii=False, indent=2) + "\n",
    )

    model_calls = 0
    completed = 0
    quarantined = 0
    retries_used = 0
    total_prompt_tokens = 0
    total_candidate_tokens = 0
    total_tokens = 0

    for idx, cell in enumerate(plan):
        cell_id = cell["cell_id"]
        cell_dir = ROOT / "docs/experiments/results" / cell["output_relative_path"]
        prompt_path = ROOT / cell["prompt_path"]
        prompt = prompt_path.read_text(encoding="utf-8")
        prompt_sha = get_file_sha256(prompt_path)
        if prompt_sha != cell["prompt_sha256"]:
            raise ValueError(f"Prompt SHA mismatch at execute time for {cell_id}")

        if cell_dir.exists() and (cell_dir / "artifact.json").exists():
            art = json.loads((cell_dir / "artifact.json").read_text(encoding="utf-8"))
            if (
                art.get("persisted_complete") is True
                and art.get("prompt_sha256") == cell["prompt_sha256"]
                and art.get("condition") == CONDITION
                and art.get("seed") == cell["seed"]
            ):
                print(f"[{idx+1}/20] SKIP complete: {cell_id}")
                completed += 1
                continue
            print(f"[{idx+1}/20] Incomplete/mismatch → quarantine {cell_id}")
            quarantine_cell(cell_id, cell_dir, OUTPUT_ROOT)
            quarantined += 1

        print(f"[{idx+1}/20] Calling Gemini for {cell_id}")

        def execute_fn(p: str):
            nonlocal model_calls
            model_calls += 1
            return call_gemini_once(p, model=cell["model_tag"])

        started_at = datetime.now(timezone.utc).isoformat()
        started_wall = time.monotonic()
        cell_result = run_cell_with_retries(
            prompt, cell_id, execute_fn, runtime["retry_policy"]
        )
        duration = time.monotonic() - started_wall
        attempts = cell_result["metadata"]["attempt_count"]
        if attempts > 1:
            retries_used += attempts - 1

        usage = {
            "prompt_token_count": cell_result["metadata"].get("prompt_token_count"),
            "candidates_token_count": cell_result["metadata"].get("candidates_token_count"),
            "total_token_count": cell_result["metadata"].get("total_token_count"),
        }
        total_prompt_tokens += int(usage.get("prompt_token_count") or 0)
        total_candidate_tokens += int(usage.get("candidates_token_count") or 0)
        total_tokens += int(usage.get("total_token_count") or 0)

        cell_data = {
            "experiment_id": runtime["experiment_id"],
            "cell_id": cell_id,
            "task_id": cell["task_id"],
            "condition": CONDITION,
            "seed": cell["seed"],
            "model_tag": cell["model_tag"],
            "runtime_config_fingerprint": EXPECTED_FINGERPRINT,
            "runtime_parameters": {
                "temperature": runtime["temperature"],
                "max_output_tokens": runtime["max_output_tokens"],
            },
            "prompt_sha256": cell["prompt_sha256"],
            "request_metadata": {
                "temperature": runtime["temperature"],
                "max_output_tokens": runtime["max_output_tokens"],
            },
            "raw_response": cell_result["raw_text"],
            "attempt_count": attempts,
            "started_at_utc": started_at,
            "completed_at_utc": datetime.now(timezone.utc).isoformat(),
            "duration": duration,
            "persisted_complete": True,
            "provenance": {
                "api_attempts": cell_result["api_attempts"],
                "provider_metadata": usage,
            },
        }
        cell_dir.mkdir(parents=True, exist_ok=True)
        _atomic_write_text(cell_dir / "prompt.txt", prompt)
        _atomic_write_text(cell_dir / "raw_response.txt", cell_result["raw_text"])
        _atomic_write_text(
            cell_dir / "artifact.json",
            json.dumps(cell_data, ensure_ascii=False, indent=2) + "\n",
        )
        completed += 1
        print(f"[{idx+1}/20] saved {cell_id} attempts={attempts}")

    summary = {
        "completed": completed,
        "expected": 20,
        "model_calls": model_calls,
        "retries_used": retries_used,
        "quarantined": quarantined,
        "total_prompt_tokens": total_prompt_tokens,
        "total_candidate_tokens": total_candidate_tokens,
        "total_tokens": total_tokens,
    }
    _atomic_write_text(
        OUTPUT_ROOT / "generation_summary.json",
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if completed != 20:
        raise RuntimeError(f"Expected 20/20 completed, got {completed}")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Ab2d+spec-v2 20-cell generation")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--preflight-only", action="store_true")
    group.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    try:
        data = do_preflight()
        if args.preflight_only:
            return 0
        execute_generations(data["runtime"], data["plan"])
        print("AB2D_SPEC_V2_20CELL_GENERATION_COMPLETE")
        return 0
    except Exception:
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
