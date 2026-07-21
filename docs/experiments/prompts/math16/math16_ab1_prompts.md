# Math16 Ab1 (Native Baseline) Prompts

- **實驗條件定義**: Ab1 (Native baseline) 為模型原生提示模式。提示詞僅包含基本任務描述、frozen parameters 以及輸出格式契約 (answer contract)，不添加任何格式或安全鷹架。
- **Prompt組裝來源**: 經由 `agent_tools/finals_rebuild/ce115_clean_incremental_ablation.py` 中的 `build_condition_prompt("ab1", task, frozen)` 程式化組裝。
- **Prompt版本**: 與 Qwen 4B/9B 正式 `run_002` 實驗及後續 Gemini `run_003_multiseed` 採用的正式版本一致。
- **生成日期**: 2026-07-21
- **16題完整性檢查結果**: 經程式化檢查，16題題目、參數與輸出格式完全齊備，無缺失、無截斷。
- **文件SHA-256產生方式**: 使用 `prompt_sha256(prompt)`（計算記憶體中 UTF-8 編碼且換行符為 LF 的 Prompt 字串 SHA-256 哈希值）。

---

## 題目01：ce115_calc_polynomial_division_l1

- **Domain**：polynomials
- **Condition**：ab1
- **Frozen seed／parameters**：`seed=2026071301` / `{"dividend_coefficients": [6, 0, 6], "divisor_coefficients": [1, -4]}`
- **Answer contract**：d. question_text must use formal LaTeX delimiters \( \) / \[ \]. correct_answer must include quotient_coefficients, remainder_coefficients, quotient_latex, and remainder_latex. Exact arithmetic; no floats.
- **Prompt SHA-256**：`fdf193cdb3bf18cbd3e37627168fd1824042198d278b2a45114ddc8bacd8ff86`
- **適用模型**：Gemini 3.5 Flash／Qwen 3.5 4B／Qwen 3.5 9B
- **Prompt版本基準**：Current SSOT version (consistent with Qwen run_002)

### 實際送模Prompt

```text
Write only Python source. Implement def generate(level=1, **kwargs).
Task: ce115_calc_polynomial_division_l1 (polynomials, difficulty level 1).
Task specification: math16_polynomial_division_general.
Frozen sampled parameters: {"dividend_coefficients": [6, 0, 6], "divisor_coefficients": [1, -4]}
generate() must return a dict with exactly question_text, correct_answer, and oracle_payload. question_text must use formal LaTeX delimiters \( \) / \[ \]. correct_answer must include quotient_coefficients, remainder_coefficients, quotient_latex, and remainder_latex. Exact arithmetic; no floats. oracle_payload must exactly equal the frozen sampled parameters. Do not use input, files, network, subprocess, Markdown fences, or explanations.
```

---

## 題目02：ce115_calc_polynomial_factor_roots_l1

- **Domain**：polynomials
- **Condition**：ab1
- **Frozen seed／parameters**：`seed=2026071301` / `{"quadratic_coefficients": [1, 4, -12]}`
- **Answer contract**：d. question_text must use formal LaTeX delimiters. correct_answer must include roots (ascending), factorization_latex, and roots_latex. Exact arithmetic; no floats.
- **Prompt SHA-256**：`62fcdc20f64c26274f92f2d05134f84475477eacfec37cfadae8f5dd3505e50e`
- **適用模型**：Gemini 3.5 Flash／Qwen 3.5 4B／Qwen 3.5 9B
- **Prompt版本基準**：Current SSOT version (consistent with Qwen run_002)

### 實際送模Prompt

```text
Write only Python source. Implement def generate(level=1, **kwargs).
Task: ce115_calc_polynomial_factor_roots_l1 (polynomials, difficulty level 1).
Task specification: math16_polynomial_factor_roots.
Frozen sampled parameters: {"quadratic_coefficients": [1, 4, -12]}
generate() must return a dict with exactly question_text, correct_answer, and oracle_payload. question_text must use formal LaTeX delimiters. correct_answer must include roots (ascending), factorization_latex, and roots_latex. Exact arithmetic; no floats. oracle_payload must exactly equal the frozen sampled parameters. Do not use input, files, network, subprocess, Markdown fences, or explanations.
```

---

## 題目03：ce115_calc_exact_rational_expression_l1

- **Domain**：rational_arithmetic
- **Condition**：ab1
- **Frozen seed／parameters**：`seed=2026071301` / `{"products": [{"sign": 1, "left": "2.79", "right": "89.3"}, {"sign": -1, "left": "-0.21", "right": "89.3"}]}`
- **Answer contract**：d. question_text must use formal LaTeX delimiters. correct_answer must include value (irreducible p/q string) and canonical_latex. Exact arithmetic; no floats.
- **Prompt SHA-256**：`c7bff96c64c0aa9785092575c7f89ece51cd11d03c72c8f801c6b629d791a0ec`
- **適用模型**：Gemini 3.5 Flash／Qwen 3.5 4B／Qwen 3.5 9B
- **Prompt版本基準**：Current SSOT version (consistent with Qwen run_002)

### 實際送模Prompt

```text
Write only Python source. Implement def generate(level=1, **kwargs).
Task: ce115_calc_exact_rational_expression_l1 (rational_arithmetic, difficulty level 1).
Task specification: math16_exact_rational_expression.
Frozen sampled parameters: {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}
generate() must return a dict with exactly question_text, correct_answer, and oracle_payload. question_text must use formal LaTeX delimiters. correct_answer must include value (irreducible p/q string) and canonical_latex. Exact arithmetic; no floats. oracle_payload must exactly equal the frozen sampled parameters. Do not use input, files, network, subprocess, Markdown fences, or explanations.
```

---

## 題目04：ce115_calc_radical_simplification_l1

- **Domain**：radicals
- **Condition**：ab1
- **Frozen seed／parameters**：`seed=2026071301` / `{"radicand": 27}`
- **Answer contract**：d. question_text must use formal LaTeX delimiters. correct_answer must include coefficient, radicand, and canonical_latex. Exact integers only; no floats.
- **Prompt SHA-256**：`2a445d5de76c068590ce05619f521eff42098c71257319bf12d82796d4d92f86`
- **適用模型**：Gemini 3.5 Flash／Qwen 3.5 4B／Qwen 3.5 9B
- **Prompt版本基準**：Current SSOT version (consistent with Qwen run_002)

### 實際送模Prompt

```text
Write only Python source. Implement def generate(level=1, **kwargs).
Task: ce115_calc_radical_simplification_l1 (radicals, difficulty level 1).
Task specification: math16_radical_simplification.
Frozen sampled parameters: {"radicand": 27}
generate() must return a dict with exactly question_text, correct_answer, and oracle_payload. question_text must use formal LaTeX delimiters. correct_answer must include coefficient, radicand, and canonical_latex. Exact integers only; no floats. oracle_payload must exactly equal the frozen sampled parameters. Do not use input, files, network, subprocess, Markdown fences, or explanations.
```

---

## 題目05：ce111_q02_polynomial_division_remainder

- **Domain**：polynomials
- **Condition**：ab1
- **Frozen seed／parameters**：`seed=2026071301` / `{"dividend_coefficients": [6, 4, 0], "divisor_coefficients": [2, 0, 0]}`
- **Answer contract**：d. question_text must use formal LaTeX delimiters. correct_answer must include only remainder and canonical_latex (quotient is not scored).
- **Prompt SHA-256**：`138e8eae8822fb96a655fd1cfb5c14873f5397fb4b5a09ed617defd5fc0e42e5`
- **適用模型**：Gemini 3.5 Flash／Qwen 3.5 4B／Qwen 3.5 9B
- **Prompt版本基準**：Current SSOT version (consistent with Qwen run_002)

### 實際送模Prompt

```text
Write only Python source. Implement def generate(level=1, **kwargs).
Task: ce111_q02_polynomial_division_remainder (polynomials, difficulty level 1).
Task specification: math16_polynomial_division_remainder_only.
Frozen sampled parameters: {"dividend_coefficients": [6, 4, 0], "divisor_coefficients": [2, 0, 0]}
generate() must return a dict with exactly question_text, correct_answer, and oracle_payload. question_text must use formal LaTeX delimiters. correct_answer must include only remainder and canonical_latex (quotient is not scored). oracle_payload must exactly equal the frozen sampled parameters. Do not use input, files, network, subprocess, Markdown fences, or explanations.
```

---

## 題目06：ce111_q08_polynomial_factor_parameter_recovery

- **Domain**：polynomials
- **Condition**：ab1
- **Frozen seed／parameters**：`seed=2026071301` / `{"quadratic_coefficients": [39, 5, -14], "template_left_x_coefficient": 3, "factor_order_policy": "strict_source_template"}`
- **Answer contract**：d. question_text must use formal LaTeX delimiters. factor_order_policy is strict_source_template: first factor is fixed as (3x+a). correct_answer must be the integer a+2c. Do not redefine parameters after swapping factors.
- **Prompt SHA-256**：`447f8b48f394c373b3fa8d7fa4d11932cdce5b411bbf27f61cc9e822b2670cd4`
- **適用模型**：Gemini 3.5 Flash／Qwen 3.5 4B／Qwen 3.5 9B
- **Prompt版本基準**：Current SSOT version (consistent with Qwen run_002)

### 實際送模Prompt

```text
Write only Python source. Implement def generate(level=1, **kwargs).
Task: ce111_q08_polynomial_factor_parameter_recovery (polynomials, difficulty level 1).
Task specification: math16_polynomial_factor_parameter_recovery.
Frozen sampled parameters: {"factor_order_policy": "strict_source_template", "quadratic_coefficients": [39, 5, -14], "template_left_x_coefficient": 3}
generate() must return a dict with exactly question_text, correct_answer, and oracle_payload. question_text must use formal LaTeX delimiters. factor_order_policy is strict_source_template: first factor is fixed as (3x+a). correct_answer must be the integer a+2c. Do not redefine parameters after swapping factors. oracle_payload must exactly equal the frozen sampled parameters. Do not use input, files, network, subprocess, Markdown fences, or explanations.
```

---

## 題目07：ce111_q03_prime_factor_selection

- **Domain**：integers
- **Condition**：ab1
- **Frozen seed／parameters**：`seed=2026071301` / `{"candidates": [11, 12, 13, 14], "n": 156}`
- **Answer contract**：d. question_text must use formal LaTeX delimiters where math appears. correct_answer must be a single exact integer.
- **Prompt SHA-256**：`398a9ab7067574286a3f7b6a955033b2f3af8d244d34098aa907623bb706bcc4`
- **適用模型**：Gemini 3.5 Flash／Qwen 3.5 4B／Qwen 3.5 9B
- **Prompt版本基準**：Current SSOT version (consistent with Qwen run_002)

### 實際送模Prompt

```text
Write only Python source. Implement def generate(level=1, **kwargs).
Task: ce111_q03_prime_factor_selection (integers, difficulty level 1).
Task specification: math16_prime_factor_selection.
Frozen sampled parameters: {"candidates": [11, 12, 13, 14], "n": 156}
generate() must return a dict with exactly question_text, correct_answer, and oracle_payload. question_text must use formal LaTeX delimiters where math appears. correct_answer must be a single exact integer. oracle_payload must exactly equal the frozen sampled parameters. Do not use input, files, network, subprocess, Markdown fences, or explanations.
```

---

## 題目08：ce112_q01_negative_integer_power

- **Domain**：integers
- **Condition**：ab1
- **Frozen seed／parameters**：`seed=2026071301` / `{"base": -3, "exponent": 3}`
- **Answer contract**：d. question_text must use formal LaTeX delimiters where math appears. correct_answer must be a single exact integer.
- **Prompt SHA-256**：`d7f97e59388da3962bab6c3b0b55ebacdb7679340bf7955215431120c98301c9`
- **適用模型**：Gemini 3.5 Flash／Qwen 3.5 4B／Qwen 3.5 9B
- **Prompt版本基準**：Current SSOT version (consistent with Qwen run_002)

### 實際送模Prompt

```text
Write only Python source. Implement def generate(level=1, **kwargs).
Task: ce112_q01_negative_integer_power (integers, difficulty level 1).
Task specification: math16_negative_integer_power.
Frozen sampled parameters: {"base": -3, "exponent": 3}
generate() must return a dict with exactly question_text, correct_answer, and oracle_payload. question_text must use formal LaTeX delimiters where math appears. correct_answer must be a single exact integer. oracle_payload must exactly equal the frozen sampled parameters. Do not use input, files, network, subprocess, Markdown fences, or explanations.
```

---

## 題目09：ce112_q09_divisor_multiple_intersection

- **Domain**：integers
- **Condition**：ab1
- **Frozen seed／parameters**：`seed=2026071301` / `{"multiple_of": 18, "divisor_of": 216}`
- **Answer contract**：d. question_text must use formal LaTeX delimiters where math appears. correct_answer must be a JSON-compatible dict with exactly count (int).
- **Prompt SHA-256**：`7eafd0610772ae6f3576a2d7d24017b28f0195d01e3b713feb8a6b629a79148e`
- **適用模型**：Gemini 3.5 Flash／Qwen 3.5 4B／Qwen 3.5 9B
- **Prompt版本基準**：Current SSOT version (consistent with Qwen run_002)

### 實際送模Prompt

```text
Write only Python source. Implement def generate(level=1, **kwargs).
Task: ce112_q09_divisor_multiple_intersection (integers, difficulty level 1).
Task specification: math16_divisor_multiple_intersection.
Frozen sampled parameters: {"divisor_of": 216, "multiple_of": 18}
generate() must return a dict with exactly question_text, correct_answer, and oracle_payload. question_text must use formal LaTeX delimiters where math appears. correct_answer must be a JSON-compatible dict with exactly count (int). oracle_payload must exactly equal the frozen sampled parameters. Do not use input, files, network, subprocess, Markdown fences, or explanations.
```

---

## 題目10：ce111_nonchoice_q01_part1_exponential_growth

- **Domain**：integers
- **Condition**：ab1
- **Frozen seed／parameters**：`seed=2026071301` / `{"initial": 1, "split_factor": 4, "hours_per_generation": 20, "days": 15}`
- **Answer contract**：d. question_text must use formal LaTeX delimiters where math appears. correct_answer must be a JSON-compatible dict with exactly k (int).
- **Prompt SHA-256**：`105840296a8d546e9ca86a9aa27cf92df5da24004f78624f5fd96e031b114d62`
- **適用模型**：Gemini 3.5 Flash／Qwen 3.5 4B／Qwen 3.5 9B
- **Prompt版本基準**：Current SSOT version (consistent with Qwen run_002)

### 實際送模Prompt

```text
Write only Python source. Implement def generate(level=1, **kwargs).
Task: ce111_nonchoice_q01_part1_exponential_growth (integers, difficulty level 1).
Task specification: math16_exponential_growth_generation_count.
Frozen sampled parameters: {"days": 15, "hours_per_generation": 20, "initial": 1, "split_factor": 4}
generate() must return a dict with exactly question_text, correct_answer, and oracle_payload. question_text must use formal LaTeX delimiters where math appears. correct_answer must be a JSON-compatible dict with exactly k (int). oracle_payload must exactly equal the frozen sampled parameters. Do not use input, files, network, subprocess, Markdown fences, or explanations.
```

---

## 題目11：ce111_q05_exact_fraction_expression

- **Domain**：rational_arithmetic
- **Condition**：ab1
- **Frozen seed／parameters**：`seed=2026071301` / `{"expression": "9/22 + 11/18 - (23/22 - 7/18)"}`
- **Answer contract**：d. question_text must use formal LaTeX delimiters. correct_answer must include numerator, denominator, and canonical_latex for an irreducible fraction.
- **Prompt SHA-256**：`321d4fd2830ebc32bfbb64fefd30735af2260cffbb4d5ce695cfe030ca6e2ece`
- **適用模型**：Gemini 3.5 Flash／Qwen 3.5 4B／Qwen 3.5 9B
- **Prompt版本基準**：Current SSOT version (consistent with Qwen run_002)

### 實際送模Prompt

```text
Write only Python source. Implement def generate(level=1, **kwargs).
Task: ce111_q05_exact_fraction_expression (rational_arithmetic, difficulty level 1).
Task specification: math16_exact_fraction_expression.
Frozen sampled parameters: {"expression": "9/22 + 11/18 - (23/22 - 7/18)"}
generate() must return a dict with exactly question_text, correct_answer, and oracle_payload. question_text must use formal LaTeX delimiters. correct_answer must include numerator, denominator, and canonical_latex for an irreducible fraction. oracle_payload must exactly equal the frozen sampled parameters. Do not use input, files, network, subprocess, Markdown fences, or explanations.
```

---

## 題目12：ce113_q01_negative_fraction_subtraction

- **Domain**：rational_arithmetic
- **Condition**：ab1
- **Frozen seed／parameters**：`seed=2026071301` / `{"expression": "3/7 - (-1/4)"}`
- **Answer contract**：d. question_text must use formal LaTeX delimiters. correct_answer must include numerator, denominator, and canonical_latex for an irreducible fraction.
- **Prompt SHA-256**：`d690b208e09d5f893ecd8b8abc38b4abb7d044968dc42c60dde3de96c0ad410d`
- **適用模型**：Gemini 3.5 Flash／Qwen 3.5 4B／Qwen 3.5 9B
- **Prompt版本基準**：Current SSOT version (consistent with Qwen run_002)

### 實際送模Prompt

```text
Write only Python source. Implement def generate(level=1, **kwargs).
Task: ce113_q01_negative_fraction_subtraction (rational_arithmetic, difficulty level 1).
Task specification: math16_negative_fraction_subtraction.
Frozen sampled parameters: {"expression": "3/7 - (-1/4)"}
generate() must return a dict with exactly question_text, correct_answer, and oracle_payload. question_text must use formal LaTeX delimiters. correct_answer must include numerator, denominator, and canonical_latex for an irreducible fraction. oracle_payload must exactly equal the frozen sampled parameters. Do not use input, files, network, subprocess, Markdown fences, or explanations.
```

---

## 題目13：ce112_q12_independent_probability_fraction

- **Domain**：rational_arithmetic
- **Condition**：ab1
- **Frozen seed／parameters**：`seed=2026071301` / `{"p1": [2, 6], "p2": [1, 5]}`
- **Answer contract**：d. question_text must use formal LaTeX delimiters. correct_answer must include numerator, denominator, and canonical_latex for an irreducible fraction.
- **Prompt SHA-256**：`ce709937aef3026d48af8ea0b6eb6dbc53d0c07731b232df03b0657672d7d74c`
- **適用模型**：Gemini 3.5 Flash／Qwen 3.5 4B／Qwen 3.5 9B
- **Prompt版本基準**：Current SSOT version (consistent with Qwen run_002)

### 實際送模Prompt

```text
Write only Python source. Implement def generate(level=1, **kwargs).
Task: ce112_q12_independent_probability_fraction (rational_arithmetic, difficulty level 1).
Task specification: math16_independent_probability_fraction.
Frozen sampled parameters: {"p1": [2, 6], "p2": [1, 5]}
generate() must return a dict with exactly question_text, correct_answer, and oracle_payload. question_text must use formal LaTeX delimiters. correct_answer must include numerator, denominator, and canonical_latex for an irreducible fraction. oracle_payload must exactly equal the frozen sampled parameters. Do not use input, files, network, subprocess, Markdown fences, or explanations.
```

---

## 題目14：ce112_q04_radical_simplification

- **Domain**：radicals
- **Condition**：ab1
- **Frozen seed／parameters**：`seed=2026071301` / `{"radicand": 135}`
- **Answer contract**：d. question_text must use formal LaTeX delimiters. correct_answer must include coefficient, radicand, and canonical_latex.
- **Prompt SHA-256**：`f696edca9ba89d8daf6ae0a01bef98c0098c508517ba9d6e631b287fa5764d53`
- **適用模型**：Gemini 3.5 Flash／Qwen 3.5 4B／Qwen 3.5 9B
- **Prompt版本基準**：Current SSOT version (consistent with Qwen run_002)

### 實際送模Prompt

```text
Write only Python source. Implement def generate(level=1, **kwargs).
Task: ce112_q04_radical_simplification (radicals, difficulty level 1).
Task specification: math16_radical_simplification_fixed.
Frozen sampled parameters: {"radicand": 135}
generate() must return a dict with exactly question_text, correct_answer, and oracle_payload. question_text must use formal LaTeX delimiters. correct_answer must include coefficient, radicand, and canonical_latex. oracle_payload must exactly equal the frozen sampled parameters. Do not use input, files, network, subprocess, Markdown fences, or explanations.
```

---

## 題目15：ce111_q10_ordered_quadratic_roots_radical

- **Domain**：radicals
- **Condition**：ab1
- **Frozen seed／parameters**：`seed=2026071301` / `{"equation": "(x-2)^2=3", "order": "a>b", "target": "2a+b"}`
- **Answer contract**：d. question_text must use formal LaTeX delimiters. correct_answer must include result with rational, radical_coefficient (may be +1 or -1), radicand, and canonical_latex. Structured comparison is required; do not rely on string-only equality.
- **Prompt SHA-256**：`8371aff72b11bd70ea327920302233f5b7d60c0e6e594daa5ce635ef386d56fb`
- **適用模型**：Gemini 3.5 Flash／Qwen 3.5 4B／Qwen 3.5 9B
- **Prompt版本基準**：Current SSOT version (consistent with Qwen run_002)

### 實際送模Prompt

```text
Write only Python source. Implement def generate(level=1, **kwargs).
Task: ce111_q10_ordered_quadratic_roots_radical (radicals, difficulty level 1).
Task specification: math16_ordered_quadratic_roots_radical.
Frozen sampled parameters: {"equation": "(x-2)^2=3", "order": "a>b", "target": "2a+b"}
generate() must return a dict with exactly question_text, correct_answer, and oracle_payload. question_text must use formal LaTeX delimiters. correct_answer must include result with rational, radical_coefficient (may be +1 or -1), radicand, and canonical_latex. Structured comparison is required; do not rely on string-only equality. oracle_payload must exactly equal the frozen sampled parameters. Do not use input, files, network, subprocess, Markdown fences, or explanations.
```

---

## 題目16：ce113_q11_rationalize_denominator

- **Domain**：radicals
- **Condition**：ab1
- **Frozen seed／parameters**：`seed=2026071301` / `{"numerator": 9, "denominator": "4-sqrt(7)", "radicand": 7}`
- **Answer contract**：d. question_text must use formal LaTeX delimiters where math appears. correct_answer must be a single exact integer.
- **Prompt SHA-256**：`16c617438948cbd476c48addcd9cfc9b61c804e3e01b852d5a0eafb883cb34ce`
- **適用模型**：Gemini 3.5 Flash／Qwen 3.5 4B／Qwen 3.5 9B
- **Prompt版本基準**：Current SSOT version (consistent with Qwen run_002)

### 實際送模Prompt

```text
Write only Python source. Implement def generate(level=1, **kwargs).
Task: ce113_q11_rationalize_denominator (radicals, difficulty level 1).
Task specification: math16_rationalize_denominator_ab_sum.
Frozen sampled parameters: {"denominator": "4-sqrt(7)", "numerator": 9, "radicand": 7}
generate() must return a dict with exactly question_text, correct_answer, and oracle_payload. question_text must use formal LaTeX delimiters where math appears. correct_answer must be a single exact integer. oracle_payload must exactly equal the frozen sampled parameters. Do not use input, files, network, subprocess, Markdown fences, or explanations.
```

---
