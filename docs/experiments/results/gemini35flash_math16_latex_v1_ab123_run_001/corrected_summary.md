# Corrected Math16 LaTeX v1 Gemini results

- Source run: gemini35flash_math16_latex_v1_ab123_run_001
- Re-evaluation: evaluation_revision_002
- Original evaluator hash: c1f1687e1c7d13127165d9bfed5688f7657efd3ab449c6021d903c18ee3a151d
- Revised evaluator hash: d91389a48fd38283a9e7d6227111af3dfb34649f4621f4f33f4128dc7a72ce11
- Model calls during re-eval: 0
- Original cell artifacts mutated: false

## Treatment PASSED (revised)

- Ab1: 13/16
- Ab2g: 14/16
- Ab2d: 12/16

## Primary PASS changes (exactly 3)

- gemini_3_5_flash__ce115_calc_polynomial_division_l1__ab2d__seed_2026071301: INTRINSIC_SAFETY → PASSED
- gemini_3_5_flash__ce115_calc_polynomial_factor_roots_l1__ab1__seed_2026071301: INTRINSIC_SAFETY → PASSED
- gemini_3_5_flash__ce115_calc_polynomial_factor_roots_l1__ab2g__seed_2026071301: INTRINSIC_SAFETY → PASSED

## Special checks (revised)

{
  "q02": {
    "ab1": "ANSWER_INCORRECT",
    "ab2g": "ANSWER_INCORRECT",
    "ab2d": "ANSWER_INCORRECT"
  },
  "q04": {
    "ab1": "PASSED",
    "ab2g": "PASSED",
    "ab2d": "INTRINSIC_SAFETY"
  },
  "q08": {
    "ab1": "INTRINSIC_SAFETY",
    "ab2g": "INTRINSIC_SAFETY",
    "ab2d": "PASSED"
  },
  "q10": {
    "ab1": "PASSED",
    "ab2g": "PASSED",
    "ab2d": "EXECUTION_FAILURE"
  },
  "q11": {
    "ab1": "PARSE_MINOR",
    "ab2g": "PASSED",
    "ab2d": "PASSED"
  }
}
