# -*- coding: utf-8 -*-
"""Math16 Pilot-02 Qwen 3.5 9B formal 320-cell generation runner.

Consumes frozen runtime manifest + cell plan only. Does not score, heal,
or call any non-qwen3.5:9b model.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

MANIFEST_PATH = ROOT / "docs/experiments/manifests/math16_pilot02_qwen9b_runtime_manifest.json"
PLAN_PATH = ROOT / "docs/experiments/manifests/math16_pilot02_qwen9b_cell_plan.json"
OUTPUT_ROOT = ROOT / "docs/experiments/results/math16_pilot02_qwen9b"
EXPECTED_FINGERPRINT = "f45f79238bbf9400729fd00dbfaf4e33a7a7716cb9f81d4095a1fd1d52e0da5b"
EXPECTED_DIGEST = "6488c96fa5faab64bb65cbd30d4289e20e6130ef535a93ef9a49f42eda893ea7"
EXPECTED_HEAD = "f782a55cea95af96803e0146a29985d30916468b"
MODEL_TAG = "qwen3.5:9b"
CONSECUTIVE_FAILURE_STOP = 5

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


def _sha_text(text: str) -> str:
    return hashlib.sha256(text.replace("\r\n", "\n").encode("utf-8")).hexdigest()


def _sha_file_lf(path: Path) -> str:
    return _sha_text(path.read_text(encoding="utf-8"))


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


def _append_journal(row: dict[str, Any]) -> None:
    journal = OUTPUT_ROOT / "cell_journal.jsonl"
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    with journal.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(row, ensure_ascii=False) + "\n")
        handle.flush()
        os.fsync(handle.fileno())


def _http_json(url: str, payload: dict | None = None) -> dict:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"} if data else {},
        method="GET" if data is None else "POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def verify_live_digest() -> str:
    tags = _http_json("http://localhost:11434/api/tags")
    for m in tags.get("models", []):
        if m.get("name") == MODEL_TAG or m.get("model") == MODEL_TAG:
            digest = m["digest"]
            if digest != EXPECTED_DIGEST:
                raise RuntimeError(
                    f"MODEL_DIGEST_MISMATCH: expected {EXPECTED_DIGEST}, got {digest}"
                )
            return digest
    raise RuntimeError(f"{MODEL_TAG} not found in Ollama tags")


def compute_fingerprint(manifest: dict[str, Any]) -> str:
    sub = {k: manifest[k] for k in FINGERPRINT_KEYS}
    return hashlib.sha256(
        json.dumps(sub, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()


def quarantine_cell(cell_id: str, cell_dir: Path) -> None:
    if not cell_dir.exists() or not any(cell_dir.iterdir()):
        return
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    quarantine_dir = OUTPUT_ROOT / "_quarantine" / cell_id / timestamp
    quarantine_dir.parent.mkdir(parents=True, exist_ok=True)
    try:
        cell_dir.rename(quarantine_dir)
    except OSError:
        quarantine_dir.mkdir(parents=True, exist_ok=True)
        for item in list(cell_dir.iterdir()):
            item.rename(quarantine_dir / item.name)
        if cell_dir.exists():
            try:
                cell_dir.rmdir()
            except OSError:
                pass


def resolve_prompt(cell: dict[str, Any], tasks: dict) -> str:
    from agent_tools.finals_rebuild.ce115_clean_incremental_ablation import (
        build_condition_prompt,
    )
    from agent_tools.finals_rebuild.math16_pool import frozen_for_prompt

    cond = cell["condition"]
    tid = cell["task_id"]
    if cond == "ab2d_spec_v2":
        path = ROOT / cell["prompt_path"]
        if "ab2d_spec_v2" not in str(path).replace("\\", "/"):
            raise RuntimeError(f"PROMPT_PATH_NOT_V2: {path}")
        text = path.read_text(encoding="utf-8")
    elif cond in ("ab1", "ab2g", "ab2d"):
        task = tasks[tid]
        frozen = frozen_for_prompt(task)
        text = build_condition_prompt(cond, task, frozen)
    else:
        raise RuntimeError(f"UNKNOWN_CONDITION: {cond}")
    sha = _sha_text(text)
    if sha != cell["prompt_sha256"]:
        raise RuntimeError(
            f"PROMPT_SHA_DRIFT: {cell['cell_id']} expected {cell['prompt_sha256']} got {sha}"
        )
    return text.replace("\r\n", "\n")


def do_preflight() -> dict[str, Any]:
    from scripts.math16_qwen_ollama_adapter import TEMPERATURE, build_math16_chat_payload
    from scripts.preflight_math16_pilot02_qwen9b_runtime import do_preflight as base_preflight

    base = base_preflight()
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))

    if manifest["runtime_config_fingerprint"] != EXPECTED_FINGERPRINT:
        raise RuntimeError("FINGERPRINT_MISMATCH vs frozen constant")
    if compute_fingerprint(manifest) != EXPECTED_FINGERPRINT:
        raise RuntimeError("FINGERPRINT_RECOMPUTE_MISMATCH")
    if manifest["temperature"] != 0.2:
        raise RuntimeError(f"TEMPERATURE_NOT_0_2: {manifest['temperature']}")
    if TEMPERATURE != 0.2:
        raise RuntimeError(f"ADAPTER_TEMPERATURE_NOT_0_2: {TEMPERATURE}")
    if manifest["thinking_mode"] is not False:
        raise RuntimeError("THINKING_MODE_NOT_FALSE")
    if manifest["model_digest"] != EXPECTED_DIGEST:
        raise RuntimeError("MANIFEST_DIGEST_MISMATCH")

    digest = verify_live_digest()
    payload = build_math16_chat_payload("preflight", seed=2026071301, model=MODEL_TAG)
    if payload["think"] is not False:
        raise RuntimeError("payload think not false")
    if payload["options"].get("temperature") != 0.2:
        raise RuntimeError("payload temperature not 0.2")
    if "seed" not in payload["options"]:
        raise RuntimeError("seed not in options")

    if len(plan) != 320 or len({c["cell_id"] for c in plan}) != 320:
        raise RuntimeError("CELL_PLAN_GEOMETRY_INVALID")

    print(
        json.dumps(
            {
                "generation_preflight": "PASS",
                "fingerprint": EXPECTED_FINGERPRINT,
                "model_digest": digest,
                "temperature": 0.2,
                "cells": 320,
                "expected_head": EXPECTED_HEAD,
            },
            indent=2,
        )
    )
    return {"manifest": manifest, "cell_plan": plan, "base": base}


def execute_generations(manifest: dict[str, Any], cell_plan: list[dict[str, Any]]) -> dict[str, Any]:
    from agent_tools.finals_rebuild.math16_pool import tasks_by_id
    from scripts.math16_qwen_ollama_adapter import (
        InvalidInfrastructureError,
        call_qwen_with_retries,
        probe_ollama,
    )

    probe = probe_ollama(model=MODEL_TAG)
    if not probe.get("model_present") or not probe.get("digest_ok"):
        raise RuntimeError(f"OLLAMA_PROBE_FAILED: {probe}")
    live_version = _http_json("http://localhost:11434/api/version").get("version")
    if live_version != manifest["runtime_version"]:
        raise RuntimeError(
            f"OLLAMA_VERSION_MISMATCH: frozen={manifest['runtime_version']} live={live_version}"
        )
    verify_live_digest()

    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    run_manifest = {
        "experiment_id": manifest["experiment_id"],
        "model_tag": MODEL_TAG,
        "model_digest": EXPECTED_DIGEST,
        "runtime_config_fingerprint": EXPECTED_FINGERPRINT,
        "temperature": 0.2,
        "thinking_mode": False,
        "frozen_head": EXPECTED_HEAD,
        "cell_count": 320,
        "started_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "llm_policy": "qwen3.5:9b_only",
        "scoring": False,
        "healer": False,
        "ab3": False,
    }
    _atomic_write_text(
        OUTPUT_ROOT / "run_manifest.json",
        json.dumps(run_manifest, ensure_ascii=False, indent=2) + "\n",
    )
    # snapshot frozen inputs (read-only copies for audit)
    _atomic_write_text(
        OUTPUT_ROOT / "frozen_runtime_manifest.json",
        MANIFEST_PATH.read_text(encoding="utf-8").replace("\r\n", "\n"),
    )
    _atomic_write_text(
        OUTPUT_ROOT / "frozen_cell_plan.json",
        PLAN_PATH.read_text(encoding="utf-8").replace("\r\n", "\n"),
    )

    tasks = tasks_by_id()
    consecutive_failures = 0
    stats = Counter()

    for idx, cell in enumerate(cell_plan):
        cell_id = cell["cell_id"]
        cell_dir = ROOT / "docs/experiments/results" / cell["output_relative_path"]
        expected = {
            "experiment_id": manifest["experiment_id"],
            "cell_id": cell_id,
            "task_id": cell["task_id"],
            "condition": cell["condition"],
            "seed": cell["seed"],
            "prompt_sha256": cell["prompt_sha256"],
            "model_tag": cell["model_tag"],
            "runtime_config_fingerprint": EXPECTED_FINGERPRINT,
        }

        status = "run"
        if cell_dir.exists() and any(cell_dir.iterdir()):
            art_path = cell_dir / "artifact.json"
            raw_path = cell_dir / "raw_response.txt"
            if art_path.exists():
                try:
                    art = json.loads(art_path.read_text(encoding="utf-8"))
                except Exception:
                    status = "incomplete"
                    art = None
                if art is not None:
                    for key, val in expected.items():
                        if art.get(key) != val:
                            raise RuntimeError(
                                f"INCOMPATIBLE_EXISTING_CELL: {cell_id} key={key} "
                                f"expected={val} got={art.get(key)}"
                            )
                    if (
                        art.get("persisted_complete") is True
                        and art.get("runtime_config_fingerprint") == EXPECTED_FINGERPRINT
                        and art.get("runtime_parameters", {}).get("temperature") == 0.2
                        and raw_path.exists()
                    ):
                        # success cells need non-empty raw; error cells may have error marker file
                        gen_status = art.get("generation_status", "success")
                        if gen_status == "success":
                            raw = raw_path.read_text(encoding="utf-8")
                            if not raw.strip():
                                status = "incomplete"
                            else:
                                status = "skip"
                        else:
                            status = "skip"
                    else:
                        status = "incomplete"
            else:
                status = "incomplete"

        if status == "skip":
            print(f"[{idx+1}/320] SKIP resume-complete {cell_id}")
            stats["skipped"] += 1
            continue

        if status == "incomplete":
            print(f"[{idx+1}/320] quarantine incomplete {cell_id}")
            quarantine_cell(cell_id, cell_dir)

        prompt = resolve_prompt(cell, tasks)
        print(
            f"[{idx+1}/320] CALL {cell_id} seed={cell['seed']} "
            f"temp=0.2 think=false"
        )
        started_at = datetime.now(timezone.utc).isoformat()
        t0 = time.monotonic()
        generation_status = "success"
        raw_text = ""
        error_record: dict[str, Any] | None = None
        api_attempts: list[dict[str, Any]] = []
        meta: dict[str, Any] = {}

        try:
            result = call_qwen_with_retries(
                prompt,
                seed=int(cell["seed"]),
                model=MODEL_TAG,
                timeout_s=float(manifest["timeout_seconds"]),
            )
            raw_text = result["raw_text"]
            if not isinstance(raw_text, str) or not raw_text.strip():
                raise RuntimeError("empty_response_after_adapter")
            # enforce request used frozen sampling
            req_opts = (
                (result.get("metadata") or {})
                .get("request_payload", {})
                .get("options", {})
            )
            if req_opts.get("temperature") != 0.2:
                raise RuntimeError(
                    f"RUNTIME_TEMP_MISMATCH: {req_opts.get('temperature')}"
                )
            if (result.get("metadata") or {}).get("think") is not False:
                raise RuntimeError("RUNTIME_THINK_NOT_FALSE")
            if req_opts.get("seed") != int(cell["seed"]):
                raise RuntimeError("RUNTIME_SEED_NOT_APPLIED")
            api_attempts = result.get("api_attempts") or []
            meta = result.get("metadata") or {}
            consecutive_failures = 0
            stats["success"] += 1
        except InvalidInfrastructureError as exc:
            generation_status = "runtime_error"
            error_record = {
                "exception_type": type(exc).__name__,
                "exception_message": str(exc),
                "layer": getattr(exc, "layer", "L0"),
                "validity": getattr(exc, "validity", "INVALID_INFRASTRUCTURE"),
                "api_attempts": getattr(exc, "api_attempts", []),
            }
            api_attempts = list(getattr(exc, "api_attempts", []) or [])
            raw_text = ""
            consecutive_failures += 1
            stats["runtime_error"] += 1
            print(f"[{idx+1}/320] RUNTIME_ERROR {cell_id}: {exc}")
        except Exception as exc:  # noqa: BLE001
            msg = str(exc).lower()
            if "timeout" in msg or "timed out" in msg:
                generation_status = "timeout"
                stats["timeout"] += 1
            elif "empty" in msg:
                generation_status = "empty_response"
                stats["empty_response"] += 1
            else:
                generation_status = "runtime_error"
                stats["runtime_error"] += 1
            error_record = {
                "exception_type": type(exc).__name__,
                "exception_message": str(exc),
            }
            raw_text = ""
            consecutive_failures += 1
            print(f"[{idx+1}/320] ERROR {generation_status} {cell_id}: {exc}")

        duration = time.monotonic() - t0
        completed_at = datetime.now(timezone.utc).isoformat()
        artifact = {
            "experiment_id": manifest["experiment_id"],
            "cell_id": cell_id,
            "task_id": cell["task_id"],
            "family": cell.get("family"),
            "condition": cell["condition"],
            "seed": cell["seed"],
            "model_tag": MODEL_TAG,
            "model_digest": EXPECTED_DIGEST,
            "runtime_config_fingerprint": EXPECTED_FINGERPRINT,
            "runtime_parameters": {
                "temperature": 0.2,
                "top_p": 0.8,
                "top_k": 20,
                "repeat_penalty": "ollama_default_unset",
                "think": False,
                "num_ctx": manifest["context_window"],
                "num_predict": manifest["max_output_tokens"],
                "timeout_seconds": manifest["timeout_seconds"],
                "seed": int(cell["seed"]),
            },
            "prompt_sha256": cell["prompt_sha256"],
            "prompt_path": cell.get("prompt_path"),
            "generation_status": generation_status,
            "raw_response": raw_text,
            "error": error_record,
            "attempt_count": len(api_attempts) or meta.get("api_attempt_count"),
            "started_at_utc": started_at,
            "completed_at_utc": completed_at,
            "duration": duration,
            "persisted_complete": True,
            "provenance": {
                "api_attempts": api_attempts,
                "provider_metadata": {
                    "prompt_eval_count": meta.get("prompt_eval_count"),
                    "eval_count": meta.get("eval_count"),
                    "total_token_count": meta.get("total_token_count"),
                    "total_duration": meta.get("total_duration"),
                    "load_duration": meta.get("load_duration"),
                    "done_reason": meta.get("done_reason"),
                    "latency_ms": meta.get("latency_ms"),
                    "request_payload": meta.get("request_payload"),
                    "inference_config": meta.get("inference_config"),
                },
            },
            "scoring": False,
            "healer": False,
            "ab3": False,
        }

        cell_dir.mkdir(parents=True, exist_ok=True)
        _atomic_write_text(cell_dir / "prompt.txt", prompt)
        if generation_status == "success":
            _atomic_write_text(cell_dir / "raw_response.txt", raw_text)
        else:
            _atomic_write_text(
                cell_dir / "raw_response.txt",
                f"[GENERATION_{generation_status.upper()}]\n{json.dumps(error_record, ensure_ascii=False)}\n",
            )
            _atomic_write_text(
                cell_dir / "error.json",
                json.dumps(error_record, ensure_ascii=False, indent=2) + "\n",
            )
        _atomic_write_text(
            cell_dir / "artifact.json",
            json.dumps(artifact, ensure_ascii=False, indent=2) + "\n",
        )
        _append_journal(
            {
                "ts_utc": completed_at,
                "index": idx + 1,
                "of": 320,
                "cell_id": cell_id,
                "generation_status": generation_status,
                "duration": duration,
                "prompt_sha256": cell["prompt_sha256"],
                "runtime_config_fingerprint": EXPECTED_FINGERPRINT,
                "temperature": 0.2,
            }
        )
        print(f"[{idx+1}/320] SAVED {generation_status} {cell_id} ({duration:.1f}s)")

        if consecutive_failures >= CONSECUTIVE_FAILURE_STOP:
            raise RuntimeError(
                f"CONSECUTIVE_FAILURE_STOP after {consecutive_failures} "
                f"failures at cell {cell_id}"
            )

    summary = {
        "completed_cells": 320,
        "stats": dict(stats),
        "fingerprint": EXPECTED_FINGERPRINT,
        "finished_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    _atomic_write_text(
        OUTPUT_ROOT / "generation_summary.json",
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
    )
    return summary


def completeness_audit() -> dict[str, Any]:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    assert len(plan) == 320

    missing = []
    duplicates_check = Counter()
    prompt_drift = []
    fingerprint_mismatch = []
    temp_mismatch = []
    digest_mismatch = []
    empty_success = []
    status_counts = Counter()

    for cell in plan:
        duplicates_check[cell["cell_id"]] += 1
        cell_dir = ROOT / "docs/experiments/results" / cell["output_relative_path"]
        art_path = cell_dir / "artifact.json"
        raw_path = cell_dir / "raw_response.txt"
        if not art_path.exists():
            missing.append(cell["cell_id"])
            continue
        art = json.loads(art_path.read_text(encoding="utf-8"))
        status = art.get("generation_status", "success")
        status_counts[status] += 1
        if art.get("runtime_config_fingerprint") != EXPECTED_FINGERPRINT:
            fingerprint_mismatch.append(cell["cell_id"])
        if art.get("runtime_parameters", {}).get("temperature") != 0.2:
            temp_mismatch.append(cell["cell_id"])
        if art.get("model_digest") != EXPECTED_DIGEST:
            digest_mismatch.append(cell["cell_id"])
        if art.get("prompt_sha256") != cell["prompt_sha256"]:
            prompt_drift.append(cell["cell_id"])
        if not raw_path.exists():
            missing.append(cell["cell_id"] + ":raw")
            continue
        raw = raw_path.read_text(encoding="utf-8")
        if status == "success" and not raw.strip():
            empty_success.append(cell["cell_id"])
        # verify prompt file sha if present
        pfile = cell_dir / "prompt.txt"
        if pfile.exists() and _sha_file_lf(pfile) != cell["prompt_sha256"]:
            prompt_drift.append(cell["cell_id"] + ":prompt_file")

    cond_c = Counter()
    fam_c = Counter()
    task_c = Counter()
    seed_c = Counter()
    for cell in plan:
        cell_dir = ROOT / "docs/experiments/results" / cell["output_relative_path"]
        if (cell_dir / "artifact.json").exists():
            cond_c[cell["condition"]] += 1
            fam_c[cell["family"]] += 1
            task_c[cell["task_id"]] += 1
            seed_c[cell["seed"]] += 1

    duplicate_ids = [k for k, v in duplicates_check.items() if v != 1]
    present = 320 - len([m for m in missing if not m.endswith(":raw")])
    # recount present properly
    present = sum(
        1
        for cell in plan
        if (ROOT / "docs/experiments/results" / cell["output_relative_path"] / "artifact.json").exists()
    )

    # forbid scoring/healer outputs
    forbidden = []
    for name in (
        "evaluation",
        "ab3",
        "healer",
        "score",
        "taxonomy_eval",
    ):
        for p in OUTPUT_ROOT.rglob(f"*{name}*"):
            if "_quarantine" in str(p):
                continue
            # allow none of these directories for generation-only
            if p.is_file() and name in p.name.lower():
                if p.name in ("generation_summary.json", "run_manifest.json", "cell_journal.jsonl"):
                    continue
                if "error.json" in p.name:
                    continue
                forbidden.append(str(p.relative_to(ROOT)))

    report = {
        "audit": "generation_completeness",
        "present_artifacts": present,
        "expected": 320,
        "missing": missing,
        "duplicate_cell_ids_in_plan": duplicate_ids,
        "prompt_drift": prompt_drift,
        "fingerprint_mismatch": fingerprint_mismatch,
        "temperature_mismatch": temp_mismatch,
        "model_digest_mismatch": digest_mismatch,
        "empty_success_raw": empty_success,
        "status_counts": dict(status_counts),
        "counts": {
            "condition": dict(cond_c),
            "family": dict(fam_c),
            "task": {k: task_c[k] for k in sorted(task_c)},
            "seed": {str(k): seed_c[k] for k in sorted(seed_c)},
        },
        "geometry_ok": (
            present == 320
            and not missing
            and not duplicate_ids
            and not prompt_drift
            and not fingerprint_mismatch
            and not temp_mismatch
            and not digest_mismatch
            and not empty_success
            and cond_c == {"ab1": 80, "ab2g": 80, "ab2d": 80, "ab2d_spec_v2": 80}
            and fam_c == {"integer": 80, "polynomial": 80, "radical": 80, "fraction": 80}
            and all(v == 20 for v in task_c.values())
            and len(task_c) == 16
            and all(v == 64 for v in seed_c.values())
        ),
        "scoring_ab3_healer_present": False,
        "forbidden_paths": forbidden,
        "fingerprint": EXPECTED_FINGERPRINT,
        "model_tag": MODEL_TAG,
        "manifest_temperature": manifest["temperature"],
    }
    report["passed"] = bool(report["geometry_ok"] and not forbidden)
    _atomic_write_text(
        OUTPUT_ROOT / "generation_completeness_audit.json",
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--preflight-only", action="store_true")
    group.add_argument("--execute", action="store_true")
    group.add_argument("--audit-only", action="store_true")
    args = parser.parse_args()

    if args.audit_only:
        report = completeness_audit()
        return 0 if report.get("passed") else 2

    data = do_preflight()
    if args.preflight_only:
        return 0

    summary = execute_generations(data["manifest"], data["cell_plan"])
    print(json.dumps(summary, indent=2))
    report = completeness_audit()
    if not report.get("passed"):
        print("GENERATION_COMPLETENESS_AUDIT_FAILED")
        return 2
    print("QWEN9B_320CELL_GENERATION_COMPLETED")
    print("QWEN9B_GENERATION_COMPLETENESS_AUDIT_PASSED")
    print("QWEN9B_RAW_OUTPUTS_FROZEN_FOR_EVIDENCE_CLOSEOUT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
