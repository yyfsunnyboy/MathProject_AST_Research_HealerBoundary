# Math16 Final Package Consolidation Report v1

Report date: 2026-07-29  
Task: Create current formal delivery package `docs/決賽文件/實驗結果文件/Math16/`  
Result: **PASS**

## 1. Package path

`docs/決賽文件/實驗結果文件/Math16/`

## 2. Formal file inventory（19 files；manifest 不含自身）

| Relative path | Role |
|---|---|
| `README.md` | 正式入口說明 |
| `01_math16_pilot02_final_report_v13.md` | Final Report（Batch 5 正本 copy；僅改相對路徑） |
| `02_math16_pilot02_one_pager_v23.png` | One-Pager PNG |
| `03_math16_pilot02_one_pager_v23.pdf` | One-Pager PDF |
| `04_math16_pilot02_jury_qa_final_v1.md` | Jury Q&A 正本 copy（Q1–Q21；僅改 Correction Note 路徑） |
| `05_math16_baseline_correction_note_v1.md` | Correction Note |
| `figures/figure_01_baseline_overall.svg` | Fig1 SVG |
| `figures/figure_01_baseline_overall.png` | Fig1 PNG |
| `figures/figure_02_prompt_conditions.svg` | Fig2 SVG |
| `figures/figure_02_prompt_conditions.png` | Fig2 PNG（80/80*） |
| `figures/figure_03_family_breakdown.svg` | Fig3 SVG |
| `figures/figure_03_family_breakdown.png` | Fig3 PNG |
| `figures/figure_04_tier1_paired_analysis.svg` | Fig4 SVG |
| `figures/figure_04_tier1_paired_analysis.png` | Fig4 PNG |
| `figures/figure_05_healer_eligibility_boundary.svg` | Fig5 SVG |
| `figures/figure_05_healer_eligibility_boundary.png` | Fig5 PNG |
| `figures/figure_06_healer_concept_zones.svg` | Fig6 SVG |
| `figures/figure_06_healer_concept_zones.png` | Fig6 PNG |
| `appendices/05_math16_pilot02_appendices_v1.md` | 附錄總冊（自 20260724 正式附錄） |
| `manifest_sha256.txt` | SHA 清單（不列入自身） |

## 3. Core numbers

| Check | Result |
|---|---|
| Gemini 289/320 | PASS |
| 9B 101/320 | PASS |
| 4B Baseline 79/320 | PASS |
| Final 85/320 | PASS |
| Verified rescue 6 | PASS |
| Tier1／p=0.015440／Polynomial 17/80 | PASS |
| Order Gemini→9B→4B | PASS |
| Gemini Ab2d+spec 80/80*＋Primary 63/80 | PASS |

## 4. Figures 1–6

- 來源：`docs/experiments/visualization/math16_pilot02_core_figures_v1/` byte-copy  
- 未 re-render  
- Fig2 PNG SHA = `8b72c42e4e8590a0fd67388a3b1c30317d174521fc9469beff1d6fae25ddae5f`（與 canonical 一致）  
- SVG／PNG 各 6 檔皆存在且可開啟  

## 5. One-Pager

| Asset | Check |
|---|---|
| PNG | 3619×2541；SHA `7eee10d8b53f911cafa1a68e5333840568ff6e89afd9ca91c2591566bdc941c4` |
| PDF | 1 page |

來源：`docs/experiments/presentation/math16_pilot02_one_pager_v23/`（本輪未改來源）

## 6. Links

| Doc | Fix |
|---|---|
| Final Report | `figures/figure_0*.png`；Correction Note → `05_math16_baseline_correction_note_v1.md` |
| Jury Q&A | Correction Note → `05_math16_baseline_correction_note_v1.md` |
| README | 指向本目錄正式檔 |
| Appendices | 無失效相對路徑（repo-root 風格引用保留為說明） |

Package-internal markdown link resolve：**0 broken**。

## 7. Appendices

- `appendices/05_math16_pilot02_appendices_v1.md`  
- 來源：`20260724_Math16/05_math16_pilot02_appendices_v1.md`  
- **未**納入 `archive_or_working_notes/`、scratch、batch reports、Poster  

## 8. Old dated directories

- `20260724_Math16/**`：**零變動**（pre/post SHA 快照一致）  
- `20260722_Math16/**`：**零變動**  

## 9. Poster／PPT

- **零納入**（目錄樹無 poster／ppt／pptx）  

## 10. Manifest

- Path：`docs/決賽文件/實驗結果文件/Math16/manifest_sha256.txt`  
- Listed files：**19**  

## 11. Hard limits

- 未修改 Batch 5 來源正本、canonical figures、One-Pager 來源、Poster、results／frozen、未 commit／push  
- 僅 copy-forward、相對連結修正、README、manifest、驗證  

## 12. Verdict

**Final package consolidation：PASS**
