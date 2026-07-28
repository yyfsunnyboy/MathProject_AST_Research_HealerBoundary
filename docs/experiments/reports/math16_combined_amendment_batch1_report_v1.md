# Math16 Combined Amendment — Batch 1 Report v1

Report date: 2026-07-28  
Batch: **1 — claims completion + amendment renderer/spec + schema validation + staging dry-run**  
Result: **PASS**

## 1. Scope executed

- Updated `presentation_claims_v1.json` with trio totals / FAIL order / Final fail+rate + figure payload fields
- Added `scripts/render_math16_pilot02_amended_figures_v1.py`
- Added `amendment_renderer_spec_v1.json`
- Schema validation PASS
- Staging dry-run for Figures 1, 2, 3, 5 only
- Did **not** execute Batches 2–7; did **not** promote; did **not** modify canonical figures

## 2. Claims update

| | SHA-256 |
|---|---|
| Before Batch 1 | `1e924eee38d193ea44abba6a9a6bf8209fdd71675d89eb278fe780cc0c5d05cc` |
| After Batch 1 | `f7014b6e69e3d46fe210a24f55a03a66795d312bc1efb7371d8e9a5053363fc7` |

### Fields added / completed

- `schema_version` = `1.1.0`
- `updated_by_batch` = 1
- `three_model_totals` (Gemini 289/31, 9B 101/219, 4B 79/241; all total 320)
- `three_model_fail_ordered` (`model_order` G→9→4; `fail_counts`=[31,219,241])
- `headline_presentation.baseline.fail` = 241
- `headline_presentation.final.fail` = 235, `rate_pct` = 26.56
- `figure_02_condition_scores` (presentation-only condition cells)
- `figure_03_family_pass_counts` (Polynomial 4B = 17)
- `figure_05_healer_boundary` (FAIL/Eligible/Verified-rescue in G→9→4; Primary 84 demoted)

### Arithmetic verification

| Check | Result |
|---|---|
| 289+31=320 | PASS |
| 101+219=320 | PASS |
| 79+241=320 | PASS |
| 85+235=320 | PASS |
| baseline `rate_pct`=24.69 | PASS |
| final `rate_pct`=26.56 | PASS |
| 85−79 = verified_rescue 6 | PASS |
| fail_counts identity == three_model_totals.fail in G→9→4 | PASS |
| Overall / Polynomial amended stats vs decision record | PASS |
| frozen declaration remains 78/320 | PASS |

## 3. Claims schema validation

**PASS** (`python scripts/render_math16_pilot02_amended_figures_v1.py --validate-only` / full dry-run gate)

Required fields present; trio unique and ordered; Baseline/Final/rescue arithmetic consistent; FAIL triplet [31,219,241]; Overall/Polynomial match decision record; frozen 78 not rewritten.

## 4. Renderer / spec

| Artifact | Path | SHA-256 |
|---|---|---|
| Renderer | `scripts/render_math16_pilot02_amended_figures_v1.py` | `e3f9599ab91b1e7144c967719f60987f19e68451c48fb6df279c1a13cd97dd04` |
| Spec | `docs/experiments/visualization/math16_pilot02_amendment_layer_v1/amendment_renderer_spec_v1.json` | (see file; claims/renderer SHAs embedded) |

Renderer rules observed:

- Reads only `presentation_claims_v1.json`
- Does not read/write `frozen_numeric_claims.json` or `results/**`
- Does not modify frozen core-figure builder
- Writes only under `amendment_layer_v1/staging/`
- Fig4 not recomputed; Fig6 not handled
- Colors identity-bound; order Gemini→9B→4B

## 5. Staging dry-run outputs

| Figure | File | SHA-256 | Verdict |
|---|---|---|---|
| 1 | `…/staging/figure_01_baseline_overall.staging.svg` | `455297d4893eec022bca770c6a32fe8208c381ad2d54c526b411f8b3a1c801db` | **PASS** |
| 2 | `…/staging/figure_02_condition_breakdown.staging.svg` | `bc2feed3c5b5bebf9e08886d035bde8a450c47db5c99deb2634b076f100ba277` | **PASS** |
| 3 | `…/staging/figure_03_family_breakdown.staging.svg` | `a5240cc79b4196121441a9962f39fc6b0de9bb4b94cb7106852843500d58e9b2` | **PASS** |
| 5 | `…/staging/figure_05_healer_eligibility_boundary.staging.svg` | `19930f2665ea6250b13ffe140b3bb1a064e0e57e20f678a832d5dffec4f57b13` | **PASS** |

### Per-figure checks

- **Fig1:** 79/320 + 289/320 + 101/320; order Gemini→9B→4B; identity colors; no `78/320` residual in figure text
- **Fig2:** group/legend/hatch order Gemini→9B→4B; identity colors
- **Fig3:** Polynomial 16/80→17/80; two-model structure retained; no `16/80` label residual
- **Fig5:** Baseline 79/241; Final 85/235; Verified rescue=6; FAIL=[31,219,241]; G→9→4; no Primary 84 / 83 / 242 label residuals

No Figure 4 or 6 staging files written. No canonical SVG overwrite.

## 6. Canonical zero-change confirmation

| Canonical path | SHA-256 (unchanged) |
|---|---|
| `…/core_figures_v1/figure_01_baseline_overall.svg` | `608a3aa4a2f3cb3b4387c81177e3952c05575039f22fb84829f718a9e523860c` |
| `…/core_figures_v1/figure_04_tier1_paired_analysis.svg` | `0b7f004abf518db36a55b868b88618c6074574d7140d4145dd3d871e998fcf79` |

Matches Batch 0 WT backup SHAs. Fig1/Fig4 WT content not modified this batch.

## 7. Forbidden-scope confirmation

| Forbidden class | Touched? |
|---|---|
| Canonical SVG/PNG/PDF | No |
| Formal reports / Jury / Method / Integrated / One-Pager / Poster | No |
| Frozen core-figure builder | No |
| `frozen_numeric_claims` / results / journals / manifests / protocols / tests | No |
| Model/Healer/Evaluator rerun; stats recompute | No |
| commit / push | No |
| Batches 2–7 | Not executed |

## 8. Batch 1 verdict

**PASS**

Gate for later batches: staging dry-run artifacts + claims schema + renderer/spec exist; promotion remains Batch 3+.
