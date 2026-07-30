# Math16 Pilot-02 正式整合研究報告 (Final Report v1.3)

```text
MATH16_PILOT02_FINAL_REPORT_V13_FINALIZED
DETERMINISTIC_AST_HEALER_BOUNDARY_RESEARCH_LINE
IVAN_MACRONIX_SCIENCE_FAIR_OFFICIAL_REPORT
```

> **⚠ 更正說明 (Correction Notice, 2026-07-28)**：Method 1／Method 2 交叉稽核發現單一 cell（`ce115_calc_polynomial_division_l1 / ab1 / seed 2026072003`）之候選程式擷取錨定錯誤（非模型能力差異），已依分析／報告層更正本文所有主要敘述與數據表：Qwen 4B Baseline **78/320 → 79/320 (24.69%)**；Final（corrected-chain verified rescue）**84/320 → 85/320**（Verified rescue 維持 6 格不變）；Primary 中繼值（原 83/320）依更正基準連動為 84/320，已下修為附註、不再列為主表標題數字。三模型呈現順序統一調整為 Gemini 3.5 Flash → Qwen 3.5 9B → Qwen 3.5 4B（僅為展示順序調整，不影響任何數值或研究結論）。**凍結證據（raw evaluation results、Healer/Eligibility journals、manifests、pinned Evaluator/Protocol scripts、regression tests）永久保留原始 78/83/84 數值，不受本更正影響、不被修改**。本輪僅更正文字敘述與數據表，Figure 1、3、4、5 已完成更正後重繪，現行正式圖檔位於 `figures/`。完整稽核鏈見：[Math16 Baseline Correction Note v1](05_math16_baseline_correction_note_v1.md)。
>
> **⚠ Aggressive Round 1 overlay (Correction Notice, 2026-07-30)**：單一 cell `ce112_q04_radical_simplification / ab2d / seed 2026072003` 發生 **source–label promotion mismatch**（密封 source 為 `FAILED／parse_minor`，C5a 卻記 `PASS／PRIOR_PASS_PRESERVED`）。分析層 overlay：**Baseline 79／241 不變**；Aggressive Round 1 Final **88→87**、verified rescue **9→8**、修復率 **9／241=3.73% → 8／241=3.32%**。真 rescue＝Tier A **6**＋D1 active-shadow **2**；C2 +1 為幽靈帳（開發 replay 曾修成功，但修復 bytes 未晉升 sealed final）。**凍結 labels／manifest／journals／sealed sources 永久保留 88／9**。Conservative **79→85／rescue 6 不受影響**。Fixpoint v1 之 232／232 zero-change **僅對 frozen 88／232 人口鎖成立**，不得宣稱涵蓋 corrected residual FAIL＝233。三模型 Final PASS sealed-source 重評 **478／479** 一致（4B 87／88、9B 102／102、Gemini 289／289）；唯一 mismatch＝本格，**非**系統性問題。完整說明：[Correction Note](10_math16_aggressive_round1_source_label_promotion_mismatch_correction_note_v1.md)；overlay JSON：`docs/experiments/manifests/math16_aggressive_round1_corrected_overlay_v1.json`。
>
> **研究聲明**：
> Deterministic AST Healer 不是第二個解題模型，而是只在修法唯一、局部、可驗證的窄小窗口介入；其餘情況主動 Abstain。

---

## 1. 摘要

本研究針對小參數在地化語言模型（Qwen 3.5 4B 與 9B）在 AI 生成數學解題程式的多層失敗，包含語法、契約、API、執行與語意層問題，實證劃定硬性工程干預機制（Deterministic AST Healer）的安全修復邊界。實驗 Protocol 採用 16 道 K12 數學題型（涵蓋 Integer 整數、Polynomial 多項式、Radical 根式與 Fraction 分數四大家族）、3 個模型（包含雲端強模型參照組 Gemini 3.5 Flash）、4 種 Prompt 引導條件（Ab1 Native 原生、Ab2g Generic 鷹架、Ab2d+api 領域 API 鷹架以及 Ab2d+spec 標準規範）與 5 個隨機種子，系統化構建全量 960 個測試單元（cells）之實證矩陣。整體評估流程嚴格分為 Baseline 評估、Active Healer 靜態 Eligibility 審查與 Tier 1 雙模型配對交叉分析。

實驗結果顯示：Gemini Primary 為 289/320 格 (90.31%)；Primary 的 `Ab2d+spec-v1` 為 63/80。後續 `Ab2d+spec-v2` 的 post-hoc inventory 為 80/80，與 Ab1 72/80、Ab2g 76/80、Ab2d+api 78/80 合計為四條件 post-hoc hybrid inventory 306/320，僅作機制／版本盤點，不作 Primary 正式比較。Qwen 9B 通過 101/320 格 (31.56%)，Qwen 4B Baseline 通過 **79/320 格 (24.69%)**（原 78/320 (24.38%)，因單一 cell 抽取錨定瑕疵於分析／報告層更正，詳見更正說明）。針對 Qwen 4B 的 **241** 格 Baseline 失敗案例，Active Healer 執行靜態 Eligibility 審查，其中 10 格符合修法唯一且可靜態驗證之安全介入條件；verified rescue 共 6 格，通過數由 79/320 提升至最終 **85/320**。原 Primary 中繼值（5 格於 Primary run 確認）依更正後基準連動為 84/320，依採行原則自主表標題數據中下修為附註，僅作技術分帳參考；另 1 格經 post-hoc corrected-chain 確認方達最終 85/320。Method 1 未對 Baseline PASS cells 執行 Healer，因此 Regression not measured；Method 2 對全部 320 格完成 Raw／Final 雙路評分，Regression measured = 0/320。Gemini 與 Qwen 9B 因殘餘失敗案例未命中事前凍結之修復規則，系統依凍結規則選擇 Abstain (Eligible = 0)，呈現本研究所定義的安全介入邊界。

在 4B 與 9B 之 320 格 Tier 1 配對分析中，雙過 52 格、4B 獨過 **27** 格、9B 獨過 49 格、雙敗 **192** 格，淨增加 **22** 格 (RD = **+6.875%**)。單元層級 Exact McNemar 檢定顯示顯著差異 ($p = **0.015440**$；Wald 95% CI `[1.59%, 12.16%]`；配對勝算比 OR = **1.81**)；然考量 16 個 Task 聚類效應之 Task-clustered Bootstrap 95% 信賴區間跨 0 (`[-1.56%, +14.37%]`)，顯示將結論外推至未知全新數學題型時仍具抽樣不確定性（以上皆已依更正說明由原 26/193/+23/+7.1875%/0.010582/`[-0.94%, +14.38%]` 更新，顯著性方向與結論未變）。在家族分層中，Fraction 家族 9B 淨勝 14 格 ($p = 0.012541$)，機制拆解顯示 21 格 NINE_B_ONLY 中有 15 格屬 L1–L4（涵蓋語法、契約、API 與執行問題），另 6 格屬 L5 語意層，不可解讀為純數學推理能力差距。此外，Polynomial 家族中 9B 表現偏低（9/80）集中於單一題型與特定 LaTeX 組裝衝突，4B 於該家族為 **17/80**（原 16/80）。

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
4. **安全防禦與倒退量測**：Method 1 未量測 Regression；Method 2 對全部 320 格 Raw／Final 雙路評分後，實際量測之 Regression 是否為 0/320？

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
1. **Gemini 3.5 Flash (Cloud)**：雲端強模型，作為 Tier 2 描述性基準參照 (Descriptive Reference Only)。
2. **Qwen 3.5 9B (Local)**：中參數在地化模型，測試規模擴展對 Baseline 與修復邊界之影響。
3. **Qwen 3.5 4B (Local)**：小參數在地化模型，測試 Primary Healer 救援能力。

> 三模型呈現順序統一採 Gemini 3.5 Flash → Qwen 3.5 9B → Qwen 3.5 4B（僅為展示一致性慣例，不代表效能排名，數值與統計定義不變；4B vs 9B 兩模型配對分析維持原有結構）。

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

Ab2d 工具契約與模型遵守性另經補充稽核；結果不改變既有分數與 Healer 統計，但限制條件層級的機制解釋，詳見附錄。

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

![Figure 1 Baseline總覽](figures/figure_01_baseline_overall.png)

### Baseline 統計數據
- **Gemini 3.5 Flash**：通過 289 / 320 格，通過率 **90.31%** (FAIL = 31 格)。
- **Qwen 3.5 9B**：通過 101 / 320 格，通過率 **31.56%** (FAIL = 219 格)。
- **Qwen 3.5 4B**：通過 **79 / 320** 格，通過率 **24.69%** (FAIL = **241** 格)。（原 78/320 (24.38%)，經分析／報告層基準更正，詳見 [更正說明](05_math16_baseline_correction_note_v1.md)；凍結原始評測證據仍永久保留 78/320）

---

## 10. Qwen 4B Primary Healer

針對 Qwen 4B 之 **241** 格 Baseline 失敗案例，Active Healer 執行 Primary 修復：

![Figure 5 Eligibility／Rescue](figures/figure_05_healer_eligibility_boundary.png)

### 修復數據彙整（主表）

| 項目 | 數值 |
|---|---|
| Baseline PASS | **79/320** 格 |
| Healer verified rescue | 6 格 |
| Post-hoc Final | **85/320** 格（相較 Baseline +6 格） |
| Method 1 Regression | Not measured |

> **基準更正說明**：Baseline 已由 78/320 更正為 **79/320**（單一 cell 抽取錨定瑕疵，非模型能力差異，詳見 [更正說明](05_math16_baseline_correction_note_v1.md)）；Post-hoc Final 相應由 84/320 更正為 **85/320**。原 Primary 中繼值（5 格於 Primary run 確認）依更正基準連動為 84/320，依採行原則不再作為主表標題數字，僅作 10.2 節技術分帳參考。
>
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

上述7格中，6格verified rescue對應本節「Primary Rescue 5格、對應更正後基準84/320（原83/320，中繼值已依更正原則下修為附註）」與「Post-hoc Total Rescue 6格、對應更正後基準85/320（原84/320）」之全部來源；另1格repaired-still-fail不計入任何rescue統計，僅代表規則matcher/guard觸發、transform已套用，但healed後仍未通過完整G1–G4。

7格對照Healer介入前4B／9B Tier1結果：6格屬BOTH_FAIL（Primary 4、Post-hoc 1、修復後仍FAIL 1），1格屬NINE_B_ONLY_PASS（Primary 1），皆未落在BOTH_PASS或FOUR_B_ONLY_PASS。多數案例即使4B提升至9B仍未自然轉為PASS，非僅見於4B落後9B案例。唯一NINE_B_ONLY_PASS案例中，Healer使4B由FAIL轉PASS，與9B同為PASS。僅屬post-hoc交叉標註，不動原Tier1統計與McNemar結果。

| Baseline Tier 1象限 | Primary rescue | Post-hoc rescue | 修復後仍FAIL | 合計 |
|---|---:|---:|---:|---:|
| BOTH_FAIL | 4 | 1 | 1 | 6 |
| NINE_B_ONLY_PASS | 1 | 0 | 0 | 1 |
| 合計 | 5 | 1 | 1 | 7 |

Tier 1象限均依Healer介入前的4B與9B Baseline結果判定；Healer後結果僅作案例交叉標註。

---

### 10.2 完整 10 格 eligible 帳與修復效果分層

針對 Qwen 4B **241** 格 Baseline FAIL，`decide_healer_eligibility()` 凍結規則審查後共 10 格符合事前凍結之安全介入條件。詳細母體與處置狀態來自 `docs/experiments/results/math16_pilot02_qwen4b_healer_v4_r001/eligible_execution_records.jsonl`（10 筆）與 `docs/experiments/results/math16_pilot02_qwen4b_healer_v4_posthoc_corrected_chain_r001/eligible_execution_records.jsonl`（corrected-chain 重放）。

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

Primary 仍維持 5 格 rescue（依更正後基準對應 84/320，原 83/320，中繼值已依更正原則下修為附註，不再作主表標題）；Post-hoc corrected-chain 為 6 格 rescue（依更正後基準對應 **85/320**，原 84/320）。兩者嚴格分帳：84/320（原 83/320）為 Primary Protocol 正式認可之技術中繼數據，85/320（原 84/320）為經基準更正後之最終 Verified 結果，詳見 [更正說明](05_math16_baseline_correction_note_v1.md)。

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

為維護實證研究之嚴謹性，嚴格實施 Primary 與 Post-hoc 數據分帳（模型呈現順序：Gemini 3.5 Flash → Qwen 3.5 9B → Qwen 3.5 4B）：

| 模型與項目 | Primary / Baseline | Eligible | Primary Rescue / Final | Post-hoc hybrid inventory / Corrected Final | Method 1 Regression |
|---|---|---|---|---|---|
| **Gemini 3.5 Flash** | **Primary 289 / 320** | 0 格 | **0 格 (289/320)** | **Post-hoc hybrid inventory 306/320** | Not measured |
| **Qwen 9B** | 101 / 320 | 0 格 | **0 格 (101/320)** | 0 格 (101/320) | Not measured |
| **Qwen 4B** | **79/320** | 10 格 | 5 格（84/320，中繼值，demoted，見附註†） | 總救援 **6 格 (85/320)** | Not measured |

† Qwen 4B Baseline 已依 [更正說明](05_math16_baseline_correction_note_v1.md) 由 78/320 更正為 79/320（單一 cell 抽取瑕疵，非模型能力差異）。Primary 中繼值（原 83/320）依更正基準連動為 84/320，依採行原則自本表標題數據中下修為附註，不再作為主要比較數字；85/320（原 84/320）為 corrected-chain 總救援 6 格之最終 Verified 結果。

- **分帳原則**：Qwen 4B 的 84/320（原 83/320）為事前預註冊 Protocol 之 Primary 技術中繼數據，現依更正原則不再作為主表標題；85/320（原 84/320）為 corrected-chain 總救援 6 格的最終 Verified 結果（相較 Primary 僅多 1 個 PASS）。Gemini 的 Primary 為 289/320（`Ab2d+spec-v1` 為 63/80）；`Ab2d+spec-v2` 的 80/80 與其餘三條件合計為 post-hoc hybrid inventory 306/320，僅作機制／版本盤點，不得誤稱為 Gemini Primary 或正式比較結果。

### Method 1 依 Development 40／Evaluation 120 切分結果

| 範圍 | Baseline PASS | 最終技術修正結果 PASS | 救回 |
|---|---:|---:|---:|
| 官方 320 格 | **79/320** | **85/320** | 6 |
| Contract-Aware 160 格 | 44/160 | 48/160 | 4 |
| Development 40 格 | 11/40 | 11/40 | 0 |
| Evaluation 120 格 | 33/120 | 37/120 | 4 |
| 敏感度 70 格 | 21/70 | 21/70 | 0 |

> **表下注記：**
> - 官方 320 格已依 [更正說明](05_math16_baseline_correction_note_v1.md) 由 Baseline 78/320／最終 84/320 更正為 79/320／85/320（單一 cell 屬 `ab1` 條件，不在本切分之 `ab2d`／`ab2d_spec_v2` 範圍內，故 Contract-Aware 160／Development 40／Evaluation 120／敏感度 70 子集數字不受影響、維持不變）。
> - Primary 技術中繼結果對應更正後為 84/320（原 83/320，demoted，不再作主表標題）；85/320 為 corrected-chain 最終技術修正結果。
> - Method 1 未對 Baseline PASS cells 執行 Healer。Regression: Not measured under Method 1。
> - Evaluation 120 格是主要結果。
> - 70 格只是排除 5 個 `cohort_level_provenance_uncertain` 任務後的敏感度分析，不得取代 120 格。
> - 70 格救援為 0 與既有 split 結構及 Generic Core 已知命中分布一致，不寫成新發現。
> - **資料分帳治理／Contract-Aware 定義：** Round 1 全量＝**16題 × 4條件 × 5 seeds = 320**。本切分為 Contract-Aware 子集，**僅含** `ab2d` + `ab2d_spec_v2`＝**16題 × 2條件 × 5 seeds = 160**（Development：`4×2×5=40`；Evaluation：`12×2×5=120`；**40+120=160**，只是 320 子集）。`ab1`／`ab2g` 仍在 320 總體，但因無 domain API／function contract 不納入此 split；**不得**推論一般 Healer 完全不能作用於 `ab1`／`ab2g`。Development 40 用於理解失敗模式，不宣稱完全未見；該切分內 verified rescue **全部**在 Evaluation 120，Development 40 verified rescue＝**0**。結論只支持**非題目客製化**，不宣稱完全無污染風險。後續 Aggressive 規則採通用 AST／結構 pattern，development influence 仍以 frozen-rule benchmark 控制。Method 1 之 Dev／Eval rescue **不得**與 Round 1 Aggressive overlay（corrected **79→87／rescue 8**；frozen archive 79→88／9）混稱。

詳細結果與切分說明見：[Math16 Method 1 — 依 Development 40／Evaluation 120 切分成果報告](../../../experiments/reports/math16_method1_40_120_split_results_report_v1.md)。

### Method 2 All-Cell 正式結果

| Raw PASS | Final PASS | 淨增 | Verified rescue | Regression | Preserved pass | Still failed |
|---:|---:|---:|---:|---:|---:|---:|
| 79/320 | 85/320 | 6 | 6 | 0 | 79 | 235 |

> Method 2 對全部 320 格 raw source 先執行 Eligibility，Eligible 11 格才套用 frozen Healer；完成 source decision 後，再以同一 pinned Evaluator 分別評分 Raw 與 Final。Eligible 11 格為 6 格 rescue、5 格 still failed。Method 2 的 `Regression measured = 0/320` 為全 320 格 Raw／Final 雙路評分之實際量測結果；Method 1 則為 `Regression not measured`。

詳細流程、eligible 逐格帳與 rule_id 分帳見：[Math16 Method 2 All-Cell 正式結果報告](../../../experiments/reports/math16_method2_all_cell_results_report_v1.md)。

---

## 11B. 三模型 Aggressive Healer Round 1（FAIL-only 單輪正式主分析）

> **分帳聲明：** 第 10–11 節 Method 1／Method 2 Conservative／Primary 帳目（4B **79→85**，verified rescue **6**）維持不變。本節為後續封存之 **Aggressive／cumulative FAIL-only Round 1** 三模型正式比較主分析；兩者**不得混帳**。權威比較見 [08_math16_three_model_aggressive_healer_round1_comparison_v1.md](08_math16_three_model_aggressive_healer_round1_comparison_v1.md) 與 `docs/experiments/manifests/math16_three_model_round1_summary_v1.json`。

### 11B.1 安全邊界 vs 能力邊界

| 邊界 | 定義 | Round 1 含義 |
|---|---|---|
| **能力邊界** | Baseline 生成 PASS／320 | Gemini 289、9B 101、4B 79 |
| **安全邊界** | 殘餘 FAIL 是否落入 frozen rules 的唯一、局部、可驗證修法窗口 | 修復率取決於 residual failure type／rule fit，而非「Baseline 越高越好修」 |

**設計口號：** **先求不修壞，再求修得好**——以 Abstain 與 regression=0 守住安全邊界，再談 verified rescue／partial repair。

### 11B.2 Round 1 核心結果

Protocol：凍結規則 × **FAIL-only** × **single-pass** Deterministic Healer；不呼叫模型。

| 模型 | Baseline → Final | verified rescue | Baseline FAIL | 修復率 | regression |
|---|---|---:|---:|---:|---:|
| Gemini 3.5 Flash | 289 → 289 | 0 | 31 | 0% | 0 |
| Qwen 9B | 101 → 102 | 1 | 219 | 0.46% | 0 |
| Qwen 4B（corrected overlay） | 79 → **87** | **8** | 241 | **3.32%** | 0 |
| Qwen 4B（frozen archive） | 79 → 88 | 9 | 241 | 3.73% | 0 |

> 4B 主表採 **corrected overlay**（見 2026-07-30 Correction Notice）；frozen archive 88／9 永久保留於 C5a／Round1 summary，不作分析主敘事。

Cumulative PASS 曲線（C0→C5c；4B 為 corrected overlay；括號內為 frozen）：

| 模型 | C0 | C1 | C2 | C3 | C4 | C5a | C5b | C5c |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Gemini | 289 | 289 | 289 | 289 | 289 | 289 | 289 | 289 |
| Qwen 9B | 101 | 101 | 102 | 102 | 102 | 102 | 102 | 102 |
| Qwen 4B | 79 | 85 | **85**（86） | **85**（86） | **85**（86） | **87**（88） | **87**（88） | **87**（88） |

**正式結論（不得擴張因果）：** 在同一套凍結、FAIL-only、單輪 Deterministic Healer 下，分析層 corrected overlay 為 Qwen 4B／9B／Gemini verified rescue **8／1／0**（frozen archive 仍記 4B＝9）；以 Baseline FAIL 為分母，修復率分別為 **3.32%**／0.46%／0%（frozen 4B 率 3.73% 僅作歷史封存）。4B 真 rescue＝Tier A 6＋D1 active-shadow 2；C2 +1 為幽靈帳。在本次三模型與 16 題實驗範圍內，Baseline 表現較高的模型，其殘餘失敗較少命中現有 frozen rules 的安全修復窗口。此結果顯示 Healer 效益與 residual failure type 及規則適配程度密切相關，但不宣稱模型規模與修復率存在普遍因果關係。三模型 regression 均為 0。

### 11B.3 Partial repair 分帳

**正式定義：** Partial repair 不計入 verified rescue，但可表示 Healer 已移除語法、執行或結構 blocker，使程式由不可解析／不可執行前進至可診斷狀態。

| 帳目 | 含義 |
|---|---|
| verified rescue | FAIL→PASS |
| parse gain | 不可解析 → 可解析 |
| execution gain | 不可執行 → 可執行／可診斷 |
| blocker-removal-only | 已移除 blocker，但仍未 PASS |
| modified-still-failed | 有修改但最終仍 FAIL |
| abstain | 不滿足唯一安全修法 → 不介入 |
| regression | PASS→FAIL |

**9B（authoritative FAIL-gated，已封存）：** Tier B parse 4／exec 2／blocker-only 3；C1 modified-still-failed 1；C2 modified-still-failed 6；D1（C4→C5a）exec 3／blocker-only 3／modified-still-failed 12。

**Gemini：** 全層 eligible＝0、modified＝0 → Abstain；rescue 與 partial-repair 增益皆 0。

**4B（cumulative `_v1` sealed；分析 overlay）：** Tier A rescue 6、modified-still-failed 5；Tier B **帳面** rescue 1（幽靈：密封 bytes 未晉升）／overlay 計 **0**、parse 5、exec 1、modified-still-failed 4；Tier C2 modified-still-failed 5；D3+D1 合併 rescue **2**（active-shadow）、parse 1、exec 4、modified-still-failed 5；D5 modified-still-failed 1；D2 exec 1 且 verdict=`BLOCKER_REMOVAL_ONLY`。缺獨立欄位者**不推估**。

Abstain 與 regression＝0 的意義：Abstain 是安全邊界防禦（不猜修）；regression＝0 是本次 Round 1 三模型觀察結果，不宣稱任意情境保證。

### 11B.4 Round 邊界、40／120 切分、2B exploratory 與 4B fixpoint

| 項目 | 狀態 |
|---|---|
| Round 1 | **正式主分析**（本節與比較報告；三模型主表不變） |
| 三模型 Round 2 | **尚未執行**（不得以 4B fixpoint 冒充 Round 2 覆寫） |
| 4B cell-wise fixpoint | **已完成** post-hoc 機制探針（見 §11B.4.3）；不得覆寫 Round 1 主表 |
| Development 40／Evaluation 120 | Method 1 contract-aware 切分另帳（見第 11 節）；Evaluation 120 為該切分主要結果；Dev rescue＝0、Eval rescue＝4；與 Round 1 全量 320 headline **分帳** |
| Qwen 3.5 2B | 四條件 smoke **0/16 PASS**；**已完成** 16-cell exploratory lower-bound frozen Healer 零模型 replay（namespace：`qwen2b_16cell_exploratory_lower_bound_v1`）；**不納入**三模型正式主表，**不估計**一般修復率 |

#### 11B.4.1 Qwen 3.5 2B exploratory Healer 結果（已封存）

Protocol：與 Round 1 相同之凍結規則 × FAIL-only × single-pass；僅使用既有 smoke／timeout-rerun raw；不呼叫模型。

| 指標 | 數值 |
|---|---|
| Baseline → Final | **0/16 → 0/16** |
| verified rescue | **0** |
| regression | **0** |
| Tier A | eligible 2、modified 2、parse gain 1、blocker-removal-only 1 |
| D3 | eligible 1、modified 1、modified-still-failed 1 |
| D1 | eligible 1、modified 1、modified-still-failed 1 |
| Tier B／C1／C2／D5／D2 | eligible／modified／rescue 皆 0（noop／ineligible） |

主要失敗型態（C0／smoke 對齊）：runtime failure **7**、catastrophic truncation **5**、parse minor **2**、schema **1**、answer incorrect **1**。

解讀：2B 失敗可被局部修正（partial repair），但多數仍距完整 PASS 較遠；**不**把 0/16 寫成一般修復率，亦**不**混入第 11B.2 三模型正式主表。

#### 11B.4.2 四模型探索性「可修復窗口」敘事（非正式同等比較）

> **證據層級：** 探索性機制假說（exploratory mechanism hypothesis）。**不得**畫成與三模型 Round 1 同等正式統計比較；樣本規模異質（2B＝16 cells；4B／9B／Gemini 各＝320 cells）。

四模型結果呈現一個探索性的可修復窗口圖像：2B 的失敗雖可被局部修正，但多數仍距完整 PASS 較遠；Gemini 的 residual FAIL 未命中現有 frozen rules；介於兩者之間的 4B 與 9B 出現較多 deterministic rules 可介入案例，其中 4B 的 verified rescue 最明顯。這支持一項機制性假說：Healer 的施力空間可能集中在模型已具備主要解題骨架、但仍殘留局部、唯一、可驗證結構瑕疵的中間區間。

**必須同時遵守之限制：**
- 2B 僅 16 cells；4B／9B／Gemini 各 320 cells。
- 僅屬 exploratory mechanism hypothesis。
- 不作正式相關、因果或普遍化主張。
- 不寫「Gemini 幾乎無結構性失敗」。
- 不寫「9B 多數已是語意層」。

#### 11B.4.3 Qwen 4B cell-wise deterministic fixpoint replay（已封存）

> **定位：** 4B-only post-hoc mechanism pilot。**不得**覆寫 Round 1 三模型主表；**不是**三模型 Round 2 正式覆寫。

Protocol／結果：`math16_qwen4b_cellwise_fixpoint_replay_protocol_v1`；`docs/experiments/results/math16_qwen4b_cellwise_fixpoint_replay_v1/`。

| 指標 | 數值 |
|---|---|
| 輸入 | Round 1 final 後仍 FAIL **232** cells |
| 永久排除 | Round 1 final 已 PASS **88** cells（本輪未掃描） |
| 規則順序 | `A→B→C1→C2→D3→D1→D5→D2`；`max_round=8` |
| `ZERO_CHANGE_CONVERGENCE` | **232**（全部第一輪 zero-change） |
| `ITERATIVE_RESCUE` | **0** |
| `CYCLE_DETECTED` | **0** |
| `MAX_ROUND_NON_CONVERGENT` | **0** |
| model calls | **0** |

**結論：** 現有凍結 Healer 在 Round 1 後對 **frozen** 4B residual FAIL（232）已達**操作上的 fixpoint**（再跑完整一輪 stack 無 source 變更、無額外 verified rescue）。**限制（2026-07-30 overlay）：** 232／232 zero-change **僅對 frozen 88／232 人口鎖成立**；corrected residual FAIL＝**233**（含未掃描之 source–label mismatch cell），**不得**宣稱涵蓋全部 corrected residual FAIL；本輪不補跑 fixpoint v2。

**限制：** 本輪**未掃描** 88 個 PASS cells，**不得**把本輪 regression＝0 當新安全性證據；正式 regression 證據仍來自 Round 1／Method 2 等已封存帳。

#### 11B.4.4 Healer 世代切割（方法／provenance）

舊版工程 Healer（`core/healers`）目標是盡量恢復可執行；Math16 正式 Healer 重新建立 deterministic、evaluator-blind、保守拒修與固定證據紀錄。舊系統僅作歷史來源，**不參與** Round 1 正式修補決策。若共用 parser／AST 等基礎設施，僅能主張「修補決策模組獨立重寫」，不得宣稱整套完全不共用程式碼。詳見權威 provenance：`docs/experiments/reports/math16_healer_rule_provenance_audit_v1.md` §7–§9。

---

## 11C. 三重安全性驗證

> **定位：** 整合 Round 1 FAIL-gated、三模型 cell-wise Fixpoint Replay、與三模型 320-cell Safety Benchmark 的安全性證據層。**不**覆寫第 10–11 節 Conservative／Primary 帳，亦**不**覆寫第 11B 節 Aggressive Round 1 主表。主報告科學口徑採 corrected account：Conservative **+6**；Aggressive 額外 **+2**；Aggressive Final **79→87**（verified rescue **8**）。

### 11C.1 Round 1 FAIL-gated

Round 1 正式修復流程**只對 FAIL cells** 套用凍結規則；**PASS cells 不進入**正式修復流程。此為第一層防禦：避免對已通過單元做不必要修改。

### 11C.2 Cell-wise Fixpoint Replay

Protocol：固定規則序 `A→B→C1→C2→D3→D1→D5→D2`；`max_round=8`；不呼叫模型。母體＝各模型 Round 1 後 residual FAIL。

| 模型 | residual FAIL | 第1輪收斂 | 第2輪收斂 | rescue | cycle | max-round exhaustion |
|---|---:|---:|---:|---:|---:|---:|
| Qwen 4B | 232 | 232 | 0 | 0 | 0 | 0 |
| Qwen 9B | 218 | 215 | 3 | 0 | 0 | 0 |
| Gemini | 31 | 31 | 0 | 0 | 0 | 0 |
| **合計** | **481** | **478** | **3** | **0** | **0** | **0** |

**正式解讀：** 三模型皆在最多兩輪內收斂；固定規則反覆執行**未產生**新增 verified rescue。此為操作收斂證據，**不得**寫成「單輪架構是真實 fixpoint」。

結果根目錄：`math16_qwen4b_cellwise_fixpoint_replay_v1/`、`math16_qwen9b_cellwise_fixpoint_replay_v1/`、`math16_gemini_cellwise_fixpoint_replay_v1/`。

### 11C.3 320-cell Safety Benchmark

Protocol：對完整 320 cells（含 source-validated PASS 與 FAIL）執行同一固定規則序之單輪 safety scan；量測 preserved pass、regression、modified。科學口徑採 **corrected／source-validated** PASS 母體（4B＝**87**）。

| 模型 | cells | source-validated PASS | preserved | regression | modified |
|---|---:|---:|---:|---:|---:|
| Qwen 4B | 320 | 87 | 87 | 0 | 2 |
| Qwen 9B | 320 | 102 | 102 | 0 | 13 |
| Gemini | 320 | 289 | 289 | 0 | 5 |
| **合計** | **960** | **478** | **478** | **0** | **20** |

> **口徑註記：** 4B 的 PASS／preserved 採 sealed-source corrected account（87／87）；9B 與 Gemini 採 frozen label，且其 sealed-source 重評皆與 frozen label 一致（102／102、289／289）。三模型 479-cell audit 僅發現 4B 一格 label／source mismatch，其餘 478 格一致。

**正式解讀：** 三模型所有 source-validated PASS 均 preserved，**未觀察到** PASS→FAIL regression。Modified 表示 source 被規則修改，**不等於** rescue／regression。

結果根目錄：`math16_qwen4b_aggressive_320_safety_benchmark_v1/`、`math16_qwen9b_aggressive_320_safety_benchmark_v1/`、`math16_gemini_aggressive_320_safety_benchmark_v1/`。

### 11C.4 Gemini 補充

Gemini 的 5 個 modified cells 全部由 `TIER_D_OPS_SHADOW_REMOVAL_V1` 修改，原本與修改後皆 PASS；顯示高通過率模型仍可能存在可安全移除的 Ops shadow binding，提供 D1 類規則跨模型安全性的補充證據。

---

## 12. Qwen 4B與9B配對分析

在 320 個完全相同題目與條件配對單元中，對 Qwen 4B 與 9B 進行一對一 Tier 1 配對分析（本節為 4B vs 9B 兩模型配對統計結構，維持原有排序，不套用三模型呈現順序規則）：

![Figure 4 Tier 1配對](figures/figure_04_tier1_paired_analysis.png)

### 2×2 配對矩陣
- **BOTH_PASS (兩者皆過)**：52 格
- **FOUR_B_ONLY (4B 獨過)**：**27** 格
- **NINE_B_ONLY (9B 獨過)**：49 格
- **BOTH_FAIL (兩者皆敗)**：**192** 格
- **總測試數**：320 格

> 已依 [更正說明](05_math16_baseline_correction_note_v1.md) 更正：單一 cell（`ce115_calc_polynomial_division_l1 / ab1 / seed 2026072003`）由 BOTH_FAIL 移至 FOUR_B_ONLY_PASS（原 26→27 格；原 193→192 格），BOTH_PASS (52) 與 NINE_B_ONLY (49) 不受影響。

### 配對統計量
- **Net Cell Gain (淨增加格數)**：**+22** 格 ($49 - 27$)
- **Paired Risk Difference (RD)**：**+6.875%**
- **Exact McNemar Test**：$p = 0.015440$ (單元層級顯示顯著偏向 9B；原 0.010582)
- **Wald 95% CI**：`[1.59%, 12.16%]`（即 `[0.0159, 0.1216]`）
- **Matched-pairs Odds Ratio (OR)**：**1.81** ($49/27$，原 1.88)
- **Task-clustered Bootstrap 95% CI**：`[-1.56%, +14.37%]` (考量 16 題型聚類效應後信賴區間跨 0；原 `[-0.94%, +14.38%]`)

---

## 13. Family分層

將 320 個配對單元按四大數學家族拆解（欄位順序固定為 `BOTH_PASS / FOUR_B_ONLY / NINE_B_ONLY / BOTH_FAIL`；本節為 4B vs 9B 兩模型配對統計結構，不套用三模型呈現順序規則）：

![Figure 3 Family差異](figures/figure_03_family_breakdown.png)

### 四大家族配對表現表

| 數學家族 | BOTH_PASS | FOUR_B_ONLY | NINE_B_ONLY | BOTH_FAIL | 總格數 | Exact McNemar p | 備註 |
|---|---|---|---|---|---|---|---|
| **Integer** | 29 | 1 | 13 | 37 | 80 | $p = 0.001831$ | 9B 表現較佳 |
| **Polynomial** | 3 | **14** | 6 | **57** | 80 | $p = 0.1153$ | 4B 獨過較多 (異常分析見 14 節) |
| **Radical** | 10 | 5 | 9 | 56 | 80 | $p = 0.423950$ | 兩者無顯著差距 |
| **Fraction** | 10 | 7 | 21 | 42 | 80 | $p = 0.012541$ | 9B 淨勝 14 格 (拆解見 14 節) |

> Polynomial 家族已依 [更正說明](05_math16_baseline_correction_note_v1.md) 更正：FOUR_B_ONLY 原 13→14 格、BOTH_FAIL 原 58→57 格（單一 cell 由 BOTH_FAIL 移至 FOUR_B_ONLY_PASS）、p 值原 0.167089→0.1153；4B Polynomial 總通過數對應由 16/80 更正為 **17/80**，9B（9/80）不受影響。

Fraction 的 NINE_B_ONLY = 21；其中 L1–L4 = 15（涵蓋語法、契約、API 與執行問題），L5 = 6，不可解讀為純數學能力差異。

---

## 14. 4B Ab2d+api與9B Polynomial異常

### 4B `Ab2d+api` 通過率低下診斷
4B 在 `Ab2d+api` 條件下通過數降至 8/80 格。事後診斷顯示：在已剖析之 27 格失敗診斷樣本中，77.8% (21/27) 屬 Python 本體 SyntaxError（括號未閉合或語法破碎），僅 18.5% (5/27) 屬 Parser 不友善。診斷結果不偏向以評分 Parser 偏差為主要失敗來源；此結論僅限定於已剖析之 27 格診斷樣本，未建立 Prompt 結構與生成錯誤之因果關係，亦不可外推為全域比例或完全排除 Parser 影響。

### 9B Polynomial 表現低下與 Fraction 拆解診斷
Qwen 9B 在 Polynomial 家族通過數偏低 (9/80 vs 4B 的 **17/80**，原 16/80，已依基準更正調整)，集中於 `ce115_calc_polynomial_division_l1` 單一題型與特定 LaTeX 組裝衝突。此屬特定欄位提示結構敏感性，未建立因果關係，不可外推為 9B 全域能力失控。

在 Fraction 家族 21 格 NINE_B_ONLY 通過案例中，機制拆解顯示：有 15 格屬 L1–L4（涵蓋語法、契約、API 與執行問題），另 6 格屬 L5（語意與數學邏輯層）。差距較多反映端到端生成穩定性，不可解讀為純數學推理能力差異。

---

## 15. Gemini描述性參照

Prompt 條件對三模型通過數之影響如下（欄位順序統一調整為 Gemini 3.5 Flash → Qwen 3.5 9B → Qwen 3.5 4B）：

![Figure 2 Prompt條件](figures/figure_02_prompt_conditions.png)

### Prompt 條件比較

| Condition | Gemini 3.5 Flash | Qwen 3.5 9B | Qwen 3.5 4B |
|---|---|---|---|
| **Ab1** | 72 / 80 | 18 / 80 | **16 / 80** |
| **Ab2g** | 76 / 80 | 27 / 80 | 19 / 80 |
| **Ab2d+api** | 78 / 80 | 16 / 80 | 8 / 80 |
| **Ab2d+spec-v2** | 80 / 80* | 40 / 80 | 36 / 80 |

> **Figure 2 圖說與分帳特別聲明**：
> - Gemini 的 `Ab2d+spec-v2` 為 post-hoc inventory；補齊 API 簽名卡後該條件達 80/80。
> - Gemini 正式 Primary 生成採用 `Ab2d+spec-v1`，通過數為 63/80（屬研究歷程）。
> - Qwen 4B 與 9B 採用 `Ab2d+spec-v2` 正式生成。
> - 三模型提示版本不同，不得假裝為完全同條件之 Primary 直接推論。
> - `Ab1` 之 Qwen 4B 已依 [更正說明](05_math16_baseline_correction_note_v1.md) 由 15/80 更正為 **16/80**（單一 cell 抽取瑕疵更正，屬本表唯一受影響儲存格）。

---

## 16. Healer安全介入邊界

Deterministic AST Healer 之安全介入架構概念如下：

![Figure 6 安全介入概念圖](figures/figure_06_healer_concept_zones.png)

### 安全邊界 vs 能力邊界
- **能力邊界**：Baseline 生成能否通過（PASS／320）。
- **安全邊界**：殘餘失敗是否落入 frozen rules 的唯一、局部、可驗證修法窗口；未命中則 **Abstain**。
- **先求不修壞，再求修得好**：先以 Eligibility／Abstain 避免猜修與 regression，再追求 verified rescue 與可審計的 partial repair。
- Round 1 三模型比較顯示：Baseline 較高者（Gemini）未必有更高 Healer 修復率；核心是 residual failure type／rule fit（見第 11B 節）。

### 安全介入邊界三原則
1. **可修復區 (Repair Window)**：僅對語法解答唯一、局部且可驗證之瑕疵（如特定 JSON key 包含瑕疵）進行確定性修正。
2. **防禦性放棄 (Abstain Zone)**：對於邏輯錯誤、語義缺失或具備多種修正可能之案例，Healer 拒絕盲猜，主動選擇 Abstain。
3. **零倒退防線 (Zero Regression)**：透過事前 Eligibility 與事後 Revalidation 兩道防線，降低修改破壞原本正確程式之風險。本次 Round 1 三模型觀察到 regression＝0；此為觀察結果，非任意情境保證。

### Partial repair 的位置
**正式定義：** Partial repair 不計入 verified rescue，但可表示 Healer 已移除語法、執行或結構 blocker，使程式由不可解析／不可執行前進至可診斷狀態。主表仍以 verified rescue（FAIL→PASS）為準；parse／execution／blocker-removal／modified-still-failed 另帳（見第 11B.3 節）。

---

## 17. 五項主要發現

本研究歸納出以下核心實證發現：

1. **Baseline能力與Healer可修復窗口不同**：模型 Baseline 生成通過率高，不代表剩餘失敗中包含更多可修復瑕疵；修復視窗取決於失敗案例是否符合凍結之修復規則。
2. **4B存在窄小且可驗證的repair window（Conservative／Primary 帳）**：Qwen 4B 經 Active Healer verified rescue 6 格，通過數由 **79/320** 提升至 **85/320**（原 78→84/320，已依 [更正說明](05_math16_baseline_correction_note_v1.md) 更正）。分帳上，5 格於 Primary run 確認（對應更正後基準 84/320，中繼值，不再作主表標題），另 1 格經 corrected-chain 確認方達最終 85/320；另有 1 格 repaired-still-fail 不計入 rescue。
3. **三模型 Aggressive Healer Round 1（正式主分析，另帳）**：同一套 FAIL-only 單輪凍結規則下，分析層 corrected overlay 為 4B／9B／Gemini **79→87（rescue 8）／101→102（rescue 1）／289→289（rescue 0）**（修復率 **3.32%**／0.46%／0%）；frozen archive 仍記 4B **79→88（rescue 9／3.73%）**。僅描述本次遞減關聯，不宣稱規模因果；核心是 residual failure type／rule fit。三模型 Round 2 尚未執行；4B-only fixpoint（frozen 232 全 zero-change、rescue 0；**不涵蓋** corrected residual 233）為 post-hoc 機制探針，不覆寫主表。
4. **2B exploratory lower-bound（另帳，非正式主表）**：16-cell frozen Healer replay 為 **0/16 → 0/16**（rescue 0、regression 0）；Tier A／D3／D1 可見局部 partial repair，但不估計一般修復率，亦不納入三模型正式主表。
5. **9B整體通過較高，但Family結果非單調**：9B 在 Overall 通過率高於 4B，但在 Polynomial 家族因單一題型提示敏感性出現非單調狀況。
6. **Prompt效果依模型、版本與部署條件而異**：同一 Prompt 條件（如 `Ab2d+api`）在 4B 與 Gemini 上呈現截然不同之效用。
7. **Abstain與partial repair皆屬安全／診斷價值**：Abstain 是 Deterministic Healer 的重要安全能力；partial repair（parse／execution／blocker-removal）不計入 verified rescue，但可表示 blocker 已移除並進入可診斷狀態。
8. **四模型可修復窗口僅屬探索性機制假說**：2B（16）與 4B／9B／Gemini（各 320）不得作同等正式比較；不作相關／因果／普遍化主張（見第 11B.4.2 節）。

---

## 18. 方法學限制

本研究嚴格受限於以下 10 項凍結方法學限制：

1. **Overall 統計顯著性與外推不確定性 (Cell-level vs Task-level)**：細胞層級 Exact McNemar 檢定顯示 9B-only (49格) 顯著多於 4B-only (**27**格) ($p = 0.015440$；Wald 95% CI `[1.59%, 12.16%]`；OR = 1.81)；然考慮 16 個 Task 聚類效應之 Task-clustered Bootstrap 95% CI 跨 0 (`[-1.56%, +14.37%]`)，顯示外推至未知全新題型時仍具抽樣不確定性。不得宣稱「9B 保證優於 4B」。（已依 [更正說明](05_math16_baseline_correction_note_v1.md) 更正，原 4B-only 26 格、$p = 0.010582$、CI `[-0.94%, +14.38%]`；顯著性方向與結論未變。）
2. **四大數學家族分層屬探索性分析 (Exploratory Subgroup Analysis)**：四大家族分層未事前預註冊族群 alpha 矯正，屬 Post-hoc 探索性分析，其 $p$-values 僅供假說生成參考。
3. **Fraction 家族差距不可解讀為純數學能力差異 (Fraction Gap Interpretation)**：9B 在 Fraction 淨勝 14 格 ($p = 0.012541$)，機制拆解顯示 21 格 NINE_B_ONLY 中有 15 格屬 L1–L4（涵蓋語法、契約、API 與執行問題），另 6 格屬 L5 語意層，不可解讀為純數學推理能力差距。
4. **Polynomial 9B 偏低為局部格式共現 (Polynomial Anomaly Localized Co-occurrence)**：9B 在 Polynomial 表現偏低集中於 `ce115_calc_polynomial_division_l1` 多項式除法單一題型與特定 LaTeX 組裝衝突，未建立因果關係，不可外推為 9B 全域能力失控。
5. **Qwen 4B `Ab2d+api` 77.8% 語法錯誤侷限於診斷樣本 (4B Ab2d Anomaly Sample Bound)**：4B 在 `Ab2d+api` 下 77.8% (21/27) SyntaxError 結論僅適用於已剖析之 27 格診斷樣本，不可外推為全域失敗比例。
6. **Gemini 作為 Tier 2 描述性參照 (Gemini as Tier 2 Reference Only)**：Gemini 3.5 Flash (289/320, 90.31%) 僅作強模型描述性基準參照，不可宣稱「證明大模型規模因果壓倒性勝出」。
7. **Prompt 提示版本異質性 (Prompt Version Discrepancy)**：Gemini Primary 採用 `Ab2d+spec-v1` (63/80)；後續 `Ab2d+spec-v2` 補齊 API 簽名卡後為 80/80 的 post-hoc inventory，與其餘三條件形成 306/320 post-hoc hybrid inventory，僅作機制／版本盤點。Qwen 4B/9B 正式生成採用 `Ab2d+spec-v2`，通過數為 36/80 與 40/80。
8. **Regression 分帳與範圍**：Method 1 未對 Baseline PASS cells 執行 Healer，因此 `Regression not measured`；Method 2 的 `Regression measured = 0/320` 僅代表本次 320 個單元及凍結規則下的實際量測結果，不可宣稱「保證在任意情境下 100% 絕不倒退」。
9. **`Eligible = 0` 不代表模型無失敗 (Eligibility Zero Scope)**：Gemini (31 FAIL) 與 9B (219 FAIL) 之 `Eligible = 0` 代表殘餘失敗未命中事前凍結規則，系統主動 Abstain，不代表生成無錯誤。
10. **全域邊界與範疇受限 (Global Protocol Bound)**：本研究所有數字與結論，僅嚴格適用於本次測試之 16 道數學題型、3 個模型、4 種 Prompt 條件、5 個隨機種子與凍結規則。

---

## 19. 評審追問摘要

選錄 8 項關鍵評審追問與標準答覆摘要：

### Q1: 為什麼要先做 Eligibility 審查，不直接全部程式都嘗試修復？
**答覆**：若不設 Eligibility 門檻，修復器將被迫對無明確修復依據的程式進行猜測性修改，破壞可解釋性並可能引入倒退 (Regression)。Eligibility 是維護「確定性安全介入」的必要防禦。

### Q2: Gemini 與 9B 的 `eligible=0` 是否代表 Healer 沒有用？
**答覆**：不是。Primary／Conservative 帳的 `eligible=0` 是安全 Abstain。Aggressive Healer Round 1 正式比較下，9B 有 verified rescue 1、Gemini 仍為 0；Gemini 的 0 代表安全窗口未命中，不是系統失效。

### Q3: 為什麼 4B 可以修復較多格，9B／Gemini 反而較少或為 0？
**答覆**：分帳：Primary 為 4B rescue 6；Round 1 正式比較採 corrected overlay 為 4B／9B／Gemini＝**8／1／0**（修復率 **3.32%**／0.46%／0%；frozen archive 仍記 4B＝9／3.73%）。關鍵是殘餘失敗型態是否落入凍結規則，不是模型越大越好修；不宣稱普遍因果。

### Q4: 為什麼不把所有 SyntaxError 都納入 Healer 修復範圍？
**答覆**：因為大多數 SyntaxError（如少寫半段邏輯、字串未閉合）並沒有唯一的修復解答。若強行修復將違反「修法唯一、不可反推答案」的核心原則，帶來極高修壞風險。

### Q5: 4B 的 Primary (84/320) 與 Post-hoc (85/320) 只差 1 格，其重放處置細節為何？
**答覆**：Qwen 4B Baseline = **79/320**（已依 [更正說明](05_math16_baseline_correction_note_v1.md) 由 78/320 更正，單一 cell 抽取瑕疵，非 Healer 相關）；Primary rescue = 5，final = **84/320**（原 83/320，中繼值，依採行原則不再作主表標題）；Post-hoc total rescue = 6，final = **85/320**（原 84/320，即本文最終 Verified rescue headline），相較 Primary 僅增加 1 個 PASS。在 10 個 Eligible 案例重放中，8 個處置狀態完全不變；2 個處置狀態改變（1 格由 `no_op` 改為 `rescued` 使 PASS 增加 1 格，1 格由 `no_op` 改為 `repaired_still_fail` 仍為 FAIL）。因此只有 1 格改變最終 PASS/FAIL 結果；此與基準更正之單一 cell 為互相獨立之兩件事（後者非 Healer eligible）。

### Q6: Abstain（不介入）是不是代表 Healer 的能力不足？
**答覆**：不是。知曉「何時不該介入」與「何時該介入」同等重要。Abstain 是控制 Regression 風險的防禦機制，代表系統在面臨不明確修復目標時主動放棄盲猜。

### Q7: Overall McNemar 與 Task-clustered Bootstrap 結論看似不同，該如何解讀？
**答覆**：兩者代表不同層級的統計檢視。McNemar 顯示本次 320 個 matched cells 中 discordant 方向偏向 9B ($p = 0.015440$，已依基準更正自 0.010582 更新)；而 task-clustered bootstrap CI 跨 0 (95% CI `[-1.56%, +14.37%]`，原 `[-0.94%, +14.38%]`)，顯示外推到其他未知題目時仍具抽樣不確定性。

### Q8: 為什麼 Fraction family 的 9B 優勢最明顯 (淨增加 14 格)？
**答覆**：在 21 格 9B-only PASS 中，拆解顯示 15 格 (71.43%) 屬 L1~L4（涵蓋語法、契約、API 與執行問題），另 6 格屬 L5 語意層。差距較多反映端到端生成穩定性，不可解讀為純數學推理能力差異。

---

## 20. 結論、後續工作與正式證據索引

### 結論
本研究結果支持以下定位：Deterministic AST Healer 具備精確價值與安全介入邊界。實證顯示：
1. AST Healer 不扮演第二個解題模型，而在可驗證之特定語法瑕疵窗口發揮確定性救援功能。Conservative／Primary 帳：4B verified rescue 共 6 格，通過數由 **79/320** 提升至 **85/320**（已依 [更正說明](05_math16_baseline_correction_note_v1.md) 自原 78→84/320 更正）。技術分帳上，Primary 救援 5 格、final 對應 84/320（原 83/320，中繼值，demoted）；另 1 格由 corrected-chain 確認方達最終 85/320，且另有 1 格 repaired-still-fail 不計入 rescue。
2. **Aggressive Healer Round 1（三模型正式主分析，另帳）：** 4B／9B／Gemini corrected overlay 分別 **79→87（rescue 8）／101→102（rescue 1）／289→289（rescue 0）**；修復率 **3.32%**／0.46%／0%（frozen 4B 仍為 79→88／9／3.73%）。只描述本次關聯，不宣稱規模因果；Gemini 0 rescue 代表安全窗口未命中（Abstain），不代表 Healer 無效。
3. Regression 嚴格分帳：Method 1 為 `Regression not measured`；Method 2 對全部 320 格 Raw／Final 雙路評分後為 `Regression measured = 0/320`；Round 1 三模型 cumulative 亦觀察到 regression＝0。
4. 面臨無確定修法之失敗時，系統依凍結規則選擇 Abstain；partial repair 另帳，不計入 verified rescue。
5. 三模型 Round 2 尚未執行。三模型 cell-wise Fixpoint Replay 已完成（residual 481：第1輪 478／第2輪 3；rescue＝0；見第 11C 節），屬 post-hoc 機制探針，不得覆寫 Round 1 主表；**不得**寫成「單輪架構是真實 fixpoint」。
6. **三重安全性驗證（第 11C 節）：** FAIL-gated ＋ 481-cell fixpoint ＋ 960-cell safety；source-validated PASS 478／478 preserved、regression＝0（本研究樣本中未觀察到，非絕對保證）；**不得**與 Method 2、Round 2 混稱。
7. Qwen 3.5 2B 四條件 smoke 為 0/16 PASS，且**已完成** 16-cell exploratory lower-bound frozen Healer replay：**0/16 → 0/16**（rescue 0、regression 0）；不估計一般修復率，不納入三模型正式主表。四模型「可修復窗口」僅作探索性機制假說（見第 11B.4 節）。
8. Development 40／Evaluation 120：Dev rescue＝0、Eval rescue＝4；只支持非題目客製化，不宣稱零污染。舊版 `core/healers` 不進 Round 1 正式決策（見 provenance §7）。

### 後續工作
1. 若執行三模型 Round 2：僅 post-hoc iterative replay，獨立分帳，不覆寫 Round 1。
2. 2B 若擴樣，須另開協議；不得把 16-cell exploratory 帳寫成 320 正式主表。
3. 擴充預註冊修復規則庫時，須以獨立驗證集驗證，禁止事後配合資料改規則。
4. 引入多 Task 跨領域擴展測試，縮減 Task-clustered Bootstrap 信賴區間不確定性。
5. 不以 fixpoint 收斂放寬 frozen rules；不以「單輪＝真實 fixpoint」改寫敘事。
6. **三重安全性驗證／320-cell safety：** 主報告採 corrected／source-validated 口徑；**不得**與 Method 2、Round 2 混稱；regression＝0 僅為樣本觀察。

### 正式證據與產物索引
- **Evidence Complete Milestone v1**：`docs/experiments/milestones/math16_pilot02_evidence_complete_v1/`
- **Integrated Results Report v1**：`docs/experiments/reports/math16_pilot02_integrated_results_report_v1.md`
- **正式 Jury Q&A Defense Manual v1**：`docs/決賽文件/實驗結果文件/Math16/04_math16_pilot02_jury_qa_final_v1.md`
- **三模型 Round 1 比較**：`docs/決賽文件/實驗結果文件/Math16/08_math16_three_model_aggressive_healer_round1_comparison_v1.md`
- **老師展示摘要**：`docs/決賽文件/實驗結果文件/Math16/09_math16_three_model_round1_teacher_brief_v1.md`
- **Round 1 summary JSON**：`docs/experiments/manifests/math16_three_model_round1_summary_v1.json`
- **2B exploratory lower-bound cumulative**：`docs/experiments/results/math16_cumulative_qwen2b_16cell_exploratory_lower_bound_v1/summary.json`
- **三重安全性驗證（§11C）**：三模型 Fixpoint＋320-cell Safety results roots（`math16_{qwen4b,qwen9b,gemini}_cellwise_fixpoint_replay_v1/`；`math16_{qwen4b,qwen9b,gemini}_aggressive_320_safety_benchmark_v1/`）
- **Healer provenance audit（含世代切割／40–120／fixpoint）**：`docs/experiments/reports/math16_healer_rule_provenance_audit_v1.md`
- **Six Core Figures v1**：`docs/experiments/visualization/math16_pilot02_core_figures_v1/`
- **One-Pager v2.3 (Pairwise Collision-Free)**：`docs/experiments/presentation/math16_pilot02_one_pager_v23/`
- **Final Report v1 (Base Version)**：`docs/experiments/reports/math16_pilot02_final_report_v1.md`
- **Seven-Cell Tier 1 Crosswalk v1**：`docs/experiments/reports/math16_healer_seven_cell_tier1_crosswalk_v1.md`
- **Post-hoc Six-Cell L2 Payload-Wrap Deep Audit v1**：`docs/experiments/reports/math16_posthoc_six_cell_l2_payload_wrap_deep_audit_v1.md`
- **L2 Payload-Wrap Eligibility Answer Leakage Audit v1**：`docs/experiments/reports/qwen4b_l2_payload_wrap_eligibility_answer_leakage_audit_v1.md`
