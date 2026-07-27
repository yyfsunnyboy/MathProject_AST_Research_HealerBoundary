# Math16 Pilot-02 正式整合研究報告 (Final Report v1.3)

```text
MATH16_PILOT02_FINAL_REPORT_V13_FINALIZED
DETERMINISTIC_AST_HEALER_BOUNDARY_RESEARCH_LINE
IVAN_MACRONIX_SCIENCE_FAIR_OFFICIAL_REPORT
```

> **研究聲明**：
> Deterministic AST Healer 不是第二個解題模型，而是只在修法唯一、局部、可驗證的窄小窗口介入；其餘情況主動 Abstain。

---

## 1. 摘要

本研究針對小參數在地化語言模型（Qwen 3.5 4B 與 9B）在 AI 生成數學解題程式的多層失敗，包含語法、契約、API、執行與語意層問題，實證劃定硬性工程干預機制（Deterministic AST Healer）的安全修復邊界。實驗 Protocol 採用 16 道 K12 數學題型（涵蓋 Integer 整數、Polynomial 多項式、Radical 根式與 Fraction 分數四大家族）、3 個模型（包含雲端強模型參照組 Gemini 3.5 Flash）、4 種 Prompt 引導條件（Ab1 Native 原生、Ab2g Generic 鷹架、Ab2d+api 領域 API 鷹架以及 Ab2d+spec 標準規範）與 5 個隨機種子，系統化構建全量 960 個測試單元（cells）之實證矩陣。整體評估流程嚴格分為 Baseline 評估、Active Healer 靜態 Eligibility 審查與 Tier 1 雙模型配對交叉分析。

實驗結果顯示：Gemini Primary 為 289/320 格 (90.31%)；Primary 的 `Ab2d+spec-v1` 為 63/80。後續 `Ab2d+spec-v2` 的 post-hoc inventory 為 80/80，與 Ab1 72/80、Ab2g 76/80、Ab2d+api 78/80 合計為四條件 post-hoc hybrid inventory 306/320，僅作機制／版本盤點，不作 Primary 正式比較。Qwen 9B 通過 101/320 格 (31.56%)，Qwen 4B Baseline 通過 78/320 格 (24.38%)。針對 Qwen 4B 的 242 格 Baseline 失敗案例，Active Healer 執行靜態 Eligibility 審查，其中 10 格符合修法唯一且可靜態驗證之安全介入條件；verified rescue 共 6 格，通過數由 78/320 提升至 84/320，且實證觀察到零倒退 (Observed Regression = 0)。其中 5 格於 Primary run 確認（83/320），另 1 格經 post-hoc corrected-chain 確認。Gemini 與 Qwen 9B 因殘餘失敗案例未命中事前凍結之修復規則，系統依凍結規則選擇 Abstain (Eligible = 0)，呈現本研究所定義的安全介入邊界。

在 4B 與 9B 之 320 格 Tier 1 配對分析中，雙過 52 格、4B 獨過 26 格、9B 獨過 49 格、雙敗 193 格，淨增加 23 格 (RD = +7.1875%)。單元層級 Exact McNemar 檢定顯示顯著差異 ($p = 0.010582$)；然考量 16 個 Task 聚類效應之 Task-clustered Bootstrap 95% 信賴區間跨 0 (`[-0.94%, +14.38%]`)，顯示將結論外推至未知全新數學題型時仍具抽樣不確定性。在家族分層中，Fraction 家族 9B 淨勝 14 格 ($p = 0.012541$)，機制拆解顯示 21 格 NINE_B_ONLY 中有 15 格屬 L1–L4（涵蓋語法、契約、API 與執行問題），另 6 格屬 L5 語意層，不可解讀為純數學推理能力差距。此外，Polynomial 家族中 9B 表現偏低集中於單一題型與特定 LaTeX 組裝衝突。

本研究結果支持以下定位：Deterministic AST Healer 的核心定位並非第二個解題模型，而是只在修法唯一、局部、可驗證的窄小窗口內提供確定性安全介入，面臨不明確修法時主動 Abstain 放棄盲猜，以維護整體系統之可解釋性與安全性。

---

## 2. 研究動機

隨著大型語言模型 (LLM) 在自動程式碼生成領域的廣泛應用，將小參數在地化模型 (4B/9B) 部署於邊緣算力設備已成為重要趨勢。然而，小模型在生成結構化程式碼時，常面臨多層失敗（涵蓋語法、契約、API、執行與語意層問題）導致可執行檔崩潰。若直接採用第二個 LLM 進行對話式修復，不僅顯著增加推論延遲與算力成本，更可能引入不可預測的邏輯改變與倒退 (Regression)。因此，開發具備確定性 (Deterministic) 保證、低延遲且可解釋的 AST 層級修復機制（AST Healer），並實證劃定其安全介入邊界，具備高度之科學與工程價值。

---

## 3. 研究問題

本研究聚焦於以下核心研究問題：
1. **修復視窗與能力劃分**：AI 生成程式失敗時，哪些錯誤型態可由 Deterministic AST Healer 安全修復？哪些錯誤必須主動 Abstain？
2. **小模型與工程干預之協同**：經工程干預 (Scaffold + Healer) 之 4B 小模型，能否在特定語法瑕疵視窗內達成確定性救援？
3. **規模與家族分層影響**：Qwen 4B 與 9B 在四個數學家族（Integer, Polynomial, Radical, Fraction）中的配對表現有何差異？
4. **安全防禦與零倒退**：Deterministic AST Healer 能否在救援失敗案例的同時，保持觀察到零倒退 (Observed Regression = 0)？

---

## 4. Deterministic AST Healer定位

Deterministic AST Healer **不是第二個解題模型**，它不參與數學推理，也不嘗試改寫程式碼的核心解題邏輯。其定位為基於抽象語法樹 (AST) 與確定性規則的靜態安全防線：
- **安全介入原則**：僅在「修法唯一、局部瑕疵、靜態可驗證」的窄小窗口內進行代換。
- **主動放棄 (Abstain)**：若失敗案例涉及語義錯誤、邏輯缺失或存在多種可能修法，Healer 拒絕盲目猜測，主動選擇 Abstain，將控制權交還系統。
- **零倒退防禦**：透過事前 Eligibility 審查與事後 Revalidation 兩道防線，降低將原本可運行的程式修改至失效狀態之風險。

---

## 5. 題目與模型

### 題庫設計
採用 16 道涵蓋 K12 數學領域之代表性題型，分為四大數學家族。正式題目識別碼採用 `docs/experiments/manifests/math16_three_model_five_seed_manifest.json` 之 `task_ids` 清單（非簡化別名）：
- **Integer (整數四則)**：`ce111_q03_prime_factor_selection`, `ce112_q01_negative_integer_power`, `ce112_q09_divisor_multiple_intersection`, `ce111_nonchoice_q01_part1_exponential_growth`
- **Polynomial (多項式)**：`ce115_calc_polynomial_division_l1`, `ce115_calc_polynomial_factor_roots_l1`, `ce111_q02_polynomial_division_remainder`, `ce111_q08_polynomial_factor_parameter_recovery`
- **Radical (根式運算)**：`ce115_calc_radical_simplification_l1`, `ce112_q04_radical_simplification`, `ce111_q10_ordered_quadratic_roots_radical`, `ce113_q11_rationalize_denominator`
- **Fraction (分數運算)**：`ce115_calc_exact_rational_expression_l1`, `ce111_q05_exact_fraction_expression`, `ce113_q01_negative_fraction_subtraction`, `ce112_q12_independent_probability_fraction`

### 測試模型
1. **Qwen 3.5 4B (Local)**：小參數在地化模型，測試 Primary Healer 救援能力。
2. **Qwen 3.5 9B (Local)**：中參數在地化模型，測試規模擴展對 Baseline 與修復邊界之影響。
3. **Gemini 3.5 Flash (Cloud)**：雲端強模型，作為 Tier 2 描述性基準參照 (Descriptive Reference Only)。

---

## 6. 四種Prompt條件

評估以下四種 Prompt 引導與規範條件：
1. **`Ab1` (Native)**：原生提示，不提供語義規範與 API 引導，測試模型原生隨機性。
2. **`Ab2g` (Generic Scaffold)**：一般性鷹架引導，鎖定變數命名與 LaTeX 結構。
3. **`Ab2d+api` (Domain Scaffold + API)**：領域專用鷹架，注入 `IntegerOps`, `FractionOps` 等封裝工具類別。
4. **`Ab2d+spec` (Domain Scaffold + Standard Spec)**：
   - Qwen 4B 與 9B 正式生成採用 `Ab2d+spec-v2`。
   - Gemini Primary 採用 `Ab2d+spec-v1`，通過數為 63/80。
   - 後續 `Ab2d+spec-v2` 補齊 API 簽名卡後的 post-hoc inventory 為 80/80；與其餘 Primary 條件合計為 post-hoc hybrid inventory 306/320，僅作機制／版本盤點，不作 Primary 正式比較。

---

## 7. 960-cell實驗矩陣

實驗矩陣規模如下：
- **矩陣維度**：16 題型 × 3 模型 × 4 條件 × 5 隨機種子 = 960 cells。
- **Tier 1 配對矩陣**：Qwen 4B (320 cells) vs Qwen 9B (320 cells) 進行一對一完全匹配配對分析。
- **Tier 2 參照矩陣**：Gemini 3.5 Flash (320 cells) 提供強模型天花板基準。

---

## 8. 評估方法與Eligibility

### 評估契約
每一個測試單元產生的程式碼均經由獨立 Evaluator 進行嚴格評分：
- **PASS**：程式可執行、無語法錯誤、輸出格式符合 specification、且數學結果 100% 正確。
- **FAIL**：包含語法錯誤 (SyntaxError)、契約違反 (Contract Error)、API 引用錯誤或數學計算錯誤。

### Eligibility 審查機制
對於所有 Baseline FAIL 案例，Healer 在決定是否介入前執行 Eligibility 靜態審查：
- **Eligible**：案例符合事前凍結之修復規則（如 `L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP` 語法瑕疵），且修法解答唯一。
- **Noneligible / Abstain**：不符合特定規則或存在歧義者，系統依凍結規則選擇 Abstain，呈現本研究所定義的安全介入邊界並保持原始 FAIL。

---

## 9. 三模型Baseline

在無 Healer 介入之 Baseline 條件下，三模型於 320 個測試單元中之通過表現如下：

![Figure 1 Baseline總覽](../visualization/math16_pilot02_core_figures_v1/figure_01_baseline_overall.png)

### Baseline 統計數據
- **Gemini 3.5 Flash**：通過 289 / 320 格，通過率 **90.31%** (FAIL = 31 格)。
- **Qwen 3.5 9B**：通過 101 / 320 格，通過率 **31.56%** (FAIL = 219 格)。
- **Qwen 3.5 4B**：通過 78 / 320 格，通過率 **24.38%** (FAIL = 242 格)。

---

## 10. Qwen 4B Primary Healer

針對 Qwen 4B 之 242 格 Baseline 失敗案例，Active Healer 執行 Primary 修復：

![Figure 5 Eligibility／Rescue](../visualization/math16_pilot02_core_figures_v1/figure_05_healer_eligibility_boundary.png)

### 修復數據彙整（主表）

| 項目 | 數值 |
|---|---|
| Baseline PASS | 78/320 格 |
| Healer verified rescue | 6 格 |
| Post-hoc Final | 84/320 格（相較 Baseline +6 格） |
| Observed Regression | 0 格 |

> 完整事實：規則實際觸發 7 格；其中 6 格為 verified rescue（5 格於 Primary run 確認、1 格因 runner 誤判假循環回退為 no_op，經 post-hoc corrected-chain 校正後確認），另 1 格為 repaired-still-fail（局部結構問題已修正，但因獨立後續錯誤仍未 PASS）。詳細 10 格 eligible 帳與修復效果分層見 10.2 節。

### 10.1 單一規則之實際作用範圍：L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP 七格

規則L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP實際涉及7格：6格為verified rescue，另1格transform已套用但仍FAIL。6格中5格屬Primary rescue；另1格屬Post-hoc technical correction rescue，因primary時runner誤判假循環回退為no_op，經Post-hoc corrected chain修正後才通過完整G1–G4。規則僅改寫oracle_payload欄位之值表達式，不改correct_answer，不重新求解；規則命中不等於rescue，須重新通過完整G1–G4才算verified rescue。

**6格verified rescue家族分布**（另附1格repaired-still-fail所屬家族）：

| 家族 | Verified rescue | 修復後仍FAIL |
|---|---|---|
| Radical | 4 | 1 |
| Fraction | 2 | 0 |
| Integer | 0 | 0 |
| Polynomial | 0 | 0 |

**最小 before/after 範例**（僅改寫`oracle_payload`欄位之值表達式，`correct_answer`與其餘程式邏輯逐字不變）：

```diff
-        "oracle_payload": radicand
+        "oracle_payload": {"radicand": 27}
```

上述7格中，6格verified rescue對應本節「Primary Rescue 5格、83/320」與「Post-hoc Total Rescue 6格、84/320」之全部來源；另1格repaired-still-fail不計入任何rescue統計，僅代表規則matcher/guard觸發、transform已套用，但healed後仍未通過完整G1–G4。

7格對照Healer介入前4B／9B Tier1結果：6格屬BOTH_FAIL（Primary 4、Post-hoc 1、修復後仍FAIL 1），1格屬NINE_B_ONLY_PASS（Primary 1），皆未落在BOTH_PASS或FOUR_B_ONLY_PASS。多數案例即使4B提升至9B仍未自然轉為PASS，非僅見於4B落後9B案例。唯一NINE_B_ONLY_PASS案例中，Healer使4B由FAIL轉PASS，與9B同為PASS。僅屬post-hoc交叉標註，不動原Tier1統計與McNemar結果。

| Baseline Tier 1象限 | Primary rescue | Post-hoc rescue | 修復後仍FAIL | 合計 |
|---|---:|---:|---:|---:|
| BOTH_FAIL | 4 | 1 | 1 | 6 |
| NINE_B_ONLY_PASS | 1 | 0 | 0 | 1 |
| 合計 | 5 | 1 | 1 | 7 |

Tier 1象限均依Healer介入前的4B與9B Baseline結果判定；Healer後結果僅作案例交叉標註。

---

### 10.2 完整 10 格 eligible 帳與修復效果分層

針對 Qwen 4B 242 格 Baseline FAIL，`decide_healer_eligibility()` 凍結規則審查後共 10 格符合事前凍結之安全介入條件。詳細母體與處置狀態來自 `docs/experiments/results/math16_pilot02_qwen4b_healer_v4_r001/eligible_execution_records.jsonl`（10 筆）與 `docs/experiments/results/math16_pilot02_qwen4b_healer_v4_posthoc_corrected_chain_r001/eligible_execution_records.jsonl`（corrected-chain 重放）。

#### 10.2.1 按規則的 eligible 分帳

| 規則 | 格數 |
|---|---|
| L1_CLOSE_UNBALANCED_PARENTHESIS | 1 |
| L1_PROSE_RESIDUE_NARROW | 1 |
| L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP | 7 |
| L2_CORRECT_ANSWER_JSON_DUMPS_UNWRAP | 1 |
| **合計** | **10** |

#### 10.2.2 Corrected-chain 處置分帳

| 處置 | 格數 | 說明 |
|---|---|---|
| verified rescue | 6 | 全部為 L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP，最終 PASS；其中 5 格屬 Primary、1 格屬 Post-hoc corrected-chain 技術修正 |
| repaired-still-fail | 4 | 規則確實觸發並套用 transform，但 healed 後仍 FAIL |

Primary 仍維持 5 格 rescue（83/320）；Post-hoc corrected-chain 為 6 格 rescue（84/320）。兩者嚴格分帳：83/320 為 Primary Protocol 正式認可數據，84/320 屬事後機制驗證。

#### 10.2.3 修復效果分層

| 分層 | 格數 | 規則 | 效果 |
|---|---|---|---|
| contract rescue | 6 | L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP | 修正契約 schema 介面（`oracle_payload` 包裝），最終通過完整 G1–G4 |
| execution rescue | 1 | L1_CLOSE_UNBALANCED_PARENTHESIS | 由 parse failure（`g1_parse` FAIL）前進到可執行／可診斷，但 healed 後仍於 schema 層 FAIL（`g3s_output_schema` FAIL） |
| 局部 transform、未達 PASS | 3 | L1_PROSE_RESIDUE_NARROW、L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP、L2_CORRECT_ANSWER_JSON_DUMPS_UNWRAP 各 1 格 | 有局部 transform，但未形成最終 PASS；依證據描述，不誇大 |

execution rescue 格為 `ce115_calc_exact_rational_expression_l1 / Ab1 / seed 2026072004`，baseline 為 `g1_parse` FAIL（SyntaxError `'(' was never closed`），healed 後進展為 `g3s_output_schema` FAIL。

#### 10.2.4 Triage leakage 稽核結論

依 `docs/experiments/reports/qwen4b_l2_payload_wrap_eligibility_answer_leakage_audit_v1.md` 逐行追蹤：

- 結論：**CLEAN_SCHEMA_ONLY**。
- `L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP` 的 eligibility 僅檢視 AST 結構、schema 欄位存在性、凍結參數一致性與 `correct_answer` 欄位存在性；**不讀取 `correct_answer` 的實際答案數值**。
- `classify_math16_response()` 中 schema 判定式於數值 oracle 比較前以 `return` 提早返回，因此 schema failure 在 `evaluate_math_task_oracle()` 執行前即被攔截。
- 現行 Healer 腳本在 FAIL/PASS 節流層仍讀取 `cell_level_baseline.jsonl` 的 `base["final_status"]` 作為 FAIL 節流；此欄位對 schema_failure 格本身亦由答案盲的 schema 判定產生，因此不構成 oracle／答案數值洩漏。
- 正確名稱為：**outcome-gated、answer-value-blind**；不得寫成完全 evaluator-blind。

---

## 11. Primary／Post-hoc分帳

為維護實證研究之嚴謹性，嚴格實施 Primary 與 Post-hoc 數據分帳：

| 模型與項目 | Primary / Baseline | Eligible | Primary Rescue / Final | Post-hoc hybrid inventory / Corrected Final | Observed Regression |
|---|---|---|---|---|---|
| **Qwen 4B** | 78/320 | 10 格 | **5 格 (83/320)** | 總救援 6 格 (84/320) | 0 格 |
| **Qwen 9B** | 101 / 320 | 0 格 | **0 格 (101/320)** | 0 格 (101/320) | 0 格 |
| **Gemini 3.5 Flash** | **Primary 289 / 320** | 0 格 | **0 格 (289/320)** | **Post-hoc hybrid inventory 306/320** | 0 格 |

- **分帳原則**：Qwen 4B 的 83/320 為事前預註冊 Protocol 唯一 Primary 正式認可數據；84/320 為 corrected-chain 總救援 6 格的事後技術分帳（相較 Primary 僅多 1 個 PASS）。Gemini 的 Primary 為 289/320（`Ab2d+spec-v1` 為 63/80）；`Ab2d+spec-v2` 的 80/80 與其餘三條件合計為 post-hoc hybrid inventory 306/320，僅作機制／版本盤點，不得誤稱為 Gemini Primary 或正式比較結果。

---

## 12. Qwen 4B與9B配對分析

在 320 個完全相同題目與條件配對單元中，對 Qwen 4B 與 9B 進行一對一 Tier 1 配對分析：

![Figure 4 Tier 1配對](../visualization/math16_pilot02_core_figures_v1/figure_04_tier1_paired_analysis.png)

### 2×2 配對矩陣
- **BOTH_PASS (兩者皆過)**：52 格
- **FOUR_B_ONLY (4B 獨過)**：26 格
- **NINE_B_ONLY (9B 獨過)**：49 格
- **BOTH_FAIL (兩者皆敗)**：193 格
- **總測試數**：320 格

### 配對統計量
- **Net Cell Gain (淨增加格數)**：+23 格 ($49 - 26$)
- **Paired Risk Difference (RD)**：+7.1875%
- **Exact McNemar Test**：$p = 0.010582$ (單元層級顯示顯著偏向 9B)
- **Task-clustered Bootstrap 95% CI**：`[-0.94%, +14.38%]` (考量 16 題型聚類效應後信賴區間跨 0)

---

## 13. Family分層

將 320 個配對單元按四大數學家族拆解（欄位順序固定為 `BOTH_PASS / FOUR_B_ONLY / NINE_B_ONLY / BOTH_FAIL`）：

![Figure 3 Family差異](../visualization/math16_pilot02_core_figures_v1/figure_03_family_breakdown.png)

### 四大家族配對表現表

| 數學家族 | BOTH_PASS | FOUR_B_ONLY | NINE_B_ONLY | BOTH_FAIL | 總格數 | Exact McNemar p | 備註 |
|---|---|---|---|---|---|---|---|
| **Integer** | 29 | 1 | 13 | 37 | 80 | $p = 0.001831$ | 9B 表現較佳 |
| **Polynomial** | 3 | 13 | 6 | 58 | 80 | $p = 0.167089$ | 4B 獨過較多 (異常分析見 14 節) |
| **Radical** | 10 | 5 | 9 | 56 | 80 | $p = 0.423950$ | 兩者無顯著差距 |
| **Fraction** | 10 | 7 | 21 | 42 | 80 | $p = 0.012541$ | 9B 淨勝 14 格 (拆解見 14 節) |

Fraction 的 NINE_B_ONLY = 21；其中 L1–L4 = 15（涵蓋語法、契約、API 與執行問題），L5 = 6，不可解讀為純數學能力差異。

---

## 14. 4B Ab2d+api與9B Polynomial異常

### 4B `Ab2d+api` 通過率低下診斷
4B 在 `Ab2d+api` 條件下通過數降至 8/80 格。事後診斷顯示：在已剖析之 27 格失敗診斷樣本中，77.8% (21/27) 屬 Python 本體 SyntaxError（括號未閉合或語法破碎），僅 18.5% (5/27) 屬 Parser 不友善。診斷結果不偏向以評分 Parser 偏差為主要失敗來源；此結論僅限定於已剖析之 27 格診斷樣本，未建立 Prompt 結構與生成錯誤之因果關係，亦不可外推為全域比例或完全排除 Parser 影響。

### 9B Polynomial 表現低下與 Fraction 拆解診斷
Qwen 9B 在 Polynomial 家族通過數偏低 (9/80 vs 4B 的 16/80)，集中於 `ce115_calc_polynomial_division_l1` 單一題型與特定 LaTeX 組裝衝突。此屬特定欄位提示結構敏感性，未建立因果關係，不可外推為 9B 全域能力失控。

在 Fraction 家族 21 格 NINE_B_ONLY 通過案例中，機制拆解顯示：有 15 格屬 L1–L4（涵蓋語法、契約、API 與執行問題），另 6 格屬 L5（語意與數學邏輯層）。差距較多反映端到端生成穩定性，不可解讀為純數學推理能力差異。

---

## 15. Gemini描述性參照

Prompt 條件對三模型通過數之影響如下：

![Figure 2 Prompt條件](../visualization/math16_pilot02_core_figures_v1/figure_02_prompt_conditions.png)

### Prompt 條件比較

| Condition | Gemini 3.5 Flash | Qwen 3.5 4B | Qwen 3.5 9B |
|---|---|---|---|
| **Ab1** | 72 / 80 | 15 / 80 | 18 / 80 |
| **Ab2g** | 76 / 80 | 19 / 80 | 27 / 80 |
| **Ab2d+api** | 78 / 80 | 8 / 80 | 16 / 80 |
| **Ab2d+spec-v2** | 80 / 80* | 36 / 80 | 40 / 80 |

> **Figure 2 圖說與分帳特別聲明**：
> - Gemini 的 `Ab2d+spec-v2` 為 post-hoc inventory；補齊 API 簽名卡後該條件達 80/80。
> - Gemini 正式 Primary 生成採用 `Ab2d+spec-v1`，通過數為 63/80（屬研究歷程）。
> - Qwen 4B 與 9B 採用 `Ab2d+spec-v2` 正式生成。
> - 三模型提示版本不同，不得假裝為完全同條件之 Primary 直接推論。

---

## 16. Healer安全介入邊界

Deterministic AST Healer 之安全介入架構概念如下：

![Figure 6 安全介入概念圖](../visualization/math16_pilot02_core_figures_v1/figure_06_healer_concept_zones.png)

### 安全介入邊界三原則
1. **可修復區 (Repair Window)**：僅對語法解答唯一、局部且可驗證之瑕疵（如特定 JSON key 包含瑕疵）進行確定性修正。
2. **防禦性放棄 (Abstain Zone)**：對於邏輯錯誤、語義缺失或具備多種修正可能之案例，Healer 拒絕盲猜，主動選擇 Abstain。
3. **零倒退防線 (Zero Regression)**：透過事前 Eligibility 與事後 Revalidation 兩道防線，降低修改破壞原本正確程式之風險。

---

## 17. 五項主要發現

本研究歸納出以下五項核心實證發現：

1. **Baseline能力與Healer可修復窗口不同**：模型 Baseline 生成通過率高，不代表剩餘失敗中包含更多可修復瑕疵；修復視窗取決於失敗案例是否符合凍結之修復規則。
2. **4B存在窄小且可驗證的repair window**：Qwen 4B 經 Active Healer verified rescue 6 格，通過數由 78/320 提升至 84/320，結果顯示小模型配接硬性干預具有救援價值。分帳上，5 格於 Primary run 確認（83/320），另 1 格經 corrected-chain 確認；另有 1 格 repaired-still-fail 不計入 rescue。
3. **9B整體通過較高，但Family結果非單調**：9B 在 Overall 通過率高於 4B，但在 Polynomial 家族因單一題型提示敏感性出現非單調狀況。
4. **Prompt效果依模型、版本與部署條件而異**：同一 Prompt 條件（如 `Ab2d+api`）在 4B 與 Gemini 上呈現截然不同之效用。
5. **Abstain是Deterministic Healer的重要安全能力**：知曉何時不該猜與何時該修同等重要，主動 Abstain 是控制 Regression 風險的核心防禦。

---

## 18. 方法學限制

本研究嚴格受限於以下 10 項凍結方法學限制：

1. **Overall 統計顯著性與外推不確定性 (Cell-level vs Task-level)**：細胞層級 Exact McNemar 檢定顯示 9B-only (49格) 顯著多於 4B-only (26格) ($p = 0.010582$)；然考慮 16 個 Task 聚類效應之 Task-clustered Bootstrap 95% CI 跨 0 (`[-0.94%, +14.38%]`)，顯示外推至未知全新題型時仍具抽樣不確定性。不得宣稱「9B 保證優於 4B」。
2. **四大數學家族分層屬探索性分析 (Exploratory Subgroup Analysis)**：四大家族分層未事前預註冊族群 alpha 矯正，屬 Post-hoc 探索性分析，其 $p$-values 僅供假說生成參考。
3. **Fraction 家族差距不可解讀為純數學能力差異 (Fraction Gap Interpretation)**：9B 在 Fraction 淨勝 14 格 ($p = 0.012541$)，機制拆解顯示 21 格 NINE_B_ONLY 中有 15 格屬 L1–L4（涵蓋語法、契約、API 與執行問題），另 6 格屬 L5 語意層，不可解讀為純數學推理能力差距。
4. **Polynomial 9B 偏低為局部格式共現 (Polynomial Anomaly Localized Co-occurrence)**：9B 在 Polynomial 表現偏低集中於 `ce115_calc_polynomial_division_l1` 多項式除法單一題型與特定 LaTeX 組裝衝突，未建立因果關係，不可外推為 9B 全域能力失控。
5. **Qwen 4B `Ab2d+api` 77.8% 語法錯誤侷限於診斷樣本 (4B Ab2d Anomaly Sample Bound)**：4B 在 `Ab2d+api` 下 77.8% (21/27) SyntaxError 結論僅適用於已剖析之 27 格診斷樣本，不可外推為全域失敗比例。
6. **Gemini 作為 Tier 2 描述性參照 (Gemini as Tier 2 Reference Only)**：Gemini 3.5 Flash (289/320, 90.31%) 僅作強模型描述性基準參照，不可宣稱「證明大模型規模因果壓倒性勝出」。
7. **Prompt 提示版本異質性 (Prompt Version Discrepancy)**：Gemini Primary 採用 `Ab2d+spec-v1` (63/80)；後續 `Ab2d+spec-v2` 補齊 API 簽名卡後為 80/80 的 post-hoc inventory，與其餘三條件形成 306/320 post-hoc hybrid inventory，僅作機制／版本盤點。Qwen 4B/9B 正式生成採用 `Ab2d+spec-v2`，通過數為 36/80 與 40/80。
8. **`Regression = 0` 僅屬實證觀察 (Observed Zero Regression Only)**：`Observed Regression = 0` 僅代表本次 320 個單元及凍結規則下「觀察到零倒退」，不可宣稱「保證在任意情境下 100% 絕不倒退」。
9. **`Eligible = 0` 不代表模型無失敗 (Eligibility Zero Scope)**：Gemini (31 FAIL) 與 9B (219 FAIL) 之 `Eligible = 0` 代表殘餘失敗未命中事前凍結規則，系統主動 Abstain，不代表生成無錯誤。
10. **全域邊界與範疇受限 (Global Protocol Bound)**：本研究所有數字與結論，僅嚴格適用於本次測試之 16 道數學題型、3 個模型、4 種 Prompt 條件、5 個隨機種子與凍結規則。

---

## 19. 評審追問摘要

選錄 8 項關鍵評審追問與標準答覆摘要：

### Q1: 為什麼要先做 Eligibility 審查，不直接全部程式都嘗試修復？
**答覆**：若不設 Eligibility 門檻，修復器將被迫對無明確修復依據的程式進行猜測性修改，破壞可解釋性並可能引入倒退 (Regression)。Eligibility 是維護「確定性安全介入」的必要防禦。

### Q2: Gemini 與 9B 的 `eligible=0` 是否代表 Healer 沒有用？
**答覆**：不是。`eligible=0` 代表在本次 320 個單元與現有凍結規則下，失敗案例未同時滿足唯一、安全、可驗證的介入條件。Healer 在無適用規則時選擇 Abstain（不介入），屬符合規範的安全行為。

### Q3: 為什麼 4B 可以修復 5~6 格，9B 反而 0 格？
**答覆**：因為 4B 模型的失敗案例中恰好有 10 格命中事前凍結的特定語法瑕疵規則；而 9B 雖然也有失敗，但沒有案例同時符合唯一且安全的現有修法條件。修復視窗取決於失敗型態是否落在凍結規則內。

### Q4: 為什麼不把所有 SyntaxError 都納入 Healer 修復範圍？
**答覆**：因為大多數 SyntaxError（如少寫半段邏輯、字串未閉合）並沒有唯一的修復解答。若強行修復將違反「修法唯一、不可反推答案」的核心原則，帶來極高修壞風險。

### Q5: 4B 的 Primary (83/320) 與 Post-hoc (84/320) 只差 1 格，其重放處置細節為何？
**答覆**：Qwen 4B Baseline = 78/320；Primary rescue = 5，final = 83/320；Post-hoc total rescue = 6，final = 84/320，相較 Primary 僅增加 1 個 PASS。在 10 個 Eligible 案例重放中，8 個處置狀態完全不變；2 個處置狀態改變（1 格由 `no_op` 改為 `rescued` 使 PASS 增加 1 格，1 格由 `no_op` 改為 `repaired_still_fail` 仍為 FAIL）。因此只有 1 格改變最終 PASS/FAIL 結果。

### Q6: Abstain（不介入）是不是代表 Healer 的能力不足？
**答覆**：不是。知曉「何時不該介入」與「何時該介入」同等重要。Abstain 是控制 Regression 風險的防禦機制，代表系統在面臨不明確修復目標時主動放棄盲猜。

### Q7: Overall McNemar 與 Task-clustered Bootstrap 結論看似不同，該如何解讀？
**答覆**：兩者代表不同層級的統計檢視。McNemar 顯示本次 320 個 matched cells 中 discordant 方向偏向 9B ($p = 0.010582$)；而 task-clustered bootstrap CI 跨 0 (95% CI `[-0.94%, +14.38%]`)，顯示外推到其他未知題目時仍具抽樣不確定性。

### Q8: 為什麼 Fraction family 的 9B 優勢最明顯 (淨增加 14 格)？
**答覆**：在 21 格 9B-only PASS 中，拆解顯示 15 格 (71.43%) 屬 L1~L4（涵蓋語法、契約、API 與執行問題），另 6 格屬 L5 語意層。差距較多反映端到端生成穩定性，不可解讀為純數學推理能力差異。

---

## 20. 結論、後續工作與正式證據索引

### 結論
本研究結果支持以下定位：Deterministic AST Healer 具備精確價值與安全介入邊界。實證顯示：
1. AST Healer 不扮演第二個解題模型，而在可驗證之特定語法瑕疵窗口發揮確定性救援功能（4B verified rescue 共 6 格，通過數由 78/320 提升至 84/320）。技術分帳上，Primary 救援 5 格、final 83/320；另 1 格由 corrected-chain 確認，且另有 1 格 repaired-still-fail 不計入 rescue。
2. 在命中凍結規則之修復案例中，實證觀察到 `Regression = 0`。
3. 面臨無確定修法之失敗時，系統依凍結規則選擇 Abstain，降低盲目修改帶來之風險並維持整體架構之可解釋性。

### 後續工作
1. 擴充預註冊修復規則庫，針對 9B 語法瑕疵開發獨立驗證集。
2. 引入多 Task 跨領域擴展測試，縮減 Task-clustered Bootstrap 信賴區間不確定性。

### 正式證據與產物索引
- **Evidence Complete Milestone v1**：`docs/experiments/milestones/math16_pilot02_evidence_complete_v1/`
- **Integrated Results Report v1**：`docs/experiments/reports/math16_pilot02_integrated_results_report_v1.md`
- **正式 Jury Q&A Defense Manual v1（20260724 唯一正式交付入口）**：`docs/決賽文件/實驗結果文件/20260724_Math16/04_math16_pilot02_jury_qa_final_v1.md`
- **Six Core Figures v1**：`docs/experiments/visualization/math16_pilot02_core_figures_v1/`
- **One-Pager v2.3 (Pairwise Collision-Free)**：`docs/experiments/presentation/math16_pilot02_one_pager_v23/`
- **Final Report v1 (Base Version)**：`docs/experiments/reports/math16_pilot02_final_report_v1.md`
- **Seven-Cell Tier 1 Crosswalk v1**：`docs/experiments/reports/math16_healer_seven_cell_tier1_crosswalk_v1.md`
- **Post-hoc Six-Cell L2 Payload-Wrap Deep Audit v1**：`docs/experiments/reports/math16_posthoc_six_cell_l2_payload_wrap_deep_audit_v1.md`
- **L2 Payload-Wrap Eligibility Answer Leakage Audit v1**：`docs/experiments/reports/qwen4b_l2_payload_wrap_eligibility_answer_leakage_audit_v1.md`
