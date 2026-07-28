# Math16 Baseline 79/320 Amendment — Decision Record v1

Record date: 2026-07-28
Status: **decision record, analysis/reporting layer only.** No frozen evidence, results, journal, Healer, Eligibility, Evaluator, Protocol, Manifest, or test file was modified in producing this record. No existing tracked file was edited. The only file created is this record. All statistics below were recomputed in-memory from the existing frozen cell-level ledger (`paired_cell_ledger.jsonl`) by applying the already-audited single-cell correction; no model or Healer was re-run.

## 0. Basis for this record

This record closes out the remaining governance blockers from `docs/experiments/reports/math16_baseline_79_amendment_plan_v1.md` (specifically Blocker #6, the Tier 1 4B-vs-9B paired statistical analysis) and answers the question the amendment plan explicitly left open: **does the one-cell Baseline correction (78/320 → 79/320) change the Qwen 4B vs Qwen 9B paired statistical conclusion?**

Inputs read (all pre-existing, all read-only):
- `docs/experiments/reports/math16_method1_method2_78_79_discrepancy_audit_v1.md`
- `docs/experiments/reports/math16_method1_method2_extraction_closure_320.csv` / `_summary_v1.json`
- `docs/experiments/reports/math16_baseline_79_amendment_plan_v1.md`
- `docs/experiments/results/math16_pilot02_qwen4b_vs_qwen9b_tier1_paired_analysis_v1/{analysis_report.md, paired_cell_ledger.jsonl, overall_paired_summary.json, condition_paired_summary.json, family_paired_summary.json, bootstrap_summary.json, seed_stability_summary.json, task_level_summary.json, analysis_manifest.json}`
- `scripts/analyze_math16_pilot02_qwen4b_vs_qwen9b_tier1_paired.py` (methodology source — exact McNemar via `Binomial(b+c, 0.5)`, Wald CI, task-clustered bootstrap: 16 tasks resampled with replacement, `random.seed(42)`, 10,000 resamples, 2.5/97.5 percentile CI)

Corrected cell: `qwen3_5_4b__ce115_calc_polynomial_division_l1__ab1__seed_2026072003` — task `ce115_calc_polynomial_division_l1`, family `polynomial`, condition `ab1`, seed `2026072003`. Method 1 baseline `final_status` corrected FAILED → PASSED (extraction artifact-selection bug, confirmed root cause, `healer_eligible: false`).

## 1. Qwen 9B status for the same cell, and quadrant movement

From `paired_cell_ledger.jsonl`, pair `pair_264`, key `ce115_calc_polynomial_division_l1__ab1__seed_2026072003`:

- **Qwen 9B `final_status` for this exact task/condition/seed = FAILED** (`qwen9b_passed: false`). Unaffected by this correction — no change proposed or evidence found for the 9B side.
- **Quadrant before correction**: 4B=FAIL, 9B=FAIL → **`BOTH_FAIL`**.
- **Quadrant after correction**: 4B=PASS, 9B=FAIL → **`FOUR_B_ONLY_PASS`** (i.e. this cell becomes a 4B-only-pass discordant pair).

Net effect on the paired ledger: `BOTH_FAIL` count decreases by 1 (193→192), `FOUR_B_ONLY_PASS` count increases by 1 (26→27). `BOTH_PASS` (52) and `NINE_B_ONLY_PASS` (49) are unaffected.

## 2. OLD vs NEW overall 2×2 matrix (320 pairs)

| | Qwen 9B PASS | Qwen 9B FAIL | Total (Qwen 4B) |
|---|---:|---:|---:|
| **OLD — Qwen 4B PASS** | 52 (`BOTH_PASS`) | 26 (`FOUR_B_ONLY_PASS`) | 78 (24.38%) |
| **OLD — Qwen 4B FAIL** | 49 (`NINE_B_ONLY_PASS`) | 193 (`BOTH_FAIL`) | 242 (75.62%) |
| **OLD — Total (9B)** | 101 (31.56%) | 219 | 320 |

| | Qwen 9B PASS | Qwen 9B FAIL | Total (Qwen 4B) |
|---|---:|---:|---:|
| **NEW — Qwen 4B PASS** | 52 (`BOTH_PASS`) | **27** (`FOUR_B_ONLY_PASS`) | **79** (24.69%) |
| **NEW — Qwen 4B FAIL** | 49 (`NINE_B_ONLY_PASS`) | **192** (`BOTH_FAIL`) | 241 (75.31%) |
| **NEW — Total (9B)** | 101 (31.56%) | 219 | 320 |

Qwen 9B totals (101, 31.56%) are unchanged in both matrices — only the Qwen 4B row and the `FOUR_B_ONLY_PASS`/`BOTH_FAIL` cells move.

## 3. OLD vs NEW Polynomial-family 2×2 matrix (80 pairs: 4 conditions × 5 seeds × 4 polynomial tasks)

| | OLD 9B PASS | OLD 9B FAIL | OLD Total (4B) |
|---|---:|---:|---:|
| **4B PASS** | 3 (`BOTH_PASS`) | 13 (`FOUR_B_ONLY_PASS`) | 16/80 |
| **4B FAIL** | 6 (`NINE_B_ONLY_PASS`) | 58 (`BOTH_FAIL`) | 64/80 |
| **Total (9B)** | 9/80 | 71 | 80 |

| | NEW 9B PASS | NEW 9B FAIL | NEW Total (4B) |
|---|---:|---:|---:|
| **4B PASS** | 3 (`BOTH_PASS`) | **14** (`FOUR_B_ONLY_PASS`) | **17/80** |
| **4B FAIL** | 6 (`NINE_B_ONLY_PASS`) | **57** (`BOTH_FAIL`) | 63/80 |
| **Total (9B)** | 9/80 | 71 | 80 |

Polynomial family 9B pass total (9/80) unchanged.

## 4. OLD vs NEW statistics

### 4.1 Overall (320 pairs)

| Statistic | OLD (Baseline 78/320) | NEW (Baseline 79/320) |
|---|---:|---:|
| 4B PASS total | 78 (24.38%) | 79 (24.69%) |
| 9B PASS total | 101 (31.56%) | 101 (31.56%) |
| Discordant `b` (4B-only) | 26 | **27** |
| Discordant `c` (9B-only) | 49 | 49 |
| Net difference (`c − b`) | +23 | **+22** |
| Paired risk difference `(c−b)/n` | +7.1875% (+0.0719) | **+6.8750% (+0.0688)** |
| Exact two-sided McNemar `p` | 0.010582 (reported 0.0106) | **0.015440** |
| Wald 95% CI | [0.0194, 0.1243] | **[0.0159, 0.1216]** |
| Task-clustered bootstrap 95% CI (10,000 resamples, seed=42) | [−0.0094, 0.1437] | **[−0.0156, 0.1437]** |
| Matched-pairs odds ratio `c/b` | 1.88 | **1.81** (49/27 = 1.8148) |

The Wald CI, bootstrap CI, and McNemar `p` were all recomputed by re-running the exact same formulas/RNG sequence from `scripts/analyze_math16_pilot02_qwen4b_vs_qwen9b_tier1_paired.py` against the corrected ledger (task-clustered bootstrap reruns the identical `random.seed(42)` / 16-tasks-with-replacement / 10,000-resample procedure; only the per-cell pass/fail values feeding the aggregation differ for the one corrected pair).

### 4.2 Polynomial family only (80 pairs)

| Statistic | OLD | NEW |
|---|---:|---:|
| 4B PASS | 16/80 (20.0%) | **17/80 (21.25%)** |
| 9B PASS | 9/80 (11.25%) | 9/80 (11.25%) |
| Discordant `b` (4B-only) | 13 | **14** |
| Discordant `c` (9B-only) | 6 | 6 |
| Net difference (`c − b`) | −7 | **−8** |
| Paired risk difference | −8.75% (−0.0875) | **−10.00% (−0.1000)** |
| Exact two-sided McNemar `p` | 0.1671 | **0.1153** |
| Task-clustered bootstrap 95% CI | [−0.2750, 0.0750] | **[−0.3125, 0.0625]** |

## 5. Does the qualitative conclusion change?

**No — the qualitative conclusion direction and significance calls are unchanged.**

- **Overall claim** ("Qwen 9B's paired baseline pass rate is statistically significantly higher than Qwen 4B's, controlling for task/condition/seed"): still holds. `p` moves from 0.0106 to 0.0154 — both `< 0.05`, so the McNemar significance call does **not** cross the 0.05 threshold in either direction. The Wald CI ([0.0159, 0.1216]) still excludes zero, same as before ([0.0194, 0.1243]).
- **One caveat introduced**: the **task-clustered bootstrap 95% CI**, which already crossed zero before the correction ([−0.0094, 0.1437]), now crosses zero by a slightly wider margin ([−0.0156, 0.1437]). This does not change any stated conclusion — the existing report (§8, Multiple Comparisons Governance) already treats the bootstrap CI as a secondary robustness check that does not itself carry the Confirmatory significance claim (only the overall exact McNemar test is Confirmatory), and that CI already crossed zero pre-correction. No report text needs to change its qualitative claim on this point, only its printed CI bounds.
- **Polynomial-family reversal claim** ("Polynomial shows a localized reverse difference, 9B < 4B, not globally interpretable as 9B math-ability regression"): still holds, and is in fact *slightly reinforced* — the reverse gap widens from −7 to −8 cells and `p` moves from 0.1671 to 0.1153 (still `> 0.05`, still non-significant, still framed as exploratory/non-confirmatory per §8 of the existing report). No sign flip, no crossing of the 0.05 boundary in either family-level or overall statistics.
- **Odds ratio**: 1.88 → 1.81. Same qualitative direction (9B favored), no threshold crossed.
- **Task/seed-level qualitative claims** (9B ahead in all 5 seeds; `ce115_calc_polynomial_division_l1` as the single-task driver of the polynomial reversal) are unaffected — the corrected cell (seed 2026072003, condition `ab1`) was already inside that flagged task and already contributing to seed 2026072003's and the polynomial family's counts as a `BOTH_FAIL`; it now contributes as a `FOUR_B_ONLY_PASS`, which if anything makes the existing task-level and seed-level narrative (already isolating this task/family as the exception) more precise, not different in kind.

**Net verdict: no qualitative conclusion reverses. Every previously-significant result stays significant; every previously-non-significant result stays non-significant. Point estimates and CI bounds shift by small amounts consistent with a single-cell correction out of 320.**

## 6. Which existing charts/report figures/numbers would need to move in lockstep

If Baseline 79/320 is formally adopted, the following Tier-1 paired-analysis artifacts contain numbers that are now stale and would need regeneration/update in lockstep (this record does not edit them):

- `docs/experiments/results/math16_pilot02_qwen4b_vs_qwen9b_tier1_paired_analysis_v1/analysis_report.md` — §2 (78→79), §3.1 table and stats (26→27, 193→192, 24.38%→24.69%, p 0.0106→0.0154, OR 1.88→1.81, both CIs), §4 `ab1` condition row (see Section 8 below), §5 polynomial family row, §9 conservative conclusions text.
- `docs/experiments/results/math16_pilot02_qwen4b_vs_qwen9b_tier1_paired_analysis_v1/overall_paired_summary.json` — `qwen4b_baseline_pass`, `qwen4b_baseline_pass_rate`, `paired_contingency_table.FOUR_B_ONLY_PASS`, `paired_contingency_table.BOTH_FAIL`, `net_difference`, `paired_risk_difference`, `wald_95_ci`, `bootstrap_task_clustered_95_ci`, `exact_mcnemar_pvalue`, `matched_pairs_odds_ratio`.
- `condition_paired_summary.json` (the `ab1` entry) and `family_paired_summary.json` (the `polynomial` entry).
- `paired_cell_ledger.jsonl` — pair_264's `qwen4b_status`/`qwen4b_passed`/`pair_category`.
- `bootstrap_summary.json`, `seed_stability_summary.json` (seed `2026072003` row: 4B PASS 14→15, net difference +9→+8), `task_level_summary.json` (`ce115_calc_polynomial_division_l1` row: 4B PASS 6→7, net −6→−7).
- `scripts/analyze_math16_pilot02_qwen4b_vs_qwen9b_tier1_paired.py` — this is the generator; correcting the outputs above is properly done by re-running this script against a corrected 4B baseline source, not by hand-patching the JSON/MD outputs.
- Downstream: any main-report table/abstract text or figure that cites the 78/320 Tier-1 comparison figure (78 vs 101, McNemar p=0.0106, OR 1.88) — per the existing amendment plan (Blocker #6), this includes the Final Report's/One-Pager's/Poster's Tier-1 comparison callouts wherever they quote `78 (24.38%)` in the 4B-vs-9B context, not just the Method-1-only Baseline callouts already inventoried there.

This record intentionally does **not** regenerate any of the above files — it only establishes, by independent recomputation from the frozen ledger, what the corrected numbers would be, so a future engineering pass can apply them without re-deriving the statistics from scratch.

### Supplementary: `ab1` condition-level shift (not requested as a primary deliverable, included for completeness since the corrected cell is inside `ab1`)

| | OLD `ab1` | NEW `ab1` |
|---|---:|---:|
| 4B PASS | 15/80 | **16/80** |
| BOTH_PASS / 4B-only / 9B-only / BOTH_FAIL | 12 / 3 / 6 / 59 | 12 / **4** / 6 / **58** |
| Exact McNemar `p` | 0.5078 | **0.7539** |

No significance-threshold crossing here either (both non-significant, `p > 0.05`).

## 7. Frozen-evidence-untouched principle (restated)

- Frozen raw evaluation records (`cell_level_baseline.jsonl` for both Qwen 4B and Qwen 9B, `overall_summary.json`, `baseline_summary.json`, all condition/family/task/seed summary JSONs under `math16_pilot02_qwen4b_evaluation_v4_r001/` and `math16_pilot02_qwen9b_evaluation_v4_r001/`), Healer/Eligibility journals, Evaluator/Protocol/Manifest files, and all pinned test assertions **retain their historical "78" (and derived "83"/"84") values and are never modified** by this record or by adopting the correction. They remain the permanent record of what was originally scored.
- Any correction — including the recomputed Tier-1 paired statistics in Sections 2–6 above — happens **only at the analysis/reporting layer**: a documented, evidence-backed recomputation layered on top of the frozen evidence, never a silent overwrite of the frozen evidence itself.
- `docs/experiments/reports/math16_healer_rule_provenance_audit_v1.md` and its manifest keep their explicit self-imposed no-edit clause on the Primary(83)/Corrected(84) accounting; that file is **not** touched by this record. This record's existence — a new, separate, evidence-backed decision record that only references and cross-links to the provenance audit — is the permitted mechanism: it layers a formal amendment on top without rewriting or silently overwriting the provenance audit's own numbers.
- The single canonical, official main report for this experiment remains `docs/決賽文件/實驗結果文件/20260724_Math16/01_math16_pilot02_final_report_v13.md`; this record does not edit it. `math16_pilot02_integrated_results_report_v1.md` remains classified as a supporting/secondary report and is not treated as a replacement for the canonical main report.

## 8. File classification lists

### List A — MUST be edited (or regenerated) in a future edit round (formal external-facing docs/figures, and the derived Tier-1 paired-analysis layer)

1. `docs/決賽文件/實驗結果文件/20260724_Math16/01_math16_pilot02_final_report_v13.md` — **canonical main report** (per task decision). Abstract + main tables: Baseline 78→79/320, Final 83→85/320 (demoting intermediate Primary 84 per adopted principle), Tier-1 4B-vs-9B comparison callouts (78→79, McNemar p 0.0106→0.0154, OR 1.88→1.81).
2. `docs/experiments/reports/math16_pilot02_final_report_v13.md` — synchronized copy (plain-path v13); update in lockstep with #1.
3. `docs/experiments/reports/math16_method1_40_120_split_results_report_v1.md` — Method 1 report; Baseline 78→79, Primary/corrected-chain figures demoted to appendix per adopted principle.
4. `docs/experiments/reports/math16_method2_all_cell_results_report_v1.md` — cross-reference update (Method 1 now matches Method 2 at 79/320 for this cell).
5. `docs/experiments/reports/math16_pilot02_jury_qa_final_v1.md` + duplicate `docs/決賽文件/實驗結果文件/20260724_Math16/04_math16_pilot02_jury_qa_final_v1.md` — synchronized copies, Q5/Q7 wording update.
6. `docs/experiments/presentation/math16_pilot02_one_pager_v23/one_pager_v23_manifest.json` + `scripts/build_math16_pilot02_one_pager_v23.py` + rendered `02_math16_pilot02_one_pager_v23.pdf` — current One-Pager; requires regeneration.
7. `docs/experiments/presentation/math16_pilot02_poster_v11/poster_v11_build_report.md` + `scripts/build_math16_pilot02_poster_v11.py` + rendered `03_math16_pilot02_poster_v11.pdf` — current Poster; requires regeneration.
8. `docs/experiments/visualization/math16_pilot02_core_figures_v1/figure_01_baseline_overall.svg` and `figure_05_healer_eligibility_boundary.svg` + `scripts/build_math16_pilot02_core_figures_v1.py` — rendered charts; requires regeneration.
9. `docs/experiments/visualization/math16_pilot02_core_figure_spec_v1/*` (`core_figure_spec.json`, `figure_caption_bank.md`, `figure_data_tables.json`, `primary_posthoc_visual_governance.md`, `source_traceability.json`, `one_pager_figure_selection.md`, `poster_and_oral_figure_order.md`, `figure_spec_report.md`) — governance/spec docs gating #8; must be amended before #8 can be regenerated.
10. `docs/experiments/results/math16_pilot02_qwen4b_vs_qwen9b_tier1_paired_analysis_v1/analysis_report.md`, `overall_paired_summary.json`, `condition_paired_summary.json`, `family_paired_summary.json`, `bootstrap_summary.json`, `seed_stability_summary.json`, `task_level_summary.json`, `paired_cell_ledger.jsonl` — this is the **analysis/reporting layer** for the Tier-1 4B-vs-9B comparison (derived from, but distinct from, the frozen raw baseline evidence); correction happens here, by re-running `scripts/analyze_math16_pilot02_qwen4b_vs_qwen9b_tier1_paired.py` against a corrected 4B source, per the recomputation in Sections 2–6 of this record. (This resolves Blocker #6 of `math16_baseline_79_amendment_plan_v1.md`: the paired-analysis output is analysis layer, not frozen raw evidence, and is therefore an A-list edit target, not a C-list never-touch item.)
11. `20260728_math16_method1_method2_progress_handoff.md` — status field update marking the open item as resolved (kept historical in narrative, but its live "open discrepancy" status line should be updated).

**Excluded — not List A:** `docs/決賽文件/實驗結果文件/20260722_Math16/01_math16_pilot02_final_report_v13.md` and `.../20260722_Math16/04_math16_pilot02_jury_qa_final_v1.md`, previously listed as synchronized copies, are removed from List A per explicit user instruction below (List D).

### List B — correction-note link only (historical / synchronized-copy documents that keep their original numbers, with a pointer added)

1. `docs/experiments/reports/math16_pilot02_final_report_v1.md`, `v11.md`, `v12.md` — superseded Final Report versions; correction-note link only, no number update.
2. `docs/experiments/reports/math16_pilot02_integrated_results_report_v1.md` (+ `決賽文件/.../archive_or_working_notes/05_...` duplicates) — **classified as supporting/secondary report per task decision, not a replacement for the canonical main report**; correction-note link only.
3. `docs/experiments/audits/math16_healer_revalidation_false_loop_fix_v1.md` / `.json` — historical, already-closed correction event; cross-reference note only.
4. `docs/experiments/audits/math16_pilot02_qwen4b_posthoc_corrected_chain_freeze_v1.md` / `.json` — frozen historical freeze record; cross-reference note only.
5. `docs/experiments/design/math16_posthoc_six_cell_rescue_audit_v1_spec.md` — frozen design record; cross-reference note only.
6. `docs/experiments/reports/healerboundary_final_evidence_gap_decision_v1.md` — historical decision record; cross-reference note only.
7. `docs/experiments/reports/math16_jury_risk_review_v1.md` — historical risk-review record; cross-reference note only.
8. `docs/決賽文件/實驗結果文件/20260724_Math16/README.md` — historical index page; optional one-line pointer to this decision record. (The `20260722_Math16` equivalent, if present, is excluded — see List D.)
9. `docs/experiments/audits/math16_pilot02_nonfraction_family_table_revalidation_v1/audit_report.md` — historical revalidation snapshot; cross-reference note only.
10. `docs/experiments/reports/math16_method1_method2_78_79_discrepancy_audit_v1.md`, `math16_method1_method2_extraction_closure_320.csv`, `math16_method1_method2_extraction_closure_summary_v1.json`, `math16_baseline_79_amendment_plan_v1.md` — the pre-existing frozen audit/plan chain this record builds on; already correctly scoped as proposals, left as-is (not edited by this record either).

### List D — EXCLUDED entirely, out of scope for this amendment (per explicit user instruction)

`docs/決賽文件/實驗結果文件/20260722_Math16/**` (the entire directory, including but not limited to `01_math16_pilot02_final_report_v13.md`, `04_math16_pilot02_jury_qa_final_v1.md`, and any `README.md` or other file inside it) is an **immutable historical archive** recording an earlier process snapshot. It is excluded entirely from this amendment: no number edit, no correction-note link, no chart regeneration, no cross-reference of any kind. This directory must not be conflated with the canonical `20260724_Math16/` copy (List A #1/#5) or treated as a synchronized copy needing lockstep update (it was previously miscategorized as such in an earlier draft of this record and in `math16_baseline_79_amendment_plan_v1.md`; both have been corrected).

### List C — must NEVER be modified (evidence / results / tests / frozen provenance audit)

1. `docs/experiments/results/math16_pilot02_qwen4b_evaluation_v4_r001/{cell_level_baseline.jsonl, baseline_summary.json, overall_summary.json, condition_summary.json, family_summary.json, task_summary.json, seed_summary.json, failure_taxonomy_summary.json, report.md, scoring_manifest.json}` — frozen Qwen 4B raw evaluation evidence.
2. `docs/experiments/results/math16_pilot02_qwen9b_evaluation_v4_r001/{cell_level_baseline.jsonl, overall_summary.json, ...}` — frozen Qwen 9B raw evaluation evidence.
3. `docs/experiments/results/math16_pilot02_qwen4b_healer_v4_r001/{eligibility_inventory.jsonl, healer_results.jsonl, overall_summary.json, post_healer_summary.json, report.md}` — frozen Healer/Eligibility evidence.
4. `docs/experiments/results/math16_pilot02_qwen4b_healer_v4_posthoc_corrected_chain_r001/*` — frozen corrected-chain evidence.
5. `docs/experiments/results/math16_pilot02_qwen4b/cells/.../artifact.json` (all generation-time artifacts, including the flagged cell) — frozen generation-time evidence.
6. `docs/experiments/manifests/math16_pilot02_qwen4b_evaluation_v4_r001_manifest.json` and all other pinned manifests.
7. `scripts/evaluate_math16_pilot02_qwen4b_healer_v4.py`, `scripts/evaluate_math16_pilot02_qwen4b_healer_v4_posthoc_corrected_chain.py`, `scripts/evaluate_math16_pilot02_full_v4.py`, `scripts/run_math16_latex_v1_gemini_live.py` — pinned Evaluator/Protocol scripts, including hard-coded `baseline_pass_fraction == "78/320"`-style assertions; any change here is a coordinated engineering task, out of scope for a documentation/analysis-layer amendment.
8. All `tests/test_math16_*.py` and `tests/finals_rebuild/test_math16_healer_revalidation_false_loop.py` (16 files, per the amendment plan's inventory) — automated regression tests pinned to the current frozen numbers.
9. `docs/experiments/reports/math16_healer_rule_provenance_audit_v1.md` and `_manifest.json` — **explicit self-imposed no-edit clause**; never modified, only cross-referenced from a new document (this record does so).
10. `docs/experiments/milestones/math16_pilot02_evidence_complete_v1/{evidence_complete_report.md, frozen_numeric_claims.json, primary_posthoc_accounting.json}` — frozen numeric-claims ledger (evidence-only, per the amendment plan's resolution of its own Blocker #3: treated as F/never-touch, not E/cross-reference-only, given its explicit "frozen" naming and ledger nature).
11. `docs/experiments/results/_scratch_confirmatory_reeval_320/*` (the pre-existing scratch confirmatory-reevaluation output) — read-only supporting evidence for the audit chain; not part of this record's scope and not modified.

## 9. Open blockers / limitations

- **None specific to the Tier-1 paired-analysis recomputation.** The 9B status for the exact matching cell (task/condition/seed) was found directly in the existing frozen `paired_cell_ledger.jsonl` with an unambiguous 1:1 key match (`ce115_calc_polynomial_division_l1__ab1__seed_2026072003`), and the bootstrap/McNemar/Wald methodology was read directly from `scripts/analyze_math16_pilot02_qwen4b_vs_qwen9b_tier1_paired.py` and replicated exactly (including reusing `random.seed(42)` so the resampled-task sequence is identical to the original run). Reproducing the OLD statistics from the unmodified ledger against this same replication script reproduced the report's own published OLD numbers exactly (McNemar p = 0.010582 vs. published 0.0106; Wald CI, OR, and bootstrap CI values matched to the digits shown in the published report), which serves as an internal validation that the recomputation methodology is correct before it was applied to the corrected ledger.
- **Carried forward from `math16_baseline_79_amendment_plan_v1.md` Blocker #1** (which Final Report version is the single "live" submitted copy) is **partially resolved**: the task's explicit instruction designates `docs/決賽文件/實驗結果文件/20260724_Math16/01_math16_pilot02_final_report_v13.md` as canonical, and a subsequent explicit user instruction excludes `docs/決賽文件/實驗結果文件/20260722_Math16/**` in its entirety as an immutable historical archive (List D) — so that copy is no longer an open "live vs. historical" question, it is simply out of scope. Remaining open question: whether the plain-path `docs/experiments/reports/math16_pilot02_final_report_v13.md` is still separately "live" (vs. purely a working/synchronized copy) is left to a human/future edit round, as originally flagged.
- **Carried forward from the same plan's Blocker #7** (exact SVG drawn-text-element diff for the two chart files) is unchanged and still open — this record adds one more number (the Tier-1 McNemar/OR figures) to what those charts would need to reflect if they visualize the 4B-vs-9B comparison, but does not perform the visual/DOM diff itself.
- No other ambiguity was encountered in locating or computing the statistics requested for this round.

## 10. Frozen-evidence / read-only confirmation

This record was produced by reading only pre-existing files and running read-only Python computations against `paired_cell_ledger.jsonl` (loaded, one field flipped in memory, never written back to disk) and reusing the published analysis script's formulas. No file under `docs/experiments/results/`, `docs/experiments/manifests/`, `scripts/`, or `tests/` was modified. No git commit was made. The only file created is this record, `docs/experiments/reports/math16_baseline_79_amendment_decision_record_v1.md`.

## 11. Closure update (2026-07-28, addendum)

This section appends closure status for items this record left open in Section 9 ("Open blockers / limitations"). It does not alter any settled number, table, or classification list above — additions only, plus cross-references to two new companion documents produced in this round: `docs/experiments/reports/math16_baseline_correction_note_v1.md` (the formal Correction Note) and `docs/experiments/reports/math16_baseline_79_figure_amendment_spec_v1.md` (the per-figure amendment spec).

### 11.1 Plain-path `math16_pilot02_final_report_v13.md` role — now resolved

Section 9's carried-forward blocker ("whether the plain-path `docs/experiments/reports/math16_pilot02_final_report_v13.md` is still separately 'live' vs. purely a working/synchronized copy") is **resolved by direct read-only comparison**:

- Content diff against the canonical `docs/決賽文件/實驗結果文件/20260724_Math16/01_math16_pilot02_final_report_v13.md` shows the two files are **materially different**, not identical or near-identical (423 lines in the canonical copy vs. 311 in the plain-path copy; the canonical copy contains an entirely different abstract framing of the Gemini Primary/post-hoc-inventory numbers, an added Method 1/Method 2 Regression split paragraph, and two entirely new sections — §10.1 "L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP 七格" and §10.2 "完整 10 格 eligible 帳與修復效果分層" — none of which exist in the plain-path copy).
- `git log --follow` on both paths shows they share five early commits (`bd576ec3`, `d17a086d`, `8883975b`, `799180dc`, `3a8c5293`) and then **diverge**: the canonical `決賽文件` copy received ten further commits after that point (`8cd7ab45` through `f829eb21`, including the Method 2 results/regression-split integration), while the plain-path copy in `docs/experiments/reports/` received **zero** further commits after `3a8c5293`.
- **Classification: (B) supporting/historical copy** — the plain-path `v13.md` is a superseded snapshot frozen at the point the two copies diverged; it is not maintained in lockstep with the canonical copy and has not been touched since. This is consistent with, and finalizes, the classification already implied by `math16_baseline_79_amendment_plan_v1.md`'s own note ("older non-current report versions kept for history") for the analogous v1/v11/v12 versions, and matches this record's own List B item 1 disposition (correction-note-link-only, no live-table edit) rather than List A (synchronized copy requiring lockstep edit). **List A of this record (Section 8) is corrected by this note**: item 2 ("synchronized copy (plain-path v13); update in lockstep with #1") should be read as **superseded** — the plain-path copy is List B, not List A. No List A/B/C/D table cell above is rewritten; this paragraph is the authoritative correction, per this section's append-only mandate.
- No blocker remains open on this question.

### 11.2 Figure inventory — now complete

Section 9's other carried-forward blocker ("exact SVG drawn-text-element diff for the two chart files... unchanged and still open") is **closed** by `docs/experiments/reports/math16_baseline_79_figure_amendment_spec_v1.md`, produced this round. That spec:

- Confirms, by direct raw-XML inspection (not assumption), that exactly **four** figures in `docs/experiments/visualization/math16_pilot02_core_figures_v1/` are affected: **Figure 1** (`figure_01_baseline_overall.svg`), **Figure 3** (`figure_03_family_breakdown.svg`), **Figure 4** (`figure_04_tier1_paired_analysis.svg`), and **Figure 5** (`figure_05_healer_eligibility_boundary.svg`).
- Confirms Figures 2 (`figure_02_prompt_conditions.svg`) and 6 (`figure_06_healer_concept_zones.svg`) contain zero hits for the affected-number token set and require no change.
- Extracts the exact literal old/new comment-and-text values for all four affected figures (e.g. Figure 1's `<!-- 78/320 -->` → `<!-- 79/320 -->`; Figure 4's `<!-- 26 -->`/`<!-- 193 -->`/`p = 0.010582`/CI bounds → `27`/`192`/`p = 0.015440`/updated CI bounds; Figure 5's dual `Primary rescue = 5 (83/320)` / `Post-hoc rescue = 6 (84/320)` annotations → a single `Verified rescue = 6 (79/320 → 85/320)` annotation).
- Remains specification-only — no SVG or generator script was regenerated this round, consistent with this record's List A item 8/9 (figures and their governance specs are still future regeneration targets, not yet executed).
- No blocker remains open on this question.

### 11.3 Remaining open items (unchanged from Section 9, not addressed this round)

- Blocker carried from `math16_baseline_79_amendment_plan_v1.md` #2 (whether `math16_pilot02_integrated_results_report_v1.md` is a live main report or fully superseded) — already resolved in Section 7/List B item 2 of this record ("classified as supporting/secondary report per task decision"); no further action needed, noted here only for completeness.
- No actual live-table edits, figure regenerations, or script/test changes have been performed by this record, the Correction Note, or the Figure Amendment Spec — all three remain analysis/specification/documentation-layer artifacts. Applying the specified edits to Category A files (Final Report, One-Pager, Poster, figures) and regenerating the Tier-1 paired-analysis outputs remains a distinct future engineering/editing task.
