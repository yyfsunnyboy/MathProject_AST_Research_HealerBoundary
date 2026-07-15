# 🧬 CE115 Corrected Healer Candidate Pool Report

This report catalogs the potential heuristic healer rules and candidates identified from the corrected cohort run.

---

## 1. Summary of Governance Tiers

- **SAFE_HISTORICAL_CANDIDATE**: 11
- **MINIMAL_CORE_CANDIDATE**: 0
- **EXPLORATORY_ONLY**: 0
- **ABSTAIN**: 52
- **INSUFFICIENT_EVIDENCE**: 0

---

## 2. Healer Candidate Registry

| Candidate ID | Failure Family | Proposed Repair Level | Preliminary Governance Tier |
| :--- | :--- | :--- | :--- |
| `cand_qwen3_5_4b__ce115_calc_exact_rational_expression_l1__ab1__seed_2026071301` | `OUTPUT_WRAPPING_OR_LEAKAGE` | `display` | `SAFE_HISTORICAL_CANDIDATE` |
| `cand_qwen3_5_4b__ce115_calc_exact_rational_expression_l1__ab1__seed_2026071302` | `CORE_LOGIC_INCORRECT` | `ast` | `ABSTAIN` |
| `cand_qwen3_5_4b__ce115_calc_exact_rational_expression_l1__ab1__seed_2026071303` | `CORE_LOGIC_MISSING` | `ast` | `ABSTAIN` |
| `cand_qwen3_5_4b__ce115_calc_exact_rational_expression_l1__ab2d__seed_2026071301` | `CORE_LOGIC_MISSING` | `ast` | `ABSTAIN` |
| `cand_qwen3_5_4b__ce115_calc_exact_rational_expression_l1__ab2d__seed_2026071302` | `OUTPUT_WRAPPING_OR_LEAKAGE` | `display` | `SAFE_HISTORICAL_CANDIDATE` |
| `cand_qwen3_5_4b__ce115_calc_exact_rational_expression_l1__ab2d__seed_2026071303` | `ENTRY_POINT_OR_CONTRACT_FAILURE` | `ast` | `ABSTAIN` |
| `cand_qwen3_5_4b__ce115_calc_exact_rational_expression_l1__ab2g__seed_2026071301` | `MODEL_DEGENERATIVE_NONTERMINATION` | `ast` | `ABSTAIN` |
| `cand_qwen3_5_4b__ce115_calc_exact_rational_expression_l1__ab2g__seed_2026071302` | `CORE_LOGIC_INCORRECT` | `ast` | `ABSTAIN` |
| `cand_qwen3_5_4b__ce115_calc_exact_rational_expression_l1__ab2g__seed_2026071303` | `MODEL_DEGENERATIVE_NONTERMINATION` | `ast` | `ABSTAIN` |
| `cand_qwen3_5_4b__ce115_calc_polynomial_division_l1__ab1__seed_2026071301` | `CORE_LOGIC_INCORRECT` | `ast` | `ABSTAIN` |
| `cand_qwen3_5_4b__ce115_calc_polynomial_division_l1__ab1__seed_2026071302` | `CORE_LOGIC_INCORRECT` | `ast` | `ABSTAIN` |
| `cand_qwen3_5_4b__ce115_calc_polynomial_division_l1__ab1__seed_2026071303` | `CORE_LOGIC_INCORRECT` | `ast` | `ABSTAIN` |
| `cand_qwen3_5_4b__ce115_calc_polynomial_division_l1__ab2d__seed_2026071301` | `CORE_LOGIC_INCORRECT` | `ast` | `ABSTAIN` |
| `cand_qwen3_5_4b__ce115_calc_polynomial_division_l1__ab2d__seed_2026071302` | `CORE_LOGIC_INCORRECT` | `ast` | `ABSTAIN` |
| `cand_qwen3_5_4b__ce115_calc_polynomial_division_l1__ab2d__seed_2026071303` | `CORE_LOGIC_INCORRECT` | `ast` | `ABSTAIN` |
| `cand_qwen3_5_4b__ce115_calc_polynomial_division_l1__ab2g__seed_2026071301` | `CORE_LOGIC_INCORRECT` | `ast` | `ABSTAIN` |
| `cand_qwen3_5_4b__ce115_calc_polynomial_division_l1__ab2g__seed_2026071302` | `CORE_LOGIC_INCORRECT` | `ast` | `ABSTAIN` |
| `cand_qwen3_5_4b__ce115_calc_polynomial_division_l1__ab2g__seed_2026071303` | `CORE_LOGIC_INCORRECT` | `ast` | `ABSTAIN` |
| `cand_qwen3_5_4b__ce115_calc_polynomial_factor_roots_l1__ab1__seed_2026071302` | `CORE_LOGIC_INCORRECT` | `ast` | `ABSTAIN` |
| `cand_qwen3_5_4b__ce115_calc_polynomial_factor_roots_l1__ab1__seed_2026071303` | `CORE_LOGIC_INCORRECT` | `ast` | `ABSTAIN` |
| `cand_qwen3_5_4b__ce115_calc_polynomial_factor_roots_l1__ab2d__seed_2026071302` | `CORE_LOGIC_INCORRECT` | `ast` | `ABSTAIN` |
| `cand_qwen3_5_4b__ce115_calc_polynomial_factor_roots_l1__ab2d__seed_2026071303` | `CORE_LOGIC_INCORRECT` | `ast` | `ABSTAIN` |
| `cand_qwen3_5_4b__ce115_calc_polynomial_factor_roots_l1__ab2g__seed_2026071303` | `CORE_LOGIC_INCORRECT` | `ast` | `ABSTAIN` |
| `cand_qwen3_5_4b__ce115_calc_radical_simplification_l1__ab1__seed_2026071301` | `OUTPUT_WRAPPING_OR_LEAKAGE` | `display` | `SAFE_HISTORICAL_CANDIDATE` |
| `cand_qwen3_5_4b__ce115_calc_radical_simplification_l1__ab1__seed_2026071302` | `MODEL_DEGENERATIVE_NONTERMINATION` | `ast` | `ABSTAIN` |
| `cand_qwen3_5_4b__ce115_calc_radical_simplification_l1__ab1__seed_2026071303` | `MODEL_DEGENERATIVE_NONTERMINATION` | `ast` | `ABSTAIN` |
| `cand_qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d__seed_2026071301` | `MODEL_DEGENERATIVE_NONTERMINATION` | `ast` | `ABSTAIN` |
| `cand_qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d__seed_2026071302` | `MODEL_DEGENERATIVE_NONTERMINATION` | `ast` | `ABSTAIN` |
| `cand_qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d__seed_2026071303` | `CORE_LOGIC_INCORRECT` | `ast` | `ABSTAIN` |
| `cand_qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2g__seed_2026071301` | `MODEL_DEGENERATIVE_NONTERMINATION` | `ast` | `ABSTAIN` |
| `cand_qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2g__seed_2026071302` | `MODEL_DEGENERATIVE_NONTERMINATION` | `ast` | `ABSTAIN` |
| `cand_qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2g__seed_2026071303` | `CORE_LOGIC_MISSING` | `ast` | `ABSTAIN` |
| `cand_qwen3_5_9b__ce115_calc_exact_rational_expression_l1__ab1__seed_2026071301` | `ENTRY_POINT_OR_CONTRACT_FAILURE` | `ast` | `ABSTAIN` |
| `cand_qwen3_5_9b__ce115_calc_exact_rational_expression_l1__ab1__seed_2026071302` | `MODEL_DEGENERATIVE_NONTERMINATION` | `ast` | `ABSTAIN` |
| `cand_qwen3_5_9b__ce115_calc_exact_rational_expression_l1__ab1__seed_2026071303` | `CORE_LOGIC_MISSING` | `ast` | `ABSTAIN` |
| `cand_qwen3_5_9b__ce115_calc_exact_rational_expression_l1__ab2d__seed_2026071301` | `MODEL_DEGENERATIVE_NONTERMINATION` | `ast` | `ABSTAIN` |
| `cand_qwen3_5_9b__ce115_calc_exact_rational_expression_l1__ab2d__seed_2026071302` | `MODEL_DEGENERATIVE_NONTERMINATION` | `ast` | `ABSTAIN` |
| `cand_qwen3_5_9b__ce115_calc_exact_rational_expression_l1__ab2d__seed_2026071303` | `ENTRY_POINT_OR_CONTRACT_FAILURE` | `ast` | `ABSTAIN` |
| `cand_qwen3_5_9b__ce115_calc_exact_rational_expression_l1__ab2g__seed_2026071301` | `CORE_LOGIC_MISSING` | `ast` | `ABSTAIN` |
| `cand_qwen3_5_9b__ce115_calc_exact_rational_expression_l1__ab2g__seed_2026071302` | `CORE_LOGIC_MISSING` | `ast` | `ABSTAIN` |
| `cand_qwen3_5_9b__ce115_calc_exact_rational_expression_l1__ab2g__seed_2026071303` | `OUTPUT_WRAPPING_OR_LEAKAGE` | `display` | `SAFE_HISTORICAL_CANDIDATE` |
| `cand_qwen3_5_9b__ce115_calc_polynomial_division_l1__ab1__seed_2026071301` | `OUTPUT_WRAPPING_OR_LEAKAGE` | `display` | `SAFE_HISTORICAL_CANDIDATE` |
| `cand_qwen3_5_9b__ce115_calc_polynomial_division_l1__ab1__seed_2026071302` | `MODEL_DEGENERATIVE_NONTERMINATION` | `ast` | `ABSTAIN` |
| `cand_qwen3_5_9b__ce115_calc_polynomial_division_l1__ab1__seed_2026071303` | `MODEL_DEGENERATIVE_NONTERMINATION` | `ast` | `ABSTAIN` |
| `cand_qwen3_5_9b__ce115_calc_polynomial_division_l1__ab2d__seed_2026071301` | `MODEL_DEGENERATIVE_NONTERMINATION` | `ast` | `ABSTAIN` |
| `cand_qwen3_5_9b__ce115_calc_polynomial_division_l1__ab2d__seed_2026071302` | `CORE_LOGIC_MISSING` | `ast` | `ABSTAIN` |
| `cand_qwen3_5_9b__ce115_calc_polynomial_division_l1__ab2d__seed_2026071303` | `CORE_LOGIC_MISSING` | `ast` | `ABSTAIN` |
| `cand_qwen3_5_9b__ce115_calc_polynomial_division_l1__ab2g__seed_2026071301` | `MODEL_DEGENERATIVE_NONTERMINATION` | `display` | `SAFE_HISTORICAL_CANDIDATE` |
| `cand_qwen3_5_9b__ce115_calc_polynomial_division_l1__ab2g__seed_2026071302` | `MODEL_DEGENERATIVE_NONTERMINATION` | `display` | `SAFE_HISTORICAL_CANDIDATE` |
| `cand_qwen3_5_9b__ce115_calc_polynomial_division_l1__ab2g__seed_2026071303` | `MODEL_DEGENERATIVE_NONTERMINATION` | `ast` | `ABSTAIN` |
| `cand_qwen3_5_9b__ce115_calc_polynomial_factor_roots_l1__ab1__seed_2026071301` | `CORE_LOGIC_MISSING` | `ast` | `ABSTAIN` |
| `cand_qwen3_5_9b__ce115_calc_polynomial_factor_roots_l1__ab1__seed_2026071302` | `MODEL_DEGENERATIVE_NONTERMINATION` | `display` | `SAFE_HISTORICAL_CANDIDATE` |
| `cand_qwen3_5_9b__ce115_calc_polynomial_factor_roots_l1__ab2d__seed_2026071301` | `CORE_LOGIC_INCORRECT` | `ast` | `ABSTAIN` |
| `cand_qwen3_5_9b__ce115_calc_polynomial_factor_roots_l1__ab2d__seed_2026071302` | `CORE_LOGIC_MISSING` | `ast` | `ABSTAIN` |
| `cand_qwen3_5_9b__ce115_calc_polynomial_factor_roots_l1__ab2d__seed_2026071303` | `CORE_LOGIC_MISSING` | `ast` | `ABSTAIN` |
| `cand_qwen3_5_9b__ce115_calc_polynomial_factor_roots_l1__ab2g__seed_2026071301` | `CORE_LOGIC_INCORRECT` | `ast` | `ABSTAIN` |
| `cand_qwen3_5_9b__ce115_calc_polynomial_factor_roots_l1__ab2g__seed_2026071302` | `MODEL_DEGENERATIVE_NONTERMINATION` | `ast` | `ABSTAIN` |
| `cand_qwen3_5_9b__ce115_calc_polynomial_factor_roots_l1__ab2g__seed_2026071303` | `MODEL_DEGENERATIVE_NONTERMINATION` | `ast` | `ABSTAIN` |
| `cand_qwen3_5_9b__ce115_calc_radical_simplification_l1__ab1__seed_2026071303` | `MODEL_DEGENERATIVE_NONTERMINATION` | `display` | `SAFE_HISTORICAL_CANDIDATE` |
| `cand_qwen3_5_9b__ce115_calc_radical_simplification_l1__ab2d__seed_2026071301` | `CORE_LOGIC_MISSING` | `ast` | `ABSTAIN` |
| `cand_qwen3_5_9b__ce115_calc_radical_simplification_l1__ab2g__seed_2026071301` | `MODEL_DEGENERATIVE_NONTERMINATION` | `display` | `SAFE_HISTORICAL_CANDIDATE` |
| `cand_qwen3_5_9b__ce115_calc_radical_simplification_l1__ab2g__seed_2026071302` | `OUTPUT_WRAPPING_OR_LEAKAGE` | `display` | `SAFE_HISTORICAL_CANDIDATE` |
| `cand_qwen3_5_9b__ce115_calc_radical_simplification_l1__ab2g__seed_2026071303` | `CORE_LOGIC_MISSING` | `ast` | `ABSTAIN` |

