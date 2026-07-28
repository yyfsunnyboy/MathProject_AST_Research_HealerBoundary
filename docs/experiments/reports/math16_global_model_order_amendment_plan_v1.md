# Math16 Global Model Presentation Order Amendment Plan v1

Plan date: 2026-07-28  
Status: **planning / specification only — no formal document, SVG, PNG, PDF, or generator was modified to produce this plan.** Only this plan, the companion CSV, and the companion JSON were added.

## 0. Adopted presentation rule (reporting-layer only)

Teacher-specified **global presentation order** for all current-facing results, tables, figures, legends, and three-model comparison prose:

1. **Gemini 3.5 Flash**
2. **Qwen3.5 9B**
3. **Qwen3.5 4B**

Short form used below: **G → 9B → 4B**.

This is a **presentation / reporting-layer** rule. It does **not**:

- re-rank research performance;
- change any numeric value, statistical definition, or raw evidence ordering;
- force two-model analyses into three-model tables;
- alter McNemar / 2×2 quadrant definitions;
- authorize edits to frozen evidence, `docs/experiments/results/**`, or excluded historical packages.

Dominant observed wrong trio order in current artifacts: **G → 4B → 9B** (bars, legends, many table columns/rows, One-Pager/Poster cards). Some prose already uses G → 9B → 4B (e.g. Final Report §9 bullets; several captions).

## 1. Scope and search method

### In scope (current-facing)

- `docs/決賽文件/實驗結果文件/20260724_Math16/**`
- Current Final Report (canonical: `20260724_Math16/01_math16_pilot02_final_report_v13.md`; Abstract is inline)
- Jury Q&A, Appendices, README in that package
- Current Method 1 / Method 2 reports, integrated report, handoff
- Current core figures SVG/PNG + figure specs
- Current One-Pager v23 / Poster v11 + builders
- Corresponding generator / extract / render scripts
- Current-facing figure governance / caption / data-table sources

### Explicitly excluded (G — no edit, no reorder, no correction link)

- `docs/決賽文件/實驗結果文件/20260722_Math16/**`
- `docs/experiments/reports/math16_pilot02_final_report_v13.md`
- `docs/experiments/results/**`
- frozen journals / manifests / protocols / milestones / audit evidence
- raw cell-level data
- historical tests and frozen-result assertions

### Model-name variants searched

`Gemini 3.5 Flash`, `Gemini Flash`, `gemini-3.5-flash`, `Qwen3.5 9B`, `Qwen 9B`, `qwen3_5_9b`, `qwen3.5:9b`, `Qwen3.5 4B`, `Qwen 4B`, `qwen3_5_4b`, `qwen3.5:4b`, plus short `4B`/`9B`/`Gemini` in multi-model lines.

### Old order patterns searched

`4B→9B→Gemini`, `9B→4B→Gemini`, `Gemini→4B→9B`, `Qwen 4B／Qwen 9B／Gemini`, and table column/row / legend / series permutations.

### Classification legend

| Code | Meaning |
|---|---|
| **A** | Must edit current formal document / governance text |
| **B** | Must remake or reorder current figure / render asset |
| **C** | Must edit generator / render / data-spec source |
| **D** | Two-model (or single-model) analysis — trio global order N/A |
| **E** | Semantic / research-logic order — keep |
| **F** | Historical / frozen evidence — forbidden to modify |
| **G** | Excluded directory / explicitly excluded file |

Machine-readable per-location rows: `docs/experiments/reports/math16_global_model_order_crosswalk_v1.csv` (84 entries).  
Roll-up: `docs/experiments/reports/math16_global_model_order_summary_v1.json`.

### Working-tree constraint (Figure 1 / 4)

Uncommitted edits already present (baseline 78→79 amendment track):

- `figure_01_baseline_overall.svg` — Qwen 4B label `78/320`→`79/320`, `(24.4%)`→`(24.7%)`
- `figure_04_tier1_paired_analysis.svg` — 4B-only / BOTH_FAIL (and related) cell updates

**This round must not overwrite, revert, or lose those edits.** Future model-order remakes must compose with them.

---

## 2. Answers to required inventory questions

| # | Question | Answer |
|---|---|---|
| 1 | 命中文件總數 | **75** distinct paths in the crosswalk (plus 3 G directory globs as entries) |
| 2 | 真正需要修改的文件數 | **38** (A∪B∪C actionable paths) |
| 3 | 需重製圖表數 | **22** B assets (canonical SVG/PNG + One-Pager/Poster renders + 決賽 copies) |
| 4 | 需修改 generator 數 | **4** Python scripts (`core_figures`, `one_pager_v23`, `poster_v11`, `extract_figure_data`); **10** C sources if counting JSON/manifest/spec companions |
| 5 | 不適用的兩模型分析數 | **16** D entries |
| 6 | 禁止修改的 frozen／historical 數 | **17** (F=14 + G=3 entries) |
| 7 | 欄名已換但數值未跟著移動的既有風險？ | **No existing desync found.** Prospective risk is high on future table edits. Spec caption already narrates G→9→4 while `x_axis` still lists G→4→9 (values remain key-bound). |
| 8 | 模型顏色與位置綁定？ | **Yes for positions.** `COLORS` dict is identity-safe; bar/legend arrays and Fig5 `x=1` posthoc overlay are position-bound. |
| 9 | Figure 1／3／4／5 新處理判定 | **Fig1: 需再次結構重製（保留 79）**；**Fig3: 不因序重製（D）**；**Fig4: 不因序重製（D），保留 WT 79 修正**；**Fig5: 需再次結構重製** |
| 10 | 未列入的圖表／One-Pager／Poster？ | Current v23/v11 + 決賽 copies inventoried. Older one-pager/poster versions = F. Method1-only figures under `reports/figures/math16_method1_40_120/` = D. |

### A–G entry counts

| A | B | C | D | E | F | G | Total |
|---|---|---|---|---|---|---|---|
| 12 | 22 | 10 | 16 | 7 | 14 | 3 | **84** |

---

## 3. File-by-file amendment specification

For every row below: **target order = G → 9B → 4B** unless classification is D/E/F/G (then target is N/A or “do not modify”).

### 3.1 A — Current formal documents / governance text

| Path | Line / section | Artifact | Existing order | Move | Values move? | Color? | Remake? | Generator | Risk | Verify |
|---|---|---|---|---|---|---|---|---|---|---|
| `…/20260724_Math16/01_math16_pilot02_final_report_v13.md` | §5 測試模型 L61–63 | list | 4B→9B→Gemini | reorder 3 bullets | text roles stay with model | no | no | n/a | medium | list = G→9→4 |
| same | §11 table L217–220 | table **rows** | 4B→9B→Gemini | whole rows | **yes** | no | no | n/a | **high** | Gemini289 / 9B101 / 4B78·83·84 |
| same | §15 table L315–320 | table **cols** | G→4B→9B | whole columns | **yes** | no | no | n/a | **high** | header G\|9B\|4B; Ab1 72/18/15 |
| same | §9 L110–112 | bullets | **already G→9→4** | none | n/a | no | no | n/a | low | keep; 78→79 is separate track |
| `docs/experiments/reports/math16_pilot02_integrated_results_report_v1.md` | **L114 explicit 展現順序** | statement | **G→4B→9B written as policy** | rewrite policy sentence | n/a | no | no | n/a | **critical** | search「展現順序」= G→9→4 |
| same | L121–123 baseline rows | table rows | G→4B→9B | whole rows | **yes** | no | no | n/a | high | G→9→4 |
| same | L156 condition cols; L177 family cols | table cols | G→4B→9B | whole columns | **yes** | no | no | n/a | high | dual-table schema log |
| same | L220 / L275–277 / L331–333 | mixed tables | mixed 4→9→G and G→4→9 | whole col/row by identity | **yes** | no | no | n/a | high | per-table before/after schema |
| `…/core_figure_spec_v1/figure_caption_bank.md` | Fig1/2/5 captions | md | mixed; Fig1 report already G→9→4 | trio clauses only | text | no | no | mirrors spec JSON | medium | do not rewrite Fig3/4 as trio |
| `…/primary_posthoc_visual_governance.md` | display-order mentions | governance | G→4→9 | add/replace presentation-order rule | n/a | no | no | gates regen | medium | rule states G→9→4 ≠ ranking |
| `…/one_pager_figure_selection.md` | selection notes | governance | partial G→9→4 | align trio wording | n/a | no | no | one-pager | low | consistent |
| `…/poster_and_oral_figure_order.md` | oral points | governance | mixed | trio oral order | n/a | no | no | poster/oral | low | G→9→4 |

**Abstract:** no standalone file; lives in Final Report opening. Baseline sentence already presents Gemini → 9B → 4B.

**Jury Q&A** (`20260724` + `experiments/reports` copies): classified **D** (pairwise), not A — see §3.4.

**README / Appendices:** **E** (topic or 4B-centric), not mechanical trio reorder.

### 3.2 B — Figures / rendered assets requiring remake

| Path | Figure / asset | Existing | Move | Values? | Color? | Remake? | Generator | Risk | Verify |
|---|---|---|---|---|---|---|---|---|---|
| `…/figure_01_baseline_overall.svg` (+ `.png`) | Fig1 L→R bars | G→4B→9B | whole bars+labels+colors | **yes** | **yes** identity | **structural** | `build_math16_pilot02_core_figures_v1.py` | **critical** vs WT 79 | L→R G(藍289), 9B(琥珀101), 4B(綠**79**) |
| `…/figure_02_prompt_conditions.svg` (+ `.png`) | Fig2 grouped + legend | G,4B,9B per group | series slots + legend | **yes** | **yes** | **structural** | same | high | per condition G,9B,4B; hatch Gemini stays Gemini |
| `…/figure_05_healer_eligibility_boundary.svg` (+ `.png`) | Fig5 categories | G→4B→9B | groups + posthoc overlay | **yes** | metric colors OK; overlay follows 4B | **structural** | same | **critical** index=1 | FAIL [31,219,242]; overlay on 4B |
| One-Pager v23 png/pdf + `fig1`/`fig5` compact | cards+bars | G→4B→9B | cards + trio figs | **yes** | **yes** | yes | `build_math16_pilot02_one_pager_v23.py` | high desync | visual G→9→4 |
| Poster v11 png/pdf + fig1/2/5 compact | cards+figs | G→4B→9B; prose 4B,9B,G | cards + trio figs + prose | **yes** | **yes** | yes | `build_math16_pilot02_poster_v11.py` | high | cards G→9→4 |
| `20260724_Math16/02_…one_pager….pdf`, `03_…poster….pdf`, `supporting_assets/…` fig1/2/5 + one-pager/poster png | package copies | same as sources | copy-forward after regen | **yes** | **yes** | yes | upstream builders | high miss-sync | match canonical outputs |

**Figure 1 / 3 / 4 / 5 disposition (order amendment):**

| Figure | Order remake? | Notes |
|---|---|---|
| **1** | **YES** | Still G→4B→9B in SVG comments (Gemini @L53, 4B @L531, 9B @L748). Remake **must preserve** WT `79/320 (24.7%)`. |
| **3** | **NO (D)** | 4B vs 9B family bars only. Do not insert Gemini. Optional 9B↔4B side swap is **out of scope** under two-model rule. |
| **4** | **NO (D)** | McNemar axes 4B×9B are statistical structure. **Do not overwrite** WT 79-related edits. |
| **5** | **YES** | G→4B→9B categories; posthoc overlay hard-bound to index 1 in generator. |

Fig6: **E** — conceptual, no model axis.

### 3.3 C — Generators / render sources

| Path | Section | Existing | Move | Values? | Color? | Remake downstream? | Risk | Verify |
|---|---|---|---|---|---|---|---|---|
| `scripts/build_math16_pilot02_core_figures_v1.py` | COLORS; `render_figure_1/2/5` | G→4B→9B lists; Fig5 `x=1` & asserts `[31,242,219]` | models + parallel arrays + legend + Fig5 index | **yes** | identity COLORS OK; position arrays not | yes | **critical** also asserts `baseline_pass==78` via frozen claims | models=[G,9B,4B]; overlay follows 4B; **do not edit** `frozen_numeric_claims.json` |
| `scripts/build_math16_pilot02_one_pager_v23.py` | fig1/fig5 ticks; cards L440–442 | G→4B→9B | ticks, color arrays, card strip, value arrays | **yes** | **yes** | yes | high | output G→9→4; fig3/4 stay D |
| `scripts/build_math16_pilot02_poster_v11.py` | cards L174–178; L185 prose | cards G→4B→9B; prose 4→9→G | cards + prose | **yes** | card fills | yes | high | G→9→4 |
| `scripts/extract_math16_pilot02_figure_data.py` | dict key insertion | G→4B→9B | key order in emitted JSON | **yes** | indirect | writes data tables | medium | `list(keys)==[G,9B,4B]`; no writes to `results/**` |
| `core_figure_spec.json` | `x_axis`, `exact_data` keys | G→4B→9B | axis string + key order | key-bound values | indirect | yes | high | axis matches captions |
| `figure_data_tables.json` | fig1/2/5 objects | G→4B→9B insertion | key blocks | **yes** | indirect | yes | medium-high | key order check |
| `source_traceability.json` | model→path map | G→4B→9B | key order if displayed | paths stay | no | no | low-medium | paths unchanged |
| `figure_build_manifest.json` / `figure_build_report.md` / `poster_v11_manifest.json` | build metadata | prior build | update **only after** intentional regen | n/a | no | on regen | low | this round: read-only |

**Frozen evidence collision:** regenerating via `build_math16_pilot02_core_figures_v1.py` currently loads `frozen_numeric_claims` and asserts 4B baseline **78**. Ordering work must **not** “fix” that by editing frozen evidence. Sequencing with the separate baseline-79 amendment is an open blocker.

### 3.4 D — Two-model / single-model (do not force trio order)

| Path | Why D |
|---|---|
| Final Report §12 + Fig3/4 embeds | Tier-1 4B vs 9B pairing |
| Integrated report McNemar 2×2 L133–137 | Statistical 4B×9B structure |
| `figure_03_*`, `figure_04_*` (+ 決賽 PNG copies) | Two-model charts |
| One-Pager/Poster `fig3`/`fig4` compact assets | Same |
| Jury Q&A (both copies) | Pairwise Qs (4B↔9B, Gemini alone, etc.) |
| Method 1 / Method 2 reports | **4B-only** — no trio columns |
| `analyze_math16_pilot02_qwen4b_vs_qwen9b_tier1_paired.py` | Analysis direction; outputs under `results/**` (F/G) |
| `figure_spec_report.md` Fig3 row | Two-model wording |

### 3.5 E — Keep research / semantic order

| Path | Why keep |
|---|---|
| Final Report causal narratives (“為何 4B eligible 而 9B/Gemini=0”) | Contrast logic, not presentation ranking |
| `20260724` README L55–57 | Topic bullets (Gemini spec history / Qwen Primary / Healer), not trio table |
| Appendices | 4B-centric mechanism appendix |
| Handoff `20260728_…progress_handoff.md` | Method progress, no trio presentation |
| Figure 6 (+ copies) | Concept zones, no model axis |

### 3.6 F — Historical / frozen — forbidden

Superseded Final Report v1/v11/v12; superseded one-pager/poster builders; `archive_or_working_notes/*` under `20260724`; `frozen_numeric_claims.json`; other milestone/frozen artifacts. **No edit for ordering.**

### 3.7 G — Excluded

| Path | Note |
|---|---|
| `docs/experiments/reports/math16_pilot02_final_report_v13.md` | Explicit exclude |
| `docs/決賽文件/實驗結果文件/20260722_Math16/**` | Historical finals package |
| `docs/experiments/results/**` | Raw / machine evidence |

---

## 4. Table schema before → after (trio tables only)

### Final Report §11 (rows)

| Before (top→bottom) | After |
|---|---|
| Qwen 4B \| Qwen 9B \| Gemini | Gemini \| Qwen 9B \| Qwen 4B |

Entire row cells travel with the model. No Total row.

### Final Report §15 (columns)

| Before (L→R) | After |
|---|---|
| Condition \| Gemini \| Qwen 4B \| Qwen 9B | Condition \| Gemini \| Qwen 9B \| Qwen 4B |

Example Ab1 after: `72 / 80 | 18 / 80 | 15 / 80`.

### Integrated report baseline rows L121–123

| Before | After |
|---|---|
| Gemini → 4B → 9B | Gemini → 9B → 4B |

### Integrated Condition / Family column tables

Same column swap as Final Report §15.

### McNemar 2×2 (D — do not change)

| Keep |
|---|
| Rows = 4B PASS/FAIL; Cols = 9B PASS/FAIL; b=4B-only; c=9B-only |

---

## 5. Color mapping rule for future edit pass

| Model identity | Color token | Hex (current) |
|---|---|---|
| Gemini 3.5 Flash | `COLORS["gemini"]` | `#4285F4` |
| Qwen3.5 9B | `COLORS["qwen9b"]` | `#D97706` |
| Qwen3.5 4B | `COLORS["qwen4b"]` | `#0F9D58` |

**Allowed:** reorder position arrays so color token stays with the same model.  
**Forbidden:** leave colors in place while swapping labels (would re-point color semantics).

---

## 6. Highest-risk locations (top 5)

1. **`render_figure_5`** — hardcoded posthoc `x=1` + value asserts tied to G→4B→9B positions.  
2. **`figure_01_baseline_overall.svg`** — order remake must preserve uncommitted **79/320** WT edit; generator still asserts **78**.  
3. **Final Report §15 + integrated multi-tables** — whole-column/row move hazard (header-only swap).  
4. **`render_figure_2`** — grouped offsets + legend + Gemini hatched slot identity.  
5. **One-Pager / Poster / 決賽 package copies** — multi-artifact desync.

---

## 7. Open blockers (not resolved this round)

1. Generator ↔ `frozen_numeric_claims` assert on 4B baseline **78** vs intended **79** presentation + WT Fig1/4 — ordering regen path needs a strategy that **does not edit frozen evidence**.  
2. Confirm `20260724/.../archive_or_working_notes/**` stays **F** while live integrated report under `docs/experiments/reports/` is **A**.  
3. Accept drift between excluded plain-path `math16_pilot02_final_report_v13.md` (**G**) and canonical `20260724` Final Report after future A edits — or define a later sync policy.  
4. Dual PNG trees (`visualization/` vs `決賽 supporting_assets/`) + presentation compact assets need an explicit copy-forward checklist.  
5. Confirm Figure 3 remains **D** (no forced 9B→4B side swap).  
6. Sequencing: baseline-79 amendment and model-order amendment both touch Figure 1 — compose, don’t clobber.

---

## 8. What this round did / did not do

**Did:** read-only inventory; add plan + CSV + JSON only.  
**Did not:** edit formal docs, SVG/PNG/PDF, generators; overwrite Fig1/Fig4 WT changes; rerun models/Healer/Evaluator; recompute stats; edit frozen evidence; commit/push; global search-and-replace; force two-model tables into trio; change color identity semantics.

---

## 9. Companion artifacts

- `docs/experiments/reports/math16_global_model_order_crosswalk_v1.csv`
- `docs/experiments/reports/math16_global_model_order_summary_v1.json`
