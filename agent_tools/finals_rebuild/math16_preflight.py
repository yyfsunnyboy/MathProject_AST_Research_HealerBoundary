"""No-model preflight for Math16-LaTeX-v1 (oracle/contract/prompt/G6; no Gemini calls)."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from agent_tools.finals_rebuild.ce115_clean_incremental_ablation import (
    DOMAIN_BUDGET,
    LINEAGE_ID,
    TASK_DOMAIN_APIS,
    assert_clean_ablation_invariants,
    build_condition_prompt,
    canonical_prompt_hash,
    domain_section,
    prompt_sha256,
)
from agent_tools.finals_rebuild.domain_api_ssot import (
    DOMAIN_API_SSOT, render_api_prompt_line, validate_inventory,
)
from agent_tools.finals_rebuild.domain_answer_assembly import TASK_OUTPUT_ASSEMBLY
from agent_tools.finals_rebuild.git_blob_hash import (
    normalize_to_lf,
    sha256_bytes,
    sha256_git_blob_lf,
)
from core.prompts.domain_function_library import PolynomialOps
from agent_tools.finals_rebuild.generator_success import evaluate_math_notation
from agent_tools.finals_rebuild.math16_oracles import (
    compound_radicals_equal,
    normalize_compound_radical,
)
from agent_tools.finals_rebuild.math16_pool import (
    POOL_ID,
    SEED,
    build_pool_manifest,
    domain_ops_distribution,
    frozen_for_prompt,
    write_pool_manifest,
)
from agent_tools.finals_rebuild.math_answer_contracts import CONTRACTS, render_answer_contract
from agent_tools.finals_rebuild.math_task_oracles import evaluate_math_task_oracle
from agent_tools.finals_rebuild.math_task_sampler import sample_task_parameters

ROOT = Path(__file__).resolve().parents[2]
CONDITIONS = ("ab1", "ab2g", "ab2d")


def _file_sha(path: Path) -> str:
    return sha256_git_blob_lf(path, repo_root=ROOT)


def _component_hashes() -> dict[str, str]:
    paths = {
        "toolbox_domain_function_library": ROOT / "core/prompts/domain_function_library.py",
        "evaluator_math_task_oracles": ROOT / "agent_tools/finals_rebuild/math_task_oracles.py",
        "evaluator_math16_oracles": ROOT / "agent_tools/finals_rebuild/math16_oracles.py",
        "healer_protocol": ROOT / "agent_tools/finals_rebuild/ce115_research_healer_protocol.py",
        "clean_incremental_ablation": ROOT / "agent_tools/finals_rebuild/ce115_clean_incremental_ablation.py",
        "domain_api_ssot": ROOT / "agent_tools/finals_rebuild/domain_api_ssot.py",
        "math_answer_contracts": ROOT / "agent_tools/finals_rebuild/math_answer_contracts.py",
        "math16_pool": ROOT / "agent_tools/finals_rebuild/math16_pool.py",
    }
    skills_dir = ROOT / "agent_skills"
    skill_files = sorted(skills_dir.rglob("skill.json")) if skills_dir.exists() else []
    skill_blob = b"".join(normalize_to_lf(path.read_bytes()) for path in skill_files)
    out = {name: _file_sha(path) for name, path in paths.items()}
    out["skills_snapshot"] = sha256_bytes(skill_blob) if skill_files else "NO_SKILLS"
    return out


def run_math16_preflight(*, write_manifest: bool = True) -> dict[str, Any]:
    if write_manifest:
        manifest = write_pool_manifest(ROOT)
    else:
        manifest = build_pool_manifest()

    tasks = manifest["tasks"]
    checks: dict[str, Any] = {}
    blockers: list[str] = []

    dist = domain_ops_distribution(tasks)
    checks["domain_ops_4_4_4_4"] = dist == {
        "PolynomialOps": 4,
        "IntegerOps": 4,
        "FractionOps": 4,
        "RadicalOps": 4,
    }
    if not checks["domain_ops_4_4_4_4"]:
        blockers.append(f"domain_ops_distribution={dist}")

    checks["task_count_16"] = len(tasks) == 16
    checks["no_year_114"] = all(t.get("year_source") != "114" for t in tasks)
    checks["pool_id"] = manifest.get("pool_id") == POOL_ID

    q08 = next(t for t in tasks if t["task_id"] == "ce111_q08_polynomial_factor_parameter_recovery")
    checks["q08_correct_params"] = q08["oracle_payload"] == {
        "a": 2,
        "b": 13,
        "c": -7,
        "expanded_check": [39, 5, -14],
    } and q08["correct_answer"] == -12
    checks["q08_strict_factor_order"] = (
        q08.get("factor_order_policy") == "strict_source_template"
        and q08["frozen_params"].get("factor_order_policy") == "strict_source_template"
    )
    checks["q08_no_legacy_wrong"] = (
        q08["provenance"].get("forbidden_legacy_wrong_values")
        == {"a": -2, "c": 7, "answer": 12}
    )

    q12 = next(t for t in tasks if t["task_id"] == "ce112_q12_independent_probability_fraction")
    checks["q12_substantial_abstraction"] = (
        q12["provenance"].get("transformation_level") == "substantial_abstraction"
    )

    q11 = next(t for t in tasks if t["task_id"] == "ce113_q11_rationalize_denominator")
    checks["q11_reuse_rerun"] = q11.get("reuse_policy") == "rerun"

    q10 = next(t for t in tasks if t["task_id"] == "ce111_q10_ordered_quadratic_roots_radical")
    larger = normalize_compound_radical(q10["oracle_payload"]["larger_root"])
    smaller = normalize_compound_radical(q10["oracle_payload"]["smaller_root"])
    checks["q10_compound_signed_coeffs"] = larger[1] == 1 and smaller[1] == -1
    checks["q10_nested_payload"] = "larger_root" in q10["oracle_payload"] and "smaller_root" in q10[
        "oracle_payload"
    ]

    # Layering: correct_answer vs oracle_payload
    layering_ok = True
    for task in tasks:
        if task["task_id"] == "ce111_q02_polynomial_division_remainder":
            if "quotient" in (task["correct_answer"] or {}):
                layering_ok = False
            if "quotient" not in task["oracle_payload"]:
                layering_ok = False
        if task["task_id"] == "ce111_q10_ordered_quadratic_roots_radical":
            if "larger_root" in (task["correct_answer"] or {}):
                layering_ok = False
    checks["correct_answer_oracle_payload_layering"] = layering_ok

    # Sampler identity + oracle golden
    oracle_failures: list[str] = []
    latex_failures: list[str] = []
    contract_failures: list[str] = []
    domain_failures: list[str] = []
    prompt_rows: list[dict[str, Any]] = []

    for task in tasks:
        tid = task["task_id"]
        sampled = sample_task_parameters(
            {
                "task_id": tid,
                "domain": task["domain"],
                "skill_id": task["skill_id"],
                "oracle_type": task["oracle_type"],
                "difficulty_level": task["difficulty_level"],
                "parameter_ranges": task["parameter_ranges"],
            },
            SEED,
        )
        if sampled["oracle_payload"] != task["frozen_params"]:
            oracle_failures.append(f"{tid}:sampler_identity")

        # Evaluator uses audit-capable oracle_payload; prompt freeze uses frozen_params.
        verdict = evaluate_math_task_oracle(
            task["oracle_type"], task["oracle_payload"], task["correct_answer"]
        )
        if not verdict.get("is_correct"):
            oracle_failures.append(f"{tid}:oracle:{verdict.get('error')}")

        if task["oracle_type"] not in CONTRACTS:
            contract_failures.append(f"{tid}:missing_contract")
        else:
            try:
                render_answer_contract(task, task["oracle_payload"])
            except ValueError as exc:
                contract_failures.append(f"{tid}:contract:{exc}")

        g6 = evaluate_math_notation(task["math16_question_text"])
        if g6.get("status") != "PASS":
            latex_failures.append(f"{tid}:g6:{g6.get('reason')}")
        if r"\(" not in task["math16_question_text"] and r"\[" not in task["math16_question_text"]:
            latex_failures.append(f"{tid}:missing_latex_delimiters")

        if tid not in TASK_DOMAIN_APIS:
            domain_failures.append(f"{tid}:missing_domain_api")
        else:
            section = domain_section(tid)
            if not (DOMAIN_BUDGET[0] <= len(section) <= DOMAIN_BUDGET[1]):
                domain_failures.append(f"{tid}:domain_budget:{len(section)}")

        frozen = frozen_for_prompt(task)
        prompts = assert_clean_ablation_invariants(task, frozen)
        for condition in CONDITIONS:
            prompt = prompts[condition]
            prompt_rows.append(
                {
                    "task_id": tid,
                    "condition": condition,
                    "prompt_sha256": prompt_sha256(prompt),
                    "canonical_prompt_hash": canonical_prompt_hash(prompt),
                    "chars": len(prompt),
                }
            )

    # Targeted compound radical negatives / JSON round-trip
    compound_ok = True
    try:
        pos = evaluate_math_task_oracle(
            "compound_radical_result",
            q10["oracle_payload"],
            q10["correct_answer"],
        )
        neg_coeff = evaluate_math_task_oracle(
            "compound_radical_result",
            q10["oracle_payload"],
            {
                "result": {
                    "rational": 6,
                    "radical_coefficient": -1,
                    "radicand": 3,
                    "canonical_latex": r"6-\sqrt{3}",
                }
            },
        )
        nested = json.loads(json.dumps(q10["oracle_payload"], ensure_ascii=False))
        roundtrip = evaluate_math_task_oracle(
            "compound_radical_result", nested, q10["correct_answer"]
        )
        compound_ok = (
            pos["is_correct"]
            and not neg_coeff["is_correct"]
            and roundtrip["is_correct"]
            and compound_radicals_equal(q10["correct_answer"], q10["correct_answer"])
            and normalize_compound_radical(q10["oracle_payload"]["smaller_root"])[1] == -1
        )
    except Exception as exc:  # noqa: BLE001
        compound_ok = False
        blockers.append(f"compound_radical:{exc}")
    checks["compound_radical_support"] = compound_ok

    # Legacy wrong answer rejected for 111-8
    wrong08 = evaluate_math_task_oracle(
        "polynomial_factor_parameter_recovery",
        q08["oracle_payload"],
        12,
    )
    checks["q08_rejects_legacy_12"] = wrong08.get("is_correct") is False

    # Domain API SSOT: registry ↔ prompt text ↔ runtime return shape (factor).
    ssot_failures: list[str] = list(validate_inventory())
    task_ids = {t["task_id"] for t in tasks}
    if set(TASK_OUTPUT_ASSEMBLY) != task_ids:
        ssot_failures.append("task_output_assembly_coverage")
    for tid in [t["task_id"] for t in tasks]:
        for api in TASK_DOMAIN_APIS.get(tid, ()):
            name = api["name"]
            if name not in DOMAIN_API_SSOT:
                ssot_failures.append(f"{tid}:missing_ssot:{name}")
                continue
            line = render_api_prompt_line(name)
            section = domain_section(tid)
            if line not in section:
                ssot_failures.append(f"{tid}:prompt_ssot_mismatch:{name}")
    try:
        factors = PolynomialOps.factor_quadratic_exact(1, 4, -12)
        if not (
            isinstance(factors, list)
            and len(factors) == 2
            and all(set(f) == {"x_coefficient", "constant"} for f in factors)
        ):
            ssot_failures.append("runtime_factor_quadratic_exact_shape")
        else:
            # Contract test: 3-value unpack must fail against real return shape.
            try:
                _a, _b, _c = factors  # type: ignore[misc]
                ssot_failures.append("runtime_factor_quadratic_exact_unexpected_3tuple")
            except ValueError:
                pass
    except Exception as exc:  # noqa: BLE001
        ssot_failures.append(f"runtime_factor_quadratic_exact:{exc}")
    checks["domain_api_ssot_aligned"] = not ssot_failures
    if ssot_failures:
        blockers.append(f"domain_api_ssot:{ssot_failures[:8]}")

    checks["oracle_golden_all_pass"] = not oracle_failures
    checks["latex_g6_all_pass"] = not latex_failures
    checks["contracts_all_present"] = not contract_failures
    checks["domain_apis_all_present"] = not domain_failures
    checks["prompt_cells_48"] = len(prompt_rows) == 48

    # Representative prompt hashes (one task per condition builder identity is per-cell)
    # Report path as builder lineage (runtime-assembled; no static prompt files).
    sample_task = tasks[0]
    frozen = frozen_for_prompt(sample_task)
    prompt_paths = {
        "lineage": LINEAGE_ID,
        "builder_module": "agent_tools/finals_rebuild/ce115_clean_incremental_ablation.py",
        "builder_functions": {
            "ab1": "build_base_prompt -> math_boundary_pilot.build_ab1_prompt",
            "ab2g": "build_ab2g_clean_prompt",
            "ab2d": "build_ab2d_clean_prompt",
        },
        "runner_reference": "scripts/preflight_math16_latex_v1.py (no-model); live runner deferred",
        "per_condition_example_task": sample_task["task_id"],
        "per_condition_sha256": {
            condition: prompt_sha256(build_condition_prompt(condition, sample_task, frozen))
            for condition in CONDITIONS
        },
        "all_cells": prompt_rows,
    }

    component_hashes = _component_hashes()
    manifest_path = ROOT / "docs/experiments/manifests/math16_latex_v1_pool_manifest.json"
    hashes = {
        "pool_identity_hash": manifest["pool_identity_hash"],
        "final_manifest_hash": manifest["manifest_content_sha256"],
        "task_freeze_hash": manifest["task_freeze_hash"],
        "manifest_file_sha256": _file_sha(manifest_path) if manifest_path.exists() else None,
        "prompt_lineage": LINEAGE_ID,
        **{f"component_{k}": v for k, v in component_hashes.items()},
    }

    for key, value in checks.items():
        if key in {"pool_id"}:
            continue
        if value is False:
            blockers.append(key)

    passed = not blockers and all(
        checks[k]
        for k in checks
        if k
        not in {
            # already encoded
        }
    )
    # Explicit required gates
    required = [
        "domain_ops_4_4_4_4",
        "task_count_16",
        "no_year_114",
        "q08_correct_params",
        "q08_strict_factor_order",
        "q08_rejects_legacy_12",
        "q12_substantial_abstraction",
        "q11_reuse_rerun",
        "q10_compound_signed_coeffs",
        "compound_radical_support",
        "correct_answer_oracle_payload_layering",
        "oracle_golden_all_pass",
        "latex_g6_all_pass",
        "contracts_all_present",
        "domain_apis_all_present",
        "prompt_cells_48",
    ]
    passed = all(checks[k] for k in required) and not blockers

    return {
        "pool_id": POOL_ID,
        "passed": passed,
        "blocker": None if passed else (" | ".join(blockers) if blockers else "PREFLIGHT_FAILED"),
        "checks": checks,
        "failures": {
            "oracle": oracle_failures,
            "latex": latex_failures,
            "contracts": contract_failures,
            "domain": domain_failures,
        },
        "hashes": hashes,
        "prompts": prompt_paths,
        "domain_ops_distribution": dist,
        "task_ids": manifest["task_ids"],
        "gemini_live_run": "blocked_until_explicit_go",
    }
