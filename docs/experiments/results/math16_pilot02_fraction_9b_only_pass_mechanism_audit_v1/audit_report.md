# Math16 Pilot-02 Fraction Family 9B-Only Pass 機制分布診斷報告

```text
MATH16_PILOT02_FRACTION_9B_ONLY_PASS_AUDIT_COMPLETED
FRACTION_GAP_MECHANISM_DISTRIBUTION_DOCUMENTED
CATEGORY_A_COMPLETED_WITH_INTERPRETATION_LIMITATIONS
```

**診斷識別碼：** `math16_pilot02_fraction_9b_only_pass_mechanism_audit_v1`
**分析集合：** Tier 1 配對帳本中 Fraction 家族的 **21 個 `NINE_B_ONLY_PASS` cells** ($c=21$, $b=7$, 淨增加 $+14$ 格)
**主要 Verdict：** `FRACTION_GAP_MAINLY_FORMAT_EXECUTION_RELATED`
**集中度標籤：** `NO_SINGLE_DOMINATION`
**驗證狀態：** 100% 完整鎖定（無重複、無缺漏，4B 全部 FAIL，9B 全部 PASS）

---

## 1. 分析目的與配對計數說明

本診斷旨在回答：**「在 Tier 1 配對分析中，9B 在 Fraction 家族基線通過率顯著高於 4B（4B 17/80 vs 9B 31/80，淨增加 14 格）。在配對不一致矩陣中，$c=21$ 格為 9B 獨贏 (`NINE_B_ONLY_PASS`)，$b=7$ 格為 4B 獨贏 (`FOUR_B_ONLY_PASS`)，淨增加 $c - b = 14$ 格。這 21 格 4B 失敗/9B 成功案例集中在哪些 Task、Condition，以及 4B 對應的 Failure Layer 與 Mechanism 為何？」**

---

## 2. Task 分布 (Task Distribution)

21 格 `NINE_B_ONLY_PASS` 在 Fraction 家族 4 個 Tasks 中的分布如下：

| Task ID | 21格 Gap 數 ($c$) | 占 21 格比例 (%) | 4B PASS / 20 | 9B PASS / 20 | 配對淨增加 (9B - 4B) |
| :--- | ---: | ---: | ---: | ---: | ---: |
| `ce111_q05_exact_fraction_expression` | **5** | 23.81% | 5 | 6 | **+1** |
| `ce112_q12_independent_probability_fraction` | **4** | 19.05% | 3 | 7 | **+4** |
| `ce113_q01_negative_fraction_subtraction` | **9** | 42.86% | 8 | 14 | **+6** |
| `ce115_calc_exact_rational_expression_l1` | **3** | 14.29% | 1 | 4 | **+3** |

### 觀察與集中度：
- **最多差距 Task**：`ce113_q01_negative_fraction_subtraction` 占 **9 格 (42.86%)**。
- **次要差距 Task**：`ce111_q05_exact_fraction_expression` 占 **5 格 (23.81%)**、`ce112_q12_independent_probability_fraction` 占 **4 格 (19.05%)**、`ce115_calc_exact_rational_expression_l1` 占 **3 格 (14.29%)**。
- **Task 集中度判斷**：最大單一 Task (42.86%) 未達 50%，差距廣泛分散於多個分數題型。

---

## 3. Condition 分布 (Condition Distribution)

21 格 `NINE_B_ONLY_PASS` 在 4 種 Prompt 條件中的分布如下：

| Prompt 條件 | 21格 Gap 數 ($c$) | 占 21 格比例 (%) |
| :--- | ---: | ---: |
| **ab1** | **4** | 19.05% |
| **ab2g** | **7** | 33.33% |
| **ab2d** | **3** | 14.29% |
| **ab2d_spec_v2** | **7** | 33.33% |

### 觀察與集中度：
- `Ab2g` 與 `Ab2d+spec-v2` 各占 **7 格 (33.33%)**，合計占 **66.67%**。
- `Ab1` 占 **4 格 (19.05%)**。
- `Ab2d+api` 僅占 **3 格 (14.29%)**。
- **Condition 集中度判斷**：差距分散於各種 Prompt 條件，**非由 Ab2d+api 條件主導**（Ab2d+api 僅占 14.29%）。

---

## 4. 4B Failure Layer 分布 (4B Failure Layer Distribution)

對這 21 格中 Qwen 4B 原先失敗的 Failure Layer 統計如下：

| Layer 層級 | 定義 | 4B 失敗格數 | 占 21 格比例 (%) |
| :--- | :--- | ---: | ---: |
| **L1** | Syntax / Parse Failure | **10** | 47.62% |
| **L2** | Contract / Entry Point Failure | **2** | 9.52% |
| **L3** | Domain-API Misuse | **1** | 4.76% |
| **L4** | Runtime Execution Exception | **2** | 9.52% |
| **L5** | Semantic / Algorithmic Error | **6** | 28.57% |

### 主要結構：
- **L1 至 L4 (格式與執行層級失敗)**：合計 **15 格 (71.43%)**。
- **L5 (演算法/語義層級失敗)**：合計 **6 格 (28.57%)**。

---

## 5. 4B Mechanism 分布 (4B Mechanism Tags Distribution)

對這 21 格中 Qwen 4B 的正式 Mechanism 標籤統計如下：

| Mechanism Tag | 4B 標籤出現數 | 占 21 格比例 (%) |
| :--- | ---: | ---: |
| `algorithmic_error` | **6** | 28.57% |
| `format_contamination` | **10** | 47.62% |
| `invalid_api_call` | **1** | 4.76% |
| `output_packaging` | **2** | 9.52% |
| `schema_mismatch` | **2** | 9.52% |
| `control_flow_failure` | **2** | 9.52% |

---

## 6. 與既有 4B Ab2d+api 27格診斷之交集

- 21 格 gap 中，僅有 **1 格 (4.76%)** 落入既有的 Qwen 4B Ab2d+api 27 格診斷集合（`ce111_q05` 在 Ab2d 條件下的 2 個 Seed）。
- **方法學限制提示**：舊 27 格診斷顯示該 Ab2d 樣本中有 77.8% 屬 SyntaxError-in-extracted，**絕對不可將該 77.8% 比例外推至整體 21 格 Fraction gap**。

---

## 7. 保守研究結論與禁止過度主張

### 可寫入報告之描述性結論：
1. 9B 在 Fraction 家族的 21 格 `NINE_B_ONLY_PASS` 差距主要落在 4B 的 **FRACTION_GAP_MAINLY_FORMAT_EXECUTION_RELATED** 區域（L1~L4 格式與執行層級佔 71.43%）。
2. 差距廣泛分散於多個 Fraction 題型與各種 Prompt 條件，**非單一 Task 或 Ab2d+api 所獨佔**。
3. 9B 在 Fraction 家族展現了跨題型與跨 Prompt 條件的穩定累積優勢。

### 嚴禁過度推論事項：
- **不可寫成**「9B 比較會做分數題」（包含語法、包裝與 API 呼叫等工程因子）。
- **不可寫成**「4B Fraction 差距是由 Parser 造成」或「格式問題導致整體差距」。
- **不可寫成**「Ab2d+api 是造成差距的因果主因」。
- **不可寫成**「$p = 0.0001$ 證明了純數學能力差異」。

---
*本報告完全由 `scripts/audit_math16_pilot02_fraction_9b_only_pass.py` 從凍結數據程式化產出。*
