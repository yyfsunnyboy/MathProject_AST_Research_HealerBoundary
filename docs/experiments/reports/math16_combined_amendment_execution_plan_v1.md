# Math16 Combined Amendment Execution Plan v1

Plan date: 2026-07-28  
Revision: **blocker_closure_v3** — closes Jury Q&A canonical/sync, E-class link batching, and Figure 4 PNG pipeline.  
Status: **execution design ready.** Updates only the three untracked combined artifacts. No formal docs, SVG/PNG/PDF, generators, or Fig1/Fig4 WT changes in this round.

Machine companions:

- `math16_combined_amendment_asset_map_v1.csv`
- `math16_combined_amendment_execution_summary_v1.json`

---

## 0. Locked constants

| Item | Value |
|---|---|
| Current-facing execution paths | 55 |
| Batches | **0–7** (8) |
| Model order | Gemini 3.5 Flash → Qwen3.5 9B → Qwen3.5 4B |
| Presentation numbers | Baseline **79/320**, Final **85/320**, Verified rescue **6** |
| Frozen evidence | keeps **78**; never modify |
| Presentation claims (Batch 0) | `docs/experiments/visualization/math16_pilot02_amendment_layer_v1/presentation_claims_v1.json` |

Hard exclusions unchanged: `20260722_Math16/**`, plain-path `math16_pilot02_final_report_v13.md`, `results/**`, frozen claims/manifests/protocols/milestones/tests.

---

## 1. Blocker closed — Jury Q&A canonical vs sync

### Evidence (sufficient — not a human guess)

| Evidence | Finding |
|---|---|
| `20260724_Math16/README.md` | 權威性交付聲明：正式報告／數字／圖表／**口試依據**均以 `20260724_Math16/` 為準 |
| Canonical Final Report ~L417 | 「正式 Jury Q&A…（**20260724 唯一正式交付入口**）」→ `04_math16_pilot02_jury_qa_final_v1.md` |
| `math16_pilot02_final_report_v13_manifest.json` | `jury_qa` → `20260724_Math16/04_…` |
| Size / structure | Canonical **121 lines / 7550 chars**; sync **149 lines / 9039 chars** |
| Structure diff | Sync has extra **§三 最容易被追問的速答 R1–R8**; canonical does **not** |
| Git | Canonical tip `e64cf5b0` (2026-07-27 package align); sync-path tip `cd9b96ae` (2026-07-23 risk review); shared earlier history |
| Other refs | Integrated report still links `experiments/reports/…jury_qa…` (supporting, not package authority) |

### Designation

| Role | Exact path |
|---|---|
| **唯一內容正本 (canonical content master)** | `docs/決賽文件/實驗結果文件/20260724_Math16/04_math16_pilot02_jury_qa_final_v1.md` |
| **同步副本 (claim-only sync)** | `docs/experiments/reports/math16_pilot02_jury_qa_final_v1.md` |
| Excluded historical | `docs/決賽文件/實驗結果文件/20260722_Math16/04_math16_pilot02_jury_qa_final_v1.md` |

### Sync rules (Batch 6)

1. **正本**：保留全部散文與結構（Q1–Q20）；就地改數字主張／Correction Note；不得為「對齊」而灌入 R1–R8。  
2. **同步副本**：只同步數字主張、表格（若有）、模型順序 token（若有）、Correction Note link；**禁止全文覆蓋**；**保留**本地 R1–R8。  
3. 禁止把兩檔當 byte-identical twins 做全域 search-replace。

**Human blocker remaining:** none (evidence sufficient).

---

## 2. Blocker closed — E-class Correction Note links

### Rules

- **Not** mixed into early numeric batches (0–6).  
- Execute **only in Batch 7** (consistency).  
- **Only** current-facing E paths.  
- **No** links on: frozen／historical no-edit, `20260722/**`, plain-path v13, `results/**`, `archive_or_working_notes/**`, `frozen_numeric_claims`.

Correction Note target: `docs/experiments/reports/math16_baseline_correction_note_v1.md`

### Exact E paths (7) and insertion points

| # | Path | Insertion |
|---|---|---|
| 1 | `docs/決賽文件/實驗結果文件/20260724_Math16/README.md` | After 權威性交付聲明 blockquote, or new Baseline Correction bullet in reading-order |
| 2 | `docs/決賽文件/實驗結果文件/20260724_Math16/05_math16_pilot02_appendices_v1.md` | After title/front-matter, before first appendix body |
| 3 | `docs/experiments/reports/math16_pilot02_final_report_v1.md` | Under H1 — historical banner + link; **do not** rewrite body numbers |
| 4 | `docs/experiments/reports/math16_pilot02_final_report_v11.md` | Under H1 — historical banner + link |
| 5 | `docs/experiments/reports/math16_pilot02_final_report_v12.md` | Under H1 — historical banner + link |
| 6 | `docs/experiments/reports/math16_jury_risk_review_v1.md` | Under H1 — historical banner + link |
| 7 | `docs/experiments/reports/healerboundary_final_evidence_gap_decision_v1.md` | Under H1 — historical banner + link |

**E path count = 7.**

---

## 3. Blocker closed — Figure 4 PNG lag

### Confirmation

| Item | Value |
|---|---|
| Canonical amended SVG | `docs/experiments/visualization/math16_pilot02_core_figures_v1/figure_04_tier1_paired_analysis.svg` |
| Current PNG | `docs/experiments/visualization/math16_pilot02_core_figures_v1/figure_04_tier1_paired_analysis.png` |
| Stale? | **Yes** — SVG is `git M` + newer mtime; PNG clean/unmodified |
| SVG amended tokens present | `27`, `192`, `4B-only PASS: 27`, `+22`, `p = 0.015440`, `-1.56` |
| Old tokens absent in SVG | `26`, `193`, `0.010582` |

### Fixed pipeline

```text
amended SVG (SOT)
  → regenerated PNG (from SVG)
  → visual validation
  → compact copies (one_pager fig4 + poster fig4)
  → One-Pager / Poster full renders
  → 決賽 package supporting_assets/figure_04_…png
```

### Export command (Batch 3)

Prefer **SVG→PNG rasterize** (does not rewrite SVG):

```bash
inkscape docs/experiments/visualization/math16_pilot02_core_figures_v1/figure_04_tier1_paired_analysis.svg \
  --export-filename=docs/experiments/visualization/math16_pilot02_core_figures_v1/figure_04_tier1_paired_analysis.png \
  --export-dpi=300
```

(Equivalents: `rsvg-convert`, `cairosvg`.)

**FORBIDDEN:** `python scripts/build_math16_pilot02_core_figures_v1.py` — loads/asserts frozen 78 and would overwrite SVG.

### PNG validation

1. PNG mtime ≥ SVG mtime  
2. Visual: 27 / 192 / +22 / p=0.015440 / CI with −1.56; axes still 4B×9B  
3. `git diff` on SVG still shows only intended WT amendment (not reverted)

Copy-forward order matches the pipeline above (canonical PNG before package copy).

---

## 4. Executable Batch 0–7

### Batch 0 — Scaffold claims + backup

| | |
|---|---|
| Inputs | Prior plans; WT Fig1/Fig4 SVG |
| Outputs | `presentation_claims_v1.json`; `wt_backup/`; `staging/` |
| May edit | New `amendment_layer_v1/` only |
| Forbidden | Formal docs; in-place tracked renders; generators; frozen evidence |
| Rollback | Delete amendment_layer dir |
| Verify | Claims: G→9→4, 79, 85, rescue 6, amended Fig4 stats; backup has Fig1+Fig4 |
| Gate →1 | Claims file exists + schema OK |

### Batch 1 — Specs / governance / data tables

| | |
|---|---|
| Inputs | presentation_claims |
| Outputs | Amended `core_figure_spec_v1` presentation specs |
| May edit | caption_bank, governance, selection md, `core_figure_spec.json`, `figure_data_tables.json`, `source_traceability.json`, `figure_spec_report.md` |
| Forbidden | results/**; frozen claims; Jury/Method yet; **E links** |
| Rollback | Restore those spec paths |
| Verify | Keys/order G→9→4; 79 not 78 |
| Gate →2 | Specs match claims |

### Batch 2 — Render figures → staging

| | |
|---|---|
| Inputs | Claims; new amendment renderer |
| Outputs | Staging Fig1–3,5 (Fig4 SVG stays WT SOT) |
| May edit | New renderer; `staging/` only |
| Forbidden | Overwrite WT Fig1/Fig4 yet; frozen core builder |
| Rollback | Discard staging |
| Verify | Fig1=79+G94; Fig5=79→85+G94; Fig3=17/80 only |
| Gate →3 | Staging checklist pass |

### Batch 3 — Promote + Fig4 PNG export

| | |
|---|---|
| Inputs | Staging; WT Fig4 SVG |
| Outputs | Promoted Fig1–3,5 SVG/PNG; **Fig4 PNG from SVG** |
| May edit | Canonical visualization after validation; **Fig4 PNG only** (SVG remains WT amended) |
| Forbidden | Frozen builder; revert Fig4 SVG to 26/193 |
| Rollback | `wt_backup` / HEAD |
| Verify | Fig4 PNG mtime≥SVG; amended visuals; Fig1/5 match claims |
| Gate →4 | Fig4 PNG stale cleared |

### Batch 4 — One-Pager / Poster generators + regen

| | |
|---|---|
| Inputs | Promoted figs including fresh Fig4 PNG |
| Outputs | One-Pager/Poster renders, compacts, manifests, build reports |
| May edit | `build_math16_pilot02_one_pager_v23.py`, `build_math16_pilot02_poster_v11.py`, their outputs |
| Forbidden | Frozen core builder; `extract_figure_data.py`; frozen evidence I/O |
| Rollback | Restore builders + outputs |
| Verify | Cards G→9→4; 79→85 rescue=6; fig4 compact amended |
| Gate →5 | Presentation validated |

### Batch 5 — Copy-forward 20260724 package

| | |
|---|---|
| Inputs | Canonical PNG/PDF |
| Outputs | Package PDFs + supporting_assets (incl. Fig4 PNG) |
| May edit | `20260724_Math16` copies only |
| Forbidden | `20260722/**`; plain-path v13 |
| Rollback | Restore package binaries |
| Verify | Package Fig4 PNG matches canonical PNG |
| Gate →6 | Copy-forward OK |

### Batch 6 — Formal reports + Jury claim sync

| | |
|---|---|
| Inputs | Claims; promoted figs |
| Outputs | Canonical FR; integrated; Method1/2; handoff; Jury **canonical full**; Jury **sync claim-only** |
| May edit | `20260724/01` FR; live integrated; method1/2; handoff; `20260724/04` Jury; `experiments/reports` Jury (claims only) |
| Forbidden | **E links**; plain-path v13; 20260722; archive notes; **Jury full overwrite** |
| Rollback | Restore those md paths |
| Verify | Canonical Jury 79 + Correction Note; sync retains R1–R8; FR G→9→4 + 79/85 |
| Gate →7 | Batch 6 numeric/order audit pass |

### Batch 7 — Consistency audit + E-class links

| | |
|---|---|
| Inputs | All prior outputs; Correction Note |
| Outputs | Links on **7** E paths; final checklist |
| May edit | 7 E paths — **link only** |
| Forbidden | Rewriting E body numbers; links on G/F excluded paths |
| Rollback | Revert E link hunks only |
| Verify | 7 links present; no forbidden links; full consistency checklist |
| Gate | **DONE** |

---

## 5. Generator differential (restated)

| Script | Decision |
|---|---|
| `build_math16_pilot02_core_figures_v1.py` | **Frozen — do not modify** (frozen claims/asserts) |
| `render_math16_pilot02_core_figures_amendment_v1.py` | **Create** — reads presentation_claims only |
| `build_math16_pilot02_one_pager_v23.py` / `poster_v11.py` | **May modify** — presentation assembly; no frozen evidence I/O |
| `extract_math16_pilot02_figure_data.py` | **Frozen — do not modify** |

---

## 6. Open blockers

**None remaining** for execution start. Prior three blockers are closed in §§1–3.

---

## 7. This round

Updated only the three untracked combined plan artifacts. Did not modify tracked formal files, SVG/PNG/PDF, generators, or Fig1/Fig4 WT.
