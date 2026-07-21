# Math16 Ab2g (Generic Scaffold) Prompts

- **實驗條件定義**: Ab2g (Generic scaffold) 在 Ab1 基礎上增加了通用程式碼鷹架。在提示詞尾部附加 `## Clean-incremental GENERIC` 區塊，強調只輸出完整 Python 程式碼、禁止 explanatory prose 以及 markdown fences，並規範輸出 key 的完整性與一致性。
- **Prompt組裝來源**: 經由 `agent_tools/finals_rebuild/ce115_clean_incremental_ablation.py` 中的 `build_condition_prompt("ab2g", task, frozen)` 程式化組裝。
- **Prompt版本**: 與 Qwen 4B/9B 正式 `run_002` 實驗及後續 Gemini `run_003_multiseed` 採用的正式版本一致。
- **生成日期**: 2026-07-21
- **16題完整性檢查結果**: 經程式化檢查，16題題目、參數與輸出格式完全齊備，且皆包含完整的通用程式碼鷹架區塊。
- **文件SHA-256產生方式**: 使用 `prompt_sha256(prompt)`（計算記憶體中 UTF-8 編碼且換行符為 LF 的 Prompt 字串 SHA-256 哈希值）。

---

## 題目01：ce115_calc_polynomial_division_l1

- **Domain**：polynomials
- **Condition**：ab2g
- **Frozen seed／parameters**：`seed=2026071301` / `{"dividend_coefficients": [6, 0, 6], "divisor_coefficients": [1, -4]}`
- **Answer contract**：d. question_text must use formal LaTeX delimiters \( \) / \[ \]. correct_answer must include quotient_coefficients, remainder_coefficients, quotient_latex, and remainder_latex. Exact arithmetic; no floats.
- **Prompt SHA-256**：`3d60a095612840e6d08496d68f759c891c049481c5af862609bd89ece29121b6`
- **適用模型**：Gemini 3.5 Flash／Qwen 3.5 4B／Qwen 3.5 9B
- **Prompt版本基準**：Current SSOT version (consistent with Qwen run_002)

### 實際送模Prompt

```text
Write only Python source. Implement def generate(level=1, **kwargs).
Task: ce115_calc_polynomial_division_l1 (polynomials, difficulty level 1).
Task specification: math16_polynomial_division_general.
Frozen sampled parameters: {"dividend_coefficients": [6, 0, 6], "divisor_coefficients": [1, -4]}
generate() must return a dict with exactly question_text, correct_answer, and oracle_payload. question_text must use formal LaTeX delimiters \( \) / \[ \]. correct_answer must include quotient_coefficients, remainder_coefficients, quotient_latex, and remainder_latex. Exact arithmetic; no floats. oracle_payload must exactly equal the frozen sampled parameters. Do not use input, files, network, subprocess, Markdown fences, or explanations.

## Clean-incremental GENERIC
Output complete Python source only. Do not use Markdown fences or explanatory prose. Preserve frozen parameters exactly. Verify that generate() exists. Verify that the return value has exactly the three required top-level keys. Verify field types match the stated contract and that oracle_payload equals the frozen parameters.
```

---

## 題目02：ce115_calc_polynomial_factor_roots_l1

- **Domain**：polynomials
- **Condition**：ab2g
- **Frozen seed／parameters**：`seed=2026071301` / `{"quadratic_coefficients": [1, 4, -12]}`
- **Answer contract**：d. question_text must use formal LaTeX delimiters. correct_answer must include roots (ascending), factorization_latex, and roots_latex. Exact arithmetic; no floats.
- **Prompt SHA-256**：`9aa875c3c2de0b79cb0cf0bb5ec18ef9a02ead452db9d4d044500f175a8f485f`
- **適用模型**：Gemini 3.5 Flash／Qwen 3.5 4B／Qwen 3.5 9B
- **Prompt版本基準**：Current SSOT version (consistent with Qwen run_002)

### 實際送模Prompt

```text
Write only Python source. Implement def generate(level=1, **kwargs).
Task: ce115_calc_polynomial_factor_roots_l1 (polynomials, difficulty level 1).
Task specification: math16_polynomial_factor_roots.
Frozen sampled parameters: {"quadratic_coefficients": [1, 4, -12]}
generate() must return a dict with exactly question_text, correct_answer, and oracle_payload. question_text must use formal LaTeX delimiters. correct_answer must include roots (ascending), factorization_latex, and roots_latex. Exact arithmetic; no floats. oracle_payload must exactly equal the frozen sampled parameters. Do not use input, files, network, subprocess, Markdown fences, or explanations.

## Clean-incremental GENERIC
Output complete Python source only. Do not use Markdown fences or explanatory prose. Preserve frozen parameters exactly. Verify that generate() exists. Verify that the return value has exactly the three required top-level keys. Verify field types match the stated contract and that oracle_payload equals the frozen parameters.
```

---

## 題目03：ce115_calc_exact_rational_expression_l1

- **Domain**：rational_arithmetic
- **Condition**：ab2g
- **Frozen seed／parameters**：`seed=2026071301` / `{"products": [{"sign": 1, "left": "2.79", "right": "89.3"}, {"sign": -1, "left": "-0.21", "right": "89.3"}]}`
- **Answer contract**：d. question_text must use formal LaTeX delimiters. correct_answer must include value (irreducible p/q string) and canonical_latex. Exact arithmetic; no floats.
- **Prompt SHA-256**：`5f397d56fab2649201b606af7abf51780a93d6d74269fd5f5d216a538aa8b8d9`
- **適用模型**：Gemini 3.5 Flash／Qwen 3.5 4B／Qwen 3.5 9B
- **Prompt版本基準**：Current SSOT version (consistent with Qwen run_002)

### 實際送模Prompt

```text
Write only Python source. Implement def generate(level=1, **kwargs).
Task: ce115_calc_exact_rational_expression_l1 (rational_arithmetic, difficulty level 1).
Task specification: math16_exact_rational_expression.
Frozen sampled parameters: {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}
generate() must return a dict with exactly question_text, correct_answer, and oracle_payload. question_text must use formal LaTeX delimiters. correct_answer must include value (irreducible p/q string) and canonical_latex. Exact arithmetic; no floats. oracle_payload must exactly equal the frozen sampled parameters. Do not use input, files, network, subprocess, Markdown fences, or explanations.

## Clean-incremental GENERIC
Output complete Python source only. Do not use Markdown fences or explanatory prose. Preserve frozen parameters exactly. Verify that generate() exists. Verify that the return value has exactly the three required top-level keys. Verify field types match the stated contract and that oracle_payload equals the frozen parameters.
```

---

## 題目04：ce115_calc_radical_simplification_l1

- **Domain**：radicals
- **Condition**：ab2g
- **Frozen seed／parameters**：`seed=2026071301` / `{"radicand": 27}`
- **Answer contract**：d. question_text must use formal LaTeX delimiters. correct_answer must include coefficient, radicand, and canonical_latex. Exact integers only; no floats.
- **Prompt SHA-256**：`a88ec9aa5f19dc7b5348cdd1cfdc9b503c1fbefcc0ad12889e21eeff5cb19621`
- **適用模型**：Gemini 3.5 Flash／Qwen 3.5 4B／Qwen 3.5 9B
- **Prompt版本基準**：Current SSOT version (consistent with Qwen run_002)

### 實際送模Prompt

```text
Write only Python source. Implement def generate(level=1, **kwargs).
Task: ce115_calc_radical_simplification_l1 (radicals, difficulty level 1).
Task specification: math16_radical_simplification.
Frozen sampled parameters: {"radicand": 27}
generate() must return a dict with exactly question_text, correct_answer, and oracle_payload. question_text must use formal LaTeX delimiters. correct_answer must include coefficient, radicand, and canonical_latex. Exact integers only; no floats. oracle_payload must exactly equal the frozen sampled parameters. Do not use input, files, network, subprocess, Markdown fences, or explanations.

## Clean-incremental GENERIC
Output complete Python source only. Do not use Markdown fences or explanatory prose. Preserve frozen parameters exactly. Verify that generate() exists. Verify that the return value has exactly the three required top-level keys. Verify field types match the stated contract and that oracle_payload equals the frozen parameters.
```

---

## 題目05：ce111_q02_polynomial_division_remainder

- **Domain**：polynomials
- **Condition**：ab2g
- **Frozen seed／parameters**：`seed=2026071301` / `{"dividend_coefficients": [6, 4, 0], "divisor_coefficients": [2, 0, 0]}`
- **Answer contract**：d. question_text must use formal LaTeX delimiters. correct_answer must include only remainder and canonical_latex (quotient is not scored).
- **Prompt SHA-256**：`1cb912077ad2776904919f36b8947a00c6986c58c24c9311c1d8872dbc447e31`
- **適用模型**：Gemini 3.5 Flash／Qwen 3.5 4B／Qwen 3.5 9B
- **Prompt版本基準**：Current SSOT version (consistent with Qwen run_002)

### 實際送模Prompt

```text
Write only Python source. Implement def generate(level=1, **kwargs).
Task: ce111_q02_polynomial_division_remainder (polynomials, difficulty level 1).
Task specification: math16_polynomial_division_remainder_only.
Frozen sampled parameters: {"dividend_coefficients": [6, 4, 0], "divisor_coefficients": [2, 0, 0]}
generate() must return a dict with exactly question_text, correct_answer, and oracle_payload. question_text must use formal LaTeX delimiters. correct_answer must include only remainder and canonical_latex (quotient is not scored). oracle_payload must exactly equal the frozen sampled parameters. Do not use input, files, network, subprocess, Markdown fences, or explanations.

## Clean-incremental GENERIC
Output complete Python source only. Do not use Markdown fences or explanatory prose. Preserve frozen parameters exactly. Verify that generate() exists. Verify that the return value has exactly the three required top-level keys. Verify field types match the stated contract and that oracle_payload equals the frozen parameters.
```

---

## 題目06：ce111_q08_polynomial_factor_parameter_recovery

- **Domain**：polynomials
- **Condition**：ab2g
- **Frozen seed／parameters**：`seed=2026071301` / `{"quadratic_coefficients": [39, 5, -14], "template_left_x_coefficient": 3, "factor_order_policy": "strict_source_template"}`
- **Answer contract**：d. question_text must use formal LaTeX delimiters. factor_order_policy is strict_source_template: first factor is fixed as (3x+a). correct_answer must be the integer a+2c. Do not redefine parameters after swapping factors.
- **Prompt SHA-256**：`1ddb92a07ec3df5f46360fdf5c9881eb4745bf1f339bac0c6d00e5e41217ac17`
- **適用模型**：Gemini 3.5 Flash／Qwen 3.5 4B／Qwen 3.5 9B
- **Prompt版本基準**：Current SSOT version (consistent with Qwen run_002)

### 實際送模Prompt

```text
Write only Python source. Implement def generate(level=1, **kwargs).
Task: ce111_q08_polynomial_factor_parameter_recovery (polynomials, difficulty level 1).
Task specification: math16_polynomial_factor_parameter_recovery.
Frozen sampled parameters: {"factor_order_policy": "strict_source_template", "quadratic_coefficients": [39, 5, -14], "template_left_x_coefficient": 3}
generate() must return a dict with exactly question_text, correct_answer, and oracle_payload. question_text must use formal LaTeX delimiters. factor_order_policy is strict_source_template: first factor is fixed as (3x+a). correct_answer must be the integer a+2c. Do not redefine parameters after swapping factors. oracle_payload must exactly equal the frozen sampled parameters. Do not use input, files, network, subprocess, Markdown fences, or explanations.

## Clean-incremental GENERIC
Output complete Python source only. Do not use Markdown fences or explanatory prose. Preserve frozen parameters exactly. Verify that generate() exists. Verify that the return value has exactly the three required top-level keys. Verify field types match the stated contract and that oracle_payload equals the frozen parameters.
```

---

## 題目07：ce111_q03_prime_factor_selection

- **Domain**：integers
- **Condition**：ab2g
- **Frozen seed／parameters**：`seed=2026071301` / `{"candidates": [11, 12, 13, 14], "n": 156}`
- **Answer contract**：d. question_text must use formal LaTeX delimiters where math appears. correct_answer must be a single exact integer.
- **Prompt SHA-256**：`5436b011cb2be3d0edee52770f8c5a28348f9ef4763ae485b8c6a80798ef1cbf`
- **適用模型**：Gemini 3.5 Flash／Qwen 3.5 4B／Qwen 3.5 9B
- **Prompt版本基準**：Current SSOT version (consistent with Qwen run_002)

### 實際送模Prompt

```text
Write only Python source. Implement def generate(level=1, **kwargs).
Task: ce111_q03_prime_factor_selection (integers, difficulty level 1).
Task specification: math16_prime_factor_selection.
Frozen sampled parameters: {"candidates": [11, 12, 13, 14], "n": 156}
generate() must return a dict with exactly question_text, correct_answer, and oracle_payload. question_text must use formal LaTeX delimiters where math appears. correct_answer must be a single exact integer. oracle_payload must exactly equal the frozen sampled parameters. Do not use input, files, network, subprocess, Markdown fences, or explanations.

## Clean-incremental GENERIC
Output complete Python source only. Do not use Markdown fences or explanatory prose. Preserve frozen parameters exactly. Verify that generate() exists. Verify that the return value has exactly the three required top-level keys. Verify field types match the stated contract and that oracle_payload equals the frozen parameters.
```

---

## 題目08：ce112_q01_negative_integer_power

- **Domain**：integers
- **Condition**：ab2g
- **Frozen seed／parameters**：`seed=2026071301` / `{"base": -3, "exponent": 3}`
- **Answer contract**：d. question_text must use formal LaTeX delimiters where math appears. correct_answer must be a single exact integer.
- **Prompt SHA-256**：`cf486895c58fc5f91aaf2ba8cb03259f0eb98cb10d99a9d8a5734721bfdd7edb`
- **適用模型**：Gemini 3.5 Flash／Qwen 3.5 4B／Qwen 3.5 9B
- **Prompt版本基準**：Current SSOT version (consistent with Qwen run_002)

### 實際送模Prompt

```text
Write only Python source. Implement def generate(level=1, **kwargs).
Task: ce112_q01_negative_integer_power (integers, difficulty level 1).
Task specification: math16_negative_integer_power.
Frozen sampled parameters: {"base": -3, "exponent": 3}
generate() must return a dict with exactly question_text, correct_answer, and oracle_payload. question_text must use formal LaTeX delimiters where math appears. correct_answer must be a single exact integer. oracle_payload must exactly equal the frozen sampled parameters. Do not use input, files, network, subprocess, Markdown fences, or explanations.

## Clean-incremental GENERIC
Output complete Python source only. Do not use Markdown fences or explanatory prose. Preserve frozen parameters exactly. Verify that generate() exists. Verify that the return value has exactly the three required top-level keys. Verify field types match the stated contract and that oracle_payload equals the frozen parameters.
```

---

## 題目09：ce112_q09_divisor_multiple_intersection

- **Domain**：integers
- **Condition**：ab2g
- **Frozen seed／parameters**：`seed=2026071301` / `{"multiple_of": 18, "divisor_of": 216}`
- **Answer contract**：d. question_text must use formal LaTeX delimiters where math appears. correct_answer must be a JSON-compatible dict with exactly count (int).
- **Prompt SHA-256**：`8465217dde30310c3f927c2ec00e152e065f40c5508cd0339ae46a541c19496e`
- **適用模型**：Gemini 3.5 Flash／Qwen 3.5 4B／Qwen 3.5 9B
- **Prompt版本基準**：Current SSOT version (consistent with Qwen run_002)

### 實際送模Prompt

```text
Write only Python source. Implement def generate(level=1, **kwargs).
Task: ce112_q09_divisor_multiple_intersection (integers, difficulty level 1).
Task specification: math16_divisor_multiple_intersection.
Frozen sampled parameters: {"divisor_of": 216, "multiple_of": 18}
generate() must return a dict with exactly question_text, correct_answer, and oracle_payload. question_text must use formal LaTeX delimiters where math appears. correct_answer must be a JSON-compatible dict with exactly count (int). oracle_payload must exactly equal the frozen sampled parameters. Do not use input, files, network, subprocess, Markdown fences, or explanations.

## Clean-incremental GENERIC
Output complete Python source only. Do not use Markdown fences or explanatory prose. Preserve frozen parameters exactly. Verify that generate() exists. Verify that the return value has exactly the three required top-level keys. Verify field types match the stated contract and that oracle_payload equals the frozen parameters.
```

---

## 題目10：ce111_nonchoice_q01_part1_exponential_growth

- **Domain**：integers
- **Condition**：ab2g
- **Frozen seed／parameters**：`seed=2026071301` / `{"initial": 1, "split_factor": 4, "hours_per_generation": 20, "days": 15}`
- **Answer contract**：d. question_text must use formal LaTeX delimiters where math appears. correct_answer must be a JSON-compatible dict with exactly k (int).
- **Prompt SHA-256**：`93f82f61b6271d56cbaf1b7bf1276afc821b055cf767d2e9a496414ee933441e`
- **適用模型**：Gemini 3.5 Flash／Qwen 3.5 4B／Qwen 3.5 9B
- **Prompt版本基準**：Current SSOT version (consistent with Qwen run_002)

### 實際送模Prompt

```text
Write only Python source. Implement def generate(level=1, **kwargs).
Task: ce111_nonchoice_q01_part1_exponential_growth (integers, difficulty level 1).
Task specification: math16_exponential_growth_generation_count.
Frozen sampled parameters: {"days": 15, "hours_per_generation": 20, "initial": 1, "split_factor": 4}
generate() must return a dict with exactly question_text, correct_answer, and oracle_payload. question_text must use formal LaTeX delimiters where math appears. correct_answer must be a JSON-compatible dict with exactly k (int). oracle_payload must exactly equal the frozen sampled parameters. Do not use input, files, network, subprocess, Markdown fences, or explanations.

## Clean-incremental GENERIC
Output complete Python source only. Do not use Markdown fences or explanatory prose. Preserve frozen parameters exactly. Verify that generate() exists. Verify that the return value has exactly the three required top-level keys. Verify field types match the stated contract and that oracle_payload equals the frozen parameters.
```

---

## 題目11：ce111_q05_exact_fraction_expression

- **Domain**：rational_arithmetic
- **Condition**：ab2g
- **Frozen seed／parameters**：`seed=2026071301` / `{"expression": "9/22 + 11/18 - (23/22 - 7/18)"}`
- **Answer contract**：d. question_text must use formal LaTeX delimiters. correct_answer must include numerator, denominator, and canonical_latex for an irreducible fraction.
- **Prompt SHA-256**：`9932c16c2dd3109a2f340ae98c4b0e51ef01fe9e024fbcc5f63bab49ef3ae965`
- **適用模型**：Gemini 3.5 Flash／Qwen 3.5 4B／Qwen 3.5 9B
- **Prompt版本基準**：Current SSOT version (consistent with Qwen run_002)

### 實際送模Prompt

```text
Write only Python source. Implement def generate(level=1, **kwargs).
Task: ce111_q05_exact_fraction_expression (rational_arithmetic, difficulty level 1).
Task specification: math16_exact_fraction_expression.
Frozen sampled parameters: {"expression": "9/22 + 11/18 - (23/22 - 7/18)"}
generate() must return a dict with exactly question_text, correct_answer, and oracle_payload. question_text must use formal LaTeX delimiters. correct_answer must include numerator, denominator, and canonical_latex for an irreducible fraction. oracle_payload must exactly equal the frozen sampled parameters. Do not use input, files, network, subprocess, Markdown fences, or explanations.

## Clean-incremental GENERIC
Output complete Python source only. Do not use Markdown fences or explanatory prose. Preserve frozen parameters exactly. Verify that generate() exists. Verify that the return value has exactly the three required top-level keys. Verify field types match the stated contract and that oracle_payload equals the frozen parameters.
```

---

## 題目12：ce113_q01_negative_fraction_subtraction

- **Domain**：rational_arithmetic
- **Condition**：ab2g
- **Frozen seed／parameters**：`seed=2026071301` / `{"expression": "3/7 - (-1/4)"}`
- **Answer contract**：d. question_text must use formal LaTeX delimiters. correct_answer must include numerator, denominator, and canonical_latex for an irreducible fraction.
- **Prompt SHA-256**：`b0fe97bca3b7957bb481e88060e49681e6c7ccd67ff19c2eaf13d3ec47559a0b`
- **適用模型**：Gemini 3.5 Flash／Qwen 3.5 4B／Qwen 3.5 9B
- **Prompt版本基準**：Current SSOT version (consistent with Qwen run_002)

### 實際送模Prompt

```text
Write only Python source. Implement def generate(level=1, **kwargs).
Task: ce113_q01_negative_fraction_subtraction (rational_arithmetic, difficulty level 1).
Task specification: math16_negative_fraction_subtraction.
Frozen sampled parameters: {"expression": "3/7 - (-1/4)"}
generate() must return a dict with exactly question_text, correct_answer, and oracle_payload. question_text must use formal LaTeX delimiters. correct_answer must include numerator, denominator, and canonical_latex for an irreducible fraction. oracle_payload must exactly equal the frozen sampled parameters. Do not use input, files, network, subprocess, Markdown fences, or explanations.

## Clean-incremental GENERIC
Output complete Python source only. Do not use Markdown fences or explanatory prose. Preserve frozen parameters exactly. Verify that generate() exists. Verify that the return value has exactly the three required top-level keys. Verify field types match the stated contract and that oracle_payload equals the frozen parameters.
```

---

## 題目13：ce112_q12_independent_probability_fraction

- **Domain**：rational_arithmetic
- **Condition**：ab2g
- **Frozen seed／parameters**：`seed=2026071301` / `{"p1": [2, 6], "p2": [1, 5]}`
- **Answer contract**：d. question_text must use formal LaTeX delimiters. correct_answer must include numerator, denominator, and canonical_latex for an irreducible fraction.
- **Prompt SHA-256**：`d68af74fd5f59ae1178e9835684479397bd58a2b1f31fd9ef7b022e34b96fcf1`
- **適用模型**：Gemini 3.5 Flash／Qwen 3.5 4B／Qwen 3.5 9B
- **Prompt版本基準**：Current SSOT version (consistent with Qwen run_002)

### 實際送模Prompt

```text
Write only Python source. Implement def generate(level=1, **kwargs).
Task: ce112_q12_independent_probability_fraction (rational_arithmetic, difficulty level 1).
Task specification: math16_independent_probability_fraction.
Frozen sampled parameters: {"p1": [2, 6], "p2": [1, 5]}
generate() must return a dict with exactly question_text, correct_answer, and oracle_payload. question_text must use formal LaTeX delimiters. correct_answer must include numerator, denominator, and canonical_latex for an irreducible fraction. oracle_payload must exactly equal the frozen sampled parameters. Do not use input, files, network, subprocess, Markdown fences, or explanations.

## Clean-incremental GENERIC
Output complete Python source only. Do not use Markdown fences or explanatory prose. Preserve frozen parameters exactly. Verify that generate() exists. Verify that the return value has exactly the three required top-level keys. Verify field types match the stated contract and that oracle_payload equals the frozen parameters.
```

---

## 題目14：ce112_q04_radical_simplification

- **Domain**：radicals
- **Condition**：ab2g
- **Frozen seed／parameters**：`seed=2026071301` / `{"radicand": 135}`
- **Answer contract**：d. question_text must use formal LaTeX delimiters. correct_answer must include coefficient, radicand, and canonical_latex.
- **Prompt SHA-256**：`6d252e1058c14eee07326788693fec710a5247c404e7dd74f3d22156235a82f4`
- **適用模型**：Gemini 3.5 Flash／Qwen 3.5 4B／Qwen 3.5 9B
- **Prompt版本基準**：Current SSOT version (consistent with Qwen run_002)

### 實際送模Prompt

```text
Write only Python source. Implement def generate(level=1, **kwargs).
Task: ce112_q04_radical_simplification (radicals, difficulty level 1).
Task specification: math16_radical_simplification_fixed.
Frozen sampled parameters: {"radicand": 135}
generate() must return a dict with exactly question_text, correct_answer, and oracle_payload. question_text must use formal LaTeX delimiters. correct_answer must include coefficient, radicand, and canonical_latex. oracle_payload must exactly equal the frozen sampled parameters. Do not use input, files, network, subprocess, Markdown fences, or explanations.

## Clean-incremental GENERIC
Output complete Python source only. Do not use Markdown fences or explanatory prose. Preserve frozen parameters exactly. Verify that generate() exists. Verify that the return value has exactly the three required top-level keys. Verify field types match the stated contract and that oracle_payload equals the frozen parameters.
```

---

## 題目15：ce111_q10_ordered_quadratic_roots_radical

- **Domain**：radicals
- **Condition**：ab2g
- **Frozen seed／parameters**：`seed=2026071301` / `{"equation": "(x-2)^2=3", "order": "a>b", "target": "2a+b"}`
- **Answer contract**：d. question_text must use formal LaTeX delimiters. correct_answer must include result with rational, radical_coefficient (may be +1 or -1), radicand, and canonical_latex. Structured comparison is required; do not rely on string-only equality.
- **Prompt SHA-256**：`6179a8fb58654189712d53044e6df49b7171ccf57f1b1666d3e735f38758a766`
- **適用模型**：Gemini 3.5 Flash／Qwen 3.5 4B／Qwen 3.5 9B
- **Prompt版本基準**：Current SSOT version (consistent with Qwen run_002)

### 實際送模Prompt

```text
Write only Python source. Implement def generate(level=1, **kwargs).
Task: ce111_q10_ordered_quadratic_roots_radical (radicals, difficulty level 1).
Task specification: math16_ordered_quadratic_roots_radical.
Frozen sampled parameters: {"equation": "(x-2)^2=3", "order": "a>b", "target": "2a+b"}
generate() must return a dict with exactly question_text, correct_answer, and oracle_payload. question_text must use formal LaTeX delimiters. correct_answer must include result with rational, radical_coefficient (may be +1 or -1), radicand, and canonical_latex. Structured comparison is required; do not rely on string-only equality. oracle_payload must exactly equal the frozen sampled parameters. Do not use input, files, network, subprocess, Markdown fences, or explanations.

## Clean-incremental GENERIC
Output complete Python source only. Do not use Markdown fences or explanatory prose. Preserve frozen parameters exactly. Verify that generate() exists. Verify that the return value has exactly the three required top-level keys. Verify field types match the stated contract and that oracle_payload equals the frozen parameters.
```

---

## 題目16：ce113_q11_rationalize_denominator

- **Domain**：radicals
- **Condition**：ab2g
- **Frozen seed／parameters**：`seed=2026071301` / `{"numerator": 9, "denominator": "4-sqrt(7)", "radicand": 7}`
- **Answer contract**：d. question_text must use formal LaTeX delimiters where math appears. correct_answer must be a single exact integer.
- **Prompt SHA-256**：`61d3826e10d9cccb5d18a02c8aa951421bd38216d4cd773792201aac261778a7`
- **適用模型**：Gemini 3.5 Flash／Qwen 3.5 4B／Qwen 3.5 9B
- **Prompt版本基準**：Current SSOT version (consistent with Qwen run_002)

### 實際送模Prompt

```text
Write only Python source. Implement def generate(level=1, **kwargs).
Task: ce113_q11_rationalize_denominator (radicals, difficulty level 1).
Task specification: math16_rationalize_denominator_ab_sum.
Frozen sampled parameters: {"denominator": "4-sqrt(7)", "numerator": 9, "radicand": 7}
generate() must return a dict with exactly question_text, correct_answer, and oracle_payload. question_text must use formal LaTeX delimiters where math appears. correct_answer must be a single exact integer. oracle_payload must exactly equal the frozen sampled parameters. Do not use input, files, network, subprocess, Markdown fences, or explanations.

## Clean-incremental GENERIC
Output complete Python source only. Do not use Markdown fences or explanatory prose. Preserve frozen parameters exactly. Verify that generate() exists. Verify that the return value has exactly the three required top-level keys. Verify field types match the stated contract and that oracle_payload equals the frozen parameters.
```

---
