# -*- coding: utf-8 -*-
"""Math16 Pilot-02 Integer generation runner with preflight validation."""
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

MANIFEST_PATH = ROOT / "docs/experiments/manifests/math16_pilot02_integer_runtime_manifest.json"
CELL_PLAN_PATH = ROOT / "docs/experiments/manifests/math16_pilot02_integer_cell_plan.json"

SPEC_HASHES = {
    "ce111_q03_prime_factor_selection": "5417185bc8f5d084bd04d6bf4d346762f6fa4738c6a52d30ea34706f4121e6f0",
    "ce112_q01_negative_integer_power": "1aa4f2a789b546a5f81f4a773db6c783edb359f5fbbc3c21966853d57db6a61b",
    "ce112_q09_divisor_multiple_intersection": "6ab35b719b39c1336e47f8fea3d373ec2482ad3f8d1c6979b192576090228035",
    "ce111_nonchoice_q01_part1_exponential_growth": "5d8e3f4084038b1e99a581bf26ad77e49c295362a076ff374e5614960f38c019"
}

def _hash(val: str) -> str:
    return hashlib.sha256(val.encode("utf-8")).hexdigest()

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

def do_preflight() -> dict[str, any]:
    print("Executing zero-model preflight checks...")

    # 1. Load manifest and cell plan
    if not MANIFEST_PATH.exists():
        raise FileNotFoundError(f"Manifest not found at {MANIFEST_PATH}")
    if not CELL_PLAN_PATH.exists():
        raise FileNotFoundError(f"Cell plan not found at {CELL_PLAN_PATH}")

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    cell_plan = json.loads(CELL_PLAN_PATH.read_text(encoding="utf-8"))

    # 2. Check source commit and lineage
    expected_commit = "dae588d99d9c68f920a8089f4a6ee0d24178f3a1"
    if manifest.get("source_commit") != expected_commit:
        raise ValueError(f"Source commit mismatch in manifest: expected {expected_commit}")

    # 3. Check geometry consistency
    expected_cells = 80
    if len(cell_plan) != expected_cells:
        raise ValueError(f"Cell plan size mismatch: expected {expected_cells}, got {len(cell_plan)}")
    if manifest.get("expected_cell_count") != expected_cells:
        raise ValueError(f"Manifest expected cell count mismatch: expected {expected_cells}")

    # 4. Check uniqueness
    cell_ids = set()
    output_paths = set()
    for cell in cell_plan:
        cell_id = cell["cell_id"]
        if cell_id in cell_ids:
            raise ValueError(f"Duplicate cell_id detected: {cell_id}")
        cell_ids.add(cell_id)

        out_path = cell["output_relative_path"]
        if out_path in output_paths:
            raise ValueError(f"Duplicate output path detected: {out_path}")
        output_paths.add(out_path)

    # 5. Check manifest vs cell plan variables
    if manifest["model_tag"] != "gemini-3.5-flash":
        raise ValueError(f"Model tag mismatch: expected gemini-3.5-flash")
    if manifest["temperature"] != 0.0:
        raise ValueError(f"Temperature mismatch: expected 0.0")
    if manifest["max_output_tokens"] != 24576:
        raise ValueError(f"Max output tokens mismatch: expected 24576")
    if manifest["timeout_seconds"] != 600:
        raise ValueError(f"Timeout mismatch: expected 600")

    # 6. Verify static ab2d_spec prompt files and hashes
    for task_id, expected_hash in SPEC_HASHES.items():
        spec_prompt_path = ROOT / "docs/experiments/prompts/ab2d_spec/prompts" / f"{task_id}.txt"
        if not spec_prompt_path.exists():
            raise FileNotFoundError(f"Spec prompt file not found: {spec_prompt_path}")
        prompt_content = spec_prompt_path.read_text(encoding="utf-8")
        actual_hash = _hash(prompt_content)
        if actual_hash != expected_hash:
            raise ValueError(f"Prompt hash mismatch for {task_id}: expected {expected_hash}, got {actual_hash}")

        # Verify 0 matches for forbidden strings
        for forbidden in ["IntegerOps", "domain_function_library", "Ab2d+api", "Domain API exposure"]:
            if forbidden in prompt_content:
                raise ValueError(f"Forbidden term '{forbidden}' found in spec prompt of {task_id}")

    # 7. Check that ab1/ab2g/ab2d prompts are buildable and match hashes
    from agent_tools.finals_rebuild.math16_pool import tasks_by_id, frozen_for_prompt
    from agent_tools.finals_rebuild.ce115_clean_incremental_ablation import build_condition_prompt, prompt_sha256

    tasks = tasks_by_id()
    for cell in cell_plan:
        cond = cell["condition"]
        tid = cell["task_id"]
        if cond in ["ab1", "ab2g", "ab2d"]:
            task = tasks[tid]
            frozen = frozen_for_prompt(task)
            built_prompt = build_condition_prompt(cond, task, frozen)
            built_hash = prompt_sha256(built_prompt)
            if built_hash != cell["prompt_sha256"]:
                raise ValueError(f"Built prompt hash mismatch for {cell['cell_id']}: expected {cell['prompt_sha256']}, got {built_hash}")

    print("Preflight checks PASSED successfully.")
    return {
        "manifest": manifest,
        "cell_plan": cell_plan
    }

def run_cell_with_retries(prompt: str, cell_id: str, execute_fn) -> dict[str, any]:
    """Execute model request with retry policy: max attempts 3, backoff [5, 20] seconds."""
    attempts = []
    last_exc = None

    for attempt in range(1, 4):
        started = time.monotonic()
        try:
            resp = execute_fn(prompt)
            raw = resp.get("raw_text") if isinstance(resp, dict) else None
            if raw is None and isinstance(resp, dict) and "text" in resp:
                raw = resp["text"]
            if not isinstance(raw, str) or not raw.strip():
                raise RuntimeError("empty_response")

            meta = dict(resp.get("metadata") or {})
            attempts.append({
                "attempt": attempt,
                "status": "success",
                "retryable": False,
                "wall_clock_seconds": time.monotonic() - started
            })
            meta.update({
                "api_attempts": attempts,
                "attempt_count": attempt
            })
            return {
                "raw_text": raw,
                "metadata": meta,
                "api_attempts": attempts
            }
        except BaseException as exc:
            last_exc = exc
            attempts.append({
                "attempt": attempt,
                "status": "error",
                "retryable": True,
                "exception_type": type(exc).__name__,
                "exception_message": str(exc),
                "wall_clock_seconds": time.monotonic() - started,
                "timestamp_utc": datetime.now(timezone.utc).isoformat()
            })
            if attempt == 3:
                break
            # Backoff wait
            wait_time = 5 if attempt == 1 else 20
            print(f"Attempt {attempt} failed: {exc}. Retrying in {wait_time}s...")
            time.sleep(wait_time)

    raise RuntimeError(f"API calls exhausted for cell {cell_id} after 3 attempts: {last_exc}")

def execute_generations(manifest: dict[str, any], cell_plan: list[dict[str, any]]) -> None:
    output_root = ROOT / manifest["output_root"]

    # Overwrite & Incompatible directory validation
    if output_root.exists():
        manifest_file = output_root / "manifest.json"
        if manifest_file.exists():
            try:
                existing_manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
                if existing_manifest.get("experiment_id") != manifest["experiment_id"]:
                    raise RuntimeError(f"Output directory exists with incompatible experiment_id: {existing_manifest.get('experiment_id')}")
            except Exception as e:
                raise RuntimeError(f"Incompatible directory detected at {output_root}: {e}")
    else:
        output_root.mkdir(parents=True, exist_ok=True)

    # Write current manifest to output directory
    manifest_out = output_root / "manifest.json"
    _atomic_write_text(manifest_out, json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")

    # Import Google Gemini transport dynamically
    from scripts.ce115_v4_gemini_transport import call_gemini_once, api_key_status

    # Validate API key presence
    status = api_key_status()
    if not status.get("api_key_present"):
        raise RuntimeError("GEMINI_API_KEY environment variable is missing or empty")

    from agent_tools.finals_rebuild.math16_pool import tasks_by_id, frozen_for_prompt
    from agent_tools.finals_rebuild.ce115_clean_incremental_ablation import build_condition_prompt

    tasks = tasks_by_id()

    for idx, cell in enumerate(cell_plan):
        cell_id = cell["cell_id"]
        cell_dir = output_root / cell["output_relative_path"]

        # 1. Resume validation
        artifact_path = cell_dir / "artifact.json"
        raw_response_path = cell_dir / "raw_response.txt"

        if artifact_path.exists() and raw_response_path.exists():
            try:
                art = json.loads(artifact_path.read_text(encoding="utf-8"))
                if (
                    art.get("persisted_complete") is True and
                    art.get("cell_id") == cell_id and
                    art.get("prompt_sha256") == cell["prompt_sha256"] and
                    art.get("model_tag") == cell["model_tag"]
                ):
                    print(f"[{idx+1}/80] Resuming completed cell: {cell_id}")
                    continue
                else:
                    print(f"[{idx+1}/80] Cell directory exists but is incomplete or mismatch. Will overwrite/re-run: {cell_id}")
            except Exception:
                print(f"[{idx+1}/80] Cell files exist but are corrupted. Will re-run: {cell_id}")

        # 2. Get prompt
        cond = cell["condition"]
        tid = cell["task_id"]
        if cond == "ab2d_spec":
            spec_prompt_path = ROOT / "docs/experiments/prompts/ab2d_spec/prompts" / f"{tid}.txt"
            prompt = spec_prompt_path.read_text(encoding="utf-8")
        else:
            task = tasks[tid]
            frozen = frozen_for_prompt(task)
            prompt = build_condition_prompt(cond, task, frozen)

        print(f"[{idx+1}/80] Calling API for cell: {cell_id} (seed {cell['seed']})")

        # Define the dynamic call function for retry wrapper
        def execute_fn(p: str):
            return call_gemini_once(p, model=cell["model_tag"])

        started_at = datetime.now(timezone.utc).isoformat()
        started_wall = time.monotonic()

        # 3. Call model with retry logic
        cell_result = run_cell_with_retries(prompt, cell_id, execute_fn)

        duration = time.monotonic() - started_wall
        completed_at = datetime.now(timezone.utc).isoformat()

        # 4. Save results using atomic write
        cell_data = {
            "cell_id": cell_id,
            "task_id": tid,
            "condition": cond,
            "seed": cell["seed"],
            "model_tag": cell["model_tag"],
            "runtime_parameters": cell["runtime_parameters"],
            "prompt_sha256": cell["prompt_sha256"],
            "request_metadata": {
                "temperature": cell["runtime_parameters"]["temperature"],
                "max_output_tokens": cell["runtime_parameters"]["max_output_tokens"]
            },
            "raw_response": cell_result["raw_text"],
            "attempt_count": cell_result["metadata"]["attempt_count"],
            "started_at_utc": started_at,
            "completed_at_utc": completed_at,
            "duration": duration,
            "persisted_complete": True,
            "provenance": {
                "api_attempts": cell_result["api_attempts"],
                "provider_metadata": cell_result["metadata"].get("usage_metadata") or {}
            }
        }

        cell_dir.mkdir(parents=True, exist_ok=True)
        _atomic_write_text(cell_dir / "prompt.txt", prompt)
        _atomic_write_text(cell_dir / "raw_response.txt", cell_result["raw_text"])
        _atomic_write_text(cell_dir / "artifact.json", json.dumps(cell_data, ensure_ascii=False, indent=2) + "\n")
        print(f"Cell completed and saved: {cell_id}")

def main() -> int:
    parser = argparse.ArgumentParser(description="Pilot-02 Integer generation runner")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--preflight-only", action="store_true", help="Run checks only, no model calls")
    group.add_argument("--execute", action="store_true", help="Perform model execution")

    args = parser.parse_args()

    try:
        checks = do_preflight()
        if args.preflight_only:
            print("Zero-model preflight checks completed successfully. No execution requested.")
            return 0

        # Execute generations
        execute_generations(checks["manifest"], checks["cell_plan"])
        print("PILOT_02_INTEGER_GENERATION_COMPLETE")
        return 0
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Runner failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
