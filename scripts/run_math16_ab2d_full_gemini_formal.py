"""Math16 Ab2d+full Gemini formal 80-cell runner entrypoint.

Uses shared QFIX-001 null-safe artifact assembly
(``agent_tools.finals_rebuild.math16_ab2d_full_artifact_assembly``).

Does not modify Prompt / API / scaffold / evaluator / task identity.
Live model calls require ``--execute-api`` (not used in QFIX-001 freeze).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.math16_ab2d_full_artifact_assembly import (
    QFIX_001_ID,
    atomic_write_json,
    atomic_write_text,
    build_evaluation_result,
    write_artifact_manifest,
    write_evaluation_artifacts,
)
from agent_tools.finals_rebuild.math16_pool import load_pool_manifest, tasks_by_id
from scripts.ce115_v4_gemini_transport import (
    MAX_OUTPUT_TOKENS,
    MODEL_ID,
    REQUEST_TIMEOUT_SECONDS,
    TEMPERATURE,
    api_key_status,
    build_redacted_request,
    call_gemini_once,
)
from scripts.run_math16_latex_v1_gemini_live import classify_math16_response

DESIGN_FREEZE_COMMIT = "e4bc9ec7e36ecd6cc46b84d75aa6b485beb557de"
EXPERIMENT_ID = "math16_ab2d_full_domain_assisted_v1"
CONDITION = "ab2d_full"
MODEL_KEY = "gemini"
EXPECTED_SCAFFOLD = "7ea108503d09b8f0130827e928ea38dbddf5a56833c2fde7741a35f85a6b1f1f"
EXPECTED_TASK_FREEZE = "349dfb2f786a4aa029453d844cac7eca07deb24a777ba1be4ef70f7002882e14"
EXPECTED_POOL_IDENTITY = "2ff41465d818d7e3d9b990a27ad2a1535e72c271bb04b2a37abe29cec1824636"

ARTIFACT_ROOT = ROOT / "artifacts" / EXPERIMENT_ID
FORMAL_ROOT = ARTIFACT_ROOT / "formal" / MODEL_KEY
QUAL_CELLS_ROOT = ARTIFACT_ROOT / "qualification" / "cells"
PREREG = ARTIFACT_ROOT / "preregistration"
PROMPT_DIR = ROOT / "docs/experiments/prompts/ab2d_full/prompts"
SCAFFOLD_PATH = ROOT / "docs/experiments/prompts/ab2d_full/derived_scaffolds_v1.json"

RETRY_POLICY = {
    "max_attempts": 3,
    "retry_delays_seconds": [5, 20],
}


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_gemini_manifest_cells() -> list[dict[str, Any]]:
    path = PREREG / "cell_manifest.jsonl"
    cells = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if row.get("model_key") == MODEL_KEY:
            cells.append(row)
    if len(cells) != 80:
        raise RuntimeError(f"expected 80 gemini cells, got {len(cells)}")
    return cells


def verify_design_hashes() -> dict[str, Any]:
    pool = load_pool_manifest(ROOT)
    prompt_freeze = json.loads((PREREG / "prompt_freeze.json").read_text(encoding="utf-8"))
    scaffold = sha256_file(SCAFFOLD_PATH)
    ok = (
        scaffold == EXPECTED_SCAFFOLD
        and pool["task_freeze_hash"] == EXPECTED_TASK_FREEZE
        and pool["pool_identity_hash"] == EXPECTED_POOL_IDENTITY
        and prompt_freeze.get("all_match_builder") is True
    )
    return {
        "ok": ok,
        "design_freeze_commit": DESIGN_FREEZE_COMMIT,
        "scaffold_sha256": scaffold,
        "task_freeze_hash": pool["task_freeze_hash"],
        "pool_identity_hash": pool["pool_identity_hash"],
        "artifact_assembly_module": "agent_tools.finals_rebuild.math16_ab2d_full_artifact_assembly",
        "qfix": QFIX_001_ID,
        "model_settings": {
            "model_identifier": MODEL_ID,
            "temperature": TEMPERATURE,
            "max_output_tokens": MAX_OUTPUT_TOKENS,
            "timeout_seconds": REQUEST_TIMEOUT_SECONDS,
            "top_p": "UNRESOLVED_NOT_IN_TRANSPORT",
        },
    }


def assemble_from_raw(
    *,
    cell_dir: Path,
    task: dict[str, Any],
    cell_meta: dict[str, Any],
    raw: str,
    preserve_extracted: bool = True,
) -> dict[str, Any]:
    """Classify raw and write evaluation/artifact using QFIX-001 assembly."""
    outcome, source, details = classify_math16_response(
        raw,
        frozen_params=task["frozen_params"],
        audit_oracle_payload=task["oracle_payload"],
        task=task,
    )
    extracted_path = cell_dir / "extracted_source.py"
    if source and not (preserve_extracted and extracted_path.exists()):
        atomic_write_text(extracted_path, source)
    elif source and preserve_extracted and not extracted_path.exists():
        atomic_write_text(extracted_path, source)

    evaluation = build_evaluation_result(
        outcome=outcome,
        source=source if source is not None else (
            extracted_path.read_text(encoding="utf-8") if extracted_path.exists() else None
        ),
        details=details,
        frozen_params=task["frozen_params"],
    )
    write_evaluation_artifacts(cell_dir, evaluation=evaluation, outcome=outcome)

    artifact = {
        "experiment_id": EXPERIMENT_ID,
        "cell_id": cell_meta["cell_id"],
        "qualification_only": cell_meta.get("qualification_only", False),
        "primary_evidence": cell_meta.get("primary_evidence", True),
        "model": MODEL_ID,
        "model_key": MODEL_KEY,
        "task_id": cell_meta["task_id"],
        "condition": CONDITION,
        "seed": cell_meta["seed"],
        "prompt_sha256": cell_meta["prompt_sha256"],
        "scaffold_sha256": EXPECTED_SCAFFOLD,
        "freeze_commit": DESIGN_FREEZE_COMMIT,
        "outcome": outcome,
        "persisted_complete": True,
        "completed_at_utc": datetime.now(timezone.utc).isoformat(),
        "artifact_assembly": QFIX_001_ID,
    }
    return write_artifact_manifest(cell_dir, artifact)


def replay_qualification_assembly() -> dict[str, Any]:
    """Re-assemble qualification cells from preserved raw; never call the model."""
    tasks = tasks_by_id(ROOT)
    rows = []
    for cell_dir in sorted(QUAL_CELLS_ROOT.glob("gemini__*")):
        raw_path = cell_dir / "raw_response.txt"
        if not raw_path.exists():
            continue
        before = {
            "raw": sha256_file(raw_path),
            "extracted": sha256_file(cell_dir / "extracted_source.py")
            if (cell_dir / "extracted_source.py").exists()
            else None,
            "evaluation": sha256_file(cell_dir / "evaluation_result.json")
            if (cell_dir / "evaluation_result.json").exists()
            else None,
        }
        # Parse identity from directory name: gemini__{task}__ab2d_full__seed_{seed}
        name = cell_dir.name
        parts = name.split("__")
        task_id = parts[1]
        seed = int(parts[-1].replace("seed_", ""))
        task = tasks[task_id]
        prompt = (cell_dir / "prompt.txt").read_text(encoding="utf-8")
        meta = {
            "cell_id": name,
            "task_id": task_id,
            "seed": seed,
            "prompt_sha256": sha256_text(prompt),
            "qualification_only": True,
            "primary_evidence": False,
        }
        # Ensure request_metadata / logs exist for required list
        if not (cell_dir / "request_metadata.json").exists():
            atomic_write_json(
                cell_dir / "request_metadata.json",
                build_redacted_request(prompt, model=MODEL_ID)
                | {"qualification_only": True, "primary_evidence": False},
            )
        if not (cell_dir / "logs.json").exists():
            atomic_write_json(
                cell_dir / "logs.json",
                {"api_attempts": [{"attempt": 1, "ok": True, "reused_raw": True}], "transport_error": None},
            )
        art = assemble_from_raw(
            cell_dir=cell_dir,
            task=task,
            cell_meta=meta,
            raw=raw_path.read_text(encoding="utf-8"),
            preserve_extracted=True,
        )
        after = {
            "raw": sha256_file(raw_path),
            "extracted": sha256_file(cell_dir / "extracted_source.py")
            if (cell_dir / "extracted_source.py").exists()
            else None,
            "evaluation": sha256_file(cell_dir / "evaluation_result.json"),
        }
        rows.append(
            {
                "cell_id": name,
                "outcome": art["outcome"],
                "artifact_complete": (cell_dir / "artifact.json").exists(),
                "raw_hash_unchanged": before["raw"] == after["raw"],
                "extracted_hash_unchanged": before["extracted"] == after["extracted"],
                "evaluation_hash_unchanged": before["evaluation"] == after["evaluation"]
                if before["evaluation"]
                else True,
                "before": before,
                "after": after,
            }
        )
    return {
        "mode": "replay_qualification_assembly",
        "model_calls": 0,
        "replayed": len(rows),
        "rows": rows,
        "all_raw_unchanged": all(r["raw_hash_unchanged"] for r in rows),
        "all_extracted_unchanged": all(r["extracted_hash_unchanged"] for r in rows),
        "all_artifacts_complete": all(r["artifact_complete"] for r in rows),
    }


def call_with_retries(prompt: str, cell_id: str) -> dict[str, Any]:
    delays = RETRY_POLICY["retry_delays_seconds"]
    max_attempts = RETRY_POLICY["max_attempts"]
    attempts = []
    last_err: Exception | None = None
    for attempt in range(1, max_attempts + 1):
        try:
            resp = call_gemini_once(prompt, model=MODEL_ID)
            raw = resp.get("raw_text")
            if not isinstance(raw, str) or not raw.strip():
                raise RuntimeError("empty_response")
            meta = dict(resp.get("metadata") or {})
            meta["attempt_count"] = attempt
            attempts.append({"attempt": attempt, "ok": True})
            return {"raw_text": raw, "metadata": meta, "api_attempts": attempts, "transport_error": None}
        except Exception as exc:  # noqa: BLE001
            last_err = exc
            attempts.append({"attempt": attempt, "ok": False, "error": f"{type(exc).__name__}: {exc}"})
            if attempt < max_attempts:
                time.sleep(delays[min(attempt - 1, len(delays) - 1)])
    return {
        "raw_text": "",
        "metadata": {"attempt_count": max_attempts},
        "api_attempts": attempts,
        "transport_error": f"{type(last_err).__name__}: {last_err}" if last_err else "unknown",
    }


def execute_formal_cell(cell: dict[str, Any], tasks: dict[str, Any]) -> dict[str, Any]:
    """Live formal cell (requires --execute-api). Writes under formal/gemini/."""
    task = tasks[cell["task_id"]]
    cell_dir = FORMAL_ROOT / cell["cell_id"]
    if (cell_dir / "artifact.json").exists():
        art = json.loads((cell_dir / "artifact.json").read_text(encoding="utf-8"))
        if art.get("persisted_complete"):
            return {"skipped": True, "cell_id": cell["cell_id"]}

    prompt_path = PROMPT_DIR / f"{cell['task_id']}.txt"
    prompt = prompt_path.read_text(encoding="utf-8")
    if sha256_text(prompt) != cell["prompt_sha256"]:
        raise RuntimeError(f"prompt hash drift: {cell['task_id']}")

    cell_dir.mkdir(parents=True, exist_ok=True)
    atomic_write_text(cell_dir / "prompt.txt", prompt)
    req = build_redacted_request(prompt, model=MODEL_ID)
    req["qualification_only"] = False
    req["primary_evidence"] = True
    req["seed"] = cell["seed"]
    atomic_write_json(cell_dir / "request_metadata.json", req)

    started = datetime.now(timezone.utc).isoformat()
    t0 = time.monotonic()
    call = call_with_retries(prompt, cell["cell_id"])
    duration = time.monotonic() - t0
    atomic_write_text(cell_dir / "raw_response.txt", call["raw_text"] or "")
    atomic_write_json(
        cell_dir / "logs.json",
        {
            "started_at_utc": started,
            "duration_seconds": duration,
            "api_attempts": call["api_attempts"],
            "transport_error": call["transport_error"],
            "provider_metadata": call["metadata"],
        },
    )
    if call["transport_error"]:
        evaluation = build_evaluation_result(
            outcome="transport_failure",
            source=None,
            details={"error": call["transport_error"], "api_attempts": call["api_attempts"]},
            frozen_params=task["frozen_params"],
        )
        write_evaluation_artifacts(cell_dir, evaluation=evaluation, outcome="transport_failure")
        artifact = {
            "experiment_id": EXPERIMENT_ID,
            "cell_id": cell["cell_id"],
            "qualification_only": False,
            "primary_evidence": True,
            "model": MODEL_ID,
            "model_key": MODEL_KEY,
            "task_id": cell["task_id"],
            "condition": CONDITION,
            "seed": cell["seed"],
            "prompt_sha256": cell["prompt_sha256"],
            "scaffold_sha256": EXPECTED_SCAFFOLD,
            "freeze_commit": DESIGN_FREEZE_COMMIT,
            "outcome": "transport_failure",
            "persisted_complete": True,
            "artifact_assembly": QFIX_001_ID,
        }
        return write_artifact_manifest(cell_dir, artifact)

    return assemble_from_raw(
        cell_dir=cell_dir,
        task=task,
        cell_meta={**cell, "qualification_only": False, "primary_evidence": True},
        raw=call["raw_text"],
        preserve_extracted=False,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--replay-qualification-assembly",
        action="store_true",
        help="Re-assemble qualification cells from preserved raw (zero model calls).",
    )
    parser.add_argument(
        "--execute-api",
        action="store_true",
        help="Live formal 80-cell generation (forbidden during QFIX-001 freeze verification).",
    )
    parser.add_argument(
        "--integration-check",
        action="store_true",
        help="Print formal runner integration metadata and exit.",
    )
    args = parser.parse_args(argv)

    hashes = verify_design_hashes()
    if args.integration_check:
        print(
            json.dumps(
                {
                    "formal_runner_path": "scripts/run_math16_ab2d_full_gemini_formal.py",
                    "formal_runner_imports_assembly": True,
                    "assembly_module": hashes["artifact_assembly_module"],
                    "qfix": QFIX_001_ID,
                    "design_hashes_ok": hashes["ok"],
                    "gemini_cells": 80,
                    "formal_output_root": str(FORMAL_ROOT).replace("\\", "/"),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0 if hashes["ok"] else 2

    if not hashes["ok"]:
        raise RuntimeError(f"design hash verification failed: {hashes}")

    if args.replay_qualification_assembly:
        result = replay_qualification_assembly()
        out = ARTIFACT_ROOT / "qualification" / "qfix001_replay_summary.json"
        atomic_write_json(out, result)
        print(json.dumps({k: result[k] for k in result if k != "rows"}, ensure_ascii=False, indent=2))
        return 0 if result["all_raw_unchanged"] and result["all_artifacts_complete"] else 1

    if args.execute_api:
        if not api_key_status().get("api_key_present"):
            raise RuntimeError("GEMINI_API_KEY missing")
        tasks = tasks_by_id(ROOT)
        FORMAL_ROOT.mkdir(parents=True, exist_ok=True)
        summary = []
        for cell in load_gemini_manifest_cells():
            summary.append(execute_formal_cell(cell, tasks))
        atomic_write_json(FORMAL_ROOT / "run_summary.json", {"cells": summary, "n": len(summary)})
        print(json.dumps({"executed": len(summary)}, indent=2))
        return 0

    parser.error("Specify --integration-check, --replay-qualification-assembly, or --execute-api")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
