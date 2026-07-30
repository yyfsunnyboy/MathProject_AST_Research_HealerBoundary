# -*- coding: utf-8 -*-
"""Qwen9B cell-wise deterministic fixpoint replay runner (v1).

Implements:
``docs/experiments/design/math16_qwen9b_cellwise_fixpoint_replay_protocol_v1.md``

Reuses frozen 4B stack application / SHA-history / termination judgment via
``math16_qwen4b_cellwise_fixpoint_replay_v1`` helpers without modifying that
module or any Healer rules.

Population is locked to Qwen9B C5c Final: 218 FAIL active / 102 PASS excluded.
Formal 218-cell replay is gated; default preflight is zero-execution and does
not invoke the observational evaluator.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping, Optional

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.aggressive_healer_tier_a import (  # noqa: E402
    RULE_ORDER as TIER_B_RULE_ORDER,
)
from agent_tools.finals_rebuild.aggressive_healer_tier_d.ranking import (  # noqa: E402
    MIN_MARGIN,
    MIN_SCORE,
)
from agent_tools.finals_rebuild.ce115_research_healer_runner import (  # noqa: E402
    RULE_ALLOWLIST,
)
from agent_tools.finals_rebuild.math16_observational_evaluator_v1 import (  # noqa: E402
    AUTHORITATIVE_BINDING,
    evaluator_binding_report,
    make_observational_evaluator_for_cell,
)
from agent_tools.finals_rebuild.math16_qwen4b_cellwise_fixpoint_replay_v1 import (  # noqa: E402
    AGGREGATE_SUMMARY_REQUIRED_FIELDS,
    CELL_FINAL_REQUIRED_FIELDS,
    CELL_JOURNAL_REQUIRED_FIELDS,
    FIXED_SEQUENCE,
    LAYER_ORDER,
    MAX_ROUND,
    Population,
    Round1Cell,
    TERMINATION_ENUM,
    apply_one_cycle,
    apply_one_cycle_with_stub_stack,
    apply_stack_once,
    assert_pass_cells_excluded,
    finalize_cycle_observation,
    judge_after_cycle,
    population_ids_overlap,
    read_round1_final_source,
    sha256_text,
)

PROTOCOL_MANIFEST = (
    ROOT
    / "docs/experiments/manifests/math16_qwen9b_cellwise_fixpoint_replay_protocol_v1.json"
)
ROUND1_SUMMARY = (
    ROOT / "docs/experiments/manifests/math16_three_model_round1_summary_v1.json"
)
C5C_CLOSURE = (
    ROOT
    / "docs/experiments/manifests/math16_c5c_final_source_closure_qwen9b_fail_gated_authoritative_v1.json"
)
RESULTS_ROOT = (
    ROOT / "docs/experiments/results/math16_qwen9b_cellwise_fixpoint_replay_v1"
)
CELL_JOURNAL_NAME = "cell_cycle_journal.jsonl"
CELL_FINAL_JOURNAL_NAME = "cell_final_journal.jsonl"
SUMMARY_NAME = "summary.json"
RUN_LOCK_NAME = "formal_run.lock"

PROTOCOL_ID = "math16_qwen9b_cellwise_fixpoint_replay_protocol_v1"
EXPECTED_TOTAL = 320
EXPECTED_PASS = 102
EXPECTED_FAIL = 218
MODEL_GROUP = "qwen9b"
# Hard reject any accidental 4B population constants.
FORBIDDEN_4B_PASS = 88
FORBIDDEN_4B_FAIL = 232

TIER_B_EXPECTED_ORDER = (
    "core.normalize_fullwidth_python_punctuation",
    "TIER_A_UNIQUE_MISSING_DELIMITER_REPAIR_V1",
    "TIER_A_EMPTY_SUITE_INSERT_PASS_V1",
    "TIER_A_UNIQUE_IMPORT_BINDING_REPAIR_V1",
)


class FixpointProtocolError(RuntimeError):
    """Raised when frozen 9B fixpoint protocol invariants are violated."""


class FormalExecutionBlocked(RuntimeError):
    """Raised when formal 218-cell replay is requested without authorization."""


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_round1_population(*, root: Path = ROOT) -> Population:
    """Load sealed Round 1 9B population from C5c; lock 218 FAIL / 102 PASS."""
    summary = load_json(root / ROUND1_SUMMARY.relative_to(ROOT))
    c5c = load_json(root / C5C_CLOSURE.relative_to(ROOT))
    q9 = summary["models"]["qwen9b"]
    if q9["final_pass"] != EXPECTED_PASS or q9["final_fail"] != EXPECTED_FAIL:
        raise FixpointProtocolError(
            f"Round1 summary mismatch: pass={q9['final_pass']} fail={q9['final_fail']}"
        )
    val = c5c["validation"]
    if val.get("c5c_pass") != EXPECTED_PASS or val.get("c5c_fail") != EXPECTED_FAIL:
        raise FixpointProtocolError(
            f"C5c closure mismatch: pass={val.get('c5c_pass')} fail={val.get('c5c_fail')}"
        )
    if val.get("n_cells") != EXPECTED_TOTAL:
        raise FixpointProtocolError(f"C5c n_cells={val.get('n_cells')} != 320")
    if c5c.get("namespace") != "qwen9b_fail_gated_authoritative_v1":
        raise FixpointProtocolError(f"unexpected C5c namespace: {c5c.get('namespace')}")

    active: list[Round1Cell] = []
    excluded: list[Round1Cell] = []
    for raw in c5c["cells"]:
        if raw.get("model_group") != MODEL_GROUP:
            raise FixpointProtocolError(f"non-9B cell in C5c: {raw.get('cell_id')}")
        outcome = raw["c5c_outcome"]
        if outcome not in {"PASSED", "FAILED"}:
            raise FixpointProtocolError(f"bad c5c_outcome: {outcome}")
        cell = Round1Cell(
            cell_id=raw["cell_id"],
            task_id=raw["task_id"],
            condition=raw["condition"],
            seed=int(raw["seed"]),
            model=raw["model"],
            model_group=raw["model_group"],
            round1_outcome="PASS" if outcome == "PASSED" else "FAIL",
            round1_final_source_path=raw["c5c_final_source_path"],
            round1_final_source_sha256=raw["c5c_final_source_sha256"],
            source_origin=raw.get("source_origin") or "C5C_FINAL",
        )
        if cell.round1_outcome == "PASS":
            excluded.append(cell)
        else:
            active.append(cell)

    if len(active) != EXPECTED_FAIL or len(excluded) != EXPECTED_PASS:
        raise FixpointProtocolError(
            f"population lock failed: active={len(active)} excluded={len(excluded)}"
        )
    if population_ids_overlap(active, excluded):
        raise FixpointProtocolError("PASS/FAIL id overlap")
    ids = [c.cell_id for c in active] + [c.cell_id for c in excluded]
    if len(ids) != len(set(ids)) or len(ids) != EXPECTED_TOTAL:
        raise FixpointProtocolError("cell_id uniqueness / total lock failed")
    # Explicitly forbid 4B override paths / counts leaking in.
    for cell in active + excluded:
        if "qwen4b" in cell.cell_id or cell.model_group != MODEL_GROUP:
            raise FixpointProtocolError(f"4B leakage in cell: {cell.cell_id}")
        if "d5_post" in cell.source_origin or "d2_post" in cell.source_origin:
            raise FixpointProtocolError(
                f"4B D5/D2 override origin forbidden for 9B: {cell.cell_id}"
            )
    return Population(active_fail=active, excluded_pass=excluded)


def check_freeze_invariants() -> dict[str, Any]:
    protocol = load_json(PROTOCOL_MANIFEST)
    errors: list[str] = []
    if protocol["execution_model"]["max_round"] != MAX_ROUND:
        errors.append("max_round mismatch")
    if protocol["fixed_sequence"] != FIXED_SEQUENCE:
        errors.append("fixed_sequence mismatch")
    if protocol["layer_order"] != list(LAYER_ORDER):
        errors.append("layer_order mismatch")
    if list(TIER_B_RULE_ORDER) != list(TIER_B_EXPECTED_ORDER):
        errors.append("tier_b rule order drift")
    if MIN_SCORE != 8 or MIN_MARGIN != 2:
        errors.append("d5 threshold drift")
    if not RULE_ALLOWLIST:
        errors.append("tier_a allowlist empty")
    if protocol["population"]["fixpoint_active_n"] != EXPECTED_FAIL:
        errors.append("protocol active_n drift")
    if protocol["population"]["permanently_excluded_pass_n"] != EXPECTED_PASS:
        errors.append("protocol excluded_n drift")
    if protocol["population"]["round1_final_pass_n"] == FORBIDDEN_4B_PASS:
        errors.append("4B pass count leaked into 9B protocol")
    if protocol["population"]["round1_final_fail_n"] == FORBIDDEN_4B_FAIL:
        errors.append("4B fail count leaked into 9B protocol")
    if protocol["positioning"]["model_group"] != MODEL_GROUP:
        errors.append("model_group must be qwen9b")
    obs = protocol.get("observational_evaluator") or {}
    if obs.get("binding_id") != AUTHORITATIVE_BINDING["binding_id"]:
        errors.append("observational evaluator binding not pinned")
    return {"ok": not errors, "errors": errors}


def check_resume_and_duplicate_guards(
    *, results_root: Path = RESULTS_ROOT, allow_resume: bool = False
) -> dict[str, Any]:
    journal = results_root / CELL_JOURNAL_NAME
    final_journal = results_root / CELL_FINAL_JOURNAL_NAME
    summary = results_root / SUMMARY_NAME
    lock = results_root / RUN_LOCK_NAME
    existing = [p.name for p in (journal, final_journal, summary, lock) if p.exists()]
    if existing and not allow_resume:
        return {
            "ok": False,
            "errors": [
                "formal outputs already present; refuse duplicate run without allow_resume",
                f"existing={existing}",
            ],
            "existing": existing,
        }
    if allow_resume and lock.exists():
        return {
            "ok": False,
            "errors": [
                "formal_run.lock present; incomplete prior run — manual triage required"
            ],
            "existing": existing,
        }
    return {"ok": True, "errors": [], "existing": existing}


def empty_aggregate_summary(*, formal_replay_executed: bool = False) -> dict[str, Any]:
    summary = {
        "protocol_id": PROTOCOL_ID,
        "model_group": MODEL_GROUP,
        "n_active_cells": EXPECTED_FAIL,
        "n_excluded_pass_cells": EXPECTED_PASS,
        "max_round": MAX_ROUND,
        "fixed_sequence": FIXED_SEQUENCE,
        "termination_counts": {k: 0 for k in TERMINATION_ENUM},
        "iterative_rescue_n": 0,
        "zero_change_n": 0,
        "cycle_detected_n": 0,
        "max_round_n": 0,
        "model_calls": 0,
        "formal_replay_executed": formal_replay_executed,
        "deterministic_second_cycle_probe": None,
        "observational_evaluator_binding_id": AUTHORITATIVE_BINDING["binding_id"],
    }
    missing = [k for k in AGGREGATE_SUMMARY_REQUIRED_FIELDS if k not in summary]
    if missing:
        raise FixpointProtocolError(f"summary missing: {missing}")
    return summary


def build_aggregate_summary(final_rows: list[Mapping[str, Any]]) -> dict[str, Any]:
    if len(final_rows) != EXPECTED_FAIL:
        raise FixpointProtocolError(
            f"final rows {len(final_rows)} != active {EXPECTED_FAIL}"
        )
    summary = empty_aggregate_summary(formal_replay_executed=True)
    counts = {k: 0 for k in TERMINATION_ENUM}
    for row in final_rows:
        reason = row.get("termination_reason")
        if reason not in counts:
            raise FixpointProtocolError(f"unknown termination: {reason}")
        counts[reason] += 1
    summary["termination_counts"] = counts
    summary["iterative_rescue_n"] = counts["ITERATIVE_RESCUE"]
    summary["zero_change_n"] = counts["ZERO_CHANGE_CONVERGENCE"]
    summary["cycle_detected_n"] = counts["CYCLE_DETECTED"]
    summary["max_round_n"] = counts["MAX_ROUND_NON_CONVERGENT"]
    return summary


def run_preflight(*, root: Path = ROOT, results_root: Path = RESULTS_ROOT) -> dict[str, Any]:
    """Zero-execution preflight: population, freeze, sources, evaluator pin.

    Does not apply healers, does not call the observational evaluator on cells,
    and does not create formal result artifacts.
    """
    errors: list[str] = []
    freeze = check_freeze_invariants()
    if not freeze["ok"]:
        errors.extend(freeze["errors"])

    binding = evaluator_binding_report()
    if not binding.get("ok"):
        errors.append("observational evaluator binding failed")

    try:
        population = load_round1_population(root=root)
    except Exception as exc:  # noqa: BLE001
        return {
            "ok": False,
            "errors": [f"population_load_failed: {exc}"],
            "formal_replay_executed": False,
            "healer_cycles_executed": 0,
            "model_calls": 0,
            "evaluator_invocations": 0,
        }

    missing = 0
    sha_mismatches = 0
    for cell in list(population.active_fail) + list(population.excluded_pass):
        path = root / cell.round1_final_source_path
        if not path.is_file():
            missing += 1
            continue
        digest = sha256_text(path.read_text(encoding="utf-8"))
        if digest != cell.round1_final_source_sha256:
            sha_mismatches += 1

    if missing or sha_mismatches:
        errors.append(f"sources missing={missing} sha_mismatches={sha_mismatches}")

    dup = check_resume_and_duplicate_guards(results_root=results_root)
    ids = [c.cell_id for c in population.active_fail] + [
        c.cell_id for c in population.excluded_pass
    ]
    duplicate_ids = len(ids) - len(set(ids))

    report = {
        "ok": not errors and duplicate_ids == 0,
        "errors": errors,
        "protocol_id": PROTOCOL_ID,
        "formal_replay_executed": False,
        "healer_cycles_executed": 0,
        "model_calls": 0,
        "evaluator_invocations": 0,
        "population": {
            "active_fail_n": len(population.active_fail),
            "excluded_pass_n": len(population.excluded_pass),
            "total_n": len(ids),
            "unique_ids": len(set(ids)),
            "duplicate_ids": duplicate_ids,
            "active_fail_locked": len(population.active_fail) == EXPECTED_FAIL,
            "excluded_pass_locked": len(population.excluded_pass) == EXPECTED_PASS,
            "no_4b_pass_fail_leak": (
                len(population.active_fail) != FORBIDDEN_4B_FAIL
                and len(population.excluded_pass) != FORBIDDEN_4B_PASS
            ),
        },
        "sources": {"missing": missing, "sha_mismatches": sha_mismatches},
        "max_round": MAX_ROUND,
        "fixed_sequence": FIXED_SEQUENCE,
        "freeze_checks": freeze,
        "duplicate_guards": dup,
        "observational_evaluator": binding,
        "results_root": str(results_root.relative_to(ROOT)).replace("\\", "/"),
        "results_root_exists": results_root.exists(),
    }
    return report


def run_formal_fixpoint_replay(
    *,
    allow_formal_execution: bool = False,
    evaluate_final_status: Optional[
        Callable[[str, Mapping[str, Any]], str]
    ] = None,
    root: Path = ROOT,
    results_root: Path = RESULTS_ROOT,
    allow_resume: bool = False,
    inject_authoritative_evaluator: bool = False,
) -> dict[str, Any]:
    """Gated formal 218-cell replay. Default refuses execution.

    When ``inject_authoritative_evaluator=True`` and no callback is supplied,
    the pinned Math16 observational evaluator factory is used. Callers that
    only want contract wiring should leave formal execution blocked.
    """
    if not allow_formal_execution:
        raise FormalExecutionBlocked(
            "formal 218-cell fixpoint replay blocked; "
            "(set allow_formal_execution=True only in an authorized execution round)"
        )

    if evaluate_final_status is None:
        if not inject_authoritative_evaluator:
            raise FormalExecutionBlocked(
                "formal replay requires an observational evaluate_final_status "
                "callback (or inject_authoritative_evaluator=True)"
            )

        def evaluate_final_status(source: str, meta: Mapping[str, Any]) -> str:
            return make_observational_evaluator_for_cell(meta)(source)

    freeze = check_freeze_invariants()
    if not freeze["ok"]:
        raise FixpointProtocolError(f"freeze checks failed: {freeze['errors']}")

    guards = check_resume_and_duplicate_guards(
        results_root=results_root, allow_resume=allow_resume
    )
    if not guards["ok"]:
        raise FixpointProtocolError(f"duplicate guards failed: {guards['errors']}")

    population = load_round1_population(root=root)
    results_root.mkdir(parents=True, exist_ok=True)
    lock = results_root / RUN_LOCK_NAME
    lock.write_text("running\n", encoding="utf-8")

    cycle_rows: list[dict[str, Any]] = []
    final_rows: list[dict[str, Any]] = []
    try:
        for cell in population.active_fail:
            source = read_round1_final_source(cell, root=root)
            history = [cell.round1_final_source_sha256]
            meta = cell.as_dict()
            current = source
            last_cycle = None
            for cycle_index in range(1, MAX_ROUND + 1):
                cycle = apply_stack_once(
                    cell=meta, source=current, cycle_index=cycle_index
                )
                obs = evaluate_final_status(cycle.round_end_source, meta)
                if obs not in {"PASS", "FAIL"}:
                    raise FixpointProtocolError(f"bad observational status: {obs}")
                finalized = finalize_cycle_observation(
                    cycle,
                    final_status=obs,
                    full_sha_history=history,
                    max_round=MAX_ROUND,
                )
                cycle_rows.append(finalized.journal_row())
                decision = finalized.decision
                history = list(decision["full_sha_history"])
                current = finalized.round_end_source
                last_cycle = finalized
                if not decision.get("continue"):
                    break
            assert last_cycle is not None
            final_rows.append(
                {
                    "cell_id": cell.cell_id,
                    "round1_final_sha": cell.round1_final_source_sha256,
                    "final_sha": last_cycle.round_end_sha,
                    "cycles_completed": last_cycle.cycle_index,
                    "termination_reason": last_cycle.decision["termination_reason"],
                    "rescue_cycle": last_cycle.decision.get("rescue_cycle"),
                    "rescue_rule_id": last_cycle.decision.get("rescue_rule_id"),
                    "full_sha_history": last_cycle.decision["full_sha_history"],
                    "cycle_detected": last_cycle.decision.get("cycle_detected", False),
                    "max_round_reached": last_cycle.decision.get(
                        "max_round_reached", False
                    ),
                    "regression": False,
                    "evaluator_result": last_cycle.final_status,
                }
            )
            for field in CELL_FINAL_REQUIRED_FIELDS:
                if field not in final_rows[-1]:
                    raise FixpointProtocolError(f"final journal missing {field}")

        assert_pass_cells_excluded(population, [r["cell_id"] for r in final_rows])
        summary = build_aggregate_summary(final_rows)

        cycle_path = results_root / CELL_JOURNAL_NAME
        with cycle_path.open("w", encoding="utf-8", newline="\n") as fh:
            for row in cycle_rows:
                missing = [k for k in CELL_JOURNAL_REQUIRED_FIELDS if k not in row]
                if missing:
                    raise FixpointProtocolError(f"cycle journal missing: {missing}")
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")
        final_path = results_root / CELL_FINAL_JOURNAL_NAME
        with final_path.open("w", encoding="utf-8", newline="\n") as fh:
            for row in final_rows:
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")
        (results_root / SUMMARY_NAME).write_text(
            json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    finally:
        if lock.exists():
            lock.unlink()

    return {
        "ok": True,
        "n_active_cells": len(final_rows),
        "summary": summary,
        "results_root": str(results_root),
    }


# Re-export helpers tests may need.
__all__ = [
    "AGGREGATE_SUMMARY_REQUIRED_FIELDS",
    "CELL_FINAL_REQUIRED_FIELDS",
    "CELL_JOURNAL_REQUIRED_FIELDS",
    "EXPECTED_FAIL",
    "EXPECTED_PASS",
    "EXPECTED_TOTAL",
    "FIXED_SEQUENCE",
    "FormalExecutionBlocked",
    "FixpointProtocolError",
    "MAX_ROUND",
    "MODEL_GROUP",
    "PROTOCOL_ID",
    "RESULTS_ROOT",
    "apply_one_cycle",
    "apply_one_cycle_with_stub_stack",
    "apply_stack_once",
    "assert_pass_cells_excluded",
    "build_aggregate_summary",
    "check_resume_and_duplicate_guards",
    "empty_aggregate_summary",
    "judge_after_cycle",
    "load_round1_population",
    "read_round1_final_source",
    "run_formal_fixpoint_replay",
    "run_preflight",
    "sha256_text",
]
