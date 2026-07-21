# -*- coding: utf-8 -*-
"""Math16 Pilot-02 Full generation runner with preflight validation."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

MANIFEST_PATH = ROOT / "docs/experiments/manifests/math16_pilot02_full_runtime_manifest.json"
CELL_PLAN_PATH = ROOT / "docs/experiments/manifests/math16_pilot02_full_generation_plan.json"
INVENTORY_PATH = ROOT / "docs/experiments/manifests/math16_pilot02_full_analysis_inventory.json"
INTEGER_MANIFEST_PATH = ROOT / "docs/experiments/manifests/math16_pilot02_integer_runtime_manifest.json"

EXPECTED_FINGERPRINT = "8bcb0d7177bc35216410108bda88b014848181a95b12bc09bf171866749f3057"

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

    print("--- Zero-Model Preflight Report ---")
    print(f"Runtime Fingerprint:  {calculated_fingerprint}")
    print(f"Reused Integer Cells: 80")
    print(f"New Generation Cells: 240")
    print(f"Combined Inventory:   320")
    print("Zero-Model Preflight PASS.")
    return {"manifest": manifest, "cell_plan": cell_plan, "inventory": inventory}

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

        # Execute is strictly disallowed in this turn
        print("ERROR: Execution of the generation pipeline is not permitted in this turn.")
        raise RuntimeError("EXECUTE_DISALLOWED: This runner is currently restricted to preflight-only. Generation execution is disabled.")
    except Exception as e:
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
