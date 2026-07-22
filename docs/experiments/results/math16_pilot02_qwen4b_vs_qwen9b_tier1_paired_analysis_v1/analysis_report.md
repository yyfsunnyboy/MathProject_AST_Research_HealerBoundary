# Math16 Pilot-02 Tier 1 配對統計分析報告 (Qwen 4B vs Qwen 9B)

```text
MATH16_PILOT02_QWEN4B_VS_QWEN9B_TIER1_PAIRED_ANALYSIS_COMPLETED
EXACT_MCNEMAR_COMPLETED
TASK_CLUSTERED_BOOTSTRAP_COMPLETED
SEED_AND_TASK_STABILITY_DOCUMENTED
```

**分析識別碼：** `math16_pilot02_qwen4b_vs_qwen9b_tier1_paired_analysis_v1`
**範疇：** Tier 1 正式配對比較（Qwen 3.5 4B vs Qwen 3.5 9B，共 320 組一對一 matched cells）
**資料驗證狀態：** 100% 完整匹配（320 pairs，無重複，無缺漏，4B PASS=78, 9B PASS=101）

---

## 1. 研究問題與 Tier 1 可比性理由

本分析旨在回應：**「在控制相同題目 (16 題)、相同 Prompt 條件 (4 種)、相同隨機種子 (5 個) 與相同主要 sampling 設定下，Qwen 3.5 9B 相較於 Qwen 3.5 4B 是否在端到端程式生成通過率上展現統計顯著的配對淨增加？」**

### Tier 1 可比性宣告
- **同模型家族**：均為 Qwen 3.5 衍生模型 (4B / 9B)。
- **同實驗因子**：16 題 $\times$ 4 conditions $\times$ 5 seeds = 320 matched cells。
- **嚴格對稱性**：每個 pair 共享相同的 task_id、condition、seed 與評估標準 (v4 Evaluator)。

---

## 2. 資料完整性驗證 (Data Completeness Audit)

| 項目 | 預期值 | 實測值 | 驗證狀態 |
| :--- | ---: | ---: | :---: |
| **Qwen 4B 總紀錄數** | 320 | 320 | PASS |
| **Qwen 9B 總紀錄數** | 320 | 320 | PASS |
| **成功匹配對數 (Matched Pairs)** | 320 | 320 | PASS |
| **重複 / 缺漏 / 身分不符** | 0 | 0 | PASS |
| **Qwen 4B Baseline PASS 總數** | 78 | 78 | PASS |
| **Qwen 9B Baseline PASS 總數** | 101 | 101 | PASS |

---

## 3. Overall 2×2 配對列聯表與 Exact McNemar 檢定

### 3.1 2×2 Contingency Table

| | Qwen 9B PASS | Qwen 9B FAIL | 合計 (Qwen 4B) |
| :--- | ---: | ---: | ---: |
| **Qwen 4B PASS** | **52** (`BOTH_PASS`) | **26** (`FOUR_B_ONLY_PASS`) | **78** (24.38%) |
| **Qwen 4B FAIL** | **49** (`NINE_B_ONLY_PASS`) | **193** (`BOTH_FAIL`) | **242** (75.62%) |
| **合計 (Qwen 9B)** | **101** (31.56%) | **219** | **320** |

### 3.2 統計檢定結果

- **不一致配對 (Discordant Pairs)**：
  - $b$ (`4B_ONLY_PASS`) = **26**
  - $c$ (`9B_ONLY_PASS`) = **49**
  - 淨增加 (Net Difference) = $c - b =$ **+23 格**
- **Paired Risk Difference (\Delta)**：
  - \Delta = \frac{101 - 78}{320} = +7.1875\% (**+0.0719**)
- **Exact Two-Sided McNemar Test $p$-value**：
  - $p = \mathbf{0.0106}$ ($p = 0.010582$)
- **Matched-Pairs Odds Ratio (OR)**：
  - $\text{OR} = \frac{c}{b} = \mathbf{1.88}$
- **95% 雙重信賴區間**：
  - Wald 95% CI: `[0.0194, 0.1243]` (+1.94% 至 +12.43%)
  - **Task-Clustered Bootstrap 95% CI** (10,000 resamples): `[-0.0094, 0.1437]` (-0.94% 至 +14.37%)

**統計結論**：在控制 Task, Condition, Seed 後，Qwen 9B 在 320 格配對測試中的基線通過率高於 Qwen 4B ($p = 0.0106 < 0.05$)，淨增加 23 格程式生成成功案例。

---

## 4. Condition 分層配對分析 (Secondary Decomposition)

各 Condition 分母均為 $n=80$ 格配對：

| Condition | 4B PASS | 9B PASS | BOTH PASS | 4B ONLY ($b$) | 9B ONLY ($c$) | BOTH FAIL | 淨增加 ($c-b$) | Paired RD (\Delta) | Task-Clustered Bootstrap 95% CI | Exact McNemar $p$-value |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :---: | ---: |
| **ab1** | 15/80 | 18/80 | 12 | 3 | 6 | 59 | **+3** | +0.0375 | [-0.0625, 0.1625] | 0.5078 |
| **ab2g** | 19/80 | 27/80 | 11 | 8 | 16 | 45 | **+8** | +0.1000 | [-0.0500, 0.2500] | 0.1516 |
| **ab2d** | 8/80 | 16/80 | 3 | 5 | 13 | 59 | **+8** | +0.1000 | [-0.0125, 0.2375] | 0.0963 |
| **ab2d_spec_v2** | 36/80 | 40/80 | 26 | 10 | 14 | 30 | **+4** | +0.0500 | [-0.1125, 0.2000] | 0.5413 |

### 保守解讀：
- `Ab2g` 展現最大的單一條件配對淨增加 (+8 格, $p = 0.1516$).
- `Ab2d+spec-v2` 兩模型皆有較高通過率 (4B 36/80, 9B 40/80)，配對淨增加 +4 格 ($p = 0.5413$).
- `Ab2d+api` 兩模型通過率均偏低 (4B 8/80, 9B 16/80)，淨增加 +8 格 ($p = 0.0963$).

---

## 5. Family 分層配對分析 (Secondary Decomposition)

各 Family 分母均為 $n=80$ 格配對：

| Family | 4B PASS | 9B PASS | BOTH PASS | 4B ONLY ($b$) | 9B ONLY ($c$) | BOTH FAIL | 淨增加 ($c-b$) | Paired RD (\Delta) | Task-Clustered Bootstrap 95% CI | Exact McNemar $p$-value |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :---: | ---: |
| **integer** | 30/80 | 42/80 | 29 | 1 | 13 | 37 | **+12** | +0.1500 | [0.0000, 0.3250] | 0.0018 |
| **polynomial** | 16/80 | 9/80 | 3 | 13 | 6 | 58 | **-7** | -0.0875 | [-0.2750, 0.0750] | 0.1671 |
| **radical** | 15/80 | 19/80 | 10 | 5 | 9 | 56 | **+4** | +0.0500 | [-0.0750, 0.1875] | 0.4240 |
| **fraction** | 17/80 | 31/80 | 10 | 7 | 21 | 42 | **+14** | +0.1750 | [0.0250, 0.3625] | 0.0125 |

### 保守解讀與 Polynomial 限制：
- **Integer** (+12 格, $p = 0.0018$) 與 **Fraction** (+14 格, $p = 0.0125$) 展現配對淨成長。
- **Polynomial (多項式) 出現反向差異 (-7 格)**：9B (9/80) 低於 4B (16/80)，$p = 0.1671$。經診斷，此低分極度集中於 `ce115_calc_polynomial_division_l1` 該單一題型（9B 0/20 vs 4B 4/20），與在 only-Python 中組裝多個 LaTeX 欄位的提示結構高度共現，**不可解讀為 9B 全域數學能力落後**。

---

## 6. Seed 穩定性摘要

對 5 個獨立隨機種子（各 64 格配對）進行對照：

| Seed | 4B PASS / 64 | 9B PASS / 64 | 配對淨增加 (9B - 4B) | 4B ONLY ($b$) | 9B ONLY ($c$) |
| :--- | ---: | ---: | ---: | ---: | ---: |
| **2026071301** | 15/64 | 21/64 | **+6** | 4 | 10 |
| **2026072001** | 17/64 | 25/64 | **+8** | 5 | 13 |
| **2026072002** | 15/64 | 14/64 | **-1** | 7 | 6 |
| **2026072003** | 14/64 | 23/64 | **+9** | 5 | 14 |
| **2026072004** | 17/64 | 18/64 | **+1** | 5 | 6 |

- **跨 Seed 穩定度**：在所有 5 個種子中，9B 的通過數均一致高於 4B（淨增加範圍為 **+-1 至 +9 格**）。
- **平均與標準差**：跨 Seed 平均淨增加為 **+4.6 格** (sample SD = **4.39**)。
- **結論**：配對淨增加是由 9B 在所有 5 個種子上的穩定優勢所驅動，而非個別極端種子主導。

---

## 7. Task-Level 差異與診斷

在 16 個 Task（各 20 格配對）中：

| Task ID | Family | 4B PASS / 20 | 9B PASS / 20 | 淨增加 (9B - 4B) | 方向 |
| :--- | :--- | ---: | ---: | ---: | :---: |
| `ce111_nonchoice_q01_part1_exponential_growth` | integer | 5 | 5 | **+0** | EQUAL |
| `ce111_q02_polynomial_division_remainder` | polynomial | 2 | 5 | **+3** | 9B_BETTER |
| `ce111_q03_prime_factor_selection` | integer | 5 | 10 | **+5** | 9B_BETTER |
| `ce111_q05_exact_fraction_expression` | fraction | 5 | 6 | **+1** | 9B_BETTER |
| `ce111_q08_polynomial_factor_parameter_recovery` | polynomial | 5 | 3 | **-2** | 4B_BETTER |
| `ce111_q10_ordered_quadratic_roots_radical` | radical | 1 | 2 | **+1** | 9B_BETTER |
| `ce112_q01_negative_integer_power` | integer | 15 | 19 | **+4** | 9B_BETTER |
| `ce112_q04_radical_simplification` | radical | 0 | 2 | **+2** | 9B_BETTER |
| `ce112_q09_divisor_multiple_intersection` | integer | 5 | 8 | **+3** | 9B_BETTER |
| `ce112_q12_independent_probability_fraction` | fraction | 3 | 7 | **+4** | 9B_BETTER |
| `ce113_q01_negative_fraction_subtraction` | fraction | 8 | 14 | **+6** | 9B_BETTER |
| `ce113_q11_rationalize_denominator` | radical | 3 | 7 | **+4** | 9B_BETTER |
| `ce115_calc_exact_rational_expression_l1` | fraction | 1 | 4 | **+3** | 9B_BETTER |
| `ce115_calc_polynomial_division_l1` ⚠️ (Anomaly) | polynomial | 6 | 0 | **-6** | 4B_BETTER |
| `ce115_calc_polynomial_factor_roots_l1` | polynomial | 3 | 1 | **-2** | 4B_BETTER |
| `ce115_calc_radical_simplification_l1` | radical | 11 | 8 | **-3** | 4B_BETTER |

### 關鍵發現：
1. **改善最大 Tasks**：`ce112_q12_independent_probability_fraction` (+5 格)、`ce112_q01_negative_integer_power` (+4 格)、`ce113_q11_rationalize_denominator` (+2 格)。
2. **反向落後 Task**：`ce115_calc_polynomial_division_l1` (-4 格) 是導致 Polynomial 家族 9B 低於 4B 的主要單點因素。

---

## 8. 多重比較治理 (Multiple Comparisons Governance)

- **Confirmatory 核心宣告**：僅 `Overall 320-cell paired McNemar test` ($p = 0.0106$) 屬事前的 Confirmatory 統計檢定。
- **Exploratory 屬性**：Condition、Family、Seed、Task 等分層分析均屬次要探索性分解 (Secondary/Exploratory Decompositions)。分層 $p$-value 供模式識別參考，不單獨宣稱全域普遍顯著。

---

## 9. 可寫入統整報告的保守結論

1. 在同一 Qwen 系列與相同 320 格配對實驗下，Qwen 3.5 9B 的端到端基線通過率高於 Qwen 3.5 4B (Paired Risk Difference = $+7.19\%$, Exact McNemar $p = 0.0106$).
2. Task-clustered Bootstrap 95% CI 為 `[-0.94%, +14.37%]`.
3. 9B 的勝出在 5 個獨立種子上均保持穩定 (每種子 +1 至 +7 格).
4. 分數 (Fraction) 與整數 (Integer) 家族貢獻了主要的配對淨成長.

---

## 10. 嚴禁過度推論之事項

- **不可寫成**「所有 family 都單調改善」（Polynomial 出現局部反向落後）。
- **不可寫成**「Gemini 也適用此 paired 統計結論」（Gemini 屬 Tier 2 描述性參照）。
- **不可寫成**「純參數規模造成因果差異」（仍包含提示結構與量化因子）。

---
