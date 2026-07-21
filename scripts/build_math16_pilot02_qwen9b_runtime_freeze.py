# -*- coding: utf-8 -*-
"""Build Math16 Pilot-02 Qwen 3.5 9B runtime freeze assets (zero model calls).

Mirrors Qwen 4B geometry/prompts/sampling exactly; only model identity differs.
Does NOT modify Qwen 4B assets or shared prompt files.
"""
from __future__ import annotations

import hashlib
import json
import platform
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
MODEL_TAG = "qwen3.5:9b"
MODEL_SLUG = "qwen3_5_9b"
EXPERIMENT_ID = "math16_pilot02_qwen9b_freeze_v1"

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

HEALER_ALLOWLIST = [
    "L1_CLOSE_UNBALANCED_PARENTHESIS",
    "L1_CLOSE_UNBALANCED_DELIMITER_EXTENDED",
    "L1_PROSE_RESIDUE_NARROW",
    "L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP",
    "L2_KWARGS_EMPTY_BAG_INLINE_UNIQUE_PARAM",
    "L2_CORRECT_ANSWER_JSON_DUMPS_UNWRAP",
]

# Corrected-chain Healer pins (record only; do not run Healer this round).
EXPECTED_HEALER_RUNNER_HASH = (
    "38453d1294382f061efe149484f5a3059a47d085d2aeef358874a954e37adebf"
)
EXPECTED_HEALER_PROTOCOL_HASH = (
    "bdb4121ee266f91bfa116019a334cf4a528da0d71629b96540a5f763826aff39"
)

TAXONOMY_PATH = ROOT / "docs/決賽文件/20260720_AI 生成程式共同失敗分類標準_實際使用版 v3.md"
EVALUATOR_PATH = ROOT / "scripts/evaluate_math16_pilot02_full_v4.py"
HEALER_RUNNER_PATH = ROOT / "agent_tools/finals_rebuild/ce115_research_healer_runner.py"
HEALER_PROTOCOL_PATH = ROOT / "agent_tools/finals_rebuild/ce115_research_healer_protocol.py"
V2_PROMPTS = ROOT / "docs/experiments/prompts/ab2d_spec_v2/prompts"
QWEN4B_PLAN = ROOT / "docs/experiments/manifests/math16_pilot02_qwen4b_cell_plan.json"
QWEN4B_MANIFEST = ROOT / "docs/experiments/manifests/math16_pilot02_qwen4b_runtime_manifest.json"

OUT_RUNTIME = ROOT / "docs/experiments/manifests/math16_pilot02_qwen9b_runtime_manifest.json"
OUT_PLAN = ROOT / "docs/experiments/manifests/math16_pilot02_qwen9b_cell_plan.json"
OUT_DESIGN = ROOT / "docs/experiments/design/math16_pilot02_qwen9b_runtime_preregistration.md"

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

SAMPLING_RATIONALE = (
    "本實驗固定temperature=0.2、top_p=0.8、top_k=20與think=false，並與Qwen 4B完全一致。"
    "temperature作為主要抽樣隨機性控制參數；top_p與top_k沿用既有凍結設定，未另行調校。"
    "本設定目的不是尋找Qwen 9B最佳解碼參數，而是建立可重現且除模型大小外保持一致的公平比較。"
)


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

    if FROZEN_INFERENCE_CONFIG["temperature"] != 0.2:
        raise RuntimeError("adapter temperature must be 0.2")
    if FROZEN_INFERENCE_CONFIG["top_p"] != 0.8:
        raise RuntimeError("adapter top_p must be 0.8")
    if FROZEN_INFERENCE_CONFIG["top_k"] != 20:
        raise RuntimeError("adapter top_k must be 20")
    if FROZEN_INFERENCE_CONFIG["think"] is not False:
        raise RuntimeError("adapter think must be false")
    if FROZEN_INFERENCE_CONFIG["num_ctx"] != 65536:
        raise RuntimeError("adapter num_ctx must be 65536")
    if FROZEN_INFERENCE_CONFIG["num_predict"] != 24576:
        raise RuntimeError("adapter num_predict must be 24576")

    sample_payload = build_math16_chat_payload("preflight", seed=SEEDS[0], model=MODEL_TAG)
    seed_supported = "seed" in (sample_payload.get("options") or {})
    if sample_payload.get("think") is not False:
        raise RuntimeError("adapter think must be false")
    if not seed_supported:
        raise RuntimeError("expected options.seed in adapter payload")
    if sample_payload["options"].get("temperature") != 0.2:
        raise RuntimeError("payload temperature must be 0.2")
    if sample_payload["options"].get("top_p") != 0.8:
        raise RuntimeError("payload top_p must be 0.8")
    if sample_payload["options"].get("top_k") != 20:
        raise RuntimeError("payload top_k must be 20")

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


def build_prompt_registry() -> list[dict[str, Any]]:
    """Reuse existing frozen prompts; do not rewrite shared prompt assets."""
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
        path = V2_PROMPTS / f"{tid}.txt"
        if not path.exists():
            raise FileNotFoundError(f"missing ab2d_spec_v2 prompt: {path}")
        text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
        sha = sha_text(text)
        rows.append(
            {
                "task_id": tid,
                "family": FAMILY_OF[tid],
                "condition": "ab2d_spec_v2",
                "condition_display": "Ab2d+spec-v2",
                "prompt_source": "frozen_file",
                "prompt_path": f"docs/experiments/prompts/ab2d_spec_v2/prompts/{tid}.txt",
                "prompt_sha256": sha,
                "provenance": "shared_with_qwen4b_ab2d_spec_v2",
                "char_count": len(text),
            }
        )
    return rows


def compute_fingerprint(payload: dict[str, Any]) -> str:
    sub = {k: payload[k] for k in FINGERPRINT_KEYS}
    blob = json.dumps(sub, sort_keys=True, ensure_ascii=False)
    lower = blob.lower()
    for bad in ("api_key", "username", "c:\\users\\", "/users/"):
        if bad in lower:
            raise RuntimeError(f"forbidden content in fingerprint payload: {bad}")
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
                        "temperature": 0.2,
                        "top_p": 0.8,
                        "top_k": 20,
                        "think": False,
                        "output_relative_path": (
                            f"math16_pilot02_qwen9b/cells/{cell_id}"
                        ),
                    }
                )
    return plan


def assert_aligned_with_qwen4b(plan: list[dict[str, Any]], prompt_rows: list[dict[str, Any]]) -> None:
    q4_plan = json.loads(QWEN4B_PLAN.read_text(encoding="utf-8"))
    q4_man = json.loads(QWEN4B_MANIFEST.read_text(encoding="utf-8"))
    if len(q4_plan) != 320:
        raise RuntimeError("qwen4b plan not 320")

    # Prompt SHA registry must match 4B exactly.
    q4_reg = {
        (r["task_id"], r["condition"]): r["prompt_sha256"]
        for r in q4_man["prompt_verification_registry"]
    }
    q9_reg = {(r["task_id"], r["condition"]): r["prompt_sha256"] for r in prompt_rows}
    if q4_reg != q9_reg:
        drift = sorted(k for k in q4_reg if q4_reg.get(k) != q9_reg.get(k))
        raise RuntimeError(f"prompt SHA drift vs Qwen4B: {drift[:5]}")

    # Cell identity except model fields must align.
    q4_by_key = {
        (c["task_id"], c["condition"], c["seed"]): c for c in q4_plan
    }
    for c in plan:
        key = (c["task_id"], c["condition"], c["seed"])
        q4 = q4_by_key[key]
        if c["prompt_sha256"] != q4["prompt_sha256"]:
            raise RuntimeError(f"cell prompt SHA mismatch: {key}")
        if c["family"] != q4["family"]:
            raise RuntimeError(f"family mismatch: {key}")
        if c["condition_display"] != q4["condition_display"]:
            raise RuntimeError(f"condition_display mismatch: {key}")
        if (c.get("prompt_path") or None) != (q4.get("prompt_path") or None):
            raise RuntimeError(f"prompt_path mismatch: {key}")
        # model fields must differ
        if c["model_tag"] == q4["model_tag"]:
            raise RuntimeError("model_tag unexpectedly equal to 4B")
        if not c["cell_id"].startswith("qwen3_5_9b__"):
            raise RuntimeError(f"bad 9B cell_id: {c['cell_id']}")
        if not q4["cell_id"].startswith("qwen3_5_4b__"):
            raise RuntimeError(f"unexpected 4B cell_id: {q4['cell_id']}")

    # Sampling must match 4B lock.
    if q4_man["temperature"] != 0.2 or q4_man["top_p"] != 0.8 or q4_man["top_k"] != 20:
        raise RuntimeError("qwen4b sampling lock drifted")
    if q4_man["thinking_mode"] is not False:
        raise RuntimeError("qwen4b thinking_mode drifted")


def write_prereg_md(
    runtime: dict[str, Any],
    manifest: dict[str, Any],
    prompt_rows: list[dict[str, Any]],
) -> None:
    hw = runtime["hardware"]
    lines: list[str] = [
        "# Math16 Pilot-02 Qwen 3.5 9B Runtime Preregistration / Freeze",
        "",
        "```text",
        "QWEN9B_RUNTIME_PREREGISTRATION_FROZEN",
        "QWEN9B_320CELL_PLAN_VERIFIED",
        "QWEN9B_ZERO_MODEL_PREFLIGHT_PASSED",
        "QWEN9B_320CELL_GENERATION_READY",
        "```",
        "",
        "**Policy:** zero-model freeze only — no generation, no Ollama `/api/chat` calls.",
        "Probes allowed: `/api/tags` `/api/show` `/api/version` `/api/ps`.",
        "",
        "## 1. Scope",
        "",
        "Cross-model Math16 Pilot-02 geometry for **Qwen 3.5 9B**: "
        "16 tasks × 4 conditions × 5 seeds = **320 cells**.",
        "",
        "Except for the model itself, design is **identical to Qwen 4B**.",
        "",
        "| Condition (machine) | Display | Prompt asset |",
        "| :--- | :--- | :--- |",
        "| `ab1` | Ab1 | Same builder as Qwen 4B / Gemini Pilot-02 |",
        "| `ab2g` | Ab2g | Same builder as Qwen 4B / Gemini Pilot-02 |",
        "| `ab2d` | Ab2d+api | Same builder as Qwen 4B / Gemini Pilot-02 |",
        "| `ab2d_spec_v2` | Ab2d+spec-v2 | Frozen `ab2d_spec_v2` files (shared with Qwen 4B) |",
        "",
        "## 2. Locked shared assets",
        "",
        f"- Seeds: `{SEEDS}`",
        f"- Evaluator SHA: `{manifest['evaluator_hash']}`",
        f"- Taxonomy v3 SHA: `{manifest['taxonomy_hash']}`",
        f"- Healer allowlist SHA: `{manifest['healer_allowlist_hash']}`",
        f"- Corrected-chain Healer runner SHA: `{EXPECTED_HEALER_RUNNER_HASH}`",
        f"- Healer protocol SHA: `{EXPECTED_HEALER_PROTOCOL_HASH}`",
        f"- Source commit (at freeze build): `{SOURCE_COMMIT}`",
        f"- Qwen 4B alignment reference: `math16_pilot02_qwen4b_runtime_manifest.json`",
        "",
        "## 3. Sampling rationale",
        "",
        f"> {SAMPLING_RATIONALE}",
        "",
        "## 4. Qwen 9B runtime (queried)",
        "",
    ]
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
    lines += [
        f"- **stop_sequences**: `{runtime['stop_sequences']}` ({runtime['stop_sequences_note']})",
        f"- **retry_policy**: `{json.dumps(runtime['retry_policy'], ensure_ascii=False)}`",
        "",
        "### Thinking mode",
        "",
        "```text",
        "think=false",
        "```",
        "",
        "### Hardware",
        "",
        f"- CPU: `{hw['cpu']}`",
        f"- GPU: `{hw['gpu']}`",
        f"- VRAM: `{hw['vram_mib']} MiB`",
        f"- RAM: `{hw['ram_gib_approx']} GiB` (`{hw['ram_bytes']}` bytes)",
        f"- OS: `{hw['os']}`",
        f"- Driver: `{hw['driver_version']}`",
        "",
        "### Cold / warm",
        "",
        f"- Definition: {runtime['cold_warm']['definition']}",
        f"- Observed at preregistration: **{runtime['cold_warm']['observed_at_preregistration']}**",
        f"- Policy: {runtime['cold_warm']['policy']}",
        "",
        "## 5. Runtime fingerprint",
        "",
        f"- **Qwen 9B fingerprint**: `{manifest['runtime_config_fingerprint']}`",
        f"- **Qwen 4B fingerprint (reference)**: `{manifest['qwen4b_reference_fingerprint']}`",
        "",
        "Fingerprint differs from 4B by model identity fields (tag/digest/parameters/version) "
        "while sharing prompt_manifest_hash, evaluator/taxonomy/healer hashes, seeds, and sampling.",
        "",
        "## 6. Expected cell geometry",
        "",
        "```text",
        "16 tasks × 4 conditions × 5 seeds = 320 cells / model",
        "4 families × 4 tasks × 4 conditions × 5 seeds = 80 cells / family",
        "```",
        "",
        "- 320 unique `cell_id`",
        "- 80 / condition, 80 / family, 20 / task, 64 / seed",
        "- Prompt SHA identical to Qwen 4B for all 16×4 condition/task pairs",
        "",
        "## 7. Prompt SHA registry (16 × 4)",
        "",
        "| Task | Cond | Path | SHA-256 |",
        "| :--- | :--- | :--- | :--- |",
    ]
    for r in prompt_rows:
        path = r.get("prompt_path") or "(builder)"
        lines.append(
            f"| `{r['task_id']}` | `{r['condition']}` | `{path}` | `{r['prompt_sha256']}` |"
        )
    lines += [
        "",
        "## 8. Corrected-chain Healer pins (record only)",
        "",
        f"- Runner: `{EXPECTED_HEALER_RUNNER_HASH}`",
        f"- Protocol: `{EXPECTED_HEALER_PROTOCOL_HASH}`",
        "- This preregistration does **not** execute Healer.",
        "",
        "## 9. Governance",
        "",
        "- No generation in this freeze.",
        "- Resume later: skip only if complete artifact metadata matches plan + fingerprint.",
        "- Mismatch: fail-closed; never overwrite.",
        "- After this freeze, do not switch think/sampling/model digest/prompt SHAs mid-cohort.",
        "",
        "- Runtime manifest: `docs/experiments/manifests/math16_pilot02_qwen9b_runtime_manifest.json`",
        "- Cell plan: `docs/experiments/manifests/math16_pilot02_qwen9b_cell_plan.json`",
        "",
    ]
    OUT_DESIGN.write_text("\n".join(lines), encoding="utf-8", newline="\n")


def main() -> int:
    runtime = query_runtime()
    prompt_rows = build_prompt_registry()
    plan = build_cell_plan(prompt_rows)

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
    assert all(c["model_tag"] == MODEL_TAG for c in plan)
    assert all(c["temperature"] == 0.2 for c in plan)
    assert all(c["top_p"] == 0.8 for c in plan)
    assert all(c["top_k"] == 20 for c in plan)
    assert all(c["think"] is False for c in plan)

    assert_aligned_with_qwen4b(plan, prompt_rows)

    taxonomy_hash = sha_file_raw(TAXONOMY_PATH)
    evaluator_hash = sha_file_raw(EVALUATOR_PATH)
    healer_hash = sha_json(HEALER_ALLOWLIST)
    runner_hash = sha_file_raw(HEALER_RUNNER_PATH)
    protocol_hash = sha_file_raw(HEALER_PROTOCOL_PATH)
    if runner_hash != EXPECTED_HEALER_RUNNER_HASH:
        raise RuntimeError(f"healer runner hash drift: {runner_hash}")
    if protocol_hash != EXPECTED_HEALER_PROTOCOL_HASH:
        raise RuntimeError(f"healer protocol hash drift: {protocol_hash}")

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
    q4_man = json.loads(QWEN4B_MANIFEST.read_text(encoding="utf-8"))
    if prompt_manifest_hash != q4_man["prompt_manifest_hash"]:
        raise RuntimeError("prompt_manifest_hash drift vs Qwen4B")

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
    if fingerprint == q4_man["runtime_config_fingerprint"]:
        raise RuntimeError("9B fingerprint must differ from 4B")

    manifest = {
        **fp_payload,
        "preregistration_status": "FROZEN",
        "study_stage": "pilot02_qwen9b_runtime_preregistration",
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
            "固定Qwen 9B cohort內的推理模式，並與Qwen 4B一致（think=false）；"
            "不宣稱其與Gemini內部推理機制完全等價。"
        ),
        "sampling_rationale": SAMPLING_RATIONALE,
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
        "corrected_chain_healer_runner_sha256": EXPECTED_HEALER_RUNNER_HASH,
        "corrected_chain_healer_protocol_sha256": EXPECTED_HEALER_PROTOCOL_HASH,
        "healer_execution_this_round": False,
        "prompt_verification_registry": prompt_rows,
        "ab2d_spec_v2_api_cards": [
            "FractionOps.create(value)",
            "FractionOps.from_parts(numerator, denominator)",
            "PolynomialOps.format_latex(coeffs, var='x')",
        ],
        "qwen4b_reference_fingerprint": q4_man["runtime_config_fingerprint"],
        "qwen4b_alignment": {
            "prompt_sha_identical": True,
            "sampling_identical": True,
            "cell_geometry_identical": True,
            "model_fields_differ": True,
        },
        "fingerprint_schema_keys": FINGERPRINT_KEYS,
        "output_root": "docs/experiments/results/math16_pilot02_qwen9b",
        "resume_policy": "skip_if_complete_and_metadata_match_else_fail_closed",
        "overwrite_policy": "never",
        "created_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "runtime_config_fingerprint": fingerprint,
        "preflight_probes_only": [
            "/api/version",
            "/api/tags",
            "/api/show",
            "/api/ps",
        ],
        "llm_generation_calls": 0,
        "formal_generation_started": False,
    }

    OUT_RUNTIME.parent.mkdir(parents=True, exist_ok=True)
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
    write_prereg_md(runtime, manifest, prompt_rows)

    print(
        json.dumps(
            {
                "status": "BUILT",
                "cells": len(plan),
                "fingerprint": fingerprint,
                "model_tag": runtime["model_tag"],
                "model_digest": runtime["model_digest"],
                "architecture": runtime["architecture"],
                "parameter_count": runtime["parameter_count"],
                "quantization": runtime["quantization"],
                "runtime_version": runtime["runtime_version"],
                "thinking_mode": False,
                "temperature": 0.2,
                "llm_generation_calls": 0,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
