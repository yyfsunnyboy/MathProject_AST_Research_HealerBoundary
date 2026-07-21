"""Math16-LaTeX-v1 Qwen 4B Ab2s Integer Pilot Runner.

Executes:
- 4 integer tasks x 2 conditions (ab2d_replication, ab2s_integer_skill)
- Seed: 2026071301
- Model: qwen3.5:4b (via Ollama local transport)
- No Healer active (first valid response only)
- Evaluated using frozen evaluator and classification rules.
"""
from __future__ import annotations

import difflib
import json
import hashlib
import os
import sys
import time
import traceback
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.math16_pool import build_pool_tasks, frozen_for_prompt
from agent_tools.finals_rebuild.ce115_clean_incremental_ablation import build_condition_prompt, prompt_sha256
from agent_tools.finals_rebuild.failure_classification_v2 import classify_math16_cell_for_future_runner
from scripts.math16_qwen_ollama_adapter import call_qwen_with_retries, DEFAULT_BASE_URL
from scripts.run_math16_latex_v1_gemini_live import classify_math16_response

SEED = 2026071301
MODEL = "qwen3.5:4b"

TARGET_TASKS = [
    "ce111_q03_prime_factor_selection",
    "ce112_q01_negative_integer_power",
    "ce112_q09_divisor_multiple_intersection",
    "ce111_nonchoice_q01_part1_exponential_growth"
]

def load_ab2s_prompts() -> dict[str, str]:
    spec_path = ROOT / "docs/experiments/manifests/ab2s_integer_prompt_spec_v1.md"
    with open(spec_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Normalize CRLF to LF
    content = content.replace('\r\n', '\n')

    # Split using hex representation of backtick to avoid powershell parsing issues
    parts = content.split('\x60\x60\x60text\n')
    if len(parts) < 5:
        raise RuntimeError(f"Expected at least 5 parts in prompt spec markdown split, got {len(parts)}")

    prompts = {}
    for i, tid in enumerate(TARGET_TASKS):
        block = parts[i+1].split('\x60\x60\x60')[0].rstrip('\n')
        prompts[tid] = block
    return prompts

def verify_and_get_prompts() -> dict[str, dict[str, str]]:
    tasks = {t["task_id"]: t for t in build_pool_tasks()}
    ab2s_drafts = load_ab2s_prompts()

    # Read prompt index for ab2d expected hashes
    index_path = ROOT / "docs/experiments/prompts/math16/math16_prompt_index.json"
    with open(index_path, "r", encoding="utf-8") as f:
        index_data = json.load(f)

    expected_ab2d_hashes = {}
    for item in index_data:
        if item["task_id"] in TARGET_TASKS and item["condition"] == "ab2d":
            expected_ab2d_hashes[item["task_id"]] = item["prompt_sha256"]

    prompts = {}
    mismatches = []

    for tid in TARGET_TASKS:
        task = tasks[tid]
        frozen = frozen_for_prompt(task)

        # 1. ab2d_replication
        ab2d_prompt = build_condition_prompt("ab2d", task, frozen)
        ab2d_sha = prompt_sha256(ab2d_prompt)
        expected_ab2d = expected_ab2d_hashes[tid]
        if ab2d_sha != expected_ab2d:
            mismatches.append(f"ab2d mismatch for {tid}: got {ab2d_sha}, expected {expected_ab2d}")

        # 2. ab2s_integer_skill
        ab2s_prompt = ab2s_drafts[tid]
        ab2s_sha = prompt_sha256(ab2s_prompt)

        # Verify ab2g prefix exact-match
        ab2g_prompt = build_condition_prompt("ab2g", task, frozen)
        if not ab2s_prompt.startswith(ab2g_prompt):
            mismatches.append(f"ab2s prefix mismatch for {tid}: does not start with ab2g prompt")

        # Verify no leaks or forbidden tokens in ab2s block
        forbidden_tokens = ["Ab2d-v1", "ab2d_v1", "Ab4", "ab4", "core.prompts.domain_function_library"]
        for token in forbidden_tokens:
            if token in ab2s_prompt:
                mismatches.append(f"Forbidden token {token!r} found in ab2s prompt for {tid}")

        prompts[tid] = {
            "ab2d_replication": ab2d_prompt,
            "ab2s_integer_skill": ab2s_prompt
        }

    if mismatches:
        for m in mismatches:
            print("ERROR:", m)
        print("BLOCKED_ACTUAL_PROMPT_MISMATCH")
        sys.exit(1)

    print("Preflight verification PASSED: All prompts are byte-exact and aligned with spec.")
    return prompts

def run_pilot():
    prompts = verify_and_get_prompts()
    tasks = {t["task_id"]: t for t in build_pool_tasks()}

    output_dir = ROOT / "docs/experiments/results/math16_ab2s_pilot_integer_4b"
    output_dir.mkdir(parents=True, exist_ok=True)

    results = []

    # 4 tasks x 2 conditions
    for tid in TARGET_TASKS:
        task = tasks[tid]
        frozen = frozen_for_prompt(task)

        for condition in ("ab2d_replication", "ab2s_integer_skill"):
            cell_id = f"qwen35_4b__{tid}__{condition}__seed_{SEED}"
            print("="*80)
            print(f"Running cell: {cell_id}")
            print("="*80)

            prompt = prompts[tid][condition]
            prompt_sha = prompt_sha256(prompt)

            # Execute Qwen 3.5 4B
            started = time.monotonic()
            response = call_qwen_with_retries(prompt, seed=SEED, model=MODEL)
            wall = time.monotonic() - started

            raw_response = response["raw_text"]
            metadata = response["metadata"]
            api_attempts = response["api_attempts"]

            # Classify using frozen validator
            outcome, code, details = classify_math16_response(
                raw_response,
                frozen_params=frozen["oracle_payload"],
                audit_oracle_payload=task["oracle_payload"],
                task=task,
                execution_timeout=3.0
            )

            completion = "NATURAL_COMPLETE" if code else outcome.upper()
            evaluator = "PASSED" if outcome == "passed" else (
                "ANSWER_INCORRECT" if outcome == "answer_incorrect" else "EXECUTION_FAILURE"
            )
            failure_category = "none" if outcome == "passed" else outcome

            # Get failure layer
            failure_layer = classify_math16_cell_for_future_runner(
                evaluation_gates=details.get("evaluation_gates") or details.get("gates"),
                evaluator_status=evaluator,
                validity=details.get("validity"),
                infrastructure_valid=details.get("validity") != "INVALID_INFRASTRUCTURE",
                raw_response_present=bool(raw_response),
            )

            cell_data = {
                "cell_id": cell_id,
                "task_id": tid,
                "condition": condition,
                "model": MODEL,
                "seed": SEED,
                "prompt_sha256": prompt_sha,
                "prompt_char_length": len(prompt),
                "prompt_byte_length": len(prompt.encode("utf-8")),
                "raw_first_attempt_output": raw_response,
                "candidate_extracted": code,
                "evaluator_status": evaluator,
                "failure_category": failure_category,
                "failure_layer": failure_layer,
                "wall_clock_seconds": wall,
                "provider_duration": metadata.get("latency_ms"),
                "gates": details.get("evaluation_gates") or details.get("gates"),
                "hashes": {
                    "prompt": prompt_sha,
                    "raw": hashlib.sha256(raw_response.encode("utf-8")).hexdigest(),
                    "extracted_candidate": hashlib.sha256((code or "").encode("utf-8")).hexdigest(),
                },
                "provenance": {
                    "first_attempt_only": True,
                    "api_retry_same_cell": True,
                    "api_attempts": api_attempts,
                    "adapter": "math16_qwen_ollama_adapter",
                    "model_version": MODEL,
                },
                "persisted_complete": True
            }
            results.append(cell_data)

            # Save cell-specific files
            cell_dir = output_dir / "cells" / cell_id
            cell_dir.mkdir(parents=True, exist_ok=True)

            with open(cell_dir / "prompt.txt", "w", encoding="utf-8", newline="\n") as f:
                f.write(prompt)
            with open(cell_dir / "raw_response.txt", "w", encoding="utf-8", newline="\n") as f:
                f.write(raw_response)
            if code:
                with open(cell_dir / "extracted_candidate.py", "w", encoding="utf-8", newline="\n") as f:
                    f.write(code)
            with open(cell_dir / "artifact.json", "w", encoding="utf-8", newline="\n") as f:
                json.dump(cell_data, f, indent=2, ensure_ascii=False)

            print(f"Cell outcome: {evaluator} | failure_category: {failure_category} | failure_layer: {failure_layer.get('primary_layer')}")

    # Write summary
    with open(output_dir / "cell_results.json", "w", encoding="utf-8", newline="\n") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print("="*80)
    print("EXPLORATORY PILOT EXECUTION COMPLETED")
    print("="*80)

if __name__ == "__main__":
    run_pilot()
