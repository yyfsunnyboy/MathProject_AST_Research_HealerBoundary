"""Sync analysis_summary + per-cell validity after deep adjudication."""
from __future__ import annotations

import csv
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent

INVALID_EVALUATOR = {
    "gemini_3_5_flash__ce115_calc_polynomial_division_l1__ab2d__seed_2026071301",
    "gemini_3_5_flash__ce115_calc_polynomial_factor_roots_l1__ab1__seed_2026071301",
    "gemini_3_5_flash__ce115_calc_polynomial_factor_roots_l1__ab2g__seed_2026071301",
}

# Taxonomy mislabel only (oracle answer_mismatch / radical_mismatch labeled INTRINSIC_SAFETY)
INVALID_INFRA_TAXONOMY = {
    "gemini_3_5_flash__ce111_q08_polynomial_factor_parameter_recovery__ab1__seed_2026071301",
    "gemini_3_5_flash__ce111_q08_polynomial_factor_parameter_recovery__ab2g__seed_2026071301",
    "gemini_3_5_flash__ce112_q04_radical_simplification__ab2d__seed_2026071301",
}

VALIDITY = {}
table = json.loads((RUN / "full_cell_table.json").read_text(encoding="utf-8"))
for row in table:
    cid = row["cell_id"]
    if cid in INVALID_EVALUATOR:
        v = "INVALID_EVALUATOR"
        note = "structure-correct; latex exact-string false negative"
    elif cid in INVALID_INFRA_TAXONOMY:
        # outcome itself is valid model failure; taxonomy label is wrong
        v = "VALID_MODEL_OUTCOME"
        note = "model answer wrong/type/latex; runner mislabeled as INTRINSIC_SAFETY"
    else:
        v = "VALID_MODEL_OUTCOME"
        note = "ok" if row["evaluator_status"] == "PASSED" else "valid model/runtime failure"
    VALIDITY[cid] = {"validity": v, "note": note, **{k: row[k] for k in (
        "task_id", "condition", "domain_ops", "evaluator_status", "failure_category"
    )}}

counts: dict[str, int] = {}
for item in VALIDITY.values():
    counts[item["validity"]] = counts.get(item["validity"], 0) + 1

summary = json.loads((RUN / "analysis_summary.json").read_text(encoding="utf-8"))
summary["validity_counts"] = counts
summary["production_bug_cells"] = sorted(INVALID_EVALUATOR)
summary["commit_allowed"] = False
summary["commit_block_reason"] = (
    "INVALID_EVALUATOR latex exact-string false negatives on 3 cells; "
    "formal confirmatory commit blocked"
)
summary["final_adjudication"] = {
    "invalid_evaluator_cells": sorted(INVALID_EVALUATOR),
    "taxonomy_mislabeled_but_valid_model": sorted(INVALID_INFRA_TAXONOMY),
    "q02_verdict": "common_model_schema_error_bare_string_4x",
    "ab2d_failures_model_or_runtime": [
        "ce111_q02 (schema)",
        "ce111_q10 (Fraction/runtime channel)",
        "ce112_q04 (latex wrong)",
        "ce115_calc_polynomial_division_l1 (INVALID_EVALUATOR)",
        "ce115_calc_polynomial_factor_roots_l1 (API unpack EXECUTION_FAILURE)",
    ],
}
(RUN / "analysis_summary.json").write_text(
    json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)

per_cell = [VALIDITY[r["cell_id"]] for r in table]
(RUN / "per_cell_validity.json").write_text(
    json.dumps(per_cell, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)

# enrich CSV
rows_out = []
with (RUN / "full_cell_table.csv").open(encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)
    fieldnames = list(reader.fieldnames or []) + ["validity", "validity_note"]
    for r in reader:
        cid = r["cell_id"]
        r["validity"] = VALIDITY[cid]["validity"]
        r["validity_note"] = VALIDITY[cid]["note"]
        rows_out.append(r)
with (RUN / "full_cell_table.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    w.writerows(rows_out)

# also enrich json table
for r in table:
    cid = r["cell_id"]
    r["validity"] = VALIDITY[cid]["validity"]
    r["validity_note"] = VALIDITY[cid]["note"]
(RUN / "full_cell_table.json").write_text(
    json.dumps(table, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)

# forensic task×treatment matrix
matrix = {}
for r in table:
    matrix.setdefault(r["task_id"], {})[r["condition"]] = {
        "status": r["evaluator_status"],
        "validity": r["validity"],
    }
(RUN / "task_treatment_matrix.json").write_text(
    json.dumps(matrix, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)

print(json.dumps({"validity_counts": counts, "commit_allowed": False}, indent=2))
