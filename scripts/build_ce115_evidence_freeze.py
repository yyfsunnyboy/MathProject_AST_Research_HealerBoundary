"""Build CE115 Evidence Freeze + Master Matrix (offline; real_model_calls=0)."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs/experiments/analysis/ce115_evidence_freeze_20260717"
SEC_RENAME = {"SHARED_BINOMIAL_U_TEMPLATE": "SPURIOUS_SHARED_BINOMIAL_SQUARE_TEMPLATE"}
CORE_TASKS = [
    "ce115_calc_exact_rational_expression_l1",
    "ce115_calc_polynomial_division_l1",
    "ce115_calc_radical_simplification_l1",
]
HEALER_MAP = {
    "qwen3_5_4b__ce115_calc_radical_simplification_l1__ab1__seed_2026071301": {
        "healer_action": "L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP",
        "post_healer_status": "repair_to_pass",
        "production_approved": True,
        "fixture": "tests/finals_rebuild/fixtures/ce115_research_healer/cases/fail_radical_ab1_l2/",
        "layer_outcome": "repair_to_pass",
    },
    "qwen3_5_4b__ce115_calc_exact_rational_expression_l1__ab2d__seed_2026071301": {
        "healer_action": "L1_COMMENT_ONLY_IF_INSERT_PASS",
        "post_healer_status": "exploratory_parse_probe_only",
        "production_approved": False,
        "fixture": "tests/finals_rebuild/fixtures/ce115_research_healer/cases/fail_exact_ab2d_l1/",
        "layer_outcome": "exploratory_l1_not_production",
    },
}


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def freeze_q09_mechanism_names() -> dict[str, Any]:
    ledger_path = ROOT / "docs/experiments/analysis/ce115_q09_gemini_l5_mechanism_ledger.json"
    ledger = _load(ledger_path)
    tax = ledger.get("secondary_taxonomy", {})
    if "SHARED_BINOMIAL_U_TEMPLATE" in tax:
        tax["SPURIOUS_SHARED_BINOMIAL_SQUARE_TEMPLATE"] = tax.pop("SHARED_BINOMIAL_U_TEMPLATE")
    for cell in ledger.get("cells", []):
        if cell.get("secondary_label") == "SHARED_BINOMIAL_U_TEMPLATE":
            cell["secondary_label"] = "SPURIOUS_SHARED_BINOMIAL_SQUARE_TEMPLATE"
    sab = ledger.get("same_answer_vs_same_mechanism", {})
    for value in sab.values():
        if isinstance(value, dict) and isinstance(value.get("mechanism"), str):
            value["mechanism"] = value["mechanism"].replace(
                "SHARED_BINOMIAL_U_TEMPLATE", "SPURIOUS_SHARED_BINOMIAL_SQUARE_TEMPLATE"
            )
        elif isinstance(value, str):
            pass
    caf = sab.get("cross_answer_same_family")
    if isinstance(caf, dict):
        sab["cross_answer_same_family"] = {
            k: (v.replace("SHARED_BINOMIAL_U_TEMPLATE", "SPURIOUS_SHARED_BINOMIAL_SQUARE_TEMPLATE") if isinstance(v, str) else v)
            for k, v in caf.items()
        }
    freeze = {
        "primary": "EQUATION_RECONSTRUCTION_WRONG",
        "secondary_canonical": "SPURIOUS_SHARED_BINOMIAL_SQUARE_TEMPLATE",
        "alias_retired": "SHARED_BINOMIAL_U_TEMPLATE",
        "other_confirmed_secondaries": [
            "SHIFT_PM_SUBTRACTED",
            "PARAMS_COPIED_AS_ROOTS",
            "SHIFT_AND_SHIFT_MINUS_SUB",
            "SHIFT_AND_SHIFT_PLUS_SUB_NO_DIV",
            "SHIFT_PM_SUB_OVER_LEADING",
        ],
    }
    ledger["mechanism_name_freeze"] = freeze
    _write(ledger_path, ledger)
    md_path = ROOT / "docs/experiments/analysis/ce115_q09_gemini_l5_mechanism_forensic.md"
    md = md_path.read_text(encoding="utf-8")
    md_path.write_text(md.replace("SHARED_BINOMIAL_U_TEMPLATE", "SPURIOUS_SHARED_BINOMIAL_SQUARE_TEMPLATE"), encoding="utf-8")
    return freeze


def summarize_cohort(cid: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    nat = [r for r in rows if r.get("row_kind") != "regression_support"]
    regrows = [r for r in rows if r.get("row_kind") == "regression_support"]
    return {
        "cohort_id": cid,
        "rows_total": len(rows),
        "natural_rows": len(nat),
        "regression_support_rows": len(regrows),
        "natural_failures": sum(1 for r in nat if r["observed_status"] != "PASSED"),
        "already_passed": sum(1 for r in nat if r["observed_status"] == "PASSED" or r["eligibility"] == "ALREADY_PASSED"),
        "production_eligible": sum(1 for r in nat if r["eligibility"] == "ELIGIBLE"),
        "conditional": sum(1 for r in nat if r["eligibility"] == "CONDITIONAL"),
        "ineligible": sum(1 for r in nat if r["eligibility"] == "INELIGIBLE"),
        "triggered_formal_L2": sum(
            1 for r in nat if r["healer_action"] == "L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP" and r.get("production_approved")
        ),
        "triggered_exploratory_L1": sum(1 for r in nat if r["healer_action"] == "L1_COMMENT_ONLY_IF_INSERT_PASS"),
        "repair_to_pass_formal": sum(1 for r in nat if r["post_healer_status"] == "repair_to_pass"),
        "repair_to_next_layer": sum(1 for r in nat if r["post_healer_status"] == "repair_to_next_layer"),
        "no_op_regression_guards": sum(1 for r in regrows if r["post_healer_status"] == "no_op")
        + sum(1 for r in nat if r["post_healer_status"] == "no_op"),
        "false_positive": 0,
        "exploratory_l1_counted_as_formal_success": False,
    }


def build() -> dict[str, Any]:
    freeze = freeze_q09_mechanism_names()
    gem_core = _load(ROOT / "docs/experiments/results/ce115_gemini_clean_incremental_pilot_01/cell_results.json")
    qwen_core = _load(ROOT / "docs/experiments/results/ce115_qwen_clean_incremental_pilot_01/cell_results.json")
    seven = _load(ROOT / "docs/experiments/analysis/ce115_qwen_clean_incremental_seven_cell_forensic_ledger.json")
    seven_by = {c["cell_id"]: c for c in seven["cells"]}
    l5 = _load(ROOT / "docs/experiments/analysis/ce115_q09_gemini_l5_mechanism_ledger.json")
    l5_by = {c["cell_id"]: c for c in l5["cells"]}
    reg = _load(ROOT / "tests/finals_rebuild/fixtures/ce115_research_healer/regression_manifest.json")

    matrix: list[dict[str, Any]] = []

    def add_row(**kwargs: Any) -> None:
        for key in (
            "cohort_id",
            "cell_id",
            "model",
            "task_or_instance",
            "condition",
            "observed_status",
            "primary_layer",
            "secondary_mechanism",
            "eligibility",
            "healer_action",
            "post_healer_status",
            "evidence_artifact",
        ):
            if key not in kwargs:
                raise KeyError(key)
        matrix.append(kwargs)

    for row in gem_core:
        add_row(
            cohort_id="A_core_clean_pilot",
            cell_id=row["cell_id"],
            model=row.get("model") or "gemini-3.5-flash",
            task_or_instance=row["task_id"],
            condition=row["condition"],
            observed_status=row["evaluator_status"],
            primary_layer="N_A_PASSED",
            secondary_mechanism=None,
            eligibility="ALREADY_PASSED",
            healer_action="none",
            post_healer_status="N_A_no_healer_in_pilot",
            evidence_artifact=(
                "docs/experiments/results/ce115_gemini_clean_incremental_pilot_01/cells/"
                f"{row['cell_id']}/artifact.json"
            ),
            seed=row.get("seed", 2026071301),
            notes="natural outcome; healer not applied in pilot",
        )

    for row in qwen_core:
        cid = row["cell_id"]
        if row["evaluator_status"] == "PASSED":
            add_row(
                cohort_id="A_core_clean_pilot",
                cell_id=cid,
                model=row.get("model") or "qwen3.5:4b",
                task_or_instance=row["task_id"],
                condition=row["condition"],
                observed_status="PASSED",
                primary_layer="N_A_PASSED",
                secondary_mechanism=None,
                eligibility="ALREADY_PASSED",
                healer_action="none",
                post_healer_status="N_A_no_healer_in_pilot",
                evidence_artifact=(
                    "docs/experiments/results/ce115_qwen_clean_incremental_pilot_01/cells/"
                    f"{cid}/artifact.json"
                ),
                seed=row.get("seed", 2026071301),
                notes="natural PASS",
            )
            continue
        forensic = seven_by[cid]
        add_row(
            cohort_id="A_core_clean_pilot",
            cell_id=cid,
            model=row.get("model") or "qwen3.5:4b",
            task_or_instance=row["task_id"],
            condition=row["condition"],
            observed_status=row["evaluator_status"],
            primary_layer=forensic["primary_layer"],
            secondary_mechanism=None,
            eligibility=forensic["eligibility"],
            healer_action="none",
            post_healer_status="N_A_no_healer_in_pilot",
            evidence_artifact=forensic["artifact_path"],
            seed=forensic.get("seed", 2026071301),
            forensic_ledger_ref="ce115_qwen_clean_incremental_seven_cell_forensic_ledger.json",
            notes="natural failure; layer from forensic ledger",
        )

    for cid, forensic in seven_by.items():
        mapped = HEALER_MAP.get(
            cid,
            {
                "healer_action": "none_production_allowlist",
                "post_healer_status": "unchanged_natural_failure",
                "production_approved": False,
                "fixture": None,
                "layer_outcome": "no_production_trigger",
            },
        )
        if cid not in HEALER_MAP:
            if forensic["eligibility"] == "CONDITIONAL":
                mapped = {**mapped, "layer_outcome": "conditional_no_production_rule"}
            elif forensic["eligibility"] == "INELIGIBLE":
                mapped = {**mapped, "layer_outcome": "ineligible"}
        add_row(
            cohort_id="B_healer_qwen_core_failures",
            cell_id=cid,
            model="qwen3.5:4b",
            task_or_instance=forensic["task_id"],
            condition=forensic["condition"],
            observed_status=forensic["observed_evaluator_status"],
            primary_layer=forensic["primary_layer"],
            secondary_mechanism=None,
            eligibility=forensic["eligibility"],
            healer_action=mapped["healer_action"],
            post_healer_status=mapped["post_healer_status"],
            evidence_artifact=forensic["artifact_path"],
            seed=forensic.get("seed", 2026071301),
            healer_fixture=mapped.get("fixture"),
            production_approved=mapped.get("production_approved", False),
            layer_outcome=mapped["layer_outcome"],
            notes="Healer cohort; L2 formal single repair-to-pass; L1 exploratory only",
        )

    for case in reg["cases"]:
        if case["case_id"] == "fail_radical_ab1_l2":
            continue
        add_row(
            cohort_id="B_healer_qwen_core_failures",
            cell_id=f"regression::{case['case_id']}",
            model="qwen3.5:4b" if str(case.get("source_cell_id", "")).startswith("qwen") else "synthetic",
            task_or_instance=case.get("source_cell_id") or case["case_id"],
            condition="regression",
            observed_status="REGRESSION_FIXTURE",
            primary_layer="N_A_REGRESSION",
            secondary_mechanism=None,
            eligibility="REGRESSION_GUARD",
            healer_action="L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP",
            post_healer_status=case["expected_final_status"],
            evidence_artifact=f"tests/finals_rebuild/fixtures/ce115_research_healer/{case['source_artifact']}",
            seed=None,
            production_approved=True,
            layer_outcome="no_op" if case["expected_final_status"] == "no_op" else case["expected_final_status"],
            notes="regression corpus guard; not a natural pilot cell",
            row_kind="regression_support",
        )

    q09_dirs = {
        "formal_gemini": ROOT / "docs/experiments/results/ce115_q09_gemini_clean_incremental_pilot_01",
        "formal_qwen": ROOT / "docs/experiments/results/ce115_q09_qwen_clean_incremental_pilot_01",
        "sign_gemini": ROOT / "docs/experiments/results/ce115_q09_sign_pairing_gemini_01",
        "sign_qwen": ROOT / "docs/experiments/results/ce115_q09_sign_pairing_qwen_01",
    }
    for path in q09_dirs.values():
        for row in _load(path / "cell_results.json"):
            cid = row["cell_id"]
            mech = l5_by.get(cid)
            instance = row.get("instance_id") or row.get("task_id") or "ce115_calc_common_factor_quadratic_root_ordering_l1"
            if mech:
                primary = "L5"
                secondary = mech.get("secondary_label")
                eligibility = "INELIGIBLE"
                notes = f"Gemini L5 forensic; primary_mechanism={mech['L5_mechanism']}"
                primary_mechanism = mech["L5_mechanism"]
                l5_unrepairable = True
            else:
                status = row["evaluator_status"]
                if status == "ANSWER_INCORRECT":
                    primary = "L5_STATUS_ONLY_NOT_VERIFIED_MECHANISM"
                elif status == "PARSE_MINOR":
                    primary = "L1_STATUS_ONLY_NOT_VERIFIED"
                elif status == "SCHEMA_FAILURE":
                    primary = "L2_STATUS_ONLY_NOT_VERIFIED"
                elif status == "RUNTIME_FAILURE":
                    primary = "L4_OR_L5_STATUS_ONLY_NOT_VERIFIED"
                else:
                    primary = "NOT_VERIFIED"
                secondary = "NOT_VERIFIED"
                primary_mechanism = None
                eligibility = "INELIGIBLE" if status == "ANSWER_INCORRECT" else "NOT_ASSESSED_FOR_HEALER"
                notes = "q09 diagnostic cell; L5 mechanism forensic Gemini-only"
                l5_unrepairable = status == "ANSWER_INCORRECT"
            rel = (path / f"cells/{cid}/artifact.json").relative_to(ROOT).as_posix()
            add_row(
                cohort_id="C_q09_diagnostic",
                cell_id=cid,
                model=row.get("model") or row.get("model_family"),
                task_or_instance=instance,
                condition=row["condition"],
                observed_status=row["evaluator_status"],
                primary_layer=primary,
                secondary_mechanism=secondary,
                primary_mechanism=primary_mechanism,
                eligibility=eligibility,
                healer_action="none",
                post_healer_status="N_A_diagnostic_no_healer",
                evidence_artifact=rel,
                seed=row.get("seed", 2026071301),
                notes=notes,
                l5_unrepairable=l5_unrepairable,
            )

    keys = [(m["cohort_id"], m["cell_id"]) for m in matrix]
    if len(keys) != len(set(keys)):
        raise SystemExit(f"duplicate matrix keys: {Counter(keys).most_common(5)}")

    a_n = sum(1 for m in matrix if m["cohort_id"] == "A_core_clean_pilot")
    b_nat = sum(1 for m in matrix if m["cohort_id"] == "B_healer_qwen_core_failures" and not m.get("row_kind"))
    b_reg = sum(1 for m in matrix if m.get("row_kind") == "regression_support")
    c_n = sum(1 for m in matrix if m["cohort_id"] == "C_q09_diagnostic")

    manifest = {
        "manifest_id": "ce115_evidence_freeze_master_v1",
        "frozen_date": "2026-07-17",
        "real_model_calls": 0,
        "status": "evidence_freeze",
        "mechanism_name_freeze": freeze,
        "cohorts": [
            {
                "cohort_id": "A_core_clean_pilot",
                "purpose": (
                    "Core clean-incremental pilot on CE115 tasks 3/5/7 "
                    "(exact_rational, polynomial_division, radical_simplification) under Ab1/Ab2g/Ab2d."
                ),
                "tasks": CORE_TASKS,
                "models": ["gemini-3.5-flash", "qwen3.5:4b"],
                "conditions": ["ab1", "ab2g", "ab2d"],
                "seeds": [2026071301],
                "cell_count": a_n,
                "included_artifacts": [
                    "docs/experiments/results/ce115_gemini_clean_incremental_pilot_01/",
                    "docs/experiments/results/ce115_qwen_clean_incremental_pilot_01/",
                    "docs/experiments/analysis/ce115_qwen_clean_incremental_seven_cell_forensic_ledger.json",
                ],
                "primary_outcomes": {
                    "gemini_passed": 9,
                    "qwen_passed": 2,
                    "qwen_natural_failures": 7,
                },
                "prohibited_aggregations": [
                    "Do not merge with cohort B healer success into a single pilot success rate",
                    "Do not merge with cohort C q09 diagnostic outcomes",
                    "Do not treat task_id *_l1 as failure layer L1",
                ],
            },
            {
                "cohort_id": "B_healer_qwen_core_failures",
                "purpose": (
                    "Healer adjudication on Qwen core natural failures: one formal L2 repair-to-pass "
                    "+ exploratory L1 (not production) + regression no-op guards."
                ),
                "tasks": CORE_TASKS,
                "models": ["qwen3.5:4b"],
                "conditions": ["ab1", "ab2g", "ab2d", "regression"],
                "seeds": [2026071301],
                "cell_count": b_nat + b_reg,
                "cell_count_natural_failures": b_nat,
                "cell_count_regression_support": b_reg,
                "included_artifacts": [
                    "docs/experiments/analysis/ce115_qwen_clean_incremental_seven_cell_forensic_ledger.json",
                    "docs/experiments/analysis/ce115_research_healer_frozen_spec_v1.md",
                    "tests/finals_rebuild/fixtures/ce115_research_healer/regression_manifest.json",
                    "agent_tools/finals_rebuild/ce115_research_healer_rules_l2.py",
                    "agent_tools/finals_rebuild/ce115_research_healer_rules_l1.py",
                ],
                "primary_outcomes": {
                    "formal_L2_repair_to_pass": 1,
                    "exploratory_L1_not_production": 1,
                    "production_eligible_natural": 1,
                    "regression_no_ops": 4,
                },
                "prohibited_aggregations": [
                    "Do not count exploratory L1 as formal repair-to-pass",
                    "Do not generalize single L2 fixture to all SCHEMA_FAILURE",
                    "Do not claim oracle-free L2",
                    "Do not mix with cohort C L5 unrepairable rates",
                ],
            },
            {
                "cohort_id": "C_q09_diagnostic",
                "purpose": (
                    "q09 formal clean-incremental pilot + sign-pairing diagnostic; "
                    "Gemini L5 mechanism forensic (equation reconstruction)."
                ),
                "tasks": [
                    "ce115_calc_common_factor_quadratic_root_ordering_l1",
                    "xp7_2xm10",
                    "xm7_2xm10",
                    "xp7_2xp10",
                    "xm7_2xp10",
                ],
                "models": ["gemini-3.5-flash", "qwen3.5:4b"],
                "conditions": ["ab1", "ab2g", "ab2d"],
                "seeds": [2026071301],
                "cell_count": c_n,
                "included_artifacts": [
                    "docs/experiments/results/ce115_q09_gemini_clean_incremental_pilot_01/",
                    "docs/experiments/results/ce115_q09_qwen_clean_incremental_pilot_01/",
                    "docs/experiments/results/ce115_q09_sign_pairing_gemini_01/",
                    "docs/experiments/results/ce115_q09_sign_pairing_qwen_01/",
                    "docs/experiments/results/ce115_q09_sign_pairing_combined_01/",
                    "docs/experiments/analysis/ce115_q09_gemini_l5_mechanism_ledger.json",
                    "docs/experiments/analysis/ce115_q09_gemini_l5_mechanism_forensic.md",
                ],
                "primary_outcomes": {
                    "formal_q09_cells": 6,
                    "sign_pairing_cells": 24,
                    "gemini_l5_mechanism_forensiced": 15,
                    "dominant_mechanism": (
                        "EQUATION_RECONSTRUCTION_WRONG / SPURIOUS_SHARED_BINOMIAL_SQUARE_TEMPLATE"
                    ),
                },
                "prohibited_aggregations": [
                    "Do not mix q09 diagnostic pass/fail with core Healer success rates",
                    "Do not claim L5 equation-reconstruction is Healer-repairable",
                    "Do not treat sign-pairing as production task expansion",
                ],
            },
        ],
    }

    layer = {
        "summary_id": "ce115_evidence_freeze_layer_summary_v1",
        "real_model_calls": 0,
        "by_cohort": {},
        "healer_formal_headline": {
            "L2_formal_repair_to_pass": 1,
            "L1_exploratory_not_production": 1,
            "L5_q09_equation_reconstruction_unrepairable": (
                "Gemini forensic dominant; not Healer-eligible"
            ),
        },
        "prohibited": [
            "Do not sum A+B+C into one success rate",
            "Do not count exploratory L1 as repair-to-pass",
            "Do not count q09 diagnostic cells in Healer success denominator",
        ],
    }
    for cid in ("A_core_clean_pilot", "B_healer_qwen_core_failures", "C_q09_diagnostic"):
        layer["by_cohort"][cid] = summarize_cohort(cid, [m for m in matrix if m["cohort_id"] == cid])
    bsum = layer["by_cohort"]["B_healer_qwen_core_failures"]
    layer["healer_layer_rollup_from_B_only"] = {
        "natural_failures": bsum["natural_failures"],
        "production_eligible": bsum["production_eligible"],
        "triggered": bsum["triggered_formal_L2"],
        "repair_to_pass": bsum["repair_to_pass_formal"],
        "repair_to_next_layer": bsum["repair_to_next_layer"],
        "ineligible": bsum["ineligible"],
        "no_op": bsum["no_op_regression_guards"],
        "false_positive": bsum["false_positive"],
        "exploratory_L1": bsum["triggered_exploratory_L1"],
    }

    OUT.mkdir(parents=True, exist_ok=True)
    _write(OUT / "master_experiment_manifest.json", manifest)
    _write(
        OUT / "cell_level_final_matrix.json",
        {
            "matrix_id": "ce115_evidence_freeze_cell_matrix_v1",
            "real_model_calls": 0,
            "cell_count": len(matrix),
            "cells": matrix,
        },
    )
    _write(OUT / "layer_level_summary.json", layer)
    _write(OUT / "ce115_q09_mechanism_name_freeze.json", freeze)

    errors: list[str] = []
    if a_n != 18:
        errors.append(f"A expected 18 got {a_n}")
    if b_nat != 7:
        errors.append(f"B natural expected 7 got {b_nat}")
    if b_reg != 4:
        errors.append(f"B regression expected 4 got {b_reg}")
    if c_n != 30:
        errors.append(f"C expected 30 got {c_n}")
    gem_n = len(list((ROOT / "docs/experiments/results/ce115_gemini_clean_incremental_pilot_01/cells").iterdir()))
    qwen_n = len(list((ROOT / "docs/experiments/results/ce115_qwen_clean_incremental_pilot_01/cells").iterdir()))
    if gem_n != 9 or qwen_n != 9:
        errors.append(f"core artifact dirs gem={gem_n} qwen={qwen_n}")
    re_b = summarize_cohort(
        "B_healer_qwen_core_failures",
        [m for m in matrix if m["cohort_id"] == "B_healer_qwen_core_failures"],
    )
    if re_b != layer["by_cohort"]["B_healer_qwen_core_failures"]:
        errors.append("layer B mismatch on recompute")
    rtp = [m for m in matrix if m["post_healer_status"] == "repair_to_pass"]
    if len(rtp) != 1:
        errors.append(f"repair_to_pass count {len(rtp)}")
    if any(
        m["healer_action"] == "L1_COMMENT_ONLY_IF_INSERT_PASS" and m["post_healer_status"] == "repair_to_pass"
        for m in matrix
    ):
        errors.append("L1 counted as repair_to_pass")
    if freeze["secondary_canonical"] != "SPURIOUS_SHARED_BINOMIAL_SQUARE_TEMPLATE":
        errors.append("mechanism freeze name mismatch")
    if any(c.get("secondary_label") == "SHARED_BINOMIAL_U_TEMPLATE" for c in l5_by.values()):
        # reload after freeze
        l5_reload = _load(ROOT / "docs/experiments/analysis/ce115_q09_gemini_l5_mechanism_ledger.json")
        if any(c.get("secondary_label") == "SHARED_BINOMIAL_U_TEMPLATE" for c in l5_reload["cells"]):
            errors.append("old secondary name still present in ledger")

    validation = {
        "ok": not errors,
        "errors": errors,
        "counts": {"A": a_n, "B_natural": b_nat, "B_regression": b_reg, "C": c_n, "matrix_total": len(matrix)},
        "real_model_calls": 0,
    }
    _write(OUT / "validation.json", validation)
    return validation


if __name__ == "__main__":
    result = build()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    raise SystemExit(0 if result["ok"] else 2)
