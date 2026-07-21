# -*- coding: utf-8 -*-
"""Math16 Pilot-02 Integer Evaluation Revision v3_r001 script."""
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

EVAL_MANIFEST_PATH = ROOT / "docs/experiments/manifests/math16_pilot02_integer_evaluation_v3_r001_manifest.json"
TAXONOMY_JSON_PATH = ROOT / "docs/experiments/taxonomy/ai_generated_program_failure_taxonomy_v3.json"
TAXONOMY_MD_PATH = ROOT / "docs/決賽文件/20260720_AI 生成程式共同失敗分類標準_實際使用版 v3.md"

def _hash_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def do_preflight_checks() -> None:
    print("Executing zero-result evaluation preflight...")

    # 1. Verify taxonomy Markdown file
    if not TAXONOMY_MD_PATH.exists():
        raise FileNotFoundError(f"Taxonomy Markdown not found at: {TAXONOMY_MD_PATH}")
    md_sha = _hash_file(TAXONOMY_MD_PATH)
    expected_md_sha = "7df8f4472ce048569967436cbc73ede8fd4bd117ad67d0028ddd95af2055a304"
    if md_sha != expected_md_sha:
        raise ValueError(f"Taxonomy Markdown SHA mismatch. Expected {expected_md_sha}, got {md_sha}")
    print(f"Taxonomy Markdown verified. SHA-256: {md_sha}")

    # 2. Verify taxonomy JSON file
    if not TAXONOMY_JSON_PATH.exists():
        raise FileNotFoundError(f"Taxonomy JSON not found at: {TAXONOMY_JSON_PATH}")
    tax = json.loads(TAXONOMY_JSON_PATH.read_text(encoding="utf-8"))
    if tax.get("source_file_sha256") != md_sha:
        raise ValueError("Taxonomy JSON source SHA does not match MD file SHA")

    # 3. Verify Evaluation Manifest
    if not EVAL_MANIFEST_PATH.exists():
        raise FileNotFoundError(f"Evaluation Manifest not found at: {EVAL_MANIFEST_PATH}")
    manifest = json.loads(EVAL_MANIFEST_PATH.read_text(encoding="utf-8"))

    if manifest.get("evaluation_revision") != "v3_r001":
        raise ValueError("Manifest evaluation_revision mismatch")
    if manifest.get("taxonomy_file_sha256") != md_sha:
        raise ValueError("Manifest taxonomy SHA mismatch")

    # 4. Verify Cell Plan & Expected Cells
    cell_plan_path = ROOT / manifest["inventory_reference"]
    if not cell_plan_path.exists():
        raise FileNotFoundError(f"Cell plan not found at: {cell_plan_path}")
    plan_sha = _hash_file(cell_plan_path)
    if plan_sha != manifest["inventory_file_sha256"]:
        raise ValueError("Cell plan file SHA mismatch")

    cell_plan = json.loads(cell_plan_path.read_text(encoding="utf-8"))
    expected_cells = manifest["expected_cell_count"]
    if len(cell_plan) != expected_cells:
        raise ValueError(f"Cell plan size mismatch: expected {expected_cells}, got {len(cell_plan)}")

    # 5. Verify Raw Output Inventory
    raw_root = ROOT / manifest["raw_result_root"]
    if not raw_root.exists():
        raise FileNotFoundError(f"Raw results directory not found at: {raw_root}")

    raw_manifest_file = raw_root / "manifest.json"
    if not raw_manifest_file.exists():
        raise FileNotFoundError("Raw results manifest not found")
    raw_manifest = json.loads(raw_manifest_file.read_text(encoding="utf-8"))
    if raw_manifest.get("experiment_id") != manifest["run_id"]:
        raise ValueError("Raw run_id mismatch")

    # Calculate fingerprint of raw manifest dynamically
    keys = [
        "experiment_id", "model_provider", "model_tag", "model_version",
        "runtime", "runtime_version", "thinking_mode", "temperature",
        "top_p", "top_k", "max_output_tokens", "timeout_seconds",
        "retry_policy", "seed_list", "source_commit"
    ]
    sub = {k: raw_manifest[k] for k in keys}
    serialized = json.dumps(sub, sort_keys=True, ensure_ascii=False)
    raw_fingerprint = hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    # Verify each cell directory and files presence
    for cell in cell_plan:
        cell_id = cell["cell_id"]
        cell_dir = raw_root / cell["output_relative_path"]
        artifact_path = cell_dir / "artifact.json"
        raw_response_path = cell_dir / "raw_response.txt"
        prompt_path = cell_dir / "prompt.txt"

        if not artifact_path.exists():
            raise FileNotFoundError(f"Missing artifact.json for cell: {cell_id}")
        if not raw_response_path.exists():
            raise FileNotFoundError(f"Missing raw_response.txt for cell: {cell_id}")
        if not prompt_path.exists():
            raise FileNotFoundError(f"Missing prompt.txt for cell: {cell_id}")

        art = json.loads(artifact_path.read_text(encoding="utf-8"))
        if art.get("persisted_complete") is not True:
            raise ValueError(f"Cell {cell_id} is incomplete")
        if art.get("prompt_sha256") != cell["prompt_sha256"]:
            raise ValueError(f"Prompt SHA mismatch for cell: {cell_id}")
        if art.get("runtime_config_fingerprint") != raw_fingerprint:
            raise ValueError(f"Runtime fingerprint mismatch for cell: {cell_id}")


    # 6. Verify Output Evaluation Root
    eval_out_root = ROOT / "docs/experiments/results" / manifest["evaluation_id"]
    if eval_out_root.exists():
        eval_manifest_out = eval_out_root / "manifest.json"
        if eval_manifest_out.exists():
            try:
                existing_eval = json.loads(eval_manifest_out.read_text(encoding="utf-8"))
                if existing_eval.get("evaluation_revision") != manifest["evaluation_revision"]:
                    raise RuntimeError("Incompatible evaluation revision directory exists")
            except Exception as e:
                raise RuntimeError(f"Corrupted evaluation directory at {eval_out_root}: {e}")

    print("--- Zero-Result Preflight Report ---")
    print(f"Taxonomy MD SHA:       {md_sha}")
    print(f"Evaluation Revision:   {manifest['evaluation_revision']}")
    print(f"Expected Cell Count:   {expected_cells}")
    print(f"All {expected_cells} cells are verified to be unmodified and complete.")
    print("Zero-Result Preflight PASS.")

def main() -> int:
    parser = argparse.ArgumentParser(description="Math16 Pilot-02 evaluation v3 script")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--preflight-only", action="store_true", help="Run preflight validation checks")
    group.add_argument("--execute", action="store_true", help="Perform evaluation execution")

    args = parser.parse_args()

    try:
        if args.preflight_only:
            do_preflight_checks()
            return 0

        # Execute evaluation is strictly disallowed in this run
        print("ERROR: Execution of the evaluation pipeline is not permitted in this turn.")
        raise RuntimeError("EXECUTE_DISALLOWED: This evaluation revision run is currently restricted to preflight-only. Evaluator execution is disabled.")
    except Exception as e:
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
