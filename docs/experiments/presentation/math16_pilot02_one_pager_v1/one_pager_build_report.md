# Math16 Pilot-02 Executive One-Pager v1 建置報告

```text
MATH16_PILOT02_ONE_PAGER_V1_COMPLETED
EXACTLY_FOUR_CORE_FIGURES_USED
EVIDENCE_COMPLETE_VALUES_PRESERVED
PRIMARY_POSTHOC_ACCOUNTING_PRESERVED
ONE_PAGER_READY_FOR_REVIEW
```

## 一、 摘要

本報告記錄「Ivan旺宏科學展」HealerBoundary 研究線 Math16 Pilot-02 Executive One-Pager v1 的建置過程。
格式：A4 橫式（297 mm × 210 mm），嚴格單頁，共嵌入 4 張核心圖（Fig 1, 3, 4, 5）。

## 二、 版面結構

| 區域 | 內容 |
|---|---|
| 上方 | 主標題、研究問題（三欄）、實驗設計、核心結果 |
| 中段左上 | Figure 1：三模型 Baseline 通過率 |
| 中段右上 | Figure 3：四 Family × Qwen 4B/9B |
| 中段左下 | Figure 4：Tier 1 配對分析（McNemar p, Bootstrap CI） |
| 中段右下 | Figure 5：Healer Eligibility/Rescue 邊界 |
| 下方 | 5點結論、統計摘要（含 Primary/Post-hoc 分帳警示） |

## 三、 數字來源

所有數字嚴格抽自 `frozen_numeric_claims.json`（SHA: `b93faea5c323d2a4...`）。

## 四、 來源圖表 SHA 驗證

| 圖表 | PNG SHA-256 | 狀態 |
|---|---|---|
| Figure 1 | `5bc0c714769c9877...` | ✅ 未變動 |
| Figure 3 | `f164edc807659c45...` | ✅ 未變動 |
| Figure 4 | `f18bbb774e9a75c5...` | ✅ 未變動 |
| Figure 5 | `5887f0b829797ab6...` | ✅ 未變動 |

## 五、 輸出 SHA-256

| 檔案 | SHA-256 |
|---|---|
| `math16_pilot02_one_pager_v1.png` | `1998988aabcb0b61e37c257e51e35008db56ab51abe0e43540789355cbb8d234` |
| `math16_pilot02_one_pager_v1.pdf` | `adc5b870cdcdbd7595dbcaa79efb44b08423196893bd544f3ab10d18d262cd21` |

## 六、 Primary / Post-hoc 分帳

- **4B Primary Healer 救回 5 格** → 83/320 (25.94%)（正式 Primary 結果）
- **4B Post-hoc 驗證救回 6 格** → 84/320（事後機制驗證，非 Primary 正式數字）
- **Gemini Eligible=0 / 9B Eligible=0 / Regression=0**（本次320格觀察）

## 七、 統計摘要

- Exact McNemar p = **0.010582**
- Task-clustered Bootstrap 95% CI = **[-0.94%, +14.38%]**
- 9B-only=49格，4B-only=26格，Net=+23格，Paired Risk Diff=+7.19%

## 八、 禁止事項確認

- 不含 Figure 2 / Figure 6
- 不含 Poster 或 Oral Slides
- Evidence Complete / Q&A / Figure Spec / 六張核心圖原始檔未修改
