"""Offline re-evaluation revision_003: compound latex + taxonomy; confirmatory stats.

- Official 48 cells: original run_001 first responses only.
- q10 Ab2d official = original first attempt under revised evaluator (PASSED).
- Supplemental q10 Ab2d is validation-only and excluded from confirmatory stats.
- model_calls = 0; raw responses never overwritten.
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.math16_pool import tasks_by_id
from scripts.run_math16_latex_v1_gemini_live import classify_math16_response
from agent_tools.finals_rebuild.math16_oracles import EVALUATOR_LATEX_SEMANTIC_REVISION

ORIG_RUN = ROOT / "docs/experiments/results/gemini35flash_math16_latex_v1_ab123_run_001"
SUPP_RUN = ROOT / "docs/experiments/results/gemini35flash_math16_q10_ab2d_contract_fix_r1"
OUT = ORIG_RUN / "evaluation_revision_003"
Q10 = "ce111_q10_ordered_quadratic_roots_radical"
ORIG_Q10_AB2D = f"gemini_3_5_flash__{Q10}__ab2d__seed_2026071301"
OLD_ORACLE_HASH = "6e937d0a2bc39b62eea475c3de02105bc2603c500af5851765396edeead47e7b"


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _map(outcome: str) -> str:
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
    if status == "PASSED":
        return 3
    if status == "ANSWER_INCORRECT":
        return 2
    return 1 if status not in {"API_FAILURE", "NOT_RUN"} else 0


def _reeval_cell(cell_dir: Path, by_id: dict[str, Any]) -> dict[str, Any]:
    art = json.loads((cell_dir / "artifact.json").read_text(encoding="utf-8"))
    raw = (cell_dir / "raw_response.txt").read_text(encoding="utf-8")
    task = by_id[art["task_id"]]
    outcome, _code, details = classify_math16_response(
        raw,
        frozen_params=art["frozen_parameters"],
        audit_oracle_payload=art.get("audit_oracle_payload") or art["frozen_parameters"],
        task=task,
    )
    new_status = _map(outcome)
    return {
        "cell_id": art["cell_id"],
        "task_id": art["task_id"],
        "condition": art["condition"],
        "domain_ops": art.get("domain_ops"),
        "historical_evaluator_status": art.get("evaluator_status"),
        "revised_evaluator_status": new_status,
        "revised_outcome": outcome,
        "primary_pass_changed": (art.get("evaluator_status") == "PASSED")
        != (new_status == "PASSED"),
        "status_changed": art.get("evaluator_status") != new_status,
        "oracle_error": details.get("oracle_error"),
        "structural_ok": details.get("structural_ok"),
        "latex_ok": details.get("latex_ok"),
        "source": "original_run_001_first_attempt",
        "included_in_confirmatory_statistics": True,
    }


def main() -> int:
    by_id = tasks_by_id()
    revised_hash = _sha256_file(ROOT / "agent_tools/finals_rebuild/math16_oracles.py")
    cell_dirs = sorted((ORIG_RUN / "cells").glob("gemini_3_5_flash__*"))
    if len(cell_dirs) != 48:
        raise SystemExit(f"expected 48 cells, got {len(cell_dirs)}")

    rows = [_reeval_cell(d, by_id) for d in cell_dirs]
    # Official q10 Ab2d must be PASSED from original first attempt.
    q10 = next(r for r in rows if r["cell_id"] == ORIG_Q10_AB2D)
    if q10["revised_evaluator_status"] != "PASSED":
        raise SystemExit(
            f"official q10 Ab2d not PASSED under revision_003: {q10['revised_evaluator_status']}"
        )

    # Supplemental validation-only reeval (excluded from stats).
    supp_dir = next((SUPP_RUN / "cells").iterdir())
    supp_art = json.loads((supp_dir / "artifact.json").read_text(encoding="utf-8"))
    supp_raw = (supp_dir / "raw_response.txt").read_text(encoding="utf-8")
    task = by_id[Q10]
    supp_outcome, _, supp_details = classify_math16_response(
        supp_raw,
        frozen_params=supp_art["frozen_parameters"],
        audit_oracle_payload=supp_art["audit_oracle_payload"],
        task=task,
    )
    supplemental = {
        "cell_id": supp_art["cell_id"],
        "task_id": Q10,
        "condition": "ab2d",
        "historical_evaluator_status": supp_art.get("evaluator_status"),
        "revised_evaluator_status": _map(supp_outcome),
        "revised_outcome": supp_outcome,
        "oracle_error": supp_details.get("oracle_error"),
        "structural_ok": supp_details.get("structural_ok"),
        "latex_ok": supp_details.get("latex_ok"),
        "source": "supplemental_live_call",
        "supplemental_validation_only": True,
        "excluded_from_confirmatory_statistics": True,
        "extra_api_call": True,
        "included_in_confirmatory_statistics": False,
    }

    by_treatment: dict[str, Counter[str]] = defaultdict(Counter)
    by_domain: dict[str, dict[str, Counter[str]]] = defaultdict(lambda: defaultdict(Counter))
    by_task: dict[str, dict[str, str]] = defaultdict(dict)
    for r in rows:
        by_treatment[r["condition"]][r["revised_evaluator_status"]] += 1
        by_domain[r["domain_ops"] or "?"][r["condition"]][r["revised_evaluator_status"]] += 1
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

    passed = {
        cond: by_treatment[cond].get("PASSED", 0) for cond in ("ab1", "ab2g", "ab2d")
    }
    total_passed = sum(passed.values())
    if passed != {"ab1": 13, "ab2g": 14, "ab2d": 13} or total_passed != 40:
        raise SystemExit(
            f"unexpected confirmatory pass counts: {passed} total={total_passed}"
        )

    # Primary PASS changes vs historical original artifacts (not vs revision_002).
    primary_pass_changed = [r for r in rows if r["primary_pass_changed"]]
    expected_pass_flip_to_passed = {
        ORIG_Q10_AB2D,  # Fraction boundary
        "gemini_3_5_flash__ce115_calc_polynomial_division_l1__ab2d__seed_2026071301",
        "gemini_3_5_flash__ce115_calc_polynomial_factor_roots_l1__ab1__seed_2026071301",
        "gemini_3_5_flash__ce115_calc_polynomial_factor_roots_l1__ab2g__seed_2026071301",
    }
    # Relative to historical original, these 4 should flip to PASSED; no other PASS flips.
    unexpected_pass = [
        r["cell_id"]
        for r in primary_pass_changed
        if r["revised_evaluator_status"] == "PASSED"
        and r["cell_id"] not in expected_pass_flip_to_passed
    ]
    unexpected_fail = [
        r["cell_id"]
        for r in primary_pass_changed
        if r["revised_evaluator_status"] != "PASSED"
        and r["historical_evaluator_status"] == "PASSED"
    ]
    if unexpected_pass or unexpected_fail:
        raise SystemExit(
            f"unexpected primary pass/fail changes: to_passed={unexpected_pass} "
            f"to_fail={unexpected_fail}"
        )

    OUT.mkdir(parents=True, exist_ok=True)
    summary = {
        "revision_id": "evaluation_revision_003",
        "evaluator_revision": EVALUATOR_LATEX_SEMANTIC_REVISION,
        "model_calls": 0,
        "original_artifacts_mutated": False,
        "cells_reevaluated_official": 48,
        "original_evaluator_hash": OLD_ORACLE_HASH,
        "revised_evaluator_hash": revised_hash,
        "treatment_passed_confirmatory": {
            "ab1": "13/16",
            "ab2g": "14/16",
            "ab2d": "13/16",
            "total": "40/48",
        },
        "treatment_x_outcome_confirmatory": {
            k: dict(v) for k, v in sorted(by_treatment.items())
        },
        "domain_x_treatment_x_outcome_confirmatory": {
            dom: {c: dict(ctr) for c, ctr in sorted(conds.items())}
            for dom, conds in sorted(by_domain.items())
        },
        "paired_comparisons_confirmatory": {
            "Ab1->Ab2g": paired("ab1", "ab2g"),
            "Ab1->Ab2d": paired("ab1", "ab2d"),
            "Ab2g->Ab2d": paired("ab2g", "ab2d"),
        },
        "official_q10_ab2d": {
            "cell_id": ORIG_Q10_AB2D,
            "source": "original_run_001_first_attempt",
            "revised_evaluator_status": "PASSED",
            "note": "Fraction→int boundary + compound latex presentation; confirmatory",
        },
        "supplemental_q10_ab2d": supplemental,
        "provenance": {
            "original_first_attempt_is_official_result": True,
            "supplemental_is_extra_validation_only": True,
            "extra_api_call_not_in_48_budget": True,
            "excluded_from_confirmatory_statistics": [supplemental["cell_id"]],
        },
        "primary_pass_changed_vs_historical_original": [
            {
                "cell_id": r["cell_id"],
                "historical": r["historical_evaluator_status"],
                "revised": r["revised_evaluator_status"],
            }
            for r in primary_pass_changed
        ],
        "commit_allowed": True,
    }

    (OUT / "cell_outcomes.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (OUT / "supplemental_reeval.json").write_text(
        json.dumps(supplemental, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (OUT / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (OUT / "paired_comparison_report.json").write_text(
        json.dumps(summary["paired_comparisons_confirmatory"], ensure_ascii=False, indent=2)
        + "\n",
        encoding="utf-8",
    )

    # Final corrected analysis (confirmatory).
    final_dir = ORIG_RUN / "final_corrected_analysis_confirmatory"
    final_dir.mkdir(parents=True, exist_ok=True)
    table = []
    for r in rows:
        table.append(
            {
                **r,
                "final_evaluator_status": r["revised_evaluator_status"],
                "validity": "VALID_MODEL_OUTCOME",
                "confirmatory": True,
            }
        )
    (final_dir / "full_cell_table.json").write_text(
        json.dumps(table, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    with (final_dir / "full_cell_table.csv").open("w", encoding="utf-8", newline="") as fh:
        fields = [
            "cell_id",
            "task_id",
            "condition",
            "domain_ops",
            "historical_evaluator_status",
            "final_evaluator_status",
            "source",
            "included_in_confirmatory_statistics",
            "validity",
        ]
        w = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(table)

    final_summary = {
        "analysis_id": "math16_confirmatory_final_revision_003",
        "treatment_passed": summary["treatment_passed_confirmatory"],
        "treatment_x_outcome": summary["treatment_x_outcome_confirmatory"],
        "domain_x_treatment_x_outcome": summary["domain_x_treatment_x_outcome_confirmatory"],
        "paired_comparisons": summary["paired_comparisons_confirmatory"],
        "official_q10_ab2d": summary["official_q10_ab2d"],
        "supplemental_q10_ab2d": {
            **supplemental,
            "role": "supplemental_validation_only",
        },
        "provenance": summary["provenance"],
        "revised_evaluator_hash": revised_hash,
        "original_evaluator_hash": OLD_ORACLE_HASH,
        "model_calls_during_reeval": 0,
        "total_passed": "40/48",
    }
    (final_dir / "summary.json").write_text(
        json.dumps(final_summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (final_dir / "validity_provenance_report.json").write_text(
        json.dumps(
            {
                "validity_counts": {"VALID_MODEL_OUTCOME": 48},
                "confirmatory_cells": 48,
                "supplemental_excluded": 1,
                "official_result_source": "original_run_001_first_attempt",
                "supplemental_run": str(SUPP_RUN.relative_to(ROOT)).replace("\\", "/"),
                "notes": [
                    "Original first attempt is the official confirmatory result.",
                    "Supplemental live call is extra validation only and excluded from 48-cell stats.",
                    "Extra API call does not count toward the original 48-cell budget.",
                    "Confirmatory total PASSED = 40/48 (Ab1 13, Ab2g 14, Ab2d 13).",
                ],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (final_dir / "summary.md").write_text(
        "\n".join(
            [
                "# Math16 confirmatory final (evaluation_revision_003)",
                "",
                "- Official source: original run_001 first attempts",
                "- Supplemental q10 Ab2d: validation only (excluded)",
                f"- PASSED: Ab1 13/16, Ab2g 14/16, Ab2d 13/16, **total 40/48**",
                f"- Official q10 Ab2d: PASSED (`{ORIG_Q10_AB2D}`)",
                f"- Supplemental revised status: {supplemental['revised_evaluator_status']} (excluded)",
                "",
            ]
        ),
        encoding="utf-8",
    )

    # Also stamp supplemental run metadata without overwriting raw.
    stamp = {
        "supplemental_validation_only": True,
        "excluded_from_confirmatory_statistics": True,
        "evaluation_revision_003": supplemental,
        "official_replacement": {
            "uses_original_first_attempt": True,
            "original_cell_id": ORIG_Q10_AB2D,
            "official_status": "PASSED",
        },
    }
    (SUPP_RUN / "confirmatory_exclusion_stamp.json").write_text(
        json.dumps(stamp, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    print(
        json.dumps(
            {
                "commit_allowed": True,
                "treatment_passed": summary["treatment_passed_confirmatory"],
                "official_q10_ab2d": "PASSED",
                "supplemental_excluded_status": supplemental["revised_evaluator_status"],
                "revised_evaluator_hash": revised_hash,
                "primary_pass_changed": len(primary_pass_changed),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
