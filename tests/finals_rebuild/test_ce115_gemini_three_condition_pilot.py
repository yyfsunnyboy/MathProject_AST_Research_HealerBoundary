import json

import pytest

from scripts import run_ce115_gemini_three_condition_pilot as pilot


def test_plan_is_exact_frozen_nine_cell_matrix(tmp_path):
    plan = pilot.build_plan(tmp_path / "new")
    assert plan["planned_cells"] == 9
    assert {(c["task_id"], c["condition"]) for c in plan["cells"]} == {
        (task, condition) for task in pilot.TASK_IDS for condition in pilot.CONDITIONS
    }
    assert {c["seed"] for c in plan["cells"]} == {2026071301}
    assert {c["model"] for c in plan["cells"]} == {"gemini-3.5-flash"}
    assert pilot.EXCLUDED_TASK not in {c["task_id"] for c in plan["cells"]}
    for task in pilot.TASK_IDS:
        assert len({json.dumps(c["frozen_parameters"], sort_keys=True) for c in plan["cells"] if c["task_id"] == task}) == 1
    assert all("## Clean-incremental DOMAIN" in c["prompt"] for c in plan["cells"] if c["condition"] == "ab2d")
    assert all("CE115 Ab2d-Assembly domain contract" not in c["prompt"] for c in plan["cells"])
    assert plan["prompt_lineage"] == "ce115_clean_incremental_ablation_v1"


def test_preflight_fail_closed_and_never_calls_transport(tmp_path, monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    assert pilot.preflight(tmp_path / "new")["checks"]["blocker"] == "API_KEY_REQUIRED"
    assert not (tmp_path / "new").exists()


def test_output_isolation(tmp_path, monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "fake")
    occupied = tmp_path / "occupied"
    occupied.mkdir()
    assert pilot.preflight(occupied)["checks"]["output_isolated"] is False
    with pytest.raises(RuntimeError):
        pilot.run(occupied, transport=lambda _: {})


def test_mock_run_artifact_schema_and_failure_accounting(tmp_path):
    output = tmp_path / "pilot"
    def fake(_prompt):
        return {"raw_text": "def generate(level=1, **kwargs):\n    raise RuntimeError('candidate boom')\n", "metadata": {"total_token_count": 7}}
    rows = pilot.run(output, transport=fake, require_api_key=False)
    assert len(rows) == 9
    assert all(r["failure_class"] == "model_generated_failure" for r in rows)
    required = {"run_id", "cell_id", "task_id", "family", "condition", "seed", "model", "prompt_hash", "completion_status", "adoption_status", "evaluator_status", "exception_type", "traceback", "token_metadata", "duration_metadata", "hashes"}
    assert all(required <= set(r) for r in rows)
    assert len(list((output / "cells").glob("*/artifact.json"))) == 9
    assert (output / "manifest.json").is_file()
    assert (output / "summary.json").is_file()


def test_transport_failure_is_separate_from_model_failure(tmp_path):
    def broken_transport(_prompt):
        raise ConnectionError("offline")
    rows = pilot.run(tmp_path / "transport_failure", transport=broken_transport, require_api_key=False)
    assert len(rows) == 9
    assert all(r["failure_class"] == "transport_or_infrastructure_failure" for r in rows)
    assert all(r["exception_type"] == "ConnectionError" for r in rows)
