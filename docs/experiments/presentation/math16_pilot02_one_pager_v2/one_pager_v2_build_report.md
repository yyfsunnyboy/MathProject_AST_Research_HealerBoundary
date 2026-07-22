# Math16 Pilot-02 Executive One-Pager v2 建置報告

```text
MATH16_PILOT02_ONE_PAGER_V2_REDESIGNED
TOP_TEXT_CLIPPING_RESOLVED
COMPACT_DERIVATIVE_FIGURES_CREATED
ORIGINAL_FIGURE_SHAS_PRESERVED
ONE_PAGER_V2_READY_FOR_REVIEW
```

## 一、v1 缺陷與 v2 修正

| v1 缺陷 | v2 修正 |
|---|---|
| 上方三欄多行框文字被裁切覆蓋 | 改為深色標題帶 + 三張數字卡（單行資訊）|
| 原始 PNG 壓入 2×2 造成圖形扁 | 重新繪製 compact 衍生圖，正確比例 |
| Figure 4/5 資訊密度等尺寸塞入 | 非對稱版面：Fig4 佔左 55%，Fig1/3/5 疊右 45% |
| 下方文字超頁 | 嚴格 3點結論 + 1 行統計摘要 ≤ 6 行 |

## 二、版面結構

| 區域 | 高度% | 內容 |
|---|---|---|
| Header | 24% | 白字標題 + 研究問題 + 實驗設計 + 3 數字卡 |
| Figure area | 57% | 左：Fig4 compact；右疊：Fig1/Fig3/Fig5 |
| Bottom | 19% | 3點結論 + 統計摘要框 |

## 三、來源 SHA 驗證

| 檔案 | SHA-256 (前16碼) | 狀態 |
|---|---|---|
| figure_01_baseline_overall.png | `5bc0c714769c9877...` | ✅ 未動 |
| figure_03_family_breakdown.png | `f164edc807659c45...` | ✅ 未動 |
| figure_04_tier1_paired_analysis.png | `f18bbb774e9a75c5...` | ✅ 未動 |
| figure_05_healer_eligibility_boundary.png | `5887f0b829797ab6...` | ✅ 未動 |

## 四、Compact 衍生圖 SHA

| 檔案 | SHA-256 |
|---|---|
| fig1_compact.png | `eef6f46f8272cf32f13e44d93db2d680b120176b42b9bd97817779710b99c1ab` |
| fig3_compact.png | `480f3ce9c8fbb6627b45780fae04c9fc17bdcd42fea9591055b5aa332c0acef3` |
| fig4_compact.png | `0ec651c30ec9473cadebf58b845265dc4cbd25ee2bc82cefd151abb6d115bec3` |
| fig5_compact.png | `261fa5acfc912ac7bd1a7e46dd8223a500ece5f5ddb392ce83f52f815b9721cc` |

## 五、輸出 SHA

| 檔案 | SHA-256 |
|---|---|
| math16_pilot02_one_pager_v2.png | `7e582554e2a1c2e27aa86199ec759f583fcd498e6fd6a1bd9ef9da50467fbefc` |
| math16_pilot02_one_pager_v2.pdf | `4fb1443d8e10b3abe74fc06d99e04356e940be38b57ed9de20b0fb65e46ae2d7` |

## 六、Primary/Post-hoc 分帳

- Primary rescue = **5格 → 83/320** (正式 Primary 結果)
- Post-hoc rescue = **6格 → 84/320** (事後機制驗證，非 Primary)
- Gemini Eligible=0 / 9B Eligible=0 / Regression=0 (本次觀察)

## 七、統計

- McNemar p = **0.010582**
- Task-clustered Bootstrap 95% CI = **[-0.94%, +14.38%]**
- 9B-only=49格，4B-only=26格，Net=+23格
