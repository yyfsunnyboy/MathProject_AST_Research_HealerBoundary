# Math16 Pilot-02 — Working Mirror／編輯工作副本

**目錄：** `docs/決賽文件/實驗結果文件/Math16/`  
**狀態：** Working mirror（編輯工作副本；非第三份 Final Report）

---

## 1. 權威性聲明

| 目錄 | 角色 |
|---|---|
| **`20260724_Math16/`** | **Canonical 正式交付入口**（正式主報告、protected-SHA、老師／評審交付以該目錄為準） |
| **`Math16/`**（本目錄） | **Working mirror**：編輯與超前草稿；A／B／C 等交付主張必須同步回 `20260724_Math16/` |
| `20260722_Math16/` | 歷史快照（零修改、不作為現行入口） |

正式報告、數字、圖表與口試之 **authoritative 正文** 以 **`20260724_Math16/01_math16_pilot02_final_report_v13.md`** 為準（見 Baseline Correction Note §8）。本目錄 `01_…final_report_v13.md` **不是**第三份 Final Report，亦不得以本目錄覆寫 protected-SHA 交付指紋。

**本目錄未包含 Poster／PPT／oral 資產。**

---

## 2. 建議閱讀順序

1. [`01_math16_pilot02_final_report_v13.md`](01_math16_pilot02_final_report_v13.md) — 工作副本報告（同步前請先核對 canonical）
2. [`02_math16_pilot02_one_pager_v23.png`](02_math16_pilot02_one_pager_v23.png)／[`03_…pdf`](03_math16_pilot02_one_pager_v23.pdf) — 一頁精華
3. [`04_math16_pilot02_jury_qa_final_v1.md`](04_math16_pilot02_jury_qa_final_v1.md) — 評審 Q&A（含 Q21）
4. [`figures/`](figures/) — 核心圖表 Figure 1–6
5. [`05_math16_baseline_correction_note_v1.md`](05_math16_baseline_correction_note_v1.md) — Baseline 更正說明
6. [`10_math16_aggressive_round1_source_label_promotion_mismatch_correction_note_v1.md`](10_math16_aggressive_round1_source_label_promotion_mismatch_correction_note_v1.md) — Aggressive Round 1 source–label overlay＋479-cell consistency；formal evidence：`docs/experiments/results/math16_historical_round1_final_overlay_audit_v1/final_overlay_audit.jsonl`、`validation_summary.json`、`sha256_manifest.json`、`scripts/build_math16_historical_round1_final_overlay_audit_v1.py`、`docs/experiments/reports/math16_aggressive_round1_source_label_promotion_mismatch_correction_note_v1.md`、`docs/experiments/reports/math16_healer_rule_provenance_audit_v1.md`／`math16_healer_rule_provenance_audit_v1_manifest.json`
7. [`appendices/`](appendices/) — 附錄總冊

---

## 3. 核心數字摘要

| 項目 | 數值 |
|---|---|
| Gemini 3.5 Flash | **289/320** |
| Qwen3.5 9B | **101/320** |
| Qwen3.5 4B Baseline | **79/320** |
| Healer Final（Conservative） | **85/320** |
| Verified rescue（Conservative） | **6** |
| Aggressive Round 1（corrected overlay） | **79→87／rescue 8／3.32%** |
| Aggressive Round 1（frozen archive） | 79→88／rescue 9／3.73% |
| 呈現順序 | Gemini → Qwen3.5 9B → Qwen3.5 4B |
| Tier1（4B vs 9B） | 52／27／49／192 |
| McNemar p | **0.015440** |
| RD | **+6.875%** |
| OR | **1.81** |
| Polynomial 4B | **17/80**（p=0.1153） |

### `80/80*` 星號意義

Gemini **Ab2d+spec** 顯示 **80/80\***：採 **Post-hoc spec-v2** 結果；原 Primary **spec-v1** 為 **63/80**。星號表示版本／分帳差異，不作 Primary 正式四條件比較 headline。

---

## 4. 各檔用途

| 檔案 | 用途 |
|---|---|
| `01_…final_report_v13.md` | Working mirror 報告（同步回 canonical） |
| `02_…one_pager_v23.png` | One-Pager 圖檔 |
| `03_…one_pager_v23.pdf` | One-Pager PDF（1 頁） |
| `04_…jury_qa_final_v1.md` | 口試／評審 Q1–Q21 |
| `05_…correction_note_v1.md` | 分析／報告層 Baseline 更正說明（凍結證據不變） |
| `figures/` | Figure 1–6 最新 canonical SVG／PNG |
| `appendices/05_…appendices_v1.md` | 評審理解用附錄總冊 |
| `manifest_sha256.txt` | 本目錄正式檔案 SHA-256 目錄 |

---

## 5. 完整性索引

- 圖表：[`figures/figure_01_baseline_overall.png`](figures/figure_01_baseline_overall.png) … [`figures/figure_06_healer_concept_zones.png`](figures/figure_06_healer_concept_zones.png)  
- 附錄：[`appendices/05_math16_pilot02_appendices_v1.md`](appendices/05_math16_pilot02_appendices_v1.md)  
- 校驗：[`manifest_sha256.txt`](manifest_sha256.txt)  
