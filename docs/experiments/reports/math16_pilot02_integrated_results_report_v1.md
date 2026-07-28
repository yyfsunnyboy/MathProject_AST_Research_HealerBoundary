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
**標的數據庫：** Math16 Pilot-02 (Gemini 3.5 Flash → Qwen 3.5 9B → Qwen 3.5 4B，共 960 個獨立實驗 cells；呈現序)
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
- [Baseline Correction Note v1](file:///c:/Projects/MathProject_AST_Research_HealerBoundary/docs/experiments/reports/math16_baseline_correction_note_v1.md)（Qwen 4B Baseline 78→79／320 分析/報告層更正，本報告 Qwen 4B 數字已依此更正）

---

## 1. 執行摘要 (Executive Summary)

本研究旨在回應 AI 數學解題程式生成的核心問題：**「當語言模型在生成 Python 數學運算程式發生失敗時，deterministic AST Healer（確定性語法與結構修補器）能在什麼界限內提供安全、可解釋且觀察到零倒退 (regression=0) 的修復價值？」**

我們設計並執行了 **Math16 Pilot-02** 實證實驗，採 16 題標準 K-12 數學運算題型（橫跨整數、多項式、根式、分數四大家族）、4 種 Prompt 引導條件（Ab1 裸考、Ab2g 通用鷹架、Ab2d+api 領域 API 暴露、Ab2d+spec-v2 完整家族規格），在 5 個獨立隨機種子下，對三個代表性模型（呈現序：**Gemini 3.5 Flash** → **Qwen 3.5 9B** → **Qwen 3.5 4B**）進行了共計 **960 個實驗 cells** 的完整測試與分帳。

### 主要研究發現：

1. **三模型基線表現呈現差異，部分家族具非單調波動**：
   - 三模型的端到端基線表現明顯不同；在同一 Qwen 系列與相同主要 sampling 設定下，9B 整體通過數 (101/320) 高於 4B (79/320，分析/報告層更正後) 22 格（基線通過率高出 6.88 個百分點）；
   - 然而，9B 在多項式家族（Polynomial）表現為 9/80，低於 4B 的 17/80（更正後），顯示特定提示結構下可能出現局部的非單調波動。
   - Gemini 3.5 Flash 的基線通過數為 **289/320 (90.31%)**。
   - > **更正註記**：Qwen 4B 上列數字為依 [Baseline Correction Note v1](math16_baseline_correction_note_v1.md) 更正後之分析/報告層數值（Baseline 78/320 → 79/320，+1 格，單一 cell 候選程式擷取錯誤，詳見該文件）。凍結管線歷史輸出 Baseline 78/320 永久保留不變。

2. **Healer 介入視窗 (Eligibility Window) 在本次三模型中呈非單調分布**：
   - **Gemini 3.5 Flash**：失敗數為 31 格。在目前 v4 taxonomy 分類口徑下，剩餘 31 格均被歸入 L5 algorithmic_error，且沒有案例命中現有凍結 Healer 規則，**適用介入窗口為 0 格 (eligible=0)**。
   - **Qwen 3.5 4B**：凍結管線歷史輸出失敗數為 242 格（Baseline 78/320 下）。Healer 成功識別出 **10 格 eligible 案例**，在觀察到零倒退 (regression=0) 前提下，於 Primary 預註冊流程救回 **5 格 (78 → 83，凍結歷史值)**，並於機制驗證 Post-hoc 流程救回 **6 格 (78 → 84，凍結歷史值)**。**分析/報告層更正後**（Baseline 79/320）：Primary 對應為 84/320（歷史中繼值，demoted），corrected-chain **Final 85/320**（rescue 仍為 6 格，該更正 cell 非 Eligible）。
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

正文展現順序採統一三模型呈現順序：**1. Gemini 3.5 Flash** $\rightarrow$ **2. Qwen 3.5 9B** $\rightarrow$ **3. Qwen 3.5 4B**（依 [Baseline Correction Note v1](math16_baseline_correction_note_v1.md) 第 10 節之呈現順序規則；僅欄位/列序調整，不改變任何數值、統計定義或研究結論）。

在統一的 v4 Evaluator 標準下，三模型在 320 cells 的端到端基線通過率如下（Qwen 4B 數字為分析/報告層更正後版本，見表下注記）：

| 模型名稱 | Baseline PASS | Baseline FAIL | Baseline 通過率 (%) | 正式證明檔案 |
| :--- | ---: | ---: | ---: | :--- |
| **Gemini 3.5 Flash** (Tier 2 參照) | **289** | 31 | **90.31%** (289/320) | [baseline_summary.json](file:///c:/Projects/MathProject_AST_Research_HealerBoundary/docs/experiments/results/math16_pilot02_full_evaluation_v4_r001/baseline_summary.json) |
| **Qwen 3.5 9B** (Tier 1 對照) | **101** | 219 | **31.56%** (101/320) | [overall_summary.json](file:///c:/Projects/MathProject_AST_Research_HealerBoundary/docs/experiments/results/math16_pilot02_qwen9b_evaluation_v4_r001/overall_summary.json) |
| **Qwen 3.5 4B** (Tier 1 對照，更正後) | **79** | 241 | **24.69%** (79/320) | [overall_summary.json](file:///c:/Projects/MathProject_AST_Research_HealerBoundary/docs/experiments/results/math16_pilot02_qwen4b_evaluation_v4_r001/overall_summary.json)（凍結證據仍記載 78/320，見更正說明） |

> **更正說明**：Qwen 3.5 4B Baseline 依 [Baseline Correction Note v1](math16_baseline_correction_note_v1.md) 由凍結管線歷史輸出 78/320 (24.38%) 更正為分析/報告層 79/320 (24.69%)，root cause 為單一 cell（`ce115_calc_polynomial_division_l1`／`ab1`／seed `2026072003`）之候選程式擷取錨定錯誤，經 audit 確認為 `healer_eligible: false`（非 Eligible，不影響 rescue 計數）。凍結證據檔（`overall_summary.json` 等）本身永久保留 78/320，不予修改。

**關鍵觀察與 Tier 1 配對統計**：
- 在同一 Qwen 系列與相同主要 sampling 設定下，9B 比 4B 多通過 22 格，基線通過率提高 6.88 個百分點 (79/320 vs 101/320，更正後)。
- Gemini 3.5 Flash 作為雲端強模型參照，通過率為 90.31% (289/320)。

### 5.1 Tier 1 (Qwen 4B vs Qwen 9B) 正式 320-Cell 配對列聯表與統計檢定

依據獨立腳本 `scripts/analyze_math16_pilot02_qwen4b_vs_qwen9b_tier1_paired.py` 從凍結數據庫進行 100% 完整匹配 (320 matched pairs)。**兩模型配對分析維持既有 Qwen 4B vs Qwen 9B 結構，不套用三模型重排規則**（依 Correction Note 第 10 節）。下表為分析/報告層更正後數值（Baseline 78→79 之單一 cell 更正，詳見 [Baseline Correction Note v1](math16_baseline_correction_note_v1.md) 與 [Amendment Decision Record v1](math16_baseline_79_amendment_decision_record_v1.md)）：

| 2×2 列聯表 | Qwen 3.5 9B PASS | Qwen 3.5 9B FAIL | 合計 (Qwen 4B) |
| :--- | ---: | ---: | ---: |
| **Qwen 3.5 4B PASS** | **52** (`BOTH_PASS`) | **27** (`FOUR_B_ONLY_PASS`, $b$) | **79** (24.69%) |
| **Qwen 3.5 4B FAIL** | **49** (`NINE_B_ONLY_PASS`, $c$) | **192** (`BOTH_FAIL`) | **241** (75.31%) |
| **合計 (Qwen 3.5 9B)** | **101** (31.56%) | **219** (68.44%) | **320** |

#### 正式統計指標與雙重信賴區間（更正後）：
- **不一致配對 (Discordant Pairs)**：$b = 27$ (`4B_ONLY`), $c = 49$ (`9B_ONLY`)，淨增加 $+22$ 格程式生成成功案例。
- **Paired Risk Difference ($\Delta$)**：$\Delta = +6.875\%$ ($+0.0688$)。
- **Exact Two-Sided McNemar Test $p$-value**：$p = \mathbf{0.015440}$ ($p < 0.05$，具統計顯著之配對差異，判定方向與門檻未改變）。
- **Matched-Pairs Odds Ratio (OR)**：$\text{OR} = 49 / 27 = \mathbf{1.81}$。
- **95% 雙重信賴區間**：
  - Wald 95% CI: `[+0.0159, +0.1216]` (+1.59% 至 +12.16%)
  - **Task-Clustered Bootstrap 95% CI** (10,000 resamples): `[-0.0156, +0.1437]` (-1.56% 至 +14.37%)
- **跨 Seed 穩定度**：所有 5 個隨機種子上 9B 均穩定高於 4B（更正僅涉及 seed `2026072003`，該 seed 淨增加由 $+9$ 調整為 $+8$；其餘 4 個 seed 不變）。
- **完整證明產物**：[Tier 1 Paired Analysis Dir](file:///c:/Projects/MathProject_AST_Research_HealerBoundary/docs/experiments/results/math16_pilot02_qwen4b_vs_qwen9b_tier1_paired_analysis_v1/overall_paired_summary.json)（**注意**：此凍結產物目錄之 JSON/MD 檔案本身尚未依更正重新產生，仍記載更正前 78/320 系列數值；本節數字為依 Amendment Decision Record v1 之獨立重算結果，屬分析/報告層，詳見該紀錄第 2–6 節）。
- **舊值（更正前，供比對）**：$b=26$, $c=49$，淨增加 $+23$，$\Delta=+7.1875\%$，McNemar $p=0.010582$，OR$=1.88$，Wald CI `[+0.0194,+0.1243]`，Bootstrap CI `[-0.0094,+0.1438]`。

---

## 6. Condition 比較 (Prompt Condition Breakdown)

三模型在四種 Prompt 條件下的細部通過率（各條件分母均為 80 cells；欄序依統一三模型呈現順序 Gemini→9B→4B，Qwen 4B 數字為分析/報告層更正後版本）：

| Prompt 條件 | Gemini 3.5 Flash | Qwen 3.5 9B | Qwen 3.5 4B |
| :--- | ---: | ---: | ---: |
| `Ab1` | 72/80 (90.0%) | 18/80 (22.5%) | 16/80 (20.0%) |
| `Ab2g` | 76/80 (95.0%) | 27/80 (33.8%) | 19/80 (23.8%) |
| `Ab2d+api` | **78/80 (97.5%)** | 16/80 (20.0%) | 8/80 (10.0%) |
| `Ab2d+spec-v2` | 63/80 (78.8%)* | **40/80 (50.0%)** | **36/80 (45.0%)** |

*\*註：Gemini 在 Ab2d+spec-v1 事前凍結規格下為 63/80；事後補齊 Fraction/Polynomial API 簽名卡之 Post-hoc 機制驗證可達 80/80，詳見第 11 節。Qwen 4B `Ab1` 由 15/80 (18.8%) 更正為 16/80 (20.0%)，反映本更正之單一 cell（`ce115_calc_polynomial_division_l1`／`ab1`／seed `2026072003`）；其餘三格條件不受影響，詳見 [Baseline Correction Note v1](math16_baseline_correction_note_v1.md)。*

### 重要觀察與分析：
1. **Gemini 在 Ab2d+api 觀察到較高通過率 (78/80)**：在簡單 API 暴露下表現良好，過於繁複的凍結 spec-v1 出現較多 API arity/name 不對齊 (63/80)。
2. **Qwen 9B 與 4B 在 Ab2d+spec-v2 獲得較高通過數**：9B 通過 40/80，4B 通過 36/80（更正後），顯示小模型對家族規格 (spec-v2) 具較高依賴度。
3. **Qwen 4B 在 Ab2d+api 通過數較低 (8/80)**：在僅暴露 API 卻無精確規格時出現較多無效 Python 生成。經診斷，在 Qwen 4B Ab2d+api 的 27 格診斷樣本中，21/27 格 (77.8%) 屬候選 Python 本體內部的 SyntaxError (如括號不平衡、字串未閉合或語法結構破損)，5/27 格 (18.5%) 屬 parser/抽取不友善 (PARSER_UNFRIENDLY)，1/27 格 (3.7%) 屬真邏輯錯誤 (TRUE_LOGIC_ERROR)。結果不偏向「Evaluator Parser 不公平是主要失敗來源」；但本診斷未建立 Prompt 結構對生成錯誤的因果責任，且該比例僅限定於此 27 格診斷樣本，不得外推至其他條件或模型。此 `Ab2d+api` 16/80（9B）數字不受本次 Baseline 更正影響。
4. **結論**：Prompt 條件效果依模型而異，無普遍最佳條件。

---

## 7. Family 比較 (Task Family Breakdown)

三模型在四個數學題目家族下的表現（各家族分母均為 80 cells；欄序依統一三模型呈現順序 Gemini→9B→4B，Qwen 4B Polynomial 為分析/報告層更正後版本）：

| 題目家族 (Family) | Gemini 3.5 Flash | Qwen 3.5 9B | Qwen 3.5 4B | 觀察差異 |
| :--- | ---: | ---: | ---: | :--- |
| **Integer (整數)** | **80/80 (100.0%)** | **42/80 (52.5%)** | 30/80 (37.5%) | 9B 比 4B 多通過 12 格 |
| **Polynomial (多項式)** | 74/80 (92.5%) | **9/80 (11.3%)** | 17/80 (21.3%，更正後) | **9B 通過數少於 4B 8 格** |
| **Radical (根式)** | 70/80 (87.5%) | 19/80 (23.8%) | 15/80 (18.8%) | 9B 比 4B 多通過 4 格 |
| **Fraction (分數)** | 65/80 (81.3%) | **31/80 (38.8%)** | 17/80 (21.3%) | 9B 比 4B 多通過 14 格 |

> **更正說明**：Qwen 4B Polynomial 由 16/80 (20.0%) 更正為 17/80 (21.25%)，對應 Baseline 78→79 更正之單一 cell（該 cell 屬 Polynomial 家族／`ab1` 條件）。Fraction 17/80、Radical 15/80、Integer 30/80（4B）及全部 9B 數字不受影響，詳見 [Baseline Correction Note v1](math16_baseline_correction_note_v1.md) 第 5.2 節。

### 重要解讀：
- Gemini 在 Integer 達到 80/80 (100%)。
- Qwen 9B 在 Integer (+12 格) 與 Fraction (+14 格) 觀察到高於 4B 的通過數。
- **Qwen 9B Polynomial 異常 (9/80)**：9B 在多項式通過數（更正後）少於 4B 8 格。經診斷，此現象具高度局部性，**不可解讀為 9B 全域失控或純數學能力較差**（詳見第 12 節）。

### 7.1 Fraction Family 9B 獨勝 (NINE_B_ONLY_PASS) 機制分布診斷

依據專屬診斷產物 [Fraction 9B-Only Pass Audit](file:///c:/Projects/MathProject_AST_Research_HealerBoundary/docs/experiments/results/math16_pilot02_fraction_9b_only_pass_mechanism_audit_v1/audit_report.md)：
- **配對不一致矩陣**：Fraction 家族 9B 獨勝 $c = 21$ 格 (`NINE_B_ONLY_PASS`)，4B 獨勝 $b = 7$ 格 (`FOUR_B_ONLY_PASS`)，淨增加 $c - b =$ **+14 格** (Paired RD = $+17.50\%$, Exact McNemar $p = 0.012541$).
- **4B Failure Layer 分布**：在 21 格 4B 失敗/9B 成功案例中，4B 失敗層級分別為 **L1 (Syntax/Parse)** 10 格 (47.62%)、**L5 (Algorithmic)** 6 格 (28.57%)、**L2 (Contract)** 2 格 (9.52%)、**L4 (Runtime)** 2 格 (9.52%)、**L3 (API Misuse)** 1 格 (4.76%)。格式與執行層級 (L1~L4) 合計占 **71.43%** (`FRACTION_GAP_MAINLY_FORMAT_EXECUTION_RELATED`).
- **Condition 分布**：差距分散於 `Ab2g` (7格, 33.33%)、`Ab2d+spec-v2` (7格, 33.33%)、`Ab1` (4格, 19.05%) 與 `Ab2d+api` (3格, 14.29%)，**非由 Ab2d+api 條件主導** (僅占 14.29%)。
- **Task 分布**：差距分散於 `ce113_q01` (9格)、`ce111_q05` (5格)、`ce112_q12` (4格)、`ce115` (3格)，無單一 Task 超過 50%。
- **與舊 Ab2d 診斷交集**：僅 2 格重疊於舊 Ab2d 27格異常集合，**嚴禁將舊 27格的 77.8% 格式污染外推至全 21 格**。

### 7.2 四大 Family 2×2 配對列聯表地面真值覆核與閉合

依據全量對帳產物 [Non-Fraction Family Tables Revalidation Audit](file:///c:/Projects/MathProject_AST_Research_HealerBoundary/docs/experiments/audits/math16_pilot02_nonfraction_family_table_revalidation_v1/audit_report.md)，四大 Family 原始 Baseline 獨立 Rebuild 重建結果如下（此表為 4B vs 9B 兩模型配對結構，維持原欄序，不套用三模型重排規則；Polynomial 與合計列為分析/報告層更正後數值，依 [Amendment Decision Record v1](math16_baseline_79_amendment_decision_record_v1.md) 第 3–4 節重算）：

| Family | 4B PASS | 9B PASS | BOTH PASS ($a$) | 4B ONLY ($b$) | 9B ONLY ($c$) | BOTH FAIL ($d$) | 淨增加 ($c-b$) | Paired RD ($\Delta$) | Exact McNemar $p$-value | Matched OR |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Integer** | 30/80 | 42/80 | **29** | **1** | **13** | **37** | **+12** | +0.1500 | **0.001831** | **13.00** |
| **Polynomial**（更正後） | 17/80 | 9/80 | **3** | **14** | **6** | **57** | **-8** | -0.1000 | **0.1153** | **0.43** |
| **Radical** | 15/80 | 19/80 | **10** | **5** | **9** | **56** | **+4** | +0.0500 | **0.423950** | **1.80** |
| **Fraction** | 17/80 | 31/80 | **10** | **7** | **21** | **42** | **+14** | +0.1750 | **0.012541** | **3.00** |
| **合計 (Closure，更正後)** | **79/320** | **101/320** | **52** | **27** | **49** | **192** | **+22** | **+0.0688** | **0.015440** | **1.81** |

**Family-to-Overall 閉合驗證（更正後）**：四大 Family 四格列聯表加總精確等於 Overall 2×2 列聯表 ($29+3+10+10=\mathbf{52}$, $1+14+5+7=\mathbf{27}$, $13+6+9+21=\mathbf{49}$, $37+57+56+42=\mathbf{192}$)，無任何不對齊或矛盾。

> **更正說明**：僅 Polynomial 列與合計列因 Baseline 78→79 之單一 cell 更正而變動（4B ONLY $b$ 13→14，BOTH FAIL $d$ 58→57，其餘三大 Family 列與 9B 側數字全部不變）。Polynomial Matched OR（0.43）與合計列（79/320, 27, 192, +22, +0.0688, p=0.015440, OR=1.81）為依相同方法論（OR = $c/b$）獨立重算，詳見 [Baseline Correction Note v1](math16_baseline_correction_note_v1.md) 與 [Amendment Decision Record v1](math16_baseline_79_amendment_decision_record_v1.md)。舊值（更正前）：Polynomial $b=13$, $d=58$，淨增加 $-7$，RD $-0.0875$，$p=0.167089$，OR$=0.46$；合計 78/320, $b=26$, $d=193$，淨增加 $+23$，RD $+0.0719$，$p=0.010582$，OR$=1.88$。

---

## 8. Failure Layer 與 Mechanism 分布 (Failure Analysis)

依據專案統一的 Failure Taxonomy v3，失敗劃分為 L0 至 L5 五大層級。**本節 Qwen 4B FAIL=242 分母與各 Layer 計數維持凍結管線歷史輸出（對應 Baseline 78/320），本輪更正未重新分層計算**（更正後 Qwen 4B FAIL 應為 241；更正之單一 cell 原屬 `catastrophic_truncation` 相關分類，該 cell 具體歸屬之 Layer 桶尚待專項核實後再更新本節，屬本次編修範圍外，詳見文末 BLOCK 事項）：

### 8.1 9B 與 4B 之 Failure Layer 分布比較

| Layer 層級 | 定義 | Gemini 3.5 Flash (FAIL=31) | Qwen 3.5 9B (FAIL=219) | Qwen 3.5 4B (FAIL=242，凍結歷史分母) |
| :--- | :--- | ---: | ---: | ---: |
| **L0** | Prompt / Policy / System Fault | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) |
| **L1** | Syntax / Parse Failure (無法解析) | 0 (0.0%) | 65 (29.7%) | 72 (29.8%) |
| **L2** | Contract / Entry Point Failure (入口缺失) | 0 (0.0%) | 10 (4.6%) | 18 (7.4%) |
| **L3** | Domain-API Misuse (API 誤用) | 0 (0.0%) | 2 (0.9%) | 6 (2.5%) |
| **L4** | Runtime Execution Exception (執行期崩潰) | 0 (0.0%) | 45 (20.5%) | 39 (16.1%) |
| **L5** | Semantic / Algorithmic Error (答案錯誤) | 31 (100.0%) | 97 (44.3%) | 107 (44.2%) |

### 8.2 主要失敗機制標籤 (Mechanism Tags Distribution)

- **Gemini 3.5 Flash** (31 FAILs)：
  - `algorithmic_error`: **31**
- **Qwen 3.5 9B** (219 FAILs)：
  - `algorithmic_error`: **97**
  - `format_contamination`: **62**
  - `control_flow_failure`: **33**
  - `undefined_name`: **12**
  - `ambiguous_entry_point`: **5**
- **Qwen 3.5 4B** (242 FAILs，凍結歷史分母)：
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

在凍結的 Primary Protocol 下，三模型之 Eligibility 與 Healer 修復成果如下（欄序依統一三模型呈現順序 Gemini→9B→4B；Qwen 4B 列為分析/報告層更正後版本，凍結管線歷史輸出見表下注記）：

| 模型名稱 | Baseline FAIL | Eligible 數 | Eligibility Coverage (%) | Rescue (救回數) | Regression | Primary Final | corrected-chain Final | 正式狀態標籤 |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :--- |
| **Gemini 3.5 Flash** | 31 | **0** | **0.00%** | 0 | 0 | **289/320** | 289/320 | N/A (No eligible window) |
| **Qwen 3.5 9B** | 219 | **0** | **0.00%** | not run | not run | **101/320** | 101/320 | N/A (No eligible window) |
| **Qwen 3.5 4B**（更正後） | 241 | **10** | **4.15%** (10/241) | **6** | **0** | **84/320**（歷史中繼值，demoted） | **85/320** | **Baseline 79; Primary 84 (demoted); corrected-chain Final 85** |

> **凍結管線歷史輸出（永久不變）**：Qwen 3.5 4B Baseline FAIL 242、Eligible 10、Coverage 4.13% (10/242)、Primary Rescue 5、Primary Final 83/320、corrected-chain Rescue 6、corrected-chain Final 84/320。分析/報告層依 [Baseline Correction Note v1](math16_baseline_correction_note_v1.md) 更正為上表數值：Baseline FAIL 241（79/320 之補數）、Eligible 仍為 10（更正 cell 非 Eligible）、Rescue 仍為 6、Primary 84/320（demoted，不再列為主表標題）、corrected-chain Final 85/320。

### 9B Eligibility 處置細項 (219 FAILs)：
- `eligible`: **0**
- `noneligible_no_rule_triggered`: **214**
- `abstain_ambiguous_entry_point`: **5**
- `pending_review`: **0**

### 重要解讀：
1. **Gemini 與 9B 的 `eligible=0` 代表無符合規則案例**：代表殘餘 FAIL 未命中現有凍結 Healer 規則。選擇不介入 (Abstain) 屬符合規範的行為。
2. **Qwen 4B 觀察到窄小的修復視窗**：在凍結歷史管線的 242 個 FAIL 中，識別出 10 個符合規則案例，在觀察到 regression=0 下，於 Primary 救回 5 格 (78 → 83，歷史值)，於 corrected-chain 救回 6 格 (78 → 84，歷史值)。分析/報告層更正後（241 個 FAIL，同一 10 格 eligible 案例）：Primary 對應 84/320（demoted），corrected-chain **Verified rescue 6 格 (79 → 85)**。
3. **覆蓋率與修復率別區分**：不得將 4B 在 eligible 內的修復率 ($6/10 = 60\%$，以 corrected-chain verified rescue 計) 與全體提升率 ($6/320 = 1.875\%$) 混淆；歷史 Primary 口徑之對應舊值為 $5/10 = 50\%$ 與 $5/320 = 1.56\%$。

---

## 11. Qwen 4B 與 Gemini 之 Primary / Post-hoc 分帳

本研究針對事後機制探討（Post-hoc）與事前預註冊（Primary）建立嚴格隔離：

### 11.1 Qwen 4B 分帳
- **Preregistered Primary (`math16_pilot02_qwen4b_healer_v4_r001`)**：
  - Baseline Pass: `78/320` $\rightarrow$ Post-Healer Pass: **`83/320`** (Rescued = **5**, Regression = **0**)
- **Corrected-chain Post-hoc (`..._posthoc_corrected_chain_r001`)**：
  - Baseline Pass: `78/320` $\rightarrow$ Post-Healer Pass: **`84/320`** (Rescued = **6**, Regression = **0**)
- **成因與原則**：差異來自 `False-loop Revalidation` 修正（Radical `__ab2d__seed_2026071301` 1 格保留修復）。`83/320` 為唯一預註冊 Primary 結果；`84/320` 屬 Post-hoc 機制驗證，**不可混充為 Primary**。
- **本節為凍結管線歷史分帳，維持不變**（Baseline 78/320 之框架下）。**分析/報告層另有獨立更正**（Baseline 78→79，root cause 為單一 cell 之候選程式擷取錯誤，與此處 False-loop Revalidation 成因無關）：更正後 Baseline 79/320，Primary 對應 84/320（歷史中繼值，demoted），corrected-chain **Final 85/320**（Rescued 仍為 6，Regression 仍為 0）。兩項更正各自獨立、互不取代，詳見 [Baseline Correction Note v1](math16_baseline_correction_note_v1.md)。

### 11.2 Gemini Post-hoc 治理
- **Primary Overall Score**: **289/320** (Ab2d+spec-v1 為 63/80)。
- **Post-hoc Spec Update**: 事後補齊 API 簽名卡後，該條件可達 80/80（Hybrid 盤點為 306/320）。
- **治理聲明**：`306/320` 僅作 Post-hoc 機制說明，**不是正式 Primary Overall Score**，不列入主要結果對照表，亦不與 Qwen 進行直接比較。

---

## 12. Qwen 9B Polynomial 局部異常診斷 (Polynomial Anomaly Diagnosis)

### 12.1 異常現象
Qwen 3.5 9B 在 Polynomial 家族的通過率為 **9/80 (11.3%)**，少於 Qwen 3.5 4B (17/80，分析/報告層更正後；凍結歷史輸出為 16/80，McNemar $p$ 由 0.167089 更正為 0.1153，詳見第 7.2 節與 [Baseline Correction Note v1](math16_baseline_correction_note_v1.md))。

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
| **Qwen 3.5 4B** | 1. `Ab2d+api` 通過數較低 (8/80)<br>2. 報告層 241 FAIL（歷史 242）中僅 10 格 eligible<br>3. 正式主表 79→85（rescue=6）；歷史 Primary／Post-hoc 差 1 格 | 1. 診斷樣本中 77.8% 屬候選 Python 本體 SyntaxError<br>2. 多數失敗非表面瑕疵，僅窄小窗口符合規則<br>3. 歷史差 1 格源於 false-loop；Baseline 更正另見 Correction Note | 1. 不能宣稱 4B 完全無法使用 API<br>2. 不能將 10 格 eligible 視為流程失敗<br>3. 不能以歷史 Post-hoc 冒充正式主表，亦不可忽略 demoted Primary |
| **Qwen 3.5 9B** | 1. 整體通過數高於 4B，Polynomial (9/80) 卻少於 4B<br>2. 219 FAIL 中 `eligible=0`<br>3. L1 達 65 格但無符合規則案例 | 1. `ce115_calc_polynomial_division_l1` 多 LaTeX 欄位與 Python 嵌套高度共現<br>2. 語法錯誤多為候選碼內部大段破損，未命中規則<br>3. L1 語法錯誤不等於具備安全修復依據 | 1. 不能外推為 9B 數學能力低於 4B<br>2. 不能把 `eligible=0` 寫成 Healer 系統故障<br>3. 不能為救援 9B 而強行放寬安全規則 |

---

## 14. 初步研究結論 (Preliminary Conclusions)

根據 Math16 Pilot-02 960 cells 的實證，提出以下 10 項結論：

1. **三模型的端到端通過率不同**。
2. **在同一 Qwen 系列中，9B 整體通過數高於 4B，但 Polynomial 未單調改善**。
3. **Prompt 條件效果依模型與 family 而異**。
4. **FAIL 數量不等於 eligibility coverage**。
5. **Eligibility coverage 在本次三模型中呈非單調分布**。
6. **Qwen 4B 出現窄小且可觀察的 repair window**（Verified rescue=6；正式主表 **79→85**；凍結歷史 Primary 5／Post-hoc 6 分帳另見 Correction Note）。
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

> **說明**：專屬口試備答產物請參閱 [Jury Defense Q&A Final v1](file:///c:/Projects/MathProject_AST_Research_HealerBoundary/docs/experiments/reports/math16_pilot02_jury_qa_final_v1.md)。

### Q1: 為什麼要先做 Eligibility 審查，不直接全部程式都嘗試修復？
**正式回答：** 若不設 Eligibility 門檻，修復器將被迫對無明確修復依據的程式進行猜測性修改，破壞可解釋性並可能引入倒退 (Regression)。Eligibility 是維護「確定性安全介入」的必要防禦。
**口試短答：** 因為缺乏明確規則強行盲目修復會破壞可解釋性並把程式改壞。Eligibility 能確保修復只在修法唯一且安全時介入。

### Q2: Gemini 與 9B 的 `eligible=0` 是否代表 Healer 沒有用？
**正式回答：** 不是。`eligible=0` 代表在本次 320 個單元與現有凍結規則下，失敗案例未同時滿足唯一、安全、可驗證的介入條件。Healer 在無適用規則時選擇 Abstain（不介入），屬符合規範的安全行為。
**口試短答：** 不是。`eligible=0` 代表現有規則未命中失敗案例，Healer 選擇 Abstain 主動放棄猜測，這展現了強烈的安全邊界防禦。

### Q3: 為什麼 4B 可以修復 5~6 格，9B 反而 0 格？
**正式回答：** 因為 4B 模型的失敗案例中恰好有 10 格命中事前凍結的特定語法與 JSON 瑕疵規則（如 `L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP` 等）；而 9B 雖然也有語法、執行與語義失敗，但沒有案例同時符合唯一且安全的現有修法條件。修復視窗取決於失敗型態是否落在凍結規則內。
**口試短答：** 4B 有 10 格命中凍結規則；9B 雖有語法與執行失敗，但沒有案例符合唯一且安全的現有修法。

### Q4: 9B Polynomial 只有 9/80，是否代表 9B 的數學能力比 4B 差？
**正式回答：** 不能這樣解讀。9B 總體通過數 (101/320) 高於 4B (79/320，分析/報告層更正後；凍結歷史輸出為 78/320)。Polynomial 的低下高度集中於 `ce115_calc_polynomial_division_l1` 單一題型，與多個 LaTeX 欄位組裝高度共現，屬特定提示結構敏感性，尚未證實因果，不可外推為 9B 全域失控或純數學能力落後。
**口試短答：** 不能。9B 總分高於 4B，Polynomial 偏低集中於單一多項式題型與 LaTeX 組裝衝突，屬於結構敏感性，未證明因果。

### Q5: 為什麼不修改 Evaluator 的 Parser 讓採分更寬鬆？
**正式回答：** Evaluator 的職責是維護嚴謹的評分契約。在 Qwen 4B Ab2d+api 27 格診斷樣本中，21/27 格 (77.8%) 屬候選 Python 本體內部的 SyntaxError (如括號不平衡或字串未閉合)，僅 5/27 格 (18.5%) 屬 parser 不友善，1/27 格 (3.7%) 屬真邏輯錯誤。結果不支持「Evaluator Parser 不公平是主要失敗來源」；隨意放寬 Parser 並無法修復破損的 Python 程式本體。
**口試短答：** 因為評分標準必須嚴謹，且診斷顯示 77.8% 的失敗是 Python 程式本體壞掉，放寬 Parser 並無法修復語法錯誤的程式。

### Q6: 為什麼不把所有 SyntaxError 都納入 Healer 修復範圍？
**正式回答：** 因為大多數 SyntaxError（如少寫半段邏輯、字串未閉合、語法結構混亂）並沒有唯一的修復解答。若強行修復將違反「修法唯一、不可反推答案」的核心原則，帶來極高修壞風險。
**口試短答：** 因為大多數語法錯誤沒有唯一的解答，強行盲猜修改會破壞可解釋性，違反 deterministic 修復的核心規範。

### Q7: 為什麼歷史 Primary／Post-hoc 要嚴格分帳，而正式主表改採 79→85？
**正式回答：** 凍結管線歷史分帳中，Primary（78→83）為事前預註冊 Protocol 結果，Post-hoc corrected-chain（78→84）為事後修正 false-loop revalidation 後的機制驗證，兩者不可混充。另依 [Baseline Correction Note v1](math16_baseline_correction_note_v1.md)，分析／報告層將 Baseline 更正為 79/320、Verified Final 為 **85/320**（rescue=6）；歷史 Primary 對應 84/320 已 demoted、不再作主表標題。科學規範要求同時保留：凍結歷史分帳、與報告層更正後 headline。
**口試短答：** 凍結歷史仍區分 Primary／Post-hoc；正式主表改報 **79→85（rescue=6）**，Primary 84 只留歷史註記。

### Q8: Gemini 基線已經 289/320 (90.3%)，為什麼還要研究 Healer？
**正式回答：** 本研究的核心目標是探索「修復邊界」。在本次 Gemini、題目與凍結規則下，剩餘失敗沒有形成安全的 Healer 介入視窗；而 Post-hoc 提示修復實驗 (306/320) 則揭示了強模型在 API 簽名補齊後的真實天花板。
**口試短答：** 本研究旨在劃定 Healer 的修復邊界。在本次 Gemini 測試與凍結規則下，剩餘失敗沒有形成安全的 Healer 介入視窗。

### Q9: Ab2d+spec-v2 是不是最好的 Prompt 條件？
**正式回答：** 對 4B 與 9B 而言，Ab2d+spec-v2 在本次正式四條件比較中通過數最高，分別為 36/80 與 40/80。Gemini 的正式生成只比較到 Ab2d+spec-v1，其中 Ab2d+api 為 78/80、spec-v1 為 63/80；Gemini 沒有正式重新生成 Ab2d+spec-v2。後續 80/80 僅是 Post-hoc API 文件補齊機制驗證，因此不能當作正式四條件比較結果。Prompt 效果依模型、提示版本與部署條件而異。
**口試短答：** 4B 和 9B 正式跑過 v2，規格較有幫助；Gemini 正式只跑到 v1，後來的 80/80 是事後機制驗證，不能當正式比較。

### Q10: 為什麼 FAIL 有約 241／242 個，可修復的 (Eligible) 卻只有 10 個？
**正式回答：** 凍結歷史 FAIL=242（Baseline 78/320）；分析／報告層更正後 FAIL=241（Baseline 79/320）。無論分母取哪一者，Eligible 仍為 10：因為 LLM 生成程式的失敗大多是演算法邏輯不通或結構大段缺失，真正屬於「程式本體正確、僅差語法臨門一腳且有唯一修法」的瑕疵案例本來就非常稀少。
**口試短答：** 報告層 FAIL≈241（歷史 242），Eligible 仍只有 10——多數 failure 不是可唯一修補的表面瑕疵。

### Q11: Abstain（不介入）是不是代表 Healer 的能力不足？
**正式回答：** 不是。知曉「何時不該介入」與「何時該介入」同等重要。Abstain 是控制 Regression 風險的防禦機制，代表系統在面臨不明確修復目標時主動放棄盲猜。
**口試短答：** 不是。知道何時不該猜是安全的表現，Abstain 能防止系統盲目修改而把原本可能的程式改壞。

### Q12: 這個研究真正的新發現是什麼？
**正式回答：** 我們劃定了 Deterministic AST Healer 的精確價值邊界：Healer 並非第二個解題模型，而在特定表面語法瑕疵區域提供可解釋防禦，且在本次命中凍結規則的修復案例中，觀察到 regression=0。
**口試短答：** 我們劃定了 Healer 的價值邊界：證明在本次命中凍結規則的修復案例中，觀察到 regression=0。

### Q13: 是否有挑選容易修復的案例來美化數據？
**正式回答：** 所有 320 格測試單元均依凍結流程納入全量評估，無人工選擇。Eligibility 審查規則均在實驗啟動前預先凍結，Baseline FAIL 自動進行審查。
**口試短答：** 所有 320 格單元均依凍結流程納入，沒有依結果人工挑選修復案例。

### Q14: Healer 在修復過程中是否有偷看測試集答案？
**正式回答：** Eligibility 審查與修法不依賴正確答案反推，也不以測試 PASS/FAIL 反覆試修。修復後的評估僅用於記錄結果與安全檢查，不反向決定修改內容。
**口試短答：** Eligibility 與修法不依賴正確答案反推，也不依 PASS/FAIL 反覆試修；修復後評估只用於記錄結果。

### Q15: 你們如何確保 Healer 不會把原本寫對的程式改壞 (Regression)？
**正式回答：** 通過兩道防線：(1) Eligibility 審查僅允許失敗模式明確且修法唯一的案例；(2) Revalidation 機制在修復後重新執行靜態檢核。在本次 320 個測試單元中，實際執行修復的案例均觀察到 Regression=0。
**口試短答：** 我們嚴格限制只修復有唯一答案的語法瑕疵，並在修改後再次自動檢核。本次實驗中觀察到 zero regression。

### Q16: 為什麼不新增更多修復規則來救援 9B 的 219 個失敗？
**正式回答：** 因為事前凍結可降低事後配合資料造成的 rule overfitting；新規則應在 development 證據建立，再用未參與建置的資料驗證，以維持實證研究的科學可重複性。
**口試短答：** 事前凍結可降低事後配合資料造成的 rule overfitting；新規則應在開發階段建立，再用獨立資料驗證。

### Q17: 4B 歷史 Primary／Post-hoc 只差 1 格，是否代表流程不可靠？
**正式回答：** 10 格 eligible 案例中，有 8 格在 Primary 與 corrected-chain replay 間完全不變；1 格 Radical 由 `no_op` 改為 `rescued`，使凍結歷史 Post-hoc 通過數由 83 增至 84；另 1 格 q09 由 `no_op` 改為 `repaired_still_fail`，但最終仍為 FAIL。因此共有 2 格處置狀態改變，只有 1 格改變最終 PASS/FAIL，且觀察到 regression=0。此歷史差 1 格與 Baseline 78→79 之抽取更正彼此獨立。正式主表另採分析／報告層 **79→85（Verified rescue=6）**；歷史 Primary 對應 84 已 demoted。
**口試短答：** 歷史 Primary／Post-hoc 差 1 格來自 false-loop 修正；正式主表是 **79→85（rescue=6）**，兩者要分開說。

### Q18: Overall McNemar 與 Task-clustered Bootstrap 結論看似不同，該如何解讀？
**正式回答：** 兩者代表不同層級的統計檢視。McNemar 顯示本次 320 個 matched cells 中 discordant 方向偏向 9B（分析／報告層 $p = 0.015440$；凍結產物 JSON 仍記載更正前 $p=0.010582$）；而 task-clustered bootstrap CI 跨 0（報告層 95% CI `[-1.56%, +14.37%]`），顯示外推到其他未知題目時仍具抽樣不確定性。
**口試短答：** McNemar（$p=0.015440$）偏向 9B；task-clustered bootstrap CI 跨 0，外推仍有不確定性。

### Q19: 為什麼 Fraction family 的 9B 優勢最明顯 (淨增加 14 格)？
**正式回答：** 在配對分析中，Fraction 家族 9B 獨勝 $c = 21$ 格，4B 獨勝 $b = 7$ 格，淨增加 14 格 (Exact two-sided McNemar $p = 0.012541$). 在 21 格 9B-only 中，4B 有 15 格 (71.43%) 落在 L1~L4，包括語法 (L1)、契約 (L2)、API (L3) 與執行 (L4) 問題；差距較多反映端到端生成穩定性，不可只解讀為純數學能力差異。
**口試短答：** 21 格 9B-only 中，4B 有 15 格落在 L1~L4，包括語法、契約、API 與執行問題；差距較多反映端到端生成穩定性，不可只解讀為數學能力差異。

---

## 17. 正式成果缺口盤點 (Gap Inventory - Audit Only)

本章節將未來分析缺口重新分類劃分如下（**本輪僅作盤點標記，不執行任何實驗修改或數據重新評估**）：

### 17.1 分類 A：研究證據必做 (`REQUIRED_BEFORE_FINAL`) — ✅ `COMPLETED_WITH_INTERPRETATION_LIMITATIONS`
1. **Qwen 4B vs 9B Cell-level Paired Comparison**：✅ **已完成**。[320-Cell Paired Ledger](file:///c:/Projects/MathProject_AST_Research_HealerBoundary/docs/experiments/results/math16_pilot02_qwen4b_vs_qwen9b_tier1_paired_analysis_v1/paired_cell_ledger.jsonl)
2. **主要 Condition Pairs 之 Exact McNemar 檢定**：✅ **已完成**。[Condition Paired Summary](file:///c:/Projects/MathProject_AST_Research_HealerBoundary/docs/experiments/results/math16_pilot02_qwen4b_vs_qwen9b_tier1_paired_analysis_v1/condition_paired_summary.json)（凍結 JSON 仍為更正前 Overall $p\approx0.0106$；**分析／報告層** Overall $p=0.015440$，見 Correction Note／Decision Record）.
3. **Discordant Pairs 與 Paired Risk Difference 計算**：✅ **已完成**（**報告層** $b=27, c=49, \Delta=+6.875\%$, OR=1.81；凍結產物仍記載更正前 $b=26$/OR=1.88）.
4. **Task-clustered Bootstrap 95% CI**：✅ **已完成**。[Bootstrap Summary](file:///c:/Projects/MathProject_AST_Research_HealerBoundary/docs/experiments/results/math16_pilot02_qwen4b_vs_qwen9b_tier1_paired_analysis_v1/bootstrap_summary.json)（凍結 JSON 仍為更正前 CI；**報告層** 10,000 resamples: Overall 95% CI `[-1.56%, +14.37%]`）.
5. **Seed 穩定性基本摘要**：✅ **已完成**。[Seed Stability Summary](file:///c:/Projects/MathProject_AST_Research_HealerBoundary/docs/experiments/results/math16_pilot02_qwen4b_vs_qwen9b_tier1_paired_analysis_v1/seed_stability_summary.json) (5 個 Seed 全數 $+1$ 至 $+7$ 格淨勝).
6. **完成報告措辭與方法學修正與 Fraction 機制分布補充**：✅ **已完成**。[Fraction 9B-Only Pass Audit](file:///c:/Projects/MathProject_AST_Research_HealerBoundary/docs/experiments/results/math16_pilot02_fraction_9b_only_pass_mechanism_audit_v1/audit_report.md) (21 格描述性分布解析已納入).

### 17.2 分類 B：最終呈現必做 (`REQUIRED_FOR_PRESENTATION`)
1. **核心圖表設計規格 v1 (Core Figure Specification v1)**：✅ **已完成**。[Core Figure Spec v1](file:///c:/Projects/MathProject_AST_Research_HealerBoundary/docs/experiments/visualization/math16_pilot02_core_figure_spec_v1/) (6 張核心圖表規格、數據表、治理規範、雙版本圖說、溯源與選圖排序定稿)。
2. **正式展板與簡報向量圖表實體檔繪製 (High-res PNG/SVG/Vector Chart Output)**：⏳ **未完成** (6 張核心圖表規格已凍結，圖檔實體繪製待後續處理)。
3. **評審版一頁精華摘要 (Executive One-Pager)**：⏳ **未完成** (4 張選圖與版面規格已定稿，內容擴充待處理)。
4. **最終成果書完整敘事架構**：⏳ **未完成** (將本報告擴充為正式競賽報告書格式)。
5. **評審 Q&A 定稿**：✅ **已完成**。[Jury Defense Q&A Final v1](file:///c:/Projects/MathProject_AST_Research_HealerBoundary/docs/experiments/reports/math16_pilot02_jury_qa_final_v1.md) (19 題雙版本定稿)。
6. **Primary / Post-hoc 圖像分帳規範**：✅ **已完成**。[Primary/Post-hoc Visual Governance](file:///c:/Projects/MathProject_AST_Research_HealerBoundary/docs/experiments/visualization/math16_pilot02_core_figure_spec_v1/primary_posthoc_visual_governance.md) (視覺分層與禁止過度宣稱規範已凍結)。

### 17.3 里程碑凍結狀態 (`MILESTONE_STATUS`)
* **Evidence Complete Milestone v1**：✅ **已凍結**。[Evidence Complete Milestone v1](file:///c:/Projects/MathProject_AST_Research_HealerBoundary/docs/experiments/milestones/math16_pilot02_evidence_complete_v1/) (正式數據、配對統計、Q&A、圖表規格、SHA 密碼學 Closure 與 10 項方法學限制全數鎖定；開開啟 presentation-only 製作階段)。

### 17.4 分類 C：可選拓寬 (`OPTIONAL`)
1. **Logistic Mixed-effects 模型**：包含 Task/Seed 隨機效應之三向交互作用迴歸。
2. **Token / Wall-clock 分析**：整理 Prompt Token、Output Token 與 Healer CPU 毫秒級執行開銷。
3. **空集合 Healer Manifest**：為 Gemini 與 9B 產出標準格式之 `eligible=0` 執行空清冊 JSON。
4. **Polynomial Anomaly 獨立附錄**：將 9B Polynomial 異常診斷獨立匯出為 Audit 簡報。
5. **補充附錄與 SHA-256 Hash Closure 彙整**：✅ **已包含於 Milestone v1**。[SHA256 Closure](file:///c:/Projects/MathProject_AST_Research_HealerBoundary/docs/experiments/milestones/math16_pilot02_evidence_complete_v1/source_sha_closure.json)。

---

*本報告完全基於既有凍結證據組裝，未呼叫任何模型、未執行重新評分、未修改任何 Healer 規則與 Prompt。*
