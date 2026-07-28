# Math16 Combined Amendment — Batch 0 Report v1

Report date: 2026-07-28  
Batch: **0 — scaffold presentation claims + WT backup + Correction Note presentation-order section**  
Result: **PASS**

## 1. Start state

| Item | Value |
|---|---|
| HEAD | `63564e959aea6164bad33a3794ea2a67778a08a5` |
| origin/main | `63564e959aea6164bad33a3794ea2a67778a08a5` (same as HEAD) |
| Tip subject | `docs: add Math16 Method 1 and Method 2 progress handoff` |

### Start `git status --short` (before Batch 0 writes)

```
 M docs/experiments/visualization/math16_pilot02_core_figures_v1/figure_01_baseline_overall.svg
 M docs/experiments/visualization/math16_pilot02_core_figures_v1/figure_04_tier1_paired_analysis.svg
?? docs/experiments/reports/_scratch_confirmatory_reeval_320/
?? docs/experiments/reports/math16_baseline_79_amendment_decision_record_v1.md
?? docs/experiments/reports/math16_baseline_79_amendment_plan_v1.md
?? docs/experiments/reports/math16_baseline_79_figure_amendment_spec_v1.md
?? docs/experiments/reports/math16_baseline_79_figure_render_validation_v1.md
?? docs/experiments/reports/math16_baseline_correction_note_v1.md
?? docs/experiments/reports/math16_combined_amendment_asset_map_v1.csv
?? docs/experiments/reports/math16_combined_amendment_execution_plan_v1.md
?? docs/experiments/reports/math16_combined_amendment_execution_summary_v1.json
?? docs/experiments/reports/math16_global_model_order_amendment_plan_v1.md
?? docs/experiments/reports/math16_global_model_order_crosswalk_v1.csv
?? docs/experiments/reports/math16_global_model_order_summary_v1.json
?? docs/experiments/reports/math16_method1_method2_78_79_discrepancy_audit_v1.md
?? docs/experiments/reports/math16_method1_method2_extraction_closure_320.csv
?? docs/experiments/reports/math16_method1_method2_extraction_closure_summary_v1.json
```

## 2. Consistency gate (claims vs decision record)

Compared presentation targets to `math16_baseline_correction_note_v1.md` §4–5 and `math16_baseline_79_amendment_decision_record_v1.md` §2–4:

| Claim | Expected | Status |
|---|---|---|
| Baseline | 79/320 | match |
| Final | 85/320 | match |
| Verified rescue | 6 | match |
| Overall 4B-only / BOTH_FAIL | 27 / 192 | match |
| Overall McNemar p | 0.015440 | match |
| Overall RD / OR / Wald CI / bootstrap CI | +6.875% / 1.81 / [0.0159, 0.1216] / [−0.0156, 0.1437] | match |
| Polynomial 4B / 4B-only / p | 17/80 / 14 / 0.1153 | match |

**Gate: PASS** — no BLOCKED; numbers not rewritten.

## 3. Files created / modified by Batch 0

### Created

| Path | Role |
|---|---|
| `docs/experiments/visualization/math16_pilot02_amendment_layer_v1/presentation_claims_v1.json` | presentation-only claims SOT for later batches |
| `docs/experiments/visualization/math16_pilot02_amendment_layer_v1/wt_backup/figure_01_baseline_overall.svg` | rollback copy of WT Fig1 |
| `docs/experiments/visualization/math16_pilot02_amendment_layer_v1/wt_backup/figure_04_tier1_paired_analysis.svg` | rollback copy of WT Fig4 |
| `docs/experiments/visualization/math16_pilot02_amendment_layer_v1/wt_backup/rollback_manifest_v1.json` | SHA-256 + path manifest |
| `docs/experiments/visualization/math16_pilot02_amendment_layer_v1/staging/.gitkeep` | empty staging scaffold |
| `docs/experiments/reports/math16_combined_amendment_batch0_report_v1.md` | this report |

### Modified

| Path | Change |
|---|---|
| `docs/experiments/reports/math16_baseline_correction_note_v1.md` | Added §10 presentation-order adjustment; renumbered prior §10 → §11 |

### Explicitly not modified

- Canonical / WT Fig1 & Fig4 SVG sources (copied only; SHA unchanged vs backup)
- Any formal main report, Jury Q&A, Method 1/2, Integrated, One-Pager, Poster
- Any generator; frozen evidence; `results/**`; manifests; protocols; milestones; tests
- `docs/決賽文件/實驗結果文件/20260722_Math16/**`
- `docs/experiments/reports/math16_pilot02_final_report_v13.md`

## 4. Claims schema summary

`presentation_claims_v1.json`:

- `status` = `presentation_only_amendment`
- `model_order` = Gemini 3.5 Flash → Qwen3.5 9B → Qwen3.5 4B (`G→9→4`)
- `model_color_identity` = gemini `#4285F4`, qwen9b `#D97706`, qwen4b `#0F9D58`
- Headline: Baseline **79/320**, Final **85/320**, Verified rescue **6**
- `tier1_overall_amended_4b_vs_9b`: matrix 52/27/49/192; p=0.01544; RD=+6.875%; OR=1.81; Wald/bootstrap CIs as decision record
- `polynomial_family_amended_4b_vs_9b`: 17/80, 14 four-b-only, p=0.1153
- Governance: not raw evidence; must not overwrite `frozen_numeric_claims`; must not write `results/**`; frozen pipeline baseline remains **78/320**

**Claims SHA-256:** `1e924eee38d193ea44abba6a9a6bf8209fdd71675d89eb278fe780cc0c5d05cc`

## 5. Rollback backup SHA-256

| Source | Backup | SHA-256 |
|---|---|---|
| `…/core_figures_v1/figure_01_baseline_overall.svg` | `…/amendment_layer_v1/wt_backup/figure_01_baseline_overall.svg` | `608a3aa4a2f3cb3b4387c81177e3952c05575039f22fb84829f718a9e523860c` |
| `…/core_figures_v1/figure_04_tier1_paired_analysis.svg` | `…/amendment_layer_v1/wt_backup/figure_04_tier1_paired_analysis.svg` | `0b7f004abf518db36a55b868b88618c6074574d7140d4145dd3d871e998fcf79` |

Source ↔ backup byte-identical verified. Sources not restored, overwritten, or regenerated.

## 6. Correction Note update

**Yes — supplemented.** Added **§10 Presentation-order adjustment (not a data correction)**:

- Unified trio order G→9→4 for reading consistency
- Only column/row/legend/position/enumeration order
- Does not change model values, identity, colors, stats, or conclusions
- Two-model paired analyses keep structure
- Explicitly **not** described as a data-error fix

## 7. Forbidden-scope confirmation

| Forbidden class | Touched? |
|---|---|
| Formal reports / Jury / Method / Integrated / One-Pager / Poster | No |
| Canonical SVG/PNG/PDF (other than pre-existing WT M status) | No new edits |
| Fig1/Fig4 WT content | No (backup only) |
| Generators | No |
| Model/Healer/Evaluator rerun; stats recompute | No |
| Frozen evidence / results / manifest / protocol / milestone / tests | No |
| `20260722_Math16/**` | No |
| plain-path `math16_pilot02_final_report_v13.md` | No |
| commit / push | No |
| Batches 1–7 | Not executed |

## 8. Batch 0 verdict

**PASS**

Next gate (not executed this round): Batch 1 may start only after this report and `presentation_claims_v1.json` exist with schema OK.
