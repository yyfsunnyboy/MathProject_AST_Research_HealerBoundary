"""Ab2d-v2 freeze hashes must use git blob (LF), not working-tree CRLF bytes."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

from agent_tools.finals_rebuild.git_blob_hash import (
    git_blob_oid,
    normalize_to_lf,
    sha256_bytes,
    sha256_git_blob_lf,
)

ROOT = Path(__file__).resolve().parents[2]
FREEZE = ROOT / "docs/experiments/results/domain_api_contract_hardening_v2/ab2d_v2_freeze_manifest.json"

COMPONENT_PATHS = {
    "toolbox": ROOT / "core/prompts/domain_function_library.py",
    "ssot": ROOT / "agent_tools/finals_rebuild/domain_api_ssot.py",
    "skills": ROOT / "agent_skills/domain_api_contract_v2/SKILL.md",
    "task_assembly": ROOT / "agent_tools/finals_rebuild/domain_answer_assembly.py",
    "answer_contract": ROOT / "agent_tools/finals_rebuild/math_answer_contracts.py",
    "oracle_evaluator": ROOT / "agent_tools/finals_rebuild/math16_oracles.py",
    "api_inventory": ROOT
    / "docs/experiments/results/domain_api_contract_hardening_v2/api_inventory.json",
    "typed_contracts": ROOT
    / "docs/experiments/results/domain_api_contract_hardening_v2/typed_contracts.json",
    "task_assembly_artifact": ROOT
    / "docs/experiments/results/domain_api_contract_hardening_v2/task_output_assembly.json",
    "math16_pool_manifest": ROOT
    / "docs/experiments/manifests/math16_latex_v1_pool_manifest.json",
}

TOP_LEVEL_PATHS = {
    "prompt_diff_sha256": ROOT
    / "docs/experiments/results/domain_api_contract_hardening_v2/prompt_hash_diff_48.json",
    "baseline_failure_attribution_sha256": ROOT
    / "docs/experiments/results/domain_api_contract_hardening_v2/baseline_failure_attribution.json",
    "freeze_gate_report_sha256": ROOT
    / "docs/experiments/results/domain_api_contract_hardening_v2/freeze_gate_report.json",
    "rerun_manifest_sha256": ROOT
    / "docs/experiments/results/domain_api_contract_hardening_v2/ab2d_v2_rerun_manifest.json",
}


def test_freeze_manifest_declares_git_blob_lf_basis() -> None:
    freeze = json.loads(FREEZE.read_text(encoding="utf-8"))
    assert freeze["hash_basis"] == "git_blob_lf"


def test_freeze_component_hashes_match_git_blob_sha256() -> None:
    freeze = json.loads(FREEZE.read_text(encoding="utf-8"))
    recorded = freeze["component_sha256"]
    assert set(COMPONENT_PATHS) == set(recorded)
    for name, path in COMPONENT_PATHS.items():
        assert recorded[name] == sha256_git_blob_lf(path, repo_root=ROOT), name


def test_freeze_top_level_artifact_hashes_match_git_blob_sha256() -> None:
    freeze = json.loads(FREEZE.read_text(encoding="utf-8"))
    for key, path in TOP_LEVEL_PATHS.items():
        assert freeze[key] == sha256_git_blob_lf(path, repo_root=ROOT), key


def test_git_hash_object_matches_ls_files_for_frozen_sources() -> None:
    for path in (
        COMPONENT_PATHS["ssot"],
        COMPONENT_PATHS["oracle_evaluator"],
        COMPONENT_PATHS["math16_pool_manifest"],
    ):
        rel = path.relative_to(ROOT).as_posix()
        oid = git_blob_oid(path, repo_root=ROOT)
        ls = subprocess.check_output(
            ["git", "-C", str(ROOT), "ls-files", "-s", rel],
            text=True,
        ).strip().split()[1]
        assert oid == ls


def test_helper_ignores_working_tree_crlf() -> None:
    path = COMPONENT_PATHS["oracle_evaluator"]
    disk = path.read_bytes()
    lf = normalize_to_lf(disk)
    assert sha256_git_blob_lf(path, repo_root=ROOT) == sha256_bytes(lf)
    if b"\r\n" in disk:
        assert sha256_bytes(disk) != sha256_bytes(lf)
