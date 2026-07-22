# Script Logic & Data Sources Comparison

| 項目 | `analyze_math16_pilot02_qwen4b_vs_qwen9b_tier1_paired.py` | `audit_math16_pilot02_fraction_9b_only_pass.py` |
| :--- | :--- | :--- |
| **資料來源** | 讀取 4B/9B `cell_level_baseline.jsonl` 建立 `paired_cell_ledger.jsonl` | 讀取 `paired_cell_ledger.jsonl` 篩選 `pair_category == "NINE_B_ONLY_PASS"` |
| **Join Key** | `(task_id, condition, seed)` | `(task_id, condition, seed)` |
| **PASS 判定** | `final_status == "PASSED"` | `pair_category == "NINE_B_ONLY_PASS"` (4B=FAIL, 9B=PASS) |
| **Fraction 2x2 計數** | BOTH_PASS=10, FOUR_B_ONLY=7, NINE_B_ONLY=21, BOTH_FAIL=42 | NINE_B_ONLY ($c$) = 21, FOUR_B_ONLY ($b$) = 7, Net ($c-b$) = 14 |
| **邏輯一致性** | 兩腳本邏輯完全相同，判定標準 100% 一致。 | 兩腳本邏輯完全相同，判定標準 100% 一致。 |
