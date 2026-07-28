# Math16 Combined Amendment — Batch 5 Report v1

Report date: 2026-07-29  
Batch: **5 — current-facing formal text sync**（本輪依使用者指令執行文字同步；**不含**計畫原文之 package copy-forward／新 `Math16/` 目錄／package consolidation）  
Result: **PASS**

> 計畫檔 `math16_combined_amendment_execution_plan_v1.md` 將「正式報告＋Jury claim sync」標為 Batch 6、將「20260724 copy-forward」標為 Batch 5。本報告依**本輪使用者任務定義**記錄為 Batch 5（文字同步），並明確排除 copy-forward。

## 0. Scope

### In scope（已修改）

| # | Path |
|---|---|
| 1 | `docs/決賽文件/實驗結果文件/20260724_Math16/01_math16_pilot02_final_report_v13.md` |
| 2 | `docs/experiments/reports/math16_pilot02_integrated_results_report_v1.md` |
| 3 | `docs/experiments/reports/math16_method1_40_120_split_results_report_v1.md` |
| 4 | `docs/experiments/reports/math16_method2_all_cell_results_report_v1.md` |
| 5 | `docs/experiments/reports/20260728_math16_method1_method2_progress_handoff.md` |
| 6 | `docs/決賽文件/實驗結果文件/20260724_Math16/04_math16_pilot02_jury_qa_final_v1.md` |
| 7 | `docs/experiments/reports/math16_pilot02_jury_qa_final_v1.md` |
| 8 | `docs/experiments/visualization/math16_pilot02_core_figure_spec_v1/figure_caption_bank.md` |
| 9 | `docs/experiments/visualization/math16_pilot02_core_figure_spec_v1/primary_posthoc_visual_governance.md` |
| 10 | `docs/experiments/visualization/math16_pilot02_core_figure_spec_v1/one_pager_figure_selection.md` |
| 11 | `docs/experiments/visualization/math16_pilot02_core_figure_spec_v1/core_figure_spec.json` |
| 12 | `docs/experiments/visualization/math16_pilot02_core_figure_spec_v1/figure_data_tables.json` |
| 13 | `docs/experiments/visualization/math16_pilot02_core_figure_spec_v1/source_traceability.json` |
| 14 | `docs/experiments/visualization/math16_pilot02_core_figure_spec_v1/figure_spec_report.md` |

**修改文件總數：14**

### Explicitly excluded this round

- 新 `docs/決賽文件/實驗結果文件/Math16/` 目錄（未建立）
- 20260724 package binary copy-forward（One-Pager／Poster／Fig PNG 未覆寫進 package）
- `20260722_Math16/**`、plain-path `math16_pilot02_final_report_v13.md`
- `docs/experiments/results/**`、frozen journals／manifests／protocols／milestones／tests、`frozen_numeric_claims.json`
- One-Pager 輸出（未再生成）
- Poster／PPT／oral；`poster_and_oral_figure_order.md`
- Canonical Figure 1–6 SVG／PNG（本輪 SHA 零變動）

## 1. Core claim migration（舊→新）

| Claim | Old (current-facing) | New |
|---|---|---|
| Baseline | 78/320 (24.38%) | **79/320 (24.69%)** |
| Final | 84/320（常作主表） | **85/320** |
| Verified rescue | 6（不變） | **6** |
| Primary | 83／84 主表分帳 | **demoted**；歷史分帳保留 |
| Tier1 matrix | 52／26／49／193 | **52／27／49／192** |
| McNemar p | 0.010582 | **0.015440** |
| RD | +7.1875% | **+6.875%** |
| OR | 1.88 | **1.81** |
| Wald CI | [0.0194, 0.1243] | **[0.0159, 0.1216]** |
| Bootstrap CI | [-0.94%, +14.38%] 類 | **[-1.56%, +14.37%]** |
| Polynomial 4B | 16/80；p≈0.1671 | **17/80；p=0.1153** |
| Trio order | 常 Gemini→4B→9B | **Gemini→9B→4B** |

## 2. Per-file notes

### Final Report（唯一正式主報告）
- 頂部 Correction Notice；主表 **79→85／rescue=6**
- Tier1／Polynomial／Ab1 4B 16／80 同步
- 三模型列／欄序 G→9→4；兩模型配對結構保留
- Gemini Ab2d+spec：Primary 63/80 vs Post-hoc **80/80***
- Figure 路徑指向 package `supporting_assets/07_core_figures_v1/`（**二進位未於本輪更新**；橫幅已聲明可能仍顯示舊圖）

### Integrated
- Headline／Tier1／Family／條件表／Eligibility 主敘同步 79→85
- 凍結歷史分帳（§8 FAIL=242、§11.1 Primary 78→83／84）**語意保留**並標註
- Failure Layer 三模型欄序改 G→9→4（數值隨欄移動）
- Jury 子節 Q7／Q10／Q17／Q18 改報告層宣稱

### Method 1
- 主摘要：**79→85，rescue=6**
- 附錄 A：**凍結歷史 78／83／84 完整保留**
- Correction Note 連結已加

### Method 2
- Raw 79／Final 85／rescue 6／regression 0 **未改**
- Method1 交叉引用改為凍結歷史 vs 報告層更正

### Handoff
- Method1 報告層 79→85；凍結 vs corrected 區分
- 「78 vs 79」下一步標為 **RESOLVED**

### Jury Q&A
| | Canonical `20260724/04` | Sync `experiments/reports/…` |
|---|---|---|
| Q1–Q20 | 保留 | 保留 |
| R1–R8 | **無**（未灌入） | **保留**；R2／R3 claim sync |
| Q21（78 vs 79） | **新增於末** | **新增於 Q20 與 R 段之間** |
| Sync 方式 | claim-only；**禁止全文覆蓋** | 同 |

## 3. Model-order audit

| Surface | Result |
|---|---|
| Final Report 三模型表／列舉 | G→9→4 PASS |
| Integrated Baseline／Failure Layer | G→9→4 PASS |
| Spec JSON／caption／one-pager selection | G→9→4 PASS |
| 兩模型 McNemar／Family 配對 | 維持 4B vs 9B 結構 PASS |
| 欄名移動但數值未動 | **未發現** |

## 4. Figure reference SHA（canonical；本輪未改）

| File | SHA-256 |
|---|---|
| figure_01_baseline_overall.png | `c5e091eedd82c4a39c78b596b970cd538d6503022546315b7832f3df4ba8d684` |
| figure_02_prompt_conditions.png | `8b72c42e4e8590a0fd67388a3b1c30317d174521fc9469beff1d6fae25ddae5f` |
| figure_03_family_breakdown.png | `2d225e069a62529d3657aec629a0b90df10ba63df9f68c927e81ab35e5b729c2` |
| figure_04_tier1_paired_analysis.png | `0daa7d332941709708f021b6f20bbb2d180f41a7ab7a36cc4f4c1572a7ac6da9` |
| figure_05_healer_eligibility_boundary.png | `05b81728393037f0657a42af34de883bbc860e44eccdfbfbf40553e86e6f1849` |
| figure_06_healer_concept_zones.png | `3b358862434ea81b74841def4ca81a6168b8e1ff36ab2b44f3868d4db891c71c` |

`core_zero = True`（本輪前後 SHA 比對）。  
Package 內 `supporting_assets/07_core_figures_v1/*` **未 copy-forward**（屬後續 package 批次）。

## 5. Residual hits（合理性）

Current-facing 主表／主敘：**無未標註之 78／83／84／0.010582／Gemini→4B→9B 殘留主張。**

允許出現處（抽樣）：
- Correction Notice／「更正前／舊值／凍結歷史」對照
- Method1 附錄 A 凍結表 78／83／84
- Integrated §11.1 凍結 Primary／Post-hoc 分帳
- Jury Q21／Forbidden #6 歷史對照
- Gemini `Ab2d+api` **78/80**（非 78/320）

## 6. Poster exclusion（excluded pending future poster work）

本輪**未修改、未還原、未刪除、未納入成果**。工作區既有 tracked `M`（先前對話殘留）：

```
M docs/experiments/presentation/math16_pilot02_poster_v11/assets/fig1_compact_v11.png
M docs/experiments/presentation/math16_pilot02_poster_v11/assets/fig2_compact_v11.png
M docs/experiments/presentation/math16_pilot02_poster_v11/assets/fig3_compact_v11.png
M docs/experiments/presentation/math16_pilot02_poster_v11/assets/fig4_compact_v11.png
M docs/experiments/presentation/math16_pilot02_poster_v11/assets/fig5_compact_v11.png
M docs/experiments/presentation/math16_pilot02_poster_v11/math16_pilot02_poster_v11.pdf
M docs/experiments/presentation/math16_pilot02_poster_v11/math16_pilot02_poster_v11.png
M docs/experiments/presentation/math16_pilot02_poster_v11/poster_v11_build_report.md
M docs/experiments/presentation/math16_pilot02_poster_v11/poster_v11_element_bboxes.json
M docs/experiments/presentation/math16_pilot02_poster_v11/poster_v11_manifest.json
M scripts/build_math16_pilot02_poster_v11.py
```

`poster_and_oral_figure_order.md`：本輪未改。  
狀態標註：**excluded pending future poster work**。

## 7. Frozen／historical 零變動

| Class | Status |
|---|---|
| `docs/experiments/results/**` | 未改 |
| frozen claims／journals／manifests／protocols／tests | 未改 |
| `20260722_Math16/**` | 未改 |
| plain-path `math16_pilot02_final_report_v13.md` | 未改 |
| Canonical Fig1–6 | SHA 零變動 |
| One-Pager 輸出 | 本輪未再生成 |

## 8. Verdict

**Batch 5 PASS**

已知限制（不構成 BLOCK）：
- 20260724 package 內嵌 PNG／PDF 仍可能為舊圖（本輪禁止 copy-forward）
- Integrated §8 Failure Layer 分母維持凍結 FAIL=242（未重算 Layer 桶；已標註）
