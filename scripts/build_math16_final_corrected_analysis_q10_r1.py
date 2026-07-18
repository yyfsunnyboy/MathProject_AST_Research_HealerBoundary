"""Build final corrected 48-cell analysis after q10 Ab2d supplemental rerun."""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORIG = ROOT / "docs/experiments/results/gemini35flash_math16_latex_v1_ab123_run_001"
REV2 = ORIG / "evaluation_revision_002"
SUPP = ROOT / "docs/experiments/results/gemini35flash_math16_q10_ab2d_contract_fix_r1"
OUT = SUPP / "final_corrected_analysis"
TASK_Q10 = "ce111_q10_ordered_quadratic_roots_radical"
ORIG_Q10_AB2D = (
    "gemini_3_5_flash__ce111_q10_ordered_quadratic_roots_radical__ab2d__seed_2026071301"
)


def _rank(status: str) -> int:
    order = {
        "PASSED": 3,
        "ANSWER_INCORRECT": 2,
        "PARSE_MINOR": 1,
        "SCHEMA_FAILURE": 1,
        "EXECUTION_FAILURE": 1,
        "INTRINSIC_SAFETY": 1,
    }
    return order.get(status, 0)


def main() -> int:
    rev_rows = json.loads((REV2 / "cell_outcomes.json").read_text(encoding="utf-8"))
    supp_summary = json.loads((SUPP / "summary.json").read_text(encoding="utf-8"))
    supp_cell_dir = next((SUPP / "cells").iterdir())
    supp_art = json.loads((supp_cell_dir / "artifact.json").read_text(encoding="utf-8"))

    # Offline validation that contract fix rescues the frozen original first attempt.
    sys.path.insert(0, str(ROOT))
    from agent_tools.finals_rebuild.math16_pool import tasks_by_id
    from scripts.run_math16_latex_v1_gemini_live import classify_math16_response

    orig_art = json.loads(
        (ORIG / "cells" / ORIG_Q10_AB2D / "artifact.json").read_text(encoding="utf-8")
    )
    raw = (ORIG / "cells" / ORIG_Q10_AB2D / "raw_response.txt").read_text(encoding="utf-8")
    task = tasks_by_id()[TASK_Q10]
    offline_outcome, _, _ = classify_math16_response(
        raw,
        frozen_params=orig_art["frozen_parameters"],
        audit_oracle_payload=orig_art.get("audit_oracle_payload")
        or orig_art["frozen_parameters"],
        task=task,
    )
    offline_status = {
        "passed": "PASSED",
        "answer_incorrect": "ANSWER_INCORRECT",
        "runtime_failure": "EXECUTION_FAILURE",
        "infrastructure_failure": "EXECUTION_FAILURE",
        "intrinsic_safety": "INTRINSIC_SAFETY",
    }.get(offline_outcome, offline_outcome.upper())

    merged = []
    for row in rev_rows:
        if row["task_id"] == TASK_Q10 and row["condition"] == "ab2d":
            merged.append(
                {
                    "cell_id": supp_art["cell_id"],
                    "task_id": TASK_Q10,
                    "condition": "ab2d",
                    "domain_ops": "RadicalOps",
                    "source": "supplemental_rerun",
                    "revision_id": supp_summary["revision_id"],
                    "historical_original_status": orig_art["evaluator_status"],
                    "evaluation_revision_002_status": row["revised_evaluator_status"],
                    "final_evaluator_status": supp_art["evaluator_status"],
                    "offline_reeval_original_first_attempt": offline_status,
                    "post_hoc_supplemental_rerun": True,
                    "validity": "VALID_MODEL_OUTCOME",
                    "validity_note": (
                        "contract Fraction boundary fixed; supplemental live first-attempt "
                        "failed latex exact match (structural OK). Original INVALID_CONTRACT "
                        "cell preserved in audit trail."
                    ),
                }
            )
        else:
            merged.append(
                {
                    "cell_id": row["cell_id"],
                    "task_id": row["task_id"],
                    "condition": row["condition"],
                    "domain_ops": row["domain_ops"],
                    "source": "original_run_evaluation_revision_002",
                    "revision_id": "evaluation_revision_002",
                    "historical_original_status": row["historical_evaluator_status"],
                    "evaluation_revision_002_status": row["revised_evaluator_status"],
                    "final_evaluator_status": row["revised_evaluator_status"],
                    "offline_reeval_original_first_attempt": None,
                    "post_hoc_supplemental_rerun": False,
                    "validity": "VALID_MODEL_OUTCOME",
                    "validity_note": "from evaluation_revision_002",
                }
            )

    by_treatment = defaultdict(Counter)
    by_domain = defaultdict(lambda: defaultdict(Counter))
    by_task = defaultdict(dict)
    for r in merged:
        st = r["final_evaluator_status"]
        by_treatment[r["condition"]][st] += 1
        by_domain[r["domain_ops"] or "?"][r["condition"]][st] += 1
        by_task[r["task_id"]][r["condition"]] = st

    def paired(a: str, b: str) -> dict:
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

    hashes = {
        "math16_oracles": hashlib.sha256(
            (ROOT / "agent_tools/finals_rebuild/math16_oracles.py").read_bytes()
        ).hexdigest(),
        "math_answer_contracts": hashlib.sha256(
            (ROOT / "agent_tools/finals_rebuild/math_answer_contracts.py").read_bytes()
        ).hexdigest(),
        "run_math16_latex_v1_gemini_live": hashlib.sha256(
            (ROOT / "scripts/run_math16_latex_v1_gemini_live.py").read_bytes()
        ).hexdigest(),
    }

    summary = {
        "analysis_id": "math16_final_corrected_q10_ab2d_contract_fix_r1",
        "revision_id": supp_summary["revision_id"],
        "merge_rule": {
            "ab1": "original 16 cells via evaluation_revision_002",
            "ab2g": "original 16 cells via evaluation_revision_002",
            "ab2d": "15 original valid cells via evaluation_revision_002 + q10 supplemental rerun",
            "q10_ab2d": "post-hoc supplemental rerun only",
            "original_invalid_contract_cell": ORIG_Q10_AB2D,
        },
        "component_hashes_new": hashes,
        "component_hashes_old": {
            "math16_oracles": "d91389a48fd38283a9e7d6227111af3dfb34649f4621f4f33f4128dc7a72ce11",
            "math_answer_contracts": "b0e4cad48aa9e54048e4b13f63b0d880d77b59a21f870492d58ef1882302f9fb",
            "note": "old contracts hash from freeze closeout; oracles hash from latex semantic v2 commit",
        },
        "q10_ab2d_forensic": {
            "original_status": orig_art["evaluator_status"],
            "original_runtime_error": (orig_art.get("evaluator_details") or {}).get(
                "runtime_error"
            ),
            "offline_reeval_original_first_attempt_under_new_boundary": offline_status,
            "supplemental_status": supp_art["evaluator_status"],
            "supplemental_oracle_error": (supp_art.get("evaluator_details") or {}).get(
                "oracle_error"
            ),
            "supplemental_finding": (
                "Fraction JSON/oracle boundary OK; structural (6,1,3) OK; "
                "canonical_latex '6 + \\sqrt{3}' != '6+\\sqrt{3}' → VALID_MODEL latex miss"
            ),
        },
        "treatment_passed_final": {
            cond: f"{by_treatment[cond].get('PASSED', 0)}/16" for cond in ("ab1", "ab2g", "ab2d")
        },
        "treatment_x_outcome_final": {k: dict(v) for k, v in sorted(by_treatment.items())},
        "domain_x_treatment_x_outcome_final": {
            dom: {c: dict(ctr) for c, ctr in sorted(conds.items())}
            for dom, conds in sorted(by_domain.items())
        },
        "paired_comparisons_final": {
            "Ab1->Ab2g": paired("ab1", "ab2g"),
            "Ab1->Ab2d": paired("ab1", "ab2d"),
            "Ab2g->Ab2d": paired("ab2g", "ab2d"),
        },
        "cells": 48,
        "original_run_mutated": False,
    }

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (OUT / "full_cell_table.json").write_text(
        json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    with (OUT / "full_cell_table.csv").open("w", encoding="utf-8", newline="") as fh:
        fields = [
            "cell_id",
            "task_id",
            "condition",
            "domain_ops",
            "source",
            "final_evaluator_status",
            "historical_original_status",
            "evaluation_revision_002_status",
            "post_hoc_supplemental_rerun",
            "validity",
            "validity_note",
        ]
        w = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(merged)

    md = [
        "# Final corrected Math16 analysis (q10 Ab2d contract-fix r1)",
        "",
        f"- Supplemental run: `{supp_summary['run_id']}`",
        f"- Revision: `{supp_summary['revision_id']}`",
        f"- Treatment PASSED: {summary['treatment_passed_final']}",
        f"- Offline re-eval of original q10 Ab2d first-attempt: **{offline_status}**",
        f"- Supplemental live q10 Ab2d: **{supp_art['evaluator_status']}** "
        f"({summary['q10_ab2d_forensic']['supplemental_finding']})",
        "",
        "Original 48-cell run artifacts were not overwritten.",
    ]
    (OUT / "summary.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(json.dumps({
        "cells": len(merged),
        "treatment_passed_final": summary["treatment_passed_final"],
        "offline_original_q10_ab2d": offline_status,
        "supplemental_q10_ab2d": supp_art["evaluator_status"],
        "out": str(OUT),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
