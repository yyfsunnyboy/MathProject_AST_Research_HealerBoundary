# -*- coding: utf-8 -*-
"""Shared Math16 Ab2d formal execution layer (domain-menu vs full-plan).

Authority for model parameters: Math16 frozen preregistration
``artifacts/math16_ab2d_full_domain_assisted_v1/preregistration/model_settings.json``
(backed by Math16 pilot02 runtime manifests). CE115 transports are not authoritative.
"""
from __future__ import annotations

import hashlib
import json
import os
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from agent_tools.finals_rebuild.math16_ab2d_full_artifact_assembly import (
    QFIX_001_ID,
    atomic_write_json,
    atomic_write_text,
    build_evaluation_result,
    write_artifact_manifest,
    write_evaluation_artifacts,
)
from agent_tools.finals_rebuild.math16_pool import load_pool_manifest, tasks_by_id

ROOT = Path(__file__).resolve().parents[2]

EXECUTION_FREEZE_COMMIT = "94fb195f9d8cb41803bd8dc3a0faaa49e7a5f03a"
EXPECTED_TASK_FREEZE = "349dfb2f786a4aa029453d844cac7eca07deb24a777ba1be4ef70f7002882e14"
EXPECTED_POOL_IDENTITY = "2ff41465d818d7e3d9b990a27ad2a1535e72c271bb04b2a37abe29cec1824636"
EXPECTED_SCAFFOLD = "7ea108503d09b8f0130827e928ea38dbddf5a56833c2fde7741a35f85a6b1f1f"

SEEDS = [2026071301, 2026072001, 2026072002, 2026072003, 2026072004]
MODEL_ORDER = ["gemini", "qwen_9b", "qwen_4b"]
MODELS = [
    {"model_key": "gemini", "model_id": "gemini-3.5-flash", "display": "Gemini"},
    {"model_key": "qwen_9b", "model_id": "qwen3.5:9b", "display": "Qwen 9B"},
    {"model_key": "qwen_4b", "model_id": "qwen3.5:4b", "display": "Qwen 4B"},
]

MATH16_MODEL_SETTINGS_REL = (
    "artifacts/math16_ab2d_full_domain_assisted_v1/preregistration/model_settings.json"
)
MATH16_EVALUATOR_BINDING_REL = (
    "artifacts/math16_ab2d_full_domain_assisted_v1/preregistration/evaluator_binding.json"
)
MATH16_GEMINI_RUNTIME_REL = "docs/experiments/manifests/math16_pilot02_full_runtime_manifest.json"
MATH16_QWEN9B_RUNTIME_REL = "docs/experiments/manifests/math16_pilot02_qwen9b_runtime_manifest.json"
MATH16_QWEN4B_RUNTIME_REL = "docs/experiments/manifests/math16_pilot02_qwen4b_runtime_manifest.json"

CONDITIONS = {
    "ab2d_full": {
        "condition": "ab2d_full",
        "experiment_id": "math16_ab2d_full_domain_assisted_v1",
        "prompt_dir": ROOT / "docs/experiments/prompts/ab2d_full/prompts",
        "artifact_root": ROOT / "artifacts/math16_ab2d_full_domain_assisted_v1",
        "has_scaffold": True,
        "scaffold_path": ROOT / "docs/experiments/prompts/ab2d_full/derived_scaffolds_v1.json",
        "prompt_builder": "agent_tools/finals_rebuild/math16_ab2d_full.py::build_ab2d_full_prompt",
    },
    "ab2d_domain_menu": {
        "condition": "ab2d_domain_menu",
        "experiment_id": "math16_ab2d_domain_menu_v1",
        "prompt_dir": ROOT / "docs/experiments/prompts/ab2d_domain_menu/prompts",
        "artifact_root": ROOT / "artifacts/math16_ab2d_domain_menu_v1",
        "has_scaffold": False,
        "scaffold_path": None,
        "prompt_builder": "agent_tools/finals_rebuild/math16_ab2d_domain_menu.py::build_domain_menu_prompt",
        "menu_manifest": ROOT / "docs/experiments/prompts/ab2d_domain_menu/manifest.json",
    },
}

REQUIRED_CELL_FILES = (
    "artifact.json",
    "evaluation_result.json",
    "execution_result.json",
    "extracted_source.py",
    "logs.json",
    "prompt.txt",
    "raw_response.txt",
    "request_metadata.json",
)

OLLAMA_BASE_URL = "http://127.0.0.1:11434"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def sha256_text(text: str) -> str:
    return sha256_bytes(text.replace("\r\n", "\n").encode("utf-8"))


def cell_id(model_key: str, task_id: str, condition: str, seed: int) -> str:
    return f"{model_key}__{task_id}__{condition}__seed_{seed}"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_math16_model_settings() -> dict[str, Any]:
    path = ROOT / MATH16_MODEL_SETTINGS_REL
    if not path.exists():
        raise RuntimeError(f"missing Math16 frozen model_settings: {path}")
    settings = load_json(path)
    if settings.get("seed_list") != SEEDS:
        raise RuntimeError(f"Math16 seed_list mismatch: {settings.get('seed_list')}")
    for key in MODEL_ORDER:
        if key not in settings.get("models", {}):
            raise RuntimeError(f"Math16 model_settings missing model_key={key}")
    # Fail-closed: Gemini must match historical 320-cell declared top_p/top_k.
    gemini = settings["models"]["gemini"]
    if float(gemini["top_p"]) != 1.0 or int(gemini["top_k"]) != 1:
        raise RuntimeError(
            f"Math16 Gemini top_p/top_k must be 1.0/1, got {gemini.get('top_p')}/{gemini.get('top_k')}"
        )
    if float(gemini["temperature"]) != 0.0 or int(gemini["max_output_tokens"]) != 24576:
        raise RuntimeError("Math16 Gemini temperature/max_output_tokens drift")
    if int(gemini["timeout_seconds"]) != 600:
        raise RuntimeError("Math16 Gemini timeout_seconds drift")
    return settings


def load_math16_evaluator_binding() -> dict[str, Any]:
    path = ROOT / MATH16_EVALUATOR_BINDING_REL
    if not path.exists():
        raise RuntimeError(f"missing Math16 evaluator_binding: {path}")
    return load_json(path)


def verify_pool_identity() -> dict[str, Any]:
    pool = load_pool_manifest(ROOT)
    ok = (
        pool["task_freeze_hash"] == EXPECTED_TASK_FREEZE
        and pool["pool_identity_hash"] == EXPECTED_POOL_IDENTITY
    )
    return {
        "ok": ok,
        "task_freeze_hash": pool["task_freeze_hash"],
        "pool_identity_hash": pool["pool_identity_hash"],
        "task_ids": list(pool["task_ids"]),
    }


def disk_prompt_sha_map(condition: str) -> dict[str, str]:
    prompt_dir: Path = CONDITIONS[condition]["prompt_dir"]
    return {p.stem: sha256_file(p) for p in sorted(prompt_dir.glob("*.txt"))}


def build_prompt_freeze(condition: str) -> dict[str, Any]:
    cfg = CONDITIONS[condition]
    pool = verify_pool_identity()
    if not pool["ok"]:
        raise RuntimeError(f"pool identity mismatch: {pool}")
    sha_map = disk_prompt_sha_map(condition)
    if len(sha_map) != 16:
        raise RuntimeError(f"{condition}: expected 16 prompts, got {len(sha_map)}")
    rows = []
    for tid in pool["task_ids"]:
        if tid not in sha_map:
            raise RuntimeError(f"missing prompt for {tid}")
        rows.append(
            {
                "task_id": tid,
                "path": str((cfg["prompt_dir"] / f"{tid}.txt").relative_to(ROOT)).replace(
                    "\\", "/"
                ),
                "prompt_sha256": sha_map[tid],
            }
        )
    if condition == "ab2d_domain_menu":
        menu = load_json(cfg["menu_manifest"])
        for t in menu["tasks"]:
            if t["prompt_sha256"] != sha_map[t["task_id"]]:
                raise RuntimeError(
                    f"menu manifest SHA drift: {t['task_id']} "
                    f"manifest={t['prompt_sha256']} disk={sha_map[t['task_id']]}"
                )
    return {
        "prompt_revision": (
            "ab2d_full_answer_contract_v1"
            if condition == "ab2d_full"
            else "ab2d_domain_menu_answer_contract_v1"
        ),
        "condition": condition,
        "experiment_id": cfg["experiment_id"],
        "execution_freeze_commit": EXECUTION_FREEZE_COMMIT,
        "prompt_builder": cfg["prompt_builder"],
        "n_tasks": 16,
        "all_match_disk": True,
        "all_match_builder": True,
        "line_endings": "LF",
        "sha_basis": "raw_bytes_utf8_lf",
        "tasks": [{"task_id": r["task_id"], "prompt_sha256": r["prompt_sha256"]} for r in rows],
        "prompts": rows,
    }


def build_cell_manifest(
    condition: str, prompt_freeze: dict[str, Any] | None = None
) -> list[dict[str, Any]]:
    cfg = CONDITIONS[condition]
    prompt_freeze = prompt_freeze or build_prompt_freeze(condition)
    sha_by_task = {r["task_id"]: r["prompt_sha256"] for r in prompt_freeze["tasks"]}
    scaffold_sha = EXPECTED_SCAFFOLD if cfg["has_scaffold"] else None
    if cfg["has_scaffold"]:
        disk_scaffold = sha256_file(cfg["scaffold_path"])
        if disk_scaffold != EXPECTED_SCAFFOLD:
            raise RuntimeError(f"scaffold SHA drift: {disk_scaffold}")
    cells: list[dict[str, Any]] = []
    for model in MODELS:
        for tid, prompt_sha in sha_by_task.items():
            for seed in SEEDS:
                row: dict[str, Any] = {
                    "cell_id": cell_id(model["model_key"], tid, condition, seed),
                    "experiment_id": cfg["experiment_id"],
                    "model": model["model_id"],
                    "model_key": model["model_key"],
                    "task_id": tid,
                    "condition": condition,
                    "seed": seed,
                    "prompt_sha256": prompt_sha,
                    "execution_freeze_commit": EXECUTION_FREEZE_COMMIT,
                }
                if scaffold_sha is not None:
                    row["scaffold_sha256"] = scaffold_sha
                cells.append(row)
    if len(cells) != 240:
        raise RuntimeError(f"expected 240 cells for {condition}, got {len(cells)}")
    return cells


def write_preregistration(condition: str) -> dict[str, Any]:
    cfg = CONDITIONS[condition]
    prereg = cfg["artifact_root"] / "preregistration"
    prereg.mkdir(parents=True, exist_ok=True)
    for model_key in MODEL_ORDER:
        (cfg["artifact_root"] / "formal" / model_key).mkdir(parents=True, exist_ok=True)

    prompt_freeze = build_prompt_freeze(condition)
    cells = build_cell_manifest(condition, prompt_freeze)
    model_settings = load_math16_model_settings()
    evaluator_binding = load_math16_evaluator_binding()

    execution_policy = {
        "model_order": MODEL_ORDER,
        "rationale": (
            "Hard sequential gate: Gemini integrity audit must pass before Qwen 9B; "
            "Qwen 9B audit must pass before Qwen 4B. No parallel/interleaved runs."
        ),
        "seed_list": SEEDS,
        "cells_per_model_per_condition": 80,
        "cells_per_condition": 240,
        "conditions": ["ab2d_domain_menu", "ab2d_full"],
        "total_formal_cells_both_conditions": 480,
        "parameter_authority": MATH16_MODEL_SETTINGS_REL,
        "math16_runtime_evidence": {
            "gemini": MATH16_GEMINI_RUNTIME_REL,
            "qwen_9b": MATH16_QWEN9B_RUNTIME_REL,
            "qwen_4b": MATH16_QWEN4B_RUNTIME_REL,
        },
        "cell_failure_policy": "continue; do not abort the full run on a single cell failure",
        "retry_scope": (
            "transport/runtime only per Math16 model_settings.retry_policy; "
            "never retry answer_incorrect / completed cells"
        ),
        "resume_policy": "never re-run completed cells; resume remaining pending cells only",
        "healer": False,
        "artifact_filenames": {
            "raw_response": "raw_response.txt",
            "extracted_source": "extracted_source.py",
            "execution_result": "execution_result.json",
            "evaluation_result": "evaluation_result.json",
            "cell_artifact": "artifact.json",
            "prompt_copy": "prompt.txt",
            "logs": "logs.json",
            "run_summary": "run_summary.json",
        },
        "cell_directory_pattern": (
            f"artifacts/{cfg['experiment_id']}/formal/{{model_key}}/{{cell_id}}/"
        ),
    }
    experiment_identity = {
        "experiment_id": cfg["experiment_id"],
        "condition": condition,
        "models": [m["model_id"] for m in MODELS],
        "model_keys": MODEL_ORDER,
        "n_tasks": 16,
        "seeds_per_task": 5,
        "seed_list": SEEDS,
        "total_cells": 240,
        "execution_freeze_commit": EXECUTION_FREEZE_COMMIT,
        "task_freeze_hash": EXPECTED_TASK_FREEZE,
        "pool_identity_hash": EXPECTED_POOL_IDENTITY,
        "scaffold_sha256": EXPECTED_SCAFFOLD if cfg["has_scaffold"] else None,
        "artifact_root": str(cfg["artifact_root"]).replace("\\", "/"),
        "model_settings_source": MATH16_MODEL_SETTINGS_REL,
        "evaluator_binding_source": MATH16_EVALUATOR_BINDING_REL,
    }

    atomic_write_json(prereg / "prompt_freeze.json", prompt_freeze)
    (prereg / "cell_manifest.jsonl").write_text(
        "".join(json.dumps(c, ensure_ascii=False, sort_keys=True) + "\n" for c in cells),
        encoding="utf-8",
        newline="\n",
    )
    atomic_write_json(prereg / "model_settings.json", model_settings)
    atomic_write_json(prereg / "evaluator_binding.json", evaluator_binding)
    atomic_write_json(prereg / "execution_policy.json", execution_policy)
    atomic_write_json(prereg / "experiment_identity.json", experiment_identity)
    return {
        "condition": condition,
        "n_cells": len(cells),
        "n_prompts": prompt_freeze["n_tasks"],
        "preregistration": str(prereg).replace("\\", "/"),
    }


def load_cell_manifest(condition: str, *, model_key: str | None = None) -> list[dict[str, Any]]:
    path = CONDITIONS[condition]["artifact_root"] / "preregistration" / "cell_manifest.jsonl"
    cells = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if model_key is not None:
        cells = [c for c in cells if c["model_key"] == model_key]
    return cells


def formal_root(condition: str, model_key: str) -> Path:
    return CONDITIONS[condition]["artifact_root"] / "formal" / model_key


def cell_is_complete(cell_dir: Path) -> bool:
    art = cell_dir / "artifact.json"
    if not art.exists():
        return False
    try:
        payload = load_json(art)
    except json.JSONDecodeError:
        return False
    if not payload.get("persisted_complete"):
        return False
    return all((cell_dir / name).exists() for name in REQUIRED_CELL_FILES)


def verify_prompt_hash(condition: str, cell: dict[str, Any]) -> str:
    path = CONDITIONS[condition]["prompt_dir"] / f"{cell['task_id']}.txt"
    disk_sha = sha256_file(path)
    if disk_sha != cell["prompt_sha256"]:
        raise RuntimeError(
            f"prompt hash drift: {cell['task_id']} cell={cell['prompt_sha256']} disk={disk_sha}"
        )
    return disk_sha


def audit_cell_plan(*, both_conditions: bool = True) -> dict[str, Any]:
    conditions = ["ab2d_domain_menu", "ab2d_full"] if both_conditions else list(CONDITIONS)
    all_ids: list[str] = []
    by_model: dict[str, int] = {m: 0 for m in MODEL_ORDER}
    by_condition: dict[str, int] = {}
    sha_mismatches: list[str] = []
    for condition in conditions:
        cells = load_cell_manifest(condition)
        by_condition[condition] = len(cells)
        disk = disk_prompt_sha_map(condition)
        for c in cells:
            all_ids.append(c["cell_id"])
            by_model[c["model_key"]] += 1
            if c["prompt_sha256"] != disk.get(c["task_id"]):
                sha_mismatches.append(c["cell_id"])
    unique = len(set(all_ids))
    expected = 480 if both_conditions else len(all_ids)
    per_model = 160 if both_conditions else 80
    return {
        "total_cells": len(all_ids),
        "unique_cells": unique,
        "duplicate": len(all_ids) - unique,
        "missing": max(0, expected - unique),
        "by_model": by_model,
        "by_condition": by_condition,
        "sha_mismatches": sha_mismatches,
        "ok": (
            unique == expected
            and (len(all_ids) - unique) == 0
            and not sha_mismatches
            and by_model.get("gemini") == per_model
            and by_model.get("qwen_9b") == per_model
            and by_model.get("qwen_4b") == per_model
        ),
        "model_calls": 0,
    }


def completeness_report(condition: str, model_key: str) -> dict[str, Any]:
    cells = load_cell_manifest(condition, model_key=model_key)
    root = formal_root(condition, model_key)
    complete = []
    incomplete = []
    for c in cells:
        d = root / c["cell_id"]
        (complete if cell_is_complete(d) else incomplete).append(c["cell_id"])
    return {
        "condition": condition,
        "model_key": model_key,
        "planned": len(cells),
        "complete": len(complete),
        "incomplete": len(incomplete),
        "incomplete_cell_ids": incomplete,
        "all_complete": len(incomplete) == 0 and len(cells) == 80,
    }


def math16_gemini_generation_config(ms: dict[str, Any]) -> dict[str, Any]:
    """Build Gemini generation_config from Math16 model_settings (fail-closed)."""
    temperature = float(ms["temperature"])
    max_output_tokens = int(ms["max_output_tokens"])
    timeout_seconds = int(ms["timeout_seconds"])
    top_p = float(ms["top_p"])
    top_k = int(ms["top_k"])
    if temperature != 0.0:
        raise RuntimeError(f"Math16 Gemini temperature must be 0.0, got {temperature}")
    if max_output_tokens != 24576:
        raise RuntimeError(f"Math16 Gemini max_output_tokens must be 24576, got {max_output_tokens}")
    if timeout_seconds != 600:
        raise RuntimeError(f"Math16 Gemini timeout_seconds must be 600, got {timeout_seconds}")
    if top_p != 1.0:
        raise RuntimeError(f"Math16 Gemini top_p must be 1.0, got {top_p}")
    if top_k != 1:
        raise RuntimeError(f"Math16 Gemini top_k must be 1, got {top_k}")
    return {
        "temperature": temperature,
        "max_output_tokens": max_output_tokens,
        "top_p": top_p,
        "top_k": top_k,
    }


def build_math16_gemini_request_metadata(prompt: str, ms: dict[str, Any]) -> dict[str, Any]:
    """Public request metadata with full Math16 generation_config (no API key)."""
    return {
        "provider": "gemini",
        "model": ms["model_identifier"],
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generation_config": math16_gemini_generation_config(ms),
        "timeout_seconds": int(ms["timeout_seconds"]),
        "tools": None,
        "code_execution": False,
        "function_calling": False,
        "api_key_source": "environment",
        "api_key_present": bool(os.environ.get("GEMINI_API_KEY")),
        "parameter_authority": MATH16_MODEL_SETTINGS_REL,
        "math16_runtime_evidence": MATH16_GEMINI_RUNTIME_REL,
    }


def _call_math16_gemini_once(prompt: str, ms: dict[str, Any]) -> dict[str, Any]:
    """Gemini call parameterized solely by Math16 model_settings."""
    if not os.environ.get("GEMINI_API_KEY"):
        raise RuntimeError("GEMINI_API_KEY missing")
    model_id = ms["model_identifier"]
    generation_config = math16_gemini_generation_config(ms)
    timeout_seconds = int(ms["timeout_seconds"])
    api_key = os.environ["GEMINI_API_KEY"]
    try:
        import importlib.util

        if importlib.util.find_spec("google.genai") is not None:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model=model_id,
                contents=prompt,
                config=types.GenerateContentConfig(**generation_config),
            )
            raw = getattr(response, "text", None)
            sdk = "google-genai"
        else:
            import google.generativeai as genai_old

            genai_old.configure(api_key=api_key)
            model = genai_old.GenerativeModel(model_id)
            response = model.generate_content(
                prompt,
                generation_config=generation_config,
                request_options={"timeout": timeout_seconds},
            )
            raw = getattr(response, "text", None)
            sdk = "google-generativeai"
    finally:
        api_key = ""
    if not isinstance(raw, str):
        raise RuntimeError("gemini response missing text string")
    return {
        "raw_text": raw,
        "metadata": {
            "model": model_id,
            "runtime": "math16_gemini",
            "sdk": sdk,
            "generation_config": generation_config,
            "timeout_seconds": timeout_seconds,
            "parameter_authority": MATH16_MODEL_SETTINGS_REL,
            "math16_runtime_evidence": MATH16_GEMINI_RUNTIME_REL,
        },
    }


def _call_math16_ollama_once(prompt: str, *, seed: int, model_key: str, ms: dict[str, Any]) -> dict[str, Any]:
    """Ollama /api/chat parameterized solely by Math16 model_settings."""
    model_id = ms["model_identifier"]
    payload = {
        "model": model_id,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "think": bool(ms.get("thinking_reasoning_setting", False)),
        "options": {
            "temperature": float(ms["temperature"]),
            "top_p": float(ms["top_p"]),
            "top_k": int(ms["top_k"]),
            "seed": int(seed),
            "num_ctx": int(ms["num_ctx_context_limit"]),
            "num_predict": int(ms["max_output_tokens"]),
        },
    }
    if payload["think"] is not False:
        # Math16 freeze requires think/reasoning false.
        raise RuntimeError("Math16 settings require thinking_reasoning_setting=false")
    timeout_s = float(ms["timeout_seconds"])
    started = time.monotonic()
    req = urllib.request.Request(
        OLLAMA_BASE_URL.rstrip("/") + "/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:  # noqa: S310
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Ollama HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise ConnectionError(f"Ollama unreachable: {exc}") from exc
    raw = (body.get("message") or {}).get("content")
    if not isinstance(raw, str):
        raise RuntimeError("model response missing message.content string")
    evidence = (
        MATH16_QWEN9B_RUNTIME_REL if model_key == "qwen_9b" else MATH16_QWEN4B_RUNTIME_REL
    )
    return {
        "raw_text": raw,
        "metadata": {
            "model": model_id,
            "model_key": model_key,
            "runtime": "math16_ollama",
            "think": False,
            "seed": int(seed),
            "options": payload["options"],
            "latency_ms": int((time.monotonic() - started) * 1000),
            "parameter_authority": MATH16_MODEL_SETTINGS_REL,
            "math16_runtime_evidence": evidence,
        },
    }


def call_model_with_math16_retries(
    *,
    model_key: str,
    prompt: str,
    seed: int,
    settings: dict[str, Any],
) -> dict[str, Any]:
    ms = settings["models"][model_key]
    policy = ms["retry_policy"]
    max_attempts = int(policy["max_attempts"])
    delays = list(policy["retry_delays_seconds"])
    attempts: list[dict[str, Any]] = []
    last_err: Exception | None = None
    for attempt in range(1, max_attempts + 1):
        try:
            if model_key == "gemini":
                resp = _call_math16_gemini_once(prompt, ms)
            else:
                resp = _call_math16_ollama_once(
                    prompt, seed=seed, model_key=model_key, ms=ms
                )
            raw = resp.get("raw_text")
            if not isinstance(raw, str) or not raw.strip():
                raise RuntimeError("empty_response")
            meta = dict(resp.get("metadata") or {})
            meta["attempt_count"] = attempt
            attempts.append({"attempt": attempt, "ok": True})
            return {
                "raw_text": raw,
                "metadata": meta,
                "api_attempts": attempts,
                "transport_error": None,
            }
        except Exception as exc:  # noqa: BLE001
            last_err = exc
            attempts.append(
                {"attempt": attempt, "ok": False, "error": f"{type(exc).__name__}: {exc}"}
            )
            if attempt < max_attempts:
                time.sleep(delays[min(attempt - 1, len(delays) - 1)])
    return {
        "raw_text": "",
        "metadata": {"attempt_count": max_attempts},
        "api_attempts": attempts,
        "transport_error": f"{type(last_err).__name__}: {last_err}" if last_err else "unknown",
    }


def assemble_cell_from_raw(
    *,
    condition: str,
    cell: dict[str, Any],
    cell_dir: Path,
    raw: str,
    task: dict[str, Any],
) -> dict[str, Any]:
    from scripts.run_math16_latex_v1_gemini_live import classify_math16_response

    outcome, source, details = classify_math16_response(
        raw,
        frozen_params=task["frozen_params"],
        audit_oracle_payload=task["oracle_payload"],
        task=task,
    )
    extracted_path = cell_dir / "extracted_source.py"
    if source:
        atomic_write_text(extracted_path, source)
    elif not extracted_path.exists():
        atomic_write_text(extracted_path, "")

    evaluation = build_evaluation_result(
        outcome=outcome,
        source=source
        if source is not None
        else (extracted_path.read_text(encoding="utf-8") if extracted_path.exists() else None),
        details=details,
        frozen_params=task["frozen_params"],
    )
    write_evaluation_artifacts(cell_dir, evaluation=evaluation, outcome=outcome)
    artifact = {
        "experiment_id": CONDITIONS[condition]["experiment_id"],
        "cell_id": cell["cell_id"],
        "qualification_only": False,
        "primary_evidence": True,
        "model": cell["model"],
        "model_key": cell["model_key"],
        "task_id": cell["task_id"],
        "condition": condition,
        "seed": cell["seed"],
        "prompt_sha256": cell["prompt_sha256"],
        "scaffold_sha256": cell.get("scaffold_sha256"),
        "execution_freeze_commit": EXECUTION_FREEZE_COMMIT,
        "outcome": outcome,
        "persisted_complete": True,
        "completed_at_utc": datetime.now(timezone.utc).isoformat(),
        "artifact_assembly": QFIX_001_ID,
        "healer": False,
        "parameter_authority": MATH16_MODEL_SETTINGS_REL,
    }
    return write_artifact_manifest(cell_dir, artifact)


def execute_formal_cell(
    *,
    condition: str,
    cell: dict[str, Any],
    tasks: dict[str, Any] | None = None,
    settings: dict[str, Any] | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    tasks = tasks or tasks_by_id(ROOT)
    settings = settings or load_math16_model_settings()
    model_key = cell["model_key"]
    root = formal_root(condition, model_key)
    cell_dir = root / cell["cell_id"]
    if cell_is_complete(cell_dir):
        return {"skipped": True, "reason": "already_complete", "cell_id": cell["cell_id"]}

    verify_prompt_hash(condition, cell)
    if dry_run:
        return {
            "dry_run": True,
            "cell_id": cell["cell_id"],
            "model_key": model_key,
            "condition": condition,
            "prompt_sha256": cell["prompt_sha256"],
            "model_calls": 0,
            "parameter_authority": MATH16_MODEL_SETTINGS_REL,
        }

    task = tasks[cell["task_id"]]
    prompt_path = CONDITIONS[condition]["prompt_dir"] / f"{cell['task_id']}.txt"
    prompt = prompt_path.read_text(encoding="utf-8")
    cell_dir.mkdir(parents=True, exist_ok=True)
    atomic_write_text(cell_dir / "prompt.txt", prompt)
    ms = settings["models"][model_key]
    if model_key == "gemini":
        req_meta = build_math16_gemini_request_metadata(prompt, ms)
        req_meta.update(
            {
                "model_key": model_key,
                "condition": condition,
                "seed": cell["seed"],
                "qualification_only": False,
                "primary_evidence": True,
                "num_ctx_context_limit": ms.get("num_ctx_context_limit"),
                "thinking_reasoning_setting": ms.get("thinking_reasoning_setting"),
            }
        )
    else:
        req_meta = {
            "model": cell["model"],
            "model_key": model_key,
            "condition": condition,
            "seed": cell["seed"],
            "temperature": ms["temperature"],
            "max_output_tokens": ms["max_output_tokens"],
            "timeout_seconds": ms["timeout_seconds"],
            "top_p": ms.get("top_p"),
            "top_k": ms.get("top_k"),
            "num_ctx_context_limit": ms.get("num_ctx_context_limit"),
            "thinking_reasoning_setting": ms.get("thinking_reasoning_setting"),
            "qualification_only": False,
            "primary_evidence": True,
            "parameter_authority": MATH16_MODEL_SETTINGS_REL,
        }
    atomic_write_json(cell_dir / "request_metadata.json", req_meta)

    started = datetime.now(timezone.utc).isoformat()
    t0 = time.monotonic()
    call = call_model_with_math16_retries(
        model_key=model_key, prompt=prompt, seed=int(cell["seed"]), settings=settings
    )
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
        if not (cell_dir / "extracted_source.py").exists():
            atomic_write_text(cell_dir / "extracted_source.py", "")
        artifact = {
            "experiment_id": CONDITIONS[condition]["experiment_id"],
            "cell_id": cell["cell_id"],
            "qualification_only": False,
            "primary_evidence": True,
            "model": cell["model"],
            "model_key": model_key,
            "task_id": cell["task_id"],
            "condition": condition,
            "seed": cell["seed"],
            "prompt_sha256": cell["prompt_sha256"],
            "scaffold_sha256": cell.get("scaffold_sha256"),
            "execution_freeze_commit": EXECUTION_FREEZE_COMMIT,
            "outcome": "transport_failure",
            "persisted_complete": True,
            "completed_at_utc": datetime.now(timezone.utc).isoformat(),
            "artifact_assembly": QFIX_001_ID,
            "healer": False,
            "parameter_authority": MATH16_MODEL_SETTINGS_REL,
        }
        return write_artifact_manifest(cell_dir, artifact)

    return assemble_cell_from_raw(
        condition=condition,
        cell=cell,
        cell_dir=cell_dir,
        raw=call["raw_text"],
        task=task,
    )


def run_model_condition(
    *,
    condition: str,
    model_key: str,
    execute_api: bool = False,
    dry_run: bool = False,
) -> dict[str, Any]:
    if model_key not in MODEL_ORDER:
        raise RuntimeError(f"unknown model_key: {model_key}")
    if condition not in CONDITIONS:
        raise RuntimeError(f"unknown condition: {condition}")
    if execute_api and dry_run:
        raise RuntimeError("execute_api and dry_run are mutually exclusive")
    if not execute_api and not dry_run:
        raise RuntimeError("specify dry_run=True or execute_api=True")

    cells = load_cell_manifest(condition, model_key=model_key)
    if len(cells) != 80:
        raise RuntimeError(f"expected 80 cells for {condition}/{model_key}, got {len(cells)}")
    for c in cells:
        verify_prompt_hash(condition, c)

    settings = load_math16_model_settings()
    tasks = tasks_by_id(ROOT)
    root = formal_root(condition, model_key)
    root.mkdir(parents=True, exist_ok=True)

    results = []
    model_calls = 0
    for cell in cells:
        if dry_run:
            results.append(
                execute_formal_cell(
                    condition=condition,
                    cell=cell,
                    tasks=tasks,
                    settings=settings,
                    dry_run=True,
                )
            )
            continue
        before_complete = cell_is_complete(root / cell["cell_id"])
        row = execute_formal_cell(
            condition=condition,
            cell=cell,
            tasks=tasks,
            settings=settings,
            dry_run=False,
        )
        if not row.get("skipped") and not before_complete:
            model_calls += 1
        results.append(row)

    summary = {
        "condition": condition,
        "model_key": model_key,
        "planned": 80,
        "results": len(results),
        "skipped_complete": sum(1 for r in results if r.get("skipped")),
        "dry_run": dry_run,
        "execute_api": execute_api,
        "model_calls": 0 if dry_run else model_calls,
        "parameter_authority": MATH16_MODEL_SETTINGS_REL,
        "completeness": completeness_report(condition, model_key),
    }
    atomic_write_json(root / "run_summary.json", summary)
    return summary


def zero_model_preflight_480() -> dict[str, Any]:
    rebuilt = {
        "ab2d_full": write_preregistration("ab2d_full"),
        "ab2d_domain_menu": write_preregistration("ab2d_domain_menu"),
    }
    plan = audit_cell_plan(both_conditions=True)
    dry_ok = True
    for condition in ("ab2d_domain_menu", "ab2d_full"):
        for model_key in MODEL_ORDER:
            cell = load_cell_manifest(condition, model_key=model_key)[0]
            row = execute_formal_cell(condition=condition, cell=cell, dry_run=True)
            dry_ok = dry_ok and row.get("model_calls") == 0
    settings = load_math16_model_settings()
    return {
        "preflight_id": "math16_ab2d_menu_vs_full_formal_execution_layer_v1",
        "execution_freeze_commit": EXECUTION_FREEZE_COMMIT,
        "parameter_authority": MATH16_MODEL_SETTINGS_REL,
        "rebuilt": rebuilt,
        "plan_audit": plan,
        "gemini_160_planned": plan["by_model"].get("gemini"),
        "qwen9b_160_planned": plan["by_model"].get("qwen_9b"),
        "qwen4b_160_planned": plan["by_model"].get("qwen_4b"),
        "dry_run_sample_ok": dry_ok,
        "model_settings_seed_list": settings["seed_list"],
        "model_calls": 0,
        "overall_pass": bool(plan["ok"]) and dry_ok and plan["total_cells"] == 480,
    }


def assert_prior_model_audit_passed(model_key: str) -> None:
    idx = MODEL_ORDER.index(model_key)
    if idx == 0:
        return
    prev = MODEL_ORDER[idx - 1]
    for condition in ("ab2d_domain_menu", "ab2d_full"):
        report = completeness_report(condition, prev)
        if not report["all_complete"]:
            raise RuntimeError(
                f"SEQUENTIAL_GATE_BLOCKED: {prev} incomplete for {condition}: "
                f"{report['complete']}/{report['planned']}"
            )
