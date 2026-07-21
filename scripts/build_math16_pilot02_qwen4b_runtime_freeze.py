# -*- coding: utf-8 -*-
"""Build Math16 Pilot-02 Qwen 3.5 4B runtime freeze assets (zero model calls).

Completes ab2d_spec_v2 16-task inventory by copying byte-identical v1 prompts
for the 11 unpatched tasks, then writes runtime manifest + 320-cell plan.
"""
from __future__ import annotations

import hashlib
import json
import platform
import shutil
import subprocess
import sys
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

SOURCE_COMMIT = subprocess.check_output(
    ["git", "rev-parse", "HEAD"], cwd=str(ROOT), text=True
).strip()

SEEDS = [2026071301, 2026072001, 2026072002, 2026072003, 2026072004]
CONDITIONS = ["ab1", "ab2g", "ab2d", "ab2d_spec_v2"]
MODEL_TAG = "qwen3.5:4b"
MODEL_SLUG = "qwen3_5_4b"
EXPERIMENT_ID = "math16_pilot02_qwen4b_freeze_v1"

TASK_ORDER = [
    "ce111_q03_prime_factor_selection",
    "ce112_q01_negative_integer_power",
    "ce112_q09_divisor_multiple_intersection",
    "ce111_nonchoice_q01_part1_exponential_growth",
    "ce111_q02_polynomial_division_remainder",
    "ce111_q08_polynomial_factor_parameter_recovery",
    "ce115_calc_polynomial_division_l1",
    "ce115_calc_polynomial_factor_roots_l1",
    "ce111_q10_ordered_quadratic_roots_radical",
    "ce112_q04_radical_simplification",
    "ce113_q11_rationalize_denominator",
    "ce115_calc_radical_simplification_l1",
    "ce111_q05_exact_fraction_expression",
    "ce112_q12_independent_probability_fraction",
    "ce113_q01_negative_fraction_subtraction",
    "ce115_calc_exact_rational_expression_l1",
]

FAMILY_OF = {
    "ce111_q03_prime_factor_selection": "integer",
    "ce112_q01_negative_integer_power": "integer",
    "ce112_q09_divisor_multiple_intersection": "integer",
    "ce111_nonchoice_q01_part1_exponential_growth": "integer",
    "ce111_q02_polynomial_division_remainder": "polynomial",
    "ce111_q08_polynomial_factor_parameter_recovery": "polynomial",
    "ce115_calc_polynomial_division_l1": "polynomial",
    "ce115_calc_polynomial_factor_roots_l1": "polynomial",
    "ce111_q10_ordered_quadratic_roots_radical": "radical",
    "ce112_q04_radical_simplification": "radical",
    "ce113_q11_rationalize_denominator": "radical",
    "ce115_calc_radical_simplification_l1": "radical",
    "ce111_q05_exact_fraction_expression": "fraction",
    "ce112_q12_independent_probability_fraction": "fraction",
    "ce113_q01_negative_fraction_subtraction": "fraction",
    "ce115_calc_exact_rational_expression_l1": "fraction",
}

PATCHED_V2_TASKS = {
    "ce111_q05_exact_fraction_expression",
    "ce112_q12_independent_probability_fraction",
    "ce113_q01_negative_fraction_subtraction",
    "ce111_q08_polynomial_factor_parameter_recovery",
    "ce111_q02_polynomial_division_remainder",
}

HEALER_ALLOWLIST = [
    "L1_CLOSE_UNBALANCED_PARENTHESIS",
    "L1_CLOSE_UNBALANCED_DELIMITER_EXTENDED",
    "L1_PROSE_RESIDUE_NARROW",
    "L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP",
    "L2_KWARGS_EMPTY_BAG_INLINE_UNIQUE_PARAM",
    "L2_CORRECT_ANSWER_JSON_DUMPS_UNWRAP",
]

TAXONOMY_PATH = ROOT / "docs/決賽文件/20260720_AI 生成程式共同失敗分類標準_實際使用版 v3.md"
EVALUATOR_PATH = ROOT / "scripts/evaluate_math16_pilot02_full_v4.py"
V2_PROMPTS = ROOT / "docs/experiments/prompts/ab2d_spec_v2/prompts"
V1_PROMPTS = ROOT / "docs/experiments/prompts/ab2d_spec/prompts"
V2_MANIFEST = ROOT / "docs/experiments/prompts/ab2d_spec_v2/manifest.json"

OUT_RUNTIME = ROOT / "docs/experiments/manifests/math16_pilot02_qwen4b_runtime_manifest.json"
OUT_PLAN = ROOT / "docs/experiments/manifests/math16_pilot02_qwen4b_cell_plan.json"
OUT_DESIGN = ROOT / "docs/experiments/design/math16_pilot02_qwen4b_runtime_preregistration.md"

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

FORBIDDEN_FINGERPRINT_SUBSTRINGS = [
    "api_key",
    "api key",
    "username",
    "user_name",
    "created_at",
    "timestamp",
    "C:\\",
    "c:\\",
    "/Users/",
    "output_root",
]


def sha_text(text: str) -> str:
    return hashlib.sha256(text.replace("\r\n", "\n").encode("utf-8")).hexdigest()


def sha_file_lf(path: Path) -> str:
    return sha_text(path.read_text(encoding="utf-8"))


def sha_file_raw(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha_json(obj: Any) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()


def http_json(url: str, payload: dict | None = None) -> dict:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"} if data else {},
        method="GET" if data is None else "POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def query_runtime() -> dict[str, Any]:
    version = http_json("http://localhost:11434/api/version")["version"]
    tags = http_json("http://localhost:11434/api/tags")
    model_row = None
    for m in tags.get("models", []):
        if m.get("name") == MODEL_TAG or m.get("model") == MODEL_TAG:
            model_row = m
            break
    if model_row is None:
        raise RuntimeError(f"{MODEL_TAG} not found in ollama tags")
    show = http_json("http://localhost:11434/api/show", {"name": MODEL_TAG})
    details = show.get("details") or {}
    mi = show.get("model_info") or {}

    # GPU via nvidia-smi
    gpu_name = None
    vram_mib = None
    driver = None
    try:
        out = subprocess.check_output(
            [
                "nvidia-smi",
                "--query-gpu=name,memory.total,driver_version",
                "--format=csv,noheader,nounits",
            ],
            text=True,
            encoding="utf-8",
            errors="ignore",
        ).strip()
        parts = [p.strip() for p in out.split(",")]
        gpu_name, vram_mib, driver = parts[0], int(float(parts[1])), parts[2]
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(f"nvidia-smi query failed: {exc}") from exc

    cpu = subprocess.check_output(
        [
            "powershell",
            "-NoProfile",
            "-Command",
            "(Get-CimInstance Win32_Processor).Name.Trim()",
        ],
        text=True,
        encoding="utf-8",
        errors="ignore",
    ).strip()
    ram_bytes = int(
        subprocess.check_output(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "(Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory",
            ],
            text=True,
            encoding="utf-8",
            errors="ignore",
        ).strip()
    )

    # Probe whether model currently resident (warm) via /api/ps
    warm = False
    try:
        ps = http_json("http://localhost:11434/api/ps")
        for row in ps.get("models", []) or []:
            if row.get("name") == MODEL_TAG or row.get("model") == MODEL_TAG:
                warm = True
                break
    except Exception:  # noqa: BLE001
        warm = False

    from scripts.math16_qwen_ollama_adapter import (
        BACKOFF_SECONDS,
        FROZEN_INFERENCE_CONFIG,
        MAX_ATTEMPTS,
        REQUEST_TIMEOUT_SECONDS,
        build_math16_chat_payload,
    )

    sample_payload = build_math16_chat_payload("preflight", seed=SEEDS[0], model=MODEL_TAG)
    seed_supported = "seed" in (sample_payload.get("options") or {})
    if sample_payload.get("think") is not False:
        raise RuntimeError("adapter think must be false")
    if not seed_supported:
        raise RuntimeError("expected options.seed in adapter payload")

    param_count = int(mi.get("general.parameter_count") or 0)
    if param_count <= 0:
        raise RuntimeError("missing general.parameter_count from ollama show")

    return {
        "model_provider": "ollama",
        "model_tag": MODEL_TAG,
        "model_digest": model_row["digest"],
        "model_version": f"{MODEL_TAG}@{model_row['digest'][:12]}",
        "architecture": details.get("family") or mi.get("general.architecture"),
        "parameter_count": param_count,
        "parameter_count_label": details.get("parameter_size"),
        "parameter_count_basis": "ollama /api/show model_info.general.parameter_count",
        "quantization": details.get("quantization_level"),
        "runtime": "ollama",
        "runtime_version": version,
        "transport": "http://localhost:11434/api/chat",
        "endpoint": "POST /api/chat",
        "thinking_mode": False,
        "thinking_mode_transport_field": "think (top-level /api/chat)",
        "temperature": FROZEN_INFERENCE_CONFIG["temperature"],
        "top_p": FROZEN_INFERENCE_CONFIG["top_p"],
        "top_k": FROZEN_INFERENCE_CONFIG["top_k"],
        "repeat_penalty": "ollama_default_unset",
        "seed_transport_supported": True,
        "seed_transport_field": "options.seed",
        "seed_role": "model_rng_seed_and_cell_label",
        "context_window": FROZEN_INFERENCE_CONFIG["num_ctx"],
        "model_native_context_length": mi.get("qwen35.context_length")
        or (details.get("context_length")),
        "max_output_tokens": FROZEN_INFERENCE_CONFIG["num_predict"],
        "max_output_tokens_runtime_field": "options.num_predict",
        "stop_sequences": [],
        "stop_sequences_note": "not set; Ollama default (empty)",
        "timeout_seconds": REQUEST_TIMEOUT_SECONDS,
        "retry_policy": {
            "max_attempts": MAX_ATTEMPTS,
            "retry_delays_seconds": list(BACKOFF_SECONDS),
            "retryable": ["timeout", "connection_failure", "empty_response"],
        },
        "hardware": {
            "cpu": cpu,
            "gpu": gpu_name,
            "vram_mib": vram_mib,
            "ram_bytes": ram_bytes,
            "ram_gib_approx": round(ram_bytes / (1024**3), 2),
            "os": f"{platform.system()} {platform.release()} ({platform.version()})",
            "driver_version": driver,
        },
        "cold_warm": {
            "definition": (
                "warm = model currently listed in Ollama /api/ps; "
                "cold = not loaded into runner VRAM/process until first request"
            ),
            "observed_at_preregistration": "warm" if warm else "cold",
            "policy": (
                "Generation may start cold or warm; do not treat warm-start "
                "latency differences as outcome confounds. Do not unload/reload "
                "mid-cohort to chase warm state."
            ),
        },
        "adapter": "scripts/math16_qwen_ollama_adapter.py",
        "sample_payload_options": sample_payload["options"],
        "sample_payload_think": sample_payload["think"],
    }


def complete_v2_prompt_inventory() -> dict[str, dict[str, Any]]:
    """Ensure all 16 tasks exist under ab2d_spec_v2/prompts (no content regen)."""
    V2_PROMPTS.mkdir(parents=True, exist_ok=True)
    registry: dict[str, dict[str, Any]] = {}
    for tid in TASK_ORDER:
        dest = V2_PROMPTS / f"{tid}.txt"
        src_v1 = V1_PROMPTS / f"{tid}.txt"
        if not src_v1.exists():
            raise FileNotFoundError(src_v1)
        if tid in PATCHED_V2_TASKS:
            if not dest.exists():
                raise FileNotFoundError(f"patched v2 prompt missing: {dest}")
            provenance = "api_signature_patch_v2"
        else:
            # byte-identical promote into v2 inventory
            if dest.exists():
                if sha_file_lf(dest) != sha_file_lf(src_v1):
                    raise RuntimeError(f"v2 unpatched prompt drifted from v1: {tid}")
            else:
                shutil.copyfile(src_v1, dest)
            provenance = "byte_identical_promote_from_ab2d_spec_v1"
        sha = sha_file_lf(dest)
        v1_sha = sha_file_lf(src_v1)
        registry[tid] = {
            "task_id": tid,
            "family": FAMILY_OF[tid],
            "condition": "ab2d_spec_v2",
            "prompt_path": f"docs/experiments/prompts/ab2d_spec_v2/prompts/{tid}.txt",
            "prompt_sha256": sha,
            "provenance": provenance,
            "matches_v1_sha256": sha == v1_sha,
            "v1_prompt_sha256": v1_sha,
        }
    # rewrite full v2 manifest tasks list while preserving patched metadata
    old = json.loads(V2_MANIFEST.read_text(encoding="utf-8"))
    old_by = {t["task_id"]: t for t in old.get("tasks", [])}
    full_tasks = []
    for tid in TASK_ORDER:
        if tid in old_by:
            row = dict(old_by[tid])
            row["prompt_path"] = registry[tid]["prompt_path"]
            row["exact_prompt_sha256"] = registry[tid]["prompt_sha256"]
            full_tasks.append(row)
        else:
            full_tasks.append(
                {
                    "condition": "ab2d_spec_v2",
                    "task_id": tid,
                    "family": FAMILY_OF[tid],
                    "prompt_revision": "ab2d_spec_v2",
                    "prior_prompt_revision": "ab2d_spec_v1",
                    "prior_exact_prompt_sha256": registry[tid]["v1_prompt_sha256"],
                    "exact_prompt_sha256": registry[tid]["prompt_sha256"],
                    "prompt_path": registry[tid]["prompt_path"],
                    "prompt_frozen": True,
                    "model_called": False,
                    "inventory_note": (
                        "Unpatched relative to v1; promoted byte-identical into "
                        "ab2d_spec_v2 inventory for cross-model fourth condition."
                    ),
                }
            )
    old["tasks"] = full_tasks
    old["inventory_complete_16"] = True
    old["inventory_completed_at_utc"] = datetime.now(timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )
    old["inventory_completion_note"] = (
        "11 unpatched tasks promoted byte-identical from ab2d_spec v1 into "
        "ab2d_spec_v2/prompts for Qwen Pilot-02 fourth-condition freeze; "
        "5 API-signature-patched prompts unchanged."
    )
    V2_MANIFEST.write_text(
        json.dumps(old, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return registry


def build_prompt_registry(v2_reg: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    from agent_tools.finals_rebuild.ce115_clean_incremental_ablation import (
        build_condition_prompt,
    )
    from agent_tools.finals_rebuild.math16_pool import frozen_for_prompt, tasks_by_id

    tasks = tasks_by_id()
    rows: list[dict[str, Any]] = []
    for tid in TASK_ORDER:
        task = tasks[tid]
        frozen = frozen_for_prompt(task)
        for cond in ("ab1", "ab2g", "ab2d"):
            text = build_condition_prompt(cond, task, frozen).replace("\r\n", "\n")
            sha = sha_text(text)
            rows.append(
                {
                    "task_id": tid,
                    "family": FAMILY_OF[tid],
                    "condition": cond,
                    "condition_display": {
                        "ab1": "Ab1",
                        "ab2g": "Ab2g",
                        "ab2d": "Ab2d+api",
                    }[cond],
                    "prompt_source": (
                        "agent_tools/finals_rebuild/ce115_clean_incremental_ablation.py"
                        "::build_condition_prompt"
                    ),
                    "prompt_path": None,
                    "prompt_sha256": sha,
                    "char_count": len(text),
                }
            )
        v2 = v2_reg[tid]
        rows.append(
            {
                "task_id": tid,
                "family": FAMILY_OF[tid],
                "condition": "ab2d_spec_v2",
                "condition_display": "Ab2d+spec-v2",
                "prompt_source": "frozen_file",
                "prompt_path": v2["prompt_path"],
                "prompt_sha256": v2["prompt_sha256"],
                "provenance": v2["provenance"],
                "char_count": len(
                    (ROOT / v2["prompt_path"]).read_text(encoding="utf-8").replace(
                        "\r\n", "\n"
                    )
                ),
            }
        )
    return rows


def compute_fingerprint(payload: dict[str, Any]) -> str:
    sub = {k: payload[k] for k in FINGERPRINT_KEYS}
    blob = json.dumps(sub, sort_keys=True, ensure_ascii=False)
    for bad in FORBIDDEN_FINGERPRINT_SUBSTRINGS:
        if bad.lower() in blob.lower() and bad not in ("created_at",):
            # allow nothing; created_at not in keys
            if bad in ("C:\\", "c:\\", "/Users/"):
                raise RuntimeError(f"forbidden path leaked into fingerprint: {bad}")
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def build_cell_plan(prompt_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by = {(r["task_id"], r["condition"]): r for r in prompt_rows}
    plan = []
    for seed in SEEDS:
        for tid in TASK_ORDER:
            for cond in CONDITIONS:
                row = by[(tid, cond)]
                cell_id = f"{MODEL_SLUG}__{tid}__{cond}__seed_{seed}"
                plan.append(
                    {
                        "cell_id": cell_id,
                        "task_id": tid,
                        "family": FAMILY_OF[tid],
                        "condition": cond,
                        "condition_display": row["condition_display"],
                        "seed": seed,
                        "model_tag": MODEL_TAG,
                        "prompt_path": row.get("prompt_path"),
                        "prompt_source": row["prompt_source"],
                        "prompt_sha256": row["prompt_sha256"],
                        "output_relative_path": (
                            f"math16_pilot02_qwen4b/cells/{cell_id}"
                        ),
                    }
                )
    return plan


def write_prereg_md(
    runtime: dict[str, Any],
    manifest: dict[str, Any],
    prompt_rows: list[dict[str, Any]],
    gemini_fp: str,
) -> None:
    lines: list[str] = []
    lines.append("# Math16 Pilot-02 Qwen 3.5 4B Runtime Preregistration / Freeze")
    lines.append("")
    lines.append("```text")
    lines.append("MATH16_PILOT02_QWEN4B_RUNTIME_PREREGISTRATION_FROZEN")
    lines.append("```")
    lines.append("")
    lines.append(
        "**Policy:** zero-model freeze only — no generation, no Ollama chat calls "
        "beyond `/api/tags` `/api/show` `/api/version` `/api/ps` probes."
    )
    lines.append("")
    lines.append("## 1. Scope")
    lines.append("")
    lines.append(
        "Cross-model Math16 Pilot-02 geometry for **Qwen 3.5 4B** only: "
        "16 tasks × 4 conditions × 5 seeds = **320 cells**."
    )
    lines.append("")
    lines.append("| Condition (machine) | Display | Prompt asset |")
    lines.append("| :--- | :--- | :--- |")
    lines.append("| `ab1` | Ab1 | Same builder as Gemini Pilot-02 |")
    lines.append("| `ab2g` | Ab2g | Same builder as Gemini Pilot-02 |")
    lines.append("| `ab2d` | Ab2d+api | Same builder as Gemini Pilot-02 |")
    lines.append(
        "| `ab2d_spec_v2` | Ab2d+spec-v2 | Frozen `ab2d_spec_v2` files "
        "(API-signature-complete); **not** Gemini primary `ab2d_spec` v1 |"
    )
    lines.append("")
    lines.append(
        "> Ab2d+spec-v2 is a post-hoc cleaned cross-model comparison asset. "
        "It must not be described as Gemini's original primary fourth condition."
    )
    lines.append("")
    lines.append("## 2. Locked shared assets")
    lines.append("")
    lines.append(f"- Seeds: `{SEEDS}`")
    lines.append(
        f"- Evaluator: `scripts/evaluate_math16_pilot02_full_v4.py` "
        f"(SHA `{manifest['evaluator_hash']}`)"
    )
    lines.append(
        f"- Taxonomy v3 SHA: `{manifest['taxonomy_hash']}`"
    )
    lines.append(
        f"- Healer allowlist SHA: `{manifest['healer_allowlist_hash']}`"
    )
    lines.append(f"- Source commit: `{SOURCE_COMMIT}`")
    lines.append("")
    lines.append("### Ab2d+spec-v2 API cards (required)")
    lines.append("")
    lines.append("- `FractionOps.create(value)`")
    lines.append("- `FractionOps.from_parts(numerator, denominator)`")
    lines.append("- `PolynomialOps.format_latex(coeffs, var='x')`")
    lines.append("")
    lines.append("## 3. Qwen 4B runtime (queried)")
    lines.append("")
    hw = runtime["hardware"]
    for k in [
        "model_provider",
        "model_tag",
        "model_digest",
        "model_version",
        "architecture",
        "parameter_count",
        "parameter_count_label",
        "parameter_count_basis",
        "quantization",
        "runtime",
        "runtime_version",
        "transport",
        "endpoint",
        "thinking_mode",
        "temperature",
        "top_k",
        "top_p",
        "repeat_penalty",
        "seed_transport_supported",
        "seed_transport_field",
        "seed_role",
        "context_window",
        "max_output_tokens",
        "timeout_seconds",
    ]:
        lines.append(f"- **{k}**: `{runtime[k]}`")
    lines.append(f"- **stop_sequences**: `{runtime['stop_sequences']}` ({runtime['stop_sequences_note']})")
    lines.append(f"- **retry_policy**: `{json.dumps(runtime['retry_policy'], ensure_ascii=False)}`")
    lines.append("")
    lines.append("### Thinking mode")
    lines.append("")
    lines.append("```text")
    lines.append("think=false")
    lines.append("```")
    lines.append("")
    lines.append(
        "> 固定 Qwen 4B cohort 內的推理模式，避免 320 格生成期間混入 thinking-mode 變因；"
        "不宣稱其與 Gemini 內部推理機制完全等價。"
    )
    lines.append("")
    lines.append("### Seed semantics")
    lines.append("")
    lines.append(
        f"- Transport supported: **{runtime['seed_transport_supported']}** "
        f"via `{runtime['seed_transport_field']}` "
        f"(preflight evidence from `build_math16_chat_payload`)."
    )
    lines.append(
        f"- `seed_role = {runtime['seed_role']}` — cell seed is both the Ollama "
        "`options.seed` RNG seed and the cell-id label."
    )
    lines.append("")
    lines.append("### Hardware")
    lines.append("")
    lines.append(f"- CPU: `{hw['cpu']}`")
    lines.append(f"- GPU: `{hw['gpu']}`")
    lines.append(f"- VRAM: `{hw['vram_mib']} MiB`")
    lines.append(f"- RAM: `{hw['ram_gib_approx']} GiB` (`{hw['ram_bytes']}` bytes)")
    lines.append(f"- OS: `{hw['os']}`")
    lines.append(f"- Driver: `{hw['driver_version']}`")
    lines.append("")
    lines.append("### Cold / warm")
    lines.append("")
    lines.append(f"- Definition: {runtime['cold_warm']['definition']}")
    lines.append(
        f"- Observed at preregistration: **{runtime['cold_warm']['observed_at_preregistration']}**"
    )
    lines.append(f"- Policy: {runtime['cold_warm']['policy']}")
    lines.append("")
    lines.append("## 4. Allowed vs required consistency vs Gemini")
    lines.append("")
    lines.append("### Must match")
    lines.append("")
    lines.append(
        "tasks/payloads, condition structure, prompt SHA for Ab1/Ab2g/Ab2d+api, "
        "Ab2d+spec-v2 API cards, seed list, evaluator, taxonomy, Healer, "
        "success definitions, cell geometry, stats口径, retry/resume/quarantine principles"
    )
    lines.append("")
    lines.append("### May differ (and are recorded)")
    lines.append("")
    lines.append(
        "provider, model tag/digest, architecture/parameters/quantization, "
        "runtime/version, thinking-mode implementation, context/output limits, "
        "sampling parameters that cannot fully align, timeout, hardware, "
        "cold/warm, seed transport capability"
    )
    lines.append("")
    lines.append("## 5. Runtime fingerprint")
    lines.append("")
    lines.append(f"- **Qwen fingerprint**: `{manifest['runtime_config_fingerprint']}`")
    lines.append(f"- **Gemini full fingerprint (reference)**: `{gemini_fp}`")
    lines.append("")
    lines.append(
        "Fingerprints share a research schema intent but **must not** differ only "
        "by `model_tag`: Qwen fingerprint includes digest, architecture, "
        "parameter_count, quantization, repeat_penalty, seed_transport_supported, "
        "context_window, prompt_manifest_hash, evaluator/taxonomy/healer hashes."
    )
    lines.append("")
    lines.append("| Field class | Gemini full | Qwen 4B |")
    lines.append("| :--- | :--- | :--- |")
    lines.append("| Schema keys for FP | 15 runtime keys | 26 expanded keys |")
    lines.append("| Must-equal across models | seed_list (values), taxonomy/eval/healer hashes, prompt SHAs for shared conditions | same |")
    lines.append("| Reasonable differences | provider/runtime/sampling/thinking/hardware/digest/quant | recorded in this freeze |")
    lines.append("")
    lines.append("Excluded from fingerprint: API keys, timestamps, usernames, absolute machine paths, transient output dirs.")
    lines.append("")
    lines.append("## 6. Expected cell geometry")
    lines.append("")
    lines.append("```text")
    lines.append("16 tasks × 4 conditions × 5 seeds = 320 cells / model")
    lines.append("4 families × 4 tasks × 4 conditions × 5 seeds = 80 cells / family")
    lines.append("```")
    lines.append("")
    lines.append("- 320 unique `cell_id`")
    lines.append("- 80 / condition, 80 / family, 20 / task, 64 / seed")
    lines.append("")
    lines.append("## 7. Prompt SHA registry (16 × 4)")
    lines.append("")
    lines.append("| Task | Cond | Path | SHA-256 |")
    lines.append("| :--- | :--- | :--- | :--- |")
    for r in prompt_rows:
        path = r.get("prompt_path") or "(builder)"
        lines.append(
            f"| `{r['task_id']}` | `{r['condition']}` | `{path}` | `{r['prompt_sha256']}` |"
        )
    lines.append("")
    lines.append("## 8. Governance")
    lines.append("")
    lines.append("- Resume: skip only if complete artifact metadata matches plan + fingerprint.")
    lines.append("- Mismatch: fail-closed (`INCOMPATIBLE_EXISTING_CELL`); never overwrite.")
    lines.append("- Incomplete cell dirs: quarantine then redo.")
    lines.append("- After this freeze, do not switch `think`, sampling, model digest, or prompt SHAs mid-cohort.")
    lines.append("")
    lines.append(f"- Runtime manifest: `docs/experiments/manifests/math16_pilot02_qwen4b_runtime_manifest.json`")
    lines.append(f"- Cell plan: `docs/experiments/manifests/math16_pilot02_qwen4b_cell_plan.json`")
    lines.append("")
    OUT_DESIGN.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    runtime = query_runtime()
    v2_reg = complete_v2_prompt_inventory()
    prompt_rows = build_prompt_registry(v2_reg)
    plan = build_cell_plan(prompt_rows)

    # geometry asserts
    assert len(plan) == 320
    assert len({c["cell_id"] for c in plan}) == 320
    assert Counter(c["condition"] for c in plan) == {c: 80 for c in CONDITIONS}
    assert Counter(c["family"] for c in plan) == {
        "integer": 80,
        "polynomial": 80,
        "radical": 80,
        "fraction": 80,
    }
    assert Counter(c["task_id"] for c in plan) == {t: 20 for t in TASK_ORDER}
    assert Counter(c["seed"] for c in plan) == {s: 64 for s in SEEDS}
    assert all(c["condition"] != "ab2d_spec" for c in plan)
    assert all(
        (c["prompt_path"] or "").startswith("docs/experiments/prompts/ab2d_spec_v2/")
        for c in plan
        if c["condition"] == "ab2d_spec_v2"
    )

    taxonomy_hash = sha_file_raw(TAXONOMY_PATH)
    evaluator_hash = sha_file_raw(EVALUATOR_PATH)
    healer_hash = sha_json(HEALER_ALLOWLIST)
    prompt_manifest_hash = sha_json(
        [
            {
                "task_id": r["task_id"],
                "condition": r["condition"],
                "prompt_sha256": r["prompt_sha256"],
                "prompt_path": r.get("prompt_path"),
            }
            for r in prompt_rows
        ]
    )

    expected_tax = "7df8f4472ce048569967436cbc73ede8fd4bd117ad67d0028ddd95af2055a304"
    expected_eval = "2cca19f2258d4ba6134ff10d4e9bcff925e2441c32820fcbc151cb6b1dd740bc"
    if taxonomy_hash != expected_tax:
        raise RuntimeError(f"taxonomy hash drift: {taxonomy_hash}")
    if evaluator_hash != expected_eval:
        raise RuntimeError(f"evaluator hash drift: {evaluator_hash}")

    fp_payload = {
        "experiment_id": EXPERIMENT_ID,
        "model_provider": runtime["model_provider"],
        "model_tag": runtime["model_tag"],
        "model_digest": runtime["model_digest"],
        "model_version": runtime["model_version"],
        "architecture": runtime["architecture"],
        "parameter_count": runtime["parameter_count"],
        "quantization": runtime["quantization"],
        "runtime": runtime["runtime"],
        "runtime_version": runtime["runtime_version"],
        "thinking_mode": False,
        "temperature": runtime["temperature"],
        "top_p": runtime["top_p"],
        "top_k": runtime["top_k"],
        "repeat_penalty": runtime["repeat_penalty"],
        "seed_transport_supported": True,
        "context_window": runtime["context_window"],
        "max_output_tokens": runtime["max_output_tokens"],
        "timeout_seconds": runtime["timeout_seconds"],
        "retry_policy": runtime["retry_policy"],
        "seed_list": SEEDS,
        "prompt_manifest_hash": prompt_manifest_hash,
        "evaluator_hash": evaluator_hash,
        "taxonomy_hash": taxonomy_hash,
        "healer_allowlist_hash": healer_hash,
        "source_commit": SOURCE_COMMIT,
    }
    fingerprint = compute_fingerprint(fp_payload)

    gemini_fp = "8bcb0d7177bc35216410108bda88b014848181a95b12bc09bf171866749f3057"

    manifest = {
        **fp_payload,
        "preregistration_status": "FROZEN",
        "study_stage": "pilot02_qwen4b_runtime_preregistration",
        "condition_order": CONDITIONS,
        "condition_display_map": {
            "ab1": "Ab1",
            "ab2g": "Ab2g",
            "ab2d": "Ab2d+api",
            "ab2d_spec_v2": "Ab2d+spec-v2",
        },
        "task_order": TASK_ORDER,
        "expected_cell_count": 320,
        "expected_per_condition": 80,
        "expected_per_family": 80,
        "expected_per_task": 20,
        "expected_per_seed": 64,
        "thinking_mode_rationale": (
            "固定Qwen 4B cohort內的推理模式，避免320格生成期間混入thinking-mode變因；"
            "不宣稱其與Gemini內部推理機制完全等價。"
        ),
        "seed_role": runtime["seed_role"],
        "seed_transport_field": runtime["seed_transport_field"],
        "stop_sequences": runtime["stop_sequences"],
        "transport": runtime["transport"],
        "endpoint": runtime["endpoint"],
        "parameter_count_label": runtime["parameter_count_label"],
        "parameter_count_basis": runtime["parameter_count_basis"],
        "model_native_context_length": runtime["model_native_context_length"],
        "hardware": runtime["hardware"],
        "cold_warm": runtime["cold_warm"],
        "adapter": runtime["adapter"],
        "healer_allowlist": HEALER_ALLOWLIST,
        "prompt_verification_registry": prompt_rows,
        "ab2d_spec_v2_api_cards": [
            "FractionOps.create(value)",
            "FractionOps.from_parts(numerator, denominator)",
            "PolynomialOps.format_latex(coeffs, var='x')",
        ],
        "ab2d_spec_v2_note": (
            "Fourth condition uses ab2d_spec_v2 (API-signature-complete). "
            "Not Gemini primary ab2d_spec v1."
        ),
        "gemini_reference_fingerprint": gemini_fp,
        "fingerprint_schema_keys": FINGERPRINT_KEYS,
        "fingerprint_forbidden": [
            "api_keys",
            "timestamps",
            "usernames",
            "absolute_machine_paths",
            "transient_output_dirs",
        ],
        "allowed_cross_model_diff_fields": [
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
            "hardware",
            "cold_warm",
            "transport",
            "endpoint",
        ],
        "must_match_cross_model_fields": [
            "seed_list",
            "task_order",
            "prompt_sha256_for_ab1_ab2g_ab2d",
            "evaluator_hash",
            "taxonomy_hash",
            "healer_allowlist_hash",
            "expected_cell_geometry",
        ],
        "output_root": "docs/experiments/results/math16_pilot02_qwen4b",
        "resume_policy": "skip_if_complete_and_metadata_match_else_fail_closed",
        "overwrite_policy": "never",
        "quarantine_policy": "move_incomplete_cell_dir_then_redo",
        "created_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "runtime_config_fingerprint": fingerprint,
        "preflight_probes_only": [
            "/api/version",
            "/api/tags",
            "/api/show",
            "/api/ps",
        ],
        "llm_generation_calls": 0,
    }

    OUT_RUNTIME.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    OUT_PLAN.write_text(
        json.dumps(plan, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    write_prereg_md(runtime, manifest, prompt_rows, gemini_fp)

    print(
        json.dumps(
            {
                "status": "BUILT",
                "cells": len(plan),
                "fingerprint": fingerprint,
                "model_digest": runtime["model_digest"],
                "thinking_mode": False,
                "seed_transport_supported": True,
                "llm_generation_calls": 0,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
