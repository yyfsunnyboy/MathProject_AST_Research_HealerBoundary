# 🕵️ CE115 Corrected Context Formal Run Summary Report

This report summarizes the execution of the full 72-cell cohort run under the corrected budget configurations: `num_ctx = 65536` and `num_predict = 24576` with `think: false`.

---

## 1. Summary of Execution Metrics

- **Planned Cells**: 72
- **Executed Cells**: 72
- **Unique Cell IDs**: 72
- **NATURAL_COMPLETE**: 50
- **CONFIGURATION_LIMIT_REACHED**: 0
- **MODEL_DEGENERATIVE_NONTERMINATION**: 22
- **MODEL_EARLY_INCOMPLETE_TERMINATION**: 0
- **RUNTIME_FAILURE**: 0
- **Telemetry Completeness**: 72 / 72

---

## 2. Exceptions & Degenerations

A total of **22** cells exhibited budget limit hits or runtime failures:
- **CONFIGURATION_LIMIT_REACHED**: 0 cells
- **MODEL_DEGENERATIVE_NONTERMINATION**: 22 cells
- **RUNTIME_FAILURE**: 0 cells

All exceptions have been cataloged in `ce115_corrected_context_formal_run_exception_report.json` for forensic evaluation.

---

## 3. Detailed Results Matrix

| Cell ID | Model | Condition | Prompt Tokens (In) | Output Tokens (Out) | Total Tokens | Classification |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab1__seed_2026071301` | `qwen3.5:4b` | `ab1` | 453 | 1292 | 1745 | `NATURAL_COMPLETE` |
| `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab1__seed_2026071302` | `qwen3.5:4b` | `ab1` | 453 | 24576 | 25029 | `MODEL_DEGENERATIVE_NONTERMINATION` |
| `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab1__seed_2026071303` | `qwen3.5:4b` | `ab1` | 454 | 24576 | 25030 | `MODEL_DEGENERATIVE_NONTERMINATION` |
| `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2g__seed_2026071301` | `qwen3.5:4b` | `ab2g` | 579 | 24576 | 25155 | `MODEL_DEGENERATIVE_NONTERMINATION` |
| `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2g__seed_2026071302` | `qwen3.5:4b` | `ab2g` | 579 | 24576 | 25155 | `MODEL_DEGENERATIVE_NONTERMINATION` |
| `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2g__seed_2026071303` | `qwen3.5:4b` | `ab2g` | 580 | 517 | 1097 | `NATURAL_COMPLETE` |
| `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d__seed_2026071301` | `qwen3.5:4b` | `ab2d` | 630 | 24576 | 25206 | `MODEL_DEGENERATIVE_NONTERMINATION` |
| `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d__seed_2026071302` | `qwen3.5:4b` | `ab2d` | 630 | 24576 | 25206 | `MODEL_DEGENERATIVE_NONTERMINATION` |
| `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d__seed_2026071303` | `qwen3.5:4b` | `ab2d` | 631 | 321 | 952 | `NATURAL_COMPLETE` |
| `qwen3_5_4b__ce115_calc_exact_rational_expression_l1__ab1__seed_2026071301` | `qwen3.5:4b` | `ab1` | 489 | 2334 | 2823 | `NATURAL_COMPLETE` |
| `qwen3_5_4b__ce115_calc_exact_rational_expression_l1__ab1__seed_2026071302` | `qwen3.5:4b` | `ab1` | 489 | 1087 | 1576 | `NATURAL_COMPLETE` |
| `qwen3_5_4b__ce115_calc_exact_rational_expression_l1__ab1__seed_2026071303` | `qwen3.5:4b` | `ab1` | 489 | 838 | 1327 | `NATURAL_COMPLETE` |
| `qwen3_5_4b__ce115_calc_exact_rational_expression_l1__ab2g__seed_2026071301` | `qwen3.5:4b` | `ab2g` | 615 | 3002 | 3617 | `MODEL_DEGENERATIVE_NONTERMINATION` |
| `qwen3_5_4b__ce115_calc_exact_rational_expression_l1__ab2g__seed_2026071302` | `qwen3.5:4b` | `ab2g` | 615 | 1263 | 1878 | `NATURAL_COMPLETE` |
| `qwen3_5_4b__ce115_calc_exact_rational_expression_l1__ab2g__seed_2026071303` | `qwen3.5:4b` | `ab2g` | 615 | 24576 | 25191 | `MODEL_DEGENERATIVE_NONTERMINATION` |
| `qwen3_5_4b__ce115_calc_exact_rational_expression_l1__ab2d__seed_2026071301` | `qwen3.5:4b` | `ab2d` | 663 | 569 | 1232 | `NATURAL_COMPLETE` |
| `qwen3_5_4b__ce115_calc_exact_rational_expression_l1__ab2d__seed_2026071302` | `qwen3.5:4b` | `ab2d` | 663 | 2646 | 3309 | `NATURAL_COMPLETE` |
| `qwen3_5_4b__ce115_calc_exact_rational_expression_l1__ab2d__seed_2026071303` | `qwen3.5:4b` | `ab2d` | 663 | 690 | 1353 | `NATURAL_COMPLETE` |
| `qwen3_5_4b__ce115_calc_polynomial_division_l1__ab1__seed_2026071301` | `qwen3.5:4b` | `ab1` | 515 | 122 | 637 | `NATURAL_COMPLETE` |
| `qwen3_5_4b__ce115_calc_polynomial_division_l1__ab1__seed_2026071302` | `qwen3.5:4b` | `ab1` | 515 | 121 | 636 | `NATURAL_COMPLETE` |
| `qwen3_5_4b__ce115_calc_polynomial_division_l1__ab1__seed_2026071303` | `qwen3.5:4b` | `ab1` | 515 | 121 | 636 | `NATURAL_COMPLETE` |
| `qwen3_5_4b__ce115_calc_polynomial_division_l1__ab2g__seed_2026071301` | `qwen3.5:4b` | `ab2g` | 641 | 126 | 767 | `NATURAL_COMPLETE` |
| `qwen3_5_4b__ce115_calc_polynomial_division_l1__ab2g__seed_2026071302` | `qwen3.5:4b` | `ab2g` | 641 | 129 | 770 | `NATURAL_COMPLETE` |
| `qwen3_5_4b__ce115_calc_polynomial_division_l1__ab2g__seed_2026071303` | `qwen3.5:4b` | `ab2g` | 641 | 120 | 761 | `NATURAL_COMPLETE` |
| `qwen3_5_4b__ce115_calc_polynomial_division_l1__ab2d__seed_2026071301` | `qwen3.5:4b` | `ab2d` | 696 | 117 | 813 | `NATURAL_COMPLETE` |
| `qwen3_5_4b__ce115_calc_polynomial_division_l1__ab2d__seed_2026071302` | `qwen3.5:4b` | `ab2d` | 696 | 129 | 825 | `NATURAL_COMPLETE` |
| `qwen3_5_4b__ce115_calc_polynomial_division_l1__ab2d__seed_2026071303` | `qwen3.5:4b` | `ab2d` | 696 | 120 | 816 | `NATURAL_COMPLETE` |
| `qwen3_5_4b__ce115_calc_polynomial_factor_roots_l1__ab1__seed_2026071301` | `qwen3.5:4b` | `ab1` | 449 | 81 | 530 | `NATURAL_COMPLETE` |
| `qwen3_5_4b__ce115_calc_polynomial_factor_roots_l1__ab1__seed_2026071302` | `qwen3.5:4b` | `ab1` | 449 | 71 | 520 | `NATURAL_COMPLETE` |
| `qwen3_5_4b__ce115_calc_polynomial_factor_roots_l1__ab1__seed_2026071303` | `qwen3.5:4b` | `ab1` | 448 | 70 | 518 | `NATURAL_COMPLETE` |
| `qwen3_5_4b__ce115_calc_polynomial_factor_roots_l1__ab2g__seed_2026071301` | `qwen3.5:4b` | `ab2g` | 575 | 84 | 659 | `NATURAL_COMPLETE` |
| `qwen3_5_4b__ce115_calc_polynomial_factor_roots_l1__ab2g__seed_2026071302` | `qwen3.5:4b` | `ab2g` | 575 | 92 | 667 | `NATURAL_COMPLETE` |
| `qwen3_5_4b__ce115_calc_polynomial_factor_roots_l1__ab2g__seed_2026071303` | `qwen3.5:4b` | `ab2g` | 574 | 99 | 673 | `NATURAL_COMPLETE` |
| `qwen3_5_4b__ce115_calc_polynomial_factor_roots_l1__ab2d__seed_2026071301` | `qwen3.5:4b` | `ab2d` | 626 | 84 | 710 | `NATURAL_COMPLETE` |
| `qwen3_5_4b__ce115_calc_polynomial_factor_roots_l1__ab2d__seed_2026071302` | `qwen3.5:4b` | `ab2d` | 626 | 99 | 725 | `NATURAL_COMPLETE` |
| `qwen3_5_4b__ce115_calc_polynomial_factor_roots_l1__ab2d__seed_2026071303` | `qwen3.5:4b` | `ab2d` | 625 | 98 | 723 | `NATURAL_COMPLETE` |
| `qwen3_5_9b__ce115_calc_radical_simplification_l1__ab1__seed_2026071301` | `qwen3.5:9b` | `ab1` | 453 | 300 | 753 | `NATURAL_COMPLETE` |
| `qwen3_5_9b__ce115_calc_radical_simplification_l1__ab1__seed_2026071302` | `qwen3.5:9b` | `ab1` | 453 | 249 | 702 | `NATURAL_COMPLETE` |
| `qwen3_5_9b__ce115_calc_radical_simplification_l1__ab1__seed_2026071303` | `qwen3.5:9b` | `ab1` | 454 | 865 | 1319 | `MODEL_DEGENERATIVE_NONTERMINATION` |
| `qwen3_5_9b__ce115_calc_radical_simplification_l1__ab2g__seed_2026071301` | `qwen3.5:9b` | `ab2g` | 579 | 490 | 1069 | `MODEL_DEGENERATIVE_NONTERMINATION` |
| `qwen3_5_9b__ce115_calc_radical_simplification_l1__ab2g__seed_2026071302` | `qwen3.5:9b` | `ab2g` | 579 | 2571 | 3150 | `NATURAL_COMPLETE` |
| `qwen3_5_9b__ce115_calc_radical_simplification_l1__ab2g__seed_2026071303` | `qwen3.5:9b` | `ab2g` | 580 | 310 | 890 | `NATURAL_COMPLETE` |
| `qwen3_5_9b__ce115_calc_radical_simplification_l1__ab2d__seed_2026071301` | `qwen3.5:9b` | `ab2d` | 630 | 291 | 921 | `NATURAL_COMPLETE` |
| `qwen3_5_9b__ce115_calc_radical_simplification_l1__ab2d__seed_2026071302` | `qwen3.5:9b` | `ab2d` | 630 | 398 | 1028 | `NATURAL_COMPLETE` |
| `qwen3_5_9b__ce115_calc_radical_simplification_l1__ab2d__seed_2026071303` | `qwen3.5:9b` | `ab2d` | 631 | 1317 | 1948 | `NATURAL_COMPLETE` |
| `qwen3_5_9b__ce115_calc_exact_rational_expression_l1__ab1__seed_2026071301` | `qwen3.5:9b` | `ab1` | 489 | 567 | 1056 | `NATURAL_COMPLETE` |
| `qwen3_5_9b__ce115_calc_exact_rational_expression_l1__ab1__seed_2026071302` | `qwen3.5:9b` | `ab1` | 489 | 4044 | 4533 | `MODEL_DEGENERATIVE_NONTERMINATION` |
| `qwen3_5_9b__ce115_calc_exact_rational_expression_l1__ab1__seed_2026071303` | `qwen3.5:9b` | `ab1` | 489 | 1196 | 1685 | `NATURAL_COMPLETE` |
| `qwen3_5_9b__ce115_calc_exact_rational_expression_l1__ab2g__seed_2026071301` | `qwen3.5:9b` | `ab2g` | 615 | 1468 | 2083 | `NATURAL_COMPLETE` |
| `qwen3_5_9b__ce115_calc_exact_rational_expression_l1__ab2g__seed_2026071302` | `qwen3.5:9b` | `ab2g` | 615 | 670 | 1285 | `NATURAL_COMPLETE` |
| `qwen3_5_9b__ce115_calc_exact_rational_expression_l1__ab2g__seed_2026071303` | `qwen3.5:9b` | `ab2g` | 615 | 2354 | 2969 | `NATURAL_COMPLETE` |
| `qwen3_5_9b__ce115_calc_exact_rational_expression_l1__ab2d__seed_2026071301` | `qwen3.5:9b` | `ab2d` | 663 | 24576 | 25239 | `MODEL_DEGENERATIVE_NONTERMINATION` |
| `qwen3_5_9b__ce115_calc_exact_rational_expression_l1__ab2d__seed_2026071302` | `qwen3.5:9b` | `ab2d` | 663 | 24576 | 25239 | `MODEL_DEGENERATIVE_NONTERMINATION` |
| `qwen3_5_9b__ce115_calc_exact_rational_expression_l1__ab2d__seed_2026071303` | `qwen3.5:9b` | `ab2d` | 663 | 613 | 1276 | `NATURAL_COMPLETE` |
| `qwen3_5_9b__ce115_calc_polynomial_division_l1__ab1__seed_2026071301` | `qwen3.5:9b` | `ab1` | 515 | 1600 | 2115 | `NATURAL_COMPLETE` |
| `qwen3_5_9b__ce115_calc_polynomial_division_l1__ab1__seed_2026071302` | `qwen3.5:9b` | `ab1` | 515 | 24576 | 25091 | `MODEL_DEGENERATIVE_NONTERMINATION` |
| `qwen3_5_9b__ce115_calc_polynomial_division_l1__ab1__seed_2026071303` | `qwen3.5:9b` | `ab1` | 515 | 24576 | 25091 | `MODEL_DEGENERATIVE_NONTERMINATION` |
| `qwen3_5_9b__ce115_calc_polynomial_division_l1__ab2g__seed_2026071301` | `qwen3.5:9b` | `ab2g` | 641 | 24576 | 25217 | `MODEL_DEGENERATIVE_NONTERMINATION` |
| `qwen3_5_9b__ce115_calc_polynomial_division_l1__ab2g__seed_2026071302` | `qwen3.5:9b` | `ab2g` | 641 | 24576 | 25217 | `MODEL_DEGENERATIVE_NONTERMINATION` |
| `qwen3_5_9b__ce115_calc_polynomial_division_l1__ab2g__seed_2026071303` | `qwen3.5:9b` | `ab2g` | 641 | 24576 | 25217 | `MODEL_DEGENERATIVE_NONTERMINATION` |
| `qwen3_5_9b__ce115_calc_polynomial_division_l1__ab2d__seed_2026071301` | `qwen3.5:9b` | `ab2d` | 696 | 24576 | 25272 | `MODEL_DEGENERATIVE_NONTERMINATION` |
| `qwen3_5_9b__ce115_calc_polynomial_division_l1__ab2d__seed_2026071302` | `qwen3.5:9b` | `ab2d` | 696 | 733 | 1429 | `NATURAL_COMPLETE` |
| `qwen3_5_9b__ce115_calc_polynomial_division_l1__ab2d__seed_2026071303` | `qwen3.5:9b` | `ab2d` | 696 | 541 | 1237 | `NATURAL_COMPLETE` |
| `qwen3_5_9b__ce115_calc_polynomial_factor_roots_l1__ab1__seed_2026071301` | `qwen3.5:9b` | `ab1` | 449 | 606 | 1055 | `NATURAL_COMPLETE` |
| `qwen3_5_9b__ce115_calc_polynomial_factor_roots_l1__ab1__seed_2026071302` | `qwen3.5:9b` | `ab1` | 449 | 1561 | 2010 | `MODEL_DEGENERATIVE_NONTERMINATION` |
| `qwen3_5_9b__ce115_calc_polynomial_factor_roots_l1__ab1__seed_2026071303` | `qwen3.5:9b` | `ab1` | 448 | 458 | 906 | `NATURAL_COMPLETE` |
| `qwen3_5_9b__ce115_calc_polynomial_factor_roots_l1__ab2g__seed_2026071301` | `qwen3.5:9b` | `ab2g` | 575 | 996 | 1571 | `NATURAL_COMPLETE` |
| `qwen3_5_9b__ce115_calc_polynomial_factor_roots_l1__ab2g__seed_2026071302` | `qwen3.5:9b` | `ab2g` | 575 | 2824 | 3399 | `MODEL_DEGENERATIVE_NONTERMINATION` |
| `qwen3_5_9b__ce115_calc_polynomial_factor_roots_l1__ab2g__seed_2026071303` | `qwen3.5:9b` | `ab2g` | 574 | 3021 | 3595 | `MODEL_DEGENERATIVE_NONTERMINATION` |
| `qwen3_5_9b__ce115_calc_polynomial_factor_roots_l1__ab2d__seed_2026071301` | `qwen3.5:9b` | `ab2d` | 626 | 1439 | 2065 | `NATURAL_COMPLETE` |
| `qwen3_5_9b__ce115_calc_polynomial_factor_roots_l1__ab2d__seed_2026071302` | `qwen3.5:9b` | `ab2d` | 626 | 1452 | 2078 | `NATURAL_COMPLETE` |
| `qwen3_5_9b__ce115_calc_polynomial_factor_roots_l1__ab2d__seed_2026071303` | `qwen3.5:9b` | `ab2d` | 625 | 1311 | 1936 | `NATURAL_COMPLETE` |

