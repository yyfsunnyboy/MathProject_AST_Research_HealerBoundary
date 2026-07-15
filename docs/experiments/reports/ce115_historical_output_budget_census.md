# 📊 CE115 Historical Output Size and Token-Budget Census Report

This report presents the forensic census of historical code outputs for Qwen3 and Gemini models across the different ablation strategies (`Ab1`, `Ab2`, and `Ab3`). It provides statistical bounds on output lengths and recommends execution budget settings for future confirmatory runs.

---

## 1. Natural Completion Token Statistics (Level A Telemetry)

| Cohort | Count (N) | Median (Out) | P90 (Out) | P95 (Out) | P99 (Out) | Max (Out) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Overall** | 85 | 1709.0 | 6526.6 | 7293.2 | 9612.5 | 10282.0 |
| **Ab1** | 25 | 3174.0 | 8175.4 | 9268.2 | 10090.7 | 10282.0 |
| **Ab2** | 30 | 1677.0 | 5404.8 | 5680.1 | 6501.1 | 6792.0 |
| **Ab3** | 30 | 1768.0 | 4896.2 | 5172.0 | 6023.7 | 6298.0 |

---

## 2. Suspected Truncation & Budget Ceilings

The census identified **4 suspected truncation instances** where output limit caps were hit:
1. `qwen3-8b_Ab1_run01`: Output token count hit exactly **16384** tokens (due to an infinite loop repeating lines of code).
2. The 3 formal Qwen3.5 confirmatory run cells where the sum of input and output tokens hit exactly **4096** (`STRONGLY_SUPPORTED_CONTEXT_BUDGET_LIMIT`):
   - `454 + 3642 = 4096`
   - `579 + 3517 = 4096`
   - `641 + 3455 = 4096`

---

## 3. Output Length Comparison: Ab1 vs. Ab2 vs. Ab3

- **Ab1 (Bare LLM Output)**: Tended to be significantly longer (median ~5.6k tokens for qwen3-8b, maxing out at 9485 tokens for natural completions, and hitting the 16384 ceiling in one looping run). This is because the model tries to write a complete parser and generator from scratch, including extensive comments and prose.
- **Ab2 (Scaffold Assembled)** and **Ab3 (Healed)**: Yielded compact code blocks (median ~1.8k-2.2k output tokens). The final program sizes (around 22-24 KB) contain a large amount of injected scaffold code (about 20 KB), meaning the actual raw generation from the model is very small (around 1k-2k tokens).

---

## 4. Assessment of Candidates A & B

| Budget Option | `num_ctx` | `num_predict` | Assessment |
| :--- | :---: | :---: | :--- |
| **Candidate A** | `32768` | `16384` | Sufficient for normal runs (overall P99 Out is 9612.5 tokens, and 16384 is 70% higher than the maximum natural completion of 9485 tokens). However, if the model enters a repetition loop, it might hit this boundary. |
| **Candidate B (Recommended)** | `65536` | `24576` | **Recommended**. Providing `num_predict = 24576` gives >150% safety margin over the longest natural completion. A context size of `num_ctx = 65536` satisfies the context equation `max_prompt_tokens + num_predict + safety_margin` with extreme headroom, preventing any configuration truncations on very long math tasks. |

---

## 5. Recommended Preflight Cells List

To validate that the recommended budget avoids truncation, we propose a preflight test suite of **6 key cells**:

1. `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab1__seed_2026071303` (Truncated 4B Ab1)
2. `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2g__seed_2026071301` (Truncated 4B Ab2g)
3. `qwen3_5_9b__ce115_calc_polynomial_division_l1__ab2g__seed_2026071302` (Truncated 9B Ab2g)
4. `qwen3_5_9b__ce115_calc_polynomial_division_l1__ab1__seed_2026071301` (Longest 9B Ab1 Cell)
5. `qwen3_5_9b__ce115_calc_polynomial_division_l1__ab2d__seed_2026071302` (9B Ab2d Cell)
6. `qwen3_5_4b__ce115_calc_exact_rational_expression_l1__ab2d__seed_2026071301` (4B Ab2d Cell)

---

## 6. Limitations Statement

- **Evidence Limitations**: Telemetry data is parsed directly from headers inserted by historical runner scripts and raw Ollama JSONL logs. The Level B character-to-token estimates (`ESTIMATED_FROM_TEXT_SIZE_NOT_RUNTIME_TOKEN_COUNT`) are approximations and should not be used as absolute ground truth.
