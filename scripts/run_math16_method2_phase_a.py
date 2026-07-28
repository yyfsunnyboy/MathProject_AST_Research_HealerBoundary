"""Execute frozen Math16 Method 2 Phase A source decisions.

Phase A only: verify pins, extract raw sources, check Eligibility for all 320
cells, run the frozen Healer for eligible cells, and freeze Raw/Final sources.
No model, baseline result, or evaluator is loaded or called.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Mapping


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.ce115_research_healer_runner import (  # noqa: E402
    MathHealerRunner,
)
from agent_tools.finals_rebuild.extraction import extract_code  # noqa: E402
from agent_tools.finals_rebuild.math16_pool import frozen_for_prompt, tasks_by_id  # noqa: E402
from scripts.preflight_math16_method2_all_cell import (  # noqa: E402
    JOURNAL_FIELDS,
    MANIFEST_PATH,
    decide_eligibility,
    load_manifest,
    sha256_text,
    verify_pins,
)


PHASE_A_ONLY_FIELDS = (
    "cell_identity",
    "raw_source_sha256",
    "eligibility_checked",
    "eligible",
    "rule_id",
    "rule_triggered",
    "source_changed",
    "final_source_sha256",
    "raw_status",
    "final_status",
    "transition",
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json_sha256(value: Any) -> str:
    encoded = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return sha256_bytes(encoded)


def write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def _cell_identity(cell: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "cell_id": cell["cell_id"],
        "task_id": cell["task_id"],
        "condition": cell["condition"],
        "seed": cell["seed"],
    }


def _assert_phase_a_row(row: Mapping[str, Any]) -> None:
    if tuple(row)[: len(PHASE_A_ONLY_FIELDS)] != PHASE_A_ONLY_FIELDS:
        raise RuntimeError("PHASE_A_JOURNAL_FIELD_DRIFT")
    if tuple(PHASE_A_ONLY_FIELDS) != tuple(JOURNAL_FIELDS):
        raise RuntimeError("FROZEN_JOURNAL_CONTRACT_DRIFT")
    if not row["eligibility_checked"]:
        raise RuntimeError("ELIGIBILITY_NOT_CHECKED")
    if row["raw_status"] is not None:
        raise RuntimeError("RAW_STATUS_FORBIDDEN_IN_PHASE_A")
    if row["final_status"] is not None:
        raise RuntimeError("FINAL_STATUS_FORBIDDEN_IN_PHASE_A")
    if row["transition"] is not None:
        raise RuntimeError("TRANSITION_FORBIDDEN_IN_PHASE_A")
    if not row["eligible"] and (
        row["raw_source_sha256"] != row["final_source_sha256"]
        or row["source_changed"]
    ):
        raise RuntimeError("NONELIGIBLE_FINAL_SOURCE_DRIFT")


def validate_phase_a(
    *,
    rows: list[dict[str, Any]],
    raw_dir: Path,
    final_dir: Path,
    expected_cells: int,
) -> dict[str, Any]:
    if len(rows) != expected_cells:
        raise RuntimeError(f"JOURNAL_CELL_COUNT_MISMATCH: {len(rows)}")
    cell_ids = [row["cell_identity"]["cell_id"] for row in rows]
    if len(set(cell_ids)) != expected_cells:
        raise RuntimeError("MISSING_OR_DUPLICATE_CELL_ID")
    if raw_dir.resolve() == final_dir.resolve():
        raise RuntimeError("RAW_FINAL_STORAGE_COLLISION")

    raw_files = sorted(raw_dir.glob("*.py"))
    final_files = sorted(final_dir.glob("*.py"))
    if len(raw_files) != expected_cells or len(final_files) != expected_cells:
        raise RuntimeError(
            f"SOURCE_FILE_COUNT_MISMATCH: raw={len(raw_files)} final={len(final_files)}"
        )

    noneligible_identity = 0
    changed = 0
    for row in rows:
        _assert_phase_a_row(row)
        cell_id = row["cell_identity"]["cell_id"]
        raw_bytes = (raw_dir / f"{cell_id}.py").read_bytes()
        final_bytes = (final_dir / f"{cell_id}.py").read_bytes()
        raw_sha = sha256_bytes(raw_bytes)
        final_sha = sha256_bytes(final_bytes)
        actual_changed = raw_bytes != final_bytes
        if raw_sha != row["raw_source_sha256"]:
            raise RuntimeError(f"RAW_SHA_MISMATCH: {cell_id}")
        if final_sha != row["final_source_sha256"]:
            raise RuntimeError(f"FINAL_SHA_MISMATCH: {cell_id}")
        if actual_changed != row["source_changed"]:
            raise RuntimeError(f"SOURCE_CHANGED_MISMATCH: {cell_id}")
        changed += int(actual_changed)
        if not row["eligible"]:
            if raw_bytes != final_bytes:
                raise RuntimeError(f"NONELIGIBLE_BYTES_DIFFER: {cell_id}")
            noneligible_identity += 1

    return {
        "cells": len(rows),
        "unique_cell_identities": len(set(cell_ids)),
        "eligibility_checked": sum(bool(row["eligibility_checked"]) for row in rows),
        "eligible": sum(bool(row["eligible"]) for row in rows),
        "rule_triggered": sum(bool(row["rule_triggered"]) for row in rows),
        "source_changed": changed,
        "noneligible": sum(not bool(row["eligible"]) for row in rows),
        "noneligible_raw_equals_final": noneligible_identity,
        "raw_source_files": len(raw_files),
        "final_source_files": len(final_files),
        "raw_final_paths_distinct": True,
    }


def execute_phase_a(manifest_path: Path = MANIFEST_PATH) -> dict[str, Any]:
    manifest = load_manifest(manifest_path)
    verify_pins(manifest)
    expected_cells = int(manifest["population"]["expected_cells"])
    plan = json.loads((ROOT / manifest["inputs"]["cell_plan"]).read_text("utf-8"))
    if len(plan) != expected_cells:
        raise RuntimeError(f"CELL_PLAN_COUNT_MISMATCH: {len(plan)}")
    if len({cell["cell_id"] for cell in plan}) != expected_cells:
        raise RuntimeError("CELL_PLAN_IDENTITY_DUPLICATE")

    output_root = ROOT / manifest["outputs"]["root"]
    raw_dir = ROOT / manifest["outputs"]["raw_source_directory"]
    final_dir = ROOT / manifest["outputs"]["final_source_directory"]
    journal_path = ROOT / manifest["outputs"]["eligibility_journal"]
    if output_root.exists():
        raise RuntimeError(f"OUTPUT_ALREADY_EXISTS: {output_root}")
    output_root.mkdir(parents=True)

    tasks = tasks_by_id()
    runner = MathHealerRunner(max_passes=int(manifest["healer"]["max_passes"]))
    rows: list[dict[str, Any]] = []
    extraction_counts: Counter[str] = Counter()
    rule_counts: Counter[str] = Counter()
    try:
        for cell in plan:
            cell_id = cell["cell_id"]
            raw_response_path = (
                ROOT
                / "docs/experiments/results"
                / cell["output_relative_path"]
                / manifest["inputs"]["raw_response_name"]
            )
            extraction = extract_code(raw_response_path.read_text(encoding="utf-8"))
            extraction_counts[extraction.extraction_status] += 1
            raw_source = (
                extraction.extracted_code
                if extraction.extraction_status == "extracted"
                else ""
            )
            frozen = frozen_for_prompt(tasks[cell["task_id"]])["oracle_payload"]
            context = {"frozen": frozen}
            eligibility = decide_eligibility(raw_source or None, context)

            provenance: list[dict[str, Any]] = []
            rolled_back = False
            if eligibility["eligible"]:
                result = runner.run(raw_source, context=context)
                final_source = result.output_source
                rolled_back = bool(result.rolled_back)
                provenance = [
                    {
                        "pass_index": item.pass_index,
                        "selected_rule_id": item.selected_rule_id,
                        "changed": item.changed,
                        "stop_reason": item.stop_reason,
                    }
                    for item in result.provenance
                ]
                for item in provenance:
                    if item["changed"] and item["selected_rule_id"]:
                        rule_counts[item["selected_rule_id"]] += 1
            else:
                final_source = raw_source

            raw_bytes = raw_source.encode("utf-8")
            final_bytes = final_source.encode("utf-8")
            write_bytes(raw_dir / f"{cell_id}.py", raw_bytes)
            write_bytes(final_dir / f"{cell_id}.py", final_bytes)
            row = {
                "cell_identity": _cell_identity(cell),
                "raw_source_sha256": sha256_bytes(raw_bytes),
                "eligibility_checked": True,
                "eligible": bool(eligibility["eligible"]),
                "rule_id": eligibility["rule_id"],
                "rule_triggered": bool(eligibility["rule_triggered"]),
                "source_changed": raw_bytes != final_bytes,
                "final_source_sha256": sha256_bytes(final_bytes),
                "raw_status": None,
                "final_status": None,
                "transition": None,
                "extraction_status": extraction.extraction_status,
                "extraction_method": extraction.extraction_method,
                "rolled_back": rolled_back,
                "healer_provenance": provenance,
            }
            _assert_phase_a_row(row)
            rows.append(row)

        write_jsonl(journal_path, rows)
        validation = validate_phase_a(
            rows=rows,
            raw_dir=raw_dir,
            final_dir=final_dir,
            expected_cells=expected_cells,
        )
        journal_sha256 = sha256_bytes(journal_path.read_bytes())
        journal_record_closure = canonical_json_sha256(
            sorted(rows, key=lambda row: row["cell_identity"]["cell_id"])
        )
        source_sha_closure = canonical_json_sha256(
            sorted(
                [
                    {
                        "cell_id": row["cell_identity"]["cell_id"],
                        "raw_source_sha256": row["raw_source_sha256"],
                        "final_source_sha256": row["final_source_sha256"],
                    }
                    for row in rows
                ],
                key=lambda item: item["cell_id"],
            )
        )
        summary = {
            "phase": "Method 2 Phase A source decisions",
            "status": "COMPLETE_FROZEN",
            "protocol": str(manifest_path.relative_to(ROOT)).replace("\\", "/"),
            "output_root": str(output_root.relative_to(ROOT)).replace("\\", "/"),
            "validation": validation,
            "extraction_counts": dict(sorted(extraction_counts.items())),
            "changed_rule_counts": dict(sorted(rule_counts.items())),
            "journal_sha256": journal_sha256,
            "journal_record_closure_sha256": journal_record_closure,
            "source_sha_closure": source_sha_closure,
            "baseline_results_read": False,
            "correct_answer_value_read": False,
            "evaluator_executed": False,
            "model_calls": 0,
            "raw_status_produced": False,
            "final_status_produced": False,
            "transition_produced": False,
        }
        write_json(output_root / "phase_a_summary.json", summary)
        write_json(
            output_root / "phase_a_freeze.json",
            {
                "journal_path": str(journal_path.relative_to(ROOT)).replace("\\", "/"),
                "journal_sha256": journal_sha256,
                "journal_record_closure_sha256": journal_record_closure,
                "source_sha_closure": source_sha_closure,
                "cells": expected_cells,
            },
        )
        (output_root / "phase_a_summary.md").write_text(
            "\n".join(
                [
                    "# Math16 Method 2 Phase A Summary",
                    "",
                    "- Status: **COMPLETE — FROZEN**",
                    f"- Cells / Eligibility checked: **{validation['cells']} / {validation['eligibility_checked']}**",
                    f"- Eligible / triggered: **{validation['eligible']} / {validation['rule_triggered']}**",
                    f"- Source changed / noneligible: **{validation['source_changed']} / {validation['noneligible']}**",
                    f"- Noneligible Raw == Final: **{validation['noneligible_raw_equals_final']} / {validation['noneligible']}**",
                    f"- Raw / Final files: **{validation['raw_source_files']} / {validation['final_source_files']}**",
                    f"- Journal SHA-256: `{journal_sha256}`",
                    f"- Journal record closure SHA-256: `{journal_record_closure}`",
                    f"- Source SHA closure: `{source_sha_closure}`",
                    "- Baseline results read: **No**",
                    "- Evaluator executed: **No**",
                    "- Model calls: **0**",
                    "- Raw/final status or transition produced: **No**",
                    "",
                ]
            ),
            encoding="utf-8",
            newline="\n",
        )
        return summary
    except Exception:
        if output_root.exists():
            shutil.rmtree(output_root)
        raise


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=MANIFEST_PATH)
    args = parser.parse_args()
    summary = execute_phase_a(args.manifest.resolve())
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
