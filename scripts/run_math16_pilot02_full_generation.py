# -*- coding: utf-8 -*-
"""Math16 Pilot-02 Full generation runner with preflight validation."""
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

MANIFEST_PATH = ROOT / "docs/experiments/manifests/math16_pilot02_full_runtime_manifest.json"
CELL_PLAN_PATH = ROOT / "docs/experiments/manifests/math16_pilot02_full_generation_plan.json"
INVENTORY_PATH = ROOT / "docs/experiments/manifests/math16_pilot02_full_analysis_inventory.json"
INTEGER_MANIFEST_PATH = ROOT / "docs/experiments/manifests/math16_pilot02_integer_runtime_manifest.json"

EXPECTED_FINGERPRINT = "8bcb0d7177bc35216410108bda88b014848181a95b12bc09bf171866749f3057"

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

def get_file_sha256(path: Path) -> str:
    content = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    return hashlib.sha256(content.encode("utf-8")).hexdigest()

def do_preflight() -> dict[str, any]:
    print("Executing zero-model preflight checks for full Math16 run...")

    # 1. Verify files exist
    if not MANIFEST_PATH.exists():
        raise FileNotFoundError(f"Manifest not found at {MANIFEST_PATH}")
    if not CELL_PLAN_PATH.exists():
        raise FileNotFoundError(f"Cell plan not found at {CELL_PLAN_PATH}")
    if not INVENTORY_PATH.exists():
        raise FileNotFoundError(f"Inventory not found at {INVENTORY_PATH}")

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    cell_plan = json.loads(CELL_PLAN_PATH.read_text(encoding="utf-8"))
    inventory = json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))

    # 2. Check fingerprint
    keys = [
        "experiment_id", "model_provider", "model_tag", "model_version",
        "runtime", "runtime_version", "thinking_mode", "temperature",
        "top_p", "top_k", "max_output_tokens", "timeout_seconds",
        "retry_policy", "seed_list", "source_commit"
    ]
    sub = {k: manifest[k] for k in keys}
    serialized = json.dumps(sub, sort_keys=True, ensure_ascii=False)
    calculated_fingerprint = hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    if calculated_fingerprint != EXPECTED_FINGERPRINT:
        raise ValueError(f"Runtime fingerprint mismatch: expected {EXPECTED_FINGERPRINT}, got {calculated_fingerprint}")
    print(f"Runtime fingerprint verified: {calculated_fingerprint}")

    # 3. Check Cell Counts
    expected_generation_cells = 240
    expected_inventory_cells = 320
    if len(cell_plan) != expected_generation_cells:
        raise ValueError(f"Generation plan size mismatch: expected {expected_generation_cells}, got {len(cell_plan)}")
    if len(inventory) != expected_inventory_cells:
        raise ValueError(f"Analysis inventory size mismatch: expected {expected_inventory_cells}, got {len(inventory)}")

    # 4. Check uniqueness
    cell_ids = set()
    output_paths = set()
    for cell in cell_plan:
        cell_id = cell["cell_id"]
        if cell_id in cell_ids:
            raise ValueError(f"Duplicate cell_id in generation plan: {cell_id}")
        cell_ids.add(cell_id)

        out_path = cell["output_relative_path"]
        if out_path in output_paths:
            raise ValueError(f"Duplicate output path in generation plan: {out_path}")
        output_paths.add(out_path)

    # 5. Check reused cells presence
    reused_count = sum(1 for c in inventory if c.get("reused") is True)
    new_count = sum(1 for c in inventory if c.get("reused") is False)
    if reused_count != 80:
        raise ValueError(f"Expected 80 reused cells in inventory, got {reused_count}")
    if new_count != 240:
        raise ValueError(f"Expected 240 new cells in inventory, got {new_count}")

    # Verify that the 80 reused cells exist on disk
    for cell in inventory:
        if cell.get("reused") is True:
            cell_dir = ROOT / "docs/experiments/results" / cell["output_relative_path"]
            artifact_file = cell_dir / "artifact.json"
            if not artifact_file.exists():
                raise FileNotFoundError(f"Reused cell artifact not found: {artifact_file}")
            art = json.loads(artifact_file.read_text(encoding="utf-8"))
            if art.get("prompt_sha256") != cell["prompt_sha256"]:
                raise ValueError(f"Reused cell prompt SHA-256 mismatch for {cell['cell_id']}")

    # 6. Verify ab2d_spec prompts on disk for the 12 non-integer tasks
    manifest_spec_path = ROOT / "docs/experiments/prompts/ab2d_spec/manifest.json"
    if not manifest_spec_path.exists():
        raise FileNotFoundError(f"ab2d_spec manifest not found at {manifest_spec_path}")
    manifest_spec = json.loads(manifest_spec_path.read_text(encoding="utf-8"))

    spec_hashes = {t["task_id"]: t["exact_prompt_sha256"] for t in manifest_spec["tasks"]}

    for cell in cell_plan:
        if cell["condition"] == "ab2d_spec":
            tid = cell["task_id"]
            expected_hash = spec_hashes[tid]
            prompt_file = ROOT / f"docs/experiments/prompts/ab2d_spec/prompts/{tid}.txt"
            if not prompt_file.exists():
                raise FileNotFoundError(f"Frozen prompt file missing: {prompt_file}")
            actual_hash = get_file_sha256(prompt_file)
            if actual_hash != expected_hash:
                raise ValueError(f"SHA-256 mismatch for frozen prompt {tid}.txt: expected {expected_hash}, got {actual_hash}")

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
            built_prompt = build_condition_prompt(cond, task, frozen).replace("\r\n", "\n")
            built_hash = prompt_sha256(built_prompt)
            if built_hash != cell["prompt_sha256"]:
                raise ValueError(f"Built prompt hash mismatch for {cell['cell_id']}: expected {cell['prompt_sha256']}, got {built_hash}")

    print("--- Zero-Model Preflight Report ---")
    print(f"Runtime Fingerprint:  {calculated_fingerprint}")
    print(f"Reused Integer Cells: 80")
    print(f"New Generation Cells: 240")
    print(f"Combined Inventory:   320")
    print("Zero-Model Preflight PASS.")
    return {"manifest": manifest, "cell_plan": cell_plan, "inventory": inventory}

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

def quarantine_cell(cell_id: str, cell_dir: Path, output_root: Path) -> None:
    if not cell_dir.exists():
        return
    if not any(cell_dir.iterdir()):
        return
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    quarantine_dir = output_root / "_quarantine" / cell_id / timestamp
    quarantine_dir.parent.mkdir(parents=True, exist_ok=True)
    try:
        cell_dir.rename(quarantine_dir)
        print(f"Quarantined incomplete cell directory for {cell_id} to: {quarantine_dir}")
    except Exception as e:
        # Fallback to file-by-file move
        try:
            quarantine_dir.mkdir(parents=True, exist_ok=True)
            for item in list(cell_dir.iterdir()):
                item.rename(quarantine_dir / item.name)
            if cell_dir.exists():
                cell_dir.rmdir()
            print(f"Quarantined incomplete cell files for {cell_id} to: {quarantine_dir}")
        except Exception as e2:
            raise RuntimeError(f"QUARANTINE_FAILED: Could not quarantine {cell_dir}: {e} / {e2}")

def execute_generations(manifest: dict[str, any], cell_plan: list[dict[str, any]]) -> None:
    output_root = ROOT / "docs/experiments/results/math16_pilot02_full_gemini"
    expected_fingerprint = EXPECTED_FINGERPRINT

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

        # Expected parameters for mismatch check
        expected_experiment_id = manifest["experiment_id"]
        expected_task_id = cell["task_id"]
        expected_condition = cell["condition"]
        expected_seed = cell["seed"]
        expected_prompt_sha256 = cell["prompt_sha256"]
        expected_model_tag = cell["model_tag"]

        status = "run"
        if cell_dir.exists() and any(cell_dir.iterdir()):
            artifact_path = cell_dir / "artifact.json"
            raw_response_path = cell_dir / "raw_response.txt"

            if artifact_path.exists():
                try:
                    art = json.loads(artifact_path.read_text(encoding="utf-8"))
                except Exception:
                    # corrupted json is incomplete
                    status = "incomplete"
                    art = None

                if art is not None:
                    # Verify mismatch
                    mismatch = False
                    for key, expected_val in [
                        ("experiment_id", expected_experiment_id),
                        ("cell_id", cell_id),
                        ("task_id", expected_task_id),
                        ("condition", expected_condition),
                        ("seed", expected_seed),
                        ("prompt_sha256", expected_prompt_sha256),
                        ("model_tag", expected_model_tag),
                        ("runtime_config_fingerprint", expected_fingerprint)
                    ]:
                        if key not in art or art[key] != expected_val:
                            mismatch = True
                            print(f"Mismatch detected for key '{key}': expected {expected_val}, got {art.get(key)}")
                            break

                    if mismatch:
                        raise RuntimeError(f"INCOMPATIBLE_EXISTING_CELL: cell {cell_id} has mismatched metadata")

                    if art.get("persisted_complete") is True and raw_response_path.exists():
                        status = "skip"
                    else:
                        status = "incomplete"
            else:
                # No artifact.json but directory is not empty
                status = "incomplete"

        if status == "skip":
            print(f"[{idx+1}/240] Resuming completed cell: {cell_id}")
            continue

        if status == "incomplete":
            print(f"[{idx+1}/240] Incomplete compatible cell detected: {cell_id}. Quarantining...")
            quarantine_cell(cell_id, cell_dir, output_root)

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

        print(f"[{idx+1}/240] Calling API for cell: {cell_id} (seed {cell['seed']})")

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
            "experiment_id": expected_experiment_id,
            "cell_id": cell_id,
            "task_id": tid,
            "condition": cond,
            "seed": cell["seed"],
            "model_tag": cell["model_tag"],
            "runtime_config_fingerprint": expected_fingerprint,
            "runtime_parameters": {
                "temperature": manifest["temperature"],
                "max_output_tokens": manifest["max_output_tokens"]
            },
            "prompt_sha256": cell["prompt_sha256"],
            "request_metadata": {
                "temperature": manifest["temperature"],
                "max_output_tokens": manifest["max_output_tokens"]
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
    parser = argparse.ArgumentParser(description="Math16 Pilot-02 full runner")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--preflight-only", action="store_true", help="Run preflight validation checks")
    group.add_argument("--execute", action="store_true", help="Perform execution")

    args = parser.parse_args()

    try:
        data = do_preflight()
        if args.preflight_only:
            return 0

        # Execute generations
        execute_generations(data["manifest"], data["cell_plan"])
        print("MATH16_NEW_240_GENERATION_COMPLETE")
        return 0
    except Exception as e:
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
