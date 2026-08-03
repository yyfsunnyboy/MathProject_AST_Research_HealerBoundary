# Answer assembly provenance audit

> **ARCHIVE NOTICE**
> - 資料來源主要為 V1 FAIL（V2 480-cell 正式重跑前）
> - 此批候選不得直接用於設計 V2 Healer 規則
> - 狀態：PENDING_V2_RESIDUAL_EVIDENCE
> - 下一個 gate：V2 480-cell 正式重跑完成後重新 census

Generated: 2026-08-03T05:35:49.969653+00:00
Baseline commit: `f0fbf4a0c2131f03a1bb9096a15d462f27e9b5d4`

## Definition (applied)

Provenance is limited to def-use chains from:
1. full-plan specified API return values;
2. prompt-allowed indexing/unpacking/sorting/normalization;
3. frozen fields explicitly allowed in correct_answer.

Violations: unsourced literals, wrong API fields, alternative algorithms, nonexistent kwargs, broken chains.
Ambiguous multi-source paths marked AMBIGUOUS (not guessed).

## Answer assembly provenance feasibility table

| task_id | condition | machine_checkable | healer_detection | healer_repair | feasibility |
|---|---|---|---|---|---|
| ce115_calc_polynomial_division_l1 | ab2d_full_v2 | partial | none | none | NOT_FEASIBLE_IN_CURRENT_HEALER |
| ce115_calc_polynomial_factor_roots_l1 | ab2d_full_v2 | partial | none | none | NOT_FEASIBLE_IN_CURRENT_HEALER |
| ce115_calc_exact_rational_expression_l1 | ab2d_full_v2 | partial | none | none | NOT_FEASIBLE_IN_CURRENT_HEALER |
| ce115_calc_radical_simplification_l1 | ab2d_full_v2 | partial | none | none | NOT_FEASIBLE_IN_CURRENT_HEALER |
| ce111_q02_polynomial_division_remainder | ab2d_full_v2 | partial | none | none | NOT_FEASIBLE_IN_CURRENT_HEALER |
| ce111_q08_polynomial_factor_parameter_recovery | ab2d_full_v2 | partial | none | none | NOT_FEASIBLE_IN_CURRENT_HEALER |
| ce111_q03_prime_factor_selection | ab2d_full_v2 | partial | none | none | NOT_FEASIBLE_IN_CURRENT_HEALER |
| ce112_q01_negative_integer_power | ab2d_full_v2 | partial | none | none | NOT_FEASIBLE_IN_CURRENT_HEALER |
| ce112_q09_divisor_multiple_intersection | ab2d_full_v2 | partial | none | none | NOT_FEASIBLE_IN_CURRENT_HEALER |
| ce111_nonchoice_q01_part1_exponential_growth | ab2d_full_v2 | partial | none | none | NOT_FEASIBLE_IN_CURRENT_HEALER |
| ce111_q05_exact_fraction_expression | ab2d_full_v2 | partial | none | none | NOT_FEASIBLE_IN_CURRENT_HEALER |
| ce113_q01_negative_fraction_subtraction | ab2d_full_v2 | partial | none | none | NOT_FEASIBLE_IN_CURRENT_HEALER |
| ce112_q12_independent_probability_fraction | ab2d_full_v2 | partial | none | none | NOT_FEASIBLE_IN_CURRENT_HEALER |
| ce112_q04_radical_simplification | ab2d_full_v2 | partial | none | none | NOT_FEASIBLE_IN_CURRENT_HEALER |
| ce111_q10_ordered_quadratic_roots_radical | ab2d_full_v2 | partial | none | none | NOT_FEASIBLE_IN_CURRENT_HEALER |
| ce113_q11_rationalize_denominator | ab2d_full_v2 | partial | none | none | NOT_FEASIBLE_IN_CURRENT_HEALER |

## Verdict

- **No existing Healer** performs AST def-use provenance tracing for `correct_answer` assembly.
- **L2_CORRECT_ANSWER_JSON_DUMPS_UNWRAP** addresses JSON double-encoding only — not provenance.
- Full-plan provenance enforcement would require new **detection-only or abstain** machinery (Prompt-Contract Healer v2 candidate scope).

