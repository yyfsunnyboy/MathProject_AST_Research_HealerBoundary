# Math16 Pilot-02 交付文件與推薦閱讀順序指南 (Teacher Delivery Package & Reading Order)

**專案／研究線：** Ivan 旺宏科學展 —— HealerBoundary (`MathProject_AST_Research_HealerBoundary`)
**交付目錄：** `docs/決賽文件/實驗結果文件/20260722_Math16/`
**最後更新 UTC：** 2026-07-23

---

## 1. 建議評審／老師閱讀順序 (Recommended Reading Sequence)

為便於老師與評審循序漸進理解本研究之核心貢獻、實驗設計、數據對決與理論邊界，請依下列 **5 大主要入口** 之固定順序查閱：

```text
  【第 1 步】 02_math16_pilot02_one_pager_v23.pdf  (一頁精華圖解：秒懂研究動機與320格結果)
       ↓
  【第 2 步】 03_math16_pilot02_poster_v11.pdf     (海報展示：看清四條件、三大家族與Healer邊界)
       ↓
  【第 3 步】 01_math16_pilot02_final_report_v13.md (正式研究報告：完整論文級別細節與數據分帳)
       ↓
  【第 4 步】 05_math16_pilot02_appendices_v1.md   (附錄總冊：彙整 A救援機制 / B壓力測試 / C題目Prompt)
       ↓
  【第 5 步】 04_math16_pilot02_jury_qa_final_v1.md (評審答辯 Q&A：19 題高頻質疑攻防處置)
```

---

## 2. 5 大主要入口目錄說明 (Five Primary Entry Points)

| 入口檔名 | 檔案類型 | 功能說明 | 核心展示內容 |
|---|---|---|---|
| **`01_math16_pilot02_final_report_v13.md`** | 論文報告 | 正式完整研究報告 v1.3 | 完整背景、320-cell 矩陣對決、4 條件/3 家族分析、Healer 邊界、限制與結論 |
| **`02_math16_pilot02_one_pager_v23.pdf`** | 簡報海報 | One-Pager 精華圖解 v2.3 | 高層次研究動機、核心發現 (289/320 vs 80/80)、圖表集萃 |
| **`03_math16_pilot02_poster_v11.pdf`** | 展示海報 | 口頭簡報海報 v1.1 | 視覺化流程圖、家族表現柱狀圖、Healer 救援機制運作邏輯 |
| **`04_math16_pilot02_jury_qa_final_v1.md`** | 答辯文件 | Jury Q&A 攻防手冊 v1.0 | 收錄 19 題評審關鍵質疑 (如 289 vs 306 說法、Healer 0 救回原因、Evaluator v4 假陰性修復) |
| **`05_math16_pilot02_appendices_v1.md`** | 附錄總冊 | 附錄 A+B+C 總冊 v1.0 | 附錄 A (六格救援驗證)、附錄 B (Eligibility 與壓力測試)、附錄 C (16 題題目與 64 Prompt) |

---

## 3. 輔助資源與歸檔資料夾 (Supporting Assets & Archive)

- **`supporting_assets/`**:
  - `07_core_figures_v1/`: 包含 One-Pager 與 Poster 用之核心高清渲染圖片。
- **`archive_or_working_notes/`**:
  - `04_math16_pilot02_final_result_interpretation.md`: 原始結果詮釋工作筆記 (已無孤兒內容，可查閱歷史推導)。
  - `05_math16_pilot02_integrated_results_report_v1.md`: 原始整合報告草稿 (已完全收斂至 Final Report v1.3)。

---

## 4. 數據誠信與嚴格對齊聲明 (Data Integrity & Boundary Statement)

1. **正式 Primary 對決**：Gemini Math16 四條件 Pass 為 **289 / 320** (Ab1 72, Ab2g 76, Ab2d+api 78, Ab2d+spec-v1 63)。
2. **Post-hoc 驗證**：Ab2d+spec-v2 補齊 API 檔案卡後為 **80 / 80 (+17)**，Hybrid Inventory 為 **306 / 320**（僅作機制驗證，不取代 Primary 計分）。
3. **Healer 救援數**：Gemini Cohort 為 **0**（Evaluator v4 修復假陰性 +24 屬評分契約修正，Spec-v2 +17 屬 Prompt/Spec 修補，皆非 Healer 算力介入）。
