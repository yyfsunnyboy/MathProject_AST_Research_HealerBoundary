# 《Math16 實驗題目、Prompt 與程式骨架展示附錄 v1》

**專案／研究線：** Ivan 旺宏科學展 —— HealerBoundary (`MathProject_AST_Research_HealerBoundary`)
**文件類型：** 正式審查附錄 C (Official Review Appendix C)
**建置時間 UTC：** 2026-07-23

---

> **固定位階聲明 (Mandatory Disclaimer)：**
> 本附錄為Evidence Complete凍結後之Post-hoc展示文件，只供老師與評審理解實驗材料，不修改、取代或重新解釋既有Primary與正式Post-hoc結果。

---

## 1. 資料角色隔離與安全防禦 (Data Role Isolation & Governance)

為確保實驗之嚴謹性與可重現性，本研究於資料與流程架構上對「模型輸入」、「Healer 輸入」與「評審對照資料」進行了嚴格的隔離設計：

1. **模型輸入 (Model Inputs)**：包含題目文本、提示詞 (Prompt)、Domain API / Spec 規格區塊與輸出契約 (Output Contract)。模型僅能視見此部分內容以生成 Python 代碼。
2. **Healer 輸入 (Healer Inputs)**：僅包含模型所生成的原始 Python 程式碼及其經過 Parser 解析後之 AST (Abstract Syntax Tree) 抽象語法樹結構。
3. **評審對照資料 (Evaluator Reference Data)**：包含專家預先計算之正確答案 (Oracle Answer / Correct Answer)、Evaluator 預期型態與得分判定。

---

> **評審對照隔離聲明 (Procedural Isolation Notice)：**
> 正確答案僅供老師與評審對照理解，不是模型生成Prompt的一部分，也不是Healer執行時可讀取的輸入。Healer僅依生成程式的語法、AST結構與凍結契約規則進行修改，`oracle_answer_used = false`。

---

## 2. 16 題實驗題目索引 (16 Benchmark Tasks Index)

以下為 Math16 實驗矩陣中全數 16 題任務之權威索引表。16 題之名稱、領域 (Family) 與 API 策略均與 Final Report v1.3 保持 100% 嚴格一致。

> **難度與執行參數澄清說明：**
> 索引表中 `runtime_level=1` 是程式生成介面 (`generate(level=1)`) 的預設執行參數，不等於題目難度。題目難度另依預註冊評估列為 `preregistered_difficulty`（`LOW` / `MEDIUM` / `HIGH`）。

| Task ID | 題目描述 / 任務說明 | Family | Runtime Level | Preregistered Difficulty | API Policy | Expected Output Type | Source Path & SHA256 | 實驗特殊角色 |
|---|---|---|---:|---|---|---|---|---|
| `ce111_nonchoice_q01_part1_exponential_growth` | 指數成長與大數邏輯計算 | Integer | 1 | MEDIUM | Native-only | `integer_exact_k` | `agent_tools/.../math16_pool.py`<br>`406965451600809f...` | Standard Benchmark |
| `ce111_q02_polynomial_division_remainder` | 多項式除法餘式定理 | Polynomial | 1 | MEDIUM | API-only | `polynomial_division_remainder_only` | `agent_tools/.../math16_pool.py`<br>`406965451600809f...` | Standard Benchmark |
| `ce111_q03_prime_factor_selection` | 質因數分解與篩選 | Integer | 1 | LOW | Native-only | `integer_exact` | `agent_tools/.../math16_pool.py`<br>`406965451600809f...` | Standard Benchmark |
| `ce111_q05_exact_fraction_expression` | 既約分數運算與表達 | Fraction | 1 | MEDIUM | API-only | `exact_fraction_canonical` | `agent_tools/.../math16_pool.py`<br>`406965451600809f...` | Standard Benchmark |
| `ce111_q08_polynomial_factor_parameter_recovery` | 多項式因式分解參數還原 | Polynomial | 1 | HIGH | Native-only | `polynomial_factor_parameter_recovery` | `agent_tools/.../math16_pool.py`<br>`406965451600809f...` | Forced Ambiguity |
| `ce111_q10_ordered_quadratic_roots_radical` | 一元二次方程式根式解順序 | Radical | 1 | HIGH | Mixed | `compound_radical_result` | `agent_tools/.../math16_pool.py`<br>`406965451600809f...` | Standard Benchmark |
| `ce112_q01_negative_integer_power` | 負整數方次計算 | Integer | 1 | LOW | Native-only | `integer_exact` | `agent_tools/.../math16_pool.py`<br>`406965451600809f...` | Standard Benchmark |
| `ce112_q04_radical_simplification` | 根式化簡與標準型態 | Radical | 1 | LOW | API-only | `radical_simplification_canonical` | `agent_tools/.../math16_pool.py`<br>`406965451600809f...` | Six-Cell Rescued |
| `ce112_q09_divisor_multiple_intersection` | 因數與倍數交集個數 | Integer | 1 | MEDIUM | Native-only | `integer_count` | `agent_tools/.../math16_pool.py`<br>`406965451600809f...` | Standard Benchmark |
| `ce112_q12_independent_probability_fraction` | 獨立事件分數機率 | Fraction | 1 | MEDIUM | API-only | `exact_fraction_canonical` | `agent_tools/.../math16_pool.py`<br>`406965451600809f...` | Standard Benchmark |
| `ce113_q01_negative_fraction_subtraction` | 帶負號分數減法運算 | Fraction | 1 | LOW | API-only | `exact_fraction_canonical` | `agent_tools/.../math16_pool.py`<br>`406965451600809f...` | Six-Cell Rescued |
| `ce113_q11_rationalize_denominator` | 分母有理化運算 | Radical | 1 | HIGH | Native-only | `integer_exact` | `agent_tools/.../math16_pool.py`<br>`406965451600809f...` | Six-Cell Rescued |
| `ce115_calc_exact_rational_expression_l1` | 繁分數與有理式化簡 | Fraction | 1 | MEDIUM | API-only | `math16_exact_rational_expression` | `agent_tools/.../math16_pool.py`<br>`406965451600809f...` | Six-Cell Rescued |
| `ce115_calc_polynomial_division_l1` | 多項式綜合除法化簡 | Polynomial | 1 | MEDIUM | API-only | `math16_polynomial_division_general` | `agent_tools/.../math16_pool.py`<br>`406965451600809f...` | Standard Benchmark |
| `ce115_calc_polynomial_factor_roots_l1` | 多項式根與係數求解 | Polynomial | 1 | MEDIUM | Native-only | `math16_polynomial_factor_roots` | `agent_tools/.../math16_pool.py`<br>`406965451600809f...` | Standard Benchmark |
| `ce115_calc_radical_simplification_l1` | 複合根式乘除化簡 | Radical | 1 | LOW | API-only | `math16_radical_simplification` | `agent_tools/.../math16_pool.py`<br>`406965451600809f...` | Six-Cell Rescued |

---

## 3. 四種 Prompt 條件對比 (Four Prompt Conditions Matrix)

本研究設計了四種階層式 Prompt 條件，旨在定量比較「語義契約」、「通用鷹架」與「領域工具／規格約束」對模型生成品質之影響：

| Prompt 條件 (Condition) | 基礎內容 (Base Content) | 比前層新增內容 (Incremental Content) | 研究與測量目的 (Research Purpose) |
|---|---|---|---|
| **Ab1（原始契約條件）** | 任務說明、題目參數、輸出契約規範 | 無 | 測量模型在無鷹架保護下之原生隨機性與契約遵守率 |
| **Ab2g (Scaffold General)** | 包含 Ab1 全部內容 | 通用 Python 代碼生成鷹架（禁 Prose、鎖定縮排與檔頭） | 測量通用代碼規範對壓制自由格式殘留（Prose Residue）之效果 |
| **Ab2d+api (Scaffold Domain API)** | 包含 Ab2g 全部內容 | 預載 Domain API 工具函式區塊 (如 `RadicalOps`, `FractionOps`) | 測量暴露預建工具庫對提升語法正確性與計算精確度之效果 |
| **Ab2d+spec-v2 (Scaffold Spec-v2)** | 包含 Ab2g 全部內容 | 領域專用語法規格約束區塊 (Family-specific Spec Block) | 測量強類型契約與細粒度規格約束對壓制結構異常之效果 |

---

## 4. 64 份 Prompt 權威索引 (64 Prompts Complete Index)

全數 64 份 Prompt（16 題 $\times$ 4 條件）均以文字檔形式完整保存於 `docs/experiments/results/` 中。權威索引表存於 `artifacts/math16_tasks_prompts_and_program_skeletons_appendix_v1/prompt_index.csv`。

---

## 5. 代表性完整案例展示 (Four Representative Cases)

本節挑選 4 個具代表性之任務案例，完整呈現其題目、Prompt、輸出契約與評審對照資料：

```carousel
### Case 1: ce112_q04_radical_simplification (Radical Family / API-only)
- **題目原文**：將根式 $\sqrt{135}$ 化簡為最簡根式 $a\sqrt{b}$ 型態。
- **Runtime Level**：`1` | **Preregistered Difficulty**：`LOW`
- **Condition**：`Ab2d+api`
- ** Prompt 路徑**：`docs/experiments/results/math16_pilot02_qwen4b_ab2d_api/seed_2026071301/ce112_q04_radical_simplification/prompt.txt`
- ** Prompt SHA256**：`69752d5b6be4c898c69136e05df84eb98ef1fd3ea64380eb9aeeeb6e91f1adfb`

> **評審對照區（不進入模型／Healer）**
> - **正確答案**：`a = 3, b = 15` ($\sqrt{135} = 3\sqrt{15}$)
> - **Oracle Payload**：`{"radicand": 135}`
> - **隔離聲明**：以上對照答案不包含於 Prompt 中，亦不供 Healer 讀取。
<!-- slide -->
### Case 2: ce113_q01_negative_fraction_subtraction (Fraction Family / API-only)
- **題目原文**：計算分數減法算式 $\frac{3}{7} - \left(-\frac{1}{4}\right)$ 之精確值。
- **Runtime Level**：`1` | **Preregistered Difficulty**：`LOW`
- **Condition**：`Ab2d+api`
- ** Prompt 路徑**：`docs/experiments/results/math16_pilot02_qwen4b_ab2d_api/seed_2026071301/ce113_q01_negative_fraction_subtraction/prompt.txt`
- ** Prompt SHA256**：`3ae3bf32db2f0b9f5f0fb5ceaa01bfa59dd7ca07d4b47ebcb0b4845ed39556bb`

> **評審對照區（不進入模型／Healer）**
> - **正確答案**：`num = 19, den = 28` ($\frac{19}{28}$)
> - **Oracle Payload**：`{"expression": "3/7 - (-1/4)"}`
> - **隔離聲明**：以上對照答案不包含於 Prompt 中，亦不供 Healer 讀取。
<!-- slide -->
### Case 3: ce115_calc_radical_simplification_l1 (Radical Family / API-only)
- **題目原文**：化簡根式算式 $\sqrt{27}$ 並回傳標準化結果。
- **Runtime Level**：`1` | **Preregistered Difficulty**：`LOW`
- **Condition**：`Ab2d_spec_v2`
- ** Prompt 路徑**：`docs/experiments/results/math16_pilot02_qwen4b_ab2d_spec_v2/seed_2026071301/ce115_calc_radical_simplification_l1/prompt.txt`
- ** Prompt SHA256**：`8046e7f1e67cfbb08f237efb32e0e5a8ddb1607ef27ca8e5eb7dfa4e0c3ce367`

> **評審對照區（不進入模型／Healer）**
> - **正確答案**：`a = 3, b = 3` ($\sqrt{27} = 3\sqrt{3}$)
> - **Oracle Payload**：`{"radicand": 27}`
> - **隔離聲明**：以上對照答案不包含於 Prompt 中，亦不供 Healer 讀取。
<!-- slide -->
### Case 4: ce111_q08_polynomial_factor_parameter_recovery (Polynomial Family / Native-only / Forced Ambiguity Case)
- **題目原文**：已知多項式 $2x^2 + 13x - 7 = (ax-1)(x+b)$，求參數 $a, b$ 與展開檢算值。
- **Runtime Level**：`1` | **Preregistered Difficulty**：`HIGH`
- **Condition**：`Ab2d+api`
- ** Prompt 路徑**：`docs/experiments/results/math16_pilot02_qwen4b_ab2d_api/seed_2026072004/ce111_q08_polynomial_factor_parameter_recovery/prompt.txt`
- ** Prompt SHA256**：`6fbff4a29a0082f42a733cfcf0dfc71b0c95d9bd90e8c07dd59e99ebc8b0fbef`

> **評審對照區（不進入模型／Healer）**
> - **正確答案**：`a = 2, b = 7, c = -7, expanded_check = [39, 5, -14]`
> - **Oracle Payload**：`{"a": 2, "b": 13, "c": -7, "expanded_check": [39, 5, -14]}`
> - **隔離聲明**：以上對照答案不包含於 Prompt 中，亦不供 Healer 讀取。
```

---

## 6. 凍結輸出契約與正確空殼程式 (Output Contract & Skeleton Code)

### 6.1 凍結契約規範 (Frozen Output Contract)
模型生成的 Python 程式碼必須嚴格遵守下列介面與回傳格式：
- **Entry-Point 函式**：`def generate(level=1, **kwargs)`
- **回傳型態**：`dict`
- **必須包含之 Key 集合**：
  1. `"question_text"`: 題目 LaTeX 文本（字串 `str`）
  2. `"correct_answer"`: 題目標準解答（純量或結構化資料）
  3. `"oracle_payload"`: 題目參數或載荷（字典 `dict`）

### 6.2 正確空殼程式碼展示 (Correct Skeleton Code)

```python
# 正確空殼程式 (Standard Compliant Skeleton)
# 僅包含契約要求欄位，無硬編碼答案，無非標準模板

def generate(level=1, **kwargs):
    # 1. 題目文本 (LaTeX 格式)
    question_text = r"化簡根式 \sqrt{135}"

    # 2. 正確答案 (計算結果)
    correct_answer = "3\\sqrt{15}"

    # 3. 題目載荷 (Frozen Parameters)
    oracle_payload = {
        "radicand": 135
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }
```

---

## 7. 六格共同錯誤結構與示意 (Six-Cell Common Error Diagram)

在 Post-hoc 救援的 6 個案例中，模型均正確生成了題目與答案，但回傳字典之結構發生了單一外包裝錯誤：

```python
# 1. 錯誤的 Before 結構 (Single-Key Oracle Payload Wrap Error)
def generate(level=1, **kwargs):
    return {
        "oracle_payload": {
            "question_text": r"化簡根式 \sqrt{135}",
            "correct_answer": "3\\sqrt{15}",
            "oracle_payload": {"radicand": 135}
        }
    }

# 2. Healer 規則修復邏輯 (Rule: L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP)
# Healer 自動移除最外層單一 "oracle_payload" Key 包裝，恢復為平鋪三欄結構

# 3. 修復機制示意 After 結構
# 【警語】：下列 after 僅為規則修復機制之邏輯示意，非原 Six-Cell 逐字 after 原始碼。
def generate(level=1, **kwargs):
    return {
        "question_text": r"化簡根式 \sqrt{135}",
        "correct_answer": "3\\sqrt{15}",
        "oracle_payload": {"radicand": 135}
    }
```

---

## 8. Forced Ambiguity 歧義案例展示 (Forced Ambiguity Case Details)

- **Canonical Cell ID**: `qwen3_5_4b__ce111_q08_polynomial_factor_parameter_recovery__ab2d__seed_2026072004`
- **任務名稱**: `ce111_q08_polynomial_factor_parameter_recovery`
- **Condition**: `Ab2d+api`
- **問題特徵**: 模型輸出包含自然語言敘述 (Prose Residue) 且內含 2 個 `def generate` 函式入口點候選。
- **強行選擇政策**: `DETERMINISTIC_FIRST_ENTRY_POINT_SOURCE_PREORDER` (選擇第一個 `def generate` 偏移量)
- **Unified Diff 檔案**: `artifacts/math16_pilot02_qwen4b_unrestricted_stress_test_v11/formal/unified_diffs/qwen3_5_4b__ce111_q08_polynomial_factor_parameter_recovery__ab2d__seed_2026072004_forced.diff`
- **Diff SHA256**: `d8f0130d0d1d532ddfa78aba1b82eae4d9df1066f1ec09aec09345a82b350c24`
- **Evaluator 評估結果**: **`FAILED`** (原因 `missing_entry_point`，因修剪 Prose 後仍留存未隔離之第二片段)
- **Safety 預分類**: `UNSAFE_MODIFICATION`

---

## 9. 獨立證據索引 (Independent Evidence Index)

| Claim | Artifact Path | Artifact SHA256 | Governing Manifest Path | Manifest SHA256 | Supports |
|---|---|---|---|---|---|
| Runtime Level 定義 | `scripts/evaluate_math16_pilot02_full_v4.py` | `2cca19f2258d4ba6134ff10d4e9bcff925e2441c32820fcbc151cb6b1dd740bc` | `docs/experiments/manifests/math16_pilot02_qwen4b_cell_plan.json` | `d83451176a51d7d9bdda15266ab28c49c5d8d46faf85e093ed3d94df044dd570` | generate(level=1) 介面預設參數定義 |
| 預註冊難度定義 | `docs/experiments/prompts/ab2d_spec/manifest.json` | `50427ccfc335a4e31ec51ee8a09ed2646b1906a2ff906c678924c0ac237c6bb7` | `docs/experiments/manifests/math16_pilot02_qwen4b_cell_plan.json` | `d83451176a51d7d9bdda15266ab28c49c5d8d46faf85e093ed3d94df044dd570` | 預註冊難度 (LOW / MEDIUM / HIGH) 評估來源 |
| 附錄 A 權威 Manifest | `docs/experiments/manifests/math16_six_cell_healer_mechanism_validation_appendix_v1_manifest.json` | `52014b1fbdbb09372953ae39be5965397d1f3813d88d99b95ff9053a25e1d29d` | `docs/experiments/manifests/math16_posthoc_six_cell_rescue_audit_v1_result_manifest.json` | `97392be833786bab90bcd5f1cb9eb9b57edaffc681466bdda62650f29dda35de` | 附錄 A 權威 Manifest 索引 |
| 附錄 B 權威 Manifest | `docs/experiments/manifests/math16_eligibility_and_unrestricted_stress_test_appendix_v1_manifest.json` | `ae61249c6dd8bafa422e401b5e6bed5abcd9262b5b6ea0df5bc641b93e9e6d1b` | `docs/experiments/manifests/math16_pilot02_qwen4b_unrestricted_stress_test_v11_result_manifest.json` | `7cfc9f8f4de8b1fbf56ef19afdedba5dc43fd3ee70fe35d72c46cfeff33cdcf0` | 附錄 B 權威 Manifest 索引 |
| 上游 Six-Cell Manifest | `docs/experiments/manifests/math16_posthoc_six_cell_rescue_audit_v1_result_manifest.json` | `97392be833786bab90bcd5f1cb9eb9b57edaffc681466bdda62650f29dda35de` | `docs/experiments/milestones/math16_pilot02_evidence_complete_v1/evidence_complete_manifest.json` | `de11b9bd5038171689ee2895fc3a499a7b404f5259b3f5b3bcc31cb4d4af2225` | 上游 Six-Cell 正式結果 Manifest |
| 上游 Stress Test Manifest | `docs/experiments/manifests/math16_pilot02_qwen4b_unrestricted_stress_test_v11_result_manifest.json` | `7cfc9f8f4de8b1fbf56ef19afdedba5dc43fd3ee70fe35d72c46cfeff33cdcf0` | `docs/experiments/milestones/math16_pilot02_evidence_complete_v1/evidence_complete_manifest.json` | `de11b9bd5038171689ee2895fc3a499a7b404f5259b3f5b3bcc31cb4d4af2225` | 上游 Stress Test v1.1 正式結果 Manifest |
