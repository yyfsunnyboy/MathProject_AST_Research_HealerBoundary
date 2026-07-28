# Math16／HealerBoundary 工作進度交接

更新日期：2026-07-28

本文件彙整截至 2026-07-28 的 Method 1／Method 2 已完成進度與唯一下一步，供另一台電腦接續。

## 1. Method 1

- 40／120 split 已凍結。
- Development 40：11/40 → 11/40，rescue 0。
- Evaluation 120：33/120 → 37/120，rescue 4。
- 敏感度 70：21/70 → 21/70，rescue 0。
- 官方 320：Baseline 78/320。
- Primary：83/320。
- Corrected-chain：84/320。
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

## 3. 已完成正式文件

- [`math16_method1_40_120_split_results_report_v1.md`](math16_method1_40_120_split_results_report_v1.md)
- [`math16_method2_all_cell_results_report_v1.md`](math16_method2_all_cell_results_report_v1.md)
- [`01_math16_pilot02_final_report_v13.md`](../../決賽文件/實驗結果文件/20260724_Math16/01_math16_pilot02_final_report_v13.md)

對應 repo 路徑：

- `docs/experiments/reports/math16_method1_40_120_split_results_report_v1.md`
- `docs/experiments/reports/math16_method2_all_cell_results_report_v1.md`
- `docs/決賽文件/實驗結果文件/20260724_Math16/01_math16_pilot02_final_report_v13.md`

## 4. Git 里程碑

- `69ed9d5f`：freeze Method 2 protocol。
- `69438baf`：Phase A。
- `dc7a5597`：Phase B。
- `f829eb21`：Method 2 report + regression correction。

## 5. 尚未處理的唯一下一步

執行只讀 audit，釐清 Method 1 Baseline 78/320 與 Method 2 Raw 79/320 的差異。

Audit 限制：

- 不得先改數字、規則、Evaluator 或結果。
- Audit 前不得宣稱兩者是完全相同 pipeline 的直接重現。
- 先保存兩種方法各自既有正式分帳，再以只讀證據定位 1 格差異來源。
