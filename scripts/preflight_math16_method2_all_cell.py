"""Zero-model preflight and journal contract for Math16 Method 2.

This module never calls a model, applies a transformation, or invokes an
evaluator.  It verifies the frozen all-cell eligibility-first data flow only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Mapping


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.ce115_research_healer_runner import (  # noqa: E402
    RULE_ALLOWLIST,
    RULE_REGISTRY,
)
from agent_tools.finals_rebuild.extraction import extract_code  # noqa: E402
from agent_tools.finals_rebuild.math16_pool import frozen_for_prompt, tasks_by_id  # noqa: E402


MANIFEST_PATH = (
    ROOT / "docs/experiments/manifests/math16_method2_all_cell_protocol_v1.json"
)
FORBIDDEN_DECISION_FIELDS = frozenset(
    {
        "final_status",
        "baseline_final_status",
        "raw_status",
        "correct_answer",
        "classifier_outcome",
        "evaluator_result",
        "evaluation_gates",
    }
)
TRANSITIONS = {
    ("FAILED", "PASSED"): "verified_rescue",
    ("PASSED", "FAILED"): "regression",
    ("PASSED", "PASSED"): "preserved_pass",
    ("FAILED", "FAILED"): "still_failed",
}
JOURNAL_FIELDS = (
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


def sha256_bytes(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def classify_transition(raw_status: str, final_status: str) -> str:
    """Map the two independently produced statuses to the frozen transition."""
    try:
        return TRANSITIONS[(raw_status, final_status)]
    except KeyError as exc:
        raise ValueError(
            f"statuses must each be PASSED or FAILED: {raw_status!r}, {final_status!r}"
        ) from exc


def decide_eligibility(
    raw_source: str | None, context: Mapping[str, Any]
) -> dict[str, Any]:
    """Probe the existing frozen allowlist without status/evaluator inputs."""
    if not raw_source:
        return {
            "eligibility_checked": True,
            "eligible": False,
            "rule_id": None,
            "rule_triggered": False,
        }

    hits: list[str] = []
    for rule_id in RULE_ALLOWLIST:
        rule = RULE_REGISTRY[rule_id]
        applicable, _, _ = rule.is_applicable(raw_source, context)
        if applicable:
            triggered, _ = rule.is_triggered(raw_source, context)
            if triggered:
                hits.append(rule_id)
    return {
        "eligibility_checked": True,
        "eligible": bool(hits),
        "rule_id": hits[0] if hits else None,
        "rule_triggered": bool(hits),
    }


def make_pre_evaluation_record(
    *,
    cell_identity: Mapping[str, Any],
    raw_source: str,
    eligibility: Mapping[str, Any],
    healed_source: str | None = None,
) -> dict[str, Any]:
    """Build a journal row before the separately authorized scoring phase."""
    eligible = bool(eligibility["eligible"])
    if eligible and healed_source is None:
        raise ValueError("eligible cell requires a Healer output in formal replay")
    final_source = healed_source if eligible else raw_source
    assert final_source is not None
    record = {
        "cell_identity": dict(cell_identity),
        "raw_source_sha256": sha256_text(raw_source),
        "eligibility_checked": bool(eligibility["eligibility_checked"]),
        "eligible": eligible,
        "rule_id": eligibility.get("rule_id"),
        "rule_triggered": bool(eligibility["rule_triggered"]),
        "source_changed": final_source != raw_source,
        "final_source_sha256": sha256_text(final_source),
        "raw_status": None,
        "final_status": None,
        "transition": None,
    }
    if tuple(record) != JOURNAL_FIELDS:
        raise AssertionError("journal field order/coverage drift")
    if not eligible and record["final_source_sha256"] != record["raw_source_sha256"]:
        raise AssertionError("noneligible final source must equal raw source")
    return record


def finalize_statuses(
    record: Mapping[str, Any], *, raw_status: str, final_status: str
) -> dict[str, Any]:
    """Attach only post-decision evaluator outputs and derive the transition."""
    finalized = dict(record)
    finalized["raw_status"] = raw_status
    finalized["final_status"] = final_status
    finalized["transition"] = classify_transition(raw_status, final_status)
    return finalized


def load_manifest(path: Path = MANIFEST_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def verify_pins(manifest: Mapping[str, Any]) -> None:
    for relative, expected in manifest["frozen_sha256"].items():
        actual = sha256_bytes(ROOT / relative)
        if actual != expected:
            raise RuntimeError(f"SHA256_DRIFT: {relative}: {actual}")
    if tuple(manifest["healer"]["rule_allowlist"]) != tuple(RULE_ALLOWLIST):
        raise RuntimeError("RULE_ALLOWLIST_DRIFT")


def run_preflight(manifest_path: Path = MANIFEST_PATH) -> dict[str, Any]:
    manifest = load_manifest(manifest_path)
    verify_pins(manifest)
    plan_path = ROOT / manifest["inputs"]["cell_plan"]
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    if len(plan) != manifest["population"]["expected_cells"]:
        raise RuntimeError(f"CELL_COUNT_MISMATCH: {len(plan)}")
    cell_ids = [cell["cell_id"] for cell in plan]
    if len(set(cell_ids)) != len(cell_ids):
        raise RuntimeError("DUPLICATE_CELL_ID")

    tasks = tasks_by_id()
    checked = 0
    noneligible_identity_checks = 0
    for cell in plan:
        raw_path = (
            ROOT
            / "docs/experiments/results"
            / cell["output_relative_path"]
            / "raw_response.txt"
        )
        extraction = extract_code(raw_path.read_text(encoding="utf-8"))
        raw_source = (
            extraction.extracted_code
            if extraction.extraction_status == "extracted"
            else None
        )
        frozen = frozen_for_prompt(tasks[cell["task_id"]])["oracle_payload"]
        decision_context = {"frozen": frozen}
        if FORBIDDEN_DECISION_FIELDS.intersection(decision_context):
            raise AssertionError("forbidden decision field reached Eligibility")
        eligibility = decide_eligibility(raw_source, decision_context)
        checked += int(eligibility["eligibility_checked"])

        if not eligibility["eligible"]:
            source_for_identity = raw_source if raw_source is not None else ""
            record = make_pre_evaluation_record(
                cell_identity={
                    "cell_id": cell["cell_id"],
                    "task_id": cell["task_id"],
                    "condition": cell["condition"],
                    "seed": cell["seed"],
                },
                raw_source=source_for_identity,
                eligibility=eligibility,
            )
            if record["raw_source_sha256"] != record["final_source_sha256"]:
                raise AssertionError("noneligible source identity failure")
            noneligible_identity_checks += 1

    if checked != manifest["population"]["expected_cells"]:
        raise RuntimeError(f"ELIGIBILITY_COVERAGE_MISMATCH: {checked}")

    raw_dir = manifest["outputs"]["raw_source_directory"]
    final_dir = manifest["outputs"]["final_source_directory"]
    if raw_dir == final_dir:
        raise RuntimeError("RAW_FINAL_STORAGE_COLLISION")
    if set(manifest["journal"]["required_fields"]) != set(JOURNAL_FIELDS):
        raise RuntimeError("JOURNAL_FIELDS_DRIFT")
    if set(manifest["journal"]["transition_enum"]) != set(TRANSITIONS.values()):
        raise RuntimeError("TRANSITION_ENUM_DRIFT")

    return {
        "expected_cells": manifest["population"]["expected_cells"],
        "eligibility_checked": checked,
        "noneligible_final_equals_raw_checks": noneligible_identity_checks,
        "raw_final_paths_distinct": True,
        "transition_contract_count": len(TRANSITIONS),
        "formal_replay_executed": False,
        "evaluator_executed": False,
        "model_calls": 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=MANIFEST_PATH)
    args = parser.parse_args()
    print(json.dumps(run_preflight(args.manifest), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
