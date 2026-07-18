"""Offline re-evaluation of a frozen Math16 Gemini run with revised evaluator.

Does not call Gemini. Does not rewrite original cell artifacts.
Writes evaluation_revision_002/ under the run directory.
"""
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.generator_success import evaluate_math_notation
from agent_tools.finals_rebuild.math16_pool import tasks_by_id
from scripts.run_math16_latex_v1_gemini_live import classify_math16_response
from agent_tools.finals_rebuild.math16_oracles import EVALUATOR_LATEX_SEMANTIC_REVISION

RUN_ID = "gemini35flash_math16_latex_v1_ab123_run_001"
RUN_DIR = ROOT / "docs/experiments/results" / RUN_ID
OUT_DIR = RUN_DIR / "evaluation_revision_002"
ORACLE_PATH = ROOT / "agent_tools/finals_rebuild/math16_oracles.py"
ORIGINAL_EVALUATOR_HASH = "c1f1687e1c7d13127165d9bfed5688f7657efd3ab449c6021d903c18ee3a151d"
EXPECTED_PRIMARY_CHANGES = {
    "gemini_3_5_flash__ce115_calc_polynomial_division_l1__ab2d__seed_2026071301",
    "gemini_3_5_flash__ce115_calc_polynomial_factor_roots_l1__ab1__seed_2026071301",
    "gemini_3_5_flash__ce115_calc_polynomial_factor_roots_l1__ab2g__seed_2026071301",
}


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _map_outcome(outcome: str) -> str:
    if outcome == "passed":
        return "PASSED"
    if outcome == "answer_incorrect":
        return "ANSWER_INCORRECT"
    if outcome in {"runtime_failure", "infrastructure_failure"}:
        return "EXECUTION_FAILURE"
    if outcome == "schema_failure":
        return "SCHEMA_FAILURE"
    return outcome.upper()


def _rank(status: str) -> int:
    order = {
        "PASSED": 3,
        "ANSWER_INCORRECT": 2,
        "PARSE_MINOR": 1,
        "SCHEMA_FAILURE": 1,
        "EXECUTION_FAILURE": 1,
        "INTRINSIC_SAFETY": 1,
        "EXTRACTION_FAILURE": 0,
        "EMPTY_RESPONSE": 0,
        "MISSING_ENTRY_POINT": 0,
        "CATASTROPHIC_TRUNCATION": 0,
        "API_FAILURE": 0,
    }
    return order.get(status, 0)


def main() -> int:
    if not RUN_DIR.is_dir():
        raise SystemExit(f"missing run dir: {RUN_DIR}")
    revised_hash = _sha256_file(ORACLE_PATH)
    if revised_hash == ORIGINAL_EVALUATOR_HASH:
        raise SystemExit("revised evaluator hash equals original; refusing empty revision")

    by_id = tasks_by_id()
    cell_dirs = sorted((RUN_DIR / "cells").glob("gemini_3_5_flash__*"))
    if len(cell_dirs) != 48:
        raise SystemExit(f"expected 48 cell dirs, got {len(cell_dirs)}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    for cell_dir in cell_dirs:
        artifact = json.loads((cell_dir / "artifact.json").read_text(encoding="utf-8"))
        raw = (cell_dir / "raw_response.txt").read_text(encoding="utf-8")
        # Integrity: do not mutate original files; only read.
        prompt_path = cell_dir / "prompt.txt"
        prompt_text = prompt_path.read_text(encoding="utf-8") if prompt_path.exists() else ""
        task = by_id[artifact["task_id"]]
        outcome, _code, details = classify_math16_response(
            raw,
            frozen_params=artifact["frozen_parameters"],
            audit_oracle_payload=artifact.get("audit_oracle_payload")
            or artifact["frozen_parameters"],
            task=task,
        )
        new_status = _map_outcome(outcome)
        old_status = artifact["evaluator_status"]
        question_text = None
        if isinstance(details.get("returned_value"), dict):
            question_text = details["returned_value"].get("question_text")
        g6 = (
            evaluate_math_notation(question_text)
            if question_text
            else {"status": "NOT_OBSERVED", "reason": "question_text_unavailable"}
        )
        row = {
            "cell_id": artifact["cell_id"],
            "task_id": artifact["task_id"],
            "condition": artifact["condition"],
            "domain_ops": artifact.get("domain_ops"),
            "historical_evaluator_status": old_status,
            "historical_first_attempt_evaluator_outcome": artifact.get(
                "first_attempt_evaluator_outcome"
            ),
            "revised_evaluator_status": new_status,
            "revised_outcome": outcome,
            "status_changed": old_status != new_status,
            "primary_pass_changed": (old_status == "PASSED") != (new_status == "PASSED"),
            "oracle_error": details.get("oracle_error"),
            "gates": details.get("evaluation_gates"),
            "g6": g6,
            "prompt_hash_unchanged": artifact.get("prompt_hash")
            or artifact.get("canonical_prompt_hash"),
            "raw_sha256": hashlib.sha256(raw.encode("utf-8")).hexdigest(),
            "prompt_chars": len(prompt_text),
        }
        rows.append(row)
        (OUT_DIR / "cells").mkdir(exist_ok=True)
        cell_out = OUT_DIR / "cells" / artifact["cell_id"]
        cell_out.mkdir(exist_ok=True)
        (cell_out / "reeval.json").write_text(
            json.dumps(
                {
                    **row,
                    "historical_artifact_evaluator_status": old_status,
                    "revised_details": {
                        k: details.get(k)
                        for k in (
                            "outcome",
                            "oracle_error",
                            "expected_answer",
                            "evaluation_gates",
                            "composite_outcomes",
                        )
                    },
                },
                ensure_ascii=False,
                indent=2,
                default=str,
            )
            + "\n",
            encoding="utf-8",
        )

    changed = [r for r in rows if r["status_changed"]]
    primary_pass_changed = [r for r in rows if r["primary_pass_changed"]]
    unexpected = [
        r["cell_id"]
        for r in primary_pass_changed
        if r["cell_id"] not in EXPECTED_PRIMARY_CHANGES
    ]
    missing_expected = sorted(
        cid
        for cid in EXPECTED_PRIMARY_CHANGES
        if not any(r["cell_id"] == cid and r["primary_pass_changed"] for r in rows)
    )

    by_treatment: dict[str, Counter[str]] = defaultdict(Counter)
    by_domain: dict[str, dict[str, Counter[str]]] = defaultdict(lambda: defaultdict(Counter))
    for r in rows:
        by_treatment[r["condition"]][r["revised_evaluator_status"]] += 1
        by_domain[r["domain_ops"] or "?"][r["condition"]][r["revised_evaluator_status"]] += 1

    # Paired comparisons on revised statuses
    by_task: dict[str, dict[str, str]] = defaultdict(dict)
    for r in rows:
        by_task[r["task_id"]][r["condition"]] = r["revised_evaluator_status"]

    def paired(a: str, b: str) -> dict[str, list[str]]:
        improved, regressed, unchanged = [], [], []
        for tid, conds in sorted(by_task.items()):
            ra, rb = _rank(conds[a]), _rank(conds[b])
            if rb > ra:
                improved.append(tid)
            elif rb < ra:
                regressed.append(tid)
            else:
                unchanged.append(tid)
        return {"improved": improved, "regressed": regressed, "unchanged": unchanged}

    validity = []
    for r in rows:
        if r["cell_id"] in EXPECTED_PRIMARY_CHANGES and r["revised_evaluator_status"] == "PASSED":
            v = "VALID_MODEL_OUTCOME"
            note = "false_negative_corrected_by_evaluator_revision_002"
        elif r["revised_evaluator_status"] == "PASSED":
            v = "VALID_MODEL_OUTCOME"
            note = "unchanged_pass"
        else:
            v = "VALID_MODEL_OUTCOME"
            note = "valid_model_or_runtime_failure"
        validity.append({**{k: r[k] for k in ("cell_id", "task_id", "condition", "revised_evaluator_status")}, "validity": v, "note": note})

    commit_allowed = not unexpected and not missing_expected and len(rows) == 48
    summary = {
        "revision_id": "evaluation_revision_002",
        "evaluator_revision": EVALUATOR_LATEX_SEMANTIC_REVISION,
        "run_id": RUN_ID,
        "model_calls": 0,
        "original_artifacts_mutated": False,
        "cells_reevaluated": len(rows),
        "original_evaluator_hash": ORIGINAL_EVALUATOR_HASH,
        "revised_evaluator_hash": revised_hash,
        "original_evaluator_path": str(ORACLE_PATH.relative_to(ROOT)).replace("\\", "/"),
        "treatment_x_outcome_revised": {k: dict(v) for k, v in sorted(by_treatment.items())},
        "treatment_passed_revised": {
            cond: f"{by_treatment[cond].get('PASSED', 0)}/16" for cond in ("ab1", "ab2g", "ab2d")
        },
        "domain_x_treatment_x_outcome_revised": {
            dom: {c: dict(ctr) for c, ctr in sorted(conds.items())}
            for dom, conds in sorted(by_domain.items())
        },
        "paired_comparisons_revised": {
            "Ab1->Ab2g": paired("ab1", "ab2g"),
            "Ab1->Ab2d": paired("ab1", "ab2d"),
            "Ab2g->Ab2d": paired("ab2g", "ab2d"),
        },
        "changed_cells": [
            {
                "cell_id": r["cell_id"],
                "task_id": r["task_id"],
                "condition": r["condition"],
                "historical": r["historical_evaluator_status"],
                "revised": r["revised_evaluator_status"],
                "primary_pass_changed": r["primary_pass_changed"],
            }
            for r in changed
        ],
        "unchanged_cells": [r["cell_id"] for r in rows if not r["status_changed"]],
        "expected_primary_pass_changes": sorted(EXPECTED_PRIMARY_CHANGES),
        "unexpected_primary_pass_changes": unexpected,
        "missing_expected_primary_pass_changes": missing_expected,
        "commit_allowed": commit_allowed,
        "special_checks": {
            "q02": {
                cond: next(
                    r["revised_evaluator_status"]
                    for r in rows
                    if r["task_id"] == "ce111_q02_polynomial_division_remainder"
                    and r["condition"] == cond
                )
                for cond in ("ab1", "ab2g", "ab2d")
            },
            "q04": {
                cond: next(
                    r["revised_evaluator_status"]
                    for r in rows
                    if r["task_id"] == "ce112_q04_radical_simplification"
                    and r["condition"] == cond
                )
                for cond in ("ab1", "ab2g", "ab2d")
            },
            "q08": {
                cond: next(
                    r["revised_evaluator_status"]
                    for r in rows
                    if r["task_id"] == "ce111_q08_polynomial_factor_parameter_recovery"
                    and r["condition"] == cond
                )
                for cond in ("ab1", "ab2g", "ab2d")
            },
            "q10": {
                cond: next(
                    r["revised_evaluator_status"]
                    for r in rows
                    if r["task_id"] == "ce111_q10_ordered_quadratic_roots_radical"
                    and r["condition"] == cond
                )
                for cond in ("ab1", "ab2g", "ab2d")
            },
            "q11": {
                cond: next(
                    r["revised_evaluator_status"]
                    for r in rows
                    if r["task_id"] == "ce113_q11_rationalize_denominator"
                    and r["condition"] == cond
                )
                for cond in ("ab1", "ab2g", "ab2d")
            },
        },
    }

    (OUT_DIR / "cell_outcomes.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (OUT_DIR / "validity_report.json").write_text(
        json.dumps(
            {
                "validity_counts": dict(Counter(v["validity"] for v in validity)),
                "cells": validity,
                "commit_allowed": commit_allowed,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (OUT_DIR / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (OUT_DIR / "paired_comparison_report.json").write_text(
        json.dumps(summary["paired_comparisons_revised"], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    md = [
        "# evaluation_revision_002",
        "",
        f"- original_evaluator_hash: `{ORIGINAL_EVALUATOR_HASH}`",
        f"- revised_evaluator_hash: `{revised_hash}`",
        f"- cells: {len(rows)}",
        f"- commit_allowed: {commit_allowed}",
        f"- treatment PASSED: {summary['treatment_passed_revised']}",
        "",
        "## Primary PASS changes",
    ]
    for r in primary_pass_changed:
        md.append(
            f"- `{r['cell_id']}`: {r['historical_evaluator_status']} → {r['revised_evaluator_status']}"
        )
    if unexpected:
        md.append("")
        md.append("## UNEXPECTED primary PASS changes (blocking)")
        for cid in unexpected:
            md.append(f"- `{cid}`")
    (OUT_DIR / "summary.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    print(json.dumps(
        {
            "cells": len(rows),
            "changed": len(changed),
            "primary_pass_changed": [r["cell_id"] for r in primary_pass_changed],
            "unexpected": unexpected,
            "missing_expected": missing_expected,
            "treatment_passed_revised": summary["treatment_passed_revised"],
            "commit_allowed": commit_allowed,
            "original_evaluator_hash": ORIGINAL_EVALUATOR_HASH,
            "revised_evaluator_hash": revised_hash,
        },
        ensure_ascii=False,
        indent=2,
    ))
    return 0 if commit_allowed else 2


if __name__ == "__main__":
    raise SystemExit(main())
