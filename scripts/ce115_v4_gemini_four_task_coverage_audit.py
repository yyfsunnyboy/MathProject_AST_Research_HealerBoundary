"""Phase A zero-model four-task coverage audit for CE115 v4 Gemini positive controls."""
from __future__ import annotations

import json
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORMAL = ROOT / "docs/experiments/results/ce115_ab2d_assembly_v4_formal_run"
POLY02 = ROOT / "docs/experiments/results/ce115_ab2d_assembly_v4_gemini35flash_positive_control_02"
RF = (
    ROOT
    / "docs/experiments/results/ce115_ab2d_assembly_v4_gemini35flash_positive_controls_radical_fraction_01"
)
OUT = (
    ROOT
    / "docs/experiments/results/ce115_ab2d_assembly_v4_gemini35flash_four_task_coverage_audit_01"
)
MISSING_DIR = (
    ROOT
    / "docs/experiments/results/ce115_ab2d_assembly_v4_gemini35flash_missing_task_positive_control_01"
)
EXPECTED_HEAD = "1f365b275937b8836c9bad362229b661bf2dbac2"


def main() -> int:
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, timeout=30
    )
    origin = subprocess.run(
        ["git", "rev-parse", "origin/main"], cwd=ROOT, capture_output=True, text=True, timeout=30
    )
    git_head = (head.stdout or "").strip()
    git_origin = (origin.stdout or "").strip()
    if git_head != EXPECTED_HEAD or git_head != git_origin:
        raise SystemExit(f"HEAD mismatch: head={git_head} origin={git_origin} expected={EXPECTED_HEAD}")
    if OUT.exists():
        raise SystemExit(f"audit directory already exists: {OUT}")
    if MISSING_DIR.exists():
        raise SystemExit(f"missing-task directory already exists: {MISSING_DIR}")

    plan = json.loads((FORMAL / "frozen_formal_run_plan.json").read_text(encoding="utf8"))
    by_task: dict[str, dict] = defaultdict(
        lambda: {"seqs": [], "seeds": [], "models": [], "families": set(), "cells": []}
    )
    for c in plan["cells"]:
        t = c["task"]
        by_task[t]["seqs"].append(c["sequence"])
        by_task[t]["seeds"].append(c["seed"])
        by_task[t]["models"].append(c["model"])
        by_task[t]["families"].add(c["task_family"])
        by_task[t]["cells"].append(
            {
                "sequence": c["sequence"],
                "cell_id": c["cell_id"],
                "model": c["model"],
                "seed": c["seed"],
                "task_family": c["task_family"],
            }
        )

    inventory = []
    for t in sorted(by_task):
        info = by_task[t]
        fam = sorted(info["families"])
        inventory.append(
            {
                "task_id": t,
                "family": fam[0] if len(fam) == 1 else fam,
                "difficulty": "L1" if t.endswith("_l1") else "UNKNOWN",
                "formal_seq_numbers": sorted(info["seqs"]),
                "three_seeds": sorted(set(info["seeds"])),
                "models": sorted(set(info["models"])),
                "n_formal_cells": len(info["cells"]),
            }
        )

    gemini_coverage = []
    p2 = json.loads((POLY02 / "positive_control_summary.json").read_text(encoding="utf8"))
    p2_art = json.loads((POLY02 / "cell_artifact.json").read_text(encoding="utf8"))
    gemini_coverage.append(
        {
            "control_dir": "docs/experiments/results/ce115_ab2d_assembly_v4_gemini35flash_positive_control_02",
            "source_sequence": p2_art.get("source_sequence"),
            "task_id": p2_art["task_id"],
            "family": p2_art["task_family"],
            "seed": p2_art["seed"],
            "verdict": p2.get("verdict"),
            "completion": p2.get("completion") or p2_art.get("completion"),
            "adoption": p2.get("toolbox_adoption") or p2_art.get("adoption_verdict"),
            "evaluator": p2.get("evaluator") or p2_art.get("evaluator_verdict"),
        }
    )
    rf = json.loads((RF / "positive_controls_summary.json").read_text(encoding="utf8"))
    for key in ("radical", "fraction"):
        cell = rf["cells"][key]
        art = json.loads((RF / f"{key}.cell_artifact.json").read_text(encoding="utf8"))
        gemini_coverage.append(
            {
                "control_dir": (
                    "docs/experiments/results/"
                    "ce115_ab2d_assembly_v4_gemini35flash_positive_controls_radical_fraction_01"
                ),
                "key": key,
                "source_sequence": cell["source_sequence"],
                "task_id": art["task_id"],
                "family": art["task_family"],
                "seed": art["seed"],
                "verdict_cell_pass": cell.get("pass"),
                "completion": cell["completion"],
                "adoption": cell["toolbox_adoption"],
                "evaluator": cell["evaluator"],
            }
        )

    covered = sorted({g["task_id"] for g in gemini_coverage})
    formal_tasks = sorted(by_task)
    missing = [t for t in formal_tasks if t not in covered]
    excluded_tasks = sorted({e["task"] for e in plan.get("exclusions", [])})
    union = sorted(set(formal_tasks) | set(excluded_tasks))

    edge_outcomes: dict[str, list] = {}
    for t in formal_tasks:
        edge_outcomes[t] = []
        for c in by_task[t]["cells"]:
            art = json.loads((FORMAL / f"{c['cell_id']}.artifact.json").read_text(encoding="utf8"))
            edge_outcomes[t].append(
                {
                    "sequence": c["sequence"],
                    "cell_id": c["cell_id"],
                    "model": c["model"],
                    "seed": c["seed"],
                    "completion": art.get("completion"),
                    "adoption": art.get("adoption_verdict"),
                    "evaluator": art.get("evaluator_verdict"),
                }
            )

    gate_ok = len(formal_tasks) == 4 and len(missing) == 1
    audit = {
        "audit_id": "ce115_ab2d_assembly_v4_gemini35flash_four_task_coverage_audit_01",
        "phase": "A_ZERO_MODEL_COVERAGE_AUDIT",
        "starting_head": git_head,
        "origin_main": git_origin,
        "head_equals_origin_main": git_head == git_origin,
        "formal_run": "docs/experiments/results/ce115_ab2d_assembly_v4_formal_run",
        "formal_planned_cells": plan["planned_cells"],
        "formal_executed_cells": len(plan["cells"]),
        "distinct_task_count_in_executed_cohort": len(formal_tasks),
        "distinct_task_ids_executed": formal_tasks,
        "task_inventory": inventory,
        "excluded_from_executed_cohort": plan.get("exclusions", []),
        "excluded_distinct_task_ids": excluded_tasks,
        "union_executed_plus_excluded_task_ids": union,
        "union_distinct_task_count": len(union),
        "gemini_positive_controls_completed": gemini_coverage,
        "gemini_covered_task_ids": covered,
        "missing_task_ids_relative_to_executed_cohort": missing,
        "missing_task_count_relative_to_executed_cohort": len(missing),
        "edge_outcomes_by_task": edge_outcomes,
        "gate": {
            "require_exactly_4_distinct_executed_tasks": True,
            "observed_executed_distinct_tasks": len(formal_tasks),
            "require_exactly_1_missing_task": True,
            "observed_missing_relative_to_executed": len(missing),
            "union_is_4_including_structural_exclusion": len(union) == 4,
            "passed": gate_ok,
            "blocker": None
            if gate_ok
            else "PLAN_INCONSISTENCY_NOT_EXACTLY_FOUR_EXECUTED_DISTINCT_TASKS",
            "detail": (
                "Formal executed cohort has 3 distinct task_ids. "
                "ce115_calc_polynomial_factor_roots_l1 appears only in exclusions "
                "(STRUCTURAL_EXCLUSION_ASSEMBLY_COVERAGE_UNAVAILABLE) and has no formal "
                "executed cell artifacts. Gemini already covers all 3 executed tasks; "
                "missing relative to executed cohort = 0. Protocol requires exactly 4 "
                "distinct executed tasks and exactly 1 missing task before Phase B."
            ),
        },
        "phase_b": {
            "executed": False,
            "network_calls": 0,
            "missing_task_positive_control_dir_created": False,
            "reason": "phase_a_gate_failed",
        },
    }

    OUT.mkdir(parents=True)
    (OUT / "coverage_audit.json").write_text(json.dumps(audit, indent=2) + "\n", encoding="utf8")
    (OUT / "AUDIT_VERDICT.txt").write_text(
        (audit["gate"]["blocker"] or "PASSED")
        + "\n"
        + f"executed_distinct_tasks={len(formal_tasks)}\n"
        + f"missing_relative_to_executed={len(missing)}\n"
        + f"union_including_exclusion={len(union)}\n"
        + "phase_b_network_calls=0\n",
        encoding="utf8",
    )
    print(json.dumps(audit["gate"] | {"network_calls": 0, "audit_dir": str(OUT)}, indent=2))
    return 0 if gate_ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
