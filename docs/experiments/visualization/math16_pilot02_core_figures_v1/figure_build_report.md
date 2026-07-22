# Math16 Pilot-02 核心圖表渲染建置報告 (Batch 01 Report v1)

```text
MATH16_PILOT02_CORE_FIGURES_BATCH01_RENDERED
FIGURES_1_3_4_5_COMPLETED
EVIDENCE_COMPLETE_VALUES_PRESERVED
PRIMARY_POSTHOC_VISUAL_ACCOUNTING_PRESERVED
ONE_PAGER_CORE_VISUALS_READY
```

## 一、 摘要 (Summary)
本建置報告記錄「Ivan旺宏科學展」HealerBoundary 研究線第一批 4 張核心圖表 (Figure 1, 3, 4, 5) 之實體渲染產出結果。
所有數據嚴格抽自已凍結之 **Evidence Complete Milestone v1** (`frozen_numeric_claims.json`)，無手抄或重新計算。

## 二、 環境與字體 (Environment & Fonts)
* **Python Version**: `3.14.6`
* **Matplotlib Version**: `3.11.1`
* **Font Family**: `Microsoft JhengHei` (微軟正黑體, Native System Font)
* **Resolution**: 300 DPI (PNG) + SVG Vector Format

## 三、 產出圖表與密碼學 SHA-256 清單

| 圖表 ID | 中文名稱 | PNG 檔名 | PNG SHA-256 | SVG 檔名 |
| :- | :--- | :--- | :--- | :--- |
| **Figure 1** | 三模型 Baseline 總覽 | `figure_01_baseline_overall.png` | `5bc0c714769c9877...` | `figure_01_baseline_overall.svg` |
| **Figure 3** | 四 Family × Qwen 4B/9B | `figure_03_family_breakdown.png` | `f164edc807659c45...` | `figure_03_family_breakdown.svg` |
| **Figure 4** | Tier 1 配對分析 | `figure_04_tier1_paired_analysis.png` | `33f024d104671995...` | `figure_04_tier1_paired_analysis.svg` |
| **Figure 5** | Healer Eligibility/Rescue | `figure_05_healer_eligibility_boundary.png` | `6aa7d30ee99c5a37...` | `figure_05_healer_eligibility_boundary.svg` |

## 四、 驗證規範 (Verification Checkpoints)
1. **Primary / Post-hoc 分帳**: Figure 5 中 Primary rescue = 5 (實體綠 Bar) 與 Post-hoc rescue = 6 (黃虛線 Overlay) 視覺清晰分開。
2. **統計指標完整性**: Figure 4 同時標記 Exact McNemar $p = 0.010582$ 與 Cluster Bootstrap 95% CI `[-0.94%, +14.38%]`.
3. **無過度宣稱**: 包含全部要求之警示註解 (Footnotes)。
