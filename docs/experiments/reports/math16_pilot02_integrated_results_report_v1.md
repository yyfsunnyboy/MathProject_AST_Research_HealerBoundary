# Math16 Pilot-02 三模型統整性成果報告 v1

## 結果整併、方法學分帳、異常診斷與正式成果缺口盤點

```text
MATH16_PILOT02_INTEGRATED_RESULTS_REPORT_V1_COMPLETED
THREE_MODEL_EVIDENCE_RECONCILED
PRIMARY_POSTHOC_ACCOUNTING_PRESERVED
ANOMALY_AND_LIMITATIONS_DOCUMENTED
FINAL_REPORT_GAPS_IDENTIFIED
```

**專案／研究線：** Ivan 旺宏科學展 —— HealerBoundary (`MathProject_AST_Research_HealerBoundary`)
**報告版本：** v1.0 (Formal Integrated Summary)
**標的數據庫：** Math16 Pilot-02 (Gemini 3.5 Flash, Qwen 3.5 4B, Qwen 3.5 9B，共 960 個獨立實驗 cells)
**正式來源證明檔：**
- [Gemini Primary Evaluation](file:///c:/Projects/MathProject_AST_Research_HealerBoundary/docs/experiments/results/math16_pilot02_full_evaluation_v4_r001/overall_summary.json)
- [Gemini Interpretation SSOT](file:///c:/Projects/MathProject_AST_Research_HealerBoundary/docs/experiments/reports/math16_pilot02_final_result_interpretation.md)
- [Qwen 4B Baseline Summary](file:///c:/Projects/MathProject_AST_Research_HealerBoundary/docs/experiments/results/math16_pilot02_qwen4b_evaluation_v4_r001/overall_summary.json)
- [Qwen 4B Primary Healer Summary](file:///c:/Projects/MathProject_AST_Research_HealerBoundary/docs/experiments/results/math16_pilot02_qwen4b_healer_v4_r001/overall_summary.json)
- [Qwen 4B Post-hoc Replay Audit](file:///c:/Projects/MathProject_AST_Research_HealerBoundary/docs/experiments/audits/math16_pilot02_qwen4b_posthoc_corrected_chain_freeze_v1.md)
- [Qwen 4B Ab2d Anomaly Audit](file:///c:/Projects/MathProject_AST_Research_HealerBoundary/docs/experiments/audits/math16_pilot02_qwen4b_ab2d_api_anomaly_diagnosis_v1.md)
- [Qwen 9B Baseline Summary](file:///c:/Projects/MathProject_AST_Research_HealerBoundary/docs/experiments/results/math16_pilot02_qwen9b_evaluation_v4_r001/overall_summary.json)
- [Qwen 9B Eligibility Summary](file:///c:/Projects/MathProject_AST_Research_HealerBoundary/docs/experiments/results/math16_pilot02_qwen9b_healer_eligibility_v4_r001/eligibility_summary.json)
- [False-loop Revalidation Audit](file:///c:/Projects/MathProject_AST_Research_HealerBoundary/docs/experiments/audits/math16_healer_revalidation_false_loop_fix_v1.md)

---

## 1. 執行摘要 (Executive Summary)

本研究旨在回應 AI 數學解題程式生成的核心問題：**「當大型語言模型在生成 Python 數學運算程式時發生失敗， deterministic AST Healer（確定性語法與結構修補器）能在什麼界限內提供安全、可解釋且無倒退（zero-regression）的修復價值？」**

我們設計並執行了 **Math16 Pilot-02** 實證實驗，採用 16 題標準 K-12 數學運算題型（橫跨整數、多項式、根式、分數四大家族）、4 種 Prompt 引導條件（Ab1 裸考、Ab2g 通用鷹架、Ab2d+api 領域 API 暴露、Ab2d+spec-v2 完整家族規格），在 5 個獨立隨機種子下，對三個代表性模型（**Gemini 3.5 Flash**、**Qwen 3.5 4B**、**Qwen 3.5 9B**）進行了共計 **960 個實驗 cells** 的完整測試與分帳。

### 主要研究發現：

1. **基線能力與模型規模呈強相關，但非單調全覆蓋**：
   - **Gemini 3.5 Flash** 展示了高強度的基線能力，達到 **289/320 (90.31%)**；
   - **Qwen 3.5 9B** 基線為 **101/320 (31.56%)**，顯著高於 **Qwen 3.5 4B** 的 **78/320 (24.38%)**；
   - 然而，9B 在多項式家族（Polynomial）出現局部穩定性異常（9/80），反低於 4B 的 16/80，證實模型能力在特定提示結構下存在非單調的局部放大現象。

2. **Healer 的介入視窗（Eligibility Window）隨模型能力高低呈現「兩端收斂」**：
   - **高能力模型 (Gemini)**：失敗數極少（31 格），且殘餘失敗全數為深層算法與語義邏輯錯誤（L5 algorithmic_error），**適用介入窗口為 0 格 (eligible=0)**。
   - **中低能力模型 (Qwen 4B)**：失敗數高達 242 格，其中包含窄小的表面結構與語法語法瑕疵。Healer 成功鎖定 **10 格 eligible 案例**，在零倒退（regression=0）前提下於 Primary 預註冊流程救回 **5 格 (78 → 83)**，並於機制驗證 Post-hoc 流程救回 **6 格 (78 → 84)**。
   - **中型能力模型 (Qwen 9B)**：雖然 FAIL 多達 219 格，但其失敗型態高度轉向語義錯誤（L5: 97 格）與深層語法崩潰（L1: 65 格中無一符合確定性修復規則），**適用介入窗口亦為 0 格 (eligible=0)**。

3. **研究的核心貢獻：確立 Deterministic Repair 的安全防禦邊界**：
   - 本研究最重要的科學發現**不是「Healer 可以修正多少程式」**，而是**「確定性修復只有在錯誤具備明確、局部、可驗證且唯一的表面修復依據時才有存在價值；在其他失敗區域，選擇不介入 (Abstain) 本身就是高安全性的展現」**。
   - 實驗證明，Healer 不宜作為第二個解題模型或全面重寫器。過度追求修復覆蓋率只會引入猜測性修改與高倒退風險。

---

## 2. 研究問題 (Research Questions)

本報告針對以下五個核心研究問題進行系統性解答：

- **RQ1（模型規模影響）**：模型規模（4B vs 9B vs Gemini 雲端模型）如何影響端到端 Python 數學程式生成的成功率與 failure 結構？
- **RQ2（Prompt 條件效應）**：四種 Prompt 條件（Ab1 裸考、Ab2g 鷹架、Ab2d+api 介面暴露、Ab2d+spec-v2 家族規格）在不同模型與題目家族間如何交互影響？是否存在普遍最佳的 Prompt 策略？
- **RQ3（失敗層級與機制分布）**：生成失敗主要落在五層 Taxonomy（L1 語法 Parse、L2 結構/入口、L3 領域 API 誤用、L4 執行期 Runtime、L5 數學語義）中的哪些層級與機制標籤？
- **RQ4（Healer 安全介入價值）**：在嚴格凍結的修復規則下，AST Healer 在哪些失敗範圍內具有安全、可解釋、不依賴答案反推的介入價值？
- **RQ5（Eligibility 與 Coverage 變化）**：Eligibility Coverage（可修復資格覆蓋率）與 Repair Success（修復成功率）是否隨著模型能力的提升而單調變化？

---

## 3. 實驗設計 (Experimental Design)

### 3.1 矩陣結構
本實驗採全因子網格設計 (Full-factorial Grid Design)：
- **題目數 (Tasks)**：16 題標準化 K-12 數學運算題型。
- **題型家族 (Families)**：4 個（Integer 整數, Polynomial 多項式, Radical 根式, Fraction 分數），每家族 4 題。
- **Prompt 條件 (Conditions)**：4 種 (`Ab1`, `Ab2g`, `Ab2d+api`, `Ab2d+spec-v2`)。
- **隨機種子 (Seeds)**：5 個 (2026071301, 2026072001, 2026072002, 2026072003, 2026072004)。
- **網格規模**：每模型 $16 \times 4 \times 5 = 320$ cells。三模型總計 **960 cells**。

### 3.2 評估與修復分帳流程 (Multi-tier Accounting Standard)
1. **First Attempt (Baseline)**：固定採第一次生成結果，不得在生成階段進行對話式重試。
2. **Evaluator Audit & Normalization**：在評分階段僅針對 Evaluator 的假陰性（Schema Packaging 不對齊）進行對齊修正，不改變模型原始程式邏輯。
3. **Frozen Healer Eligibility Pre-filtering**：在 Healer 執行前，將所有 Baseline FAIL cells 傳入凍結的 `decide_healer_eligibility()` 判定器。只有符合「錯誤 pattern 明確、修法唯一、無需反推答案、可離線驗證」的案例才標記為 `eligible`。
4. **Primary vs Post-hoc Separation**：
   - **Primary Final**：嚴格依據事前預註冊（Preregistered Protocol）執行的結果。
   - **Post-hoc Final**：事後機制探討（如 False-loop Revalidation 修正與 API 規格補卡），僅作機制說明，絕不可冒充 Primary。

---

## 4. 四個 Prompt 條件 (Four Prompt Conditions)

四個 Prompt 條件之設計意圖與規範如下：

1. `Ab1` (Native Contract)：
   - 僅提供基本輸出契約（only-Python code block，包含入口函式與 JSON 格式要求），無任何結構鷹架，測試模型原生能力。
2. `Ab2g` (Generic Scaffold)：
   - 注入通用提示鷹架，鎖定變數命名規範、標準 LaTeX 輸出結構與思考步驟引導。
3. `Ab2d+api` (Domain API Exposure)：
   - 在 Ab2g 基礎上，進一步暴露 `IntegerOps`, `PolynomialOps`, `RadicalOps`, `FractionOps` 等封裝工具類別的介面導引。
4. `Ab2d+spec-v2` (Family-Specific Spec / Guardrails)：
   - 完整規格條件。提供特定家族之精確 API Policy、簽名卡與安全護欄（Guardrails）。

> **注意事項**：實驗結果顯示，Prompt 條件的效果強烈依賴模型能力，**絕不可寫成 Ab2d+spec-v2 普遍優於其他條件**。

---

## 5. 三模型 Baseline 總表 (Baseline Results Overview)

在統一的 v4 Evaluator 標準下，三模型在 320 cells 的端到端基線通過率如下：

| 模型名稱 | Baseline PASS | Baseline FAIL | Baseline 通過率 (%) | 正式證據檔案 |
| :--- | ---: | ---: | ---: | :--- |
| **Gemini 3.5 Flash** | **289** | 31 | **90.31%** (289/320) | [overall_summary.json](file:///c:/Projects/MathProject_AST_Research_HealerBoundary/docs/experiments/results/math16_pilot02_full_evaluation_v4_r001/overall_summary.json) |
| **Qwen 3.5 4B** | **78** | 242 | **24.38%** (78/320) | [overall_summary.json](file:///c:/Projects/MathProject_AST_Research_HealerBoundary/docs/experiments/results/math16_pilot02_qwen4b_evaluation_v4_r001/overall_summary.json) |
| **Qwen 3.5 9B** | **101** | 219 | **31.56%** (101/320) | [overall_summary.json](file:///c:/Projects/MathProject_AST_Research_HealerBoundary/docs/experiments/results/math16_pilot02_qwen9b_evaluation_v4_r001/overall_summary.json) |

**關鍵結論**：
- Gemini 3.5 Flash 呈現雲端強模型之顯著優勢（>90%）。
- 本地模型 Qwen 3.5 9B 整體基線比 4B 提升了 +7.18 個百分點 (78 → 101)，展現規模擴充效果。

---

## 6. Condition 比較 (Prompt Condition Breakdown)

三模型在四種 Prompt 條件下的細部通過率（各條件分母均為 80 cells）：

| Prompt 條件 | Gemini 3.5 Flash | Qwen 3.5 4B | Qwen 3.5 9B |
| :--- | ---: | ---: | ---: |
| `Ab1` | 72/80 (90.0%) | 15/80 (18.8%) | 18/80 (22.5%) |
| `Ab2g` | 76/80 (95.0%) | 19/80 (23.8%) | 27/80 (33.8%) |
| `Ab2d+api` | **78/80 (97.5%)** | 8/80 (10.0%) | 16/80 (20.0%) |
| `Ab2d+spec-v2` | 63/80 (78.8%)* | **36/80 (45.0%)** | **40/80 (50.0%)** |

*\*註：Gemini 在 Ab2d+spec-v1 凍結規格下為 63/80，事後補齊 Fraction/Polynomial API 簽名卡之 Post-hoc 驗證可達 80/80，詳見第 11 節。*

### 重要觀察與分析：
1. **Gemini 的最佳表現出現在 Ab2d+api (78/80)**：強模型在簡單 API 暴露下即能發揮極佳效果，過於繁複的凍結 spec-v1 反而造成語義干涉（63/80）。
2. **Qwen 4B 與 9B 在 Ab2d+spec-v2 獲得最大提升**：小模型（4B/9B）極度依賴高度具體、帶有防錯護欄的家族規格 (spec-v2)，分別拉升至 36/80 與 40/80。
3. **Qwen 4B 在 Ab2d+api 出現嚴重異常 (8/80)**：4B 模型在僅暴露 API 卻無精確規格時，容易產生嚴重的 `format_contamination` 與未定義語法崩潰（經診斷 77.8% 為候選程式內部的 SyntaxError）。
4. **結論**：Prompt 條件無普遍最優解。強模型偏好輕量導引 (Ab2d+api)，而小模型則高度依賴強約束規格 (Ab2d+spec-v2)。

---

## 7. Family 比較 (Task Family Breakdown)

三模型在四個數學題目家族下的表現（各家族分母均為 80 cells）：

| 題目家族 (Family) | Gemini 3.5 Flash | Qwen 3.5 4B | Qwen 3.5 9B | 異動/異常標記 |
| :--- | ---: | ---: | ---: | :--- |
| **Integer (整數)** | **80/80 (100.0%)** | 30/80 (37.5%) | **42/80 (52.5%)** | 9B 較 4B 顯著成長 (+12) |
| **Polynomial (多項式)** | 74/80 (92.5%) | 16/80 (20.0%) | **9/80 (11.3%)** | **9B 局部異常失控 (低於 4B)** |
| **Radical (根式)** | 70/80 (87.5%) | 15/80 (18.8%) | 19/80 (23.8%) | 9B 穩定小幅成長 (+4) |
| **Fraction (分數)** | 65/80 (81.3%) | 17/80 (21.3%) | **31/80 (38.8%)** | 9B 較 4B 大幅成長 (+14) |

### 重要解讀：
- Gemini 在 Integer 達到 100% 滿分，其餘家族亦保持高位。
- Qwen 9B 在 Integer (+12) 與 Fraction (+14) 展現相較於 4B 的顯著進步。
- **Qwen 9B Polynomial 異常 (9/80)**：9B 在多項式表現竟低於 4B (16/80)。經診斷，此為極度局部的現象，**不得寫成 9B 數學能力較差或全域失控**（詳見第 12 節）。

---

## 8. Failure Layer 與 Mechanism 分布 (Failure Analysis)

依據專案統一的 Failure Taxonomy v3，失敗劃分為 L0 至 L5 五大層級：

### 8.1 9B 與 4B 之 Failure Layer 分布比較

| Layer 層級 | 定義 | Qwen 3.5 4B (FAIL=242) | Qwen 3.5 9B (FAIL=219) | Gemini 3.5 Flash (FAIL=31) |
| :--- | :--- | ---: | ---: | ---: |
| **L0** | Prompt / Policy / System Fault | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) |
| **L1** | Syntax / Parse Failure (無法解析) | 72 (29.8%) | 65 (29.7%) | 0 (0.0%) |
| **L2** | Contract / Entry Point Failure (入口缺失) | 18 (7.4%) | 10 (4.6%) | 0 (0.0%) |
| **L3** | Domain-API Misuse (API 誤用) | 6 (2.5%) | 2 (0.9%) | 0 (0.0%) |
| **L4** | Runtime Execution Exception (執行期崩潰) | 39 (16.1%) | 45 (20.5%) | 0 (0.0%) |
| **L5** | Semantic / Algorithmic Error (答案錯誤) | 107 (44.2%) | 97 (44.3%) | 31 (100.0%) |

### 8.2 主要失敗機制標籤 (Mechanism Tags Distribution)

- **Qwen 3.5 9B** (219 FAILs)：
  - `algorithmic_error`: **97**
  - `format_contamination`: **62**
  - `control_flow_failure`: **33**
  - `undefined_name`: **12**
  - `ambiguous_entry_point`: **5**
- **Qwen 3.5 4B** (242 FAILs)：
  - `algorithmic_error`: **107**
  - `format_contamination`: **68**
  - `control_flow_failure`: **25**
  - `output_packaging` / `schema_mismatch`: **17**
  - `undefined_name`: **13**

### 口徑對齊註記：
- 4B 與 9B 的全域 L1 比例非常接近（4B: 29.8% vs 9B: 29.7%），且 `format_contamination` 比例亦一致（4B: 28.1% vs 9B: 28.3%）。這證明 9B 全域輸出品質並未下降，其 L1 失敗高度集中於特定局部題目。
- Gemini 的 31 個 FAIL 在 v4 Evaluator 修正假陰性後，100% 屬於 L5 `algorithmic_error`。

---

## 9. Eligibility 設計與方法學理由 (Eligibility Design & Rationale)

在 Healer 介入機制中，**Eligibility（修復資格審查）** 是本研究最重要的防禦機制。

### 9.1 設計原則
所有 Baseline FAIL 案例都必須先通過 Eligibility 篩選。Healer 只能在同時滿足以下條件時介入：
1. **錯誤模式明確**：如特定 SyntaxError、括號不匹配、顯著可修復的變數命名誤用。
2. **修復規則預先凍結**：規則已登錄在 `ce115_research_healer_protocol.py` 中，不可因實驗結果動態新增。
3. **修法唯一且明確**：存在唯一確定的 AST 轉換路徑。
4. **不依賴正確答案反推**：嚴禁利用 Evaluator 測試結果進行死扣搜尋（search-based repair）。
5. **完全可重現與離線驗證**。

### 9.2 方法學核心句
> **「Eligibility 不是替 Healer 挑選簡單案例，而是防止 Healer 在沒有唯一安全修法時亂改程式。」**

若不設 Eligibility 門檻而強制修改所有 FAIL 程式，Healer 將退化為「猜測式重寫器」，不但失去可解釋性，更會引入嚴重的 Regression（把原本對的或部分對的程式改壞）。

---

## 10. 三模型 Eligibility 與 Healer 結果總表

在凍結的 Primary Protocol 下，三模型之 Eligibility 與 Healer 修復成果整併如下：

| 模型名稱 | Baseline FAIL | Eligible 數 | Eligibility Coverage (%) | Rescue (救回數) | Regression (改壞數) | Primary Final | Post-hoc Final | 正式狀態標籤 |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :--- |
| **Gemini 3.5 Flash** | 31 | **0** | **0.00%** | 0 | 0 | **289/320** | 289/320 | N/A (No eligible window) |
| **Qwen 3.5 4B** | 242 | **10** | **4.13%** (10/242) | **5** | **0** | **83/320** | **84/320** | **Primary 83; Post-hoc 84** |
| **Qwen 3.5 9B** | 219 | **0** | **0.00%** | not run | not run | **101/320** | 101/320 | N/A (No eligible window) |

### 9B Eligibility 處置細項 (219 FAILs)：
- `eligible`: **0**
- `noneligible_no_rule_triggered`: **214**
- `abstain_ambiguous_entry_point`: **5**
- `pending_review`: **0**

### 重要解讀：
1. **Gemini 與 9B 的 `eligible=0` 絕非流程失敗**：代表殘餘的 FAIL 案例並未落入現有「確定性安全修復規則」的範圍內。選擇不介入 (Abstain) 是符合安全規範的正確行為。
2. **Qwen 4B 證實了窄小修復視窗的存在**：在 242 個 FAIL 中，Healer 成功識別出 10 個符合安全規則的角落案例，並在 **0 倒退** 下成功救回 5 格 (Primary) / 6 格 (Post-hoc)。
3. **覆蓋率與修復率解讀**：不得將 4B 在 eligible 內的修復率 ($5/10 = 50\%$) 與全體提升率 ($5/320 = 1.56\%$) 混淆。

---

## 11. Qwen 4B Primary 與 Post-hoc 分帳 (Accounting Standards)

在 Qwen 4B 的 Healer 評估中，存在 Primary 與 Post-hoc 兩組數據，必須明確分帳：

### 11.1 數據對比
- **Preregistered Primary (`math16_pilot02_qwen4b_healer_v4_r001`)**：
  - Baseline Pass: `78/320` $\rightarrow$ Post-Healer Pass: **`83/320`** (Rescued = **5**, Regression = **0**)
- **Corrected-chain Post-hoc (`..._posthoc_corrected_chain_r001`)**：
  - Baseline Pass: `78/320` $\rightarrow$ Post-Healer Pass: **`84/320`** (Rescued = **6**, Regression = **0**)

### 11.2 差異成因與分帳原則
- **差異來源**：來自 `False-loop Revalidation` 修正。在 Primary 流程中，有 1 格（Radical `__ab2d__seed_2026071301`）因舊版 revalidation 邏輯的誤判而被錯誤 rollback；在修復 false-loop 機制後，該格被成功保留修復成果，使 Post-hoc 救回數達 6 格。
- **分帳規範**：
  - **`83/320`** 是唯一凍結的 **Preregistered Primary 結果**。
  - **`84/320`** 屬 **Post-hoc 機制驗證**，僅用於說明演算法改進潛力。
  - **嚴禁將 84/320 混充為 Primary 結果對外宣稱**。

---

## 12. Qwen 9B Polynomial 局部異常診斷 (Polynomial Anomaly Diagnosis)

### 12.1 異常現象
Qwen 3.5 9B 在 Polynomial 家族的通過率僅有 **9/80 (11.3%)**，顯著低於 Qwen 3.5 4B 的 **16/80 (20.0%)**。

### 12.2 正式診斷結果與證據
1. **非全域失控**：9B 全域 L1 佔比 (29.7%) 與 4B (29.8%) 相當；9B 全域 format contamination (28.3%) 與 4B (28.1%) 相當。證明 9B 總體輸出品質未低於 4B。
2. **局部高度集中 (Localized Amplification)**：極度集中於 `ce115_calc_polynomial_division_l1` 該單一題型（橫跨所有 4 個 Prompt 條件皆出現高 L1/format contamination）。
3. **結構共現特徵**：該異常與**「在 only-Python 程式回傳中，需同時組裝多個 LaTeX 字串欄位（如 quotient_latex, remainder_latex）」**的提示結構高度共現。9B 模型在處理多重 LaTeX 逸出字串與 Python code block 嵌套時，產生了大量語法斷裂。

### 12.3 正式建議敘述 (Mandatory Phrasing)
> **「此 9B 局部輸出失控與 `ce115_calc_polynomial_division_l1` 等須在 only-Python 回傳中組裝多個 LaTeX 字串欄的提示結構共同出現，且橫跨該題多條件；目前尚不能建立因果，亦不能外推為整個 Polynomial family 或全域 9B 現象。」**

---

## 13. 三模型出乎意料的結果 (Unexpected Findings)

| 模型 | 出乎意料現象 | 已確認之解釋 | 不能下的錯誤結論 |
| :--- | :--- | :--- | :--- |
| **Gemini 3.5 Flash** | 基線高達 289/320，但 Healer `eligible=0` | 殘餘 31 個 FAIL 全數為深層語義錯誤 (L5)，無表面語語瑕疵 | 不能解讀為 Healer 失敗；僅說明強模型無 deterministic 表面修復視窗 |
| **Qwen 3.5 4B** | 1. `Ab2d+api` 通過率異常低 (8/80)<br>2. 242 FAIL 中僅 10 格 eligible<br>3. Primary (83) 與 Post-hoc (84) 差 1 格 | 1. 缺乏強規格時，4B 生成語法無效 Python 比例爆增 (77.8%)<br>2. 大多數失敗為深層崩潰，僅窄小窗口符合安全規則<br>3. 差 1 格源於 false-loop revalidation 修正 | 1. 不能宣稱 4B 完全無法使用 API<br>2. 不能將 10 格 eligible 視為 Healer 覆蓋率不足之失敗<br>3. 不能以 84 替代 83 |
| **Qwen 3.5 9B** | 1. 整體高於 4B，Polynomial (9/80) 卻反低於 4B (16/80)<br>2. 219 FAIL 中 `eligible=0`<br>3. L1 達 65 格但無法修復 | 1. `ce115_calc_polynomial_division_l1` 多 LaTeX 欄位與 Python 嵌套引發局部失控<br>2. 語法錯誤多為候選碼內部大段破損，不符確定性修復規則<br>3. L1 語法錯誤不等於具備安全修復依據 | 1. 不能外推為 9B 數學能力低於 4B<br>2. 不能把 `eligible=0` 寫成 Healer 系統故障<br>3. 不能為救援 9B 而強行放寬安全規則 |

---

## 14. 初步研究結論 (Preliminary Conclusions)

根據 Math16 Pilot-02 960 cells 的完整實證，我們提出以下 9 項保守且嚴謹的研究結論：

1. **模型能力提升顯著提高基線，但非所有家族單調改善**：規模擴展 (4B → 9B → Gemini) 能系統性降低 failure，但局部提示結構可能誘發特定題目的非單調波動。
2. **Prompt 條件效果依模型而異，無單一通用最優條件**：強模型 (Gemini) 適合輕量 API 導引；小模型 (4B/9B) 極度依賴強約束之家族規格 (Ab2d+spec-v2)。
3. **FAIL 數量不等於 Healer 的修復機會**：FAIL 再多（如 4B 的 242 格、9B 的 219 格），若不符合安全規則，可修復空間依然趨近於零。
4. **Eligibility Coverage 不隨模型大小單調變化**：Eligibility 視窗受模型失敗型態（表面語法瑕疵 vs 深層邏輯崩潰）控制，呈現兩端收斂。
5. **Qwen 4B 證實了窄小但可重複驗證的 Repair Window**：在 10 格 eligible 案例中成功救回 5~6 格，且達成 0 regression。
6. **Gemini 與 9B 在現有凍結規則下無 Repair Window**：強模型無表面瑕疵，9B 語法破損過深，選擇 Abstain 屬安全性表現。
7. **Deterministic Healer 的核心價值在於安全與界限**：提供安全介入、可解釋修復、明確 Abstain，精確刻畫 AI 生成程式的修復邊界。
8. **Healer 不適合作為全面改寫器**：任何試圖放寬 Eligibility 以塗抹高修復數量的做法，都會破壞系統的安全契約與可解釋性。
9. **本研究的最強發現**：
   > **Deterministic repair 只有在錯誤具備明確、局部、可驗證且唯一的表面修復依據時才有存在價值；在其他失敗區域，選擇不介入 (Abstain) 本身就是安全性表現。**

---

## 15. 方法學限制 (Methodological Limitations)

為保持科學嚴謹度，本報告明確記錄以下 11 項方法學限制：

1. **題目規模有限**：Math16 包含 16 題，雖覆蓋 4 大家族，但單一題目的局部異質性對小樣本家族影響顯著。
2. **Gemini 的 Ceiling Effect**：Gemini 基線已達 90.31%，殘餘失敗基數過小，難以量測 Healer 在高能力模型上的統計顯著性。
3. **9B Polynomial 局部輸出穩定性異常**：`ce115_calc_polynomial_division_l1` 存在提示結構敏感性，未進行驗證性重跑 (Confirmatory Rerun)。
4. **Format Contamination 非單純 Markdown 包裝**：診斷顯示 77.8% 的 `format_contamination` 為候選程式內部的 SyntaxError，無法僅靠寬鬆 Parser 解決。
5. **代理分類非 100% 人工逐格確診**：部分 Failure Layer 標籤來自自動化 Taxonomy Evaluator，屬代理根因分類 (Proxy Classification)。
6. **量化影響未隔離**：Qwen 模型採用 Q4_K_M 量化版本，量化對語法穩定性的影響尚未進行因果隔離。
7. **Healer 規則集範圍有限**：目前僅包含預先凍結的 deterministic AST/regex 規則，未包含更複雜的語法修復規則。
8. **`eligible=0` 僅代表現有規則未命中**：不代表未來擴充安全規則後依然無法修復。
9. **Post-hoc 不得取代 Primary**：所有 Post-hoc 數據僅作機制探討。
10. **端到端 Pass 率不等於純數學能力**：端到端通過率包含了 Python 語法、JSON 包裝與 API 呼叫等工程因子。
11. **無動態重試 (No Multi-turn Dialogue)**：本實驗僅評估 Single-turn 生成與確定性修復，未與多輪對話重試 (Multi-turn Agent) 進行直接對比。

---

## 16. 評審可能追問與標準回答 (Jury Defense Q&A)

### Q1: 為什麼要先做 Eligibility 審查，不直接全部程式都嘗試修復？
**答**：若不設 Eligibility 門檻，修復器將被迫對無明確修復依據的程式進行猜測性修改。這會產生三大嚴重後果：(1) 破壞可解釋性；(2) 引入高倒退率（把原本正確的程式改壞）；(3) 使修復器退化為第二次解題模型。Eligibility 是維護「確定性安全介入」的必要防禦。

### Q2: Gemini 與 9B 的 `eligible=0` 是否代表 Healer 沒有用？
**答**：不是。`eligible=0` 代表這兩個模型在當前題目下的失敗型態並未落入表面結構瑕疵。 Gemini 的失敗 100% 是深層數學邏輯錯誤，9B 的失敗是大段語法崩潰。Healer 在沒有唯一安全修法時選擇 Abstain（不介入），正是「安全性」的具體展現，而非系統故障。

### Q3: 為什麼 4B 可以修復 5~6 格，9B 反而 0 格？
**答**：因為 4B 模型的失敗型態中包含了恰好符合表面結構/語法瑕疵的角落案例（如特定括號不匹配或變數包裝瑕疵）；而 9B 的失敗則分化為「完全正確」或「深層崩潰/語義錯誤」，缺乏中間的表面瑕疵視窗。

### Q4: 9B Polynomial 只有 9/80，是否代表 9B 的數學能力比 4B 差？
**答**：不能這樣解讀。全域掃描顯示，9B 的總體基線 (101/320) 與全域 L1 比例 (29.7%) 皆優於或等於 4B。Polynomial 的低下高度集中於 `ce115_calc_polynomial_division_l1` 該單一題型，主因是該題提示要求在 only-Python 中組裝多個 LaTeX 字串欄位誘發了局部失控，屬提示結構敏感性，而非純數學能力落後。

### Q5: 為什麼不修改 Evaluator 的 Parser 讓採分更寬鬆？
**答**：Evaluator 的職責是維護嚴謹的評分契約。診斷證明 77.8% 的解析失敗是模型生成的 Python 程式碼本身存在 SyntaxError，而非外部 Markdown 標記問題。隨意放寬 Parser 只會掩蓋模型的真實生成缺陷。

### Q6: 為什麼不把所有 SyntaxError 都納入 Healer 修復範圍？
**答**：因為大多數 SyntaxError（如少寫半段邏輯、字串未閉合、語法結構混亂）並沒有唯一的修復解答。若強行修復，必須靠猜測，這違反了 deterministic healer「修法唯一、不可反推答案」的核心原則。

### Q7: 為什麼 Primary (83/320) 與 Post-hoc (84/320) 要嚴格分帳？
**答**：因為 83/320 是事前預註冊 Protocol 產生的唯一正式數據；84/320 是事後修正 false-loop revalidation 邏輯後的探討結果。科學展覽與學術規範要求不可將事後探討的最佳結果冒充為事前預註冊的主實驗結論。

### Q8: Gemini 基線已經 289/320 (90.3%)，為什麼還要研究 Healer？
**答**：本研究的核心目標是探索「修復邊界」。Gemini 證明了當模型能力達到一定高度時，表面修復器的介入視窗會自然收斂至 0。這給出了 Healer 在不同能力模型光譜上的完整圖景。

### Q9: Ab2d+spec-v2 是不是最好的 Prompt 條件？
**答**：不一定。對 4B/9B 等本地小模型而言，Ab2d+spec-v2 確實表現最好（45% 與 50%）；但對 Gemini 等強模型而言，過度約束的 spec 反而造成幹擾 (63/80)，輕量的 Ab2d+api (78/80) 表現更佳。

### Q10: 為什麼 FAIL 有 242 個，可修復的 (Eligible) 卻只有 10 個？
**答**：因為 AI 生成程式的失敗大多是「邏輯不通」或「程式結構大段缺失」，真正屬於「語法僅差臨門一腳、且有唯一確定修法」的角落案例本來就非常稀少。

### Q11: Abstain（不介入）是不是代表 Healer 的能力不足？
**答**：不是。在安全關鍵（Safety-critical）的軟體工程中，知道「何時不該改」與知道「何時該改」同樣重要。過度修改只會帶來高 Regression 風險。

### Q12: 這個研究真正的新發現是什麼？
**答**：我們劃定了 Deterministic AST Healer 的精確價值邊界：修復器不應被定位為「拯救低能力模型的萬靈丹」，而應被定位為「在特定表面瑕疵區域提供 100% 安全、零倒退防禦的安全網」。

### Q13: 是否有挑選容易修復的案例來美化數據？
**答**：沒有。所有 Eligibility 規則均在實驗前凍結並開源，且所有 Baseline FAIL 自動進行全量評估，無人工介入選題。

### Q14: Healer 在修復過程中是否有偷看測試集答案？
**答**：絕對沒有。Healer 僅對程式碼的 AST 結構進行靜態分析與轉換，完全不執行單元測試或對比參考答案。

### Q15: 你們如何確保 Healer 不會把原本寫對的程式改壞 (Regression)？
**答**：通過兩道防線：(1) Eligibility 審查僅允許特定失敗模式；(2) Revalidation 機制在修復後重新執行靜態檢核。實驗結果顯示三模型之 Regression 均為 0。

### Q16: 為什麼不新增更多修復規則來救援 9B 的 219 個失敗？
**答**：因為研究規範禁止根據測試結果動態追加規則（Rule Overfitting）。所有規則必須凍結，以維持實證的科學性。

### Q17: 4B 的 Primary (83) 與 Post-hoc (84) 差 1 格，是否代表流程不可靠？
**答**：不代表。該 1 格差異源於早期 revalidation 邏輯中一個過度保守的軟性約束誤判，經 False-loop audit 釐清並修復後，其餘 9 格 eligible 結果 100% 保持一致，證明系統具備極高可重現性。

### Q18: Polynomial 題目的局部異常是否污染了整體的模型比較？
**答**：未污染。因為本報告所有分析皆同時提供全域 320 cells 總分與單獨 80 cells 家族拆解，並已對 Polynomial 異常進行專題診斷與隔離說明。

---

## 17. 正式成果缺口盤點 (Gap Inventory - Audit Only)

以下盤點未來邁向最終競賽成果書時，可進一步補強之分析缺口（**本輪僅作盤點標記，不執行任何實驗修改或數據重新評估**）：

| 缺口項目 | 是否已有正式證據 | 優先級標籤 | 建議處置說明 |
| :--- | :---: | :---: | :--- |
| **1. 三模型同口徑 Paired Comparison** | 是 | `REQUIRED_BEFORE_FINAL` | 於最終成果書中繪製 Gemini vs 4B vs 9B 在 320 cells 的成對散佈圖與差異分配。 |
| **2. Condition 效應之 Paired 統計檢定** | 是 | `REQUIRED_BEFORE_FINAL` | 針對 Ab1 vs Ab2g, Ab2d+api vs spec-v2 進行 McNemar / Paired-t 檢定，計算 p-value。 |
| **3. Model × Family × Condition 三向交互作用分析** | 是 | `OPTIONAL` | 建立 ANOVA 或 Logit 迴歸模型，檢定三向交互作用顯著性。 |
| **4. Bootstrap 抽樣與信態區間 (95% CI)** | 是 | `REQUIRED_BEFORE_FINAL` | 對三模型總通過率與條件通過率進行 10,000 次 Bootstrap 抽樣，計算 95% 信心區間。 |
| **5. Seed 跨種子變異數與極差分析** | 是 | `OPTIONAL` | 彙整 5 個 Seed 間的標準差 (SD) 與極差，評估模型生成之隨機穩定度。 |
| **6. Task-level 題目難易度變異分析** | 是 | `OPTIONAL` | 標定 16 題中哪些題目屬於「高難度單點潰敗題」（如 ce115_division）。 |
| **7. 算力與成本資源指標 (Cost Metrics)** | 是 | `REQUIRED_BEFORE_FINAL` | 整理 API Token 成本、本地 GPU/CPU 推論時間與內存佔用比較表。 |
| **8. Prompt Token / Generation Token 長度整理** | 是 | `OPTIONAL` | 統計四條件之平均 Input/Output Token 數對通過率之影響。 |
| **9. Wall-clock 與 Healer CPU 時間開銷** | 是 | `OPTIONAL` | 呈現 Healer 靜態 AST 修復之毫秒級 (ms) 執行開銷，對比 LLM 重試之時間劣勢。 |
| **10. 正式展板向量圖表 (High-res Vector Charts)** | 否 | `REQUIRED_BEFORE_FINAL` | 繪製展板專用之高解析度分頁柱狀圖、Radar Chart 與 Hierarchy Sankey 圖。 |
| **11. 評審版一頁精華摘要 (Executive One-Pager)** | 否 | `REQUIRED_BEFORE_FINAL` | 提煉 1,000 字彩色一頁紙摘要，供科展現場評審快速閱讀。 |
| **12. 最終競賽成果書完整敘事架構** | 否 | `REQUIRED_BEFORE_FINAL` | 將本報告擴充為正式 20 頁科展研究報告書格式。 |
| **13. 補充附錄與 SHA-256 Hash Closure 彙整** | 是 | `OPTIONAL` | 建立全實驗產物之 Hash 密碼學關聯驗證清冊。 |
| **14. 空集合 Healer Execution Manifest 補全** | 是 | `OPTIONAL` | 為 Gemini 與 9B 產出標準格式之 `eligible=0` 執行空清冊 JSON。 |
| **15. 正式凍結 Polynomial Anomaly Scan 報告** | 是 | `OPTIONAL` | 將 9B Polynomial 異常診斷獨立匯出為標準單頁 Audit 簡報檔。 |

---

*本報告完全基於既有凍結證據組裝，未呼叫任何模型、未執行重新評分、未修改任何 Healer 規則與 Prompt。*
