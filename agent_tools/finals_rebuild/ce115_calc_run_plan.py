"""Zero-model planning layer for CE115 local confirmatory 72 cells.

Reads the frozen main-experiment manifest, expands local confirmatory cells,
rebuilds prompts from freeze assemblers, and validates integrity — no model calls.
"""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any, Mapping

from agent_tools.finals_rebuild.ab2d_local_prompt import MATH_CORE_SCAFFOLD
from agent_tools.finals_rebuild.ce115_calc_prompt_freeze import (
    FORMAL_CONDITIONS,
    FORMAL_SEEDS,
    assert_no_leakage,
    build_condition_prompt,
    file_sha256,
    prompt_sha256,
    render_calc_task_contract,
)
from agent_tools.finals_rebuild.ce115_calc_golden_generators import FORMAL_L1_TASK_IDS, formal_l1_tasks
from agent_tools.finals_rebuild.math_task_sampler import sample_task_parameters

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MANIFEST_REL = Path("docs/experiments/manifests/ce115_calc_main_experiment_manifest.json")
FORMAL_RESULTS_DIR = Path("docs/experiments/results/ce115_calc_local_confirmatory")
LEGACY_TASK_PREFIXES = ("ce115_cr01_",)

# Manifest values that must NEVER be filled with concrete generation numbers.
UNSET_SENTINELS = frozenset({"not_explicitly_set", "runtime_default", "unavailable"})

REQUIRED_CELL_KEYS = (
    "cell_id",
    "task_id",
    "prompt_condition",
    "seed",
    "model_tag",
    "model_digest",
    "prompt_text",
    "prompt_hash",
    "temperature",
    "top_p",
    "top_k",
    "num_predict",
    "thinking_requested",
    "request_count",
    "retry_count",
    "healer_enabled",
    "ledger_stage",
    "output_path",
    "included_in_formal_analysis",
)

REQUIRED_PLANNED_RECORD_KEYS = (
    "task_id",
    "condition",
    "seed",
    "model_tag",
    "model_digest",
    "prompt_hash",
    "request_settings",
    "request_count",
    "retry_count",
    "first_attempt_is_ITT",
    "healer_enabled",
    "ledger_stage",
    "raw_first_attempt_output",
    "candidate_extracted",
    "actual_question_text",
    "evaluation_gates",
    "composite_outcomes",
    "token_duration_diagnostics",
    "commit_hash",
    "manifest_hash",
)

MODEL_SLUGS = {
    "qwen3.5:4b": "qwen3_5_4b",
    "qwen3.5:9b": "qwen3_5_9b",
}
CONFIRMATORY_MODEL_KEYS = ("qwen35_4b", "qwen35_9b")
HISTORICAL_MODEL_TAGS = frozenset(
    {
        "qwen3:4b-instruct-2507-q4_K_M",
        "qwen3:8b",
        "qwen3:4b",
    }
)


class PreflightError(ValueError):
    """Blocking preflight integrity failure."""


def load_manifest(path: Path | str | None = None) -> dict[str, Any]:
    manifest_path = Path(path) if path is not None else REPO_ROOT / DEFAULT_MANIFEST_REL
    if not manifest_path.is_file():
        raise PreflightError(f"manifest missing: {manifest_path}")
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not data.get("local_confirmatory_frozen"):
        raise PreflightError("manifest local_confirmatory_frozen is not true")
    if int(data.get("cell_counts", {}).get("confirmatory_local_cell_count", -1)) != 72:
        raise PreflightError("manifest confirmatory_local_cell_count must be 72")
    return data


def manifest_sha256(path: Path | str | None = None) -> str:
    manifest_path = Path(path) if path is not None else REPO_ROOT / DEFAULT_MANIFEST_REL
    return file_sha256(manifest_path)


def short_git_sha(git_commit: str) -> str:
    return git_commit[:12]


def model_slug(model_tag: str) -> str:
    if model_tag not in MODEL_SLUGS:
        raise PreflightError(f"unsupported confirmatory model_tag: {model_tag!r}")
    return MODEL_SLUGS[model_tag]


def cell_id_for(*, model_tag: str, task_id: str, condition: str, seed: int) -> str:
    return f"{model_slug(model_tag)}__{task_id}__{condition}__seed_{seed}"


def output_path_for(
    *,
    model_tag: str,
    task_id: str,
    condition: str,
    seed: int,
    git_commit: str,
) -> str:
    """Deterministic formal local-confirmatory path including task_id for uniqueness."""
    cid = cell_id_for(model_tag=model_tag, task_id=task_id, condition=condition, seed=seed)
    name = f"{cid}_git_{short_git_sha(git_commit)}.jsonl"
    return str(FORMAL_RESULTS_DIR / name).replace("\\", "/")


def local_confirmatory_models(manifest: Mapping[str, Any]) -> list[dict[str, Any]]:
    models = manifest["models"]
    out = []
    for key in CONFIRMATORY_MODEL_KEYS:
        if key not in models:
            raise PreflightError(f"missing confirmatory model key: {key}")
        entry = models[key]
        if not entry.get("included_in_formal_confirmatory_analysis", True):
            raise PreflightError(f"{key} must be included in confirmatory analysis")
        if entry.get("cohort_role") != "local_confirmatory":
            raise PreflightError(f"{key} cohort_role must be local_confirmatory")
        tag = entry["model_tag"]
        if tag in HISTORICAL_MODEL_TAGS:
            raise PreflightError(f"historical model leaked into confirmatory plan: {tag}")
        if not tag.startswith("qwen3.5:"):
            raise PreflightError(f"confirmatory model must be qwen3.5:*; got {tag}")
        out.append(
            {
                "registry_key": key,
                "model_tag": tag,
                "model_digest": entry.get("model_digest") or entry["digest"],
                "sampling": entry["sampling"],
                "thinking": entry["thinking"],
            }
        )
    if any("gemini" in m["model_tag"].lower() for m in out):
        raise PreflightError("Gemini must not appear in confirmatory local models")
    if len(out) != 2:
        raise PreflightError(f"expected 2 confirmatory models, got {len(out)}")
    return out


def sampling_field(sampling: Mapping[str, Any], name: str) -> Any:
    if name not in sampling:
        raise PreflightError(f"sampling missing declared field: {name}")
    return sampling[name]


def build_request_options_from_manifest(
    sampling: Mapping[str, Any],
    *,
    seed: int,
    thinking: Mapping[str, Any],
) -> dict[str, Any]:
    """Runner-ready options/plan fields. Unset sentinels stay as sentinels — no numeric fill-in."""
    options: dict[str, Any] = {
        "temperature": sampling_field(sampling, "temperature"),
        "seed": seed,
    }
    for name in ("top_p", "top_k", "presence_penalty", "num_predict"):
        value = sampling_field(sampling, name)
        options[name] = value  # may be not_explicitly_set
    thinking_requested = thinking.get("requested", thinking.get("thinking_requested", "not_explicitly_set"))
    options["thinking_requested"] = thinking_requested
    # Formal Qwen3.5 policy: explicit top-level think=false (stored here for plan cells).
    if thinking_requested is False or sampling.get("think") is False:
        options["think"] = False
    return options


def assert_request_matches_manifest(
    options: Mapping[str, Any],
    sampling: Mapping[str, Any],
    thinking: Mapping[str, Any],
) -> list[str]:
    mismatches: list[str] = []
    if options.get("temperature") != sampling.get("temperature"):
        mismatches.append("temperature")
    for name in ("top_p", "top_k", "presence_penalty", "num_predict"):
        declared = sampling.get(name)
        actual = options.get(name)
        if declared in UNSET_SENTINELS:
            if actual not in UNSET_SENTINELS:
                mismatches.append(f"{name}_filled_against_not_explicitly_set")
        elif actual != declared:
            mismatches.append(name)
    allowed = {
        "temperature",
        "seed",
        "top_p",
        "top_k",
        "presence_penalty",
        "num_predict",
        "thinking_requested",
        "think",
    }
    undeclared = sorted(set(options) - allowed)
    for key in undeclared:
        mismatches.append(f"undeclared_option:{key}")
    requested = thinking.get("requested", thinking.get("thinking_requested", "not_explicitly_set"))
    if options.get("thinking_requested") != requested:
        mismatches.append("thinking_requested")
    if requested is False:
        if options.get("think") is not False:
            mismatches.append("think_not_false")
    if requested is True:
        mismatches.append("thinking_enabled_forbidden_for_confirmatory")
    if requested in UNSET_SENTINELS and options.get("think") is True:
        mismatches.append("think_auto_enabled")
    if requested in UNSET_SENTINELS and options.get("thinking") is True:
        mismatches.append("thinking_auto_enabled")
    # Observed defaults must never appear as numeric overrides in the plan options.
    defaults = sampling.get("observed_model_defaults") or {}
    for name, default_value in defaults.items():
        if name in ("top_p", "top_k", "presence_penalty") and options.get(name) == default_value:
            mismatches.append(f"model_default_leaked_into_request:{name}")
    return mismatches


def rebuild_prompt(*, task: Mapping[str, Any], condition: str, seed: int) -> tuple[str, str]:
    payload = sample_task_parameters(task, seed)["oracle_payload"]
    text = build_condition_prompt(condition, task, payload)
    assert_no_leakage(text)
    return text, prompt_sha256(text)


def validate_prompt_condition_shape(condition: str, prompt: str, skill_id: str) -> None:
    if condition == "ab1":
        if MATH_CORE_SCAFFOLD in prompt:
            raise PreflightError("Ab1 must not contain Math Core scaffold")
        if "## Task-local domain primitive:" in prompt:
            raise PreflightError("Ab1 must not contain task-local primitive")
    elif condition == "ab2g":
        if not prompt.startswith(MATH_CORE_SCAFFOLD):
            raise PreflightError("Ab2g must start with Math Core scaffold")
        if "## Task-local domain primitive:" in prompt:
            raise PreflightError("Ab2g must not contain task-local primitive")
    elif condition == "ab2d":
        if not prompt.startswith(MATH_CORE_SCAFFOLD):
            raise PreflightError("Ab2d must start with Math Core scaffold")
        if f"## Task-local domain primitive: {skill_id}" not in prompt:
            raise PreflightError(f"Ab2d missing primitive for {skill_id}")
    else:
        raise PreflightError(f"unknown condition: {condition}")
    if "## Task contract" not in prompt or "## Frozen parameters" not in prompt:
        raise PreflightError("prompt missing contract/frozen sections")
    for token in ("qwen", "gemini", "ollama"):
        if token in prompt.lower():
            raise PreflightError(f"model identity leaked into prompt: {token}")


def build_planned_record_skeleton(cell: Mapping[str, Any], *, commit_hash: str, manifest_hash: str) -> dict[str, Any]:
    """Schema contract for a future observed ledger row — no fabricated model output."""
    record = {
        "task_id": cell["task_id"],
        "condition": cell["prompt_condition"],
        "seed": cell["seed"],
        "model_tag": cell["model_tag"],
        "model_digest": cell["model_digest"],
        "prompt_hash": cell["prompt_hash"],
        "request_settings": cell["request_options"],
        "request_count": cell["request_count"],
        "retry_count": cell["retry_count"],
        "first_attempt_is_ITT": True,
        "healer_enabled": cell["healer_enabled"],
        "ledger_stage": "observed",
        "raw_first_attempt_output": None,
        "candidate_extracted": None,
        "actual_question_text": None,
        "evaluation_gates": None,
        "composite_outcomes": None,
        "token_duration_diagnostics": None,
        "commit_hash": commit_hash,
        "manifest_hash": manifest_hash,
        "included_in_formal_analysis": cell["included_in_formal_analysis"],
        "cell_id": cell["cell_id"],
        "output_path": cell["output_path"],
        "observation_status": "experiment_not_run",
    }
    missing = [key for key in REQUIRED_PLANNED_RECORD_KEYS if key not in record]
    if missing:
        raise PreflightError(f"planned record missing keys: {missing}")
    return record


def expand_local_confirmatory_cells(
    manifest: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> list[dict[str, Any]]:
    root = repo_root or REPO_ROOT
    if not manifest.get("local_confirmatory_frozen"):
        raise PreflightError("refusing to expand: local_confirmatory_frozen is false")

    tasks = formal_l1_tasks()
    task_ids = list(manifest["formal_task_ids"])
    conditions = list(manifest["prompt_conditions"])
    seeds = list(manifest["seeds"]["formal_seeds"])
    git_commit = str(manifest["git_commit"])
    hash_seed = int(manifest.get("prompt_hash_seed", FORMAL_SEEDS[0]))
    frozen_hashes = manifest["per_task_prompt_hashes"]
    models = local_confirmatory_models(manifest)

    if tuple(task_ids) != tuple(FORMAL_L1_TASK_IDS):
        raise PreflightError("manifest formal_task_ids drift from FORMAL_L1_TASK_IDS")
    if tuple(conditions) != tuple(FORMAL_CONDITIONS):
        raise PreflightError("manifest prompt_conditions drift from FORMAL_CONDITIONS")
    if tuple(seeds) != tuple(FORMAL_SEEDS):
        raise PreflightError("manifest formal_seeds drift from FORMAL_SEEDS")

    cells: list[dict[str, Any]] = []
    for model in models:
        sampling = model["sampling"]
        thinking = model["thinking"]
        for task_id in task_ids:
            if any(task_id.startswith(prefix) for prefix in LEGACY_TASK_PREFIXES):
                raise PreflightError(f"legacy task id in expansion: {task_id}")
            task = tasks[task_id]
            contract_hash = prompt_sha256(render_calc_task_contract(task))
            expected_contract = manifest["task_contract_hashes"][task_id]
            if contract_hash != expected_contract:
                raise PreflightError(f"task contract hash mismatch: {task_id}")
            for condition in conditions:
                for seed in seeds:
                    prompt_text, prompt_hash = rebuild_prompt(task=task, condition=condition, seed=seed)
                    validate_prompt_condition_shape(condition, prompt_text, task["skill_id"])
                    if seed == hash_seed:
                        expected = frozen_hashes[task_id][condition]
                        if prompt_hash != expected:
                            raise PreflightError(
                                f"prompt hash mismatch {task_id}/{condition}/seed_{seed}: "
                                f"{prompt_hash} != {expected}"
                            )
                    options = build_request_options_from_manifest(sampling, seed=seed, thinking=thinking)
                    mismatches = assert_request_matches_manifest(options, sampling, thinking)
                    if mismatches:
                        raise PreflightError(
                            f"request setting mismatches for {model['model_tag']}: {mismatches}"
                        )
                    cid = cell_id_for(
                        model_tag=model["model_tag"],
                        task_id=task_id,
                        condition=condition,
                        seed=seed,
                    )
                    out_rel = output_path_for(
                        model_tag=model["model_tag"],
                        task_id=task_id,
                        condition=condition,
                        seed=seed,
                        git_commit=git_commit,
                    )
                    cell = {
                        "cell_id": cid,
                        "task_id": task_id,
                        "prompt_condition": condition,
                        "seed": seed,
                        "model_tag": model["model_tag"],
                        "model_digest": model["model_digest"],
                        "model_registry_key": model["registry_key"],
                        "prompt_text": prompt_text,
                        "prompt_hash": prompt_hash,
                        "prompt_hash_validated_against_manifest_table": seed == hash_seed,
                        "temperature": options["temperature"],
                        "top_p": options["top_p"],
                        "top_k": options["top_k"],
                        "presence_penalty": options["presence_penalty"],
                        "num_predict": options["num_predict"],
                        "thinking_requested": options["thinking_requested"],
                        "think": options.get("think", False),
                        "request_options": options,
                        "request_count": int(manifest["request_count"]),
                        "retry_count": int(manifest["retry_count"]),
                        "healer_enabled": bool(manifest["healer_enabled"]),
                        "ledger_stage": "observed",
                        "output_path": out_rel,
                        "output_path_abs": str((root / out_rel).resolve()),
                        "included_in_formal_analysis": True,
                    }
                    missing = [key for key in REQUIRED_CELL_KEYS if key not in cell]
                    if missing:
                        raise PreflightError(f"cell missing keys: {missing}")
                    cells.append(cell)
    return cells


def assert_cell_distribution(cells: list[dict[str, Any]]) -> None:
    ids = [c["cell_id"] for c in cells]
    if len(set(ids)) != len(ids):
        raise PreflightError("duplicate cell_id")
    combos = [(c["task_id"], c["prompt_condition"], c["seed"], c["model_tag"]) for c in cells]
    if len(set(combos)) != len(combos):
        raise PreflightError("duplicate task×condition×seed×model")
    paths = [c["output_path"] for c in cells]
    if len(set(paths)) != len(paths):
        raise PreflightError("duplicate output_path")
    if len(cells) != 72:
        raise PreflightError(f"expected 72 cells, got {len(cells)}")
    if any("gemini" in c["model_tag"].lower() for c in cells):
        raise PreflightError("Gemini cell leaked into local confirmatory plan")
    if any(c["model_tag"] in HISTORICAL_MODEL_TAGS for c in cells):
        raise PreflightError("historical Qwen3 model leaked into confirmatory plan")
    if any(not c["cell_id"].startswith(("qwen3_5_4b__", "qwen3_5_9b__")) for c in cells):
        raise PreflightError("cell_id must use qwen3_5_4b / qwen3_5_9b slugs")
    if any(c["task_id"].startswith("ce115_cr01_") for c in cells):
        raise PreflightError("legacy task leaked into plan")
    if any(c.get("thinking_requested") is not False or c.get("think") is not False for c in cells):
        raise PreflightError("every confirmatory cell must have think=false")

    task_counts = Counter(c["task_id"] for c in cells)
    cond_counts = Counter(c["prompt_condition"] for c in cells)
    seed_counts = Counter(c["seed"] for c in cells)
    model_counts = Counter(c["model_tag"] for c in cells)
    for task_id in FORMAL_L1_TASK_IDS:
        if task_counts[task_id] != 18:
            raise PreflightError(f"{task_id} count {task_counts[task_id]} != 18")
    for condition in FORMAL_CONDITIONS:
        if cond_counts[condition] != 24:
            raise PreflightError(f"{condition} count {cond_counts[condition]} != 24")
    for seed in FORMAL_SEEDS:
        if seed_counts[seed] != 24:
            raise PreflightError(f"seed {seed} count {seed_counts[seed]} != 24")
    for tag, count in model_counts.items():
        if count != 36:
            raise PreflightError(f"model {tag} count {count} != 36")


def assert_cross_model_prompt_identity(cells: list[dict[str, Any]]) -> None:
    by_key: dict[tuple[str, str, int], dict[str, str]] = {}
    for cell in cells:
        key = (cell["task_id"], cell["prompt_condition"], cell["seed"])
        by_key.setdefault(key, {})[cell["model_tag"]] = cell["prompt_text"]
    for key, prompts in by_key.items():
        if len(prompts) != 2:
            raise PreflightError(f"expected 2 models for {key}, got {len(prompts)}")
        texts = list(prompts.values())
        if texts[0] != texts[1]:
            raise PreflightError(f"4B/8B prompt bytes differ for {key}")


def assert_output_path_safety(cells: list[dict[str, Any]], *, repo_root: Path | None = None) -> list[str]:
    """Validate path determinism and record existing non-empty artifacts.

    Existing artifacts are returned as blockers (not a hard raise) so resume /
    post-smoke plan loads remain possible. Per-cell write still refuse-overwrite
    via write_executed_record / assert_output_writable.
    """
    root = (repo_root or REPO_ROOT).resolve()
    blockers: list[str] = []
    seen: set[str] = set()
    for cell in cells:
        rel = cell["output_path"]
        if rel in seen:
            raise PreflightError(f"duplicate output path: {rel}")
        seen.add(rel)
        if "timestamp" in rel.lower() or "uuid" in rel.lower():
            raise PreflightError(f"non-deterministic path token: {rel}")
        if "/dry" in rel or "pytest" in rel or "tmp" in rel.lower():
            raise PreflightError(f"path points at dry-run/test dir: {rel}")
        abs_path = Path(cell["output_path_abs"]).resolve()
        try:
            abs_path.relative_to(root / FORMAL_RESULTS_DIR)
        except ValueError as exc:
            raise PreflightError(f"output path outside formal confirmatory dir: {rel}") from exc
        if abs_path.is_file() and abs_path.stat().st_size > 0:
            blockers.append(rel)
    return blockers


def collect_runner_drift_blockers() -> list[str]:
    """Legacy pilot notes. Formal confirmatory path uses ce115_calc_formal_runner + frozen plan."""
    return [
        "legacy math_boundary_pilot prompt builders remain for legacy/pilot paths only; "
        "formal confirmatory uses cell.prompt_text from ce115_calc_run_plan",
        "live Ollama transport not exercised in Milestone 3D (plan-only / fake transport tests)",
    ]


def run_preflight(
    manifest_path: Path | str | None = None,
    *,
    repo_root: Path | None = None,
    write_results: bool = False,
) -> dict[str, Any]:
    if write_results:
        raise PreflightError("preflight must not write formal results (write_results=True forbidden)")

    root = repo_root or REPO_ROOT
    path = Path(manifest_path) if manifest_path is not None else root / DEFAULT_MANIFEST_REL
    manifest = load_manifest(path)
    m_hash = file_sha256(path)
    cells = expand_local_confirmatory_cells(manifest, repo_root=root)
    assert_cell_distribution(cells)
    assert_cross_model_prompt_identity(cells)
    assert_output_path_safety(cells, repo_root=root)

    prompt_hash_mismatches = 0
    request_setting_mismatches = 0
    # Already fail-fast above; counts stay zero when expansion succeeds.
    planned_records = [
        build_planned_record_skeleton(
            cell,
            commit_hash=str(manifest["git_commit"]),
            manifest_hash=m_hash,
        )
        for cell in cells
    ]
    for record in planned_records:
        missing = [key for key in REQUIRED_PLANNED_RECORD_KEYS if key not in record]
        if missing:
            raise PreflightError(f"schema incomplete: {missing}")

    drift = collect_runner_drift_blockers()
    summary = {
        "planned_cells": len(cells),
        "duplicate_cells": 0,
        "duplicate_paths": 0,
        "prompt_hash_mismatches": prompt_hash_mismatches,
        "request_setting_mismatches": request_setting_mismatches,
        "model_calls": 0,
        "manifest_hash": m_hash,
        "git_commit": manifest["git_commit"],
        "local_confirmatory_frozen": True,
        "cells": cells,
        "planned_record_schema_ok": True,
        "planned_records_sample": planned_records[0],
        "runner_drift_notes": drift,
        "verdict": "READY",
    }
    # JSON-safe plan without huge prompt duplication for CLI dump optional
    return summary


def plan_summary_for_cli(summary: Mapping[str, Any]) -> dict[str, Any]:
    conflicts = 0
    for cell in summary.get("cells") or []:
        abs_path = Path(cell["output_path_abs"])
        if abs_path.is_file() and abs_path.stat().st_size > 0:
            conflicts += 1
    verdict = summary["verdict"]
    if conflicts:
        verdict = "NOT READY"
    return {
        "planned_cells": summary["planned_cells"],
        "duplicate_cells": summary["duplicate_cells"],
        "duplicate_paths": summary["duplicate_paths"],
        "prompt_hash_mismatches": summary["prompt_hash_mismatches"],
        "request_setting_mismatches": summary["request_setting_mismatches"],
        "existing_output_conflicts": conflicts,
        "model_calls": summary["model_calls"],
        "local_confirmatory_frozen": True,
        "manifest_hash": summary["manifest_hash"],
        "git_commit": summary["git_commit"],
        "planned_record_schema_ok": summary["planned_record_schema_ok"],
        "runner_drift_notes": summary["runner_drift_notes"],
        "verdict": verdict,
    }


def assert_no_transport_imports_in_source(source: str) -> None:
    # Build tokens without embedding forbidden call literals as contiguous source.
    forbidden_snippets = (
        "urllib" + ".request",
        "import " + "requests",
        "import " + "httpx",
        "Google" + "AIClient",
        "call_" + "ollama_chat",
        "ollama" + ".chat",
        "ollama" + ".generate",
        "generativelanguage" + ".googleapis.com",
        "http://127.0.0.1:" + "11434",
        "http://localhost:" + "11434",
    )
    for snippet in forbidden_snippets:
        if snippet in source:
            raise PreflightError(f"transport import/call leaked into planning source: {snippet}")


def module_source_guard() -> None:
    path = Path(__file__)
    assert_no_transport_imports_in_source(path.read_text(encoding="utf-8"))
