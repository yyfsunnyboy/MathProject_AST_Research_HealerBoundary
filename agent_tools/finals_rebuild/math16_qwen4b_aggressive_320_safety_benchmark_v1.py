# -*- coding: utf-8 -*-
"""Qwen4B Aggressive Healer full 320-cell safety benchmark runner (v1).

Implements:
``docs/experiments/design/math16_qwen4b_aggressive_320_safety_benchmark_protocol_v1.md``

Reuses the frozen Aggressive stack from the fixpoint module (``apply_stack_once``)
without modifying rules, order, guards, or thresholds.

Formal 320-cell execution is gated behind ``allow_formal_execution=True``.
Default preflight is zero-execution.
"""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
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
from agent_tools.finals_rebuild.math16_qwen4b_cellwise_fixpoint_replay_v1 import (  # noqa: E402
    EXPECTED_FAIL,
    EXPECTED_PASS,
    EXPECTED_TOTAL,
    FIXED_SEQUENCE,
    LAYER_ORDER,
    Round1Cell,
    apply_stack_once,
    load_round1_population,
    read_round1_final_source,
    sha256_text,
)

PROTOCOL_MANIFEST = (
    ROOT
    / "docs/experiments/manifests/math16_qwen4b_aggressive_320_safety_benchmark_protocol_v1.json"
)
RESULTS_ROOT = (
    ROOT / "docs/experiments/results/math16_qwen4b_aggressive_320_safety_benchmark_v1"
)
CELL_JOURNAL_NAME = "cell_journal.jsonl"
SUMMARY_NAME = "summary.json"
RUN_LOCK_NAME = "formal_run.lock"

PROTOCOL_ID = "math16_qwen4b_aggressive_320_safety_benchmark_protocol_v1"
MODEL_GROUP = "qwen4b"

TRANSITION_ENUM = (
    "preserved_pass",
    "regression",
    "verified_rescue",
    "unchanged_fail",
    "modified_still_failed",
)

CELL_JOURNAL_REQUIRED_FIELDS = (
    "cell_id",
    "input_status",
    "output_status",
    "transition",
    "start_sha",
    "end_sha",
    "source_changed",
    "modified",
    "per_rule_pre_sha",
    "per_rule_post_sha",
    "rule_id",
    "eligible",
    "modified_flags",
    "abstained",
    "rescue",
    "regression",
    "preserved_pass",
    "unchanged_fail",
    "modified_still_failed",
)

AGGREGATE_SUMMARY_REQUIRED_FIELDS = (
    "protocol_id",
    "model_group",
    "n_cells",
    "n_input_pass",
    "n_input_fail",
    "fixed_sequence",
    "transition_counts",
    "verified_rescue_n",
    "regression_n",
    "preserved_pass_n",
    "unchanged_fail_n",
    "modified_still_failed_n",
    "modified_n",
    "rescue_rate",
    "regression_rate",
    "preservation_rate",
    "modification_rate",
    "net_pass_change",
    "model_calls",
    "formal_benchmark_executed",
)

TIER_B_EXPECTED_ORDER = (
    "core.normalize_fullwidth_python_punctuation",
    "TIER_A_UNIQUE_MISSING_DELIMITER_REPAIR_V1",
    "TIER_A_EMPTY_SUITE_INSERT_PASS_V1",
    "TIER_A_UNIQUE_IMPORT_BINDING_REPAIR_V1",
)


class SafetyBenchmarkProtocolError(RuntimeError):
    """Raised when safety-benchmark protocol invariants are violated."""


class FormalExecutionBlocked(RuntimeError):
    """Raised when formal 320-cell benchmark is requested without authorization."""


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


@dataclass
class SafetyPopulation:
    """All 320 Round-1 cells are active (PASS 88 + FAIL 232)."""

    cells: list[Round1Cell]

    @property
    def pass_cells(self) -> list[Round1Cell]:
        return [c for c in self.cells if c.round1_outcome == "PASS"]

    @property
    def fail_cells(self) -> list[Round1Cell]:
        return [c for c in self.cells if c.round1_outcome == "FAIL"]

    @property
    def ids(self) -> set[str]:
        return {c.cell_id for c in self.cells}


@dataclass
class CellBenchmarkResult:
    cell_id: str
    input_status: str
    output_status: str
    transition: str
    start_sha: str
    end_sha: str
    source_changed: bool
    rule_trace: list[Any] = field(default_factory=list)

    def journal_row(self) -> dict[str, Any]:
        modified_flags = [bool(s.modified) for s in self.rule_trace]
        row = {
            "cell_id": self.cell_id,
            "input_status": self.input_status,
            "output_status": self.output_status,
            "transition": self.transition,
            "start_sha": self.start_sha,
            "end_sha": self.end_sha,
            "source_changed": self.source_changed,
            "modified": self.source_changed,
            "per_rule_pre_sha": [s.pre_sha for s in self.rule_trace],
            "per_rule_post_sha": [s.post_sha for s in self.rule_trace],
            "rule_id": [s.rule_id for s in self.rule_trace],
            "eligible": [bool(s.eligible) for s in self.rule_trace],
            "modified_flags": modified_flags,
            "abstained": [bool(s.abstained) for s in self.rule_trace],
            "rescue": self.transition == "verified_rescue",
            "regression": self.transition == "regression",
            "preserved_pass": self.transition == "preserved_pass",
            "unchanged_fail": self.transition == "unchanged_fail",
            "modified_still_failed": self.transition == "modified_still_failed",
        }
        missing = [k for k in CELL_JOURNAL_REQUIRED_FIELDS if k not in row]
        if missing:
            raise SafetyBenchmarkProtocolError(f"journal missing fields: {missing}")
        return row


def load_safety_population(*, root: Path = ROOT) -> SafetyPopulation:
    """Load Round 1 population; activate all 320 cells (including PASS)."""
    fixpoint_pop = load_round1_population(root=root)
    cells = list(fixpoint_pop.active_fail) + list(fixpoint_pop.excluded_pass)
    if len(cells) != EXPECTED_TOTAL:
        raise SafetyBenchmarkProtocolError(f"n_cells={len(cells)} != 320")
    n_pass = sum(1 for c in cells if c.round1_outcome == "PASS")
    n_fail = sum(1 for c in cells if c.round1_outcome == "FAIL")
    if n_pass != EXPECTED_PASS or n_fail != EXPECTED_FAIL:
        raise SafetyBenchmarkProtocolError(
            f"population lock failed: pass={n_pass} fail={n_fail}"
        )
    ids = [c.cell_id for c in cells]
    if len(ids) != len(set(ids)):
        raise SafetyBenchmarkProtocolError("duplicate cell_id in population")
    # Stable order: fail then pass is fine; sort by cell_id for determinism.
    cells_sorted = sorted(cells, key=lambda c: c.cell_id)
    return SafetyPopulation(cells=cells_sorted)


def assert_all_320_active(population: SafetyPopulation, scanned_ids: Iterable[str]) -> None:
    scanned = set(scanned_ids)
    if scanned != population.ids:
        missing = sorted(population.ids - scanned)[:5]
        extra = sorted(scanned - population.ids)[:5]
        raise SafetyBenchmarkProtocolError(
            f"scanned set must equal full 320; missing={missing} extra={extra}"
        )


def classify_transition(
    *, input_status: str, output_status: str, source_changed: bool
) -> str:
    """Map Round1→observed statuses to frozen transition labels."""
    if input_status not in {"PASS", "FAIL"} or output_status not in {"PASS", "FAIL"}:
        raise SafetyBenchmarkProtocolError(
            f"bad statuses: input={input_status!r} output={output_status!r}"
        )
    if input_status == "PASS" and output_status == "PASS":
        return "preserved_pass"
    if input_status == "PASS" and output_status == "FAIL":
        return "regression"
    if input_status == "FAIL" and output_status == "PASS":
        return "verified_rescue"
    # FAIL→FAIL
    return "modified_still_failed" if source_changed else "unchanged_fail"


def compute_rates(
    *,
    verified_rescue_n: int,
    regression_n: int,
    preserved_pass_n: int,
    modified_n: int,
) -> dict[str, float]:
    return {
        "rescue_rate": verified_rescue_n / EXPECTED_FAIL,
        "regression_rate": regression_n / EXPECTED_PASS,
        "preservation_rate": preserved_pass_n / EXPECTED_PASS,
        "modification_rate": modified_n / EXPECTED_TOTAL,
        "net_pass_change": float(verified_rescue_n - regression_n),
    }


def empty_aggregate_summary(*, formal_benchmark_executed: bool = False) -> dict[str, Any]:
    summary = {
        "protocol_id": PROTOCOL_ID,
        "model_group": MODEL_GROUP,
        "n_cells": EXPECTED_TOTAL,
        "n_input_pass": EXPECTED_PASS,
        "n_input_fail": EXPECTED_FAIL,
        "fixed_sequence": FIXED_SEQUENCE,
        "transition_counts": {k: 0 for k in TRANSITION_ENUM},
        "verified_rescue_n": 0,
        "regression_n": 0,
        "preserved_pass_n": 0,
        "unchanged_fail_n": 0,
        "modified_still_failed_n": 0,
        "modified_n": 0,
        "rescue_rate": 0.0,
        "regression_rate": 0.0,
        "preservation_rate": 0.0,
        "modification_rate": 0.0,
        "net_pass_change": 0.0,
        "model_calls": 0,
        "formal_benchmark_executed": formal_benchmark_executed,
    }
    missing = [k for k in AGGREGATE_SUMMARY_REQUIRED_FIELDS if k not in summary]
    if missing:
        raise SafetyBenchmarkProtocolError(f"summary missing: {missing}")
    return summary


def build_aggregate_summary(rows: list[Mapping[str, Any]]) -> dict[str, Any]:
    if len(rows) != EXPECTED_TOTAL:
        raise SafetyBenchmarkProtocolError(f"rows={len(rows)} != 320")
    summary = empty_aggregate_summary(formal_benchmark_executed=True)
    counts = {k: 0 for k in TRANSITION_ENUM}
    modified_n = 0
    for row in rows:
        transition = row.get("transition")
        if transition not in counts:
            raise SafetyBenchmarkProtocolError(f"unknown transition: {transition}")
        counts[transition] += 1
        if row.get("source_changed") or row.get("modified"):
            modified_n += 1
    summary["transition_counts"] = counts
    summary["verified_rescue_n"] = counts["verified_rescue"]
    summary["regression_n"] = counts["regression"]
    summary["preserved_pass_n"] = counts["preserved_pass"]
    summary["unchanged_fail_n"] = counts["unchanged_fail"]
    summary["modified_still_failed_n"] = counts["modified_still_failed"]
    summary["modified_n"] = modified_n
    rates = compute_rates(
        verified_rescue_n=counts["verified_rescue"],
        regression_n=counts["regression"],
        preserved_pass_n=counts["preserved_pass"],
        modified_n=modified_n,
    )
    summary.update(rates)
    return summary


def check_freeze_invariants() -> dict[str, Any]:
    protocol = load_json(PROTOCOL_MANIFEST)
    errors: list[str] = []
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
    pop = protocol["population"]
    if pop["total_cells"] != EXPECTED_TOTAL:
        errors.append("total_cells drift")
    if pop["input_pass_n"] != EXPECTED_PASS or pop["input_fail_n"] != EXPECTED_FAIL:
        errors.append("pass/fail lock drift")
    if pop["active_n"] != EXPECTED_TOTAL:
        errors.append("active_n must be 320")
    if protocol["execution_model"].get("iterative_fixpoint") is not False:
        errors.append("must not be iterative fixpoint")
    return {"ok": not errors, "errors": errors}


def check_duplicate_and_formal_guards(
    *, results_root: Path = RESULTS_ROOT, allow_resume: bool = False
) -> dict[str, Any]:
    journal = results_root / CELL_JOURNAL_NAME
    summary = results_root / SUMMARY_NAME
    lock = results_root / RUN_LOCK_NAME
    existing = [p.name for p in (journal, summary, lock) if p.exists()]
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


def run_one_cell_observational(
    *,
    cell: Round1Cell,
    source: str,
    evaluate: Callable[[str], str],
) -> CellBenchmarkResult:
    """Apply frozen stack once; classify using observational evaluator only."""
    cycle = apply_stack_once(
        cell=cell.as_dict(),
        source=source,
        cycle_index=1,
    )
    output_status = evaluate(cycle.round_end_source)
    if output_status not in {"PASS", "FAIL"}:
        raise SafetyBenchmarkProtocolError(f"evaluator returned {output_status!r}")
    transition = classify_transition(
        input_status=cell.round1_outcome,
        output_status=output_status,
        source_changed=cycle.source_changed,
    )
    return CellBenchmarkResult(
        cell_id=cell.cell_id,
        input_status=cell.round1_outcome,
        output_status=output_status,
        transition=transition,
        start_sha=cycle.round_start_sha,
        end_sha=cycle.round_end_sha,
        source_changed=cycle.source_changed,
        rule_trace=cycle.rule_trace,
    )


def run_one_cell_with_stub_stack(
    *,
    cell_id: str,
    input_status: str,
    source: str,
    output_status: str,
    mutate: Callable[[str], str],
) -> CellBenchmarkResult:
    """Synthetic stack stub for focused tests (no real healer)."""
    start = source
    end = mutate(source)
    start_sha = sha256_text(start)
    end_sha = sha256_text(end)
    source_changed = end_sha != start_sha
    transition = classify_transition(
        input_status=input_status,
        output_status=output_status,
        source_changed=source_changed,
    )

    class _Stub:
        def __init__(self) -> None:
            self.pre_sha = start_sha
            self.post_sha = end_sha
            self.rule_id = "STUB_RULE"
            self.eligible = True
            self.modified = source_changed
            self.abstained = not source_changed

    return CellBenchmarkResult(
        cell_id=cell_id,
        input_status=input_status,
        output_status=output_status,
        transition=transition,
        start_sha=start_sha,
        end_sha=end_sha,
        source_changed=source_changed,
        rule_trace=[_Stub()],
    )


def run_preflight(*, root: Path = ROOT, results_root: Path = RESULTS_ROOT) -> dict[str, Any]:
    """Zero-execution preflight: population, freeze, sources, guards."""
    errors: list[str] = []
    freeze = check_freeze_invariants()
    if not freeze["ok"]:
        errors.extend(freeze["errors"])

    try:
        population = load_safety_population(root=root)
    except Exception as exc:  # noqa: BLE001
        return {
            "ok": False,
            "errors": [f"population_load_failed: {exc}"],
            "formal_benchmark_executed": False,
            "healer_cells_executed": 0,
            "model_calls": 0,
        }

    missing = 0
    sha_mismatches = 0
    for cell in population.cells:
        path = root / cell.round1_final_source_path
        if not path.is_file():
            missing += 1
            continue
        digest = sha256_text(path.read_text(encoding="utf-8"))
        if digest != cell.round1_final_source_sha256:
            sha_mismatches += 1

    dup = check_duplicate_and_formal_guards(results_root=results_root)
    if not dup["ok"]:
        # Preflight may report existing outputs as warning-level for readiness,
        # but does not block zero-execution ok unless freeze/population broken.
        pass

    if missing or sha_mismatches:
        errors.append(f"sources missing={missing} sha_mismatches={sha_mismatches}")

    report = {
        "ok": not errors,
        "errors": errors,
        "protocol_id": PROTOCOL_ID,
        "formal_benchmark_executed": False,
        "healer_cells_executed": 0,
        "model_calls": 0,
        "population": {
            "n_cells": len(population.cells),
            "n_input_pass": len(population.pass_cells),
            "n_input_fail": len(population.fail_cells),
            "active_n": len(population.cells),
            "pass_locked": len(population.pass_cells) == EXPECTED_PASS,
            "fail_locked": len(population.fail_cells) == EXPECTED_FAIL,
            "total_locked": len(population.cells) == EXPECTED_TOTAL,
        },
        "sources": {"missing": missing, "sha_mismatches": sha_mismatches},
        "fixed_sequence": FIXED_SEQUENCE,
        "freeze_checks": freeze,
        "duplicate_guards": dup,
        "results_root": str(results_root.relative_to(ROOT)).replace("\\", "/"),
    }
    return report


def run_formal_safety_benchmark(
    *,
    allow_formal_execution: bool = False,
    evaluate: Optional[Callable[[str], str]] = None,
    root: Path = ROOT,
    results_root: Path = RESULTS_ROOT,
    allow_resume: bool = False,
) -> dict[str, Any]:
    """Gated formal 320-cell run. Default refuses execution."""
    if not allow_formal_execution:
        raise FormalExecutionBlocked(
            "formal 320-cell safety benchmark blocked; "
            "pass allow_formal_execution=True only for authorized runs"
        )
    if evaluate is None:
        raise FormalExecutionBlocked(
            "formal run requires an observational evaluator callback "
            "(must not accept/rollback source)"
        )

    freeze = check_freeze_invariants()
    if not freeze["ok"]:
        raise SafetyBenchmarkProtocolError(f"freeze checks failed: {freeze['errors']}")

    guards = check_duplicate_and_formal_guards(
        results_root=results_root, allow_resume=allow_resume
    )
    if not guards["ok"]:
        raise SafetyBenchmarkProtocolError(f"duplicate guards failed: {guards['errors']}")

    population = load_safety_population(root=root)
    results_root.mkdir(parents=True, exist_ok=True)
    lock = results_root / RUN_LOCK_NAME
    lock.write_text("running\n", encoding="utf-8")

    rows: list[dict[str, Any]] = []
    try:
        for cell in population.cells:
            source = read_round1_final_source(cell, root=root)
            result = run_one_cell_observational(
                cell=cell, source=source, evaluate=evaluate
            )
            rows.append(result.journal_row())
        assert_all_320_active(population, [r["cell_id"] for r in rows])
        summary = build_aggregate_summary(rows)
        journal_path = results_root / CELL_JOURNAL_NAME
        with journal_path.open("w", encoding="utf-8", newline="\n") as fh:
            for row in rows:
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")
        summary_path = results_root / SUMMARY_NAME
        summary_path.write_text(
            json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    finally:
        if lock.exists():
            lock.unlink()

    return {
        "ok": True,
        "n_cells": len(rows),
        "summary": summary,
        "results_root": str(results_root),
    }
