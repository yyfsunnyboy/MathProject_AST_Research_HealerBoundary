# Qwen Phase 1 interim report

This document is a **Qwen Phase 1 interim report**. Gemini Phase 2 is not completed. No full three-model conclusions are drawn. New seeds are not used for rule development.

Generated programmatically by `scripts/build_math16_qwen_five_seed_interim_report.py` (sample SD = n−1). Not hand-copied.

## Inputs

- h0_seed1: `docs/experiments/results/qwen35_4b_math16_ab123_run_002/cells/*/artifact.json`
- h0_seed1: `docs/experiments/results/qwen35_9b_math16_ab123_run_002/cells/*/artifact.json`
- h0_new_seeds: `docs/experiments/results/qwen35_4b_math16_ab123_run_003_multiseed/seed_*/cells/*/artifact.json`
- h0_new_seeds: `docs/experiments/results/qwen35_9b_math16_ab123_run_003_multiseed/seed_*/cells/*/artifact.json`
- ab3: `docs/experiments/results/math16_qwen_multiseed_ab3_phase1/ab3_report_data.json`
- predictions: `docs/experiments/predictions/math16_qwen_multiseed_predictions.json`

## Model `qwen3.5:4b` (`qwen35_4b`)

### A. Per seed

| seed | PASS/48 | FAIL/48 | row sum | L0 | L1 | L2 | L3 | L4 | L5 | L0 prop | L1 prop | L2 prop | L3 prop | L4 prop | L5 prop |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2026071301 | 6/48 | 42/48 | 48 | 0 | 20 | 0 | 4 | 10 | 8 | 0.0000 | 0.4762 | 0.0000 | 0.0952 | 0.2381 | 0.1905 |
| 2026072001 | 4/48 | 44/48 | 48 | 0 | 17 | 0 | 6 | 8 | 13 | 0.0000 | 0.3864 | 0.0000 | 0.1364 | 0.1818 | 0.2955 |
| 2026072002 | 5/48 | 43/48 | 48 | 0 | 19 | 5 | 5 | 6 | 8 | 0.0000 | 0.4419 | 0.1163 | 0.1163 | 0.1395 | 0.1860 |
| 2026072003 | 6/48 | 42/48 | 48 | 0 | 16 | 3 | 4 | 9 | 10 | 0.0000 | 0.3810 | 0.0714 | 0.0952 | 0.2143 | 0.2381 |
| 2026072004 | 8/48 | 40/48 | 48 | 0 | 18 | 5 | 3 | 7 | 7 | 0.0000 | 0.4500 | 0.1250 | 0.0750 | 0.1750 | 0.1750 |

Proportions are among FAIL cells in that seed. Each row sum PASS+FAIL = 48.

### B. Five-seed pooled and seed-level statistics

- pooled count/proportion (denominator 240): **29/240** = 0.120833
- seed-level mean ± sample SD (n−1) of five seed PASS rates: **0.120833 ± 0.030901**
- pooled proportion and mean ± SD are reported separately (not interchangeable).

### C. Task–condition stability (48 groups × 5 seeds)

- summary: stable_pass=1; stable_fail=34; unstable=13

| task_id | condition | pass_frequency | stability | outcome_consistency | layer_diversity | failure_layer_consistency | outcome_buckets |
|---|---|---:|---|---:|---:|---:|---|
| ce111_nonchoice_q01_part1_exponential_growth | ab1 | 0/5 | stable_fail | False | 2 | False | semantic:4, structural/syntax:1 |
| ce111_nonchoice_q01_part1_exponential_growth | ab2d | 0/5 | stable_fail | False | 3 | False | no-program-structure:1, runtime:1, semantic:3 |
| ce111_nonchoice_q01_part1_exponential_growth | ab2g | 0/5 | stable_fail | False | 2 | False | semantic:4, structural/syntax:1 |
| ce111_q02_polynomial_division_remainder | ab1 | 0/5 | stable_fail | False | 2 | False | semantic:3, structural/syntax:2 |
| ce111_q02_polynomial_division_remainder | ab2d | 0/5 | stable_fail | False | 3 | False | no-program-structure:1, runtime:1, semantic:3 |
| ce111_q02_polynomial_division_remainder | ab2g | 0/5 | stable_fail | False | 2 | False | runtime:2, semantic:3 |
| ce111_q03_prime_factor_selection | ab1 | 1/5 | unstable | False | 3 | False | PASS:1, runtime:1, structural/syntax:3 |
| ce111_q03_prime_factor_selection | ab2d | 2/5 | unstable | False | 3 | False | PASS:2, runtime:1, semantic:1, structural/syntax:1 |
| ce111_q03_prime_factor_selection | ab2g | 0/5 | stable_fail | False | 2 | False | runtime:2, semantic:3 |
| ce111_q05_exact_fraction_expression | ab1 | 0/5 | stable_fail | False | 3 | False | runtime:2, semantic:1, structural/syntax:2 |
| ce111_q05_exact_fraction_expression | ab2d | 0/5 | stable_fail | False | 3 | False | runtime:2, structural/syntax:3 |
| ce111_q05_exact_fraction_expression | ab2g | 0/5 | stable_fail | True | 2 | False | structural/syntax:5 |
| ce111_q08_polynomial_factor_parameter_recovery | ab1 | 1/5 | unstable | False | 3 | False | PASS:1, semantic:2, structural/syntax:2 |
| ce111_q08_polynomial_factor_parameter_recovery | ab2d | 1/5 | unstable | False | 3 | False | PASS:1, no-program-structure:1, runtime:1, semantic:1, structural/syntax:1 |
| ce111_q08_polynomial_factor_parameter_recovery | ab2g | 0/5 | stable_fail | False | 3 | False | runtime:1, semantic:3, structural/syntax:1 |
| ce111_q10_ordered_quadratic_roots_radical | ab1 | 0/5 | stable_fail | False | 2 | False | semantic:4, structural/syntax:1 |
| ce111_q10_ordered_quadratic_roots_radical | ab2d | 0/5 | stable_fail | False | 3 | False | semantic:1, structural/syntax:4 |
| ce111_q10_ordered_quadratic_roots_radical | ab2g | 0/5 | stable_fail | False | 2 | False | runtime:1, structural/syntax:4 |
| ce112_q01_negative_integer_power | ab1 | 5/5 | stable_pass | True | 0 | True | PASS:5 |
| ce112_q01_negative_integer_power | ab2d | 0/5 | stable_fail | False | 2 | False | runtime:4, semantic:1 |
| ce112_q01_negative_integer_power | ab2g | 4/5 | unstable | False | 1 | True | PASS:4, structural/syntax:1 |
| ce112_q04_radical_simplification | ab1 | 0/5 | stable_fail | False | 2 | False | semantic:1, structural/syntax:4 |
| ce112_q04_radical_simplification | ab2d | 0/5 | stable_fail | False | 2 | False | no-program-structure:1, runtime:1, structural/syntax:3 |
| ce112_q04_radical_simplification | ab2g | 0/5 | stable_fail | False | 2 | False | no-program-structure:1, runtime:2, structural/syntax:2 |
| ce112_q09_divisor_multiple_intersection | ab1 | 1/5 | unstable | False | 2 | False | PASS:1, semantic:2, structural/syntax:2 |
| ce112_q09_divisor_multiple_intersection | ab2d | 3/5 | unstable | False | 2 | False | PASS:3, runtime:1, structural/syntax:1 |
| ce112_q09_divisor_multiple_intersection | ab2g | 1/5 | unstable | False | 2 | False | PASS:1, semantic:3, structural/syntax:1 |
| ce112_q12_independent_probability_fraction | ab1 | 0/5 | stable_fail | False | 2 | False | runtime:1, structural/syntax:4 |
| ce112_q12_independent_probability_fraction | ab2d | 0/5 | stable_fail | False | 3 | False | runtime:1, structural/syntax:4 |
| ce112_q12_independent_probability_fraction | ab2g | 0/5 | stable_fail | False | 2 | False | runtime:1, structural/syntax:4 |
| ce113_q01_negative_fraction_subtraction | ab1 | 2/5 | unstable | False | 3 | False | PASS:2, structural/syntax:3 |
| ce113_q01_negative_fraction_subtraction | ab2d | 0/5 | stable_fail | False | 3 | False | no-program-structure:1, runtime:1, structural/syntax:3 |
| ce113_q01_negative_fraction_subtraction | ab2g | 2/5 | unstable | False | 3 | False | PASS:2, structural/syntax:3 |
| ce113_q11_rationalize_denominator | ab1 | 0/5 | stable_fail | False | 2 | False | no-program-structure:2, structural/syntax:3 |
| ce113_q11_rationalize_denominator | ab2d | 0/5 | stable_fail | False | 2 | False | no-program-structure:2, runtime:2, structural/syntax:1 |
| ce113_q11_rationalize_denominator | ab2g | 0/5 | stable_fail | False | 3 | False | no-program-structure:1, runtime:1, semantic:2, structural/syntax:1 |
| ce115_calc_exact_rational_expression_l1 | ab1 | 0/5 | stable_fail | False | 1 | True | no-program-structure:1, structural/syntax:4 |
| ce115_calc_exact_rational_expression_l1 | ab2d | 0/5 | stable_fail | True | 2 | False | structural/syntax:5 |
| ce115_calc_exact_rational_expression_l1 | ab2g | 0/5 | stable_fail | False | 3 | False | no-program-structure:1, runtime:1, structural/syntax:3 |
| ce115_calc_polynomial_division_l1 | ab1 | 0/5 | stable_fail | False | 2 | False | no-program-structure:1, structural/syntax:4 |
| ce115_calc_polynomial_division_l1 | ab2d | 4/5 | unstable | False | 1 | True | PASS:4, runtime:1 |
| ce115_calc_polynomial_division_l1 | ab2g | 0/5 | stable_fail | False | 2 | False | runtime:1, structural/syntax:4 |
| ce115_calc_polynomial_factor_roots_l1 | ab1 | 1/5 | unstable | False | 2 | False | PASS:1, runtime:2, structural/syntax:2 |
| ce115_calc_polynomial_factor_roots_l1 | ab2d | 1/5 | unstable | False | 2 | False | PASS:1, runtime:2, structural/syntax:2 |
| ce115_calc_polynomial_factor_roots_l1 | ab2g | 0/5 | stable_fail | False | 2 | False | no-program-structure:1, structural/syntax:4 |
| ce115_calc_radical_simplification_l1 | ab1 | 0/5 | stable_fail | False | 3 | False | runtime:1, semantic:1, structural/syntax:3 |
| ce115_calc_radical_simplification_l1 | ab2d | 0/5 | stable_fail | False | 2 | False | runtime:2, structural/syntax:3 |
| ce115_calc_radical_simplification_l1 | ab2g | 0/5 | stable_fail | False | 3 | False | no-program-structure:2, structural/syntax:3 |

### D. Prompt-condition comparison

| condition | pooled PASS | pooled rate | seed mean | seed sample SD | FAIL | L0 | L1 | L2 | L3 | L4 | L5 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ab1 | 11/80 | 0.1375 | 0.1375 | 0.0523 | 69/80 | 0 | 26 | 6 | 12 | 7 | 18 |
| ab2g | 7/80 | 0.0875 | 0.0875 | 0.0342 | 73/80 | 0 | 33 | 6 | 4 | 12 | 18 |
| ab2d | 11/80 | 0.1375 | 0.1375 | 0.0815 | 69/80 | 0 | 31 | 1 | 6 | 21 | 10 |

Failure-layer proportions among FAIL for each condition:

- `ab1`: L1:0.3768, L2:0.0870, L3:0.1739, L4:0.1014, L5:0.2609
- `ab2g`: L1:0.4521, L2:0.0822, L3:0.0548, L4:0.1644, L5:0.2466
- `ab2d`: L1:0.4493, L2:0.0145, L3:0.0870, L4:0.3043, L5:0.1449

## Model `qwen3.5:9b` (`qwen35_9b`)

### A. Per seed

| seed | PASS/48 | FAIL/48 | row sum | L0 | L1 | L2 | L3 | L4 | L5 | L0 prop | L1 prop | L2 prop | L3 prop | L4 prop | L5 prop |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2026071301 | 7/48 | 41/48 | 48 | 0 | 15 | 2 | 4 | 5 | 15 | 0.0000 | 0.3659 | 0.0488 | 0.0976 | 0.1220 | 0.3659 |
| 2026072001 | 9/48 | 39/48 | 48 | 0 | 15 | 2 | 6 | 4 | 12 | 0.0000 | 0.3846 | 0.0513 | 0.1538 | 0.1026 | 0.3077 |
| 2026072002 | 6/48 | 42/48 | 48 | 0 | 19 | 1 | 3 | 4 | 15 | 0.0000 | 0.4524 | 0.0238 | 0.0714 | 0.0952 | 0.3571 |
| 2026072003 | 6/48 | 42/48 | 48 | 0 | 26 | 0 | 3 | 2 | 11 | 0.0000 | 0.6190 | 0.0000 | 0.0714 | 0.0476 | 0.2619 |
| 2026072004 | 7/48 | 41/48 | 48 | 0 | 13 | 1 | 7 | 7 | 13 | 0.0000 | 0.3171 | 0.0244 | 0.1707 | 0.1707 | 0.3171 |

Proportions are among FAIL cells in that seed. Each row sum PASS+FAIL = 48.

### B. Five-seed pooled and seed-level statistics

- pooled count/proportion (denominator 240): **35/240** = 0.145833
- seed-level mean ± sample SD (n−1) of five seed PASS rates: **0.145833 ± 0.025516**
- pooled proportion and mean ± SD are reported separately (not interchangeable).

### C. Task–condition stability (48 groups × 5 seeds)

- summary: stable_pass=2; stable_fail=32; unstable=14

| task_id | condition | pass_frequency | stability | outcome_consistency | layer_diversity | failure_layer_consistency | outcome_buckets |
|---|---|---:|---|---:|---:|---:|---|
| ce111_nonchoice_q01_part1_exponential_growth | ab1 | 0/5 | stable_fail | True | 1 | True | semantic:5 |
| ce111_nonchoice_q01_part1_exponential_growth | ab2d | 0/5 | stable_fail | False | 2 | False | semantic:4, structural/syntax:1 |
| ce111_nonchoice_q01_part1_exponential_growth | ab2g | 0/5 | stable_fail | False | 2 | False | no-program-structure:1, semantic:3, structural/syntax:1 |
| ce111_q02_polynomial_division_remainder | ab1 | 0/5 | stable_fail | False | 3 | False | semantic:3, structural/syntax:2 |
| ce111_q02_polynomial_division_remainder | ab2d | 0/5 | stable_fail | False | 3 | False | no-program-structure:1, runtime:1, semantic:2, structural/syntax:1 |
| ce111_q02_polynomial_division_remainder | ab2g | 0/5 | stable_fail | False | 2 | False | semantic:2, structural/syntax:3 |
| ce111_q03_prime_factor_selection | ab1 | 1/5 | unstable | False | 1 | True | PASS:1, semantic:4 |
| ce111_q03_prime_factor_selection | ab2d | 0/5 | stable_fail | False | 2 | False | semantic:4, structural/syntax:1 |
| ce111_q03_prime_factor_selection | ab2g | 3/5 | unstable | False | 2 | False | PASS:3, semantic:1, structural/syntax:1 |
| ce111_q05_exact_fraction_expression | ab1 | 0/5 | stable_fail | True | 3 | False | structural/syntax:5 |
| ce111_q05_exact_fraction_expression | ab2d | 1/5 | unstable | False | 2 | False | PASS:1, no-program-structure:1, runtime:2, structural/syntax:1 |
| ce111_q05_exact_fraction_expression | ab2g | 1/5 | unstable | False | 2 | False | PASS:1, runtime:2, structural/syntax:2 |
| ce111_q08_polynomial_factor_parameter_recovery | ab1 | 0/5 | stable_fail | False | 2 | False | semantic:3, structural/syntax:2 |
| ce111_q08_polynomial_factor_parameter_recovery | ab2d | 0/5 | stable_fail | False | 3 | False | no-program-structure:1, runtime:1, semantic:1, structural/syntax:2 |
| ce111_q08_polynomial_factor_parameter_recovery | ab2g | 0/5 | stable_fail | False | 3 | False | runtime:2, semantic:1, structural/syntax:2 |
| ce111_q10_ordered_quadratic_roots_radical | ab1 | 0/5 | stable_fail | False | 2 | False | semantic:3, structural/syntax:2 |
| ce111_q10_ordered_quadratic_roots_radical | ab2d | 0/5 | stable_fail | False | 2 | False | no-program-structure:1, runtime:1, structural/syntax:3 |
| ce111_q10_ordered_quadratic_roots_radical | ab2g | 0/5 | stable_fail | False | 3 | False | runtime:1, semantic:2, structural/syntax:2 |
| ce112_q01_negative_integer_power | ab1 | 5/5 | stable_pass | True | 0 | True | PASS:5 |
| ce112_q01_negative_integer_power | ab2d | 3/5 | unstable | False | 2 | False | PASS:3, no-program-structure:1, semantic:1 |
| ce112_q01_negative_integer_power | ab2g | 5/5 | stable_pass | True | 0 | True | PASS:5 |
| ce112_q04_radical_simplification | ab1 | 0/5 | stable_fail | False | 2 | False | semantic:3, structural/syntax:2 |
| ce112_q04_radical_simplification | ab2d | 0/5 | stable_fail | True | 1 | True | runtime:5 |
| ce112_q04_radical_simplification | ab2g | 0/5 | stable_fail | False | 3 | False | runtime:1, semantic:2, structural/syntax:2 |
| ce112_q09_divisor_multiple_intersection | ab1 | 1/5 | unstable | False | 1 | True | PASS:1, semantic:4 |
| ce112_q09_divisor_multiple_intersection | ab2d | 2/5 | unstable | False | 1 | True | PASS:2, semantic:3 |
| ce112_q09_divisor_multiple_intersection | ab2g | 3/5 | unstable | False | 2 | False | PASS:3, semantic:1, structural/syntax:1 |
| ce112_q12_independent_probability_fraction | ab1 | 2/5 | unstable | False | 2 | False | PASS:2, structural/syntax:3 |
| ce112_q12_independent_probability_fraction | ab2d | 0/5 | stable_fail | False | 3 | False | runtime:1, structural/syntax:4 |
| ce112_q12_independent_probability_fraction | ab2g | 3/5 | unstable | False | 2 | False | PASS:3, runtime:1, structural/syntax:1 |
| ce113_q01_negative_fraction_subtraction | ab1 | 2/5 | unstable | False | 1 | True | PASS:2, structural/syntax:3 |
| ce113_q01_negative_fraction_subtraction | ab2d | 0/5 | stable_fail | False | 2 | False | runtime:1, structural/syntax:4 |
| ce113_q01_negative_fraction_subtraction | ab2g | 1/5 | unstable | False | 2 | False | PASS:1, structural/syntax:4 |
| ce113_q11_rationalize_denominator | ab1 | 0/5 | stable_fail | True | 1 | True | semantic:5 |
| ce113_q11_rationalize_denominator | ab2d | 0/5 | stable_fail | False | 3 | False | runtime:1, semantic:3, structural/syntax:1 |
| ce113_q11_rationalize_denominator | ab2g | 1/5 | unstable | False | 1 | True | PASS:1, semantic:4 |
| ce115_calc_exact_rational_expression_l1 | ab1 | 0/5 | stable_fail | True | 2 | False | structural/syntax:5 |
| ce115_calc_exact_rational_expression_l1 | ab2d | 0/5 | stable_fail | False | 1 | True | no-program-structure:1, structural/syntax:4 |
| ce115_calc_exact_rational_expression_l1 | ab2g | 0/5 | stable_fail | True | 2 | False | structural/syntax:5 |
| ce115_calc_polynomial_division_l1 | ab1 | 0/5 | stable_fail | False | 3 | False | runtime:1, structural/syntax:4 |
| ce115_calc_polynomial_division_l1 | ab2d | 0/5 | stable_fail | True | 2 | False | structural/syntax:5 |
| ce115_calc_polynomial_division_l1 | ab2g | 0/5 | stable_fail | True | 1 | True | structural/syntax:5 |
| ce115_calc_polynomial_factor_roots_l1 | ab1 | 0/5 | stable_fail | False | 2 | False | no-program-structure:2, structural/syntax:3 |
| ce115_calc_polynomial_factor_roots_l1 | ab2d | 0/5 | stable_fail | False | 1 | True | no-program-structure:1, structural/syntax:4 |
| ce115_calc_polynomial_factor_roots_l1 | ab2g | 0/5 | stable_fail | True | 1 | True | structural/syntax:5 |
| ce115_calc_radical_simplification_l1 | ab1 | 1/5 | unstable | False | 3 | False | PASS:1, semantic:1, structural/syntax:3 |
| ce115_calc_radical_simplification_l1 | ab2d | 0/5 | stable_fail | False | 3 | False | no-program-structure:1, runtime:1, structural/syntax:3 |
| ce115_calc_radical_simplification_l1 | ab2g | 0/5 | stable_fail | False | 2 | False | semantic:1, structural/syntax:4 |

### D. Prompt-condition comparison

| condition | pooled PASS | pooled rate | seed mean | seed sample SD | FAIL | L0 | L1 | L2 | L3 | L4 | L5 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ab1 | 12/80 | 0.1500 | 0.1500 | 0.0559 | 68/80 | 0 | 15 | 5 | 16 | 1 | 31 |
| ab2g | 17/80 | 0.2125 | 0.2125 | 0.0342 | 63/80 | 0 | 34 | 0 | 5 | 7 | 17 |
| ab2d | 6/80 | 0.0750 | 0.0750 | 0.0280 | 74/80 | 0 | 39 | 1 | 2 | 14 | 18 |

Failure-layer proportions among FAIL for each condition:

- `ab1`: L1:0.2206, L2:0.0735, L3:0.2353, L4:0.0147, L5:0.4559
- `ab2g`: L1:0.5397, L3:0.0794, L4:0.1111, L5:0.2698
- `ab2d`: L1:0.5270, L2:0.0135, L3:0.0270, L4:0.1892, L5:0.2432

## E. Frozen Healer seed-generalization (4 new seeds only)

Label: `frozen-rule generalization across unseen generation seeds on the same fixed task set`

This is **not** cross-task held-out generalization.

| metric | value |
|---|---:|
| cells | 384 |
| H0 PASS | 51 |
| H0 FAIL | 333 |
| evaluable FAIL | 333 |
| no_trigger | 325 |
| guarded_abstain | 0 |
| trigger | 8 |
| layer_exposure | 8 |
| rescue_to_pass | 0 |
| regression | 0 |
| excluded | 0 |
| evaluator_failure | 0 |
| identity_reuse (PASS negative control) | 51 |
| outcome sum | 384 |
| trigger / 384 | 0.020833 |
| trigger / H0 FAIL | 0.024024 |
| exposure / trigger | 1.0 |
| rescue / 384 | 0.000000 |
| rescue / H0 FAIL | 0.000000 |
| rescue / trigger | 0.0 |
| regression / H0 PASS | 0.000000 |

## F. Prediction vs actual (192 new cells / model)

Bands are pre-registered tolerance bands, not confidence intervals.

### `qwen35_4b`

| metric | prediction band | actual | status |
|---|---|---|---|
| H0 PASS rate % | [2.5, 22.5] | 11.979167 (23/192) | within band |
| FAIL-share L0 % | [0.0, 15.0] | 0.000000 (0/169) | within band |
| FAIL-share L1 % | [32.61904761904761, 62.61904761904761] | 41.420118 (70/169) | within band |
| FAIL-share L2 % | [0.0, 15.0] | 7.692308 (13/169) | within band |
| FAIL-share L3 % | [0.0, 24.523809523809526] | 10.650888 (18/169) | within band |
| FAIL-share L4 % | [8.809523809523807, 38.80952380952381] | 17.751479 (30/169) | within band |
| FAIL-share L5 % | [4.0476190476190474, 34.04761904761905] | 22.485207 (38/169) | within band |
| trigger_count | [0, 8] | 6 | within band |
| layer_exposure | [0, 8] | 6 | within band |
| rescue_to_pass | [0, 2] | 0 | within band |
| regression | [0, 0] | 0 | within band |

### `qwen35_9b`

| metric | prediction band | actual | status |
|---|---|---|---|
| H0 PASS rate % | [4.583333333333334, 24.583333333333336] | 14.583333 (28/192) | within band |
| FAIL-share L0 % | [0.0, 15.0] | 0.000000 (0/164) | within band |
| FAIL-share L1 % | [21.585365853658537, 51.58536585365854] | 44.512195 (73/164) | within band |
| FAIL-share L2 % | [0.0, 19.878048780487806] | 2.439024 (4/164) | within band |
| FAIL-share L3 % | [0.0, 24.75609756097561] | 11.585366 (19/164) | within band |
| FAIL-share L4 % | [0.0, 27.195121951219512] | 10.365854 (17/164) | within band |
| FAIL-share L5 % | [21.585365853658537, 51.58536585365854] | 31.097561 (51/164) | within band |
| trigger_count | [0, 8] | 2 | within band |
| layer_exposure | [0, 8] | 2 | within band |
| rescue_to_pass | [0, 2] | 0 | within band |
| regression | [0, 0] | 0 | within band |

## G. Protocol and limits

- Gemini Phase 2 is not completed.
- This document is a Qwen Phase 1 interim report.
- Workflow-order deviation: H0 scoring was completed synchronously during generation (same frozen evaluator / classify path as Seed-1 live runner); no separate re-score pass was required.
- Additive runners (`scripts/run_math16_qwen_multiseed_h0.py`, `scripts/run_math16_ab3_multiseed_phase1.py`, `scripts/build_math16_qwen_five_seed_interim_report.py`) did not modify frozen Prompt, evaluator, answer contract, Healer rules, allowlist, priorities, or max_passes.
- run_002 and this round's 384 H0 artifacts are byte-level immutable (verified).
- New seeds were not used for rule development.
- No full three-model conclusions are drawn.

## Assertions

- `cells_per_model_seed_48`: True
- `cells_per_model_240`: True
- `qwen_total_480`: True
- `new_seeds_total_384`: True
- `new_seeds_PASS_51`: True
- `new_seeds_FAIL_333`: True
- `ab3_trigger_8`: True
- `ab3_layer_exposure_8`: True
- `ab3_rescue_0`: True
- `ab3_regression_0`: True
- `ab3_outcome_sum_384`: True
- `run_002_byte_level_unchanged`: True
- `h0_new_384_unchanged_vs_pre_ab3`: True
- `sample_sd_used`: True

## Immutability evidence

```json
{
  "run_002_immutability": {
    "qwen35_4b_math16_ab123_run_002": {
      "artifact_unchanged": true,
      "raw_unchanged": true,
      "artifact_concat_sha256": "8535353e8ad900296d540be112ffcc860ba25632d79aec2da5e23f208cd50fad",
      "raw_concat_sha256": "03eebed6ab12c337eeb4de6d4fa7845a84d0fe2a125e3510bd444466254532d7"
    },
    "qwen35_9b_math16_ab123_run_002": {
      "artifact_unchanged": true,
      "raw_unchanged": true,
      "artifact_concat_sha256": "4b0ef9bd188cdd30eec6db6c285e797837f9e480016e0b412b07435a41c7c267",
      "raw_concat_sha256": "aafe0e30e5084c42fff1884191614c8e2f6bd738af296fde083f4b8b3c754876"
    }
  },
  "h0_new_immutability": {
    "count": 384,
    "pre_ab3_sha256": "6e9f84a06a7d5367454359c42c4b39080a0d9636ffe03716c9cddf9019e29436",
    "current_sha256": "6e9f84a06a7d5367454359c42c4b39080a0d9636ffe03716c9cddf9019e29436",
    "unchanged": true
  }
}
```
