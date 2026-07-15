# CE115 answer_incorrect forensic (16 cells)

## Summary counts

- cases: **16**
- TRUE_ANSWER_ERROR: **16**
- EQUIVALENCE_FALSE_NEGATIVE: **0**
- CHECKER_OR_NORMALIZATION_BUG: **0**
- EXECUTION_OR_EXTRACTION_MISCLASSIFIED: **0**
- INSUFFICIENT_EVIDENCE: **0**
- found 1/4↔0.25-style FN signal: **False**
- pipeline-corrected ledger recommended: **False**

## Distribution of the 16

- by model: `{'qwen3.5:4b': 16}`
- by condition: `{'ab1': 6, 'ab2d': 6, 'ab2g': 4}`
- by task: `{'ce115_calc_exact_rational_expression_l1': 2, 'ce115_calc_polynomial_division_l1': 9, 'ce115_calc_polynomial_factor_roots_l1': 4, 'ce115_calc_radical_simplification_l1': 1}`

## Gate funnel

```json
{
  "by_model": {
    "qwen3.5:4b": {
      "n_cells": 36,
      "g1_pass": "30 / 36",
      "g2_assessed": "30 / 36",
      "g2_pass": "24 / 30",
      "g3_assessed": "24 / 36",
      "g3_pass": "21 / 24",
      "g4_assessed": "21 / 36",
      "g4_pass": "5 / 21",
      "g4_fail": "16 / 21",
      "answer_incorrect_over_g4_assessed": "16 / 21",
      "answer_incorrect_over_n": "16 / 36"
    },
    "qwen3.5:9b": {
      "n_cells": 36,
      "g1_pass": "17 / 36",
      "g2_assessed": "17 / 36",
      "g2_pass": "9 / 17",
      "g3_assessed": "9 / 36",
      "g3_pass": "4 / 9",
      "g4_assessed": "4 / 36",
      "g4_pass": "4 / 4",
      "g4_fail": "0 / 4",
      "answer_incorrect_over_g4_assessed": "0 / 4",
      "answer_incorrect_over_n": "0 / 36"
    }
  },
  "by_condition": {
    "ab1": {
      "n_cells": 24,
      "g1_pass": "13 / 24",
      "g2_assessed": "13 / 24",
      "g2_pass": "11 / 13",
      "g3_assessed": "11 / 24",
      "g3_pass": "10 / 11",
      "g4_assessed": "10 / 24",
      "g4_pass": "4 / 10",
      "g4_fail": "6 / 10",
      "answer_incorrect_over_g4_assessed": "6 / 10",
      "answer_incorrect_over_n": "6 / 24"
    },
    "ab2d": {
      "n_cells": 24,
      "g1_pass": "17 / 24",
      "g2_assessed": "17 / 24",
      "g2_pass": "13 / 17",
      "g3_assessed": "13 / 24",
      "g3_pass": "9 / 13",
      "g4_assessed": "9 / 24",
      "g4_pass": "3 / 9",
      "g4_fail": "6 / 9",
      "answer_incorrect_over_g4_assessed": "6 / 9",
      "answer_incorrect_over_n": "6 / 24"
    },
    "ab2g": {
      "n_cells": 24,
      "g1_pass": "17 / 24",
      "g2_assessed": "17 / 24",
      "g2_pass": "9 / 17",
      "g3_assessed": "9 / 24",
      "g3_pass": "6 / 9",
      "g4_assessed": "6 / 24",
      "g4_pass": "2 / 6",
      "g4_fail": "4 / 6",
      "answer_incorrect_over_g4_assessed": "4 / 6",
      "answer_incorrect_over_n": "4 / 24"
    }
  },
  "overall": {
    "n_cells": 72,
    "g1_pass": "47 / 72",
    "g2_assessed": "47 / 72",
    "g2_pass": "33 / 47",
    "g3_assessed": "33 / 72",
    "g3_pass": "25 / 33",
    "g4_assessed": "25 / 72",
    "g4_pass": "9 / 25",
    "g4_fail": "16 / 25",
    "answer_incorrect_over_g4_assessed": "16 / 25",
    "answer_incorrect_over_n": "16 / 72"
  }
}
```

## Per-cell

### `qwen3_5_4b__ce115_calc_exact_rational_expression_l1__ab1__seed_2026071302`

- class: **TRUE_ANSWER_ERROR**
- model/condition/task/seed: qwen3.5:4b / ab1 / ce115_calc_exact_rational_expression_l1 / 2026071302
- expected: `{"value": "448"}`
- submitted: `{"value": "10976/25"}`
- independent: `{"equivalent": false, "reason": "rational_not_equal", "normalized_expected": "448", "normalized_submitted": "10976/25"}`
- discrepancy: rational_not_equal

### `qwen3_5_4b__ce115_calc_exact_rational_expression_l1__ab2d__seed_2026071303`

- class: **TRUE_ANSWER_ERROR**
- model/condition/task/seed: qwen3.5:4b / ab2d / ce115_calc_exact_rational_expression_l1 / 2026071303
- expected: `{"value": "471"}`
- submitted: `{"value": "298531716353748013173465754999193/633825300114114700748351602688"}`
- independent: `{"equivalent": false, "reason": "rational_not_equal", "normalized_expected": "471", "normalized_submitted": "298531716353748013173465754999193/633825300114114700748351602688"}`
- discrepancy: rational_not_equal

### `qwen3_5_4b__ce115_calc_polynomial_division_l1__ab1__seed_2026071301`

- class: **TRUE_ANSWER_ERROR**
- model/condition/task/seed: qwen3.5:4b / ab1 / ce115_calc_polynomial_division_l1 / 2026071301
- expected: `{"quotient_coefficients": [6, 24], "remainder_coefficients": [102]}`
- submitted: `{"quotient_coefficients": [1.5, 1], "remainder_coefficients": [-9]}`
- independent: `{"equivalent": false, "reason": "poly_div_not_equal", "quotient_equal": false, "remainder_equal": false}`
- discrepancy: poly_div_not_equal

### `qwen3_5_4b__ce115_calc_polynomial_division_l1__ab1__seed_2026071302`

- class: **TRUE_ANSWER_ERROR**
- model/condition/task/seed: qwen3.5:4b / ab1 / ce115_calc_polynomial_division_l1 / 2026071302
- expected: `{"quotient_coefficients": [-6, -16], "remainder_coefficients": [-29]}`
- submitted: `{"quotient_coefficients": [0, 1], "remainder_coefficients": [8]}`
- independent: `{"equivalent": false, "reason": "poly_div_not_equal", "quotient_equal": false, "remainder_equal": false}`
- discrepancy: poly_div_not_equal

### `qwen3_5_4b__ce115_calc_polynomial_division_l1__ab1__seed_2026071303`

- class: **TRUE_ANSWER_ERROR**
- model/condition/task/seed: qwen3.5:4b / ab1 / ce115_calc_polynomial_division_l1 / 2026071303
- expected: `{"quotient_coefficients": [-7, 18], "remainder_coefficients": [-37]}`
- submitted: `{"quotient_coefficients": [3, -5], "remainder_coefficients": [9]}`
- independent: `{"equivalent": false, "reason": "poly_div_not_equal", "quotient_equal": false, "remainder_equal": false}`
- discrepancy: poly_div_not_equal

### `qwen3_5_4b__ce115_calc_polynomial_division_l1__ab2d__seed_2026071301`

- class: **TRUE_ANSWER_ERROR**
- model/condition/task/seed: qwen3.5:4b / ab2d / ce115_calc_polynomial_division_l1 / 2026071301
- expected: `{"quotient_coefficients": [6, 24], "remainder_coefficients": [102]}`
- submitted: `{"quotient_coefficients": [-2, 3], "remainder_coefficients": [18]}`
- independent: `{"equivalent": false, "reason": "poly_div_not_equal", "quotient_equal": false, "remainder_equal": false}`
- discrepancy: poly_div_not_equal

### `qwen3_5_4b__ce115_calc_polynomial_division_l1__ab2d__seed_2026071302`

- class: **TRUE_ANSWER_ERROR**
- model/condition/task/seed: qwen3.5:4b / ab2d / ce115_calc_polynomial_division_l1 / 2026071302
- expected: `{"quotient_coefficients": [-6, -16], "remainder_coefficients": [-29]}`
- submitted: `{"quotient_coefficients": ["-5/1", "-7"], "remainder_coefficients": [0]}`
- independent: `{"equivalent": false, "reason": "poly_div_not_equal", "quotient_equal": false, "remainder_equal": false}`
- discrepancy: poly_div_not_equal

### `qwen3_5_4b__ce115_calc_polynomial_division_l1__ab2d__seed_2026071303`

- class: **TRUE_ANSWER_ERROR**
- model/condition/task/seed: qwen3.5:4b / ab2d / ce115_calc_polynomial_division_l1 / 2026071303
- expected: `{"quotient_coefficients": [-7, 18], "remainder_coefficients": [-37]}`
- submitted: `{"quotient_coefficients": ["-3", "-5/6"], "remainder_coefficients": ["8"]}`
- independent: `{"equivalent": false, "reason": "poly_div_not_equal", "quotient_equal": false, "remainder_equal": false}`
- discrepancy: poly_div_not_equal

### `qwen3_5_4b__ce115_calc_polynomial_division_l1__ab2g__seed_2026071301`

- class: **TRUE_ANSWER_ERROR**
- model/condition/task/seed: qwen3.5:4b / ab2g / ce115_calc_polynomial_division_l1 / 2026071301
- expected: `{"quotient_coefficients": [6, 24], "remainder_coefficients": [102]}`
- submitted: `{"quotient_coefficients": [-2, 3], "remainder_coefficients": [18]}`
- independent: `{"equivalent": false, "reason": "poly_div_not_equal", "quotient_equal": false, "remainder_equal": false}`
- discrepancy: poly_div_not_equal

### `qwen3_5_4b__ce115_calc_polynomial_division_l1__ab2g__seed_2026071302`

- class: **TRUE_ANSWER_ERROR**
- model/condition/task/seed: qwen3.5:4b / ab2g / ce115_calc_polynomial_division_l1 / 2026071302
- expected: `{"quotient_coefficients": [-6, -16], "remainder_coefficients": [-29]}`
- submitted: `{"quotient_coefficients": ["-3", "-5/2"], "remainder_coefficients": [9]}`
- independent: `{"equivalent": false, "reason": "poly_div_not_equal", "quotient_equal": false, "remainder_equal": false}`
- discrepancy: poly_div_not_equal

### `qwen3_5_4b__ce115_calc_polynomial_division_l1__ab2g__seed_2026071303`

- class: **TRUE_ANSWER_ERROR**
- model/condition/task/seed: qwen3.5:4b / ab2g / ce115_calc_polynomial_division_l1 / 2026071303
- expected: `{"quotient_coefficients": [-7, 18], "remainder_coefficients": [-37]}`
- submitted: `{"quotient_coefficients": ["-3", "-5/6"], "remainder_coefficients": ["8"]}`
- independent: `{"equivalent": false, "reason": "poly_div_not_equal", "quotient_equal": false, "remainder_equal": false}`
- discrepancy: poly_div_not_equal

### `qwen3_5_4b__ce115_calc_polynomial_factor_roots_l1__ab1__seed_2026071302`

- class: **TRUE_ANSWER_ERROR**
- model/condition/task/seed: qwen3.5:4b / ab1 / ce115_calc_polynomial_factor_roots_l1 / 2026071302
- expected: `{"roots": [-3, 3]}`
- submitted: `{"roots": [3, -6]}`
- independent: `{"equivalent": false, "reason": "root_set_not_equal"}`
- discrepancy: root_set_not_equal

### `qwen3_5_4b__ce115_calc_polynomial_factor_roots_l1__ab1__seed_2026071303`

- class: **TRUE_ANSWER_ERROR**
- model/condition/task/seed: qwen3.5:4b / ab1 / ce115_calc_polynomial_factor_roots_l1 / 2026071303
- expected: `{"roots": [1, 2]}`
- submitted: `{"roots": [2, 3]}`
- independent: `{"equivalent": false, "reason": "root_set_not_equal"}`
- discrepancy: root_set_not_equal

### `qwen3_5_4b__ce115_calc_polynomial_factor_roots_l1__ab2d__seed_2026071303`

- class: **TRUE_ANSWER_ERROR**
- model/condition/task/seed: qwen3.5:4b / ab2d / ce115_calc_polynomial_factor_roots_l1 / 2026071303
- expected: `{"roots": [1, 2]}`
- submitted: `{"roots": [1.0]}`
- independent: `{"equivalent": false, "reason": "root_set_not_equal"}`
- discrepancy: root_set_not_equal

### `qwen3_5_4b__ce115_calc_polynomial_factor_roots_l1__ab2g__seed_2026071303`

- class: **TRUE_ANSWER_ERROR**
- model/condition/task/seed: qwen3.5:4b / ab2g / ce115_calc_polynomial_factor_roots_l1 / 2026071303
- expected: `{"roots": [1, 2]}`
- submitted: `{"roots": [1.0]}`
- independent: `{"equivalent": false, "reason": "root_set_not_equal"}`
- discrepancy: root_set_not_equal

### `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d__seed_2026071303`

- class: **TRUE_ANSWER_ERROR**
- model/condition/task/seed: qwen3.5:4b / ab2d / ce115_calc_radical_simplification_l1 / 2026071303
- expected: `{"coefficient": 4, "radicand": 7}`
- submitted: `{"coefficient": [4, 1], "radicand": 7}`
- independent: `{"equivalent": false, "reason": "radical_pair_not_equal"}`
- discrepancy: radical_pair_not_equal

