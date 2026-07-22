# Math16 Pilot-02 Fraction Family 配對計數對帳與對齊報告

```text
MATH16_PILOT02_FRACTION_PAIR_CONFLICT_RECONCILED
FRACTION_DISCORDANT_COUNTS_CORRECTED
TIER1_STATISTICS_REVALIDATED
CATEGORY_A_COMPLETED_WITH_INTERPRETATION_LIMITATIONS
```

**診斷識別碼：** `math16_pilot02_fraction_pair_reconciliation_v1`
**對帳結果：** 100% 完整對齊（Ground truth、Tier 1 paired ledger 與 Fraction audit ledger 之間 **0 筆差異**）
**地面真值 Fraction 2×2 列聯表：**
- `BOTH_PASS` ($a$): **10 格**
- `FOUR_B_ONLY_PASS` ($b$): **7 格**
- `NINE_B_ONLY_PASS` ($c$): **21 格**
- `BOTH_FAIL` ($d$): **42 格**
- **4B PASS 總數**：$10 + 7 = \mathbf{17}$ 格 (17/80, 21.25%)
- **9B PASS 總數**：$10 + 21 = \mathbf{31}$ 格 (31/80, 38.75%)
- **配對淨增加 ($c - b$)**：$21 - 7 = \mathbf{+14}$ 格 (Paired RD = $+17.50\%$)
- **Exact Two-Sided McNemar Test $p$-value**：$p = \mathbf{0.012541}$ ($p = 0.0125 < 0.05$)

---

## 1. 對帳背景與疑慮釐清

對帳核實發現：
1. 本專案 Repo 中所有既有產物（包括 `paired_cell_ledger.jsonl`、`family_paired_summary.json`、`fraction_9b_only_pass_ledger.jsonl` 以及 `integrated_results_report_v1.md`）從始至終均統一使用地面真值 **$b=7, c=21, c-b=14$**。
2. 疑慮中提及的 `4B_ONLY=0, 9B_ONLY=14` 係將**配對淨增加 (+14 格)** 誤解為單向獨勝數 ($c$) 所致。
3. 直接從原始 4B 與 9B `cell_level_baseline.jsonl` 進行獨立 Rebuild 重建，完全證實 Fraction 家族的不一致配對精確為 **$b=7$ 格** 與 **$c=21$ 格**，無任何數據矛盾。

---

## 2. 三方集合對帳結果 (3-Way Set Reconciliation)

對帳比對 3 個來源之 Fraction 配對分類集合：
1. **Rebuilt Ground-Truth Set**（從 raw baseline 獨立 Join）
2. **Tier 1 Paired Ledger Set** (`docs/experiments/results/math16_pilot02_qwen4b_vs_qwen9b_tier1_paired_analysis_v1/`)
3. **Fraction Audit Ledger Set** (`docs/experiments/results/math16_pilot02_fraction_9b_only_pass_mechanism_audit_v1/`)

### 比對結果：
- **`FOUR_B_ONLY_PASS` (7 格) 集合差異**：`0` 筆。
- **`NINE_B_ONLY_PASS` (21 格) 集合差異**：`0` 筆。
- **`BOTH_PASS` (10 格) 集合差異**：`0` 筆。
- **`BOTH_FAIL` (42 格) 集合差異**：`0` 筆。
- **結論**：三個資料來源 100% 完全相同，無任何衝突或失真。

---

## 3. 7 格 `FOUR_B_ONLY_PASS` 細胞詳細對帳

地面真值證實 4B 獨勝、9B 失敗的 7 格配對如下：

1. `ce111_q05_exact_fraction_expression__ab1__seed_2026072003`
2. `ce111_q05_exact_fraction_expression__ab2d__seed_2026072001`
3. `ce111_q05_exact_fraction_expression__ab2g__seed_2026071301`
4. `ce111_q05_exact_fraction_expression__ab2g__seed_2026072002`
5. `ce113_q01_negative_fraction_subtraction__ab2d__seed_2026072002`
6. `ce113_q01_negative_fraction_subtraction__ab2d_spec_v2__seed_2026072004`
7. `ce113_q01_negative_fraction_subtraction__ab2g__seed_2026072002`

此 7 格在 4B 中判定均為 `PASSED`，在 9B 中判定均為 `FAILED`。因為有這 7 格 4B 獨勝案例，故 9B 獨勝數 $c = 21$ 格減去 4B 獨勝數 $b = 7$ 格，得到淨增加 $c - b = 14$ 格。

---

## 4. 全局與其他分層影響檢查 (Global Revalidation)

- **Overall 320-cell 2×2 列聯表**：`BOTH_PASS=52`, `FOUR_B_ONLY=26`, `NINE_B_ONLY=49`, `BOTH_FAIL=193` ($p = 0.0106$). `[UNCHANGED & VERIFIED]`
- **Integer 家族 (80 cells)**：`BOTH_PASS=29`, `FOUR_B_ONLY=1`, `NINE_B_ONLY=13`, `BOTH_FAIL=37` (Net = $+12$, $p = 0.0018$). `[UNCHANGED & VERIFIED]`
- **Polynomial 家族 (80 cells)**：`BOTH_PASS=3`, `FOUR_B_ONLY=13`, `NINE_B_ONLY=6`, `BOTH_FAIL=58` (Net = $-7$, $p = 0.1671$). `[UNCHANGED & VERIFIED]`
- **Radical 家族 (80 cells)**：`BOTH_PASS=10`, `FOUR_B_ONLY=5`, `NINE_B_ONLY=9`, `BOTH_FAIL=56` (Net = $+4$, $p = 0.4240$). `[UNCHANGED & VERIFIED]`

---

## 5. 治理與狀態宣告

1. 配對衝突對帳完畢，確認 Repo 內數據完全一致無衝突。
2. 治理狀態恢復為：**`CATEGORY_A_COMPLETED_WITH_INTERPRETATION_LIMITATIONS`**。

---
*本報告完全由 `scripts\reconcile_math16_pilot02_fraction_pairs.py` 從凍結數據程式化產出。*
