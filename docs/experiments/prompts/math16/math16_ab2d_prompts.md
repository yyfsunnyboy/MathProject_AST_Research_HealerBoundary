# Math16 Ab2d (Domain Scaffold) Prompts

- **實驗條件定義**: Ab2d (Domain scaffold) 在 Ab2g 基礎上進一步增加了題型限定的 Domain API 說明。在提示詞尾部附加 `## Clean-incremental DOMAIN` 區塊，提供該題運算所需的 task-local Domain API（如 `PolynomialOps`、`RadicalOps` 等）之 signature 與 returns 說明，並引導模型在 `generate` 中採用。
- **Prompt組裝來源**: 經由 `agent_tools/finals_rebuild/ce115_clean_incremental_ablation.py` 中的 `build_condition_prompt("ab2d", task, frozen)` 程式化組裝。
- **Prompt版本**: 與 Qwen 4B/9B 正式 `run_002` 實驗及後續 Gemini `run_003_multiseed` 採用的正式版本一致。
- **生成日期**: 2026-07-21
- **16題完整性檢查結果**: 經程式化檢查，16題題目、參數、通用鷹架與 Domain API 區塊完全齊備，無任何缺失或截斷。
- **文件SHA-256產生方式**: 使用 `prompt_sha256(prompt)`（計算記憶體中 UTF-8 編碼且換行符為 LF 的 Prompt 字串 SHA-256 哈希值）。

---

## 題目01：ce115_calc_polynomial_division_l1

- **Domain**：polynomials
- **Condition**：ab2d
- **Frozen seed／parameters**：`seed=2026071301` / `{"dividend_coefficients": [6, 0, 6], "divisor_coefficients": [1, -4]}`
- **Answer contract**：d. question_text must use formal LaTeX delimiters \( \) / \[ \]. correct_answer must include quotient_coefficients, remainder_coefficients, quotient_latex, and remainder_latex. Exact arithmetic; no floats.
- **Prompt SHA-256**：`79b1936f146728f178f71569aa7cab9c2d284ace6e3fa97604a96c7b97f250d0`
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

## Clean-incremental DOMAIN
Task-local domain APIs (use only these):
- `PolynomialOps.div_qr` | import: `core.prompts.domain_function_library` | signature: `(dividend_coefficients, divisor_coefficients)` | returns: tuple[list[int | str], list[int | str]]  # quotient,remainder
Use the listed domain API for each supported core operation, and ensure the returned value contributes to correct_answer.
```

---

## 題目02：ce115_calc_polynomial_factor_roots_l1

- **Domain**：polynomials
- **Condition**：ab2d
- **Frozen seed／parameters**：`seed=2026071301` / `{"quadratic_coefficients": [1, 4, -12]}`
- **Answer contract**：d. question_text must use formal LaTeX delimiters. correct_answer must include roots (ascending), factorization_latex, and roots_latex. Exact arithmetic; no floats.
- **Prompt SHA-256**：`46eb44551fe48e5def0a14fdfe506b30e5987c44c0dee69f259bf42b90ab54a0`
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

## Clean-incremental DOMAIN
Task-local domain APIs (use only these):
- `PolynomialOps.factor_quadratic_exact` | import: `core.prompts.domain_function_library` | signature: `(a, b, c)` | returns: list[dict, dict]  # fixed length 2; keys x_coefficient,constant; int or 'p/q'; NOT a 3-tuple
- `FractionOps.create` | import: `core.prompts.domain_function_library` | signature: `(value)` | returns: Fraction  # not JSON serializable; use the to_exact adapter
Use the listed domain API for each supported core operation, and ensure the returned value contributes to correct_answer.
```

---

## 題目03：ce115_calc_exact_rational_expression_l1

- **Domain**：rational_arithmetic
- **Condition**：ab2d
- **Frozen seed／parameters**：`seed=2026071301` / `{"products": [{"sign": 1, "left": "2.79", "right": "89.3"}, {"sign": -1, "left": "-0.21", "right": "89.3"}]}`
- **Answer contract**：d. question_text must use formal LaTeX delimiters. correct_answer must include value (irreducible p/q string) and canonical_latex. Exact arithmetic; no floats.
- **Prompt SHA-256**：`ccc56c41370e2b807299372da9b9af0d6807abf4dbae441990b16044d5108244`
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

## Clean-incremental DOMAIN
Task-local domain APIs (use only these):
- `FractionOps.create` | import: `core.prompts.domain_function_library` | signature: `(value)` | returns: Fraction  # not JSON serializable; use the to_exact adapter
- `FractionOps.mul` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: Fraction
- `FractionOps.add` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: Fraction
Use the listed domain API for each supported core operation, and ensure the returned value contributes to correct_answer.
```

---

## 題目04：ce115_calc_radical_simplification_l1

- **Domain**：radicals
- **Condition**：ab2d
- **Frozen seed／parameters**：`seed=2026071301` / `{"radicand": 27}`
- **Answer contract**：d. question_text must use formal LaTeX delimiters. correct_answer must include coefficient, radicand, and canonical_latex. Exact integers only; no floats.
- **Prompt SHA-256**：`7277f140eeaadbdfe1f64a2215413acadf06fb134b09efa280f2011d19e5588c`
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

## Clean-incremental DOMAIN
Task-local domain APIs (use only these):
- `RadicalOps.simplify_term` | import: `core.prompts.domain_function_library` | signature: `(coeff, radicand)` | returns: tuple[int | Fraction, int]  # semantic (coefficient, square-free radicand)
Use the listed domain API for each supported core operation, and ensure the returned value contributes to correct_answer.
```

---

## 題目05：ce111_q02_polynomial_division_remainder

- **Domain**：polynomials
- **Condition**：ab2d
- **Frozen seed／parameters**：`seed=2026071301` / `{"dividend_coefficients": [6, 4, 0], "divisor_coefficients": [2, 0, 0]}`
- **Answer contract**：d. question_text must use formal LaTeX delimiters. correct_answer must include only remainder and canonical_latex (quotient is not scored).
- **Prompt SHA-256**：`d625ce0bed3b073c6289454121ab9960e1c1965a824c9db6a575d7ecbd3c0aa9`
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

## Clean-incremental DOMAIN
Task-local domain APIs (use only these):
- `PolynomialOps.div_qr` | import: `core.prompts.domain_function_library` | signature: `(dividend_coefficients, divisor_coefficients)` | returns: tuple[list[int | str], list[int | str]]  # quotient,remainder
- `PolynomialOps.format_latex` | import: `core.prompts.domain_function_library` | signature: `(coeffs, var='x')` | returns: str
Use the listed domain API for each supported core operation, and ensure the returned value contributes to correct_answer.
```

---

## 題目06：ce111_q08_polynomial_factor_parameter_recovery

- **Domain**：polynomials
- **Condition**：ab2d
- **Frozen seed／parameters**：`seed=2026071301` / `{"quadratic_coefficients": [39, 5, -14], "template_left_x_coefficient": 3, "factor_order_policy": "strict_source_template"}`
- **Answer contract**：d. question_text must use formal LaTeX delimiters. factor_order_policy is strict_source_template: first factor is fixed as (3x+a). correct_answer must be the integer a+2c. Do not redefine parameters after swapping factors.
- **Prompt SHA-256**：`7d993c836b9ef40b49f4c57d44a4c2e08ef6a895b0f2e522f0e7c029fba0a27a`
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

## Clean-incremental DOMAIN
Task-local domain APIs (use only these):
- `PolynomialOps.mul` | import: `core.prompts.domain_function_library` | signature: `(c1, c2)` | returns: list[int | float | Fraction]  # operand-dependent; highest degree first
- `FractionOps.create` | import: `core.prompts.domain_function_library` | signature: `(value)` | returns: Fraction  # not JSON serializable; use the to_exact adapter
Use the listed domain API for each supported core operation, and ensure the returned value contributes to correct_answer.
```

---

## 題目07：ce111_q03_prime_factor_selection

- **Domain**：integers
- **Condition**：ab2d
- **Frozen seed／parameters**：`seed=2026071301` / `{"candidates": [11, 12, 13, 14], "n": 156}`
- **Answer contract**：d. question_text must use formal LaTeX delimiters where math appears. correct_answer must be a single exact integer.
- **Prompt SHA-256**：`8704669323fb45ef6bd34331151b350845425d2d14e19b36c58bd2c2c86bc75f`
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

## Clean-incremental DOMAIN
Task-local domain APIs (use only these):
- `IntegerOps.is_divisible` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: bool
- `IntegerOps.safe_eval` | import: `core.prompts.domain_function_library` | signature: `(expr)` | returns: int | float  # bool and container results raise ValueError
Use the listed domain API for each supported core operation, and ensure the returned value contributes to correct_answer.
```

---

## 題目08：ce112_q01_negative_integer_power

- **Domain**：integers
- **Condition**：ab2d
- **Frozen seed／parameters**：`seed=2026071301` / `{"base": -3, "exponent": 3}`
- **Answer contract**：d. question_text must use formal LaTeX delimiters where math appears. correct_answer must be a single exact integer.
- **Prompt SHA-256**：`a03c40a37de8c5652476da0fcd76dfc714ca55c19b0279b0452358c81ccde8d4`
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

## Clean-incremental DOMAIN
Task-local domain APIs (use only these):
- `IntegerOps.safe_eval` | import: `core.prompts.domain_function_library` | signature: `(expr)` | returns: int | float  # bool and container results raise ValueError
- `IntegerOps.fmt_num` | import: `core.prompts.domain_function_library` | signature: `(n)` | returns: str
Use the listed domain API for each supported core operation, and ensure the returned value contributes to correct_answer.
```

---

## 題目09：ce112_q09_divisor_multiple_intersection

- **Domain**：integers
- **Condition**：ab2d
- **Frozen seed／parameters**：`seed=2026071301` / `{"multiple_of": 18, "divisor_of": 216}`
- **Answer contract**：d. question_text must use formal LaTeX delimiters where math appears. correct_answer must be a JSON-compatible dict with exactly count (int).
- **Prompt SHA-256**：`f4d5abe47b1d3dad2095dbc473b4f58b6f1c8cd4f9ece0ba8a1de9f5c68ad5cb`
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

## Clean-incremental DOMAIN
Task-local domain APIs (use only these):
- `IntegerOps.is_divisible` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: bool
- `IntegerOps.safe_eval` | import: `core.prompts.domain_function_library` | signature: `(expr)` | returns: int | float  # bool and container results raise ValueError
Use the listed domain API for each supported core operation, and ensure the returned value contributes to correct_answer.
```

---

## 題目10：ce111_nonchoice_q01_part1_exponential_growth

- **Domain**：integers
- **Condition**：ab2d
- **Frozen seed／parameters**：`seed=2026071301` / `{"initial": 1, "split_factor": 4, "hours_per_generation": 20, "days": 15}`
- **Answer contract**：d. question_text must use formal LaTeX delimiters where math appears. correct_answer must be a JSON-compatible dict with exactly k (int).
- **Prompt SHA-256**：`1f1491d3b68e9620550398001b27cd72e2f8b6c08c2debbf346396314a69cb42`
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

## Clean-incremental DOMAIN
Task-local domain APIs (use only these):
- `IntegerOps.safe_eval` | import: `core.prompts.domain_function_library` | signature: `(expr)` | returns: int | float  # bool and container results raise ValueError
- `IntegerOps.fmt_num` | import: `core.prompts.domain_function_library` | signature: `(n)` | returns: str
Use the listed domain API for each supported core operation, and ensure the returned value contributes to correct_answer.
```

---

## 題目11：ce111_q05_exact_fraction_expression

- **Domain**：rational_arithmetic
- **Condition**：ab2d
- **Frozen seed／parameters**：`seed=2026071301` / `{"expression": "9/22 + 11/18 - (23/22 - 7/18)"}`
- **Answer contract**：d. question_text must use formal LaTeX delimiters. correct_answer must include numerator, denominator, and canonical_latex for an irreducible fraction.
- **Prompt SHA-256**：`68a00937bf4cad2e185ea854b3d92e6fc9615ee0f045b5c86e81879b64976d4b`
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

## Clean-incremental DOMAIN
Task-local domain APIs (use only these):
- `FractionOps.create` | import: `core.prompts.domain_function_library` | signature: `(value)` | returns: Fraction  # not JSON serializable; use the to_exact adapter
- `FractionOps.add` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: Fraction
- `FractionOps.to_latex` | import: `core.prompts.domain_function_library` | signature: `(val, mixed=False)` | returns: str
Use the listed domain API for each supported core operation, and ensure the returned value contributes to correct_answer.
```

---

## 題目12：ce113_q01_negative_fraction_subtraction

- **Domain**：rational_arithmetic
- **Condition**：ab2d
- **Frozen seed／parameters**：`seed=2026071301` / `{"expression": "3/7 - (-1/4)"}`
- **Answer contract**：d. question_text must use formal LaTeX delimiters. correct_answer must include numerator, denominator, and canonical_latex for an irreducible fraction.
- **Prompt SHA-256**：`0fe4bd752d3760f08b8977916ba6edb99a7babd6cc53752bb9d80a684c8514f7`
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

## Clean-incremental DOMAIN
Task-local domain APIs (use only these):
- `FractionOps.create` | import: `core.prompts.domain_function_library` | signature: `(value)` | returns: Fraction  # not JSON serializable; use the to_exact adapter
- `FractionOps.sub` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: Fraction
- `FractionOps.to_latex` | import: `core.prompts.domain_function_library` | signature: `(val, mixed=False)` | returns: str
Use the listed domain API for each supported core operation, and ensure the returned value contributes to correct_answer.
```

---

## 題目13：ce112_q12_independent_probability_fraction

- **Domain**：rational_arithmetic
- **Condition**：ab2d
- **Frozen seed／parameters**：`seed=2026071301` / `{"p1": [2, 6], "p2": [1, 5]}`
- **Answer contract**：d. question_text must use formal LaTeX delimiters. correct_answer must include numerator, denominator, and canonical_latex for an irreducible fraction.
- **Prompt SHA-256**：`e0ceba6ddea69db946947e44372f0667b4445539f11857bbafa275c518a9506a`
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

## Clean-incremental DOMAIN
Task-local domain APIs (use only these):
- `FractionOps.create` | import: `core.prompts.domain_function_library` | signature: `(value)` | returns: Fraction  # not JSON serializable; use the to_exact adapter
- `FractionOps.mul` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: Fraction
- `FractionOps.to_latex` | import: `core.prompts.domain_function_library` | signature: `(val, mixed=False)` | returns: str
Use the listed domain API for each supported core operation, and ensure the returned value contributes to correct_answer.
```

---

## 題目14：ce112_q04_radical_simplification

- **Domain**：radicals
- **Condition**：ab2d
- **Frozen seed／parameters**：`seed=2026071301` / `{"radicand": 135}`
- **Answer contract**：d. question_text must use formal LaTeX delimiters. correct_answer must include coefficient, radicand, and canonical_latex.
- **Prompt SHA-256**：`f4766019ab80cfea7d15b358786ad841f542d8cd57b9dd61f4e7098712dba731`
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

## Clean-incremental DOMAIN
Task-local domain APIs (use only these):
- `RadicalOps.simplify_term` | import: `core.prompts.domain_function_library` | signature: `(coeff, radicand)` | returns: tuple[int | Fraction, int]  # semantic (coefficient, square-free radicand)
- `RadicalOps.format_term` | import: `core.prompts.domain_function_library` | signature: `(coeff, radicand, is_first=True)` | returns: str  # complete single-term LaTeX including coefficient/sign
Use the listed domain API for each supported core operation, and ensure the returned value contributes to correct_answer.
```

---

## 題目15：ce111_q10_ordered_quadratic_roots_radical

- **Domain**：radicals
- **Condition**：ab2d
- **Frozen seed／parameters**：`seed=2026071301` / `{"equation": "(x-2)^2=3", "order": "a>b", "target": "2a+b"}`
- **Answer contract**：d. question_text must use formal LaTeX delimiters. correct_answer must include result with rational, radical_coefficient (may be +1 or -1), radicand, and canonical_latex. Structured comparison is required; do not rely on string-only equality.
- **Prompt SHA-256**：`79e4e1abeee04352b1acfd797ec10815f2614f37bd4c94f0090c6ffef957d2c6`
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

## Clean-incremental DOMAIN
Task-local domain APIs (use only these):
- `RadicalOps.simplify_term` | import: `core.prompts.domain_function_library` | signature: `(coeff, radicand)` | returns: tuple[int | Fraction, int]  # semantic (coefficient, square-free radicand)
- `FractionOps.create` | import: `core.prompts.domain_function_library` | signature: `(value)` | returns: Fraction  # not JSON serializable; use the to_exact adapter
- `RadicalOps.format_expression` | import: `core.prompts.domain_function_library` | signature: `(terms_dict, denominator=1)` | returns: str  # complete compound-radical LaTeX
Use the listed domain API for each supported core operation, and ensure the returned value contributes to correct_answer.
```

---

## 題目16：ce113_q11_rationalize_denominator

- **Domain**：radicals
- **Condition**：ab2d
- **Frozen seed／parameters**：`seed=2026071301` / `{"numerator": 9, "denominator": "4-sqrt(7)", "radicand": 7}`
- **Answer contract**：d. question_text must use formal LaTeX delimiters where math appears. correct_answer must be a single exact integer.
- **Prompt SHA-256**：`9d3533f258e5c017845db746fbfb696ba432835385d9f38acf718a6bdff06514`
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

## Clean-incremental DOMAIN
Task-local domain APIs (use only these):
- `FractionOps.create` | import: `core.prompts.domain_function_library` | signature: `(value)` | returns: Fraction  # not JSON serializable; use the to_exact adapter
- `FractionOps.mul` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: Fraction
- `FractionOps.add` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: Fraction
Use the listed domain API for each supported core operation, and ensure the returned value contributes to correct_answer.
```

---
