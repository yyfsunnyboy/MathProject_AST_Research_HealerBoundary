"""QFIX-001: null-safe Ab2d+full artifact assembly regression and formal integration."""
from __future__ import annotations

import hashlib
import importlib
import json
from pathlib import Path

import pytest

from agent_tools.finals_rebuild.math16_ab2d_full_artifact_assembly import (
    QFIX_001_ID,
    build_evaluation_result,
    encode_returned_value_for_artifact,
    write_artifact_manifest,
    write_evaluation_artifacts,
)

ROOT = Path(__file__).resolve().parents[2]
QUAL_CELLS = ROOT / "artifacts/math16_ab2d_full_domain_assisted_v1/qualification/cells"


def test_qfix001_encode_passed_with_none_returned_value():
    details = {
        "structural_ok": True,
        "latex_ok": True,
        "ledger_stage": "ok",
        # intentionally no returned_value
    }
    # Pre-fix bug: sorted(None) when treating returned as present on pass.
    with pytest.raises(TypeError):
        sorted(details.get("returned_value"))  # type: ignore[arg-type]

    encoded = encode_returned_value_for_artifact("passed", details)
    assert isinstance(encoded, dict)
    assert "detail_keys" in encoded
    assert encoded["detail_keys"] == sorted(details.keys())


def test_qfix001_build_evaluation_and_write_artifact_when_returned_none(tmp_path: Path):
    details = {"structural_ok": True, "latex_ok": True, "actual_question_text": "q"}
    evaluation = build_evaluation_result(
        outcome="passed",
        source="def generate(level=1, **kwargs):\n    return {'question_text':'q','correct_answer':1,'oracle_payload':{}}\n",
        details=details,
        frozen_params={},
    )
    assert evaluation["outcome"] == "passed"
    assert evaluation["authoritative_evaluator_outcome"] == "passed"
    assert evaluation["three_key_output"] is True
    assert evaluation["returned_value"] is not None

    cell_dir = tmp_path / "cell"
    cell_dir.mkdir()
    (cell_dir / "prompt.txt").write_text("p", encoding="utf-8")
    (cell_dir / "raw_response.txt").write_text("raw", encoding="utf-8")
    (cell_dir / "request_metadata.json").write_text("{}", encoding="utf-8")
    (cell_dir / "logs.json").write_text("{}", encoding="utf-8")
    write_evaluation_artifacts(cell_dir, evaluation=evaluation, outcome="passed")
    art = write_artifact_manifest(
        cell_dir,
        {
            "cell_id": "test",
            "outcome": "passed",
            "persisted_complete": True,
            "artifact_assembly": QFIX_001_ID,
        },
    )
    assert (cell_dir / "artifact.json").is_file()
    assert (cell_dir / "evaluation_result.json").is_file()
    assert art["persisted_complete"] is True
    assert art["qfix_001_applied"] is True
    loaded = json.loads((cell_dir / "evaluation_result.json").read_text(encoding="utf-8"))
    assert loaded["outcome"] == "passed"


def test_formal_runner_imports_shared_assembly():
    mod = importlib.import_module("scripts.run_math16_ab2d_full_gemini_formal")
    assert mod.build_evaluation_result is build_evaluation_result
    assert hasattr(mod, "assemble_from_raw")
    assert hasattr(mod, "execute_formal_cell")
    assert mod.FORMAL_ROOT.name == "gemini"
    # 80-cell plan loader
    if (ROOT / "artifacts/math16_ab2d_full_domain_assisted_v1/preregistration/cell_manifest.jsonl").exists():
        cells = mod.load_gemini_manifest_cells()
        assert len(cells) == 80


@pytest.mark.skipif(not QUAL_CELLS.exists(), reason="qualification cells not present locally")
def test_qualification_raw_replay_via_formal_runner(tmp_path: Path):
    """Replay uses preserved raw only; no model transport import call."""
    import scripts.run_math16_ab2d_full_gemini_formal as formal

    before = {}
    for cell_dir in sorted(QUAL_CELLS.glob("gemini__*")):
        raw = cell_dir / "raw_response.txt"
        ext = cell_dir / "extracted_source.py"
        ev = cell_dir / "evaluation_result.json"
        before[cell_dir.name] = {
            "raw": hashlib.sha256(raw.read_bytes()).hexdigest(),
            "extracted": hashlib.sha256(ext.read_bytes()).hexdigest() if ext.exists() else None,
            "evaluation": hashlib.sha256(ev.read_bytes()).hexdigest() if ev.exists() else None,
            "outcome": json.loads(ev.read_text(encoding="utf-8"))["outcome"] if ev.exists() else None,
        }

    # Monkeypatch call_gemini_once to fail loudly if invoked
    def _forbid_model(*_a, **_k):
        raise AssertionError("model call forbidden during QFIX-001 replay")

    formal.call_gemini_once = _forbid_model  # type: ignore[attr-defined]
    result = formal.replay_qualification_assembly()
    assert result["model_calls"] == 0
    assert result["replayed"] >= 3  # at least non-integer cells present
    assert result["all_raw_unchanged"] is True
    assert result["all_extracted_unchanged"] is True
    assert result["all_artifacts_complete"] is True

    for cell_dir in sorted(QUAL_CELLS.glob("gemini__*")):
        name = cell_dir.name
        raw_h = hashlib.sha256((cell_dir / "raw_response.txt").read_bytes()).hexdigest()
        assert raw_h == before[name]["raw"]
        ext = cell_dir / "extracted_source.py"
        if before[name]["extracted"] is not None:
            assert hashlib.sha256(ext.read_bytes()).hexdigest() == before[name]["extracted"]
        ev = json.loads((cell_dir / "evaluation_result.json").read_text(encoding="utf-8"))
        assert ev["outcome"] == before[name]["outcome"]
        # evaluation file may gain identical null-safe encoding; hash may match after freeze
        after_ev = hashlib.sha256((cell_dir / "evaluation_result.json").read_bytes()).hexdigest()
        if before[name]["evaluation"] is not None:
            assert after_ev == before[name]["evaluation"]
        assert (cell_dir / "artifact.json").is_file()
