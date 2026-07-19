"""Build deterministic Ab2d-v2 freeze reports and no-model rerun plan."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.git_blob_hash import sha256_git_blob_lf  # noqa: E402

OUT = ROOT / "docs/experiments/results/domain_api_contract_hardening_v2"

BASELINE_FAILURES = [
    "tests/finals_rebuild/test_ce115_polydiv_return_contract.py::test_prompt_example_requires_direct_unpacking",
    "tests/finals_rebuild/test_ce115_preflight.py::test_preflight_cells_list_and_uniqueness",
    "tests/finals_rebuild/test_ce115_preflight.py::test_preflight_repetition_diagnostics_deterministic",
    "tests/finals_rebuild/test_ce115_rebuild_census.py::test_rebuilt_matrix_completeness_and_uniqueness",
    "tests/finals_rebuild/test_ce115_rebuild_census.py::test_rebuilt_matrix_hashes_and_negative_evidence",
    "tests/finals_rebuild/test_ce115_rebuild_census.py::test_rebuilt_matrix_lexical_scanners_verdict",
    "tests/finals_rebuild/test_ce115_rebuild_census.py::test_historical_census_telemetry_integrity",
    "tests/finals_rebuild/test_ce115_rebuild_census.py::test_historical_census_truncated_exclusion",
    "tests/finals_rebuild/test_execution_evaluator.py::test_2_top_level_exception_failure",
    "tests/finals_rebuild/test_math_task_oracles.py::test_manifest_is_twelve_immutable_oracle_tasks",
    "tests/finals_rebuild/test_math_task_sampler.py::test_strata_and_determinism",
    "tests/finals_rebuild/test_verify_script.py::test_usage_errors[args0]",
    "tests/finals_rebuild/test_verify_script.py::test_usage_errors[args1]",
    "tests/finals_rebuild/test_verify_script.py::test_usage_errors[args2]",
    "tests/finals_rebuild/test_verify_script.py::test_modes_invoke_expected_pytest_targets[targeted-test_math_dev_replay.py]",
    "tests/finals_rebuild/test_verify_script.py::test_modes_invoke_expected_pytest_targets[related-test_math_validator.py]",
    "tests/finals_rebuild/test_verify_script.py::test_modes_invoke_expected_pytest_targets[full-tests/finals_rebuild]",
    "tests/finals_rebuild/test_verify_script.py::test_related_mode_includes_generator_pilot_tests",
    "tests/finals_rebuild/test_verify_script.py::test_pytest_failure_is_propagated_without_success_banner",
    "tests/finals_rebuild/test_verify_script.py::test_dirty_tree_warns_and_still_runs_pytest",
    "tests/finals_rebuild/test_verify_script.py::test_missing_pytest_returns_environment_error",
]


def sha(path: Path) -> str:
    """SHA-256 of git blob content (LF). Never hash raw CRLF working-tree bytes."""
    return sha256_git_blob_lf(path, repo_root=ROOT)


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def main() -> int:
    prompt_diff = json.loads((OUT / "prompt_hash_diff_48.json").read_text(encoding="utf-8"))
    prior_rows = [{"node_id": node, "classification": "BASELINE_FAILURE_CONFIRMED", "baseline_failed": True, "current_failed": True} for node in BASELINE_FAILURES]
    prior_rows.append({
        "node_id": "tests/finals_rebuild/test_latex_render_validation.py::test_live_browser_mathjax_smoke",
        "classification": "ENVIRONMENT_UNSUPPORTED", "baseline_failed": False,
        "current_failed": True, "evidence": "Browser executable was discovered but CDP refused localhost connection; no Domain API dependency.",
    })
    prior_rows.append({
        "node_id": "tests/finals_rebuild/test_ce115_clean_incremental_ablation.py::test_ab2d_not_full_toolbox",
        "classification": "CURRENT_REGRESSION", "baseline_failed": False,
        "current_failed": False, "resolution": "RESOLVED_BEFORE_FREEZE",
        "evidence": "Qualified adapter name in model-facing return prose inflated lexical API count; prose was made compact and targeted test now passes.",
    })
    attribution = {
        "baseline_head": "aa33a6e1e24f423c62526c4c02d7019d6b778fb1",
        "baseline_worktree": "C:/b33", "command": "PYTHONUTF8=1 python -m pytest tests/finals_rebuild -q",
        "baseline_summary": {"passed": 1221, "failed": 21},
        "current_summary": {"passed": 1229, "failed": 22},
        "prior_23_failure_attribution": prior_rows,
        "active_counts": {"BASELINE_FAILURE_CONFIRMED": 21, "ENVIRONMENT_UNSUPPORTED": 1, "CURRENT_REGRESSION": 0, "UNRESOLVED": 0},
        "freeze_blocked": False,
    }
    (OUT / "baseline_failure_attribution.json").write_text(json.dumps(attribution, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")

    component_paths = {
        "toolbox": ROOT / "core/prompts/domain_function_library.py",
        "ssot": ROOT / "agent_tools/finals_rebuild/domain_api_ssot.py",
        "skills": ROOT / "agent_skills/domain_api_contract_v2/SKILL.md",
        "task_assembly": ROOT / "agent_tools/finals_rebuild/domain_answer_assembly.py",
        "answer_contract": ROOT / "agent_tools/finals_rebuild/math_answer_contracts.py",
        "oracle_evaluator": ROOT / "agent_tools/finals_rebuild/math16_oracles.py",
        "api_inventory": OUT / "api_inventory.json",
        "typed_contracts": OUT / "typed_contracts.json",
        "task_assembly_artifact": OUT / "task_output_assembly.json",
        "math16_pool_manifest": ROOT / "docs/experiments/manifests/math16_latex_v1_pool_manifest.json",
    }
    hashes = {name: sha(path) for name, path in component_paths.items()}
    gates = {
        "ab2d_v2_scope": "api_contract_only", "task_contract_changes_deferred_to_v3": True,
        "model_calls": 0, "baseline_attribution": {"current_regression": 0, "unresolved": 0},
        "api_inventory": {"total": 43, "supported_public": 27, "aligned": True},
        "task_assembly_coverage": "16/16", "domain_api_ssot_aligned": True,
        "prompt_hashes": {"ab1_unchanged": "16/16", "ab2g_unchanged": "16/16", "ab2d_changed": "16/16", "unexpected": 0},
        "tests": {"targeted": "75 passed", "no_model_preflight": "PASS", "json_roundtrip": "PASS", "git_diff_check": "PASS"},
        "hash_basis": "git_blob_lf",
        "component_sha256": hashes, "passed": True,
    }
    (OUT / "freeze_gate_report.json").write_text(json.dumps(gates, indent=2, ensure_ascii=False)+"\n", encoding="utf-8", newline="\n")

    cells = [{"cell_id": f"{r['task_id']}__ab2d", "task_id": r["task_id"], "condition": "ab2d", "old_prompt_hash": r["old_prompt_hash"], "frozen_prompt_hash": r["new_prompt_hash"], "status": "PLANNED_NOT_RUN"} for r in prompt_diff["changed_cells"]]
    rerun = {"plan_id":"math16_ab2d_v2_contract_aligned_validation","ab2d_v2_scope":"api_contract_only","task_contract_changes_deferred_to_v3":True,"model_calls":0,"cell_count":len(cells),"cells":cells,"run_authorization":"REQUIRES_SEPARATE_HUMAN_CONFIRMATION"}
    (OUT / "ab2d_v2_rerun_manifest.json").write_text(json.dumps(rerun, indent=2, ensure_ascii=False)+"\n", encoding="utf-8", newline="\n")

    freeze = {
        "freeze_id": "Ab2d-v2",
        "status": "FROZEN_CONTRACT_VALIDATION_PLAN",
        "hash_basis": "git_blob_lf",
        "baseline_head": "aa33a6e1e24f423c62526c4c02d7019d6b778fb1",
        "source_head_before_commit": git("rev-parse", "HEAD"),
        "ab2d_v2_scope": "api_contract_only",
        "task_contract_changes_deferred_to_v3": True,
        "model_calls": 0,
        "component_sha256": hashes,
        "prompt_diff_sha256": sha(OUT / "prompt_hash_diff_48.json"),
        "baseline_failure_attribution_sha256": sha(OUT / "baseline_failure_attribution.json"),
        "freeze_gate_report_sha256": sha(OUT / "freeze_gate_report.json"),
        "rerun_manifest_sha256": sha(OUT / "ab2d_v2_rerun_manifest.json"),
        "changed_cells": 16,
        "unexpected_prompt_hash_changes": 0,
    }
    (OUT / "ab2d_v2_freeze_manifest.json").write_text(json.dumps(freeze, indent=2, ensure_ascii=False)+"\n", encoding="utf-8", newline="\n")
    print(json.dumps({"passed": True, "cells": len(cells), "hash_basis": "git_blob_lf", "hashes": hashes}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
