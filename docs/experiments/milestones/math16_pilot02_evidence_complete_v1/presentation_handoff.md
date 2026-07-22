# Math16 Pilot-02 呈現層交接規範 (Presentation Handoff Specification v1)

```text
PRESENTATION_HANDOFF_SPEC_V1_FROZEN
EVIDENCE_COMPLETE_V1_LOCKED
PRESENTATION_ONLY_PHASE_OPENED
NO_SILENT_DATA_MUTATION_PERMITTED
```

## 一、 交接背景與目的

本文件為 **Math16 Pilot-02 Evidence Complete Milestone v1** 之正式呈現層交接規範。
自本里程碑凍結起，正式研究數據、統計檢定、Q&A 文字與 Healer 邊界結論全面鎖定。研究流程正式由「數據分析與驗證階段」過渡至「 presentation-only 視覺與呈現製作階段」。

---

## 二、 允許與禁止修改範圍 (Permitted vs Forbidden Edits)

### 1. 此里程碑之後允許修改 (Permitted Edits)
- 圖表視覺樣式、字體大小、顏色主題與圖例佈局。
- 展板 (Poster) 與簡報 (Oral Slides) 之美工設計、區塊對齊與背景繪製。
- Executive One-Pager 之排版、文句潤飾與排版優化。
- 圖說 (Captions) 之口語化微調或字數壓縮（須保持與 Ground Truth 一致）。
- 競賽成果報告書之章節排版、目錄與附錄編排。

### 2. 此里程碑之後嚴格禁止直接修改 (Forbidden Edits)
- **嚴禁修改任何正式 Baseline 通過數與通過率** (Gemini 289, Qwen 4B 78, Qwen 9B 101)。
- **嚴禁修改 2x2 配對聯表數字** (BOTH_PASS 52, 4B_ONLY 26, 9B_ONLY 49, BOTH_FAIL 193)。
- **嚴禁修改任何 $p$-value 或 Confidence Interval** (Exact McNemar $p=0.010582$, Bootstrap 95% CI `[-0.94%, +14.38%]`)。
- **嚴禁修改 Eligibility 與 Rescue 數字** (4B Eligible 10, Primary rescue 5, Post-hoc rescue 6)。
- **嚴禁變更 Primary / Post-hoc 歸屬關係** (不得將 306 或 84 寫為 Primary)。
- **嚴禁修改失敗分類學 (Failure Taxonomy) 或異常診斷結論**。

---

## 三、 數據異常修訂程序 (Evidence Amendment Procedure)

若後續在製作呈現產物過程中發現正式數字或檔案存在疑義，**嚴禁靜默直接修改 v1 產物**。必須遵循以下標準修正程序：

1. **建立 Evidence Amendment 案號**（例如 `math16_pilot02_evidence_amendment_v2`）。
2. **明確標註受影響之源檔案、原數據與擬修正數據**。
3. **重新執行完整一致性與迴歸測試套件** (`pytest tests/`)。
4. **產出修訂說明檔並經團隊審查覆核後，始得更新版號**。
