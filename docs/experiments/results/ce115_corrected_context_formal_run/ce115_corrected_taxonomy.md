# 🕵️ CE115 Corrected Failure Taxonomy Report

This report presents the structural and semantic failure taxonomy rebuild for the corrected 72-cell cohort run.

---

## 1. Summary of Primary Failure Families

| Primary Failure Family | Count |
| :--- | :---: |
| `MODEL_DEGENERATIVE_NONTERMINATION` | 22 |
| `OUTPUT_WRAPPING_OR_LEAKAGE` | 6 |
| `PARSE_OR_SYNTAX_FAILURE` | 0 |
| `ENTRY_POINT_OR_CONTRACT_FAILURE` | 3 |
| `CORE_LOGIC_INCORRECT` | 19 |
| `CORE_LOGIC_MISSING` | 13 |
| `SPECIFICATION_MISINTERPRETATION` | 0 |
| `NONCORE_STRUCTURAL_FAILURE` | 0 |
| `OTHER` | 0 |
| `INSUFFICIENT_EVIDENCE` | 0 |

---

## 2. Failed Cells Classification Matrix

| Cell ID | Primary Failure Family | Root Cause | Potential Repairability |
| :--- | :--- | :--- | :--- |
| `qwen3_5_4b__ce115_calc_exact_rational_expression_l1__ab1__seed_2026071301` | `OUTPUT_WRAPPING_OR_LEAKAGE` | `INLINE_REASONING_LEAK` | `regex_strip_leak` |
| `qwen3_5_4b__ce115_calc_exact_rational_expression_l1__ab1__seed_2026071302` | `CORE_LOGIC_INCORRECT` | `CODE_DEFECT` | `ast_repair_or_abstain` |
| `qwen3_5_4b__ce115_calc_exact_rational_expression_l1__ab1__seed_2026071303` | `CORE_LOGIC_MISSING` | `CODE_DEFECT` | `ast_repair_or_abstain` |
| `qwen3_5_4b__ce115_calc_exact_rational_expression_l1__ab2d__seed_2026071301` | `CORE_LOGIC_MISSING` | `CODE_DEFECT` | `ast_repair_or_abstain` |
| `qwen3_5_4b__ce115_calc_exact_rational_expression_l1__ab2d__seed_2026071302` | `OUTPUT_WRAPPING_OR_LEAKAGE` | `INLINE_REASONING_LEAK` | `regex_strip_leak` |
| `qwen3_5_4b__ce115_calc_exact_rational_expression_l1__ab2d__seed_2026071303` | `ENTRY_POINT_OR_CONTRACT_FAILURE` | `CODE_DEFECT` | `ast_repair_or_abstain` |
| `qwen3_5_4b__ce115_calc_exact_rational_expression_l1__ab2g__seed_2026071301` | `MODEL_DEGENERATIVE_NONTERMINATION` | `DEGENERATIVE_LOOP` | `ast_repair_or_abstain` |
| `qwen3_5_4b__ce115_calc_exact_rational_expression_l1__ab2g__seed_2026071302` | `CORE_LOGIC_INCORRECT` | `INLINE_REASONING_LEAK` | `ast_repair_or_abstain` |
| `qwen3_5_4b__ce115_calc_exact_rational_expression_l1__ab2g__seed_2026071303` | `MODEL_DEGENERATIVE_NONTERMINATION` | `DEGENERATIVE_LOOP` | `ast_repair_or_abstain` |
| `qwen3_5_4b__ce115_calc_polynomial_division_l1__ab1__seed_2026071301` | `CORE_LOGIC_INCORRECT` | `CODE_DEFECT` | `ast_repair_or_abstain` |
| `qwen3_5_4b__ce115_calc_polynomial_division_l1__ab1__seed_2026071302` | `CORE_LOGIC_INCORRECT` | `CODE_DEFECT` | `ast_repair_or_abstain` |
| `qwen3_5_4b__ce115_calc_polynomial_division_l1__ab1__seed_2026071303` | `CORE_LOGIC_INCORRECT` | `CODE_DEFECT` | `ast_repair_or_abstain` |
| `qwen3_5_4b__ce115_calc_polynomial_division_l1__ab2d__seed_2026071301` | `CORE_LOGIC_INCORRECT` | `CODE_DEFECT` | `ast_repair_or_abstain` |
| `qwen3_5_4b__ce115_calc_polynomial_division_l1__ab2d__seed_2026071302` | `CORE_LOGIC_INCORRECT` | `CODE_DEFECT` | `ast_repair_or_abstain` |
| `qwen3_5_4b__ce115_calc_polynomial_division_l1__ab2d__seed_2026071303` | `CORE_LOGIC_INCORRECT` | `CODE_DEFECT` | `ast_repair_or_abstain` |
| `qwen3_5_4b__ce115_calc_polynomial_division_l1__ab2g__seed_2026071301` | `CORE_LOGIC_INCORRECT` | `CODE_DEFECT` | `ast_repair_or_abstain` |
| `qwen3_5_4b__ce115_calc_polynomial_division_l1__ab2g__seed_2026071302` | `CORE_LOGIC_INCORRECT` | `CODE_DEFECT` | `ast_repair_or_abstain` |
| `qwen3_5_4b__ce115_calc_polynomial_division_l1__ab2g__seed_2026071303` | `CORE_LOGIC_INCORRECT` | `CODE_DEFECT` | `ast_repair_or_abstain` |
| `qwen3_5_4b__ce115_calc_polynomial_factor_roots_l1__ab1__seed_2026071302` | `CORE_LOGIC_INCORRECT` | `CODE_DEFECT` | `ast_repair_or_abstain` |
| `qwen3_5_4b__ce115_calc_polynomial_factor_roots_l1__ab1__seed_2026071303` | `CORE_LOGIC_INCORRECT` | `CODE_DEFECT` | `ast_repair_or_abstain` |
| `qwen3_5_4b__ce115_calc_polynomial_factor_roots_l1__ab2d__seed_2026071302` | `CORE_LOGIC_INCORRECT` | `CODE_DEFECT` | `ast_repair_or_abstain` |
| `qwen3_5_4b__ce115_calc_polynomial_factor_roots_l1__ab2d__seed_2026071303` | `CORE_LOGIC_INCORRECT` | `CODE_DEFECT` | `ast_repair_or_abstain` |
| `qwen3_5_4b__ce115_calc_polynomial_factor_roots_l1__ab2g__seed_2026071303` | `CORE_LOGIC_INCORRECT` | `CODE_DEFECT` | `ast_repair_or_abstain` |
| `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab1__seed_2026071301` | `OUTPUT_WRAPPING_OR_LEAKAGE` | `INLINE_REASONING_LEAK` | `regex_strip_leak` |
| `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab1__seed_2026071302` | `MODEL_DEGENERATIVE_NONTERMINATION` | `DEGENERATIVE_LOOP` | `ast_repair_or_abstain` |
| `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab1__seed_2026071303` | `MODEL_DEGENERATIVE_NONTERMINATION` | `DEGENERATIVE_LOOP` | `ast_repair_or_abstain` |
| `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d__seed_2026071301` | `MODEL_DEGENERATIVE_NONTERMINATION` | `DEGENERATIVE_LOOP` | `ast_repair_or_abstain` |
| `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d__seed_2026071302` | `MODEL_DEGENERATIVE_NONTERMINATION` | `DEGENERATIVE_LOOP` | `ast_repair_or_abstain` |
| `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d__seed_2026071303` | `CORE_LOGIC_INCORRECT` | `CODE_DEFECT` | `ast_repair_or_abstain` |
| `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2g__seed_2026071301` | `MODEL_DEGENERATIVE_NONTERMINATION` | `DEGENERATIVE_LOOP` | `ast_repair_or_abstain` |
| `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2g__seed_2026071302` | `MODEL_DEGENERATIVE_NONTERMINATION` | `DEGENERATIVE_LOOP` | `ast_repair_or_abstain` |
| `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2g__seed_2026071303` | `CORE_LOGIC_MISSING` | `CODE_DEFECT` | `ast_repair_or_abstain` |
| `qwen3_5_9b__ce115_calc_exact_rational_expression_l1__ab1__seed_2026071301` | `ENTRY_POINT_OR_CONTRACT_FAILURE` | `INLINE_REASONING_LEAK` | `ast_repair_or_abstain` |
| `qwen3_5_9b__ce115_calc_exact_rational_expression_l1__ab1__seed_2026071302` | `MODEL_DEGENERATIVE_NONTERMINATION` | `DEGENERATIVE_LOOP` | `ast_repair_or_abstain` |
| `qwen3_5_9b__ce115_calc_exact_rational_expression_l1__ab1__seed_2026071303` | `CORE_LOGIC_MISSING` | `CODE_DEFECT` | `ast_repair_or_abstain` |
| `qwen3_5_9b__ce115_calc_exact_rational_expression_l1__ab2d__seed_2026071301` | `MODEL_DEGENERATIVE_NONTERMINATION` | `DEGENERATIVE_LOOP` | `ast_repair_or_abstain` |
| `qwen3_5_9b__ce115_calc_exact_rational_expression_l1__ab2d__seed_2026071302` | `MODEL_DEGENERATIVE_NONTERMINATION` | `DEGENERATIVE_LOOP` | `ast_repair_or_abstain` |
| `qwen3_5_9b__ce115_calc_exact_rational_expression_l1__ab2d__seed_2026071303` | `ENTRY_POINT_OR_CONTRACT_FAILURE` | `CODE_DEFECT` | `ast_repair_or_abstain` |
| `qwen3_5_9b__ce115_calc_exact_rational_expression_l1__ab2g__seed_2026071301` | `CORE_LOGIC_MISSING` | `INLINE_REASONING_LEAK` | `ast_repair_or_abstain` |
| `qwen3_5_9b__ce115_calc_exact_rational_expression_l1__ab2g__seed_2026071302` | `CORE_LOGIC_MISSING` | `INLINE_REASONING_LEAK` | `ast_repair_or_abstain` |
| `qwen3_5_9b__ce115_calc_exact_rational_expression_l1__ab2g__seed_2026071303` | `OUTPUT_WRAPPING_OR_LEAKAGE` | `INLINE_REASONING_LEAK` | `regex_strip_leak` |
| `qwen3_5_9b__ce115_calc_polynomial_division_l1__ab1__seed_2026071301` | `OUTPUT_WRAPPING_OR_LEAKAGE` | `INLINE_REASONING_LEAK` | `regex_strip_leak` |
| `qwen3_5_9b__ce115_calc_polynomial_division_l1__ab1__seed_2026071302` | `MODEL_DEGENERATIVE_NONTERMINATION` | `DEGENERATIVE_LOOP` | `ast_repair_or_abstain` |
| `qwen3_5_9b__ce115_calc_polynomial_division_l1__ab1__seed_2026071303` | `MODEL_DEGENERATIVE_NONTERMINATION` | `DEGENERATIVE_LOOP` | `ast_repair_or_abstain` |
| `qwen3_5_9b__ce115_calc_polynomial_division_l1__ab2d__seed_2026071301` | `MODEL_DEGENERATIVE_NONTERMINATION` | `DEGENERATIVE_LOOP` | `ast_repair_or_abstain` |
| `qwen3_5_9b__ce115_calc_polynomial_division_l1__ab2d__seed_2026071302` | `CORE_LOGIC_MISSING` | `CODE_DEFECT` | `ast_repair_or_abstain` |
| `qwen3_5_9b__ce115_calc_polynomial_division_l1__ab2d__seed_2026071303` | `CORE_LOGIC_MISSING` | `CODE_DEFECT` | `ast_repair_or_abstain` |
| `qwen3_5_9b__ce115_calc_polynomial_division_l1__ab2g__seed_2026071301` | `MODEL_DEGENERATIVE_NONTERMINATION` | `DEGENERATIVE_LOOP` | `safe_prefix_extraction` |
| `qwen3_5_9b__ce115_calc_polynomial_division_l1__ab2g__seed_2026071302` | `MODEL_DEGENERATIVE_NONTERMINATION` | `DEGENERATIVE_LOOP` | `safe_prefix_extraction` |
| `qwen3_5_9b__ce115_calc_polynomial_division_l1__ab2g__seed_2026071303` | `MODEL_DEGENERATIVE_NONTERMINATION` | `DEGENERATIVE_LOOP` | `ast_repair_or_abstain` |
| `qwen3_5_9b__ce115_calc_polynomial_factor_roots_l1__ab1__seed_2026071301` | `CORE_LOGIC_MISSING` | `CODE_DEFECT` | `ast_repair_or_abstain` |
| `qwen3_5_9b__ce115_calc_polynomial_factor_roots_l1__ab1__seed_2026071302` | `MODEL_DEGENERATIVE_NONTERMINATION` | `DEGENERATIVE_LOOP` | `safe_prefix_extraction` |
| `qwen3_5_9b__ce115_calc_polynomial_factor_roots_l1__ab2d__seed_2026071301` | `CORE_LOGIC_INCORRECT` | `INLINE_REASONING_LEAK` | `ast_repair_or_abstain` |
| `qwen3_5_9b__ce115_calc_polynomial_factor_roots_l1__ab2d__seed_2026071302` | `CORE_LOGIC_MISSING` | `CODE_DEFECT` | `ast_repair_or_abstain` |
| `qwen3_5_9b__ce115_calc_polynomial_factor_roots_l1__ab2d__seed_2026071303` | `CORE_LOGIC_MISSING` | `CODE_DEFECT` | `ast_repair_or_abstain` |
| `qwen3_5_9b__ce115_calc_polynomial_factor_roots_l1__ab2g__seed_2026071301` | `CORE_LOGIC_INCORRECT` | `INLINE_REASONING_LEAK` | `ast_repair_or_abstain` |
| `qwen3_5_9b__ce115_calc_polynomial_factor_roots_l1__ab2g__seed_2026071302` | `MODEL_DEGENERATIVE_NONTERMINATION` | `DEGENERATIVE_LOOP` | `ast_repair_or_abstain` |
| `qwen3_5_9b__ce115_calc_polynomial_factor_roots_l1__ab2g__seed_2026071303` | `MODEL_DEGENERATIVE_NONTERMINATION` | `DEGENERATIVE_LOOP` | `ast_repair_or_abstain` |
| `qwen3_5_9b__ce115_calc_radical_simplification_l1__ab1__seed_2026071303` | `MODEL_DEGENERATIVE_NONTERMINATION` | `DEGENERATIVE_LOOP` | `safe_prefix_extraction` |
| `qwen3_5_9b__ce115_calc_radical_simplification_l1__ab2d__seed_2026071301` | `CORE_LOGIC_MISSING` | `CODE_DEFECT` | `ast_repair_or_abstain` |
| `qwen3_5_9b__ce115_calc_radical_simplification_l1__ab2g__seed_2026071301` | `MODEL_DEGENERATIVE_NONTERMINATION` | `DEGENERATIVE_LOOP` | `safe_prefix_extraction` |
| `qwen3_5_9b__ce115_calc_radical_simplification_l1__ab2g__seed_2026071302` | `OUTPUT_WRAPPING_OR_LEAKAGE` | `INLINE_REASONING_LEAK` | `regex_strip_leak` |
| `qwen3_5_9b__ce115_calc_radical_simplification_l1__ab2g__seed_2026071303` | `CORE_LOGIC_MISSING` | `CODE_DEFECT` | `ast_repair_or_abstain` |

