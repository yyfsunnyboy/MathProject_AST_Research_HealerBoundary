"""Write final validity adjudication after deep forensic re-exec."""
from __future__ import annotations

import json
from pathlib import Path

RUN = Path(__file__).resolve().parent

adjudication = {
    "run_id": "gemini35flash_math16_latex_v1_ab123_run_001",
    "freeze_commit": "f7439a9a6bad70a70437b71b6afb7938dc7b90d7",
    "integrity": {
        "cells_48_unique": True,
        "api_failure": 0,
        "hashes_match_freeze": True,
        "prompt_hashes_match": True,
        "json_parse_ok": True,
        "itt_no_overwrite": True,
        "healer_attempts": 0,
        "pipeline_correction_applied": 0,
    },
    "treatment_passed": {"ab1": "12/16", "ab2g": "13/16", "ab2d": "11/16"},
    "production_bugs": [
        {
            "bug_id": "MATH16_LATEX_EXACT_STRING_FALSE_NEGATIVE",
            "severity": (
                "Math16 oracles require structural fields AND exact canonical latex string match; "
                "whitespace/formatting variants fail even when math structure is correct."
            ),
            "principle_conflict": (
                "freeze guidance forbids pure string equality replacing structural comparison "
                "for math answers; latex fields currently conjunctively veto structure-correct answers"
            ),
            "affected_cells": [
                {
                    "cell_id": "gemini_3_5_flash__ce115_calc_polynomial_division_l1__ab2d__seed_2026071301",
                    "structural": {
                        "quotient_coefficients": [6, 24],
                        "remainder_coefficients": [102],
                    },
                    "submitted_latex": {
                        "quotient_latex": "6x + 24",
                        "remainder_latex": "102",
                    },
                    "expected_latex": {
                        "quotient_latex": "6x+24",
                        "remainder_latex": "102",
                    },
                    "delta": "spaces around + in quotient_latex only",
                    "validity": "INVALID_EVALUATOR",
                },
                {
                    "cell_id": "gemini_3_5_flash__ce115_calc_polynomial_factor_roots_l1__ab1__seed_2026071301",
                    "structural": {"roots": [-6, 2]},
                    "submitted_latex": {
                        "factorization_latex": "(x + 6)(x - 2)",
                        "roots_latex": "x = -6, 2",
                    },
                    "expected_latex": {
                        "factorization_latex": "(x+6)(x-2)=0",
                        "roots_latex": r"[-6,\,2]",
                    },
                    "delta": "spacing and missing =0 / roots_latex format",
                    "validity": "INVALID_EVALUATOR",
                },
                {
                    "cell_id": "gemini_3_5_flash__ce115_calc_polynomial_factor_roots_l1__ab2g__seed_2026071301",
                    "structural": {"roots": [-6, 2]},
                    "submitted_latex": {
                        "factorization_latex": "(x + 6)(x - 2)",
                        "roots_latex": "-6, 2",
                    },
                    "expected_latex": {
                        "factorization_latex": "(x+6)(x-2)=0",
                        "roots_latex": r"[-6,\,2]",
                    },
                    "delta": "spacing and roots_latex format",
                    "validity": "INVALID_EVALUATOR",
                },
            ],
            "void_recommendation": (
                "Do not commit as clean confirmatory primary ITT. Either (a) fix latex comparison "
                "to normalize whitespace/equivalent forms then rerun only affected task-conditions, "
                "or (b) keep artifacts as historical_with_known_evaluator_false_negatives and exclude "
                "these 3 cells from primary latex-conjunct claims."
            ),
            "scope": (
                "3 cells / single-task-conditions; not automatic full 48-cell void, "
                "but confirmatory commit blocked until adjudicated"
            ),
        },
        {
            "bug_id": "RUNNER_ORACLE_ERROR_FIELD_MISLABEL",
            "severity": (
                "Runner maps any oracle error string (including answer_mismatch / "
                "radical_mismatch / structural_or_latex_mismatch) to INTRINSIC_SAFETY "
                "instead of ANSWER_INCORRECT."
            ),
            "impact": "taxonomy only; pass/fail unchanged",
            "validity": "INVALID_INFRASTRUCTURE",
            "void_recommendation": (
                "Does not void mathematical outcomes; relabel in analysis. "
                "Do not treat as oracle production freeze defect."
            ),
        },
    ],
    "valid_model_failures": [
        {
            "task_id": "ce111_q02_polynomial_division_remainder",
            "conditions": ["ab1", "ab2g", "ab2d"],
            "finding": (
                "All three returned mathematically correct remainder 4x as bare string "
                "correct_answer='4x' instead of required dict {remainder, canonical_latex}. "
                "Common model schema error, not evaluator remainder wiring."
            ),
            "validity": "VALID_MODEL_OUTCOME",
        },
        {
            "task_id": "ce111_q08_polynomial_factor_parameter_recovery",
            "ab1": "returned string '-12' instead of int -12",
            "ab2g": "returned int 28 (wrong)",
            "ab2d": "PASSED",
            "strict_source_template": True,
            "freeze_answer": -12,
            "validity": "VALID_MODEL_OUTCOME",
        },
        {
            "task_id": "ce112_q04_radical_simplification",
            "ab2d": "structure 3/15 correct; canonical_latex wrong",
            "validity": "VALID_MODEL_OUTCOME",
        },
        {
            "task_id": "ce113_q11_rationalize_denominator",
            "ab1": "PARSE_MINOR f-string brace error",
            "ab2g_ab2d": "PASSED",
            "reuse_policy_rerun_ok": True,
            "validity": "VALID_MODEL_OUTCOME",
        },
        {
            "task_id": "ce115_calc_polynomial_factor_roots_l1",
            "ab2d": "EXECUTION_FAILURE unpack arity misuse of factor API",
            "validity": "VALID_MODEL_OUTCOME",
        },
        {
            "task_id": "ce111_q10_ordered_quadratic_roots_radical",
            "ab2d": "EXECUTION_FAILURE Fraction JSON serialize / non-int rational",
            "ab1_ab2g": "PASSED",
            "compound_signed_coeffs_freeze_ok": True,
            "validity": "VALID_MODEL_OUTCOME",
        },
    ],
    "special_checks": {
        "q02": "common model schema error (bare string); NOT shared evaluator remainder bug",
        "q08": "strict_source_template in prompts; freeze -12; ab2d passed; ab1 type; ab2g wrong 28",
        "q10": "freeze +1/-1 verified; nested ok; ab1/ab2g passed; ab2d Fraction/runtime",
        "q12": "substantial_abstraction retained; all three PASSED",
        "q11": "reuse_policy=rerun; this run only; no v2 mix-in",
    },
    "paired_summary_from_raw_status": {
        "note": "paired ranks use recorded evaluator_status; 3 INVALID_EVALUATOR cells distort Ab2d/Ab1 comparisons",
        "Ab1_to_Ab2g_improved": ["ce113_q11_rationalize_denominator"],
        "Ab1_to_Ab2d_improved": [
            "ce111_q08_polynomial_factor_parameter_recovery",
            "ce113_q11_rationalize_denominator",
        ],
        "Ab1_to_Ab2d_regressed_raw": [
            "ce111_q10_ordered_quadratic_roots_radical",
            "ce112_q04_radical_simplification",
            "ce115_calc_polynomial_division_l1",
            "ce115_calc_polynomial_factor_roots_l1",
        ],
        "Ab1_to_Ab2d_regressed_after_excluding_invalid_evaluator": [
            "ce111_q10_ordered_quadratic_roots_radical",
            "ce112_q04_radical_simplification",
            "ce115_calc_polynomial_factor_roots_l1",
        ],
    },
    "commit_allowed": False,
    "commit_block_reason": (
        "INVALID_EVALUATOR false negatives on 3 cells "
        "(structure-correct, latex-string-only mismatch). "
        "Formal confirmatory commit blocked per production-bug stop rule."
    ),
}

(RUN / "validity_report.json").write_text(
    json.dumps(adjudication, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)

extra = """

## FINAL ADJUDICATION (deep forensic re-exec)

**commit_allowed: false**

### Production bug: latex exact-string false negatives
Structure-correct answers rejected solely due to latex string exact match:

1. `ce115_calc_polynomial_division_l1` Ab2d — coeffs correct; `6x + 24` vs `6x+24`
2. `ce115_calc_polynomial_factor_roots_l1` Ab1 — roots correct; factorization/roots latex format differs
3. `ce115_calc_polynomial_factor_roots_l1` Ab2g — same

Validity: `INVALID_EVALUATOR` for these 3 cells.

### q02 (all three ANSWER_INCORRECT)
Re-exec shows `correct_answer = \"4x\"` (bare string). Math remainder is correct; required schema is `{remainder, canonical_latex}`.
Verdict: **common model schema error**, not polynomial normalization/evaluator remainder wiring.

### Other non-PASSED
- q08 Ab1: `\"-12\"` string vs int `-12` (model type); Ab2g: `28` wrong; Ab2d PASSED; strict template OK
- q04 Ab2d: structure OK, latex wrong
- q11 Ab1: parse/f-string error; Ab2g/Ab2d PASSED; rerun-only OK
- factor_roots Ab2d: model unpack/API misuse EXECUTION_FAILURE
- q10 Ab2d: Fraction JSON serialize / type issue; Ab1/Ab2g PASSED; +/- compound freeze OK
- q12: all PASSED; substantial_abstraction retained

### Recommendation
Do **not** commit as clean confirmatory primary results. Keep artifacts. Fix latex comparison (normalize or score structure primary) then selective rerun of affected task-conditions, or publish only with explicit exclusion of the 3 false-negative cells.
"""

md_path = RUN / "analysis_summary.md"
md_path.write_text(md_path.read_text(encoding="utf-8") + extra, encoding="utf-8")

# forensic supplement with re-exec facts
supp = {
    "q02_reexec": {
        "ab1_ab2g_ab2d_correct_answer": "4x",
        "schema_required": {"remainder": "4x", "canonical_latex": "4x"},
        "verdict": "common_model_schema_error",
    },
    "invalid_evaluator_reexec": adjudication["production_bugs"][0]["affected_cells"],
}
(RUN / "forensic_reexec_supplement.json").write_text(
    json.dumps(supp, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)

print(
    json.dumps(
        {
            "commit_allowed": False,
            "invalid_evaluator_cells": 3,
            "block": adjudication["commit_block_reason"],
        },
        ensure_ascii=False,
        indent=2,
    )
)
