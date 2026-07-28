"""Evaluate frozen Method 2 Raw and Final sources independently (Phase B)."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.math16_pool import frozen_for_prompt, tasks_by_id  # noqa: E402
from scripts.evaluate_math16_pilot02_full_v4 import (  # noqa: E402
    _load_family_and_api_policy,
    classify_outcome_to_v3,
)
from scripts.preflight_math16_method2_all_cell import (  # noqa: E402
    MANIFEST_PATH,
    classify_transition,
    load_manifest,
    verify_pins,
)
from scripts.run_math16_latex_v1_gemini_live import (  # noqa: E402
    classify_math16_response,
)


EXPECTED_PHASE_A_JOURNAL_SHA256 = (
    "1fd8aab4a7dadfeaca58af51b65bfb4c1f860037b218468dec844bc7ce9198f6"
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def write_json(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def validate_phase_a_inputs(
    manifest: dict[str, Any],
) -> tuple[list[dict[str, Any]], Path, Path, Path]:
    verify_pins(manifest)
    expected = int(manifest["population"]["expected_cells"])
    out_root = ROOT / manifest["outputs"]["root"]
    raw_dir = ROOT / manifest["outputs"]["raw_source_directory"]
    final_dir = ROOT / manifest["outputs"]["final_source_directory"]
    phase_a_journal = ROOT / manifest["outputs"]["eligibility_journal"]
    actual_journal_sha = sha256_bytes(phase_a_journal.read_bytes())
    if actual_journal_sha != EXPECTED_PHASE_A_JOURNAL_SHA256:
        raise RuntimeError(f"PHASE_A_JOURNAL_SHA_DRIFT: {actual_journal_sha}")
    freeze = json.loads((out_root / "phase_a_freeze.json").read_text(encoding="utf-8"))
    if freeze["journal_sha256"] != actual_journal_sha:
        raise RuntimeError("PHASE_A_FREEZE_JOURNAL_SHA_DRIFT")

    rows = load_jsonl(phase_a_journal)
    if len(rows) != expected:
        raise RuntimeError(f"PHASE_A_ROW_COUNT_MISMATCH: {len(rows)}")
    ids = [row["cell_identity"]["cell_id"] for row in rows]
    if len(set(ids)) != expected:
        raise RuntimeError("PHASE_A_IDENTITY_MISSING_OR_DUPLICATE")
    if len(list(raw_dir.glob("*.py"))) != expected:
        raise RuntimeError("RAW_SOURCE_FILE_COUNT_MISMATCH")
    if len(list(final_dir.glob("*.py"))) != expected:
        raise RuntimeError("FINAL_SOURCE_FILE_COUNT_MISMATCH")
    if raw_dir.resolve() == final_dir.resolve():
        raise RuntimeError("RAW_FINAL_PATH_COLLISION")

    for row in rows:
        cell_id = row["cell_identity"]["cell_id"]
        raw_bytes = (raw_dir / f"{cell_id}.py").read_bytes()
        final_bytes = (final_dir / f"{cell_id}.py").read_bytes()
        if sha256_bytes(raw_bytes) != row["raw_source_sha256"]:
            raise RuntimeError(f"RAW_SOURCE_SHA_DRIFT: {cell_id}")
        if sha256_bytes(final_bytes) != row["final_source_sha256"]:
            raise RuntimeError(f"FINAL_SOURCE_SHA_DRIFT: {cell_id}")
        if (raw_bytes != final_bytes) != row["source_changed"]:
            raise RuntimeError(f"SOURCE_CHANGED_DRIFT: {cell_id}")
        if not row["eligible"] and raw_bytes != final_bytes:
            raise RuntimeError(f"NONELIGIBLE_SOURCE_DRIFT: {cell_id}")
    return rows, raw_dir, final_dir, out_root


def score_source(
    source: str,
    *,
    task: dict[str, Any],
    frozen_params: dict[str, Any],
    api_policy: str,
) -> dict[str, Any]:
    outcome, _source, details = classify_math16_response(
        source,
        frozen_params=frozen_params,
        audit_oracle_payload=task["oracle_payload"],
        task=task,
    )
    mapped = classify_outcome_to_v3(outcome, details, api_policy=api_policy)
    status = mapped["final_status"]
    if status not in {"PASSED", "FAILED"}:
        raise RuntimeError(f"UNEXPECTED_EVALUATOR_STATUS: {status}")
    return {
        "status": status,
        "classifier_outcome": outcome,
        "primary_failure_layer": mapped["primary_failure_layer"],
        "failure_subtype": mapped["failure_subtype"],
    }


def _transition_counts(rows: list[dict[str, Any]]) -> dict[str, int]:
    counts = Counter(row["transition"] for row in rows)
    return {
        name: counts[name]
        for name in (
            "verified_rescue",
            "regression",
            "preserved_pass",
            "still_failed",
        )
    }


def _accounting(rows: list[dict[str, Any]]) -> dict[str, Any]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[row["rule_id"] or "NONELIGIBLE"].append(row)
    result: dict[str, Any] = {}
    for rule_id in sorted(grouped):
        items = grouped[rule_id]
        result[rule_id] = {
            "cells": len(items),
            "eligible": sum(bool(item["eligible"]) for item in items),
            "source_changed": sum(bool(item["source_changed"]) for item in items),
            "raw_pass": sum(item["raw_status"] == "PASSED" for item in items),
            "final_pass": sum(item["final_status"] == "PASSED" for item in items),
            "transitions": _transition_counts(items),
        }
    return result


def execute_phase_b(manifest_path: Path = MANIFEST_PATH) -> dict[str, Any]:
    manifest = load_manifest(manifest_path)
    phase_a_rows, raw_dir, final_dir, out_root = validate_phase_a_inputs(manifest)
    transition_path = ROOT / manifest["outputs"]["transition_journal"]
    eligible_path = out_root / "phase_b_eligible_11_results.jsonl"
    changed_path = out_root / "phase_b_source_changed_11_results.jsonl"
    rule_path = out_root / "phase_b_rule_accounting.json"
    summary_path = out_root / "phase_b_summary.json"
    summary_md_path = out_root / "phase_b_summary.md"
    new_outputs = (
        transition_path,
        eligible_path,
        changed_path,
        rule_path,
        summary_path,
        summary_md_path,
    )
    existing = [str(path) for path in new_outputs if path.exists()]
    if existing:
        raise RuntimeError(f"PHASE_B_OUTPUT_ALREADY_EXISTS: {existing}")

    tasks = tasks_by_id()
    _, api_policy_map = _load_family_and_api_policy()
    result_rows: list[dict[str, Any]] = []
    try:
        for index, phase_a in enumerate(phase_a_rows, start=1):
            identity = phase_a["cell_identity"]
            cell_id = identity["cell_id"]
            task = tasks[identity["task_id"]]
            frozen_params = frozen_for_prompt(task)["oracle_payload"]
            api_policy = api_policy_map[identity["task_id"]]
            raw_source = (raw_dir / f"{cell_id}.py").read_text(encoding="utf-8")
            final_source = (final_dir / f"{cell_id}.py").read_text(encoding="utf-8")

            raw_score = score_source(
                raw_source,
                task=task,
                frozen_params=frozen_params,
                api_policy=api_policy,
            )
            final_score = score_source(
                final_source,
                task=task,
                frozen_params=frozen_params,
                api_policy=api_policy,
            )
            transition = classify_transition(
                raw_score["status"], final_score["status"]
            )
            result_rows.append(
                {
                    "cell_identity": identity,
                    "raw_source_sha256": phase_a["raw_source_sha256"],
                    "final_source_sha256": phase_a["final_source_sha256"],
                    "eligibility_checked": phase_a["eligibility_checked"],
                    "eligible": phase_a["eligible"],
                    "rule_id": phase_a["rule_id"],
                    "rule_triggered": phase_a["rule_triggered"],
                    "source_changed": phase_a["source_changed"],
                    "raw_status": raw_score["status"],
                    "final_status": final_score["status"],
                    "transition": transition,
                    "raw_classifier_outcome": raw_score["classifier_outcome"],
                    "final_classifier_outcome": final_score["classifier_outcome"],
                    "raw_primary_failure_layer": raw_score["primary_failure_layer"],
                    "final_primary_failure_layer": final_score[
                        "primary_failure_layer"
                    ],
                    "raw_failure_subtype": raw_score["failure_subtype"],
                    "final_failure_subtype": final_score["failure_subtype"],
                }
            )
            if index % 20 == 0:
                print(f"[{index}/320] evaluated Raw and Final independently")

        if len(result_rows) != 320:
            raise RuntimeError(f"PHASE_B_RESULT_COUNT_MISMATCH: {len(result_rows)}")
        transitions = _transition_counts(result_rows)
        if sum(transitions.values()) != 320:
            raise RuntimeError("TRANSITION_COUNT_CLOSURE_FAILURE")
        eligible_rows = [row for row in result_rows if row["eligible"]]
        changed_rows = [row for row in result_rows if row["source_changed"]]
        if len(eligible_rows) != 11 or len(changed_rows) != 11:
            raise RuntimeError(
                f"PHASE_A_SUBSET_DRIFT: eligible={len(eligible_rows)} "
                f"changed={len(changed_rows)}"
            )

        write_jsonl(transition_path, result_rows)
        write_jsonl(eligible_path, eligible_rows)
        write_jsonl(changed_path, changed_rows)
        rule_accounting = _accounting(result_rows)
        write_json(rule_path, rule_accounting)
        journal_sha = sha256_bytes(transition_path.read_bytes())
        raw_pass = sum(row["raw_status"] == "PASSED" for row in result_rows)
        final_pass = sum(row["final_status"] == "PASSED" for row in result_rows)
        regressions = [
            row["cell_identity"]["cell_id"]
            for row in result_rows
            if row["transition"] == "regression"
        ]
        summary = {
            "phase": "Method 2 Phase B independent Raw/Final evaluation",
            "status": "COMPLETE_FROZEN",
            "cells": 320,
            "raw_evaluations": 320,
            "final_evaluations": 320,
            "raw_pass": raw_pass,
            "final_pass": final_pass,
            "net_pass_change": final_pass - raw_pass,
            "transitions": transitions,
            "eligible_cells": 11,
            "source_changed_cells": 11,
            "eligible_transitions": _transition_counts(eligible_rows),
            "source_changed_transitions": _transition_counts(changed_rows),
            "regression_cell_ids": regressions,
            "rule_accounting": rule_accounting,
            "phase_a_journal_sha256": EXPECTED_PHASE_A_JOURNAL_SHA256,
            "phase_b_journal_sha256": journal_sha,
            "evaluator": manifest["evaluation"]["evaluator"],
            "model_calls": 0,
            "phase_a_sources_modified": False,
            "phase_a_eligibility_journal_modified": False,
        }
        write_json(summary_path, summary)
        summary_md_path.write_text(
            "\n".join(
                [
                    "# Math16 Method 2 Phase B Summary",
                    "",
                    f"- Raw PASS / Final PASS: **{raw_pass} / {final_pass}**",
                    f"- Net PASS change: **{final_pass - raw_pass:+d}**",
                    f"- Verified rescue: **{transitions['verified_rescue']}**",
                    f"- Regression: **{transitions['regression']}**",
                    f"- Preserved pass: **{transitions['preserved_pass']}**",
                    f"- Still failed: **{transitions['still_failed']}**",
                    f"- Eligible / source changed: **{len(eligible_rows)} / {len(changed_rows)}**",
                    f"- Regression cell IDs: `{regressions}`",
                    f"- Phase B journal SHA-256: `{journal_sha}`",
                    "- Model calls: **0**",
                    "",
                ]
            ),
            encoding="utf-8",
            newline="\n",
        )
        return summary
    except Exception:
        for path in new_outputs:
            if path.exists():
                path.unlink()
        raise


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=MANIFEST_PATH)
    args = parser.parse_args()
    summary = execute_phase_b(args.manifest.resolve())
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
