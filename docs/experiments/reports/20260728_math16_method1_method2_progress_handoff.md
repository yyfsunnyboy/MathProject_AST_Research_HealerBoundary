# Math16／HealerBoundary 工作進度交接

更新日期：2026-07-28

本文件彙整截至 2026-07-28 的 Method 1／Method 2 已完成進度與唯一下一步，供另一台電腦接續。

## 1. Method 1

- 40／120 split 已凍結。
- Development 40：11/40 → 11/40，rescue 0。
- Evaluation 120：33/120 → 37/120，rescue 4。
- 敏感度 70：21/70 → 21/70，rescue 0。
- 官方 320（凍結管線歷史輸出，永久不變）：Baseline 78/320；Primary 83/320；corrected-chain 84/320。
- 官方 320（分析/報告層更正後，見第 5 節 Correction Note）：Baseline 79/320；Primary 84/320（歷史中繼值，demoted）；corrected-chain Final 85/320；rescue 維持 6 格。
- Method 1 Regression：not measured。

## 2. Method 2

- All-cell eligibility-first protocol 已凍結。
- 320/320 全部進 Eligibility。
- Eligible 11、source changed 11、noneligible 309。
- Raw PASS：79/320。
- Final PASS：85/320。
- Verified rescue：6。
- Regression：0。
- Preserved pass：79。
- Still failed：235。
- Phase B journal SHA-256：`5d11fb404930c5387f0f91b7dcc69c621ef477f4a22d0419a8afe2493068ae52`。
- Method 2 之 Raw／Final 數字為既有正式凍結證據，不受 Method 1 Baseline 更正影響；更正後 Method 1 Baseline 79/320 與 Method 2 Raw PASS 79/320 一致。

## 3. 已完成正式文件

- [`math16_method1_40_120_split_results_report_v1.md`](math16_method1_40_120_split_results_report_v1.md)
- [`math16_method2_all_cell_results_report_v1.md`](math16_method2_all_cell_results_report_v1.md)
- [`01_math16_pilot02_final_report_v13.md`](../../決賽文件/實驗結果文件/20260724_Math16/01_math16_pilot02_final_report_v13.md)
- [`math16_baseline_correction_note_v1.md`](math16_baseline_correction_note_v1.md)（正式 Correction Note）
- [`math16_method1_method2_78_79_discrepancy_audit_v1.md`](math16_method1_method2_78_79_discrepancy_audit_v1.md)（差異 Audit）
- [`math16_baseline_79_amendment_decision_record_v1.md`](math16_baseline_79_amendment_decision_record_v1.md)（Tier 1 統計重算決策紀錄）

對應 repo 路徑：

- `docs/experiments/reports/math16_method1_40_120_split_results_report_v1.md`
- `docs/experiments/reports/math16_method2_all_cell_results_report_v1.md`
- `docs/決賽文件/實驗結果文件/20260724_Math16/01_math16_pilot02_final_report_v13.md`
- `docs/experiments/reports/math16_baseline_correction_note_v1.md`
- `docs/experiments/reports/math16_method1_method2_78_79_discrepancy_audit_v1.md`
- `docs/experiments/reports/math16_baseline_79_amendment_decision_record_v1.md`

## 4. Git 里程碑

- `69ed9d5f`：freeze Method 2 protocol。
- `69438baf`：Phase A。
- `dc7a5597`：Phase B。
- `f829eb21`：Method 2 report + regression correction。

## 5. Baseline 78 vs 79 差異 — 已透過 Audit 與 Correction Note 解決（RESOLVED）

原列於本節之「唯一下一步」（執行只讀 audit，釐清 Method 1 Baseline 78/320 與 Method 2 Raw 79/320 的差異）已完成並正式結案，狀態由「待處理」更新為「已結案」。

- **Audit 結果**：[`math16_method1_method2_78_79_discrepancy_audit_v1.md`](math16_method1_method2_78_79_discrepancy_audit_v1.md)——全 320 格逐格比對僅發現 1 格不一致，含 raw-source 位元組同一性檢查、Evaluator 同一性檢查、root cause 追溯，以及 Section 10 全 320 格 closure sweep 與零 LLM/Healer 呼叫之 confirmatory re-evaluation。
- **正式更正紀錄**：[`math16_baseline_correction_note_v1.md`](math16_baseline_correction_note_v1.md)——採用之更正後數字：Baseline 79/320、corrected-chain Final 85/320、rescue 6（不變）。
- **統計重算決策紀錄**：[`math16_baseline_79_amendment_decision_record_v1.md`](math16_baseline_79_amendment_decision_record_v1.md)——Tier 1（Qwen 4B vs 9B）配對統計於更正後之重算結果，結論方向與顯著性判定均未反轉。
- **輔助證據**：[`math16_method1_method2_extraction_closure_320.csv`](math16_method1_method2_extraction_closure_320.csv)、[`math16_method1_method2_extraction_closure_summary_v1.json`](math16_method1_method2_extraction_closure_summary_v1.json)。
- **根因（簡述）**：Method 1 原始管線對單一 cell（`qwen3_5_4b__ce115_calc_polynomial_division_l1__ab1__seed_2026072003`）計算了兩個不同的 hash 欄位，實際評分所用之 `raw_artifact_sha256` 錨定到模型自身敘述文字中的偽 code fence，產生截斷、無法解析的候選程式（`catastrophic_truncation`）；Method 2 獨立重新擷取之 raw source 與 Method 1 自身已算出但未使用的 `candidate_hash` 位元組相同，在同一凍結 Evaluator 下可解析並 PASS。兩方法之 Evaluator、task、condition、seed 均相同，差異僅在候選程式擷取的 artifact 選取。
- **凍結證據處置**：凍結證據檔（結果／journal／manifest／pinned scripts／16 個 regression test 檔）保留歷史 78/83/84 數值，永不修改；本更正僅發生於分析/報告層。
- **本項目狀態：已結案（RESOLVED）**，無待處理之唯一下一步。

## 6. 呈現順序附註（如適用）

跨三模型呈現文件現採統一順序：**Gemini 3.5 Flash → Qwen 3.5 9B → Qwen 3.5 4B**（僅欄位/列序、圖例順序調整，不改變任何數值），詳見 [`math16_baseline_correction_note_v1.md`](math16_baseline_correction_note_v1.md) 第 10 節。本交接文件僅涉及 Method 1／Method 2（皆為 Qwen 3.5 4B 單模型分帳），不含三模型並列表格，故不受此順序規則影響；此處僅作交叉參照。
