"""Build Gemini+Qwen exam external-validation 36-cell combined census (offline).

Does not modify pilot artifacts, freeze, prompts, oracles, evaluators, or Healer rules.
real_model_calls = 0.
"""
from __future__ import annotations

import json
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "docs/experiments/analysis/ce115_exam_ext_113_114_combined_census_01"
GEMINI = ROOT / "docs/experiments/results/ce115_exam_ext_113_114_gemini_pilot_01"
QWEN = ROOT / "docs/experiments/results/ce115_exam_ext_113_114_qwen_pilot_01"
EXISTING_L2 = "L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP"

# Manual review table keyed by (family, task_id, condition).
# machine_* come from artifacts; reviewed_* / eligibility are adjudicated here.
REVIEWS: dict[tuple[str, str, str], dict] = {
    # --- Gemini special corrections ---
    ("gemini", "ce115_ext_114_02_polynomial_simplify_l1", "ab1"): {
        "reviewed_layer": "L2",
        "reviewed_mechanism": "CORRECT_ANSWER_FLAT_DEGREE_MAP_MISSING_NESTED_COEFFICIENTS",
        "evidence": (
            "correct_answer returned {'2':5,'1':1,'0':-4}; leaf values match expected; "
            "contract requires {'coefficients': {...}}; machine labeled L5/ANSWER_INCORRECT."
        ),
        "l2_eligibility": "eligible_new_rule_candidate",
        "eligibility_checks": {
            "leaf_values_ok_or_unused": True,
            "local_structure_only": True,
            "contract_unique": True,
            "deterministic_idempotent_fail_closed": True,
            "no_resolve_again": True,
            "no_answer_oracle_compare": True,
            "reparse_revalidate_reexec_reeval": True,
        },
        "existing_rule_fit": None,
        "new_rule_candidate_id": "L2_CORRECT_ANSWER_SINGLE_KEY_WRAP_COEFFICIENTS",
        "notes": "Machine L5 corrected to reviewed L2 (schema/shape of correct_answer).",
    },
    ("gemini", "ce115_ext_114_02_polynomial_simplify_l1", "ab2g"): {
        "reviewed_layer": "L2",
        "reviewed_mechanism": "CORRECT_ANSWER_FLAT_DEGREE_MAP_MISSING_NESTED_COEFFICIENTS",
        "evidence": "Same flat degree-map shape; leaves 5/1/-4 correct; missing coefficients wrapper.",
        "l2_eligibility": "eligible_new_rule_candidate",
        "eligibility_checks": {
            "leaf_values_ok_or_unused": True,
            "local_structure_only": True,
            "contract_unique": True,
            "deterministic_idempotent_fail_closed": True,
            "no_resolve_again": True,
            "no_answer_oracle_compare": True,
            "reparse_revalidate_reexec_reeval": True,
        },
        "existing_rule_fit": None,
        "new_rule_candidate_id": "L2_CORRECT_ANSWER_SINGLE_KEY_WRAP_COEFFICIENTS",
        "notes": "Machine L5 corrected to reviewed L2.",
    },
    ("gemini", "ce115_ext_114_02_polynomial_simplify_l1", "ab2d"): {
        "reviewed_layer": "L2",
        "reviewed_mechanism": "CORRECT_ANSWER_FLAT_DEGREE_MAP_MISSING_NESTED_COEFFICIENTS",
        "evidence": (
            "Executed correct_answer still flat {'2':5,'1':1,'0':-4}; "
            "Ab2d ASSEMBLY_COMPLIANT but shape defect remains."
        ),
        "l2_eligibility": "eligible_new_rule_candidate",
        "eligibility_checks": {
            "leaf_values_ok_or_unused": True,
            "local_structure_only": True,
            "contract_unique": True,
            "deterministic_idempotent_fail_closed": True,
            "no_resolve_again": True,
            "no_answer_oracle_compare": True,
            "reparse_revalidate_reexec_reeval": True,
        },
        "existing_rule_fit": None,
        "new_rule_candidate_id": "L2_CORRECT_ANSWER_SINGLE_KEY_WRAP_COEFFICIENTS",
        "notes": "Machine L5 corrected to reviewed L2; DOMAIN adoption did not prevent shape defect.",
    },
    ("gemini", "ce115_ext_114_04_linear_system_l1", "ab2d"): {
        "reviewed_layer": "L3",
        "reviewed_mechanism": "DOMAIN_API_FRACTIONOPS_CREATE_INVALID_SIGNED_LITERAL",
        "evidence": "ValueError Invalid literal for Fraction: '-240/-120'; ASSEMBLY_COMPLIANT.",
        "l2_eligibility": "ineligible",
        "eligibility_checks": {
            "leaf_values_ok_or_unused": False,
            "local_structure_only": False,
            "contract_unique": False,
            "deterministic_idempotent_fail_closed": False,
            "no_resolve_again": False,
            "no_answer_oracle_compare": True,
            "reparse_revalidate_reexec_reeval": True,
        },
        "existing_rule_fit": None,
        "new_rule_candidate_id": None,
        "notes": (
            "Machine L4 runtime is manifestation; reviewed primary layer L3 (domain wiring/API misuse). "
            "Not an L2 structural-schema case; FractionOps modification forbidden."
        ),
    },
    # --- Qwen failures ---
    ("qwen", "ce115_ext_114_02_polynomial_simplify_l1", "ab2g"): {
        "reviewed_layer": "L2",
        "reviewed_mechanism": "ORACLE_PAYLOAD_BARE_SCALAR_NEEDS_SINGLE_KEY_WRAP",
        "evidence": (
            "oracle_payload returned bare expression string; frozen is single-key {expression}; "
            "correct_answer already has coefficients with correct leaves; L2 analyze triggered=True."
        ),
        "l2_eligibility": "eligible_existing_rule",
        "eligibility_checks": {
            "leaf_values_ok_or_unused": True,
            "local_structure_only": True,
            "contract_unique": True,
            "deterministic_idempotent_fail_closed": True,
            "no_resolve_again": True,
            "no_answer_oracle_compare": True,
            "reparse_revalidate_reexec_reeval": True,
        },
        "existing_rule_fit": EXISTING_L2,
        "new_rule_candidate_id": None,
        "notes": "Canonical production L2 allowlist case.",
    },
    ("qwen", "ce115_ext_114_02_polynomial_simplify_l1", "ab2d"): {
        "reviewed_layer": "L4",
        "reviewed_mechanism": "RUNTIME_NAMEERROR_FRACTION_NOT_DEFINED",
        "evidence": "NameError: name 'Fraction' is not defined; REQUIRED_OPERATION_NOT_COVERED.",
        "l2_eligibility": "ineligible",
        "eligibility_checks": {
            "leaf_values_ok_or_unused": False,
            "local_structure_only": False,
            "contract_unique": False,
            "deterministic_idempotent_fail_closed": False,
            "no_resolve_again": False,
            "no_answer_oracle_compare": True,
            "reparse_revalidate_reexec_reeval": True,
        },
        "existing_rule_fit": None,
        "new_rule_candidate_id": None,
        "notes": "Control/runtime binding failure; not L2 schema wrap.",
    },
    ("qwen", "ce115_ext_114_04_linear_system_l1", "ab1"): {
        "reviewed_layer": "L4",
        "reviewed_mechanism": "RUNTIME_NAMEERROR_EQUATIONS_NOT_DEFINED",
        "evidence": "NameError: name 'equations' is not defined.",
        "l2_eligibility": "ineligible",
        "eligibility_checks": {
            "leaf_values_ok_or_unused": False,
            "local_structure_only": False,
            "contract_unique": False,
            "deterministic_idempotent_fail_closed": False,
            "no_resolve_again": False,
            "no_answer_oracle_compare": True,
            "reparse_revalidate_reexec_reeval": True,
        },
        "existing_rule_fit": None,
        "new_rule_candidate_id": None,
        "notes": "Scope/control failure before schema.",
    },
    ("qwen", "ce115_ext_114_04_linear_system_l1", "ab2g"): {
        "reviewed_layer": "L1",
        "reviewed_mechanism": "PARSE_INVALID_DECIMAL_LITERAL",
        "evidence": "SyntaxError invalid decimal literal line=56; code_len=21399.",
        "l2_eligibility": "ineligible",
        "eligibility_checks": {
            "leaf_values_ok_or_unused": False,
            "local_structure_only": False,
            "contract_unique": False,
            "deterministic_idempotent_fail_closed": False,
            "no_resolve_again": False,
            "no_answer_oracle_compare": True,
            "reparse_revalidate_reexec_reeval": False,
        },
        "existing_rule_fit": None,
        "new_rule_candidate_id": None,
        "notes": "Parse layer; L1 experimental rules not production-approved.",
    },
    ("qwen", "ce115_ext_114_04_linear_system_l1", "ab2d"): {
        "reviewed_layer": "L1",
        "reviewed_mechanism": "PARSE_UNCLOSED_BRACE",
        "evidence": "SyntaxError '{' was never closed line=30.",
        "l2_eligibility": "ineligible",
        "eligibility_checks": {
            "leaf_values_ok_or_unused": False,
            "local_structure_only": False,
            "contract_unique": False,
            "deterministic_idempotent_fail_closed": False,
            "no_resolve_again": False,
            "no_answer_oracle_compare": True,
            "reparse_revalidate_reexec_reeval": False,
        },
        "existing_rule_fit": None,
        "new_rule_candidate_id": None,
        "notes": "Parse layer.",
    },
    ("qwen", "ce115_ext_114_08_radical_product_l1", "ab1"): {
        "reviewed_layer": "L2",
        "reviewed_mechanism": "ORACLE_PAYLOAD_BARE_SCALAR_NEEDS_SINGLE_KEY_WRAP",
        "evidence": (
            "oracle_payload bare expression string; frozen single-key; "
            "correct_answer terms already {2√3, 2√6}; L2 triggered=True."
        ),
        "l2_eligibility": "eligible_existing_rule",
        "eligibility_checks": {
            "leaf_values_ok_or_unused": True,
            "local_structure_only": True,
            "contract_unique": True,
            "deterministic_idempotent_fail_closed": True,
            "no_resolve_again": True,
            "no_answer_oracle_compare": True,
            "reparse_revalidate_reexec_reeval": True,
        },
        "existing_rule_fit": EXISTING_L2,
        "new_rule_candidate_id": None,
        "notes": "Existing L2 should be sufficient for repair-to-pass.",
    },
    ("qwen", "ce115_ext_114_08_radical_product_l1", "ab2g"): {
        "reviewed_layer": "L2",
        "reviewed_mechanism": "ORACLE_PAYLOAD_BARE_SCALAR_NEEDS_SINGLE_KEY_WRAP",
        "evidence": (
            "Bare oracle_payload string; L2 triggered=True; "
            "correct_answer uses float coefficients 2.0 (oracle rejects floats) — residual after wrap."
        ),
        "l2_eligibility": "eligible_existing_rule",
        "eligibility_checks": {
            "leaf_values_ok_or_unused": True,
            "local_structure_only": True,
            "contract_unique": True,
            "deterministic_idempotent_fail_closed": True,
            "no_resolve_again": True,
            "no_answer_oracle_compare": True,
            "reparse_revalidate_reexec_reeval": True,
        },
        "existing_rule_fit": EXISTING_L2,
        "new_rule_candidate_id": "L2_NUMERIC_LEAF_FLOAT_TO_INT_COERCE",
        "notes": (
            "Payload scalar equals frozen.expression — existing L2 eligible. "
            "Latent residual: correct_answer uses float 2.0 (oracle rejects) → may be "
            "repair-to-next-layer after wrap; float coerce listed as separate candidate only."
        ),
    },
    ("qwen", "ce115_ext_114_08_radical_product_l1", "ab2d"): {
        "reviewed_layer": "L1",
        "reviewed_mechanism": "PARSE_INVALID_SYNTAX",
        "evidence": "SyntaxError invalid syntax line=122.",
        "l2_eligibility": "ineligible",
        "eligibility_checks": {
            "leaf_values_ok_or_unused": False,
            "local_structure_only": False,
            "contract_unique": False,
            "deterministic_idempotent_fail_closed": False,
            "no_resolve_again": False,
            "no_answer_oracle_compare": True,
            "reparse_revalidate_reexec_reeval": False,
        },
        "existing_rule_fit": None,
        "new_rule_candidate_id": None,
        "notes": "Parse layer.",
    },
    ("qwen", "ce115_ext_113_10_factorization_l1", "ab1"): {
        "reviewed_layer": "L2",
        "reviewed_mechanism": "ORACLE_PAYLOAD_BARE_SCALAR_BUT_FROZEN_MULTI_KEY",
        "evidence": (
            "Returned oracle_payload bare expression string; frozen has expression+required_form; "
            "factors leaves look canonical; existing L2 frozen_not_single_key."
        ),
        "l2_eligibility": "eligible_new_rule_candidate",
        "eligibility_checks": {
            "leaf_values_ok_or_unused": True,
            "local_structure_only": True,
            "contract_unique": True,
            "deterministic_idempotent_fail_closed": True,
            "no_resolve_again": True,
            "no_answer_oracle_compare": True,
            "reparse_revalidate_reexec_reeval": True,
        },
        "existing_rule_fit": None,
        "new_rule_candidate_id": "L2_ORACLE_PAYLOAD_RESTORE_FULL_FROZEN",
        "notes": "Restore entire frozen dict when payload is scalar matching frozen.expression.",
    },
    ("qwen", "ce115_ext_113_11_rationalize_l1", "ab1"): {
        "reviewed_layer": "L2",
        "reviewed_mechanism": "ORACLE_PAYLOAD_DICT_MUTATED_AWAY_FROM_FROZEN",
        "evidence": (
            "oracle_payload dict keys match but target_expression mutated to '4 + 1' "
            "(answer leak into payload); correct_answer a/b/radicand/value already correct."
        ),
        "l2_eligibility": "eligible_new_rule_candidate",
        "eligibility_checks": {
            "leaf_values_ok_or_unused": True,
            "local_structure_only": True,
            "contract_unique": True,
            "deterministic_idempotent_fail_closed": True,
            "no_resolve_again": True,
            "no_answer_oracle_compare": True,
            "reparse_revalidate_reexec_reeval": True,
        },
        "existing_rule_fit": None,
        "new_rule_candidate_id": "L2_ORACLE_PAYLOAD_IDENTITY_RESTORE_FROM_FROZEN",
        "notes": "Replace oracle_payload with frozen identity when keys align / contract requires equality.",
    },
    ("qwen", "ce115_ext_113_11_rationalize_l1", "ab2d"): {
        "reviewed_layer": "L4",
        "reviewed_mechanism": "RUNTIME_INT_PARSE_HEX_LITERAL",
        "evidence": "ValueError invalid literal for int() with base 10: '0x35'.",
        "l2_eligibility": "ineligible",
        "eligibility_checks": {
            "leaf_values_ok_or_unused": False,
            "local_structure_only": False,
            "contract_unique": False,
            "deterministic_idempotent_fail_closed": False,
            "no_resolve_again": False,
            "no_answer_oracle_compare": True,
            "reparse_revalidate_reexec_reeval": True,
        },
        "existing_rule_fit": None,
        "new_rule_candidate_id": None,
        "notes": "Runtime/control; not L2.",
    },
}


def _head() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        return "unknown"


def _write(path: Path, obj: object) -> None:
    path.write_text(
        json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    cells: list[dict] = []
    for family, root in (("gemini", GEMINI), ("qwen", QWEN)):
        rows = json.loads((root / "cell_results.json").read_text(encoding="utf-8"))
        for r in rows:
            key = (family, r["task_id"], r["condition"])
            machine_layer = r["failure_layer"].get("primary_layer")
            machine_outcome = r["evaluator_status"]
            if machine_outcome == "PASSED":
                reviewed = {
                    "reviewed_layer": None,
                    "reviewed_mechanism": None,
                    "evidence": "machine PASSED; no failure review",
                    "l2_eligibility": None,
                    "eligibility_checks": None,
                    "existing_rule_fit": None,
                    "new_rule_candidate_id": None,
                    "notes": "pass",
                }
            else:
                if key not in REVIEWS:
                    raise KeyError(f"missing manual review for {key}")
                reviewed = REVIEWS[key]
            cells.append(
                {
                    "cell_id": r["cell_id"],
                    "model_family": family,
                    "model": r.get("model"),
                    "task_id": r["task_id"],
                    "condition": r["condition"],
                    "seed": r["seed"],
                    "canonical_prompt_hash": r["canonical_prompt_hash"],
                    "machine_outcome": machine_outcome,
                    "machine_layer": machine_layer,
                    "machine_failure_class": r.get("failure_class"),
                    "reviewed_layer": reviewed["reviewed_layer"],
                    "reviewed_mechanism": reviewed["reviewed_mechanism"],
                    "evidence": reviewed["evidence"],
                    "l2_eligibility": reviewed["l2_eligibility"],
                    "eligibility_checks": reviewed["eligibility_checks"],
                    "existing_rule_fit": reviewed["existing_rule_fit"],
                    "new_rule_candidate_id": reviewed["new_rule_candidate_id"],
                    "review_notes": reviewed["notes"],
                    "layer_corrected": (
                        machine_outcome != "PASSED"
                        and reviewed["reviewed_layer"] is not None
                        and reviewed["reviewed_layer"] != machine_layer
                    ),
                }
            )

    assert len(cells) == 36
    fails = [c for c in cells if c["machine_outcome"] != "PASSED"]
    assert len(fails) == 15

    reviewed_l2 = [c for c in fails if c["reviewed_layer"] == "L2"]
    elig = Counter(c["l2_eligibility"] for c in reviewed_l2)

    by_model_machine = {
        fam: dict(Counter((c["machine_layer"] or "PASSED") for c in cells if c["model_family"] == fam))
        for fam in ("gemini", "qwen")
    }
    by_model_reviewed = {
        fam: dict(
            Counter((c["reviewed_layer"] or "PASSED") for c in cells if c["model_family"] == fam)
        )
        for fam in ("gemini", "qwen")
    }
    by_condition_reviewed = {
        cond: dict(
            Counter((c["reviewed_layer"] or "PASSED") for c in cells if c["condition"] == cond)
        )
        for cond in ("ab1", "ab2g", "ab2d")
    }

    mechanisms = Counter(c["reviewed_mechanism"] for c in fails)
    cross = {
        "shared_exact_mechanism_across_models": [],
        "related_structural_wrap_family": [
            {
                "family": "single_value_needs_contract_dict_wrap",
                "gemini_subtype": "CORRECT_ANSWER_FLAT_DEGREE_MAP_MISSING_NESTED_COEFFICIENTS",
                "qwen_subtype": "ORACLE_PAYLOAD_BARE_SCALAR_NEEDS_SINGLE_KEY_WRAP",
                "same_task_overlap": False,
                "note": (
                    "Both are structural wrap defects, but loci differ "
                    "(correct_answer vs oracle_payload); not the same subtype on the same task."
                ),
            }
        ],
    }

    new_rules = sorted(
        {
            c["new_rule_candidate_id"]
            for c in fails
            if c["new_rule_candidate_id"] and c["l2_eligibility"] == "eligible_new_rule_candidate"
        }
    )
    existing_eligible = [
        {
            "cell_id": c["cell_id"],
            "task_id": c["task_id"],
            "condition": c["condition"],
            "rule": c["existing_rule_fit"],
            "mechanism": c["reviewed_mechanism"],
        }
        for c in reviewed_l2
        if c["l2_eligibility"] == "eligible_existing_rule"
    ]

    summary = {
        "census_id": "ce115_exam_ext_113_114_combined_census_01",
        "starting_head": _head(),
        "real_model_calls": 0,
        "cells": 36,
        "pass_cells": 21,
        "failure_cells": 15,
        "models": {"gemini": 18, "qwen": 18},
        "machine_pass": {
            "gemini": sum(1 for c in cells if c["model_family"] == "gemini" and c["machine_outcome"] == "PASSED"),
            "qwen": sum(1 for c in cells if c["model_family"] == "qwen" and c["machine_outcome"] == "PASSED"),
        },
        "reviewed_layer_corrections": [
            {
                "cell_id": c["cell_id"],
                "machine_layer": c["machine_layer"],
                "reviewed_layer": c["reviewed_layer"],
                "mechanism": c["reviewed_mechanism"],
            }
            for c in fails
            if c["layer_corrected"]
        ],
        "reviewed_l2_count": len(reviewed_l2),
        "l2_eligibility_census": dict(elig),
        "existing_rule_eligible": existing_eligible,
        "new_rule_candidates": new_rules,
        "ineligible_failures": [
            {
                "cell_id": c["cell_id"],
                "reviewed_layer": c["reviewed_layer"],
                "mechanism": c["reviewed_mechanism"],
                "l2_eligibility": c["l2_eligibility"],
            }
            for c in fails
            if c["l2_eligibility"] == "ineligible"
        ],
        "needs_review": [
            c["cell_id"] for c in fails if c["l2_eligibility"] == "needs_review"
        ],
        "failure_mechanism_counts": dict(mechanisms),
        "by_model_machine_layer": by_model_machine,
        "by_model_reviewed_layer": by_model_reviewed,
        "by_condition_reviewed_layer": by_condition_reviewed,
        "cross_model_subtype_overlap": cross,
        "recommended_next_rule": {
            "priority_1_offline_validate_existing": {
                "rule_id": EXISTING_L2,
                "cells": len(existing_eligible),
                "rationale": (
                    "Three Qwen L2 cells already trigger production allowlist; "
                    "validate repair-to-pass offline before any new rule."
                ),
            },
            "priority_2_new_rule_if_expanding_allowlist": {
                "rule_id": "L2_CORRECT_ANSWER_SINGLE_KEY_WRAP_COEFFICIENTS",
                "cells": 3,
                "rationale": (
                    "Gemini 114-02×3: leaf-correct flat degree map; contract-unique nested wrap; "
                    "NOT implemented this round (correct_answer wrapper was previously banned for production)."
                ),
            },
            "priority_3_payload_restore_family": {
                "rule_ids": [
                    "L2_ORACLE_PAYLOAD_RESTORE_FULL_FROZEN",
                    "L2_ORACLE_PAYLOAD_IDENTITY_RESTORE_FROM_FROZEN",
                ],
                "cells": 2,
                "rationale": "Qwen multi-key / mutated oracle_payload after leaf-correct answers.",
            },
        },
        "constraints": {
            "artifacts_immutable": True,
            "no_healer_changes": True,
            "no_model_runs": True,
            "no_commit": True,
        },
    }

    _write(OUT / "combined_matrix_36.json", cells)
    _write(OUT / "failure_review_15.json", fails)
    _write(
        OUT / "l2_eligibility_audit.json",
        {
            "reviewed_l2_failures": reviewed_l2,
            "census": dict(elig),
            "existing_rule": EXISTING_L2,
        },
    )
    _write(OUT / "summary.json", summary)
    print(json.dumps({k: summary[k] for k in (
        "cells", "failure_cells", "reviewed_l2_count", "l2_eligibility_census",
        "machine_pass", "recommended_next_rule", "real_model_calls"
    )}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
