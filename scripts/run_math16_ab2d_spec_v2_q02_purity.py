# -*- coding: utf-8 -*-
"""Generate remaining 3 q02 ab2d_spec_v2 seeds for version purity (same frozen prompt)."""
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
RUNTIME_MANIFEST_PATH = ROOT / "docs/experiments/manifests/math16_pilot02_ab2d_spec_v2_runtime_manifest.json"
PLAN_PATH = ROOT / "docs/experiments/manifests/math16_pilot02_ab2d_spec_v2_q02_purity_plan.json"
OUTPUT_ROOT = ROOT / "docs/experiments/results/math16_pilot02_ab2d_spec_v2_gemini"
EXPECTED_PROMPT_SHA = "f9a51940b166e8613557d1490cf1a331467ffd95af8ca96617aeded15c78fb87"
EXPECTED_FINGERPRINT = "8bcb0d7177bc35216410108bda88b014848181a95b12bc09bf171866749f3057"
CONDITION = "ab2d_spec_v2"
TASK_ID = "ce111_q02_polynomial_division_remainder"
SEEDS = [2026072001, 2026072002, 2026072004]
ALREADY_PURE = [2026071301, 2026072003]
FROZEN_EXISTING = {
    "ce111_q05_exact_fraction_expression": "927977168ad6a72c644641fed7ef653495e55279689dc0beb06253033242926d",
    "ce112_q12_independent_probability_fraction": "183c3a708e2a1361e9ccd41de1cb33c51bb169b1f6b7cd99d874f98aa23ada51",
    "ce113_q01_negative_fraction_subtraction": "319926943ccbc9ca260979e04cf024cc1d896f00bc3e6be23e7b9632170ca54a",
    "ce111_q08_polynomial_factor_parameter_recovery": "4e8f345ad99e87317c2bb38ce741268ce4f57d9e2ca98518eea4f37fb36fb477",
}


def sha_lf(path: Path) -> str:
    return hashlib.sha256(path.read_text(encoding="utf-8").replace("\r\n", "\n").encode()).hexdigest()


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


def build_plan() -> tuple[dict, list[dict], dict]:
    runtime = json.loads(RUNTIME_MANIFEST_PATH.read_text(encoding="utf-8"))
    spec = json.loads(SPEC_V2_MANIFEST.read_text(encoding="utf-8"))
    by_id = {t["task_id"]: t for t in spec["tasks"]}
    task = by_id[TASK_ID]
    if task["exact_prompt_sha256"] != EXPECTED_PROMPT_SHA:
        raise RuntimeError("q02 frozen prompt SHA drift")
    prompt_path = ROOT / task["prompt_path"]
    if sha_lf(prompt_path) != EXPECTED_PROMPT_SHA:
        raise RuntimeError("q02 prompt file SHA drift — refuse to regenerate")
    for tid, expected in FROZEN_EXISTING.items():
        p = ROOT / "docs/experiments/prompts/ab2d_spec_v2/prompts" / f"{tid}.txt"
        if sha_lf(p) != expected:
            raise RuntimeError(f"Existing v2 task mutated: {tid}")
    # existing pure cells must remain
    for seed in ALREADY_PURE:
        d = (
            OUTPUT_ROOT
            / "cells"
            / f"gemini_3_5_flash__{TASK_ID}__{CONDITION}__seed_{seed}"
        )
        art = json.loads((d / "artifact.json").read_text(encoding="utf-8"))
        if art.get("prompt_sha256") != EXPECTED_PROMPT_SHA:
            raise RuntimeError(f"Already-pure seed {seed} SHA mismatch")

    plan = []
    for seed in SEEDS:
        cell_id = f"gemini_3_5_flash__{TASK_ID}__{CONDITION}__seed_{seed}"
        plan.append(
            {
                "cell_id": cell_id,
                "task_id": TASK_ID,
                "family": "polynomial",
                "condition": CONDITION,
                "seed": seed,
                "model_tag": "gemini-3.5-flash",
                "prompt_sha256": EXPECTED_PROMPT_SHA,
                "prompt_path": task["prompt_path"],
                "api_policy": task["api_policy"],
                "output_relative_path": f"math16_pilot02_ab2d_spec_v2_gemini/cells/{cell_id}",
            }
        )
    PLAN_PATH.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return runtime, plan, task


def run_with_retries(prompt: str, cell_id: str, execute_fn, retry_policy: dict) -> dict:
    delays = list(retry_policy.get("retry_delays_seconds") or [5, 20])
    max_attempts = int(retry_policy.get("max_attempts") or 3)
    api_attempts = []
    last_err = None
    for attempt in range(1, max_attempts + 1):
        try:
            resp = execute_fn(prompt)
            raw = resp.get("raw_text")
            if not isinstance(raw, str) or not raw.strip():
                raise RuntimeError("empty response")
            meta = dict(resp.get("metadata") or {})
            meta["attempt_count"] = attempt
            api_attempts.append({"attempt": attempt, "ok": True})
            return {"raw_text": raw, "metadata": meta, "api_attempts": api_attempts}
        except Exception as exc:  # noqa: BLE001
            last_err = exc
            api_attempts.append({"attempt": attempt, "ok": False, "error": str(exc)})
            if attempt < max_attempts:
                time.sleep(delays[min(attempt - 1, len(delays) - 1)])
    raise RuntimeError(f"retries exhausted for {cell_id}: {last_err}")


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--preflight-only", action="store_true")
    group.add_argument("--execute", action="store_true")
    args = parser.parse_args()

    runtime, plan, task = build_plan()
    print(
        json.dumps(
            {
                "preflight": "PASS",
                "cells": 3,
                "seeds": SEEDS,
                "prompt_sha256": EXPECTED_PROMPT_SHA,
                "already_pure_seeds": ALREADY_PURE,
            },
            indent=2,
        )
    )
    if args.preflight_only:
        return 0

    from scripts.ce115_v4_gemini_transport import api_key_status, call_gemini_once

    if not api_key_status().get("api_key_present"):
        raise RuntimeError("GEMINI_API_KEY missing")

    prompt_path = ROOT / task["prompt_path"]
    prompt = prompt_path.read_text(encoding="utf-8")
    model_calls = 0
    total_prompt = total_cand = total_tok = 0

    for idx, cell in enumerate(plan):
        cell_dir = ROOT / "docs/experiments/results" / cell["output_relative_path"]
        if cell_dir.exists() and (cell_dir / "artifact.json").exists():
            raise RuntimeError(f"Refuse overwrite existing cell {cell['cell_id']}")
        print(f"[{idx+1}/3] Calling Gemini {cell['cell_id']}")

        def execute_fn(p: str):
            nonlocal model_calls
            model_calls += 1
            return call_gemini_once(p, model=cell["model_tag"])

        started = datetime.now(timezone.utc).isoformat()
        t0 = time.monotonic()
        result = run_with_retries(prompt, cell["cell_id"], execute_fn, runtime["retry_policy"])
        duration = time.monotonic() - t0
        meta = result["metadata"]
        total_prompt += int(meta.get("prompt_token_count") or 0)
        total_cand += int(meta.get("candidates_token_count") or 0)
        total_tok += int(meta.get("total_token_count") or 0)
        art = {
            "experiment_id": runtime["experiment_id"],
            "cell_id": cell["cell_id"],
            "task_id": TASK_ID,
            "condition": CONDITION,
            "seed": cell["seed"],
            "model_tag": cell["model_tag"],
            "runtime_config_fingerprint": EXPECTED_FINGERPRINT,
            "runtime_parameters": {
                "temperature": runtime["temperature"],
                "max_output_tokens": runtime["max_output_tokens"],
            },
            "prompt_sha256": EXPECTED_PROMPT_SHA,
            "raw_response": result["raw_text"],
            "attempt_count": meta.get("attempt_count"),
            "started_at_utc": started,
            "completed_at_utc": datetime.now(timezone.utc).isoformat(),
            "duration": duration,
            "persisted_complete": True,
            "provenance": {
                "api_attempts": result["api_attempts"],
                "provider_metadata": {
                    "prompt_token_count": meta.get("prompt_token_count"),
                    "candidates_token_count": meta.get("candidates_token_count"),
                    "total_token_count": meta.get("total_token_count"),
                },
                "patch": "q02_version_purity_remaining_3_seeds",
            },
        }
        cell_dir.mkdir(parents=True, exist_ok=True)
        _atomic_write_text(cell_dir / "prompt.txt", prompt)
        _atomic_write_text(cell_dir / "raw_response.txt", result["raw_text"])
        _atomic_write_text(cell_dir / "artifact.json", json.dumps(art, ensure_ascii=False, indent=2) + "\n")
        print(f"[{idx+1}/3] saved")

    out_tokens = max(0, total_tok - total_prompt)
    cost = total_prompt * 1.50 / 1e6 + out_tokens * 9.00 / 1e6
    summary = {
        "completed": 3,
        "expected": 3,
        "model_calls": model_calls,
        "retries_used": 0,
        "total_prompt_tokens": total_prompt,
        "total_candidate_tokens": total_cand,
        "total_tokens": total_tok,
        "estimated_api_cost_usd": round(cost, 4),
        "pricing_basis": "gemini-3.5-flash USD1.50/1M in + USD9.00/1M out(incl thinking)",
        "prompt_sha256": EXPECTED_PROMPT_SHA,
        "seeds": SEEDS,
    }
    _atomic_write_text(
        OUTPUT_ROOT / "q02_purity_generation_summary.json",
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
    )
    print(json.dumps(summary, indent=2))
    if model_calls != 3:
        raise RuntimeError(f"expected 3 model calls, got {model_calls}")
    print("AB2D_SPEC_V2_Q02_PURITY_GENERATION_COMPLETE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
