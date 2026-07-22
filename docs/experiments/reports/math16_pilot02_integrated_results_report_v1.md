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
**報告版本：** v1.1 (Formal Integrated Summary - Methodologically Refined)
**標的數據庫：** Math16 Pilot-02 (Gemini 3.5 Flash, Qwen 3.5 4B, Qwen 3.5 9B，共 960 個獨立實驗 cells)
**正式來源證明檔：**
- [Gemini Primary Evaluation](file:///c:/Projects/MathProject_AST_Research_HealerBoundary/docs/experiments/results/math16_pilot02_full_evaluation_v4_r001/baseline_summary.json)
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

本研究旨在回應 AI 數學解題程式生成的核心問題：**「當語言模型在生成 Python 數學運算程式發生失敗時，deterministic AST Healer（確定性語法與結構修補器）能在什麼界限內提供安全、可解釋且觀察到零倒退 (regression=0) 的修復價值？」**

我們設計並執行了 **Math16 Pilot-02** 實證實驗，採 16 題標準 K-12 數學運算題型（橫跨整數、多項式、根式、分數四大家族）、4 種 Prompt 引導條件（Ab1 裸考、Ab2g 通用鷹架、Ab2d+api 領域 API 暴露、Ab2d+spec-v2 完整家族規格），在 5 個獨立隨機種子下，對三個代表性模型（**Gemini 3.5 Flash**、**Qwen 3.5 4B**、**Qwen 3.5 9B**）進行了共計 **960 個實驗 cells** 的完整測試與分帳。

### 主要研究發現：

1. **三模型基線表現呈現差異，部分家族具非單調波動**：
   - 三模型的端到端基線表現明顯不同；在同一 Qwen 系列與相同主要 sampling 設定下，9B 整體通過數 (101/320) 高於 4B (78/320) 23 格（基線通過率高出 7.18 個百分點）；
   - 然而，9B 在多項式家族（Polynomial）表現為 9/80，低於 4B 的 16/80，顯示特定提示結構下可能出現局部的非單調波動。
   - Gemini 3.5 Flash 的基線通過數為 **289/320 (90.31%)**。

2. **Healer 介入視窗 (Eligibility Window) 在本次三模型中呈非單調分布**：
   - **Gemini 3.5 Flash**：失敗數為 31 格。在目前 v4 taxonomy 分類口徑下，剩餘 31 格均被歸入 L5 algorithmic_error，且沒有案例命中現有凍結 Healer 規則，**適用介入窗口為 0 格 (eligible=0)**。
   - **Qwen 3.5 4B**：失敗數為 242 格。Healer 成功識別出 **10 格 eligible 案例**，在觀察到零倒退 (regression=0) 前提下，於 Primary 預註冊流程救回 **5 格 (78 → 83)**，並於機制驗證 Post-hoc 流程救回 **6 格 (78 → 84)**。
   - **Qwen 3.5 9B**：失敗數為 219 格。其失敗型態多為語義錯誤（L5: 97 格）或大段語法破損（L1: 65 格中無案例命中凍結規則），**適用介入窗口亦為 0 格 (eligible=0)**。

3. **研究的核心貢獻：確立 Deterministic Repair 的安全防禦邊界**：
   - 本研究最重要的科學發現**不是「Healer 可以修正多少程式」**，而是**「確定性修復只有在錯誤具備明確、局部、可驗證且唯一的表面修復依據時才有存在價值；在其他失敗區域，選擇不介入 (Abstain) 本身就是高安全性的展現」**。
   - 實驗證明，Healer 不宜作為第二個解題模型或全面重寫器。過度追求修復覆蓋率只會引入猜測性修改與倒退風險。

---

## 2. 研究問題與比較層級 (Research Questions & Comparison Tiers)

本報告解答以下五個核心研究問題，並明確建立比較層級：

- **RQ1（模型差異）**：不同模型的端到端 Python 數學程式生成成功率與 failure 結構有何差異？
- **RQ2（Prompt 條件效應）**：四種 Prompt 條件（Ab1 裸考、Ab2g 鷹架、Ab2d+api 介面暴露、Ab2d+spec-v2 家族規格）在不同模型與題目家族間如何交互影響？是否存在普遍最佳的 Prompt 策略？
- **RQ3（失敗層級與機制分布）**：生成失敗主要落在五層 Taxonomy（L1 語法 Parse、L2 結構/入口、L3 領域 API 誤用、L4 執行期 Runtime、L5 數學語義）中的哪些層級與機制標籤？
- **RQ4（Healer 安全介入價值）**：在嚴格凍結的修復規則下，AST Healer 在哪些失敗範圍內具有安全、可解釋、不依賴答案反推的介入價值？
- **RQ5（Eligibility 與 Coverage 變化）**：Eligibility Coverage（可修復資格覆蓋率）與 Repair Success（修復成功率）在不同模型間如何分布？

### 比較層級宣告 (Comparison Tiers)

1. **Tier 1 核心比較 (Qwen 3.5 4B vs Qwen 3.5 9B)**：
   - 相同 Qwen 系列、相同題目、相同 Prompt 條件、相同隨機種子 (Seeds) 與主要 sampling 設定。
   - 作為後續正式配對統計與比較分析的核心對象。

2. **Tier 2 描述性強模型參照 (Gemini 3.5 Flash vs Qwen 系列)**：
   - 作為描述性的雲端強模型基線參照。
   - 由於模型家族、部署方式、量化程度與 API 參數量設定不同，**不解讀為純參數規模的單一因果效果**。

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

> **注意事項**：實驗結果顯示，Prompt 條件的效果強烈依賴模型與家族，**不可寫成 Ab2d+spec-v2 普遍優於其他條件**。

---

## 5. 正式結果展現順序與 Baseline 總表

正文展現順序為：**1. Gemini 3.5 Flash** $\rightarrow$ **2. Qwen 3.5 4B** $\rightarrow$ **3. Qwen 3.5 9B**。
理由：Gemini 建立完整方法框架與評估治理；4B 首次揭示實際 Healer repair window；9B 驗證修正後方法並展現非單調邊界。

在統一的 v4 Evaluator 標準下，三模型在 320 cells 的端到端基線通過率如下：

| 模型名稱 | Baseline PASS | Baseline FAIL | Baseline 通過率 (%) | 正式證明檔案 |
| :--- | ---: | ---: | ---: | :--- |
| **Gemini 3.5 Flash** (Tier 2 參照) | **289** | 31 | **90.31%** (289/320) | [baseline_summary.json](file:///c:/Projects/MathProject_AST_Research_HealerBoundary/docs/experiments/results/math16_pilot02_full_evaluation_v4_r001/baseline_summary.json) |
| **Qwen 3.5 4B** (Tier 1 對照) | **78** | 242 | **24.38%** (78/320) | [overall_summary.json](file:///c:/Projects/MathProject_AST_Research_HealerBoundary/docs/experiments/results/math16_pilot02_qwen4b_evaluation_v4_r001/overall_summary.json) |
| **Qwen 3.5 9B** (Tier 1 對照) | **101** | 219 | **31.56%** (101/320) | [overall_summary.json](file:///c:/Projects/MathProject_AST_Research_HealerBoundary/docs/experiments/results/math16_pilot02_qwen9b_evaluation_v4_r001/overall_summary.json) |

**關鍵觀察**：
- 在同一 Qwen 系列與相同主要 sampling 設定下，9B 比 4B 多通過 23 格，基線通過率提高 7.18 個百分點。
- Gemini 3.5 Flash 作為雲端強模型參照，通過率為 90.31% (289/320)。

---

## 6. Condition 比較 (Prompt Condition Breakdown)

三模型在四種 Prompt 條件下的細部通過率（各條件分母均為 80 cells）：

| Prompt 條件 | Gemini 3.5 Flash | Qwen 3.5 4B | Qwen 3.5 9B |
| :--- | ---: | ---: | ---: |
| `Ab1` | 72/80 (90.0%) | 15/80 (18.8%) | 18/80 (22.5%) |
| `Ab2g` | 76/80 (95.0%) | 19/80 (23.8%) | 27/80 (33.8%) |
| `Ab2d+api` | **78/80 (97.5%)** | 8/80 (10.0%) | 16/80 (20.0%) |
| `Ab2d+spec-v2` | 63/80 (78.8%)* | **36/80 (45.0%)** | **40/80 (50.0%)** |

*\*註：Gemini 在 Ab2d+spec-v1 事前凍結規格下為 63/80；事後補齊 Fraction/Polynomial API 簽名卡之 Post-hoc 機制驗證可達 80/80，詳見第 11 節。*

### 重要觀察與分析：
1. **Gemini 在 Ab2d+api 觀察到較高通過率 (78/80)**：在簡單 API 暴露下表現良好，過於繁複的凍結 spec-v1 出現較多 API arity/name 不對齊 (63/80)。
2. **Qwen 4B 與 9B 在 Ab2d+spec-v2 獲得較高通過數**：4B 通過 36/80，9B 通過 40/80，顯示小模型對家族規格 (spec-v2) 具較高依賴度。
3. **Qwen 4B 在 Ab2d+api 通過數較低 (8/80)**：在僅暴露 API 卻無精確規格時出現較多無效 Python 生成。經診斷，在該條件 27 格診斷樣本中，有 77.8% (21/27) 屬候選 Python 本體內部的 SyntaxError。
4. **結論**：Prompt 條件效果依模型而異，無普遍最佳條件。

---

## 7. Family 比較 (Task Family Breakdown)

三模型在四個數學題目家族下的表現（各家族分母均為 80 cells）：

| 題目家族 (Family) | Gemini 3.5 Flash | Qwen 3.5 4B | Qwen 3.5 9B | 觀察差異 |
| :--- | ---: | ---: | ---: | :--- |
| **Integer (整數)** | **80/80 (100.0%)** | 30/80 (37.5%) | **42/80 (52.5%)** | 9B 比 4B 多通過 12 格 |
| **Polynomial (多項式)** | 74/80 (92.5%) | 16/80 (20.0%) | **9/80 (11.3%)** | **9B 通過數少於 4B 7 格** |
| **Radical (根式)** | 70/80 (87.5%) | 15/80 (18.8%) | 19/80 (23.8%) | 9B 比 4B 多通過 4 格 |
| **Fraction (分數)** | 65/80 (81.3%) | 17/80 (21.3%) | **31/80 (38.8%)** | 9B 比 4B 多通過 14 格 |

### 重要解讀：
- Gemini 在 Integer 達到 80/80 (100%)。
- Qwen 9B 在 Integer (+12 格) 與 Fraction (+14 格) 觀察到高於 4B 的通過數。
- **Qwen 9B Polynomial 異常 (9/80)**：9B 在多項式通過數少於 4B 7 格。經診斷，此現象具高度局部性，**不可解讀為 9B 全域失控或純數學能力較差**（詳見第 12 節）。

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

### 口徑與範疇說明：
- 4B 與 9B 的全域 L1 比例接近（4B: 29.8% vs 9B: 29.7%），`format_contamination` 比例亦相近（4B: 28.1% vs 9B: 28.3%）。顯示 9B 全域 L1 失敗比例未擴大，其低分高度集中於特定局部題目。
- 在目前 v4 taxonomy 分類口徑下，Gemini 剩餘 31 格均被歸入 L5 `algorithmic_error`。

---

## 9. Eligibility 設計與方法學理由 (Eligibility Design & Rationale)

在 Healer 介入機制中，**Eligibility（修復資格審查）** 是維護確定性修復的核心機制。

### 9.1 設計原則
所有 Baseline FAIL 案例都必須先通過 Eligibility 審查。Healer 只能在同時滿足以下條件時介入：
1. **錯誤模式明確**：命中預先登錄且凍結的修復規則（如 `L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP`、`L1_PROSE_RESIDUE_NARROW`、`L1_CLOSE_UNBALANCED_PARENTHESIS`）。
2. **修復規則預先凍結**：規則登錄在 `ce115_research_healer_protocol.py` 中，不可動態新增。
3. **修法唯一且明確**：存在唯一確定的 AST 轉換路徑。
4. **不依賴正確答案反推**：不讀取標準答案，也不以測試 PASS/FAIL 搜尋修法。
5. **完全可重現與離線驗證**。

### 9.2 方法學核心句
> **「Eligibility 不是替 Healer 挑選簡單案例，而是防止 Healer 在沒有唯一安全修法時亂改程式。」**

若不設 Eligibility 門檻而強制修改所有 FAIL 程式，Healer 將退化為猜測式重寫器，破壞可解釋性並可能引入倒退 (Regression)。

---

## 10. 三模型 Eligibility 與 Healer 結果總表

在凍結的 Primary Protocol 下，三模型之 Eligibility 與 Healer 修復成果如下：

| 模型名稱 | Baseline FAIL | Eligible 數 | Eligibility Coverage (%) | Rescue (救回數) | Regression | Primary Final | Post-hoc Final | 正式狀態標籤 |
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
1. **Gemini 與 9B 的 `eligible=0` 代表無符合規則案例**：代表殘餘 FAIL 未命中現有凍結 Healer 規則。選擇不介入 (Abstain) 屬符合規範的行為。
2. **Qwen 4B 觀察到窄小的修復視窗**：在 242 個 FAIL 中，識別出 10 個符合規則案例，在觀察到 regression=0 下，於 Primary 救回 5 格 (78 → 83)，於 Post-hoc 救回 6 格 (78 → 84)。
3. **覆蓋率與修復率別區分**：不得將 4B 在 eligible 內的修復率 ($5/10 = 50\%$) 與全體提升率 ($5/320 = 1.56\%$) 混淆。

---

## 11. Qwen 4B 與 Gemini 之 Primary / Post-hoc 分帳

本研究針對事後機制探討（Post-hoc）與事前預註冊（Primary）建立嚴格隔離：

### 11.1 Qwen 4B 分帳
- **Preregistered Primary (`math16_pilot02_qwen4b_healer_v4_r001`)**：
  - Baseline Pass: `78/320` $\rightarrow$ Post-Healer Pass: **`83/320`** (Rescued = **5**, Regression = **0**)
- **Corrected-chain Post-hoc (`..._posthoc_corrected_chain_r001`)**：
  - Baseline Pass: `78/320` $\rightarrow$ Post-Healer Pass: **`84/320`** (Rescued = **6**, Regression = **0**)
- **成因與原則**：差異來自 `False-loop Revalidation` 修正（Radical `__ab2d__seed_2026071301` 1 格保留修復）。`83/320` 為唯一預註冊 Primary 結果；`84/320` 屬 Post-hoc 機制驗證，**不可混充為 Primary**。

### 11.2 Gemini Post-hoc 治理
- **Primary Overall Score**: **289/320** (Ab2d+spec-v1 為 63/80)。
- **Post-hoc Spec Update**: 事後補齊 API 簽名卡後，該條件可達 80/80（Hybrid 盤點為 306/320）。
- **治理聲明**：`306/320` 僅作 Post-hoc 機制說明，**不是正式 Primary Overall Score**，不列入主要結果對照表，亦不與 Qwen 進行直接比較。

---

## 12. Qwen 9B Polynomial 局部異常診斷 (Polynomial Anomaly Diagnosis)

### 12.1 異常現象
Qwen 3.5 9B 在 Polynomial 家族的通過率為 **9/80 (11.3%)**，少於 Qwen 3.5 4B (16/80)。

### 12.2 正式診斷結果與證據
1. **非全域失控**：9B 全域 L1 佔比 (29.7%) 與 4B (29.8%) 相當；9B 全域 format contamination (28.3%) 與 4B (28.1%) 相當。證明 9B 總體輸出品質未低於 4B。
2. **局部高度集中 (Localized Amplification)**：極度集中於 `ce115_calc_polynomial_division_l1` 題型（橫跨 4 個 Prompt 條件皆出現高 L1/format contamination）。
3. **結構共現特徵**：該異常與**「在 only-Python 程式回傳中組裝多個 LaTeX 字串欄位（如 quotient_latex, remainder_latex）」**高度共現，目前尚不能建立因果。

### 12.3 敘述規範與整體評估
> **「此 9B 局部輸出失控與 `ce115_calc_polynomial_division_l1` 等須在 only-Python 回傳中組裝多個 LaTeX 字串欄的提示結構高度共現，但尚未以控制實驗確認因果，亦不能外推為整個 Polynomial family 或全域 9B 現象。」**

**對整體比較之說明**：Polynomial 異常確實壓低 9B 總分，因此解讀整體模型差異時必須註記；本研究透過 family 與 task 分層將其明確揭露，而未將其隱藏或誤解為純數學能力下降。

---

## 13. 三模型出乎意料的結果 (Unexpected Findings)

| 模型 | 觀察現象 | 已確認之解釋 | 不下的錯誤結論 |
| :--- | :--- | :--- | :--- |
| **Gemini 3.5 Flash** | 基線 289/320，但 Healer `eligible=0` | 剩餘 31 格均歸為 L5 algorithmic_error，無案例命中凍結規則 | 不能解讀為 Healer 失敗；僅說明現有凍結規則無適用視窗 |
| **Qwen 3.5 4B** | 1. `Ab2d+api` 通過數較低 (8/80)<br>2. 242 FAIL 中僅 10 格 eligible<br>3. Primary (83) 與 Post-hoc (84) 差 1 格 | 1. 診斷樣本中 77.8% 屬候選 Python 本體 SyntaxError<br>2. 多數失敗非表面瑕疵，僅窄小窗口符合規則<br>3. 差 1 格源於 false-loop revalidation 修正 | 1. 不能宣稱 4B 完全無法使用 API<br>2. 不能將 10 格 eligible 視為流程失敗<br>3. 不能以 84 替代 83 |
| **Qwen 3.5 9B** | 1. 整體通過數高於 4B，Polynomial (9/80) 卻少於 4B<br>2. 219 FAIL 中 `eligible=0`<br>3. L1 達 65 格但無符合規則案例 | 1. `ce115_calc_polynomial_division_l1` 多 LaTeX 欄位與 Python 嵌套高度共現<br>2. 語法錯誤多為候選碼內部大段破損，未命中規則<br>3. L1 語法錯誤不等於具備安全修復依據 | 1. 不能外推為 9B 數學能力低於 4B<br>2. 不能把 `eligible=0` 寫成 Healer 系統故障<br>3. 不能為救援 9B 而強行放寬安全規則 |

---

## 14. 初步研究結論 (Preliminary Conclusions)

根據 Math16 Pilot-02 960 cells 的實證，提出以下 10 項結論：

1. **三模型的端到端通過率不同**。
2. **在同一 Qwen 系列中，9B 整體通過數高於 4B，但 Polynomial 未單調改善**。
3. **Prompt 條件效果依模型與 family 而異**。
4. **FAIL 數量不等於 eligibility coverage**。
5. **Eligibility coverage 在本次三模型中呈非單調分布**。
6. **Qwen 4B 出現窄小且可觀察的 repair window** (Primary 救回 5 格，Post-hoc 救回 6 格)。
7. **Gemini 與 9B 在現有凍結規則下 eligible 為 0**。
8. **Healer 的價值在於選擇性、安全且可解釋的介入**。
9. **Abstain 是安全策略，不代表 Healer 全面有效或全面無效**。
10. **所有結論僅適用於本次題目、模型、prompt 與凍結規則範圍**。

---

## 15. 方法學限制 (Methodological Limitations)

1. **題目規模有限**：Math16 包含 16 題，單一題目的局部異質性對小樣本家族影響明顯。
2. **Gemini 的 Ceiling Effect**：Gemini 基線達 90.31%，殘餘失敗基數過小。
3. **9B Polynomial 局部輸出穩定性異常**：`ce115_calc_polynomial_division_l1` 存在提示結構敏感性，未進行控制實驗確認因果。
4. **77.8% 診斷樣本限制**：僅限定於 Qwen 4B Ab2d+api 診斷樣本，不得外推至其他條件或模型。
5. **代理分類非 100% 人工確診**：部分 Failure Layer 標籤來自自動化 Taxonomy Evaluator (Proxy Classification)。
6. **量化影響未隔離**：Qwen 模型採用 Q4_K_M 量化版本，未隔離量化對語法穩定性的影響。
7. **Healer 規則集範圍有限**：僅包含預先凍結的確定性規則。
8. **`eligible=0` 僅代表現有規則未命中**：不代表未來擴充規則後依然無法修復。
9. **Post-hoc 不得取代 Primary**：所有 Post-hoc 數據僅作機制探討。
10. **端到端 Pass 率不等於純數學能力**：包含 Python 語法、JSON 包裝與 API 呼叫等工程因子。
11. **無動態對話重試**：僅評估 Single-turn 生成與確定性修復。

---

## 16. 評審可能追問與標準回答 (Jury Defense Q&A)

### Q1: 為什麼要先做 Eligibility 審查，不直接全部程式都嘗試修復？
**答**：若不設 Eligibility 門檻，修復器將被迫對無明確修復依據的程式進行猜測性修改，破壞可解釋性並可能引入倒退 (Regression)。Eligibility 是維護「確定性安全介入」的必要防禦。

### Q2: Gemini 與 9B 的 `eligible=0` 是否代表 Healer 沒有用？
**答**：不是。`eligible=0` 代表在本次資料與現有凍結規則下，沒有失敗案例同時滿足唯一、安全、可驗證的介入條件。Healer 在無適用規則時選擇 Abstain（不介入），屬符合規範的行為。

### Q3: 為什麼 4B 可以修復 5~6 格，9B 反而 0 格？
**答**：因為 4B 模型的失敗案例中有 10 格恰好命中既有規則（如 `L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP`、`L1_PROSE_RESIDUE_NARROW`、`L1_CLOSE_UNBALANCED_PARENTHESIS`）；而 9B 的 219 個 FAIL 中，有 214 格未觸發規則 (noneligible_no_rule_triggered)，5 格屬入口點模糊 (abstain_ambiguous_entry_point)。

### Q4: 9B Polynomial 只有 9/80，是否代表 9B 的數學能力比 4B 差？
**答**：不能這樣解讀。9B 總體通過數 (101/320) 高於 4B (78/320)。Polynomial 的低下高度集中於 `ce115_calc_polynomial_division_l1` 單一題型，與多個 LaTeX 欄位組裝高度共現，尚未證實因果，不能外推為純數學能力落後。

### Q5: 為什麼不修改 Evaluator 的 Parser 讓採分更寬鬆？
**答**：Evaluator 的職責是維護嚴謹的評分契約。診斷顯示在特定異常樣本中 77.8% 的解析失敗是模型生成的 Python 程式碼本體存在 SyntaxError，隨意放寬 Parser 只會掩蓋真實生成缺陷。

### Q6: 為什麼不把所有 SyntaxError 都納入 Healer 修復範圍？
**答**：因為大多數 SyntaxError（如少寫半段邏輯、字串未閉合、語法結構混亂）並沒有唯一的修復解答。若強行修復違反了「修法唯一、不可反推答案」的核心原則。

### Q7: 為什麼 Primary (83/320) 與 Post-hoc (84/320) 要嚴格分帳？
**答**：因為 83/320 是事前預註冊 Protocol 產生的唯一正式數據；84/320 是事後修正 false-loop revalidation 邏輯後的探討結果。規範要求不可將事後探討結果冒充為事前預註冊結論。

### Q8: Gemini 基線已經 289/320 (90.3%)，為什麼還要研究 Healer？
**答**：本研究的核心目標是探索「修復邊界」。Gemini 展現了當模型基線較高時，現有表面修復規則的介入視窗會自然收斂至 0。

### Q9: Ab2d+spec-v2 是不是最好的 Prompt 條件？
**答**：不一定。對 4B/9B 等小模型而言，Ab2d+spec-v2 觀察到較高通過數（36/80 與 40/80）；但對 Gemini 而言，簡潔的 Ab2d+api (78/80) 表現更佳。 Prompt 效果依模型而異。

### Q10: 為什麼 FAIL 有 242 個，可修復的 (Eligible) 卻只有 10 個？
**答**：因為 AI 生成程式的失敗大多是邏輯不通或程式結構大段缺失，真正屬於「語法僅差臨門一腳且有唯一確定修法」的案例本來就非常稀少。

### Q11: Abstain（不介入）是不是代表 Healer 的能力不足？
**答**：不是。知道「何時不該改」與知道「何時該改」同樣重要。過度修改會帶來高 Regression 風險。

### Q12: 這個研究真正的新發現是什麼？
**答**：我們劃定了 Deterministic AST Healer 的精確價值邊界：在特定表面瑕疵區域提供可解釋防禦，且在本次凍結範圍內觀察到 regression=0。

### Q13: 是否有挑選容易修復的案例來美化數據？
**答**：沒有。所有 Eligibility 規則均在實驗前凍結，且所有 Baseline FAIL 自動進行全量評估，無人工選擇。

### Q14: Healer 在修復過程中是否有偷看測試集答案？
**答**：絕對沒有。Healer 的 eligibility 判定、規則選擇與程式修改不讀取標準答案，也不以測試 PASS/FAIL 搜尋修法。修復後的獨立 revalidation 或 evaluator 僅用於安全檢查與結果評估，不反向決定修改內容。

### Q15: 你們如何確保 Healer 不會把原本寫對的程式改壞 (Regression)？
**答**：通過兩道防線：(1) Eligibility 審查僅允許特定失敗模式；(2) Revalidation 機制在修復後重新執行靜態檢核。實驗結果顯示在本次凍結樣本中觀察到 regression=0。

### Q16: 為什麼不新增更多修復規則來救援 9B 的 219 個失敗？
**答**：因為研究規範禁止根據測試結果動態追加規則（Rule Overfitting）。所有規則必須凍結，以維持實證的科學性。

### Q17: 4B 的 Primary (83) 與 Post-hoc (84) 差 1 格，是否代表流程不可靠？
**答**：不代表。該 1 格差異源於早期 revalidation 邏輯中一個過度保守的軟性約束誤判，經 False-loop audit 釐清並修復後，其餘 9 格 eligible 結果 100% 保持一致。

### Q18: Polynomial 題目的局部異常是否污染了整體的模型比較？
**答**：Polynomial 異常確實影響 9B 總分，但已被分層揭露，因此沒有被隱藏；整體比較必須連同此限制一起解讀。

---

## 17. 正式成果缺口盤點 (Gap Inventory - Audit Only)

本章節將未來分析缺口重新分類劃分如下（**本輪僅作盤點標記，不執行任何實驗修改或數據重新評估**）：

### 17.1 分類 A：研究證據必做 (`REQUIRED_BEFORE_FINAL`)
1. **Qwen 4B vs 9B Cell-level Paired Comparison**：於 Tier 1 正式配對比較中繪製 paired differences。
2. **主要 Condition Pairs 之 Exact McNemar 檢定**：針對 Ab1 vs Ab2g, Ab2g vs Ab2d+api, Ab2g vs Ab2d+spec-v2, Ab2d+api vs spec-v2 進行 exact McNemar 檢定。
3. **Discordant Pairs 與 Paired Risk Difference 計算**：列出成對勝敗矩陣 (Discordant Pairs) 並計算配對風險差與 p-value。
4. **Task-clustered Bootstrap 95% CI**：採用以 Task 為 Cluster 的 Bootstrap 抽樣，計算通過率與差異之 95% 信心區間。
5. **Seed 穩定性基本摘要**：彙整 5 個 Seed 間的通過數極差與標準差。
6. **完成上述報告措辭修正**：將所有未經統計檢定之「顯著」與因果過度主張替換為描述性用語（本報告已完成第一版修正）。

### 17.2 分類 B：最終呈現必做 (`REQUIRED_FOR_PRESENTATION`)
1. **正式展板向量圖表 (High-res Vector Charts)**：繪製展板專用之分頁柱狀圖與結構圖。
2. **評審版一頁精華摘要 (Executive One-Pager)**：提煉 1,000 字精簡一頁摘要。
3. **最終成果書完整敘事架構**：將本報告擴充為正式競賽報告書格式。
4. **評審 Q&A 定稿**：根據專家審查反饋完成 18 題 Q&A 終版文字。
5. **Primary / Post-hoc 圖像分帳**：於圖表中明確以不同圖例/顏色分隔 Primary 與 Post-hoc 數據。

### 17.3 分類 C：可選拓寬 (`OPTIONAL`)
1. **Logistic Mixed-effects 模型**：包含 Task/Seed 隨機效應之三向交互作用迴歸。
2. **Token / Wall-clock 分析**：整理 Prompt Token、Output Token 與 Healer CPU 毫秒級執行開銷。
3. **空集合 Healer Manifest**：為 Gemini 與 9B 產出標準格式之 `eligible=0` 執行空清冊 JSON。
4. **Polynomial Anomaly 獨立附錄**：將 9B Polynomial 異常診斷獨立匯出為 Audit 簡報。
5. **補充附錄與 SHA-256 Hash Closure 彙整**：建立全實驗產物之 Hash 密碼學關聯驗證清冊。

---

*本報告完全基於既有凍結證據組裝，未呼叫任何模型、未執行重新評分、未修改任何 Healer 規則與 Prompt。*
