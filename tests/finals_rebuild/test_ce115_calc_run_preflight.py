"""Milestone 3C — zero-model local confirmatory 72-cell preflight tests."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from agent_tools.finals_rebuild.ce115_calc_prompt_freeze import prompt_sha256
from agent_tools.finals_rebuild.ce115_calc_run_plan import (
    PreflightError,
    REQUIRED_PLANNED_RECORD_KEYS,
    assert_cell_distribution,
    assert_cross_model_prompt_identity,
    assert_output_path_safety,
    assert_request_matches_manifest,
    build_planned_record_skeleton,
    build_request_options_from_manifest,
    expand_local_confirmatory_cells,
    load_manifest,
    manifest_sha256,
    module_source_guard,
    plan_summary_for_cli,
    run_preflight,
)

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "docs" / "experiments" / "manifests" / "ce115_calc_main_experiment_manifest.json"
CLI = ROOT / "scripts" / "preflight_ce115_calc_local_confirmatory.py"


@pytest.fixture(scope="module")
def summary():
    return run_preflight(MANIFEST, repo_root=ROOT, write_results=False)


@pytest.fixture(scope="module")
def cells(summary):
    return summary["cells"]


def test_exactly_72_cells(cells):
    assert len(cells) == 72


def test_cell_ids_unique(cells):
    ids = [c["cell_id"] for c in cells]
    assert len(set(ids)) == 72
    for cid in ids:
        assert "uuid" not in cid.lower()
        assert "timestamp" not in cid.lower()


def test_output_paths_unique(cells):
    paths = [c["output_path"] for c in cells]
    assert len(set(paths)) == 72
    for path in paths:
        assert path.startswith("docs/experiments/results/ce115_calc_local_confirmatory/")
        assert path.endswith(".jsonl")
        assert "qwen3_5_4b" in path or "qwen3_5_9b" in path
        assert "qwen3_4b__" not in path and "qwen3_8b__" not in path


def test_distribution_18_24_24_36(cells):
    assert_cell_distribution(cells)


def test_no_gemini_legacy_or_historical_qwen3(cells):
    for cell in cells:
        assert "gemini" not in cell["model_tag"].lower()
        assert cell["model_tag"] in {"qwen3.5:4b", "qwen3.5:9b"}
        assert not cell["task_id"].startswith("ce115_cr01_")
        assert cell["task_id"].startswith("ce115_calc_")
        assert cell["task_id"].endswith("_l1")
        assert cell["cell_id"].startswith(("qwen3_5_4b__", "qwen3_5_9b__"))


def test_prompt_hashes_match_manifest_for_hash_seed(cells):
    manifest = load_manifest(MANIFEST)
    hash_seed = manifest["prompt_hash_seed"]
    table = manifest["per_task_prompt_hashes"]
    checked = 0
    for cell in cells:
        if cell["seed"] != hash_seed:
            continue
        assert cell["prompt_hash"] == table[cell["task_id"]][cell["prompt_condition"]]
        assert cell["prompt_hash"] == prompt_sha256(cell["prompt_text"])
        checked += 1
    assert checked == 24  # 4 tasks × 3 conditions × 2 models


def test_4b_9b_prompts_byte_identical(cells):
    assert_cross_model_prompt_identity(cells)


def test_not_explicitly_set_not_filled_in_payload(cells):
    for cell in cells:
        assert cell["top_p"] == "not_explicitly_set"
        assert cell["top_k"] == "not_explicitly_set"
        assert cell["presence_penalty"] == "not_explicitly_set"
        assert cell["num_predict"] == "not_explicitly_set"
        assert isinstance(cell["temperature"], float)
        assert cell["temperature"] == 0.0
        opts = cell["request_options"]
        assert opts["top_p"] == "not_explicitly_set"
        assert opts["top_k"] == "not_explicitly_set"
        assert opts["presence_penalty"] == "not_explicitly_set"
        assert opts["num_predict"] == "not_explicitly_set"
        assert opts["think"] is False
        assert cell["thinking_requested"] is False
        assert cell["think"] is False


def test_both_models_explicit_think_false(cells):
    four = [c for c in cells if c["model_tag"] == "qwen3.5:4b"]
    nine = [c for c in cells if c["model_tag"] == "qwen3.5:9b"]
    assert len(four) == 36 and len(nine) == 36
    for cell in four + nine:
        assert cell["thinking_requested"] is False
        assert cell["request_options"]["think"] is False
        assert cell["request_options"]["thinking_requested"] is False


def test_request_retry_healer_policy(cells):
    for cell in cells:
        assert cell["request_count"] == 1
        assert cell["retry_count"] == 0
        assert cell["healer_enabled"] is False
        assert cell["ledger_stage"] == "observed"
        assert cell["included_in_formal_analysis"] is True


def test_duplicate_cell_fail(cells):
    foul = list(cells) + [dict(cells[0])]
    with pytest.raises(PreflightError, match="duplicate"):
        assert_cell_distribution(foul)


def test_duplicate_output_path_fail(cells):
    a = dict(cells[0])
    b = dict(cells[1])
    b["output_path"] = a["output_path"]
    b["output_path_abs"] = a["output_path_abs"]
    with pytest.raises(PreflightError, match="duplicate output path"):
        assert_output_path_safety([a, b], repo_root=ROOT)


def test_hash_mismatch_fail_fast():
    manifest = load_manifest(MANIFEST)
    # Corrupt one frozen hash entry and re-expand
    bad = json.loads(json.dumps(manifest))
    bad["per_task_prompt_hashes"]["ce115_calc_radical_simplification_l1"]["ab1"] = "0" * 64
    with pytest.raises(PreflightError, match="prompt hash mismatch"):
        expand_local_confirmatory_cells(bad, repo_root=ROOT)


def test_existing_formal_artifact_overwrite_blocked(tmp_path, cells):
    cell = dict(cells[0])
    # Build a fake repo root with an existing non-empty formal artifact
    rel = cell["output_path"]
    target = tmp_path / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text('{"already": true}\n', encoding="utf-8")
    cell["output_path_abs"] = str(target.resolve())
    blockers = assert_output_path_safety([cell], repo_root=tmp_path)
    assert rel in blockers


def test_planned_record_schema_complete(summary, cells):
    record = build_planned_record_skeleton(
        cells[0],
        commit_hash=summary["git_commit"],
        manifest_hash=summary["manifest_hash"],
    )
    for key in REQUIRED_PLANNED_RECORD_KEYS:
        assert key in record
    assert record["request_count"] == 1
    assert record["retry_count"] == 0
    assert record["healer_enabled"] is False
    assert record["ledger_stage"] == "observed"
    assert record["first_attempt_is_ITT"] is True
    assert record["raw_first_attempt_output"] is None  # no fabricated model output


def test_cli_dry_run_model_calls_zero():
    module_source_guard()
    proc = subprocess.run(
        [
            sys.executable,
            str(CLI),
            "--manifest",
            str(MANIFEST),
            "--dry-run",
        ],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode in (0, 1), proc.stderr
    assert "model_calls = 0" in proc.stdout
    assert "planned_cells = 72" in proc.stdout
    assert "duplicate_cells = 0" in proc.stdout
    assert "duplicate_paths = 0" in proc.stdout
    assert "prompt_hash_mismatches = 0" in proc.stdout
    assert "request_setting_mismatches = 0" in proc.stdout
    if "existing_output_conflicts = 0" in proc.stdout or "existing_output_conflicts=0" in proc.stdout:
        assert "verdict = READY" in proc.stdout or "verdict=READY" in proc.stdout
        assert proc.returncode == 0
    else:
        assert "NOT READY" in proc.stdout
    # Ensure CLI source stays transport-free
    source = CLI.read_text(encoding="utf-8")
    assert "call_ollama_chat" not in source
    assert "GoogleAIClient" not in source
    assert "import requests" not in source
    assert "import httpx" not in source


def test_json_serialize_plan(summary):
    slim = plan_summary_for_cli(summary)
    dumped = json.dumps(slim, ensure_ascii=False, sort_keys=True)
    restored = json.loads(dumped)
    assert restored["planned_cells"] == 72
    assert restored["model_calls"] == 0
    assert restored["verdict"] in {"READY", "NOT READY"}
    if restored["existing_output_conflicts"] == 0:
        assert restored["verdict"] == "READY"
    else:
        assert restored["verdict"] == "NOT READY"


def test_manifest_hash_deterministic():
    a = manifest_sha256(MANIFEST)
    b = manifest_sha256(MANIFEST)
    assert a == b
    assert len(a) == 64


def test_filling_not_explicitly_set_is_mismatch():
    sampling = {
        "temperature": 0.0,
        "think": False,
        "top_p": "not_explicitly_set",
        "top_k": "not_explicitly_set",
        "presence_penalty": "not_explicitly_set",
        "num_predict": "not_explicitly_set",
        "observed_model_defaults": {"temperature": 1, "top_k": 20, "top_p": 0.95, "presence_penalty": 1.5},
    }
    thinking = {"requested": False, "thinking_requested": False}
    good = build_request_options_from_manifest(sampling, seed=1, thinking=thinking)
    assert good["think"] is False
    assert assert_request_matches_manifest(good, sampling, thinking) == []
    bad = dict(good)
    bad["top_p"] = 0.9
    assert "top_p_filled_against_not_explicitly_set" in assert_request_matches_manifest(bad, sampling, thinking)
    leaked = dict(good)
    leaked["top_p"] = 0.95
    assert "model_default_leaked_into_request:top_p" in assert_request_matches_manifest(leaked, sampling, thinking)


def test_preflight_forbids_write_results_flag():
    with pytest.raises(PreflightError, match="must not write"):
        run_preflight(MANIFEST, repo_root=ROOT, write_results=True)


def test_ab_condition_shapes(cells):
    from agent_tools.finals_rebuild.ab2d_local_prompt import MATH_CORE_SCAFFOLD
    from agent_tools.finals_rebuild.ce115_calc_golden_generators import formal_l1_tasks

    tasks = formal_l1_tasks()
    for cell in cells:
        text = cell["prompt_text"]
        skill = tasks[cell["task_id"]]["skill_id"]
        if cell["prompt_condition"] == "ab1":
            assert MATH_CORE_SCAFFOLD not in text
            assert "## Task-local domain primitive:" not in text
        elif cell["prompt_condition"] == "ab2g":
            assert text.startswith(MATH_CORE_SCAFFOLD)
            assert "## Task-local domain primitive:" not in text
        else:
            assert text.startswith(MATH_CORE_SCAFFOLD)
            assert f"## Task-local domain primitive: {skill}" in text
