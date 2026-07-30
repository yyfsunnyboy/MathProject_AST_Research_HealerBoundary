# Math16 Pilot-02 交付文件與推薦閱讀順序指南 (Teacher Delivery Package & Reading Order)

**專案／研究線：** Ivan 旺宏科學展 —— HealerBoundary (`MathProject_AST_Research_HealerBoundary`)
**交付目錄：** `docs/決賽文件/實驗結果文件/20260724_Math16/`
**最後更新 UTC：** 2026-07-23

---

> **權威性交付聲明：** `20260724_Math16/` 為本研究唯一正式交付入口；`20260722_Math16/` 僅為 archived historical backup。正式報告、數字、圖表與口試依據均以 `20260724_Math16/` 為準。
>
> **Working mirror：** `docs/決賽文件/實驗結果文件/Math16/` 內同名 Final Report v1.3 為編輯工作副本（非第三份 Final Report）；A／B／C 等交付主張須同步回本目錄 canonical 正式研究報告。
>
> **Delivery Final Report SHA pin：** `FROZEN_SHA_FINAL_REPORT_V13_DELIVERY` 建立於 `e7cb0431`；自 `daeb581991` 合法正文更新後過期；後續更新已進 Git 但 pin 未同步。本次刷新僅對齊現行 canonical 正文，不回復舊版、不改寫 raw evidence。詳見 Correction Note §12。

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
| **`02_math16_pilot02_one_pager_v23.pdf`** | 簡報海報 | One-Pager 精華圖解 v2.3 | 高層次研究動機、核心發現 (Ab2d+spec-v2 80/80)、圖表集萃 |
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

1. **最終有效規格結果**：Gemini Math16 在 `Ab2d+spec-v2` 補齊 API 簽名卡後四條件 Pass 為 **306 / 320** (Ab1 72, Ab2g 76, Ab2d+api 78, Ab2d+spec-v2 80)。*Gemini 正式 Primary 採用 `Ab2d+spec-v1` 為 63/80，屬研究歷程。*
2. **Qwen 正式 Primary**：`Ab2d+spec-v2` 四條件中 4B 36/80、9B 40/80；Healer 使 4B 由 78/320 提升至 83/320（Primary）／84/320（Post-hoc）。
3. **Healer 救援數**：Gemini Cohort 為 **0**（Evaluator v4 修復假陰性 +24 屬評分契約修正，Spec-v2 +17 屬 Prompt/Spec 修補，皆非 Healer 算力介入）。



## 5. Healer 規則 Provenance Audit 對齊與雙層學術定位 (Provenance Alignment)

1. **規則凍結狀態 (`rule_freeze_status = PRE_FROZEN_UNCHANGED`)**：六條 Healer 規則及其適用條件均於正式 Math16 320-cell generation 前完成凍結 (d9aa264c)，且後續未修改 detector、eligibility、transform 或 activation scope。
2. **Primary 5 定位 (`validation_status = PROSPECTIVE_WITHIN_MATH16_COHORT`)**：Primary 帳目的 5 格救援屬於預先固定規則在 Math16 cohort 上的前瞻性評估結果；但因規則源自先期開發資料，且尚未在完全獨立資料集驗證 (independent_external_validation = false)，本研究不主張其為外部獨立確認性證據。
3. **Corrected 第 6 格定位 (POST_HOC_TECHNICAL_CORRECTION)**：第 6 格來自既有規則成功 transform 被 runner false-loop rollback 錯誤撤回後的技術修正。此修正未新增或修改 Healer 規則，不改變 PRE_FROZEN_UNCHANGED 狀態；但因屬正式結果揭露後的技術重算，只列入 Corrected technical account，不回寫 Primary。
4. **Payload Wrap 結構 (oracle_payload 內部包裝)**：single-key 指固定三欄回傳結構中 oracle_payload 欄位內部的唯一包裝鍵，不是最外層 return dict 只有一個鍵。Healer 不讀取 correct_answer，oracle_answer_used = false。此結果支持窄範圍、唯一、局部且離線可驗證的 deterministic repair candidate，不代表零副作用或一般語意安全保證。

- 權威 Provenance Audit 報告：docs/experiments/reports/math16_healer_rule_provenance_audit_v1.md (SHA256: 05a1ef08836e7f957cd0d4e87be9090d863b0c290474ae8b80bfd9ed4347bb4a)
- 權威 Provenance Audit Manifest：docs/experiments/reports/math16_healer_rule_provenance_audit_v1_manifest.json (SHA256: b882b4d31a61dbca8ab60622c75ecf82290223cdab3a816de7116e4bb515ecd5)
- 規則凍結 Commit：d9aa264c | 分類修正 Commit：97c4e985
