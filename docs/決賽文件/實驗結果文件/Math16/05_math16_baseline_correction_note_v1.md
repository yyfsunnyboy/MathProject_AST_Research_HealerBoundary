# Math16 Baseline Correction Note v1

Note date: 2026-07-28
Status: **formal correction note, analysis/reporting layer only.** This note documents a human-approved correction to reported Qwen 4B pass counts. It does not modify, and is not itself, frozen evidence. No frozen results/journal/manifest/protocol/test file is changed by this note or by the correction it documents.

## 1. What is frozen and never changes

- The frozen pipeline's raw output for Qwen 4B Baseline remains **78/320 forever** in every results/journal/manifest/protocol/test file where it was originally recorded. These files are never modified as part of this or any correction: `docs/experiments/results/math16_pilot02_qwen4b_evaluation_v4_r001/*`, `docs/experiments/results/math16_pilot02_qwen4b_healer_v4_r001/*`, `docs/experiments/results/math16_pilot02_qwen4b_healer_v4_posthoc_corrected_chain_r001/*`, `docs/experiments/manifests/*`, the pinned Evaluator/Protocol scripts (`scripts/evaluate_math16_pilot02_qwen4b_healer_v4.py`, `scripts/evaluate_math16_pilot02_qwen4b_healer_v4_posthoc_corrected_chain.py`, `scripts/evaluate_math16_pilot02_full_v4.py`), and all `tests/test_math16_*.py` regression tests pinned to `"78/320"`/`"83/320"`/`"84/320"`-style assertions.
- **This correction happens only at the analysis/reporting layer** — narrative reports, appendices, figures, and derived statistical analyses that cite the frozen numbers, never the frozen evidence itself.

## 2. Root cause (concise recap)

Method 1's original v4 baseline pipeline computed two different hash fields for cell `qwen3_5_4b__ce115_calc_polynomial_division_l1__ab1__seed_2026072003`: a correctly-extracted `candidate_hash` and a separate `raw_artifact_sha256` that was actually scored at `g1_parse`. The scored artifact was mis-bounded — the extractor anchored on a spurious in-prose ``` ``` ``` sequence inside the model's own commentary rather than the real code fence — producing a truncated/malformed candidate that failed to parse (`catastrophic_truncation`). Method 2's independently re-extracted raw source for the same cell is byte-identical to Method 1's own already-computed (but unused) `candidate_hash`, and parses and PASSES under the same pinned evaluator.

Evaluator, task, condition, and seed are identical between methods for this cell; only the candidate-extraction artifact-selection differed. This is documented in full in `docs/experiments/reports/math16_method1_method2_78_79_discrepancy_audit_v1.md` (Sections 2–3, 5–6).

## 3. Audit / confirmatory-re-evaluation evidence chain

- `docs/experiments/reports/math16_method1_method2_78_79_discrepancy_audit_v1.md` — full cell-by-cell diff across all 320 cells (exactly one disagreement), raw-source identity check, evaluator identity check, root-cause trace, and a Section 10 extension performing a full 320-cell closure sweep plus a confirmatory re-invocation of the pinned evaluator's scoring logic against both methods' sources with zero LLM/Healer calls. Result: 78/320 reproduced exactly against Method 1's own scored artifacts, 79/320 reproduced exactly against Method 2's canonical raw sources, zero mismatches either direction.
- `docs/experiments/reports/math16_method1_method2_extraction_closure_320.csv` — full 320-row crosswalk supporting the sweep.
- `docs/experiments/reports/math16_method1_method2_extraction_closure_summary_v1.json` — machine-readable summary of the closure sweep and the proposed correction list.
- `docs/experiments/reports/math16_baseline_79_amendment_plan_v1.md` — full repo hit inventory (114 files) of every location stating the pre-correction numbers, with per-file disposition (edit / correction-note-link-only / never-touch).
- `docs/experiments/reports/math16_baseline_79_amendment_decision_record_v1.md` — recomputation of the Tier-1 Qwen 4B vs Qwen 9B paired statistics (McNemar, Wald CI, task-clustered bootstrap CI, odds ratio) under the corrected ledger, and the file classification lists (A/B/C/D) resolving which artifacts must move in lockstep.

## 4. Corrected headline numbers (human-approved, adopted)

- **Baseline: 78/320 (24.38%) → 79/320 (24.69%)**
- **Final: 84/320 → 85/320**
- **Verified rescue = 6** (unchanged — the corrected cell is `healer_eligible: false` and was never in the rescue population)
- **Primary 84/320 is demoted to appendix/correction-note-only status** and is not shown in main results tables. (Primary is the pre-correction intermediate figure that arithmetically becomes 83→84/320 once Baseline moves 78→79; per adopted principle it is not surfaced as a main-table headline.)
- Method 1 Regression: **not measured**. Method 2 Regression: **measured 0/320**.

## 5. Old vs new statistics

### 5.1 Overall Qwen 4B vs Qwen 9B paired matrix (320 pairs)

| Statistic | OLD (Baseline 78/320) | NEW (Baseline 79/320) |
|---|---:|---:|
| 4B PASS total | 78 (24.38%) | 79 (24.69%) |
| 9B PASS total | 101 (31.56%) | 101 (31.56%) |
| BOTH_PASS | 52 | 52 |
| FOUR_B_ONLY_PASS | 26 | 27 |
| NINE_B_ONLY_PASS | 49 | 49 |
| BOTH_FAIL | 193 | 192 |
| Paired risk difference (c−b)/n | +7.1875% | +6.8750% |
| Exact two-sided McNemar p | 0.010582 | 0.015440 |
| Wald 95% CI | [0.0194, 0.1243] | [0.0159, 0.1216] |
| Task-clustered bootstrap 95% CI (seed=42, 10,000 resamples) | [−0.0094, 0.1437] | [−0.0156, 0.1437] |
| Matched-pairs odds ratio (c/b) | 1.88 | 1.81 |

### 5.2 Polynomial family only (80 pairs)

| Statistic | OLD | NEW |
|---|---:|---:|
| 4B PASS | 16/80 (20.0%) | 17/80 (21.25%) |
| 9B PASS | 9/80 (11.25%) | 9/80 (11.25%) |
| FOUR_B_ONLY_PASS | 13 | 14 |
| BOTH_FAIL | 58 | 57 |
| Paired risk difference | −8.75% | −10.00% |
| Exact two-sided McNemar p | 0.1671 | 0.1153 |

## 6. No qualitative research conclusion changes

- The overall claim that Qwen 9B's paired baseline pass rate is statistically significantly higher than Qwen 4B's still holds: McNemar p moves from 0.0106 to 0.0154, both `< 0.05`; Wald CI still excludes zero.
- The task-clustered bootstrap CI already crossed zero before the correction and continues to cross zero after (a secondary robustness check, not the Confirmatory significance claim).
- The polynomial-family reversal claim (9B < 4B locally, not globally interpretable, non-significant) still holds and is slightly reinforced (gap widens from −7 to −8 cells; p moves from 0.1671 to 0.1153, still `> 0.05`).
- Odds ratio moves from 1.88 to 1.81 — same direction, no threshold crossed.
- **No sign flip, no crossing of the 0.05 significance boundary in either direction, for any statistic.** Full detail in `docs/experiments/reports/math16_baseline_79_amendment_decision_record_v1.md` Sections 2–5.

## 7. Frozen artifacts, never modified

Reiterating Section 1: all raw evaluation results, Healer/Eligibility journals, corrected-chain evidence, generation-time artifacts, manifests, pinned Evaluator/Protocol scripts, and the 16 `tests/test_math16_*.py` / `tests/finals_rebuild/test_math16_healer_revalidation_false_loop.py` regression test files retain their historical 78/83/84 values permanently. Any future engineering change to those pinned test assertions (should the underlying evidence ever be regenerated) is a separate, coordinated engineering task, explicitly out of scope for this documentation/analysis-layer correction.

`docs/experiments/reports/math16_healer_rule_provenance_audit_v1.md` and its manifest carry an explicit self-imposed no-edit clause on the Primary(83)/Corrected(84) accounting and are never touched by this note; this note only cross-references it.

## 8. Canonical main report and exclusion scope

The single canonical, official main report for this experiment is:

**`docs/決賽文件/實驗結果文件/20260724_Math16/01_math16_pilot02_final_report_v13.md`**

**Working mirror（非第三份 Final Report）：** `docs/決賽文件/實驗結果文件/Math16/01_math16_pilot02_final_report_v13.md` 為編輯工作副本；可暫時含超前草稿，但 A／B／C 等交付主張必須同步回上述 canonical，且不以 working mirror 取代 protected-SHA 交付正文。

**`docs/決賽文件/實驗結果文件/20260722_Math16/**` (the entire directory) is excluded completely from this correction note and from all correction work of any kind associated with this effort**: no edit, no sync, no link, no chart regeneration, ever. It is treated as an immutable historical archive of an earlier process snapshot, separate from and not to be conflated with the canonical `20260724_Math16/` copy.

## 9. Per-figure and per-document amendment specification

Detailed per-figure literal-text/value changes (Figures 1, 3, 4, 5) are specified separately in `docs/experiments/reports/math16_baseline_79_figure_amendment_spec_v1.md`. Figure 1、3、4、5 已完成更正後重繪，現行正式圖檔位於 `figures/`。

## 10. Presentation-order adjustment (not a data correction)

Separately from the Baseline 78→79 numeric correction above, current-facing presentation surfaces adopt a **unified three-model display order**:

**Gemini 3.5 Flash → Qwen3.5 9B → Qwen3.5 4B**

- **Why:** improve intuitive cross-document reading consistency across tables, figures, legends, and prose lists.
- **What changes:** column/row order, legend order, spatial position, and textual enumeration order only.
- **What does not change:** model numeric values, model identity, color identity (Gemini `#4285F4`, Qwen 9B `#D97706`, Qwen 4B `#0F9D58`), statistical definitions, or research conclusions.
- **Two-model paired analyses** (e.g., Fig3 family bars, Fig4 Tier-1 McNemar) keep their existing statistical structure; they are not forced into a three-model reorder.

This section is a **presentation consistency rule**, not a claim that prior model-order text was a data error, and it must not be described as a numeric correction.

## 11. File modification confirmation

This note originated as analysis/reporting documentation only. Batch 0 of the combined amendment may append Section 10 (presentation-order rule) without altering Sections 1–9 settled numbers or frozen-evidence scope. No frozen evidence, results, journal, Healer, Eligibility, Evaluator, Protocol, Manifest, or test file is touched by this note. No git commit is made by Batch 0.

## 12. Delivery Final Report protected-SHA refresh（文件完整性治理）

針對 `tests/test_math16_delivery_provenance_alignment.py` 之 `FROZEN_SHA_FINAL_REPORT_V13_DELIVERY`（對應 canonical `20260724_Math16/01_math16_pilot02_final_report_v13.md`）：

1. Pin 建立於 commit `e7cb0431`（2026-07-27，Gemini post-hoc inventory labeling）。
2. 自 commit `daeb581991`（2026-07-28，Method 1 Development 40／Evaluation 120 合法正文整合）起，pin 與現行正文開始不一致。
3. 其後多次授權文件更新均已進入 Git，但 delivery protected-SHA pin 未同步刷新。
4. 本次刷新 pin 僅對齊**現行 canonical 交付正文**（含 A／B／C 段落級同步後之 raw-byte SHA），**不代表**回復舊版正文，亦**不改寫** raw evidence、journals、protocol、runner、Healer rules 或 evaluator 輸出。
