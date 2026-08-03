# -*- coding: utf-8 -*-
"""Math16 Ab2d V2 formal execution layer (runtime-contract rewrite).

Independent of the V1 layer in ``math16_ab2d_formal_execution.py``.
- Prompts: ab2d_domain_menu_v2 / ab2d_full_v2 only
- Artifacts: artifacts/math16_ab2d_menu_vs_full_runtime_contract_v2/ only
- Scaffold SSOT: math16_ab2d_v2_scaffolds.TASK_SCAFFOLDS_V2
- Model settings / evaluator: same frozen Math16 authorities as V1 (read-only reuse)
Does not write into any V1 artifact or prompt path.
"""
from __future__ import annotations

import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from agent_tools.finals_rebuild.math16_ab2d_formal_execution import (
    MATH16_EVALUATOR_BINDING_REL,
    MATH16_GEMINI_RUNTIME_REL,
    MATH16_MODEL_SETTINGS_REL,
    MATH16_QWEN4B_RUNTIME_REL,
    MATH16_QWEN9B_RUNTIME_REL,
    MODEL_ORDER,
    MODELS,
    SEEDS,
    build_math16_gemini_request_metadata,
    call_model_with_math16_retries,
    load_math16_evaluator_binding,
    load_math16_model_settings,
)
from agent_tools.finals_rebuild.math16_ab2d_full_artifact_assembly import (
    QFIX_001_ID,
    atomic_write_json,
    atomic_write_text,
    build_evaluation_result,
    write_artifact_manifest,
    write_evaluation_artifacts,
)
from agent_tools.finals_rebuild.math16_ab2d_v2_scaffolds import TASK_SCAFFOLDS_V2
from agent_tools.finals_rebuild.math16_pool import load_pool_manifest, tasks_by_id

ROOT = Path(__file__).resolve().parents[2]

# V2 qualification gate commit (Gemini + Qwen 9B live qualification complete).
EXECUTION_FREEZE_COMMIT = "23309477c4f2967c4929965cf7c8d0466a38cc18"
EXPECTED_TASK_FREEZE = "349dfb2f786a4aa029453d844cac7eca07deb24a777ba1be4ef70f7002882e14"
EXPECTED_POOL_IDENTITY = "2ff41465d818d7e3d9b990a27ad2a1535e72c271bb04b2a37abe29cec1824636"

EXPERIMENT_ID = "math16_ab2d_menu_vs_full_runtime_contract_v2"
V2_ARTIFACT_ROOT = ROOT / "artifacts" / EXPERIMENT_ID
V2_FORMAL_ROOT = V2_ARTIFACT_ROOT / "formal"
V2_PREREG_ROOT = V2_ARTIFACT_ROOT / "preregistration"

MENU_PROMPT_DIR = ROOT / "docs/experiments/prompts/ab2d_domain_menu_v2/prompts"
FULL_PROMPT_DIR = ROOT / "docs/experiments/prompts/ab2d_full_v2/prompts"
MENU_MANIFEST = ROOT / "docs/experiments/prompts/ab2d_domain_menu_v2/manifest.json"
FULL_MANIFEST = ROOT / "docs/experiments/prompts/ab2d_full_v2/manifest.json"
V2_SHA_INVENTORY = (
    ROOT
    / "docs/experiments/results/Math16/math16_ab2d_menu_vs_full_runtime_contract_v2_sha256.json"
)
V2_SCAFFOLD_MODULE = ROOT / "agent_tools/finals_rebuild/math16_ab2d_v2_scaffolds.py"

# Fail-closed: never write these paths from this module.
V1_FORBIDDEN_WRITE_PREFIXES = (
    "artifacts/math16_ab2d_domain_menu_v1/",
    "artifacts/math16_ab2d_full_domain_assisted_v1/",
    "docs/experiments/prompts/ab2d_domain_menu/prompts/",
    "docs/experiments/prompts/ab2d_full/prompts/",
    "docs/experiments/prompts/ab2d_full/derived_scaffolds_v1.json",
)

CONDITIONS: dict[str, dict[str, Any]] = {
    "ab2d_domain_menu_v2": {
        "condition": "ab2d_domain_menu_v2",
        "experiment_id": EXPERIMENT_ID,
        "prompt_dir": MENU_PROMPT_DIR,
        "manifest_path": MENU_MANIFEST,
        "has_scaffold": False,
        "prompt_builder": (
            "agent_tools/finals_rebuild/math16_ab2d_domain_menu_v2.py::build_domain_menu_prompt_v2"
        ),
        "prompt_revision": "ab2d_domain_menu_runtime_contract_v2",
    },
    "ab2d_full_v2": {
        "condition": "ab2d_full_v2",
        "experiment_id": EXPERIMENT_ID,
        "prompt_dir": FULL_PROMPT_DIR,
        "manifest_path": FULL_MANIFEST,
        "has_scaffold": True,
        "prompt_builder": "agent_tools/finals_rebuild/math16_ab2d_full_v2.py::build_full_plan_prompt_v2",
        "prompt_revision": "ab2d_full_runtime_contract_v2",
        "scaffold_ssot": "agent_tools/finals_rebuild/math16_ab2d_v2_scaffolds.py::TASK_SCAFFOLDS_V2",
    },
}

CONDITION_ORDER = ["ab2d_domain_menu_v2", "ab2d_full_v2"]

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


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text_lf(text: str) -> str:
    return sha256_bytes(text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8"))


def sha256_prompt_file(path: Path) -> str:
    """Match V2 inventory convention: SHA of LF-normalized UTF-8 bytes."""
    return sha256_text_lf(path.read_text(encoding="utf-8"))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def cell_id(model_key: str, task_id: str, condition: str, seed: int) -> str:
    return f"{model_key}__{task_id}__{condition}__seed_{seed}"


def assert_path_is_v2_write_target(path: Path) -> None:
    rel = str(path.resolve()).replace("\\", "/")
    root = str(ROOT.resolve()).replace("\\", "/")
    if not rel.startswith(root):
        raise RuntimeError(f"path escapes repo: {path}")
    rel_in_repo = rel[len(root) :].lstrip("/")
    for bad in V1_FORBIDDEN_WRITE_PREFIXES:
        if rel_in_repo == bad.rstrip("/") or rel_in_repo.startswith(bad):
            raise RuntimeError(f"V2 layer refused write into V1 path: {rel_in_repo}")
    v2_root = str(V2_ARTIFACT_ROOT.resolve()).replace("\\", "/")
    if not rel.startswith(v2_root):
        raise RuntimeError(f"V2 formal write must stay under V2 artifact root: {path}")


def load_v2_sha_inventory() -> dict[str, str]:
    if not V2_SHA_INVENTORY.exists():
        raise RuntimeError(f"missing V2 SHA inventory: {V2_SHA_INVENTORY}")
    payload = load_json(V2_SHA_INVENTORY)
    out: dict[str, str] = {}
    for row in payload.get("entries") or []:
        if row.get("missing"):
            continue
        path = str(row["path"]).replace("\\", "/")
        out[path] = row["sha256"]
    return out


def v2_scaffold_ssot_sha() -> str:
    return sha256_text_lf(V2_SCAFFOLD_MODULE.read_text(encoding="utf-8"))


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


def verify_v2_scaffold_ssot() -> dict[str, Any]:
    missing = [tid for tid in load_pool_manifest(ROOT)["task_ids"] if tid not in TASK_SCAFFOLDS_V2]
    incomplete = [
        tid
        for tid, row in TASK_SCAFFOLDS_V2.items()
        if not isinstance(row.get("full_plan_body"), str) or not row["full_plan_body"].strip()
    ]
    # Absolute ban: must not reference V1 derived scaffolds file.
    forbidden = "docs/experiments/prompts/ab2d_full/derived_scaffolds_v1.json"
    module_src = V2_SCAFFOLD_MODULE.read_text(encoding="utf-8")
    if forbidden in module_src:
        raise RuntimeError("V2 scaffold SSOT unexpectedly references V1 derived_scaffolds")
    sha = v2_scaffold_ssot_sha()
    ok = not missing and not incomplete and len(TASK_SCAFFOLDS_V2) >= 16
    return {
        "ok": ok,
        "n_scaffolds": len(TASK_SCAFFOLDS_V2),
        "missing_task_ids": missing,
        "incomplete_task_ids": incomplete,
        "scaffold_ssot_sha256": sha,
        "scaffold_ssot": "agent_tools/finals_rebuild/math16_ab2d_v2_scaffolds.py::TASK_SCAFFOLDS_V2",
        "uses_v1_derived_scaffolds": False,
    }


def _manifest_sha_checks(condition: str) -> dict[str, Any]:
    cfg = CONDITIONS[condition]
    manifest = load_json(cfg["manifest_path"])
    if manifest.get("condition") != condition:
        raise RuntimeError(
            f"manifest condition mismatch: file has {manifest.get('condition')} expected {condition}"
        )
    if manifest.get("experiment_id") != EXPERIMENT_ID:
        raise RuntimeError(f"manifest experiment_id mismatch: {manifest.get('experiment_id')}")
    inventory = load_v2_sha_inventory()
    rows = []
    mismatches = []
    for task in manifest["tasks"]:
        tid = task["task_id"]
        rel_path = str(task["prompt_path"]).replace("\\", "/")
        path = ROOT / rel_path
        if path.parent.resolve() != cfg["prompt_dir"].resolve():
            raise RuntimeError(f"manifest path outside V2 prompt dir: {rel_path}")
        if not path.exists():
            raise RuntimeError(f"missing V2 prompt: {rel_path}")
        text = path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
        disk_sha = sha256_text_lf(text)
        char_count = len(text)
        inv_sha = inventory.get(rel_path)
        char_ok = task.get("char_count") is None or int(task["char_count"]) == char_count
        inv_ok = inv_sha is None or inv_sha == disk_sha
        # Prefer explicit SHA field if a future manifest adds it.
        man_sha = task.get("prompt_sha256") or task.get("exact_prompt_sha256")
        man_ok = man_sha is None or man_sha == disk_sha
        if not (char_ok and inv_ok and man_ok):
            mismatches.append(tid)
        rows.append(
            {
                "task_id": tid,
                "path": rel_path,
                "prompt_sha256": disk_sha,
                "char_count": char_count,
                "manifest_char_count": task.get("char_count"),
                "inventory_sha256": inv_sha,
                "manifest_sha256": man_sha,
                "match": char_ok and inv_ok and man_ok,
            }
        )
    if len(rows) != 16:
        raise RuntimeError(f"{condition}: expected 16 manifest tasks, got {len(rows)}")
    return {
        "condition": condition,
        "manifest_path": str(cfg["manifest_path"].relative_to(ROOT)).replace("\\", "/"),
        "n_tasks": len(rows),
        "all_match": len(mismatches) == 0,
        "mismatches": mismatches,
        "prompts": rows,
    }


def disk_prompt_sha_map(condition: str) -> dict[str, str]:
    prompt_dir: Path = CONDITIONS[condition]["prompt_dir"]
    out = {}
    for path in sorted(prompt_dir.glob("*.txt")):
        out[path.stem] = sha256_prompt_file(path)
    return out


def build_prompt_freeze(condition: str) -> dict[str, Any]:
    cfg = CONDITIONS[condition]
    pool = verify_pool_identity()
    if not pool["ok"]:
        raise RuntimeError(f"pool identity mismatch: {pool}")
    checks = _manifest_sha_checks(condition)
    if not checks["all_match"]:
        raise RuntimeError(f"V2 prompt SHA/manifest mismatch: {checks['mismatches']}")
    sha_map = {r["task_id"]: r["prompt_sha256"] for r in checks["prompts"]}
    disk = disk_prompt_sha_map(condition)
    for tid, sha in sha_map.items():
        if disk.get(tid) != sha:
            raise RuntimeError(f"disk/manifest prompt map drift: {tid}")
    for tid in pool["task_ids"]:
        if tid not in sha_map:
            raise RuntimeError(f"missing freeze row for pool task {tid}")
    scaffold = verify_v2_scaffold_ssot() if cfg["has_scaffold"] else None
    if cfg["has_scaffold"] and not scaffold["ok"]:
        raise RuntimeError(f"V2 scaffold SSOT incomplete: {scaffold}")
    rows = [
        {
            "task_id": tid,
            "path": str((cfg["prompt_dir"] / f"{tid}.txt").relative_to(ROOT)).replace("\\", "/"),
            "prompt_sha256": sha_map[tid],
        }
        for tid in pool["task_ids"]
    ]
    return {
        "prompt_revision": cfg["prompt_revision"],
        "condition": condition,
        "experiment_id": EXPERIMENT_ID,
        "execution_freeze_commit": EXECUTION_FREEZE_COMMIT,
        "prompt_builder": cfg["prompt_builder"],
        "manifest_path": str(cfg["manifest_path"].relative_to(ROOT)).replace("\\", "/"),
        "n_tasks": 16,
        "all_match_disk": True,
        "all_match_manifest": True,
        "line_endings": "LF",
        "sha_basis": "utf8_lf_normalized",
        "sha_inventory": str(V2_SHA_INVENTORY.relative_to(ROOT)).replace("\\", "/"),
        "scaffold": scaffold,
        "tasks": [{"task_id": r["task_id"], "prompt_sha256": r["prompt_sha256"]} for r in rows],
        "prompts": rows,
    }


def build_cell_manifest(
    condition: str, prompt_freeze: dict[str, Any] | None = None
) -> list[dict[str, Any]]:
    cfg = CONDITIONS[condition]
    prompt_freeze = prompt_freeze or build_prompt_freeze(condition)
    sha_by_task = {r["task_id"]: r["prompt_sha256"] for r in prompt_freeze["tasks"]}
    scaffold_sha = None
    if cfg["has_scaffold"]:
        scaffold_sha = (prompt_freeze.get("scaffold") or {}).get("scaffold_ssot_sha256")
        if not scaffold_sha:
            scaffold_sha = v2_scaffold_ssot_sha()
    cells: list[dict[str, Any]] = []
    for model in MODELS:
        for tid, prompt_sha in sha_by_task.items():
            for seed in SEEDS:
                row: dict[str, Any] = {
                    "cell_id": cell_id(model["model_key"], tid, condition, seed),
                    "experiment_id": EXPERIMENT_ID,
                    "model": model["model_id"],
                    "model_key": model["model_key"],
                    "task_id": tid,
                    "condition": condition,
                    "seed": seed,
                    "prompt_sha256": prompt_sha,
                    "execution_freeze_commit": EXECUTION_FREEZE_COMMIT,
                }
                if scaffold_sha is not None:
                    row["scaffold_ssot_sha256"] = scaffold_sha
                    row["scaffold_ssot"] = cfg["scaffold_ssot"]
                cells.append(row)
    if len(cells) != 240:
        raise RuntimeError(f"expected 240 cells for {condition}, got {len(cells)}")
    return cells


def write_preregistration(condition: str) -> dict[str, Any]:
    if condition not in CONDITIONS:
        raise RuntimeError(f"unknown V2 condition: {condition}")
    assert_path_is_v2_write_target(V2_PREREG_ROOT / "probe")
    V2_PREREG_ROOT.mkdir(parents=True, exist_ok=True)
    for model_key in MODEL_ORDER:
        for cond in CONDITION_ORDER:
            path = formal_root(cond, model_key)
            assert_path_is_v2_write_target(path)
            path.mkdir(parents=True, exist_ok=True)

    prompt_freeze = build_prompt_freeze(condition)
    cells = build_cell_manifest(condition, prompt_freeze)
    model_settings = load_math16_model_settings()
    evaluator_binding = load_math16_evaluator_binding()

    # Write condition-specific freeze under preregistration/{condition}/
    cond_dir = V2_PREREG_ROOT / condition
    assert_path_is_v2_write_target(cond_dir)
    cond_dir.mkdir(parents=True, exist_ok=True)

    execution_policy = {
        "model_order": MODEL_ORDER,
        "rationale": (
            "Hard sequential gate: Gemini integrity audit must pass before Qwen 9B; "
            "Qwen 9B audit must pass before Qwen 4B. No parallel/interleaved runs."
        ),
        "seed_list": SEEDS,
        "cells_per_model_per_condition": 80,
        "cells_per_condition": 240,
        "conditions": list(CONDITION_ORDER),
        "total_formal_cells_both_conditions": 480,
        "parameter_authority": MATH16_MODEL_SETTINGS_REL,
        "math16_runtime_evidence": {
            "gemini": MATH16_GEMINI_RUNTIME_REL,
            "qwen_9b": MATH16_QWEN9B_RUNTIME_REL,
            "qwen_4b": MATH16_QWEN4B_RUNTIME_REL,
        },
        "prompt_roots": {
            "ab2d_domain_menu_v2": "docs/experiments/prompts/ab2d_domain_menu_v2/prompts",
            "ab2d_full_v2": "docs/experiments/prompts/ab2d_full_v2/prompts",
        },
        "artifact_root": str(V2_ARTIFACT_ROOT).replace("\\", "/"),
        "formal_root_pattern": (
            f"artifacts/{EXPERIMENT_ID}/formal/{{model_key}}/{{condition}}/{{cell_id}}/"
        ),
        "cell_failure_policy": "continue; do not abort the full run on a single cell failure",
        "retry_scope": (
            "transport/runtime only per Math16 model_settings.retry_policy; "
            "never retry answer_incorrect / completed cells"
        ),
        "resume_policy": "never re-run completed cells; resume remaining pending cells only",
        "healer": False,
        "forbids_v1_artifact_writes": True,
    }
    experiment_identity = {
        "experiment_id": EXPERIMENT_ID,
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
        "scaffold_ssot": (
            "agent_tools/finals_rebuild/math16_ab2d_v2_scaffolds.py::TASK_SCAFFOLDS_V2"
            if CONDITIONS[condition]["has_scaffold"]
            else None
        ),
        "artifact_root": str(V2_ARTIFACT_ROOT).replace("\\", "/"),
        "model_settings_source": MATH16_MODEL_SETTINGS_REL,
        "evaluator_binding_source": MATH16_EVALUATOR_BINDING_REL,
    }

    atomic_write_json(cond_dir / "prompt_freeze.json", prompt_freeze)
    (cond_dir / "cell_manifest.jsonl").write_text(
        "".join(json.dumps(c, ensure_ascii=False, sort_keys=True) + "\n" for c in cells),
        encoding="utf-8",
        newline="\n",
    )
    # Shared copies used by both conditions (authority unchanged from Math16 freeze).
    atomic_write_json(V2_PREREG_ROOT / "model_settings.json", model_settings)
    atomic_write_json(V2_PREREG_ROOT / "evaluator_binding.json", evaluator_binding)
    atomic_write_json(V2_PREREG_ROOT / "execution_policy.json", execution_policy)
    atomic_write_json(cond_dir / "experiment_identity.json", experiment_identity)
    return {
        "condition": condition,
        "n_cells": len(cells),
        "n_prompts": prompt_freeze["n_tasks"],
        "preregistration": str(cond_dir).replace("\\", "/"),
        "artifact_root": str(V2_ARTIFACT_ROOT).replace("\\", "/"),
    }


def load_cell_manifest(condition: str, *, model_key: str | None = None) -> list[dict[str, Any]]:
    path = V2_PREREG_ROOT / condition / "cell_manifest.jsonl"
    if not path.exists():
        raise RuntimeError(f"missing V2 cell_manifest for {condition}: {path}")
    cells = [
        json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()
    ]
    if model_key is not None:
        cells = [c for c in cells if c["model_key"] == model_key]
    return cells


def formal_root(condition: str, model_key: str) -> Path:
    return V2_FORMAL_ROOT / model_key / condition


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
    disk_sha = sha256_prompt_file(path)
    if disk_sha != cell["prompt_sha256"]:
        raise RuntimeError(
            f"prompt hash drift: {cell['task_id']} cell={cell['prompt_sha256']} disk={disk_sha}"
        )
    return disk_sha


def audit_cell_plan(*, both_conditions: bool = True) -> dict[str, Any]:
    conditions = list(CONDITION_ORDER) if both_conditions else list(CONDITIONS)
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
    formal_paths = {
        "artifact_root": str(V2_ARTIFACT_ROOT.relative_to(ROOT)).replace("\\", "/"),
        "formal_root": str(V2_FORMAL_ROOT.relative_to(ROOT)).replace("\\", "/"),
        "prompt_dirs": {
            "ab2d_domain_menu_v2": "docs/experiments/prompts/ab2d_domain_menu_v2/prompts",
            "ab2d_full_v2": "docs/experiments/prompts/ab2d_full_v2/prompts",
        },
    }
    return {
        "total_cells": len(all_ids),
        "unique_cells": unique,
        "duplicate": len(all_ids) - unique,
        "missing": max(0, expected - unique),
        "by_model": by_model,
        "by_condition": by_condition,
        "sha_mismatches": sha_mismatches,
        "v2_paths": formal_paths,
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
        "formal_root": str(root.relative_to(ROOT)).replace("\\", "/"),
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
        "experiment_id": EXPERIMENT_ID,
        "cell_id": cell["cell_id"],
        "qualification_only": False,
        "primary_evidence": True,
        "model": cell["model"],
        "model_key": cell["model_key"],
        "task_id": cell["task_id"],
        "condition": condition,
        "seed": cell["seed"],
        "prompt_sha256": cell["prompt_sha256"],
        "scaffold_ssot_sha256": cell.get("scaffold_ssot_sha256"),
        "execution_freeze_commit": EXECUTION_FREEZE_COMMIT,
        "outcome": outcome,
        "persisted_complete": True,
        "completed_at_utc": datetime.now(timezone.utc).isoformat(),
        "artifact_assembly": QFIX_001_ID,
        "healer": False,
        "parameter_authority": MATH16_MODEL_SETTINGS_REL,
        "namespace": "v2",
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
    if condition not in CONDITIONS:
        raise RuntimeError(f"unknown V2 condition: {condition}")
    tasks = tasks or tasks_by_id(ROOT)
    settings = settings or load_math16_model_settings()
    model_key = cell["model_key"]
    root = formal_root(condition, model_key)
    assert_path_is_v2_write_target(root)
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
            "prompt_dir": str(CONDITIONS[condition]["prompt_dir"].relative_to(ROOT)).replace(
                "\\", "/"
            ),
            "formal_root": str(root.relative_to(ROOT)).replace("\\", "/"),
            "model_calls": 0,
            "parameter_authority": MATH16_MODEL_SETTINGS_REL,
        }

    # Live path kept for completeness; orchestrator/tests must not invoke execute_api.
    task = tasks[cell["task_id"]]
    prompt_path = CONDITIONS[condition]["prompt_dir"] / f"{cell['task_id']}.txt"
    prompt = prompt_path.read_text(encoding="utf-8")
    assert_path_is_v2_write_target(cell_dir)
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
                "experiment_id": EXPERIMENT_ID,
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
            "experiment_id": EXPERIMENT_ID,
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
            "experiment_id": EXPERIMENT_ID,
            "cell_id": cell["cell_id"],
            "qualification_only": False,
            "primary_evidence": True,
            "model": cell["model"],
            "model_key": model_key,
            "task_id": cell["task_id"],
            "condition": condition,
            "seed": cell["seed"],
            "prompt_sha256": cell["prompt_sha256"],
            "scaffold_ssot_sha256": cell.get("scaffold_ssot_sha256"),
            "execution_freeze_commit": EXECUTION_FREEZE_COMMIT,
            "outcome": "transport_failure",
            "persisted_complete": True,
            "completed_at_utc": datetime.now(timezone.utc).isoformat(),
            "artifact_assembly": QFIX_001_ID,
            "healer": False,
            "parameter_authority": MATH16_MODEL_SETTINGS_REL,
            "namespace": "v2",
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
        raise RuntimeError(f"unknown V2 condition: {condition}")
    if execute_api and dry_run:
        raise RuntimeError("execute_api and dry_run are mutually exclusive")
    if not execute_api and not dry_run:
        raise RuntimeError("specify dry_run=True or execute_api=True")

    cells = load_cell_manifest(condition, model_key=model_key)
    if len(cells) != 80:
        raise RuntimeError(f"expected 80 cells for {condition}/{model_key}, got {len(cells)}")
    for c in cells:
        verify_prompt_hash(condition, c)
        # Cell namespace must be V2 condition string.
        if c["condition"] != condition or c["experiment_id"] != EXPERIMENT_ID:
            raise RuntimeError(f"cell metadata not V2: {c['cell_id']}")

    settings = load_math16_model_settings()
    tasks = tasks_by_id(ROOT)
    root = formal_root(condition, model_key)
    assert_path_is_v2_write_target(root)
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
        "prompt_dir": str(CONDITIONS[condition]["prompt_dir"].relative_to(ROOT)).replace(
            "\\", "/"
        ),
        "formal_root": str(root.relative_to(ROOT)).replace("\\", "/"),
        "experiment_id": EXPERIMENT_ID,
        "completeness": completeness_report(condition, model_key),
    }
    assert_path_is_v2_write_target(root / "run_summary.json")
    atomic_write_json(root / "run_summary.json", summary)
    return summary


def zero_model_preflight_480() -> dict[str, Any]:
    rebuilt = {
        "ab2d_domain_menu_v2": write_preregistration("ab2d_domain_menu_v2"),
        "ab2d_full_v2": write_preregistration("ab2d_full_v2"),
    }
    plan = audit_cell_plan(both_conditions=True)
    dry_ok = True
    dry_rows = []
    for condition in CONDITION_ORDER:
        for model_key in MODEL_ORDER:
            cell = load_cell_manifest(condition, model_key=model_key)[0]
            row = execute_formal_cell(condition=condition, cell=cell, dry_run=True)
            dry_ok = dry_ok and row.get("model_calls") == 0
            dry_rows.append(
                {
                    "condition": condition,
                    "model_key": model_key,
                    "prompt_dir": row.get("prompt_dir"),
                    "formal_root": row.get("formal_root"),
                    "model_calls": row.get("model_calls"),
                }
            )
    settings = load_math16_model_settings()
    n_prompts = sum(len(list(CONDITIONS[c]["prompt_dir"].glob("*.txt"))) for c in CONDITION_ORDER)
    v1_touch_guards = {
        "forbids_v1_paths": True,
        "forbidden_prefixes": list(V1_FORBIDDEN_WRITE_PREFIXES),
        "v2_artifact_root_only": str(V2_ARTIFACT_ROOT.relative_to(ROOT)).replace("\\", "/"),
    }
    # Explicit SHA inventory check for all 32 prompts.
    inv = load_v2_sha_inventory()
    inv_mismatches = []
    for condition in CONDITION_ORDER:
        for path in sorted(CONDITIONS[condition]["prompt_dir"].glob("*.txt")):
            rel = str(path.relative_to(ROOT)).replace("\\", "/")
            disk = sha256_prompt_file(path)
            if inv.get(rel) != disk:
                inv_mismatches.append(rel)
    overall = (
        bool(plan["ok"])
        and dry_ok
        and plan["total_cells"] == 480
        and n_prompts == 32
        and not inv_mismatches
        and plan["model_calls"] == 0
    )
    return {
        "preflight_id": "math16_ab2d_menu_vs_full_formal_execution_layer_v2",
        "execution_freeze_commit": EXECUTION_FREEZE_COMMIT,
        "experiment_id": EXPERIMENT_ID,
        "parameter_authority": MATH16_MODEL_SETTINGS_REL,
        "rebuilt": rebuilt,
        "plan_audit": plan,
        "n_v2_prompts": n_prompts,
        "sha_inventory_mismatches": inv_mismatches,
        "gemini_160_planned": plan["by_model"].get("gemini"),
        "qwen9b_160_planned": plan["by_model"].get("qwen_9b"),
        "qwen4b_160_planned": plan["by_model"].get("qwen_4b"),
        "dry_run_sample_ok": dry_ok,
        "dry_run_samples": dry_rows,
        "model_settings_seed_list": settings["seed_list"],
        "model_calls": 0,
        "v1_write_guards": v1_touch_guards,
        "scaffold_ssot": verify_v2_scaffold_ssot(),
        "overall_pass": overall,
    }


def assert_prior_model_audit_passed(model_key: str) -> None:
    idx = MODEL_ORDER.index(model_key)
    if idx == 0:
        return
    prev = MODEL_ORDER[idx - 1]
    for condition in CONDITION_ORDER:
        report = completeness_report(condition, prev)
        if not report["all_complete"]:
            raise RuntimeError(
                f"SEQUENTIAL_GATE_BLOCKED: {prev} incomplete for {condition}: "
                f"{report['complete']}/{report['planned']}"
            )


def runner_path_inventory() -> list[dict[str, str]]:
    """Six formal runners: prompt path + artifact root mapping."""
    rows = []
    for condition in CONDITION_ORDER:
        for model_key in MODEL_ORDER:
            rows.append(
                {
                    "condition": condition,
                    "model_key": model_key,
                    "prompt_dir": str(
                        CONDITIONS[condition]["prompt_dir"].relative_to(ROOT)
                    ).replace("\\", "/"),
                    "formal_root": str(formal_root(condition, model_key).relative_to(ROOT)).replace(
                        "\\", "/"
                    ),
                    "artifact_experiment_root": str(V2_ARTIFACT_ROOT.relative_to(ROOT)).replace(
                        "\\", "/"
                    ),
                }
            )
    return rows
