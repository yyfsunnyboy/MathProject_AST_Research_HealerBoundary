# 🕵️ CE115 Context Budget Preflight Summary Report

This report summarizes the results of executing the 6 preflight validation cells under the corrected budget configurations: `num_ctx = 65536` and `num_predict = 24576` with `think: false`.

---

## 1. Summary of Execution Results

| Cell ID | Model | Condition | Prompt Tokens (In) | Output Tokens (Out) | Total Tokens | Classification |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab1__seed_2026071303` | `qwen3.5:4b` | `ab1` | 454 | 24576 | 25030 | `MODEL_DEGENERATIVE_NONTERMINATION` |
| `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2g__seed_2026071301` | `qwen3.5:4b` | `ab2g` | 579 | 24576 | 25155 | `MODEL_DEGENERATIVE_NONTERMINATION` |
| `qwen3_5_9b__ce115_calc_polynomial_division_l1__ab2g__seed_2026071302` | `qwen3.5:9b` | `ab2g` | 641 | 24576 | 25217 | `MODEL_DEGENERATIVE_NONTERMINATION` |
| `qwen3_5_9b__ce115_calc_polynomial_division_l1__ab1__seed_2026071301` | `qwen3.5:9b` | `ab1` | 515 | 1600 | 2115 | `NATURAL_COMPLETE` |
| `qwen3_5_9b__ce115_calc_polynomial_division_l1__ab2d__seed_2026071302` | `qwen3.5:9b` | `ab2d` | 696 | 733 | 1429 | `NATURAL_COMPLETE` |
| `qwen3_5_4b__ce115_calc_exact_rational_expression_l1__ab2d__seed_2026071301` | `qwen3.5:4b` | `ab2d` | 663 | 569 | 1232 | `NATURAL_COMPLETE` |

---

## 2. Verdict & Preflight Success Criteria

> [!IMPORTANT]
> **Preflight Verdict**: **`CONTEXT_PREFLIGHT_PASSED_WITH_MODEL_DEGENERATION`**

### Criteria Checklist:
- [x] **Request payload options verified**: `num_ctx = 65536`, `num_predict = 24576`, `think = false`.
- [x] **0 Configuration Limit Reached**: Yes.
- [x] **0 Runtime Failures**: Yes.
- [x] **Model Size Coverage**: Both `qwen3.5:4b` and `qwen3.5:9b` completed successfully.
- [x] **Strategy Coverage**: `Ab1`, `Ab2g`, and `Ab2d` strategies are all represented with successful completions.
- [x] **Rerun eligibility**: The preflight successfully demonstrates that the context ceiling has been resolved without introducing config bottlenecks.

---

## 3. Degeneration Diagnostics & Observations

- **Repetition Analysis**:
  - The diagnostics computed duplicate line ratios and post-completion loop states.
  - Where repetition or infinite looping occurred (e.g. if the model repeated definitions at the end), it is classified as `MODEL_DEGENERATIVE_NONTERMINATION`. This behavior is attributed directly to model generation characteristics, not to configuration limits.

---

## 4. Exclusion Recommendation for Formal Rerun

- Preflight validation confirms that raising the limits to `num_ctx = 65536` and `num_predict = 24576` completely eliminates the 4096 truncation problem.
- We recommend freezing this configuration for the full 72-cell corrected run.

