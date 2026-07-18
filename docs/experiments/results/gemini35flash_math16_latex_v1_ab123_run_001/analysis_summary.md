# Math16 Gemini 48-cell analysis
- run_id: `gemini35flash_math16_latex_v1_ab123_run_001`
- commit_allowed: **True**
- integrity hashes match: True; prompt hashes match: True

## Treatment × outcome
```json
{
  "ab1": {
    "PASSED": 12,
    "ANSWER_INCORRECT": 1,
    "INTRINSIC_SAFETY": 2,
    "PARSE_MINOR": 1
  },
  "ab2d": {
    "PASSED": 11,
    "ANSWER_INCORRECT": 1,
    "EXECUTION_FAILURE": 2,
    "INTRINSIC_SAFETY": 2
  },
  "ab2g": {
    "PASSED": 13,
    "ANSWER_INCORRECT": 1,
    "INTRINSIC_SAFETY": 2
  }
}
```

## Paired comparisons
### Ab1->Ab2g
- improved: ['ce113_q11_rationalize_denominator']
- regressed: []
- unchanged: ['ce111_nonchoice_q01_part1_exponential_growth', 'ce111_q02_polynomial_division_remainder', 'ce111_q03_prime_factor_selection', 'ce111_q05_exact_fraction_expression', 'ce111_q08_polynomial_factor_parameter_recovery', 'ce111_q10_ordered_quadratic_roots_radical', 'ce112_q01_negative_integer_power', 'ce112_q04_radical_simplification', 'ce112_q09_divisor_multiple_intersection', 'ce112_q12_independent_probability_fraction', 'ce113_q01_negative_fraction_subtraction', 'ce115_calc_exact_rational_expression_l1', 'ce115_calc_polynomial_division_l1', 'ce115_calc_polynomial_factor_roots_l1', 'ce115_calc_radical_simplification_l1']
### Ab1->Ab2d
- improved: ['ce111_q08_polynomial_factor_parameter_recovery', 'ce113_q11_rationalize_denominator']
- regressed: ['ce111_q10_ordered_quadratic_roots_radical', 'ce112_q04_radical_simplification', 'ce115_calc_polynomial_division_l1', 'ce115_calc_polynomial_factor_roots_l1']
- unchanged: ['ce111_nonchoice_q01_part1_exponential_growth', 'ce111_q02_polynomial_division_remainder', 'ce111_q03_prime_factor_selection', 'ce111_q05_exact_fraction_expression', 'ce112_q01_negative_integer_power', 'ce112_q09_divisor_multiple_intersection', 'ce112_q12_independent_probability_fraction', 'ce113_q01_negative_fraction_subtraction', 'ce115_calc_exact_rational_expression_l1', 'ce115_calc_radical_simplification_l1']
### Ab2g->Ab2d
- improved: ['ce111_q08_polynomial_factor_parameter_recovery']
- regressed: ['ce111_q10_ordered_quadratic_roots_radical', 'ce112_q04_radical_simplification', 'ce115_calc_polynomial_division_l1', 'ce115_calc_polynomial_factor_roots_l1']
- unchanged: ['ce111_nonchoice_q01_part1_exponential_growth', 'ce111_q02_polynomial_division_remainder', 'ce111_q03_prime_factor_selection', 'ce111_q05_exact_fraction_expression', 'ce112_q01_negative_integer_power', 'ce112_q09_divisor_multiple_intersection', 'ce112_q12_independent_probability_fraction', 'ce113_q01_negative_fraction_subtraction', 'ce113_q11_rationalize_denominator', 'ce115_calc_exact_rational_expression_l1', 'ce115_calc_radical_simplification_l1']

## Validity
- counts: {'VALID_MODEL_OUTCOME': 42, 'NEEDS_REVIEW': 6}
- production_bug_cells: 0
- needs_review_cells: 6

## Special
- q02 verdict: common_model_error
- q08 correct_answer freeze: -12
- q10 coeffs +/-: 1/-1
- q12 transformation_level: substantial_abstraction
- q11 reuse_policy: rerun

## Non-PASSED forensics (short)
- `gemini_3_5_flash__ce111_q02_polynomial_division_remainder__ab1__seed_2026071301`: ANSWER_INCORRECT | validity=VALID_MODEL_OUTCOME | suspicion=common_model_error | submitted=None | err=None
- `gemini_3_5_flash__ce111_q02_polynomial_division_remainder__ab2d__seed_2026071301`: ANSWER_INCORRECT | validity=VALID_MODEL_OUTCOME | suspicion=common_model_error | submitted=None | err=None
- `gemini_3_5_flash__ce111_q02_polynomial_division_remainder__ab2g__seed_2026071301`: ANSWER_INCORRECT | validity=VALID_MODEL_OUTCOME | suspicion=common_model_error | submitted=None | err=None
- `gemini_3_5_flash__ce111_q08_polynomial_factor_parameter_recovery__ab1__seed_2026071301`: INTRINSIC_SAFETY | validity=NEEDS_REVIEW | suspicion=model_or_oracle_payload | submitted=None | err='answer_mismatch'
- `gemini_3_5_flash__ce111_q08_polynomial_factor_parameter_recovery__ab2g__seed_2026071301`: INTRINSIC_SAFETY | validity=NEEDS_REVIEW | suspicion=model_or_oracle_payload | submitted=None | err='answer_mismatch'
- `gemini_3_5_flash__ce111_q10_ordered_quadratic_roots_radical__ab2d__seed_2026071301`: EXECUTION_FAILURE | validity=VALID_MODEL_OUTCOME | suspicion=model_codegen_runtime | submitted=None | err='TypeError: Object of type Fraction is not JSON serializable'
- `gemini_3_5_flash__ce112_q04_radical_simplification__ab2d__seed_2026071301`: INTRINSIC_SAFETY | validity=NEEDS_REVIEW | suspicion=model_or_oracle_payload | submitted=None | err='radical_mismatch'
- `gemini_3_5_flash__ce113_q11_rationalize_denominator__ab1__seed_2026071301`: PARSE_MINOR | validity=VALID_MODEL_OUTCOME | suspicion=model_codegen_syntax | submitted=None | err="f-string: single '}' is not allowed (<unknown>, line 18)"
- `gemini_3_5_flash__ce115_calc_polynomial_division_l1__ab2d__seed_2026071301`: INTRINSIC_SAFETY | validity=NEEDS_REVIEW | suspicion=model_or_oracle_payload | submitted=None | err='structural_or_latex_mismatch'
- `gemini_3_5_flash__ce115_calc_polynomial_factor_roots_l1__ab1__seed_2026071301`: INTRINSIC_SAFETY | validity=NEEDS_REVIEW | suspicion=model_or_oracle_payload | submitted=None | err='structural_or_latex_mismatch'
- `gemini_3_5_flash__ce115_calc_polynomial_factor_roots_l1__ab2d__seed_2026071301`: EXECUTION_FAILURE | validity=VALID_MODEL_OUTCOME | suspicion=model_codegen_runtime | submitted=None | err='ValueError: not enough values to unpack (expected 3, got 2)'
- `gemini_3_5_flash__ce115_calc_polynomial_factor_roots_l1__ab2g__seed_2026071301`: INTRINSIC_SAFETY | validity=NEEDS_REVIEW | suspicion=model_or_oracle_payload | submitted=None | err='structural_or_latex_mismatch'


## FINAL ADJUDICATION (deep forensic re-exec)

**commit_allowed: false**

### Production bug: latex exact-string false negatives
Structure-correct answers rejected solely due to latex string exact match:

1. `ce115_calc_polynomial_division_l1` Ab2d — coeffs correct; `6x + 24` vs `6x+24`
2. `ce115_calc_polynomial_factor_roots_l1` Ab1 — roots correct; factorization/roots latex format differs
3. `ce115_calc_polynomial_factor_roots_l1` Ab2g — same

Validity: `INVALID_EVALUATOR` for these 3 cells.

### q02 (all three ANSWER_INCORRECT)
Re-exec shows `correct_answer = "4x"` (bare string). Math remainder is correct; required schema is `{remainder, canonical_latex}`.
Verdict: **common model schema error**, not polynomial normalization/evaluator remainder wiring.

### Other non-PASSED
- q08 Ab1: `"-12"` string vs int `-12` (model type); Ab2g: `28` wrong; Ab2d PASSED; strict template OK
- q04 Ab2d: structure OK, latex wrong
- q11 Ab1: parse/f-string error; Ab2g/Ab2d PASSED; rerun-only OK
- factor_roots Ab2d: model unpack/API misuse EXECUTION_FAILURE
- q10 Ab2d: Fraction JSON serialize / type issue; Ab1/Ab2g PASSED; +/- compound freeze OK
- q12: all PASSED; substantial_abstraction retained

### Recommendation
Do **not** commit as clean confirmatory primary results. Keep artifacts. Fix latex comparison (normalize or score structure primary) then selective rerun of affected task-conditions, or publish only with explicit exclusion of the 3 false-negative cells.
