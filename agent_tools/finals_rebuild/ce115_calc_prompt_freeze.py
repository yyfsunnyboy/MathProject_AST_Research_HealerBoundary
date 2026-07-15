"""CE115 corrected-calc prompt condition freeze (no model calls).

Formal treatments for the four L1 calc tasks:

Ab1  = Task Contract + Frozen Parameters
Ab2g = Math Core Scaffold + Task Contract + Frozen Parameters
Ab2d = Math Core Scaffold + task-local reusable primitive + Task Contract + Frozen Parameters

Prompt text is deterministic UTF-8 with LF newlines. Hashes exclude model identity.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

from agent_tools.finals_rebuild.ab2d_local_prompt import MATH_CORE_SCAFFOLD
from agent_tools.finals_rebuild.ce115_calc_golden_generators import FORMAL_L1_TASK_IDS, formal_l1_tasks
from agent_tools.finals_rebuild.math_answer_contracts import (
    CONTRACTS,
    GENERATION_INSTRUCTIONS,
    NEUTRAL_TASK_STATEMENTS,
    OVERRIDE_STATEMENT,
)
from agent_tools.finals_rebuild.math_task_sampler import sample_task_parameters

FORMAL_CONDITIONS = ("ab1", "ab2g", "ab2d")
FORMAL_SEEDS = (2026071301, 2026071302, 2026071303)
GENERATOR_SUCCESS_SCHEMA_VERSION = "g1_g6_v1"
MANIFEST_VERSION = "ce115_calc_main_experiment_manifest.v1"
FREEZE_SEED_FOR_PROMPT_HASH = 2026071301  # one deterministic payload snapshot for hash tables

# Minimal Ab1/schema wording: return fields only — no solving steps.
AB1_CALC_ANSWER_WORDING: dict[str, str] = {
    "radical_simplification": (
        "correct_answer must be a JSON-compatible dict with exactly coefficient (positive int) "
        "and radicand (square-free int > 1) for simplest radical form. Exact integers only; no floats; "
        "do not alter frozen parameters."
    ),
    "exact_rational_expression": (
        "correct_answer must be a JSON-compatible dict with exactly value (canonical exact rational "
        "string: integer string or irreducible p/q with positive denominator). Exact arithmetic only; "
        "no floats or decimals; do not alter frozen parameters."
    ),
    "polynomial_division_general": (
        "correct_answer must be a JSON-compatible dict with exactly quotient_coefficients "
        "(highest degree first; int or irreducible p/q strings) and remainder_coefficients "
        "(degree lower than the divisor; for a linear divisor, exactly one value). Exact arithmetic; "
        "no floats; do not alter frozen parameters."
    ),
    "polynomial_factor_roots": (
        "correct_answer must be a JSON-compatible dict with exactly roots (two distinct exact rationals "
        "as int or irreducible p/q strings) in ascending numeric order. Exact arithmetic; no floats; "
        "do not alter frozen parameters."
    ),
}

# One task-local reusable primitive per calc skill_id. No answer constants / solvers.
CALC_TASK_LOCAL_PRIMITIVES: dict[str, str] = {
    "radical_simplification": (
        "RadicalOps.simplify / RadicalOps.simplify_term may be used to extract square factors.\n"
        "Keep exact integers. Return only the coefficient and square-free radicand required by the "
        "task contract."
    ),
    "exact_rational_expression": (
        "Use fractions.Fraction or FractionOps for exact decimal-string operands.\n"
        "Accumulate sign * left * right exactly. Return a reduced canonical value string; do not use float."
    ),
    "polynomial_division_general": (
        "Use PolynomialOps.div_qr(dividend_coefficients, divisor_coefficients).\n"
        "Coefficients are highest degree first. Keep exact arithmetic. Return quotient_coefficients and "
        "remainder_coefficients exactly as required by the task contract."
    ),
    "polynomial_factor_roots": (
        "Factor or solve the quadratic over the rationals with exact arithmetic.\n"
        "Return exactly two distinct roots in ascending numeric order as required by the task contract. "
        "Do not add linear-combination fields."
    ),
}


def normalize_prompt_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def prompt_sha256(text: str) -> str:
    """SHA-256 of newline-normalized UTF-8 prompt bytes. Model name must not be hashed in."""
    return hashlib.sha256(normalize_prompt_newlines(text).encode("utf-8")).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def render_calc_task_contract(task: Mapping[str, Any]) -> str:
    """Shared task contract (no frozen parameters). Used byte-identically by Ab1/Ab2g/Ab2d."""
    oracle_type = task["oracle_type"]
    if oracle_type not in CONTRACTS or oracle_type not in AB1_CALC_ANSWER_WORDING:
        raise ValueError(f"unsupported calc oracle_type: {oracle_type!r}")
    parts = [
        NEUTRAL_TASK_STATEMENTS[oracle_type].strip(),
        GENERATION_INSTRUCTIONS.strip(),
        OVERRIDE_STATEMENT.strip(),
        CONTRACTS[oracle_type].strip(),
        "Ab1 answer-contract wording:\n" + AB1_CALC_ANSWER_WORDING[oracle_type],
    ]
    return "\n\n".join(parts) + "\n"


def render_frozen_parameters_section(frozen_parameters: Mapping[str, Any]) -> str:
    frozen = json.dumps(dict(frozen_parameters), ensure_ascii=False, sort_keys=True)
    return (
        "## Frozen parameters\n"
        f"{frozen}\n"
        "`oracle_payload` must exactly equal the frozen parameters above; do not change any value.\n"
    )


def assemble_ab1_calc_prompt(task_contract: str, frozen_parameters: Mapping[str, Any]) -> str:
    return normalize_prompt_newlines(
        f"## Task contract\n{task_contract.strip()}\n\n{render_frozen_parameters_section(frozen_parameters)}"
    )


def assemble_ab2g_calc_prompt(task_contract: str, frozen_parameters: Mapping[str, Any]) -> str:
    return normalize_prompt_newlines(
        f"{MATH_CORE_SCAFFOLD}\n"
        f"## Task contract\n{task_contract.strip()}\n\n"
        f"{render_frozen_parameters_section(frozen_parameters)}"
    )


def assemble_ab2d_calc_prompt(
    task_family: str,
    task_contract: str,
    frozen_parameters: Mapping[str, Any],
) -> str:
    try:
        primitive = CALC_TASK_LOCAL_PRIMITIVES[task_family]
    except KeyError as exc:
        raise ValueError(f"unsupported Ab2d calc task family: {task_family!r}") from exc
    return normalize_prompt_newlines(
        f"{MATH_CORE_SCAFFOLD}\n"
        f"## Task-local domain primitive: {task_family}\n{primitive}\n\n"
        f"## Task contract\n{task_contract.strip()}\n\n"
        f"{render_frozen_parameters_section(frozen_parameters)}"
    )


def build_condition_prompt(
    condition: str,
    task: Mapping[str, Any],
    frozen_parameters: Mapping[str, Any],
) -> str:
    contract = render_calc_task_contract(task)
    if condition == "ab1":
        return assemble_ab1_calc_prompt(contract, frozen_parameters)
    if condition == "ab2g":
        return assemble_ab2g_calc_prompt(contract, frozen_parameters)
    if condition == "ab2d":
        return assemble_ab2d_calc_prompt(task["skill_id"], contract, frozen_parameters)
    raise ValueError(f"unsupported condition: {condition!r}")


def strip_ab2d_primitive_section(prompt: str) -> str:
    """Remove the single task-local primitive block so Ab2d remainder must equal Ab2g."""
    marker = "## Task-local domain primitive:"
    contract_marker = "## Task contract"
    if marker not in prompt or contract_marker not in prompt:
        raise ValueError("Ab2d prompt missing expected section markers")
    head, _, tail = prompt.partition(marker)
    _, _, after = tail.partition(contract_marker)
    return normalize_prompt_newlines(head + contract_marker + after)


def build_all_formal_prompts(
    *,
    seed: int = FREEZE_SEED_FOR_PROMPT_HASH,
) -> dict[str, dict[str, str]]:
    """Return {task_id: {condition: prompt}} for the formal 4×3 lattice."""
    tasks = formal_l1_tasks()
    out: dict[str, dict[str, str]] = {}
    for task_id in FORMAL_L1_TASK_IDS:
        task = tasks[task_id]
        payload = sample_task_parameters(task, seed)["oracle_payload"]
        out[task_id] = {
            condition: build_condition_prompt(condition, task, payload)
            for condition in FORMAL_CONDITIONS
        }
    return out


def build_prompt_hash_table(prompts: Mapping[str, Mapping[str, str]]) -> dict[str, dict[str, str]]:
    return {
        task_id: {condition: prompt_sha256(text) for condition, text in conds.items()}
        for task_id, conds in prompts.items()
    }


def assert_no_leakage(prompt: str) -> None:
    lowered = prompt.lower()
    for token in ("expected_answer", "oracle_expected", "healer", "chain-of-thought", "self-correct"):
        if token in lowered:
            raise ValueError(f"forbidden token in prompt: {token}")
    for token in ("504", "98.7", "2.45", "0.55", "2961/10"):
        if token in prompt:
            raise ValueError(f"CAP exemplar leaked into prompt: {token}")


# Formal confirmatory Ollama request profile (chat runners). Values must come from
# actual request payloads — never from Modelfile / model-card defaults.
CONFIRMATORY_MODEL_KEYS = ("qwen35_4b", "qwen35_9b")

# Prompt hashes frozen before Qwen3.5 cohort revision (Milestone 3B/3C). Must remain
# byte-identical after model metadata changes.
FROZEN_PROMPT_HASHES_PRE_QWEN35 = {
    "ce115_calc_exact_rational_expression_l1": {
        "ab1": "34a72807672bcad00bea4fa096a228fa1005ffed0e8b3a092ac601e48a129092",
        "ab2d": "02b85a4a7e84a4ac9128efdcec0fde15bb140cedf850a752dd94f539a28f0fd6",
        "ab2g": "7e4b23fffc6efadb9b498673decb919449611b5f7d4f2451871d64cdd915a16f",
    },
    "ce115_calc_polynomial_division_l1": {
        "ab1": "020aa035d92953e308fff3e54d27642ad65687caed82e85953b793acb1a22b34",
        "ab2d": "abaa7b2db17a7cce21f34891454f9e9cac770304e3d7b28876d56f2e2a7a970a",
        "ab2g": "34db6c9fe7dc92ea4e70709dfd551b755f8e88be2bd5fc8da1c0dffae8b1d684",
    },
    "ce115_calc_polynomial_factor_roots_l1": {
        "ab1": "2c1238641013986ffbae4e28374c5c03e1e76da93ae0b394c82e69c5b4f88e6e",
        "ab2d": "5293a8bb69cccc516eebf49454b7b57dc53c0d449458279616ce66836ff0281d",
        "ab2g": "52ea9267bb10bd1b3b3e5fe28ac051f9e9a3ef0947889cb077d61ffaee0adf49",
    },
    "ce115_calc_radical_simplification_l1": {
        "ab1": "4cc44a9bbc9db716fbd66a4e295a4448fca51013ea9229d2ea2403d76c8752d8",
        "ab2d": "f8e17b48d773e8e317dedd600e47a8b9d8d168eec5872ce503524ec52439a9cf",
        "ab2g": "e464126f0386fc01a668cd477b219b121a0bb8a771a236085000dd8e0d8743b8",
    },
}

CONFIRMATORY_LOCAL_OLLAMA_EVIDENCE = (
    "agent_tools/finals_rebuild/ce115_calc_formal_runner.py",
    "agent_tools/finals_rebuild/ce115_calc_run_plan.py",
    "docs/experiments/healer_boundary_execution_log.md",
)
OLLAMA_SHOW_CROSSCHECK_EVIDENCE = (
    "ollama --version → 0.32.0",
    "ollama show qwen3.5:4b / qwen3.5:9b (Milestone 3R1 provenance)",
    "external qualification C:\\Temp\\qwen35_thinking_qualification (2026-07-15)",
)
GEMINI_EXPLORATORY_EVIDENCE = (
    "scripts/run_gemini_ab2g_math_core_qualification.py",
    "scripts/run_gemini_ab1_ab2d_diagnostic.py",
    "config.py",
    "core/ai_wrapper.py",
    "docs/experiments/ab2g_math_core_qualification_design_20260714.md",
)

# Paths under which UNRESOLVED blocks local confirmatory freeze.
_LOCAL_UNRESOLVED_PREFIXES = (
    "models.qwen35_4b.",
    "models.qwen35_9b.",
    "seeds.",
    "formal_task_ids",
    "prompt_conditions",
    "cell_geometry.confirmatory_local_cell_count",
    "cell_counts.confirmatory_local_cell_count",
    "request_count",
    "retry_count",
    "artifact_output_naming_rule",
    "run_inclusion_exclusion_policy",
)


def _confirmatory_ollama_sampling() -> dict[str, Any]:
    """Shared Qwen3.5 4B/9B request-options semantics for formal confirmatory chat cells."""
    return {
        "api": "/api/chat",
        "temperature": 0.0,
        "seed_binding": "per_cell_repeat_seed",
        "think": False,
        "top_p": "not_explicitly_set",
        "top_k": "not_explicitly_set",
        "presence_penalty": "not_explicitly_set",
        "num_predict": "not_explicitly_set",
        "request_explicit_settings": {
            "temperature": 0.0,
            "seed_binding": "per_cell_repeat_seed",
            "think": False,
        },
        "request_not_explicitly_set": {
            "top_p": "not_explicitly_set",
            "top_k": "not_explicitly_set",
            "presence_penalty": "not_explicitly_set",
            "num_predict": "not_explicitly_set",
        },
        "observed_model_defaults": {
            "temperature": 1,
            "top_k": 20,
            "top_p": 0.95,
            "presence_penalty": 1.5,
        },
        "effective_temperature_source": "request_override",
        "unset_options_rely_on": "ollama_runtime_default",
        "runtime_default_note": (
            "top_p, top_k, presence_penalty, and num_predict are omitted from "
            "confirmatory chat option payloads; Modelfile PARAMETER defaults are "
            "recorded separately and must not be copied into the request."
        ),
        "evidence_sources": list(CONFIRMATORY_LOCAL_OLLAMA_EVIDENCE) + list(OLLAMA_SHOW_CROSSCHECK_EVIDENCE),
    }


def _confirmatory_ollama_thinking() -> dict[str, Any]:
    return {
        "thinking_capability": "supported",
        "capability_listed_by_ollama_show": True,
        "thinking_requested": False,
        "requested": False,
        "thinking_policy": "explicit_think_false",
        "request_parameter_sent": False,
        "qualification_result": "THINK_FALSE_CLEAN",
        "qualification_scope": "external_nonformal_6_call_test",
        "qualification_evidence_path": r"C:\Temp\qwen35_thinking_qualification",
        "qualification_date": "2026-07-15",
        "effective": "formal_request_think_false",
        "policy": (
            "Formal local confirmatory requests MUST send top-level think=false. "
            "Capability listing does not imply enablement. External qualification "
            "supports THINK_FALSE_CLEAN but does not prove perpetual zero-leakage."
        ),
        "evidence_sources": list(OLLAMA_SHOW_CROSSCHECK_EVIDENCE),
    }


def _historical_qwen3_cohort() -> dict[str, Any]:
    """Prior confirmatory models retained for provenance only — not in new 72-cell plan."""
    return {
        "qwen3_4b_instruct_2507_q4_k_m": {
            "model_tag": "qwen3:4b-instruct-2507-q4_K_M",
            "model_digest": "0edcdef34593",
            "digest": "0edcdef34593",
            "parameters": "4.0B",
            "quantization": "Q4_K_M",
            "runtime": "Ollama",
            "runtime_version_recorded": "0.31.2",
            "cohort_role": "historical_mechanism_pilot",
            "included_in_new_confirmatory": False,
            "included_in_formal_confirmatory_analysis": False,
            "note": "Historical metadata preserved; do not rewrite old artifact metadata.",
        },
        "qwen3_8b": {
            "model_tag": "qwen3:8b",
            "model_digest": "500a1f067a9f",
            "digest": "500a1f067a9f",
            "parameters": "8.2B",
            "quantization": "Q4_K_M",
            "architecture": "qwen3",
            "context_length": 40960,
            "runtime": "Ollama",
            "runtime_version_recorded": "0.31.2",
            "cohort_role": "historical_mechanism_pilot",
            "included_in_new_confirmatory": False,
            "included_in_formal_confirmatory_analysis": False,
            "note": "Historical metadata preserved; do not rewrite old artifact metadata.",
        },
    }


def model_registry_snapshot() -> dict[str, Any]:
    """Resolved vs unresolved model metadata for the formal manifest (no live probes)."""
    sampling = _confirmatory_ollama_sampling()
    thinking = _confirmatory_ollama_thinking()
    return {
        "qwen35_4b": {
            "model_tag": "qwen3.5:4b",
            "model_digest": "2a654d98e6fb",
            "digest": "2a654d98e6fb",
            "architecture": "qwen35",
            "parameter_count_reported": "4.7B",
            "parameters": "4.7B",
            "ollama_tag_size_class": "4b",
            "model_size": "3.4 GB",
            "quantization": "Q4_K_M",
            "context_length_reported": 262144,
            "context_length": 262144,
            "embedding_length": 2560,
            "capabilities": ["completion", "vision", "tools", "thinking"],
            "model_requires": "0.17.1",
            "runtime": "Ollama",
            "runtime_version": "0.32.0",
            "cohort_role": "local_confirmatory",
            "role": "confirmatory_local",
            "edge_tier": "edge-small",
            "included_in_formal_confirmatory_analysis": True,
            "included_in_formal_analysis": True,
            "sampling": sampling,
            "thinking": thinking,
            "evidence_sources": list(CONFIRMATORY_LOCAL_OLLAMA_EVIDENCE) + list(OLLAMA_SHOW_CROSSCHECK_EVIDENCE),
        },
        "qwen35_9b": {
            "model_tag": "qwen3.5:9b",
            "model_digest": "6488c96fa5fa",
            "digest": "6488c96fa5fa",
            "architecture": "qwen35",
            "parameter_count_reported": "9.7B",
            "parameters": "9.7B",
            "ollama_tag_size_class": "9b",
            "model_size": "6.6 GB",
            "quantization": "Q4_K_M",
            "context_length_reported": 262144,
            "context_length": 262144,
            "embedding_length": 4096,
            "capabilities": ["completion", "vision", "tools", "thinking"],
            "model_requires": "0.17.1",
            "runtime": "Ollama",
            "runtime_version": "0.32.0",
            "cohort_role": "local_confirmatory",
            "role": "confirmatory_local",
            "edge_tier": "edge-large",
            "included_in_formal_confirmatory_analysis": True,
            "included_in_formal_analysis": True,
            "sampling": dict(sampling),
            "thinking": dict(thinking),
            "evidence_sources": list(CONFIRMATORY_LOCAL_OLLAMA_EVIDENCE) + list(OLLAMA_SHOW_CROSSCHECK_EVIDENCE),
        },
        "historical_cohort": _historical_qwen3_cohort(),
        "gemini": {
            "provider": "google",
            "analysis_role": "exploratory_optional_cloud_comparison",
            "confirmatory_or_exploratory": "exploratory",
            "included_in_formal_confirmatory_analysis": False,
            "included_in_local_confirmatory_freeze": False,
            "runner_model_tag": "gemini-3.5-flash",
            "model_tag": "gemini-3.5-flash",
            "config_preset_key": "gemini-3-flash",
            "config_preset_model_field": "gemini-3-flash-preview",
            "exact_api_model_identifier": "UNRESOLVED",
            "exact_version_string": "UNRESOLVED",
            "sdk_api_version": "UNRESOLVED",
            "sampling": {
                "temperature": 0.1,
                "max_output_tokens": 4096,
                "max_tokens": 4096,
                "top_p": "not_explicitly_set",
                "top_k": "not_explicitly_set",
                "seed": "unavailable",
                "seed_policy": (
                    "Gemini qualification runners bind a ledger seed field but do not "
                    "pass seed into GenerateContentConfig."
                ),
                "evidence_note": (
                    "temperature 0.1 from Config.CODER_PRESETS['gemini-3-flash']; "
                    "max_tokens overridden to 4096 in Gemini qualification runners; "
                    "ai_wrapper sends temperature + max_output_tokens only."
                ),
            },
            "thinking": {
                "requested": "not_explicitly_set",
                "effective": "not_explicitly_set",
                "policy": (
                    "No think/thinking fields present in GenerateContentConfig construction. "
                    "Gemini thinking is not equated to Ollama think=false policy."
                ),
            },
            "intended_task_x_condition_x_seed_cell_count": "UNRESOLVED",
            "evidence_sources": list(GEMINI_EXPLORATORY_EVIDENCE),
        },
    }


def collect_unresolved(node: Any, path: str = "") -> list[str]:
    found: list[str] = []
    if node == "UNRESOLVED":
        found.append(path or "$")
    elif isinstance(node, dict):
        for key, value in node.items():
            found.extend(collect_unresolved(value, f"{path}.{key}" if path else key))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            found.extend(collect_unresolved(value, f"{path}[{index}]"))
    return found


def is_local_confirmatory_path(path: str) -> bool:
    if path in {
        "formal_task_ids",
        "prompt_conditions",
        "request_count",
        "retry_count",
        "artifact_output_naming_rule",
        "run_inclusion_exclusion_policy",
        "cell_geometry.confirmatory_local_cell_count",
        "cell_counts.confirmatory_local_cell_count",
    }:
        return True
    return any(path.startswith(prefix) for prefix in _LOCAL_UNRESOLVED_PREFIXES)


def partition_unresolved(unresolved: list[str]) -> tuple[list[str], list[str]]:
    local = [p for p in unresolved if is_local_confirmatory_path(p)]
    other = [p for p in unresolved if p not in local]
    return local, other


def compute_freeze_flags(unresolved: list[str]) -> dict[str, Any]:
    local_unresolved, other_unresolved = partition_unresolved(unresolved)
    gemini_blocking = [p for p in other_unresolved if p.startswith("models.gemini.") or "exploratory_cloud" in p or "total_planned" in p or "gemini_cells" in p]
    local_frozen = len(local_unresolved) == 0
    gemini_frozen = len(gemini_blocking) == 0
    fully_frozen = len(unresolved) == 0
    if fully_frozen:
        verdict = "FROZEN"
    elif local_frozen and not gemini_frozen:
        verdict = "LOCAL CONFIRMATORY FROZEN"
    elif not local_frozen:
        verdict = "NOT READY — LOCAL BLOCKERS REMAIN"
    else:
        verdict = "PARTIALLY FROZEN — GEMINI UNRESOLVED"
    return {
        "local_confirmatory_frozen": local_frozen,
        "gemini_exploratory_frozen": gemini_frozen,
        "frozen": fully_frozen,
        "freeze_verdict": verdict,
        "local_unresolved_fields": local_unresolved,
        "gemini_or_other_unresolved_fields": other_unresolved,
    }


def build_run_manifest(
    *,
    git_commit: str,
    prompts: Mapping[str, Mapping[str, str]] | None = None,
) -> dict[str, Any]:
    prompts = prompts or build_all_formal_prompts()
    hash_table = build_prompt_hash_table(prompts)
    if hash_table != FROZEN_PROMPT_HASHES_PRE_QWEN35:
        raise ValueError(
            "prompt hash table drifted across cohort revision; "
            "prompt text/contract/primitives must remain unchanged"
        )
    root = Path(__file__).resolve().parents[2]
    task_manifest_path = root / "tests" / "finals_rebuild" / "fixtures" / "math_generation_tasks_ce115_pilot.jsonl"
    models = model_registry_snapshot()
    local_cell_count = len(FORMAL_L1_TASK_IDS) * len(FORMAL_CONDITIONS) * len(FORMAL_SEEDS) * 2
    component_hashes = {
        "math_core_scaffold": prompt_sha256(MATH_CORE_SCAFFOLD),
        "task_manifest": file_sha256(task_manifest_path),
        "calc_task_local_primitives": {
            skill: prompt_sha256(text) for skill, text in CALC_TASK_LOCAL_PRIMITIVES.items()
        },
        "ab1_calc_answer_wording": {
            oracle: prompt_sha256(text) for oracle, text in AB1_CALC_ANSWER_WORDING.items()
        },
    }
    # Shared contract hashes per task (independent of condition)
    tasks = formal_l1_tasks()
    task_contract_hashes = {}
    for task_id in FORMAL_L1_TASK_IDS:
        contract = render_calc_task_contract(tasks[task_id])
        task_contract_hashes[task_id] = prompt_sha256(contract)

    evidence_paths = sorted(
        {
            *CONFIRMATORY_LOCAL_OLLAMA_EVIDENCE,
            *GEMINI_EXPLORATORY_EVIDENCE,
            "docs/experiments/manifests/ce115_calc_main_experiment_manifest.json",
            "agent_tools/finals_rebuild/ce115_calc_prompt_freeze.py",
            "tests/finals_rebuild/fixtures/math_generation_tasks_ce115_pilot.jsonl",
        }
    )

    manifest = {
        "manifest_version": MANIFEST_VERSION,
        "created_date": "2026-07-15",
        "git_commit": git_commit,
        "frozen": False,
        "local_confirmatory_frozen": False,
        "gemini_exploratory_frozen": False,
        "freeze_verdict": "NOT READY — LOCAL BLOCKERS REMAIN",
        "formal_task_ids": list(FORMAL_L1_TASK_IDS),
        "legacy_task_ids_excluded": True,
        "prompt_conditions": list(FORMAL_CONDITIONS),
        "condition_definitions": {
            "ab1": "Task Contract + Frozen Parameters",
            "ab2g": "Math Core Scaffold + Task Contract + Frozen Parameters",
            "ab2d": "Math Core Scaffold + task-local reusable primitive + Task Contract + Frozen Parameters",
        },
        "prompt_section_order": {
            "ab1": ["task_contract", "frozen_parameters"],
            "ab2g": ["math_core_scaffold", "task_contract", "frozen_parameters"],
            "ab2d": ["math_core_scaffold", "task_local_primitive", "task_contract", "frozen_parameters"],
        },
        "newline_encoding": {"newline": "LF", "encoding": "UTF-8"},
        "component_hashes": component_hashes,
        "task_contract_hashes": task_contract_hashes,
        "per_task_prompt_hashes": hash_table,
        "prompt_hash_seed": FREEZE_SEED_FOR_PROMPT_HASH,
        "task_manifest_path": str(task_manifest_path.relative_to(root)).replace("\\", "/"),
        "task_manifest_hash": component_hashes["task_manifest"],
        "oracle_evaluator": {
            "module": "agent_tools.finals_rebuild.math_task_oracles",
            "bound_to_git_commit": git_commit,
        },
        "generator_success_schema_version": GENERATOR_SUCCESS_SCHEMA_VERSION,
        "seeds": {
            "formal_seeds": list(FORMAL_SEEDS),
            "policy": "fresh formal seeds only; historical failing cells are not substitutes",
        },
        "models": models,
        "cell_counts": {
            "confirmatory_local_cell_count": local_cell_count,
            "exploratory_cloud_cell_count": "UNRESOLVED",
            "total_planned_cell_count": "UNRESOLVED",
            "formula_local": "4 tasks × 3 conditions × 3 seeds × 2 local models = 72",
        },
        "cell_geometry": {
            "tasks": len(FORMAL_L1_TASK_IDS),
            "conditions": len(FORMAL_CONDITIONS),
            "seeds": len(FORMAL_SEEDS),
            "primary_local_models": 2,
            "confirmatory_local_cell_count": local_cell_count,
            "expected_primary_local_cells": local_cell_count,
            "exploratory_cloud_cell_count": "UNRESOLVED",
            "total_planned_cell_count": "UNRESOLVED",
            "gemini_cells": "UNRESOLVED",
        },
        "request_count": 1,
        "retry_count": 0,
        "first_attempt_is_ITT": True,
        "healer_enabled": False,
        "run_inclusion_exclusion_policy": {
            "include": "first-attempt observed ledger only for included_in_formal_analysis=true model runs",
            "exclude": [
                "infrastructure_dry_run",
                "synthetic_golden_no_model",
                "pipeline_corrected ledger rows as primary ITT claims",
                "post_healer ledger rows as primary ITT claims",
                "legacy non-ce115_calc_* task IDs",
            ],
        },
        "artifact_output_naming_rule": (
            "docs/experiments/results/ce115_calc_{provider}_{model_label}_{condition}_"
            "seed_{seed}_git_{short_sha}.jsonl"
        ),
        "evidence_paths": evidence_paths,
        "local_confirmatory_cohort": "qwen3.5:4b+qwen3.5:9b",
        "frozen_prompt_hashes_baseline": "FROZEN_PROMPT_HASHES_PRE_QWEN35",
        "provenance_resolution_notes": {
            "sampling_authority": "actual runner request payload only",
            "legal_explicit_non_numeric_values": ["runtime_default", "not_explicitly_set", "unavailable"],
            "request_vs_defaults": (
                "request_explicit_settings vs request_not_explicitly_set vs "
                "observed_model_defaults must remain layered; defaults are never copied into payloads"
            ),
            "ollama_thinking_rule": "formal requests send think=false; capability ≠ perpetual zero-leakage",
            "gemini_role_rule": "exploratory optional; does not expand confirmatory 72 cells",
            "historical_cohort_rule": "qwen3:4b-instruct / qwen3:8b retained as historical_mechanism_pilot only",
        },
    }
    unresolved = collect_unresolved(manifest)
    flags = compute_freeze_flags(unresolved)
    manifest["unresolved_fields"] = unresolved
    manifest["local_unresolved_fields"] = flags["local_unresolved_fields"]
    manifest["gemini_or_other_unresolved_fields"] = flags["gemini_or_other_unresolved_fields"]
    manifest["local_confirmatory_frozen"] = flags["local_confirmatory_frozen"]
    manifest["gemini_exploratory_frozen"] = flags["gemini_exploratory_frozen"]
    manifest["frozen"] = flags["frozen"]
    manifest["freeze_verdict"] = flags["freeze_verdict"]
    return manifest


def write_run_manifest(path: Path, *, git_commit: str) -> dict[str, Any]:
    manifest = build_run_manifest(git_commit=git_commit)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest
