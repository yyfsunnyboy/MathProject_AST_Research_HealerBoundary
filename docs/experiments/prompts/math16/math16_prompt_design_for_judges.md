# Math16 實驗 Prompt 設計說明書 (給高中科展評審)

本文件旨在說明本研究中 **Math16 (共16題數理程式生成挑戰)** 於三個控制條件下，實際傳送給大語言模型 (LLM) 的提示詞 (Prompt) 設計邏輯、安全性防護、以及增量鷹架的細節。

---

## 1. 我們比較什麼

本實驗採用控制變因法，設計了三個提示詞條件，呈**嚴格增量 (Strictly Additive)** 關係，用以測試模型在不同工程鷹架干預下的表現變化：
1. **Ab1 (Native baseline)**: 最基本提示。僅包含題目敘述、隨機輸入參數以及輸出格式契約 (answer contract)。模型必須自行理解並生成符合要求的程式碼。
2. **Ab2g (Generic scaffold)**: 通用鷹架提示。在 Ab1 的提示詞尾部附加了通用程式碼格式與安全規則 (GENERIC)，強制規定只輸出 Python 原始碼，不使用 markdown 圍欄，並進行一致性自我校驗。
3. **Ab2d (Domain scaffold)**: 領域學科鷹架提示。在 Ab2g 的提示詞尾部附加了針對該題型量身定做的 Domain API 函式定義（包含 signature 與 returns），引導模型使用後端已實作的高精確度學科 API（如 `PolynomialOps`、`RadicalOps` 等）來解決問題。

> [!IMPORTANT]
> 每個題目的隨機參數 (frozen parameters)、正確答案、數學格式契約及判分邏輯 (evaluator) 在三個條件中**完全相同**，保證實驗對照的公平性。

---

## 2. 三條件差異表

| 項目 | Ab1 | Ab2g | Ab2d |
|---|---|---|---|
| **題目與隨機參數** | 有 | 有 | 有 |
| **Answer Contract (輸出結構契約)** | 有 | 有 | 有 |
| **純 Python 輸出要求 (GENERIC)** | 無 (原始設定) | 有 | 有 |
| **generate() 結構檢查** | 無 (原始設定) | 有 | 有 |
| **領域 API 參考說明 (DOMAIN)** | 無 | 無 | 有 |
| **正確答案 (Correct Answer) 洩漏** | **無** | **無** | **無** |
| **Evaluator (判分器) 內部代碼** | **無** | **無** | **無** |
| **Healer (自癒) 恢復規則** | **無** | **無** | **無** |

---

## 3. 增量區塊原文

### Ab2g 相對 Ab1 新增的 GENERIC 區塊原文：
```text
## Clean-incremental GENERIC
Output complete Python source only. Do not use Markdown fences or explanatory prose. Preserve frozen parameters exactly. Verify that generate() exists. Verify that the return value has exactly the three required top-level keys. Verify field types match the stated contract and that oracle_payload equals the frozen parameters.
```

### Ab2d 相對 Ab2g 新增的 DOMAIN 區塊結構：
```text
## Clean-incremental DOMAIN
Task-local domain APIs (use only these):
- `<API_Name>` | import: `<Library>` | signature: `<Signature>` | returns: `<Returns>`
Use the listed domain API for each supported core operation, and ensure the returned value contributes to correct_answer.
```
*(各題實際帶入之 API 定義請參閱 16 題完整 Prompt 文件：[math16_ab2d_prompts.md](file:///C:/Projects/MathProject_AST_Research_HealerBoundary/docs/experiments/prompts/math16/math16_ab2d_prompts.md))*

---

## 4. 四類題型與 Domain API 說明

本實驗的學科 API (Domain API) 由後端 `core/prompts/domain_function_library.py` 精確封裝，避免了模型因浮點數漂移或算術錯誤導致答案失效。16個 Task 被分為以下四大類，每題**僅提供該題需要的 task-local API**，而不是一次性塞入所有工具：

1. **PolynomialOps (多項式類)**: 適用於多項式除法、因式分解等。例如只提供 `PolynomialOps.div_qr` 用於多項式除商求餘。
2. **RadicalOps (根式化簡類)**: 適用於二次方程根的化簡與根式運算。例如只提供 `RadicalOps.simplify_term`。
3. **FractionOps (精確分數與有理數類)**: 適用於分數算術。例如提供 `FractionOps.create` / `FractionOps.add` / `FractionOps.mul`。
4. **IntegerOps (整數算術類)**: 適用於冪次運算、倍數判斷等。例如提供 `IntegerOps.safe_eval`。

---

## 5. 公平性與防洩漏設計

- **防答案洩漏**: 提示詞內絕不包含任何題目的 `correct_answer`（正確答案）或 `oracle_expected_output`。
- **防評估器洩漏**: 評分系統的 `evaluator` 內部測試代碼及檢驗邏輯完全隔離。
- **防自癒資訊洩漏**: 後端自癒代碼 (Healer) 包含對特定錯誤的修復邏輯，這些邏輯完全處於運行時監控端，並未提供給生成階段的 LLM。
- **輸入完全一致**: 同一題在三個條件下的 frozen parameters (隨機生成參數) 均為同一組字串，排除題目難度變動干擾。

---

## 6. Prompt 版本與歷史一致性聲明

- **現行正式版本**: 本目錄下產出的 Ab2d 提示詞為目前的 **正式新版 (SSOT version)**。該版本與 `Qwen 3.5 4B/9B` 正式五-seed 實驗完全一致，且後續重跑之 `Gemini 3.5 Flash` 新五-seed Cohort 也將採用此版本。
- **舊版本備忘**: 歷史上 Gemini 早期首跑的 `Seed 1 (run_001)` 實驗之 Ab2d 使用了較早期的 SSOT 文字描述，與現行新版存在若干拼寫或格式上的差異，故其 prompt hashes 無法與新版完全重合。這些舊結果保留於歷史文檔作為 provenance 證據，不覆寫亦不刪除，但新版五-seed 橫向分析將以本版為單一真理源。

---

## 7. 評審閱讀指引

1. 先參閱 **2. 三條件差異表**，快速理解實驗變因。
2. 抽看 **附錄** 中相同題型在 Ab1、Ab2g、Ab2d 的 Prompt 組裝對照，觀察其結構如何由簡入繁，增量了哪些工程提示。
3. 透過完整提示詞文件與 JSON 索引提供的 SHA-256 Hash，可直接與程式碼庫或實驗 artifacts 進行一致性比對，確保實驗誠實性。

---

## 附錄：四大領域代表題型三條件並排對照

### 代表題型：ce115_calc_polynomial_division_l1 (多項式除法(一))

- **學科分類**: `polynomials`
- **Frozen Parameters**: `{"dividend_coefficients": [6, 0, 6], "divisor_coefficients": [1, -4]}`

#### 1. Ab1 (Native Baseline) Prompt
```text
Write only Python source. Implement def generate(level=1, **kwargs).
Task: ce115_calc_polynomial_division_l1 (polynomials, difficulty level 1).
Task specification: math16_polynomial_division_general.
Frozen sampled parameters: {"dividend_coefficients": [6, 0, 6], "divisor_coefficients": [1, -4]}
generate() must return a dict with exactly question_text, correct_answer, and oracle_payload. question_text must use formal LaTeX delimiters \( \) / \[ \]. correct_answer must include quotient_coefficients, remainder_coefficients, quotient_latex, and remainder_latex. Exact arithmetic; no floats. oracle_payload must exactly equal the frozen sampled parameters. Do not use input, files, network, subprocess, Markdown fences, or explanations.
```

#### 2. Ab2g (Generic Scaffold) Prompt
```text
Write only Python source. Implement def generate(level=1, **kwargs).
Task: ce115_calc_polynomial_division_l1 (polynomials, difficulty level 1).
Task specification: math16_polynomial_division_general.
Frozen sampled parameters: {"dividend_coefficients": [6, 0, 6], "divisor_coefficients": [1, -4]}
generate() must return a dict with exactly question_text, correct_answer, and oracle_payload. question_text must use formal LaTeX delimiters \( \) / \[ \]. correct_answer must include quotient_coefficients, remainder_coefficients, quotient_latex, and remainder_latex. Exact arithmetic; no floats. oracle_payload must exactly equal the frozen sampled parameters. Do not use input, files, network, subprocess, Markdown fences, or explanations.

## Clean-incremental GENERIC
Output complete Python source only. Do not use Markdown fences or explanatory prose. Preserve frozen parameters exactly. Verify that generate() exists. Verify that the return value has exactly the three required top-level keys. Verify field types match the stated contract and that oracle_payload equals the frozen parameters.
```

#### 3. Ab2d (Domain Scaffold) Prompt
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

#### 4. 增量差異說明
- **Ab1 -> Ab2g 增量**: 尾部增加了 `## Clean-incremental GENERIC` 部分，用以抑制 prose/explanation 並限制輸出為純 Python 代碼。
- **Ab2g -> Ab2d 增量**: 尾部增加了 `## Clean-incremental DOMAIN` 部分，注入了 `PolynomialOps.div_qr` / `PolynomialOps.format_latex` (若有) 的 task-local API 呼叫說明。

---

### 代表題型：ce115_calc_radical_simplification_l1 (最簡根式化簡)

- **學科分類**: `radicals`
- **Frozen Parameters**: `{"radicand": 27}`

#### 1. Ab1 (Native Baseline) Prompt
```text
Write only Python source. Implement def generate(level=1, **kwargs).
Task: ce115_calc_radical_simplification_l1 (radicals, difficulty level 1).
Task specification: math16_radical_simplification.
Frozen sampled parameters: {"radicand": 27}
generate() must return a dict with exactly question_text, correct_answer, and oracle_payload. question_text must use formal LaTeX delimiters. correct_answer must include coefficient, radicand, and canonical_latex. Exact integers only; no floats. oracle_payload must exactly equal the frozen sampled parameters. Do not use input, files, network, subprocess, Markdown fences, or explanations.
```

#### 2. Ab2g (Generic Scaffold) Prompt
```text
Write only Python source. Implement def generate(level=1, **kwargs).
Task: ce115_calc_radical_simplification_l1 (radicals, difficulty level 1).
Task specification: math16_radical_simplification.
Frozen sampled parameters: {"radicand": 27}
generate() must return a dict with exactly question_text, correct_answer, and oracle_payload. question_text must use formal LaTeX delimiters. correct_answer must include coefficient, radicand, and canonical_latex. Exact integers only; no floats. oracle_payload must exactly equal the frozen sampled parameters. Do not use input, files, network, subprocess, Markdown fences, or explanations.

## Clean-incremental GENERIC
Output complete Python source only. Do not use Markdown fences or explanatory prose. Preserve frozen parameters exactly. Verify that generate() exists. Verify that the return value has exactly the three required top-level keys. Verify field types match the stated contract and that oracle_payload equals the frozen parameters.
```

#### 3. Ab2d (Domain Scaffold) Prompt
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

#### 4. 增量差異說明
- **Ab1 -> Ab2g 增量**: 尾部增加了 `## Clean-incremental GENERIC` 部分，用以抑制 prose/explanation 並限制輸出為純 Python 代碼。
- **Ab2g -> Ab2d 增量**: 尾部增加了 `## Clean-incremental DOMAIN` 部分，注入了 `IntegerOps.safe_eval`、`IntegerOps.fmt_num` 等 task-local API 呼叫說明。

---

### 代表題型：ce111_q05_exact_fraction_expression (精確分數四則運算)

- **學科分類**: `rational_arithmetic`
- **Frozen Parameters**: `{"expression": "9/22 + 11/18 - (23/22 - 7/18)"}`

#### 1. Ab1 (Native Baseline) Prompt
```text
Write only Python source. Implement def generate(level=1, **kwargs).
Task: ce111_q05_exact_fraction_expression (rational_arithmetic, difficulty level 1).
Task specification: math16_exact_fraction_expression.
Frozen sampled parameters: {"expression": "9/22 + 11/18 - (23/22 - 7/18)"}
generate() must return a dict with exactly question_text, correct_answer, and oracle_payload. question_text must use formal LaTeX delimiters. correct_answer must include numerator, denominator, and canonical_latex for an irreducible fraction. oracle_payload must exactly equal the frozen sampled parameters. Do not use input, files, network, subprocess, Markdown fences, or explanations.
```

#### 2. Ab2g (Generic Scaffold) Prompt
```text
Write only Python source. Implement def generate(level=1, **kwargs).
Task: ce111_q05_exact_fraction_expression (rational_arithmetic, difficulty level 1).
Task specification: math16_exact_fraction_expression.
Frozen sampled parameters: {"expression": "9/22 + 11/18 - (23/22 - 7/18)"}
generate() must return a dict with exactly question_text, correct_answer, and oracle_payload. question_text must use formal LaTeX delimiters. correct_answer must include numerator, denominator, and canonical_latex for an irreducible fraction. oracle_payload must exactly equal the frozen sampled parameters. Do not use input, files, network, subprocess, Markdown fences, or explanations.

## Clean-incremental GENERIC
Output complete Python source only. Do not use Markdown fences or explanatory prose. Preserve frozen parameters exactly. Verify that generate() exists. Verify that the return value has exactly the three required top-level keys. Verify field types match the stated contract and that oracle_payload equals the frozen parameters.
```

#### 3. Ab2d (Domain Scaffold) Prompt
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

#### 4. 增量差異說明
- **Ab1 -> Ab2g 增量**: 尾部增加了 `## Clean-incremental GENERIC` 部分，用以抑制 prose/explanation 並限制輸出為純 Python 代碼。
- **Ab2g -> Ab2d 增量**: 尾部增加了 `## Clean-incremental DOMAIN` 部分，注入了 `IntegerOps.safe_eval`、`IntegerOps.fmt_num` 等 task-local API 呼叫說明。

---

### 代表題型：ce112_q01_negative_integer_power (負整數冪次計算)

- **學科分類**: `integers`
- **Frozen Parameters**: `{"base": -3, "exponent": 3}`

#### 1. Ab1 (Native Baseline) Prompt
```text
Write only Python source. Implement def generate(level=1, **kwargs).
Task: ce112_q01_negative_integer_power (integers, difficulty level 1).
Task specification: math16_negative_integer_power.
Frozen sampled parameters: {"base": -3, "exponent": 3}
generate() must return a dict with exactly question_text, correct_answer, and oracle_payload. question_text must use formal LaTeX delimiters where math appears. correct_answer must be a single exact integer. oracle_payload must exactly equal the frozen sampled parameters. Do not use input, files, network, subprocess, Markdown fences, or explanations.
```

#### 2. Ab2g (Generic Scaffold) Prompt
```text
Write only Python source. Implement def generate(level=1, **kwargs).
Task: ce112_q01_negative_integer_power (integers, difficulty level 1).
Task specification: math16_negative_integer_power.
Frozen sampled parameters: {"base": -3, "exponent": 3}
generate() must return a dict with exactly question_text, correct_answer, and oracle_payload. question_text must use formal LaTeX delimiters where math appears. correct_answer must be a single exact integer. oracle_payload must exactly equal the frozen sampled parameters. Do not use input, files, network, subprocess, Markdown fences, or explanations.

## Clean-incremental GENERIC
Output complete Python source only. Do not use Markdown fences or explanatory prose. Preserve frozen parameters exactly. Verify that generate() exists. Verify that the return value has exactly the three required top-level keys. Verify field types match the stated contract and that oracle_payload equals the frozen parameters.
```

#### 3. Ab2d (Domain Scaffold) Prompt
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

#### 4. 增量差異說明
- **Ab1 -> Ab2g 增量**: 尾部增加了 `## Clean-incremental GENERIC` 部分，用以抑制 prose/explanation 並限制輸出為純 Python 代碼。
- **Ab2g -> Ab2d 增量**: 尾部增加了 `## Clean-incremental DOMAIN` 部分，注入了 `IntegerOps.safe_eval`、`IntegerOps.fmt_num` 等 task-local API 呼叫說明。

---
