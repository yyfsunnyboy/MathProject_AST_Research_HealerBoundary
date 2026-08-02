# -*- coding: utf-8 -*-
"""Math16 Gemini top_p/top_k qualification (shared full-plan + domain-menu).

Uses the same Math16 model_settings authority as formal execution
(``math16_ab2d_formal_execution``), not CE115 transport constants.
qualification_only=true. No retries. Not formal evidence.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from agent_tools.finals_rebuild.math16_ab2d_formal_execution import (
    MATH16_MODEL_SETTINGS_REL,
    ROOT,
    _call_math16_gemini_once,
    build_math16_gemini_request_metadata,
    load_math16_model_settings,
    math16_gemini_generation_config,
)
from agent_tools.finals_rebuild.math16_ab2d_full_artifact_assembly import (
    QFIX_001_ID,
    atomic_write_json,
    atomic_write_text,
    build_evaluation_result,
    write_artifact_manifest,
    write_evaluation_artifacts,
)
from agent_tools.finals_rebuild.math16_pool import load_pool_manifest, tasks_by_id
from scripts.run_math16_latex_v1_gemini_live import classify_math16_response

SEED = 2026071301
EXPECTED_HEAD = "94fb195f9d8cb41803bd8dc3a0faaa49e7a5f03a"
EXPECTED_TASK_FREEZE = "349dfb2f786a4aa029453d844cac7eca07deb24a777ba1be4ef70f7002882e14"
EXPECTED_POOL_IDENTITY = "2ff41465d818d7e3d9b990a27ad2a1535e72c271bb04b2a37abe29cec1824636"
EXPECTED_SCAFFOLD = "7ea108503d09b8f0130827e928ea38dbddf5a56833c2fde7741a35f85a6b1f1f"

QUAL_CELLS = [
    {"domain": "Polynomial", "task_id": "ce115_calc_polynomial_division_l1"},
    {"domain": "Fraction", "task_id": "ce113_q01_negative_fraction_subtraction"},
    {"domain": "Radical", "task_id": "ce112_q04_radical_simplification"},
    {"domain": "Integer", "task_id": "ce112_q09_divisor_multiple_intersection"},
]

ALLOWED_DIRTY_PREFIXES = (
    "agent_tools/finals_rebuild/math16_ab2d_domain_menu.py",
    "agent_tools/finals_rebuild/math16_ab2d_full.py",
    "agent_tools/finals_rebuild/math16_ab2d_formal_execution.py",
    "agent_tools/finals_rebuild/math16_ab2d_gemini_topk_qualification.py",
    "docs/experiments/prompts/ab2d_domain_menu/",
    "docs/experiments/prompts/ab2d_full/",
    "docs/experiments/templates/ab2d_domain_menu/",
    "docs/experiments/results/math16_ab2d_domain_menu_preflight_v1/",
    "docs/experiments/results/math16_ab2d_full_phase3_preflight_v1/",
    "docs/experiments/results/Math16/",
    "tests/finals_rebuild/test_math16_ab2d_domain_menu.py",
    "tests/finals_rebuild/test_math16_ab2d_full_phase3.py",
    "tests/finals_rebuild/test_math16_ab2d_formal_execution_layer.py",
    "scripts/math16_ab2d_formal_cli.py",
    "scripts/orchestrate_math16_ab2d_menu_vs_full_formal.py",
    "scripts/run_math16_ab2d_",
    "artifacts/math16_ab2d_",
)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.replace("\r\n", "\n").encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _status_paths(status: str) -> list[str]:
    paths: list[str] = []
    for line in status.splitlines():
        if not line.strip():
            continue
        body = line[3:] if len(line) > 3 else line
        if " -> " in body:
            body = body.split(" -> ", 1)[1]
        paths.append(body.replace("\\", "/"))
    return paths


def dirty_tree_allowed(status: str) -> tuple[bool, list[str]]:
    bad: list[str] = []
    for path in _status_paths(status):
        if not any(path == p or path.startswith(p) for p in ALLOWED_DIRTY_PREFIXES):
            bad.append(path)
    return (len(bad) == 0, bad)


def build_local_prompt_freeze(
    *,
    experiment_id: str,
    condition: str,
    prompt_dir: Path,
    qual_root: Path,
) -> dict[str, Any]:
    tasks = tasks_by_id(ROOT)
    rows = []
    mismatches = []

    if condition == "ab2d_full":
        from agent_tools.finals_rebuild.math16_ab2d_full import build_ab2d_full_prompt

        builder_name = "agent_tools/finals_rebuild/math16_ab2d_full.py::build_ab2d_full_prompt"
        for cell in QUAL_CELLS:
            tid = cell["task_id"]
            path = prompt_dir / f"{tid}.txt"
            on_disk = path.read_text(encoding="utf-8").replace("\r\n", "\n")
            built = build_ab2d_full_prompt(tasks[tid], ROOT)
            disk_sha = sha256_text(on_disk)
            if on_disk != built:
                mismatches.append(tid)
            rows.append(
                {
                    "task_id": tid,
                    "path": str(path.relative_to(ROOT)).replace("\\", "/"),
                    "prompt_sha256": disk_sha,
                    "matches_builder": on_disk == built,
                }
            )
        payload = {
            "experiment_id": experiment_id,
            "condition": condition,
            "prompt_builder": builder_name,
            "n_prompts": len(rows),
            "all_match_builder": len(mismatches) == 0,
            "mismatches": mismatches,
            "prompts": rows,
        }
    else:
        from agent_tools.finals_rebuild.math16_ab2d_domain_menu import (
            build_domain_menu_prompt,
            load_domain_template,
        )

        menu_man = json.loads(
            (ROOT / "docs/experiments/prompts/ab2d_domain_menu/manifest.json").read_text(
                encoding="utf-8"
            )
        )
        by_id = {t["task_id"]: t for t in menu_man["tasks"]}
        builder_name = (
            "agent_tools/finals_rebuild/math16_ab2d_domain_menu.py::build_domain_menu_prompt"
        )
        for cell in QUAL_CELLS:
            tid = cell["task_id"]
            path = prompt_dir / f"{tid}.txt"
            on_disk = path.read_text(encoding="utf-8").replace("\r\n", "\n")
            disk_sha = sha256_text(on_disk)
            expected = by_id[tid]["prompt_sha256"]
            built = build_domain_menu_prompt(
                tasks[tid], load_domain_template(tasks[tid]["domain_ops"], ROOT)
            )
            if disk_sha != expected or on_disk != built:
                mismatches.append(tid)
            rows.append(
                {
                    "task_id": tid,
                    "path": str(path.relative_to(ROOT)).replace("\\", "/"),
                    "prompt_sha256": disk_sha,
                    "matches_manifest": disk_sha == expected,
                    "matches_builder": on_disk == built,
                    "manifest_sha256": expected,
                }
            )
        payload = {
            "experiment_id": experiment_id,
            "condition": condition,
            "prompt_builder": builder_name,
            "manifest_rel": "docs/experiments/prompts/ab2d_domain_menu/manifest.json",
            "n_prompts": len(rows),
            "all_match_builder": len(mismatches) == 0,
            "all_match_manifest": len(mismatches) == 0,
            "mismatches": mismatches,
            "prompts": rows,
        }

    atomic_write_json(qual_root / "prompt_freeze.json", payload)
    return payload


def pre_run_lock(
    *,
    experiment_id: str,
    condition: str,
    prompt_freeze: dict[str, Any],
    prompt_dir: Path,
    qual_root: Path,
    require_scaffold: bool,
) -> dict[str, Any]:
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    origin = subprocess.check_output(["git", "rev-parse", "origin/main"], cwd=ROOT, text=True).strip()
    status = subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True)
    dirty_ok, dirty_bad = dirty_tree_allowed(status)
    pool = load_pool_manifest(ROOT)
    settings = load_math16_model_settings()
    ms = settings["models"]["gemini"]
    gen_cfg = math16_gemini_generation_config(ms)

    scaffold_sha = None
    scaffold_ok = True
    if require_scaffold:
        scaffold_path = ROOT / "docs/experiments/prompts/ab2d_full/derived_scaffolds_v1.json"
        scaffold_sha = sha256_file(scaffold_path)
        scaffold_ok = scaffold_sha == EXPECTED_SCAFFOLD

    prompt_by_id = {row["task_id"]: row for row in prompt_freeze["prompts"]}
    prompt_checks = []
    for cell in QUAL_CELLS:
        tid = cell["task_id"]
        path = prompt_dir / f"{tid}.txt"
        disk_sha = sha256_text(path.read_text(encoding="utf-8"))
        expected = prompt_by_id[tid]["prompt_sha256"]
        prompt_checks.append(
            {
                "task_id": tid,
                "disk_sha256": disk_sha,
                "manifest_sha256": expected,
                "match": disk_sha == expected,
            }
        )

    ok = (
        head == EXPECTED_HEAD
        and head == origin
        and dirty_ok
        and scaffold_ok
        and pool["task_freeze_hash"] == EXPECTED_TASK_FREEZE
        and pool["pool_identity_hash"] == EXPECTED_POOL_IDENTITY
        and prompt_freeze["all_match_builder"]
        and all(c["match"] for c in prompt_checks)
        and bool(__import__("os").environ.get("GEMINI_API_KEY"))
        and gen_cfg["temperature"] == 0.0
        and gen_cfg["max_output_tokens"] == 24576
        and gen_cfg["top_p"] == 1.0
        and gen_cfg["top_k"] == 1
        and int(ms["timeout_seconds"]) == 600
        and ms["model_identifier"] == "gemini-3.5-flash"
    )
    lock = {
        "ok": ok,
        "experiment_id": experiment_id,
        "condition": condition,
        "head": head,
        "origin_main": origin,
        "expected_head": EXPECTED_HEAD,
        "working_tree_clean": status.strip() == "",
        "dirty_tree_allowed": dirty_ok,
        "dirty_unexpected": dirty_bad,
        "scaffold_sha256": scaffold_sha,
        "task_freeze_hash": pool["task_freeze_hash"],
        "pool_identity_hash": pool["pool_identity_hash"],
        "prompt_checks": prompt_checks,
        "model_settings": {
            "parameter_authority": MATH16_MODEL_SETTINGS_REL,
            "model_identifier": ms["model_identifier"],
            "generation_config": gen_cfg,
            "timeout_seconds": int(ms["timeout_seconds"]),
            "api_key_present": bool(__import__("os").environ.get("GEMINI_API_KEY")),
        },
        "no_retry": True,
        "qualification_only": True,
        "primary_evidence": False,
        "note": "Gemini settings sourced from Math16 formal model_settings (not CE115 transport).",
    }
    atomic_write_json(qual_root / "pre_run_lock.json", lock)
    if not ok:
        raise RuntimeError(f"PRE_RUN_LOCK failed: {json.dumps(lock, ensure_ascii=False)}")
    return lock


def call_once(prompt: str, ms: dict[str, Any]) -> dict[str, Any]:
    try:
        resp = _call_math16_gemini_once(prompt, ms)
        raw = resp.get("raw_text")
        if not isinstance(raw, str) or not raw.strip():
            raise RuntimeError("empty_response")
        meta = dict(resp.get("metadata") or {})
        meta["attempt_count"] = 1
        return {
            "raw_text": raw,
            "metadata": meta,
            "api_attempts": [{"attempt": 1, "ok": True}],
            "transport_error": None,
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "raw_text": "",
            "metadata": {"attempt_count": 1},
            "api_attempts": [{"attempt": 1, "ok": False, "error": f"{type(exc).__name__}: {exc}"}],
            "transport_error": f"{type(exc).__name__}: {exc}",
        }


def run_one(
    *,
    cell_spec: dict[str, Any],
    tasks: dict[str, Any],
    prompt_by_id: dict[str, Any],
    freeze_commit: str,
    experiment_id: str,
    condition: str,
    prompt_dir: Path,
    qual_root: Path,
    ms: dict[str, Any],
    scaffold_sha: str | None,
) -> dict[str, Any]:
    tid = cell_spec["task_id"]
    task = tasks[tid]
    cell_id = f"gemini__{tid}__{condition}__seed_{SEED}"
    cell_dir = qual_root / "cells" / cell_id
    cell_dir.mkdir(parents=True, exist_ok=True)

    prompt = (prompt_dir / f"{tid}.txt").read_text(encoding="utf-8").replace("\r\n", "\n")
    prompt_sha = sha256_text(prompt)
    if prompt_sha != prompt_by_id[tid]["prompt_sha256"]:
        raise RuntimeError(f"prompt hash drift: {tid}")

    req = build_math16_gemini_request_metadata(prompt, ms)
    req.update(
        {
            "qualification_only": True,
            "primary_evidence": False,
            "cell_seed": SEED,
            "freeze_commit": freeze_commit,
            "experiment_id": experiment_id,
            "condition": condition,
            "model_key": "gemini",
        }
    )
    atomic_write_text(cell_dir / "prompt.txt", prompt)
    atomic_write_json(cell_dir / "request_metadata.json", req)

    print(f"Calling Gemini (Math16 settings, no retry): {cell_id}")
    started = datetime.now(timezone.utc).isoformat()
    t0 = time.monotonic()
    call = call_once(prompt, ms)
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
            "model_calls": 0 if call["transport_error"] and not call["raw_text"] else 1,
            "generation_config_sent": math16_gemini_generation_config(ms),
        },
    )

    pipeline = {
        "model_call_attempted": True,
        "raw_response_preserved": (cell_dir / "raw_response.txt").exists(),
        "extraction_attempted": False,
        "execution_evaluation_completed_or_recorded": False,
        "transport_error": call["transport_error"],
    }

    if call["transport_error"] and not call["raw_text"]:
        outcome = "transport_failure"
        evaluation = build_evaluation_result(
            outcome=outcome,
            source=None,
            details={"error": call["transport_error"], "api_attempts": call["api_attempts"]},
            frozen_params=task["frozen_params"],
        )
        pipeline["execution_evaluation_completed_or_recorded"] = True
        source = None
    else:
        pipeline["extraction_attempted"] = True
        outcome, source, details = classify_math16_response(
            call["raw_text"],
            frozen_params=task["frozen_params"],
            audit_oracle_payload=task["oracle_payload"],
            task=task,
        )
        pipeline["execution_evaluation_completed_or_recorded"] = True
        if source:
            atomic_write_text(cell_dir / "extracted_source.py", source)
        evaluation = build_evaluation_result(
            outcome=outcome,
            source=source,
            details=details,
            frozen_params=task["frozen_params"],
        )

    write_evaluation_artifacts(cell_dir, evaluation=evaluation, outcome=outcome)
    artifact = {
        "experiment_id": experiment_id,
        "cell_id": cell_id,
        "qualification_only": True,
        "primary_evidence": False,
        "model": ms["model_identifier"],
        "model_key": "gemini",
        "task_id": tid,
        "domain": cell_spec["domain"],
        "condition": condition,
        "seed": SEED,
        "prompt_sha256": prompt_sha,
        "scaffold_sha256": scaffold_sha,
        "freeze_commit": freeze_commit,
        "outcome": outcome,
        "pipeline": pipeline,
        "duration_seconds": duration,
        "started_at_utc": started,
        "completed_at_utc": datetime.now(timezone.utc).isoformat(),
        "persisted_complete": True,
        "artifact_assembly": QFIX_001_ID,
        "no_retry": True,
        "parameter_authority": MATH16_MODEL_SETTINGS_REL,
        "generation_config": math16_gemini_generation_config(ms),
    }
    return write_artifact_manifest(cell_dir, artifact)


def pipeline_gate(qual_root: Path, artifacts: list[dict[str, Any]]) -> dict[str, Any]:
    rows = []
    schema_mismatch_cells: list[str] = []
    for art in artifacts:
        cell_dir = qual_root / "cells" / art["cell_id"]
        required = [
            "prompt.txt",
            "raw_response.txt",
            "request_metadata.json",
            "evaluation_result.json",
            "execution_result.json",
            "logs.json",
            "artifact.json",
        ]
        missing = [n for n in required if not (cell_dir / n).exists()]
        pipe = art.get("pipeline") or {}
        req = json.loads((cell_dir / "request_metadata.json").read_text(encoding="utf-8"))
        gen = req.get("generation_config") or {}
        top_ok = gen.get("top_p") == 1.0 and gen.get("top_k") == 1
        outcome = art.get("outcome")
        if outcome == "schema_failure":
            schema_mismatch_cells.append(art["cell_id"])
        complete = (
            not missing
            and pipe.get("model_call_attempted") is True
            and pipe.get("raw_response_preserved") is True
            and pipe.get("execution_evaluation_completed_or_recorded") is True
            and art.get("persisted_complete") is True
            and top_ok
        )
        rows.append(
            {
                "cell_id": art["cell_id"],
                "task_id": art["task_id"],
                "domain": art["domain"],
                "outcome": outcome,
                "pipeline_complete": complete,
                "missing_files": missing,
                "extraction_attempted": pipe.get("extraction_attempted"),
                "generation_config": gen,
                "top_p_top_k_ok": top_ok,
            }
        )
    return {
        "n_cells": len(rows),
        "all_pipeline_complete": all(r["pipeline_complete"] for r in rows),
        "schema_mismatch_count": len(schema_mismatch_cells),
        "schema_mismatch_cells": schema_mismatch_cells,
        "answer_correctness_not_required": True,
        "rows": rows,
    }


def run_qualification(
    *,
    experiment_id: str,
    condition: str,
    prompt_dir: Path,
    require_scaffold: bool,
) -> int:
    qual_root = ROOT / "artifacts" / experiment_id
    qual_root.mkdir(parents=True, exist_ok=True)
    (qual_root / "cells").mkdir(parents=True, exist_ok=True)
    freeze_commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    prompt_freeze = build_local_prompt_freeze(
        experiment_id=experiment_id,
        condition=condition,
        prompt_dir=prompt_dir,
        qual_root=qual_root,
    )
    lock = pre_run_lock(
        experiment_id=experiment_id,
        condition=condition,
        prompt_freeze=prompt_freeze,
        prompt_dir=prompt_dir,
        qual_root=qual_root,
        require_scaffold=require_scaffold,
    )
    settings = load_math16_model_settings()
    ms = settings["models"]["gemini"]
    tasks = tasks_by_id(ROOT)
    prompt_by_id = {r["task_id"]: r for r in prompt_freeze["prompts"]}
    scaffold_sha = lock.get("scaffold_sha256")

    artifacts = []
    model_calls = 0
    for cell in QUAL_CELLS:
        art = run_one(
            cell_spec=cell,
            tasks=tasks,
            prompt_by_id=prompt_by_id,
            freeze_commit=freeze_commit,
            experiment_id=experiment_id,
            condition=condition,
            prompt_dir=prompt_dir,
            qual_root=qual_root,
            ms=ms,
            scaffold_sha=scaffold_sha,
        )
        artifacts.append(art)
        logs = json.loads((qual_root / "cells" / art["cell_id"] / "logs.json").read_text(encoding="utf-8"))
        model_calls += int(logs.get("model_calls") or 0)

    gate = pipeline_gate(qual_root, artifacts)
    summary = {
        "experiment_id": experiment_id,
        "condition": condition,
        "qualification_only": True,
        "primary_evidence": False,
        "freeze_commit": freeze_commit,
        "pre_run_lock_ok": lock["ok"],
        "parameter_authority": MATH16_MODEL_SETTINGS_REL,
        "generation_config": math16_gemini_generation_config(ms),
        "model_calls": model_calls,
        "no_retry": True,
        "gate": gate,
        "artifacts": [
            {
                "cell_id": a["cell_id"],
                "task_id": a["task_id"],
                "domain": a["domain"],
                "outcome": a["outcome"],
                "prompt_sha256": a["prompt_sha256"],
                "generation_config": a.get("generation_config"),
            }
            for a in artifacts
        ],
        "passed_gate": gate["all_pipeline_complete"] and gate["schema_mismatch_count"] == 0,
    }
    atomic_write_json(qual_root / "qualification_summary.json", summary)
    print(json.dumps({k: summary[k] for k in summary if k != "artifacts"}, ensure_ascii=False, indent=2))
    print(json.dumps({"artifacts": summary["artifacts"]}, ensure_ascii=False, indent=2))
    if gate["schema_mismatch_count"] > 0:
        print("ABORT: schema_failure reappeared — stop and report.")
        return 2
    return 0 if summary["passed_gate"] else 1
