import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs/experiments/results/math16_method2_all_cell_replay_v1"
JOURNAL = OUT / "eligibility_journal.jsonl"


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _rows():
    return [
        json.loads(line)
        for line in JOURNAL.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def test_phase_a_has_complete_unique_320_cell_journal():
    rows = _rows()
    ids = [row["cell_identity"]["cell_id"] for row in rows]
    assert len(rows) == 320
    assert len(set(ids)) == 320
    assert all(row["eligibility_checked"] is True for row in rows)


def test_phase_a_has_no_evaluation_values():
    for row in _rows():
        assert row["raw_status"] is None
        assert row["final_status"] is None
        assert row["transition"] is None


def test_phase_a_source_files_and_byte_comparisons_close():
    rows = _rows()
    raw_dir = OUT / "raw_sources"
    final_dir = OUT / "final_sources"
    assert raw_dir.resolve() != final_dir.resolve()
    assert len(list(raw_dir.glob("*.py"))) == 320
    assert len(list(final_dir.glob("*.py"))) == 320
    for row in rows:
        cell_id = row["cell_identity"]["cell_id"]
        raw = raw_dir / f"{cell_id}.py"
        final = final_dir / f"{cell_id}.py"
        raw_bytes = raw.read_bytes()
        final_bytes = final.read_bytes()
        assert hashlib.sha256(raw_bytes).hexdigest() == row["raw_source_sha256"]
        assert hashlib.sha256(final_bytes).hexdigest() == row["final_source_sha256"]
        assert row["source_changed"] is (raw_bytes != final_bytes)
        if not row["eligible"]:
            assert raw_bytes == final_bytes


def test_phase_a_freeze_pins_journal_and_closures():
    freeze = json.loads((OUT / "phase_a_freeze.json").read_text(encoding="utf-8"))
    summary = json.loads((OUT / "phase_a_summary.json").read_text(encoding="utf-8"))
    assert freeze["cells"] == 320
    assert freeze["journal_sha256"] == _sha(JOURNAL)
    assert summary["journal_sha256"] == freeze["journal_sha256"]
    assert (
        summary["journal_record_closure_sha256"]
        == freeze["journal_record_closure_sha256"]
    )
    assert summary["source_sha_closure"] == freeze["source_sha_closure"]
    assert summary["evaluator_executed"] is False
    assert summary["model_calls"] == 0
