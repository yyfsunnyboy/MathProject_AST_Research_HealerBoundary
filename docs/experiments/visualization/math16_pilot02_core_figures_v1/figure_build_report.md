# Math16 Pilot-02 核心圖表渲染建置報告 (Batch 01 Visual Hotfix v1)

```text
MATH16_PILOT02_BATCH01_VISUAL_HOTFIX_COMPLETED
FIGURE4_TITLE_OVERLAP_RESOLVED
FIGURE5_QWEN9B_BASELINE_VISIBLE
FIGURES1_AND3_SHA_PRESERVED
BATCH01_READY_FOR_PRESENTATION_USE
```

## 一、 摘要與 Hotfix 記錄 (Summary & Visual Hotfix Log)
本建置報告記錄「Ivan旺宏科學展」HealerBoundary 研究線第一批 4 張核心圖表 (Figure 1, 3, 4, 5) 之 Visual Hotfix v1 修復結果：
1. **Figure 4 標題重疊修復**: 移除了 `ax_mat.set_title` 與 `fig.suptitle` 重複層疊，統一為單一頂部主標題「`Qwen 4B與9B的320格配對結果`」，保留充分垂直間距。
2. **Figure 5 遮擋修復**: 將圖例移至繪圖區域右側外部 (`loc="upper left", bbox_to_anchor=(1.02, 1.0)`)，確保 Qwen 9B Baseline FAIL=219 長條與 `219` 數值標籤完整可見、零遮擋。
3. **SHA256 不變性保護**: Figure 1 與 Figure 3 未重新渲染，其 PNG 與 SVG 密碼學 Hash 保持 100% 相同。

## 二、 環境與字體 (Environment & Fonts)
* **Python Version**: `3.14.6`
* **Matplotlib Version**: `3.11.1`
* **Font Family**: `Microsoft JhengHei` (微軟正黑體, Native System Font)
* **Resolution**: 300 DPI (PNG) + SVG Vector Format

## 三、 產出圖表與密碼學 SHA-256 清單

| 圖表 ID | 中文名稱 | Hotfix 狀態 | PNG SHA-256 | SVG SHA-256 |
| :- | :--- | :--- | :--- | :--- |
| **Figure 1** | 三模型 Baseline 總覽 | Unchanged | `5bc0c714769c9877...` | `8a3cc1c8c9bbc407...` |
| **Figure 3** | 四 Family × Qwen 4B/9B | Unchanged | `f164edc807659c45...` | `8daf1901ca83b8f9...` |
| **Figure 4** | Tier 1 配對分析 | Hotfix Applied | `f18bbb774e9a75c5...` | `b1d19764e6f16079...` |
| **Figure 5** | Healer Eligibility/Rescue | Hotfix Applied | `5887f0b829797ab6...` | `45126972a0373fca...` |

## 四、 驗證規範 (Verification Checkpoints)
1. **Primary / Post-hoc 分帳**: Figure 5 中 Primary rescue = 5 (實體綠 Bar) 與 Post-hoc rescue = 6 (黃虛線 Overlay) 視覺清晰分開。
2. **統計指標完整性**: Figure 4 同時標記 Exact McNemar $p = 0.010582$ 與 Cluster Bootstrap 95% CI `[-0.94%, +14.38%]`.
3. **無過度宣稱**: 包含全部要求之警示註解 (Footnotes)。
