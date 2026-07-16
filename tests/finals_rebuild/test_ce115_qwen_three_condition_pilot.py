import json

import pytest

from scripts import run_ce115_qwen_three_condition_pilot as pilot
from scripts.ce115_qwen_ollama_transport import MODEL_ID, build_chat_payload


def test_plan_is_exact_frozen_nine_cell_matrix(tmp_path):
    plan = pilot.build_plan(tmp_path / "new")
    assert plan["planned_cells"] == 9
    assert plan["model"] == "qwen3.5:4b"
    assert plan["think"] is False
    assert plan["api"] == "/api/chat"
    assert {(c["task_id"], c["condition"]) for c in plan["cells"]} == {
        (task, condition) for task in pilot.TASK_IDS for condition in pilot.CONDITIONS
    }
    assert {c["seed"] for c in plan["cells"]} == {2026071301}
    assert {c["model"] for c in plan["cells"]} == {"qwen3.5:4b"}
    assert pilot.EXCLUDED_TASK not in {c["task_id"] for c in plan["cells"]}
    for task in pilot.TASK_IDS:
        assert len({json.dumps(c["frozen_parameters"], sort_keys=True) for c in plan["cells"] if c["task_id"] == task}) == 1
    assert all("## Clean-incremental DOMAIN" in c["prompt"] for c in plan["cells"] if c["condition"] == "ab2d")
    assert all("CE115 Ab2d-Assembly domain contract" not in c["prompt"] for c in plan["cells"])
    assert all(c["request_think"] is False for c in plan["cells"])
    assert plan["prompt_lineage"] == "ce115_clean_incremental_ablation_v1"


def test_think_false_is_top_level_on_chat_payload():
    payload = build_chat_payload("hello", seed=2026071301, model=MODEL_ID)
    assert payload["think"] is False
    assert "think" not in payload["options"]
    assert payload["model"] == "qwen3.5:4b"
    assert payload["stream"] is False


def test_preflight_zero_model_calls_and_fail_closed_without_ollama(tmp_path, monkeypatch):
    def boom(*_a, **_k):
        raise ConnectionError("offline")

    monkeypatch.setattr(pilot, "probe_ollama", boom)
    pf = pilot.preflight(tmp_path / "new", require_ollama=True)
    assert pf["checks"]["real_model_calls"] == 0
    assert pf["checks"]["blocker"] == "OLLAMA_REQUIRED"
    assert not (tmp_path / "new").exists()


def test_preflight_passes_without_service_when_not_required(tmp_path):
    pf = pilot.preflight(tmp_path / "new", require_ollama=False)
    assert pf["checks"]["passed"] is True
    assert pf["checks"]["real_model_calls"] == 0
    assert pf["checks"]["think_false_top_level"] is True
    assert not (tmp_path / "new").exists()


def test_output_isolation(tmp_path):
    occupied = tmp_path / "occupied"
    occupied.mkdir()
    assert pilot.preflight(occupied, require_ollama=False)["checks"]["output_isolated"] is False
    with pytest.raises(RuntimeError):
        pilot.run(occupied, transport=lambda _: {}, require_ollama=False)


def test_mock_run_artifact_schema_and_model_failure_accounting(tmp_path):
    output = tmp_path / "pilot"

    def fake(_prompt):
        return {
            "raw_text": "def generate(level=1, **kwargs):\n    raise RuntimeError('candidate boom')\n",
            "metadata": {"total_token_count": 7, "think": False, "prompt_eval_count": 3, "eval_count": 4},
        }

    rows = pilot.run(output, transport=fake, require_ollama=False)
    assert len(rows) == 9
    assert all(r["failure_class"] == "model_generated_failure" for r in rows)
    required = {
        "run_id",
        "cell_id",
        "task_id",
        "family",
        "condition",
        "seed",
        "model",
        "prompt_hash",
        "completion_status",
        "adoption_status",
        "evaluator_status",
        "exception_type",
        "traceback",
        "token_metadata",
        "duration_metadata",
        "hashes",
        "artifact_sha256",
        "retry",
        "healer",
        "first_attempt_only",
    }
    assert all(required <= set(r) for r in rows)
    assert all(r["model"] == "qwen3.5:4b" for r in rows)
    assert all(r["retry"] == 0 and r["healer"] == 0 and r["first_attempt_only"] is True for r in rows)
    assert all(isinstance(r["artifact_sha256"], str) and len(r["artifact_sha256"]) == 64 for r in rows)
    assert len(list((output / "cells").glob("*/artifact.json"))) == 9
    assert (output / "manifest.json").is_file()
    assert (output / "summary.json").is_file()


def test_transport_failure_is_separate_from_model_failure(tmp_path):
    def broken_transport(_prompt):
        raise ConnectionError("offline")

    rows = pilot.run(tmp_path / "transport_failure", transport=broken_transport, require_ollama=False)
    assert len(rows) == 9
    assert all(r["failure_class"] == "transport_or_infrastructure_failure" for r in rows)
    assert all(r["exception_type"] == "ConnectionError" for r in rows)
