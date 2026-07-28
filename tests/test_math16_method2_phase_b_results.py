import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs/experiments/results/math16_method2_all_cell_replay_v1"
PHASE_A = OUT / "eligibility_journal.jsonl"
PHASE_B = OUT / "transition_journal.jsonl"


def _rows(path: Path):
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_phase_b_closes_320_independent_raw_final_results():
    rows = _rows(PHASE_B)
    ids = [row["cell_identity"]["cell_id"] for row in rows]
    assert len(rows) == 320
    assert len(set(ids)) == 320
    assert all(row["raw_status"] in {"PASSED", "FAILED"} for row in rows)
    assert all(row["final_status"] in {"PASSED", "FAILED"} for row in rows)


def test_transition_is_derived_only_from_status_pair():
    expected = {
        ("FAILED", "PASSED"): "verified_rescue",
        ("PASSED", "FAILED"): "regression",
        ("PASSED", "PASSED"): "preserved_pass",
        ("FAILED", "FAILED"): "still_failed",
    }
    for row in _rows(PHASE_B):
        assert row["transition"] == expected[
            (row["raw_status"], row["final_status"])
        ]


def test_phase_a_journal_and_sources_remain_frozen():
    summary = json.loads((OUT / "phase_b_summary.json").read_text(encoding="utf-8"))
    phase_a_rows = _rows(PHASE_A)
    phase_b = {row["cell_identity"]["cell_id"]: row for row in _rows(PHASE_B)}
    assert _sha(PHASE_A) == summary["phase_a_journal_sha256"]
    assert len(phase_a_rows) == 320
    for row in phase_a_rows:
        cell_id = row["cell_identity"]["cell_id"]
        raw = OUT / "raw_sources" / f"{cell_id}.py"
        final = OUT / "final_sources" / f"{cell_id}.py"
        assert _sha(raw) == row["raw_source_sha256"]
        assert _sha(final) == row["final_source_sha256"]
        assert phase_b[cell_id]["raw_source_sha256"] == row["raw_source_sha256"]
        assert phase_b[cell_id]["final_source_sha256"] == row[
            "final_source_sha256"
        ]


def test_phase_b_summary_subsets_and_journal_sha_close():
    rows = _rows(PHASE_B)
    summary = json.loads((OUT / "phase_b_summary.json").read_text(encoding="utf-8"))
    eligible = [row for row in rows if row["eligible"]]
    changed = [row for row in rows if row["source_changed"]]
    transitions = Counter(row["transition"] for row in rows)
    assert len(eligible) == 11
    assert len(changed) == 11
    assert sum(transitions.values()) == 320
    assert summary["phase_b_journal_sha256"] == _sha(PHASE_B)
    assert summary["raw_pass"] == sum(row["raw_status"] == "PASSED" for row in rows)
    assert summary["final_pass"] == sum(
        row["final_status"] == "PASSED" for row in rows
    )
    assert summary["net_pass_change"] == (
        summary["final_pass"] - summary["raw_pass"]
    )
    assert len(_rows(OUT / "phase_b_eligible_11_results.jsonl")) == 11
    assert len(_rows(OUT / "phase_b_source_changed_11_results.jsonl")) == 11
