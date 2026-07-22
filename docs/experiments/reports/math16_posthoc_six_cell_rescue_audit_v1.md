# Math16 Post-hoc Six-Cell Rescue Mechanism Audit Report v1

```text
MATH16_SIX_CELL_RESCUE_MECHANISM_AUDIT_V1_COMPLETED
SIX_CELL_CROSS_ANALYSIS_COMPLETED
PRIMARY_POSTHOC_SET_RELATION_VERIFIED
REPAIR_SIGNATURE_CATALOG_FROZEN
OFFICIAL_RESULTS_AND_FINAL_REPORT_PRESERVED
READY_FOR_UNRESTRICTED_STRESS_TEST_PREREGISTRATION
```

**專案／研究線：** Ivan 旺宏科學展 —— HealerBoundary (`MathProject_AST_Research_HealerBoundary`)
**報告版本：** v1.0 (Formal Post-hoc Audit Report)
**標的數據庫：** Math16 Pilot-02 Qwen 3.5 4B（320 個獨立實驗 cells，聚焦 6 格 Post-hoc 救回案例）
**正式來源證明檔：**
- [Shared Taxonomy v1](file:///c:/Projects/MathProject_AST_Research_HealerBoundary/docs/experiments/design/math16_posthoc_shared_taxonomy_v1.md)
- [Audit Spec v1](file:///c:/Projects/MathProject_AST_Research_HealerBoundary/docs/experiments/design/math16_posthoc_six_cell_rescue_audit_v1_spec.md)
- [Audit Manifest v1](file:///c:/Projects/MathProject_AST_Research_HealerBoundary/docs/experiments/manifests/math16_posthoc_six_cell_rescue_audit_v1_manifest.json)
- [Primary vs Corrected Comparison](file:///c:/Projects/MathProject_AST_Research_HealerBoundary/docs/experiments/results/math16_pilot02_qwen4b_healer_v4_posthoc_corrected_chain_r001/primary_vs_corrected_chain_comparison.json)
- [Eligible Execution Records](file:///c:/Projects/MathProject_AST_Research_HealerBoundary/docs/experiments/results/math16_pilot02_qwen4b_healer_v4_r001/eligible_execution_records.jsonl)

---

> **固定聲明 (Mandatory Disclaimer)：**
> 本分析為 Evidence Complete 凍結後之 Post-hoc 補充稽核，不修改、取代或重新解釋既有 Primary 與正式 Post-hoc 結果。

---

## 1. 執行摘要 (Executive Summary)

本報告為 **Math16 Pilot-02** 專案中 Qwen 3.5 4B 模型下成功被 AST Healer 救援之 **6 個 Post-hoc 救回 cells** 進行完全唯讀（Read-Only）、零模型呼叫、零 Healer 執行的機制層面稽核。

稽核結果確認：
1. **Primary 與 Post-hoc 集合關係驗證**：Primary 救回集合 (5 格) 為 Post-hoc 救回集合 (6 格) 之**真子集 (Strict Subset)**，差集恰為 1 格。
2. **第 6 格救回機制**：第 6 格 (`qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d__seed_2026071301`) 在 Primary run 中因舊版 Healer 觸發 false-loop 誤判撤回 (rollback) 而落入 `NO_OP`；在 Post-hoc corrected-chain 中移除誤判撤回後，成功保留合法 `L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP` 解包轉換，達成正式 `PASS`。
3. **規則極化 (Rule Polarization)**：6 格救回案例 100% 命中同一預先登錄且凍結之修復規則 —— `L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP`（將模型誤包於單鍵 JSON 字典中之運算表達式解包）。
4. **安全屬性 (Safety Properties)**：所有 6 格完全符合 **Unique (解答唯一)**、**Local (編輯局部)** 與 **Offline-Verifiable (離線可驗證)** 三大確定性修復原則，且 `oracle_answer_used = false`（100% 不依賴答案反推）。

---

## 2. 核心問題解答 (Systematic Audit Findings)

### Q1: 六格分別來自哪些 Condition 與 Family？
6 格在 Prompt Condition 與題型 Family 的分布如下：
- **Ab2g (通用鷹架)**: 2 格（1 Radical, 1 Fraction）
- **Ab2d+api (領域 API 暴露)**: 2 格（2 Radical）
- **Ab2d+spec (家族規格)**: 2 格（1 Radical, 1 Fraction）
- **Ab1 (裸考)**: 0 格

### Q2: 各格真正 Root Mechanism 是什麼？
6 格在 Surface Failure Layer 均表現為 `L2`（入口與契約層，Evaluator 回傳 `schema_failure`）。其真正的 Root Mechanism Layer 均為 **`L2_CONTRACT_SCHEMA_ENTRYPOINT`**：模型已成功生成可執行的 Python 數學表達式，但將輸出封裝於單一 Key 的 JSON 字典（例如 `{"result": "2*sqrt(3)"}`）或字串封裝中，違反了 Evaluator 要求的純表達式產出規範。

### Q3: 各 Condition 是否命中相同或不同 Rule？
100% 命中**相同**修復規則 —— `L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP`。這顯示在 Qwen 3.5 4B 模型中，AST Healer 能發揮確定性救援的故障型態高度集中於「語義正確但外層 JSON 封裝瑕疵」。

### Q4: Healer 實際修改了哪些 AST 節點／Source Span？
由於 6 格之原始 Python 生成碼儲存於 `sha_only_not_committed_py`（僅保留 sha256 哈希值），AST 節點層級之 Unified Diff 被標註為 `UNRESOLVED_SOURCE_NOT_COMMITTED`，修復簽章特徵歸類為 `AMBIGUOUS_SIGNATURE_MATCH`。但由 `repair_signature_catalog.json` 驗證，其轉換為**確定性剝離 JSON 外層字典 Key**，不改動內部運算式之 AST 運算子與控制流。

### Q5: 六格是否都符合 Unique、Local、Offline-Verifiable？
**是的**：
- `unique`: `TRUE` (剝離單一 Key 的 JSON 外層有且僅有一種確定性解法)
- `local`: `TRUE` (僅作用於頂層 Payload 解封裝，不改動區域變數或演算法)
- `offline_verifiable`: `TRUE` (可由靜態 AST / JSON 解析器在無 LLM/Evaluator 參與下獨立驗證)

### Q6: Ab2d+api 新增第 6 格的原因是否為 Corrected-Chain 處置修正？
**是的**。第 6 格 (`ce115_calc_radical_simplification_l1` under `Ab2d+api`, seed `2026071301`) 在 Primary 流程中，Healer 在修修過程中因舊版迴圈偵測器（Evaluator loop check）誤將「修復後 Evaluator 仍回傳錯誤」的判斷機制過度擴張，觸發了邏輯 Rollback 回原原始碼 (變成 `NO_OP`)。在 Post-hoc Corrected-Chain 修正 false-loop 回滾邏輯後，正確保留了 `L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP` 轉換，並在重評中證實該解包已使程式達成正式 `PASS`。此非新模型生成、亦非新 Healer 規則，純屬流程處置修復。

### Q7: Condition / Family / Rule 間有哪些描述性共現？
- **Radical (根式)** 佔 4 格 (66.7%)，**Fraction (分數)** 佔 2 格 (33.3%)。
- Integer (整數) 與 Polynomial (多項式) 在此 6 格中為 0 格。
- 顯示根式與分數題目在 LLM 輸出時，較常傾向使用結構化 JSON Payload 進行包裹。

### Q8: 有分母後，各 Condition 的 Rescued/FAIL 與 Rescued/Eligible 為何？
在 Qwen 3.5 4B 總體 320 格實驗矩陣中：
- **Ab1**: 0/65 FAIL (0.00%), 0/1 Eligible (0.00%)
- **Ab2g**: 2/61 FAIL (3.28%), 2/3 Eligible (66.67%)
- **Ab2d+api**: 2/72 FAIL (2.78%), 2/3 Eligible (66.67%)
- **Ab2d+spec**: 2/44 FAIL (4.55%), 2/3 Eligible (66.67%)
- **全體總計**: 6/242 FAIL (2.48%), 6/10 Eligible (60.00%)

---

## 3. 交叉分析表 (Crosstab Analysis)

### 3.1 Condition × Family

| Condition | Radical | Fraction | Integer | Polynomial | Total |
|---|---:|---:|---:|---:|---:|
| Ab1 | 0 | 0 | 0 | 0 | 0 |
| Ab2g | 1 | 1 | 0 | 0 | 2 |
| Ab2d+api | 2 | 0 | 0 | 0 | 2 |
| Ab2d+spec | 1 | 1 | 0 | 0 | 2 |
| **Total** | **4** | **2** | **0** | **0** | **6** |

### 3.2 Condition × Root Mechanism Layer

| Condition | L1_PARSE | L2_CONTRACT_SCHEMA | L3_DOMAIN_API | L4_RUNTIME | L5_SEMANTIC | Total |
|---|---:|---:|---:|---:|---:|---:|
| Ab1 | 0 | 0 | 0 | 0 | 0 | 0 |
| Ab2g | 0 | 2 | 0 | 0 | 0 | 2 |
| Ab2d+api | 0 | 2 | 0 | 0 | 0 | 2 |
| Ab2d+spec | 0 | 2 | 0 | 0 | 0 | 2 |
| **Total** | **0** | **6** | **0** | **0** | **0** | **6** |

### 3.3 Condition × Rule ID

| Condition | L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP | Total |
|---|---:|---:|
| Ab1 | 0 | 0 |
| Ab2g | 2 | 2 |
| Ab2d+api | 2 | 2 |
| Ab2d+spec | 2 | 2 |
| **Total** | **6** | **6** |

### 3.4 Condition × Primary / Post-hoc 救回矩陣

| Condition | Primary Rescued | Incremental Post-hoc PASS | Post-hoc Rescued Total |
|---|---:|---:|---:|
| Ab1 | 0 | 0 | 0 |
| Ab2g | 2 | 0 | 2 |
| Ab2d+api | 1 | 1 | 2 |
| Ab2d+spec | 2 | 0 | 2 |
| **Total** | **5** | **1** | **6** |

### 3.5 Condition 分母與救援率表 (320-Cell Qwen 4B Matrix)

| Condition | Total Cells | Baseline PASS | Baseline FAIL | Eligible | Primary Rescued | Post-hoc Rescued | Rescued/FAIL Rate | Rescued/Eligible Rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Ab1 | 80 | 15 | 65 | 1 | 0 | 0 | 0.00% (0/65) | 0.00% (0/1) |
| Ab2g | 80 | 19 | 61 | 3 | 2 | 2 | 3.28% (2/61) | 66.67% (2/3) |
| Ab2d+api | 80 | 8 | 72 | 3 | 1 | 2 | 2.78% (2/72) | 66.67% (2/3) |
| Ab2d+spec | 80 | 36 | 44 | 3 | 2 | 2 | 4.55% (2/44) | 66.67% (2/3) |
| **Total** | **320** | **78** | **242** | **10** | **5** | **6** | **2.48% (6/242)** | **60.00% (6/10)** |

---

## 4. 6 格個案摘要 (Case Summaries)

1. **Cell #1** (`...ce112_q04_radical...__ab2g__seed_2026072004`)
   - Condition: Ab2g | Family: Radical | Rule: `L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP`
   - Primary: Rescued | Post-hoc: Rescued
   - 摘要: 通用鷹架下根式簡化題，模型生成正確運算但包覆於 JSON dict，經 AST 解包後直接 PASS。

2. **Cell #2** (`...ce113_q01_negative_fraction...__ab2d_spec_v2__seed_2026072002`)
   - Condition: Ab2d+spec | Family: Fraction | Rule: `L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP`
   - Primary: Rescued | Post-hoc: Rescued
   - 摘要: 家族規格下負分數減法題，模型包覆 JSON 外層，解包後通過。

3. **Cell #3** (`...ce113_q01_negative_fraction...__ab2g__seed_2026072003`)
   - Condition: Ab2g | Family: Fraction | Rule: `L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP`
   - Primary: Rescued | Post-hoc: Rescued
   - 摘要: 通用鷹架下負分數減法題，解包後通過。

4. **Cell #4 (Incremental +1 Cell)** (`...ce115_calc_radical...__ab2d__seed_2026071301`)
   - Condition: Ab2d+api | Family: Radical | Rule: `L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP`
   - Primary: NO_OP (False-loop Rollback) | Post-hoc: MODIFIED_RESCUED
   - 摘要: **Post-hoc 增量救回核心案例**。Primary 流程因誤判迴圈導致無效 Rollback；Corrected-Chain 修正判斷後保留解包修改，順利達成正式 PASS。

5. **Cell #5** (`...ce115_calc_radical...__ab2d__seed_2026072002`)
   - Condition: Ab2d+api | Family: Radical | Rule: `L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP`
   - Primary: Rescued | Post-hoc: Rescued
   - 摘要: API 暴露下根式簡化題，解包後通過。

6. **Cell #6** (`...ce115_calc_radical...__ab2d_spec_v2__seed_2026071301`)
   - Condition: Ab2d+spec | Family: Radical | Rule: `L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP`
   - Primary: Rescued | Post-hoc: Rescued
   - 摘要: 家族規格下根式簡化題，解包後通過。

---

## 5. 解讀限制 (Methodological Limitations & Strict Interpretation Rules)

本報告嚴格遵循以下描述性解讀限制：
1. **不得宣稱因果因應**：禁止宣稱 Prompt 條件直接「造成」某類語法錯誤或 Payload 包覆。
2. **不得宣稱條件適配**：禁止宣稱 `Ab2d+api` 比其他條件「更適合」Radical 題型。
3. **不得宣稱 Ab1 不可修復**：Ab1 在本模型下僅有 1 格 Eligible (落入 repaired_still_fail)，不可推論 Ab1 「天生無法修復」。
4. **不得跨模型推廣**：6 格救援結果僅代表 Qwen 3.5 4B 在特定採樣與 Prompt 組合下之特例，不得宣稱推廣至 Qwen 9B、Gemini 或其他模型。
5. **不得重分類第 6 格**：第 6 格屬 Post-hoc corrected-chain 之補充驗證結果，**不得歸入 Primary 預註冊成果**。
6. **不得過度解讀安全性**：巧合通過 Evaluator 不等於完全數學安全；救援價值嚴格限定於「確定性規則」與「無倒退前提」。

---

## 6. SHA 保護驗證 (SHA Protection Verification)

所有凍結與正式基準檔案經 SHA256 比對完全一致，無任何篡改：

```text
dcf6ae6ee0ac94b5896d8bc0d037ef4f06b7a3de905edf1be891022c6fd0754b  docs/experiments/reports/math16_pilot02_final_report_v13.md
de11b9bd5038171689ee2895fc3a499a7b404f5259b3f5b3bcc31cb4d4af2225  docs/experiments/milestones/math16_pilot02_evidence_complete_v1/evidence_complete_manifest.json
84556dc38e0d21cc57f96b0d44092a516cdd76806c6f7468c0286475e23676b1  docs/experiments/manifests/math16_ab3_freeze_manifest.json
d6060e712a38738396119d148f30cb15978c25d85cbce188ef43ccd4e07dcdae  docs/experiments/audits/math16_pilot02_qwen4b_posthoc_corrected_chain_freeze_v1.json
```

---

## 7. 結案 Verdict

```text
MATH16_SIX_CELL_RESCUE_MECHANISM_AUDIT_V1_COMPLETED
SIX_CELL_CROSS_ANALYSIS_COMPLETED
PRIMARY_POSTHOC_SET_RELATION_VERIFIED
REPAIR_SIGNATURE_CATALOG_FROZEN
OFFICIAL_RESULTS_AND_FINAL_REPORT_PRESERVED
READY_FOR_UNRESTRICTED_STRESS_TEST_PREREGISTRATION
```
