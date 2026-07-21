# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import os
import pytest
import shutil
from pathlib import Path
from unittest.mock import MagicMock, patch

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "docs/experiments/manifests/math16_pilot02_integer_runtime_manifest.json"
CELL_PLAN_PATH = ROOT / "docs/experiments/manifests/math16_pilot02_integer_cell_plan.json"

from scripts.run_math16_pilot02_integer_generation import (
    do_preflight,
    run_cell_with_retries,
    execute_generations,
    compute_runtime_fingerprint
)

def test_do_preflight_succeeds():
    res = do_preflight()
    assert "manifest" in res
    assert "cell_plan" in res
    assert len(res["cell_plan"]) == 80

def test_preflight_fails_on_source_commit_mismatch():
    manifest_content = MANIFEST_PATH.read_text(encoding="utf-8")
    manifest_data = json.loads(manifest_content)
    manifest_data["source_commit"] = "outdated_or_wrong_commit"

    with patch("json.loads", return_value=manifest_data):
        with pytest.raises(ValueError, match="Source commit mismatch"):
            do_preflight()

def test_preflight_fails_on_cell_count_mismatch():
    manifest_content = MANIFEST_PATH.read_text(encoding="utf-8")
    manifest_data = json.loads(manifest_content)
    manifest_data["expected_cell_count"] = 12345

    with patch("json.loads", return_value=manifest_data):
        with pytest.raises(ValueError, match="Cell plan size mismatch|expected cell count mismatch"):
            do_preflight()

def test_preflight_fails_on_duplicate_cell_id():
    plan_content = CELL_PLAN_PATH.read_text(encoding="utf-8")
    plan_data = json.loads(plan_content)
    plan_data[1]["cell_id"] = plan_data[0]["cell_id"]

    orig_read_text = Path.read_text
    def mock_read_text(self, *args, **kwargs):
        if "math16_pilot02_integer_cell_plan" in str(self):
            return json.dumps(plan_data)
        return orig_read_text(self, *args, **kwargs)

    with patch.object(Path, "read_text", mock_read_text):
        with pytest.raises(ValueError, match="Duplicate cell_id detected"):
            do_preflight()

def test_retry_policy_exhausts_and_waits_5_and_20():
    mock_execute = MagicMock(side_effect=RuntimeError("Transient API Error"))

    with patch("time.sleep") as mock_sleep:
        with pytest.raises(RuntimeError, match="API calls exhausted for cell"):
            run_cell_with_retries("dummy prompt", "cell_123", mock_execute)

        assert mock_execute.call_count == 3
        assert mock_sleep.call_count == 2
        mock_sleep.assert_any_call(5)
        mock_sleep.assert_any_call(20)

def test_retry_policy_succeeds_on_second_attempt():
    mock_execute = MagicMock(side_effect=[RuntimeError("Transient API Error"), {"raw_text": "success", "metadata": {}}])

    with patch("time.sleep") as mock_sleep:
        res = run_cell_with_retries("dummy prompt", "cell_123", mock_execute)
        assert res["raw_text"] == "success"
        assert mock_execute.call_count == 2
        mock_sleep.assert_called_once_with(5)

def test_resume_policy_skips_compatible_cells(tmp_path):
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    manifest["output_root"] = str(tmp_path.relative_to(ROOT)) if tmp_path.is_relative_to(ROOT) else str(tmp_path)
    fingerprint = compute_runtime_fingerprint(manifest)

    cell_plan = [{
        "cell_id": "gemini_3_5_flash__ce111_q03_prime_factor_selection__ab2d_spec__seed_2026071301",
        "task_id": "ce111_q03_prime_factor_selection",
        "condition": "ab2d_spec",
        "seed": 2026071301,
        "model_tag": "gemini-3.5-flash",
        "runtime_parameters": {"temperature": 0.0, "max_output_tokens": 24576, "timeout_seconds": 600},
        "prompt_source": "dummy_path",
        "prompt_sha256": "5417185bc8f5d084bd04d6bf4d346762f6fa4738c6a52d30ea34706f4121e6f0",
        "output_relative_path": "cells/cell_001"
    }]

    cell_dir = tmp_path / "cells/cell_001"
    cell_dir.mkdir(parents=True)
    (cell_dir / "raw_response.txt").write_text("raw response", encoding="utf-8")
    (cell_dir / "artifact.json").write_text(json.dumps({
        "persisted_complete": True,
        "experiment_id": manifest["experiment_id"],
        "cell_id": "gemini_3_5_flash__ce111_q03_prime_factor_selection__ab2d_spec__seed_2026071301",
        "task_id": "ce111_q03_prime_factor_selection",
        "condition": "ab2d_spec",
        "seed": 2026071301,
        "prompt_sha256": "5417185bc8f5d084bd04d6bf4d346762f6fa4738c6a52d30ea34706f4121e6f0",
        "model_tag": "gemini-3.5-flash",
        "runtime_config_fingerprint": fingerprint
    }), encoding="utf-8")

    with patch.dict(os.environ, {"GEMINI_API_KEY": "dummy_key"}):
        with patch("scripts.ce115_v4_gemini_transport.call_gemini_once") as mock_call:
            execute_generations(manifest, cell_plan)
            mock_call.assert_not_called()

def test_resume_policy_fails_on_prompt_sha_mismatch(tmp_path):
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    manifest["output_root"] = str(tmp_path.relative_to(ROOT)) if tmp_path.is_relative_to(ROOT) else str(tmp_path)
    fingerprint = compute_runtime_fingerprint(manifest)

    cell_plan = [{
        "cell_id": "gemini_3_5_flash__ce111_q03_prime_factor_selection__ab2d_spec__seed_2026071301",
        "task_id": "ce111_q03_prime_factor_selection",
        "condition": "ab2d_spec",
        "seed": 2026071301,
        "model_tag": "gemini-3.5-flash",
        "runtime_parameters": {"temperature": 0.0, "max_output_tokens": 24576, "timeout_seconds": 600},
        "prompt_source": "dummy_path",
        "prompt_sha256": "5417185bc8f5d084bd04d6bf4d346762f6fa4738c6a52d30ea34706f4121e6f0",
        "output_relative_path": "cells/cell_001"
    }]

    cell_dir = tmp_path / "cells/cell_001"
    cell_dir.mkdir(parents=True)
    (cell_dir / "raw_response.txt").write_text("raw response", encoding="utf-8")
    (cell_dir / "artifact.json").write_text(json.dumps({
        "persisted_complete": True,
        "experiment_id": manifest["experiment_id"],
        "cell_id": "gemini_3_5_flash__ce111_q03_prime_factor_selection__ab2d_spec__seed_2026071301",
        "task_id": "ce111_q03_prime_factor_selection",
        "condition": "ab2d_spec",
        "seed": 2026071301,
        "prompt_sha256": "mismatched_prompt_sha_value",
        "model_tag": "gemini-3.5-flash",
        "runtime_config_fingerprint": fingerprint
    }), encoding="utf-8")

    with patch.dict(os.environ, {"GEMINI_API_KEY": "dummy_key"}):
        with pytest.raises(RuntimeError, match="INCOMPATIBLE_EXISTING_CELL"):
            execute_generations(manifest, cell_plan)

def test_resume_policy_fails_on_fingerprint_mismatch(tmp_path):
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    manifest["output_root"] = str(tmp_path.relative_to(ROOT)) if tmp_path.is_relative_to(ROOT) else str(tmp_path)

    cell_plan = [{
        "cell_id": "gemini_3_5_flash__ce111_q03_prime_factor_selection__ab2d_spec__seed_2026071301",
        "task_id": "ce111_q03_prime_factor_selection",
        "condition": "ab2d_spec",
        "seed": 2026071301,
        "model_tag": "gemini-3.5-flash",
        "runtime_parameters": {"temperature": 0.0, "max_output_tokens": 24576, "timeout_seconds": 600},
        "prompt_source": "dummy_path",
        "prompt_sha256": "5417185bc8f5d084bd04d6bf4d346762f6fa4738c6a52d30ea34706f4121e6f0",
        "output_relative_path": "cells/cell_001"
    }]

    cell_dir = tmp_path / "cells/cell_001"
    cell_dir.mkdir(parents=True)
    (cell_dir / "raw_response.txt").write_text("raw response", encoding="utf-8")
    (cell_dir / "artifact.json").write_text(json.dumps({
        "persisted_complete": True,
        "experiment_id": manifest["experiment_id"],
        "cell_id": "gemini_3_5_flash__ce111_q03_prime_factor_selection__ab2d_spec__seed_2026071301",
        "task_id": "ce111_q03_prime_factor_selection",
        "condition": "ab2d_spec",
        "seed": 2026071301,
        "prompt_sha256": "5417185bc8f5d084bd04d6bf4d346762f6fa4738c6a52d30ea34706f4121e6f0",
        "model_tag": "gemini-3.5-flash",
        "runtime_config_fingerprint": "incompatible_fingerprint_value_here"
    }), encoding="utf-8")

    with patch.dict(os.environ, {"GEMINI_API_KEY": "dummy_key"}):
        with pytest.raises(RuntimeError, match="INCOMPATIBLE_EXISTING_CELL"):
            execute_generations(manifest, cell_plan)

def test_resume_policy_fails_on_identity_mismatch(tmp_path):
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    manifest["output_root"] = str(tmp_path.relative_to(ROOT)) if tmp_path.is_relative_to(ROOT) else str(tmp_path)
    fingerprint = compute_runtime_fingerprint(manifest)

    cell_plan = [{
        "cell_id": "gemini_3_5_flash__ce111_q03_prime_factor_selection__ab2d_spec__seed_2026071301",
        "task_id": "ce111_q03_prime_factor_selection",
        "condition": "ab2d_spec",
        "seed": 2026071301,
        "model_tag": "gemini-3.5-flash",
        "runtime_parameters": {"temperature": 0.0, "max_output_tokens": 24576, "timeout_seconds": 600},
        "prompt_source": "dummy_path",
        "prompt_sha256": "5417185bc8f5d084bd04d6bf4d346762f6fa4738c6a52d30ea34706f4121e6f0",
        "output_relative_path": "cells/cell_001"
    }]

    cell_dir = tmp_path / "cells/cell_001"
    cell_dir.mkdir(parents=True)
    (cell_dir / "raw_response.txt").write_text("raw response", encoding="utf-8")
    # identity field seed mismatched
    (cell_dir / "artifact.json").write_text(json.dumps({
        "persisted_complete": True,
        "experiment_id": manifest["experiment_id"],
        "cell_id": "gemini_3_5_flash__ce111_q03_prime_factor_selection__ab2d_spec__seed_2026071301",
        "task_id": "ce111_q03_prime_factor_selection",
        "condition": "ab2d_spec",
        "seed": 99999999,
        "prompt_sha256": "5417185bc8f5d084bd04d6bf4d346762f6fa4738c6a52d30ea34706f4121e6f0",
        "model_tag": "gemini-3.5-flash",
        "runtime_config_fingerprint": fingerprint
    }), encoding="utf-8")

    with patch.dict(os.environ, {"GEMINI_API_KEY": "dummy_key"}):
        with pytest.raises(RuntimeError, match="INCOMPATIBLE_EXISTING_CELL"):
            execute_generations(manifest, cell_plan)

def test_resume_policy_fails_on_experiment_id_mismatch(tmp_path):
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    manifest["output_root"] = str(tmp_path.relative_to(ROOT)) if tmp_path.is_relative_to(ROOT) else str(tmp_path)
    fingerprint = compute_runtime_fingerprint(manifest)

    cell_plan = [{
        "cell_id": "gemini_3_5_flash__ce111_q03_prime_factor_selection__ab2d_spec__seed_2026071301",
        "task_id": "ce111_q03_prime_factor_selection",
        "condition": "ab2d_spec",
        "seed": 2026071301,
        "model_tag": "gemini-3.5-flash",
        "runtime_parameters": {"temperature": 0.0, "max_output_tokens": 24576, "timeout_seconds": 600},
        "prompt_source": "dummy_path",
        "prompt_sha256": "5417185bc8f5d084bd04d6bf4d346762f6fa4738c6a52d30ea34706f4121e6f0",
        "output_relative_path": "cells/cell_001"
    }]

    cell_dir = tmp_path / "cells/cell_001"
    cell_dir.mkdir(parents=True)
    (cell_dir / "raw_response.txt").write_text("raw response", encoding="utf-8")
    (cell_dir / "artifact.json").write_text(json.dumps({
        "persisted_complete": True,
        "experiment_id": "mismatched_experiment_id_here",
        "cell_id": "gemini_3_5_flash__ce111_q03_prime_factor_selection__ab2d_spec__seed_2026071301",
        "task_id": "ce111_q03_prime_factor_selection",
        "condition": "ab2d_spec",
        "seed": 2026071301,
        "prompt_sha256": "5417185bc8f5d084bd04d6bf4d346762f6fa4738c6a52d30ea34706f4121e6f0",
        "model_tag": "gemini-3.5-flash",
        "runtime_config_fingerprint": fingerprint
    }), encoding="utf-8")

    with patch.dict(os.environ, {"GEMINI_API_KEY": "dummy_key"}):
        with pytest.raises(RuntimeError, match="INCOMPATIBLE_EXISTING_CELL"):
            execute_generations(manifest, cell_plan)

def test_incomplete_cell_is_quarantined_and_run(tmp_path):
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    manifest["output_root"] = str(tmp_path.relative_to(ROOT)) if tmp_path.is_relative_to(ROOT) else str(tmp_path)
    fingerprint = compute_runtime_fingerprint(manifest)

    cell_plan = [{
        "cell_id": "gemini_3_5_flash__ce111_q03_prime_factor_selection__ab2d_spec__seed_2026071301",
        "task_id": "ce111_q03_prime_factor_selection",
        "condition": "ab2d_spec",
        "seed": 2026071301,
        "model_tag": "gemini-3.5-flash",
        "runtime_parameters": {"temperature": 0.0, "max_output_tokens": 24576, "timeout_seconds": 600},
        "prompt_source": "docs/experiments/prompts/ab2d_spec/prompts/ce111_q03_prime_factor_selection.txt",
        "prompt_sha256": "5417185bc8f5d084bd04d6bf4d346762f6fa4738c6a52d30ea34706f4121e6f0",
        "output_relative_path": "cells/cell_001"
    }]

    cell_dir = tmp_path / "cells/cell_001"
    cell_dir.mkdir(parents=True)
    # incomplete artifact: persisted_complete = False
    (cell_dir / "raw_response.txt").write_text("raw response", encoding="utf-8")
    (cell_dir / "artifact.json").write_text(json.dumps({
        "persisted_complete": False,
        "experiment_id": manifest["experiment_id"],
        "cell_id": "gemini_3_5_flash__ce111_q03_prime_factor_selection__ab2d_spec__seed_2026071301",
        "task_id": "ce111_q03_prime_factor_selection",
        "condition": "ab2d_spec",
        "seed": 2026071301,
        "prompt_sha256": "5417185bc8f5d084bd04d6bf4d346762f6fa4738c6a52d30ea34706f4121e6f0",
        "model_tag": "gemini-3.5-flash",
        "runtime_config_fingerprint": fingerprint
    }), encoding="utf-8")

    with patch.dict(os.environ, {"GEMINI_API_KEY": "dummy_key"}):
        with patch("scripts.ce115_v4_gemini_transport.call_gemini_once", return_value={"raw_text": "fresh response", "metadata": {}}):
            execute_generations(manifest, cell_plan)

    # Verify quarantine directory exists and contains old files
    quarantine_base = tmp_path / "_quarantine" / "gemini_3_5_flash__ce111_q03_prime_factor_selection__ab2d_spec__seed_2026071301"
    assert quarantine_base.exists()
    runs = list(quarantine_base.iterdir())
    assert len(runs) == 1
    assert (runs[0] / "raw_response.txt").exists()
    assert (runs[0] / "artifact.json").exists()

    # Verify cell_dir has been populated with fresh run
    fresh_art = json.loads((cell_dir / "artifact.json").read_text(encoding="utf-8"))
    assert fresh_art["persisted_complete"] is True
    assert fresh_art["raw_response"] == "fresh response"

def test_quarantine_failure_aborts_execution(tmp_path):
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    manifest["output_root"] = str(tmp_path.relative_to(ROOT)) if tmp_path.is_relative_to(ROOT) else str(tmp_path)
    fingerprint = compute_runtime_fingerprint(manifest)

    cell_plan = [{
        "cell_id": "gemini_3_5_flash__ce111_q03_prime_factor_selection__ab2d_spec__seed_2026071301",
        "task_id": "ce111_q03_prime_factor_selection",
        "condition": "ab2d_spec",
        "seed": 2026071301,
        "model_tag": "gemini-3.5-flash",
        "runtime_parameters": {"temperature": 0.0, "max_output_tokens": 24576, "timeout_seconds": 600},
        "prompt_source": "dummy_path",
        "prompt_sha256": "5417185bc8f5d084bd04d6bf4d346762f6fa4738c6a52d30ea34706f4121e6f0",
        "output_relative_path": "cells/cell_001"
    }]

    cell_dir = tmp_path / "cells/cell_001"
    cell_dir.mkdir(parents=True)
    (cell_dir / "raw_response.txt").write_text("raw response", encoding="utf-8")
    (cell_dir / "artifact.json").write_text(json.dumps({
        "persisted_complete": False,
        "experiment_id": manifest["experiment_id"],
        "cell_id": "gemini_3_5_flash__ce111_q03_prime_factor_selection__ab2d_spec__seed_2026071301",
        "task_id": "ce111_q03_prime_factor_selection",
        "condition": "ab2d_spec",
        "seed": 2026071301,
        "prompt_sha256": "5417185bc8f5d084bd04d6bf4d346762f6fa4738c6a52d30ea34706f4121e6f0",
        "model_tag": "gemini-3.5-flash",
        "runtime_config_fingerprint": fingerprint
    }), encoding="utf-8")

    # Mock rename to fail cross-device rename and files rename
    with patch.object(Path, "rename", side_effect=OSError("permission denied")):
        with patch.dict(os.environ, {"GEMINI_API_KEY": "dummy_key"}):
            with patch("scripts.ce115_v4_gemini_transport.call_gemini_once") as mock_call:
                with pytest.raises(RuntimeError, match="QUARANTINE_FAILED"):
                    execute_generations(manifest, cell_plan)
                # Model call should never execute
                mock_call.assert_not_called()

def test_mismatch_never_quarantines_or_overwrites(tmp_path):
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    manifest["output_root"] = str(tmp_path.relative_to(ROOT)) if tmp_path.is_relative_to(ROOT) else str(tmp_path)
    fingerprint = compute_runtime_fingerprint(manifest)

    cell_plan = [{
        "cell_id": "gemini_3_5_flash__ce111_q03_prime_factor_selection__ab2d_spec__seed_2026071301",
        "task_id": "ce111_q03_prime_factor_selection",
        "condition": "ab2d_spec",
        "seed": 2026071301,
        "model_tag": "gemini-3.5-flash",
        "runtime_parameters": {"temperature": 0.0, "max_output_tokens": 24576, "timeout_seconds": 600},
        "prompt_source": "dummy_path",
        "prompt_sha256": "5417185bc8f5d084bd04d6bf4d346762f6fa4738c6a52d30ea34706f4121e6f0",
        "output_relative_path": "cells/cell_001"
    }]

    cell_dir = tmp_path / "cells/cell_001"
    cell_dir.mkdir(parents=True)
    (cell_dir / "raw_response.txt").write_text("raw response", encoding="utf-8")
    (cell_dir / "artifact.json").write_text(json.dumps({
        "persisted_complete": True,
        "experiment_id": "mismatched_experiment_id_here",
        "cell_id": "gemini_3_5_flash__ce111_q03_prime_factor_selection__ab2d_spec__seed_2026071301",
        "task_id": "ce111_q03_prime_factor_selection",
        "condition": "ab2d_spec",
        "seed": 2026071301,
        "prompt_sha256": "5417185bc8f5d084bd04d6bf4d346762f6fa4738c6a52d30ea34706f4121e6f0",
        "model_tag": "gemini-3.5-flash",
        "runtime_config_fingerprint": fingerprint
    }), encoding="utf-8")

    with patch.dict(os.environ, {"GEMINI_API_KEY": "dummy_key"}):
        with patch("scripts.ce115_v4_gemini_transport.call_gemini_once") as mock_call:
            with pytest.raises(RuntimeError, match="INCOMPATIBLE_EXISTING_CELL"):
                execute_generations(manifest, cell_plan)
            # Verify no quarantine directory is created
            assert not (tmp_path / "_quarantine").exists()
            # Verify mock call is not executed
            mock_call.assert_not_called()

def test_overwrite_policy_aborts_on_incompatible_manifest(tmp_path):
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    manifest["output_root"] = str(tmp_path.relative_to(ROOT)) if tmp_path.is_relative_to(ROOT) else str(tmp_path)

    tmp_path.mkdir(parents=True, exist_ok=True)
    (tmp_path / "manifest.json").write_text(json.dumps({
        "experiment_id": "wholly_different_experiment_id_here"
    }), encoding="utf-8")

    with pytest.raises(RuntimeError, match="incompatible experiment_id"):
        execute_generations(manifest, [])
