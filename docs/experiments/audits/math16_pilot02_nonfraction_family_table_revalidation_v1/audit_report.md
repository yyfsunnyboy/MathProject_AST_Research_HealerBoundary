# Math16 Pilot-02 四大 Family 配對四格表全量覆核與閉合驗證報告

```text
MATH16_PILOT02_ALL_FAMILY_TABLES_REVALIDATED
INTEGER_POLYNOMIAL_RADICAL_TABLES_CONFIRMED
FAMILY_TO_OVERALL_CLOSURE_CONFIRMED
TIER1_STATISTICS_REVALIDATED
CATEGORY_A_COMPLETED_WITH_INTERPRETATION_LIMITATIONS
```

**診斷識別碼：** `math16_pilot02_nonfraction_family_table_revalidation_v1`
**驗證結果：** 100% 完全對齊（四大 Family 原始 Baseline Rebuild、Tier 1 Paired Ledger 與 Summary JSON 之間 **0 筆差異**）
**Family-to-Overall 4-Cell 閉合驗證：** $52 + 26 + 49 + 193 = \mathbf{320}$ 格配對 100% 精確閉合！

---

## 1. 四大 Family 地面真值 2×2 配對列聯表

| Family | 4B PASS | 9B PASS | BOTH PASS ($a$) | 4B ONLY ($b$) | 9B ONLY ($c$) | BOTH FAIL ($d$) | 淨增加 ($c-b$) | Paired RD (\Delta) | Exact McNemar $p$-value | Matched-Pairs OR |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Integer** | 30/80 | 42/80 | **29** | **1** | **13** | **37** | **+12** | +0.1500 | **0.001831** | **13.00** |
| **Polynomial** | 16/80 | 9/80 | **3** | **13** | **6** | **58** | **-7** | -0.0875 | **0.167089** | **0.46** |
| **Radical** | 15/80 | 19/80 | **10** | **5** | **9** | **56** | **+4** | +0.0500 | **0.423950** | **1.80** |
| **Fraction** | 17/80 | 31/80 | **10** | **7** | **21** | **42** | **+14** | +0.1750 | **0.012541** | **3.00** |
| **合計 (Closure)** | **78/320** | **101/320** | **52** | **26** | **49** | **193** | **+23** | **+0.0719** | **0.010582** | **1.88** |

---

## 2. Family-to-Overall 4-Cell 閉合點交 audit

- **BOTH_PASS 總和**：$29 + 3 + 10 + 10 = \mathbf{52}$ (與 Overall 52 格 100% 精確相等)
- **FOUR_B_ONLY_PASS 總和**：$1 + 13 + 5 + 7 = \mathbf{26}$ (與 Overall 26 格 100% 精確相等)
- **NINE_B_ONLY_PASS 總和**：$13 + 6 + 9 + 21 = \mathbf{49}$ (與 Overall 49 格 100% 精確相等)
- **BOTH_FAIL 總和**：$37 + 58 + 56 + 42 = \mathbf{193}$ (與 Overall 193 格 100% 精確相等)

**結論**：四大 Family 的 4 格列聯表完全閉合，無任何邏輯漏失或加總偏離。

---

## 3. 治理與狀態宣告

- 四大 Family 的全量配對四格表已由原始 Baseline 獨立 Rebuild 重建驗證完畢。
- Tier 1 統計數字、Condition / Seed 分層與 Overall 統計 100% 精確無誤。
- Category A 最終狀態正式確認標記：**`CATEGORY_A_COMPLETED_WITH_INTERPRETATION_LIMITATIONS`**。

---
*本報告完全由 `scripts\revalidate_math16_pilot02_nonfraction_family_tables.py` 從凍結數據程式化產出。*
