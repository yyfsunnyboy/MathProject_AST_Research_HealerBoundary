# Math16 Method 1 / Method 2 78-vs-79 Discrepancy Audit v1

Audit date: 2026-07-28
Status: read-only audit. No results, code, Healer, Eligibility, Evaluator, Protocol, or Manifest files were modified in producing this report. The only file created is this report.

## 0. Scope and inputs read

- Method 1 baseline (v4): `docs/experiments/results/math16_pilot02_qwen4b_evaluation_v4_r001/cell_level_baseline.jsonl` (320 rows)
- Method 1 eligibility/healer trace (v4): `docs/experiments/results/math16_pilot02_qwen4b_healer_v4_r001/eligibility_inventory.jsonl`, `healer_results.jsonl`
- Method 1 report: `docs/experiments/reports/math16_method1_40_120_split_results_report_v1.md` (states Baseline 78/320)
- Method 2 report: `docs/experiments/reports/math16_method2_all_cell_results_report_v1.md` (states Raw PASS 79/320)
- Method 2 raw data: `docs/experiments/results/math16_method2_all_cell_replay_v1/{phase_a_freeze.json, phase_a_summary.json, eligibility_journal.jsonl, phase_b_summary.json, transition_journal.jsonl, raw_sources/*}`
- Generation-time artifact for the flagged cell: `docs/experiments/results/math16_pilot02_qwen4b/cells/qwen3_5_4b__ce115_calc_polynomial_division_l1__ab1__seed_2026072003/artifact.json`
- Progress handoff: `docs/experiments/reports/20260728_math16_method1_method2_progress_handoff.md`

Both methods' 320-cell populations were joined by `cell_id` (320/320 matched, no missing cells either direction).

## 1. Full cell-by-cell diff (not assumed — computed)

Comparing Method 1 baseline `final_status` (from `cell_level_baseline.jsonl`, v4_r001) against Method 2 `raw_status` (from `transition_journal.jsonl`, which records an independent per-cell Raw evaluation for all 320 cells) yields **exactly one disagreeing cell**:

| cell_id | Method 1 baseline final_status | Method 2 raw_status |
|---|---|---|
| `qwen3_5_4b__ce115_calc_polynomial_division_l1__ab1__seed_2026072003` | FAILED | PASSED |

All other 319 cells agree between Method 1 baseline and Method 2 raw. This confirms the 78 vs 79 gap is exactly this one cell, and rules out any additional hidden disagreements.

This cell is **not** an `L1_PROSE_RESIDUE_NARROW` cell — its Method 1 `failure_subtype` is `PARSE_ERROR` / `classifier_outcome: catastrophic_truncation` with `mechanism_tags: ["candidate_extraction_failure", "truncation"]`, and it never appears in either method's `L1_PROSE_RESIDUE_NARROW` cell lists. **The L1_PROSE_RESIDUE_NARROW 1-vs-2 count difference and the 78/79 discrepancy are two separate, unrelated issues** (see Section 4).

## 2. Raw source identity check for the differing cell

For `qwen3_5_4b__ce115_calc_polynomial_division_l1__ab1__seed_2026072003`:

- Model generation `raw_response` (the actual LLM output stored in `.../math16_pilot02_qwen4b/cells/.../artifact.json`) has `raw_response_sha256 = 249670b9...` — this is the single upstream artifact both methods must extract a candidate program from. Only one generation exists for this cell; it was not regenerated.
- Method 1's baseline record (`cell_level_baseline.jsonl`) for this cell contains **three different hash fields**:
  - `raw_response_sha256`: `249670b979a09de98b9fd04d64f50bba877b772e67bca790d9a76fa3cf2a1431` (full model output)
  - `raw_artifact_sha256`: `698fc868338e78aea35b4d9d145f98acacf03c3041243a78fbed663403f5b21d` (the candidate actually scored — this is what drove `g1_parse: FAIL`)
  - `candidate_hash`: `6adedeb6f2039ecef9273927464ee460bcd0167b08981669d5c09b866fb53c37` (a *separately recorded* candidate-extraction hash, present in the same JSON record but **not** the one used for scoring)
- Method 2's `raw_source_sha256` for this cell (`eligibility_journal.jsonl` / `transition_journal.jsonl`) is `6adedeb6f2039ecef9273927464ee460bcd0167b08981669d5c09b866fb53c37`.

**Method 2's raw source hash is byte-identical to Method 1's own `candidate_hash` field for this same cell** — confirmed by direct hash match, and further confirmed by diffing file content: Method 2's stored raw source file (`raw_sources/qwen3_5_4b__ce115_calc_polynomial_division_l1__ab1__seed_2026072003.py`) is a complete, syntactically valid `generate()` function extracted from the tail of the same `raw_response`.

So: **the underlying model output is identical between methods; the candidate program actually scored by Method 1's baseline differs from the candidate program Method 2 (and Method 1's own recorded `candidate_hash`) extracted.**

### Why the extraction diverged

Inspecting the raw `raw_response` text directly: it contains **7 occurrences of the literal substring `` ``` ``** — the first 6 are backticks appearing inside the model's own prose commentary (the model is discussing code-fence formatting conventions, e.g. `` ```python `` `), or explanations`, `` `. But usually this`` , etc., at byte offsets 25677–26961), and only the **7th** occurrence (offset 27091, `` ```python\ndef generate(level=1... ``) is the real opening fence of the actual code block, closed at offset 28337. After that closing fence there is additional trailing prose ("Wait, `remainder_latex` should probably be...").

Method 1's baseline `raw_artifact_sha256` (`698fc868...`) does not match the correctly-bounded code block and is consistent with an extractor that anchored on one of the earlier, spurious in-prose `` ``` `` occurrences, producing a truncated/malformed candidate — hence `SyntaxError`-class `catastrophic_truncation` at `g1_parse`. Method 2's raw source (matching Method 1's own `candidate_hash`) is the correctly-bounded, complete, valid function, which parses, executes, and scores `PASSED` under the same pinned evaluator.

## 3. Evaluator / pipeline identity check

- `evaluator_hash` in Method 1's baseline record for this cell: `2cca19f2258d4ba6134ff10d4e9bcff925e2441c32820fcbc151cb6b1dd740bc`.
- Method 2's protocol/manifest references the same evaluator script, `scripts/evaluate_math16_pilot02_full_v4.py`, and the Method 2 report states Raw and Final were both scored "使用同一 pinned Evaluator" (the same pinned evaluator used for Method 1). No evidence of a different evaluator version was found for this cell.
- Task/condition/seed are identical (`ce115_calc_polynomial_division_l1`, `ab1`, seed `2026072003`) in both records.
- `runtime_config_fingerprint` is identical (`33fd7603f58...`) between the generation-time artifact and Method 1's baseline record.

**Conclusion: the evaluator and task/condition/seed are identical. The divergence is isolated to which candidate-extraction hash was fed into the evaluator for this one cell** — i.e., an extraction-time selection bug/inconsistency inside Method 1's original v4 baseline pipeline (it computed a correct `candidate_hash` but scored a different, incorrect `raw_artifact_sha256`), not a difference in raw model output, task setup, or evaluator logic.

## 4. Is the L1_PROSE_RESIDUE_NARROW 1-vs-2 difference the same root cause?

No — verified as a separate issue.

- Method 1's Healer eligibility trace (`eligibility_inventory.jsonl`, `healer_results.jsonl`) shows exactly **one** `L1_PROSE_RESIDUE_NARROW`-eligible cell: `qwen3_5_4b__ce115_calc_polynomial_factor_roots_l1__ab2d_spec_v2__seed_2026072002` (`healer_eligible: true`, `matched_rule_probe: L1_PROSE_RESIDUE_NARROW`).
- A second candidate cell, `qwen3_5_4b__ce112_q09_divisor_multiple_intersection__ab2d__seed_2026072003`, is marked **`healer_eligible: false` / `noneligible`** in Method 1, with `eligibility_reason: "No extractable candidate source for frozen healer."` — Method 1's extractor abstains on this cell entirely (no probe hits, no rule matched).
- Method 2's `eligibility_journal.jsonl` shows **both** cells as `eligible: true`, `rule_id: L1_PROSE_RESIDUE_NARROW`, `rule_triggered: true` — for the second cell, Method 2's extraction succeeded via `extraction_method: "plain_text"`, a path Method 1's extractor apparently did not have available or did not select for this cell's raw source shape.
- Critically, for this second cell the raw source bytes are byte-identical between methods (`raw_source_sha256` in Method 2 matches `raw_response_sha256` = `5a9e086326f2f0f68719f2a694403ed8215a15918bde244bbbb766219381325d` recorded in Method 1's baseline for the same cell).
- Both methods, regardless of the count, keep this cell as `still_failed` in Method 2's Raw→Final transition table — i.e., the 1-vs-2 rule-trigger count difference has **no effect on any PASS/FAIL count**, including the 78/79 discrepancy. It reflects a difference in **eligibility/extraction-method coverage** ("plain_text" extraction present in Method 2, seemingly absent/inactive in Method 1's frozen v4 healer path for this raw-source shape), not a difference in raw source content, evaluator, or final status.

So: the L1_PROSE_RESIDUE_NARROW 1-vs-2 count and the 78/79 discrepancy are **independent findings** with different root causes and different affected cells.

## 5. Root cause summary

| Discrepancy | Cell(s) | Raw source identical? | Evaluator identical? | Root cause | Affects PASS/FAIL counts? |
|---|---|---|---|---|---|
| Baseline 78/320 vs Raw 79/320 | `qwen3_5_4b__ce115_calc_polynomial_division_l1__ab1__seed_2026072003` | Yes (model output identical); candidate-extraction output differs (Method 1 scored a different, incorrectly-bounded slice than its own recorded `candidate_hash`) | Yes (same `evaluator_hash`, same script) | Candidate-extraction bug/inconsistency in Method 1's original v4 baseline pipeline: a spurious in-prose ``` ``` ``` sequence caused mis-bounded extraction that was scored instead of the correctly extracted candidate already computed in the same record | Yes — this is the entire 1-cell gap |
| L1_PROSE_RESIDUE_NARROW: 1 (Method 1) vs 2 (Method 2) | `qwen3_5_4b__ce112_q09_divisor_multiple_intersection__ab2d__seed_2026072003` (the second cell; first cell agrees) | Yes | Yes (evaluator not even invoked for Method 1 on this cell — it abstained pre-evaluator) | Extraction-method coverage difference: Method 2's extractor has a `plain_text` extraction path that succeeded where Method 1's frozen v4 healer extractor abstained (`"No extractable candidate source"`) | No — cell is `still_failed` under both; no PASS/FAIL count changes |

## 6. Which number is valid, and in what sense

- **Baseline 78/320 (Method 1)**: shown by this audit to undercount by exactly one cell due to a candidate-extraction bug in the original v4 baseline scoring for `..._polynomial_division_l1__ab1__seed_2026072003` — Method 1's own pipeline computed the correct candidate hash (`candidate_hash`) but scored a different, incorrectly-bounded artifact (`raw_artifact_sha256`) for `g1_parse`. As officially reported and frozen, **78/320 remains Method 1's own recorded and reported Baseline number** and is not being altered by this audit (per the hard read-only constraint). It should, however, be treated as **known-suspect for this one cell** pending a corrective re-score under Method 1's own evaluator/protocol.
- **Raw 79/320 (Method 2)**: independently re-extracted and re-scored all 320 raw sources under the same pinned evaluator, and for the disputed cell used a candidate that is byte-identical to Method 1's own already-computed (but unused) `candidate_hash`. This is the better-supported PASS count for this specific cell under the shared evaluator, and Method 2's 79/320 stands as the audited, internally consistent number for "raw" scoring of the 320-cell population under this evaluator.
- Both numbers remain "valid" in their own documented, frozen sense: 78/320 is Method 1's officially reported Baseline (unchanged, as required); 79/320 is Method 2's officially reported and now-explained Raw PASS. The evidence here indicates the **true count consistent with the shared evaluator and the correctly-extracted candidate is 79/320**, with the 1-cell gap traced to a Method 1 extraction artifact, not a real behavioral or evaluator difference.

## 7. Proposed corrections (not applied — read-only audit)

The following are proposals only; no files were changed to implement them:

1. Method 1's v4 baseline pipeline should be checked for why `raw_artifact_sha256` and `candidate_hash` diverge for `qwen3_5_4b__ce115_calc_polynomial_division_l1__ab1__seed_2026072003` (and ideally swept across all 320 cells to confirm this is an isolated occurrence, not a systemic pattern that could affect other cells beyond this single confirmed diff). This audit only diffed final PASS/FAIL status, not every intermediate hash field for all 320 cells, so a full hash-consistency sweep of Method 1's baseline (`raw_artifact_sha256` vs `candidate_hash` for all 320 rows) is an open follow-up, not yet performed.
2. If the sweep confirms this is isolated to one cell, Method 1's 40/120-split report and any dependent official numbers (78/320 Baseline; 83/320 Primary; 84/320 corrected-chain) may need a documented correction note (not a silent edit) indicating the corrected Baseline should be 79/320, with consequent review of whether the Primary/corrected-chain numbers are affected (this cell was FAILED under Method 1's original v4 scoring, so it may have entered Method 1's healer-eligible/ineligible population — its `healer_eligible` status under Method 1's v4 eligibility trace was not part of this audit's scope and should be checked before any number is revised).
3. The `L1_PROSE_RESIDUE_NARROW` 1-vs-2 count difference should be documented as a separate, known extraction-coverage difference between Method 1's frozen v4 healer extractor and Method 2's all-cell extractor (which includes a `plain_text` extraction path); this does not require changing any PASS/FAIL count since both methods agree the affected cell is `still_failed`.

## 8. Open blockers / limitations

- This audit diffed Method 1 baseline vs Method 2 raw status across all 320 cells (confirmed exactly one disagreement) and did a deep hash/content trace for that one cell and for the two `L1_PROSE_RESIDUE_NARROW` cells. It did **not** perform a full field-by-field hash-consistency sweep (`raw_artifact_sha256` vs `candidate_hash`) across all 320 Method 1 baseline rows — that would be needed to state with certainty that the extraction-mismatch bug is isolated to exactly this one cell rather than being masked elsewhere by coincidentally-matching hashes. This is flagged as an explicit open item rather than assumed.
- Method 1's original healer-eligibility disposition for `..._polynomial_division_l1__ab1__seed_2026072003` (whether it was ever considered for healing given its FAILED baseline status, and what that implies for Primary/corrected-chain 83/320 and 84/320) was not traced in this audit and should be checked before revising any downstream number.

## 10. Extension: full 320-cell closure (2026-07-28, addendum)

This section extends Sections 1-9 (which resolved only the one known cell and the one known `L1_PROSE_RESIDUE_NARROW` cell) to **all 320 cells**, per follow-up item in Section 8. New deliverables:

- Full crosswalk: `docs/experiments/reports/math16_method1_method2_extraction_closure_320.csv` (320 rows)
- Machine-readable summary: `docs/experiments/reports/math16_method1_method2_extraction_closure_summary_v1.json`
- Confirmatory re-evaluation raw output (new scratch location, not overwriting anything): `docs/experiments/reports/_scratch_confirmatory_reeval_320/{m1_evaluated_artifact_reeval.json, m2_raw_source_reeval.json, confirmatory_reeval_summary.json}`

### 10.1 Population and identity checks

All 320 cell_ids matched 1:1 between Method 1 (`cell_level_baseline.jsonl`) and Method 2 (`transition_journal.jsonl` / `eligibility_journal.jsonl`); symmetric-difference of cell_id sets = 0. Original model-response corpus identity was re-verified per cell (recomputed SHA-256 of `artifact.json["raw_response"]` against Method 1's own `raw_response_sha256` field) with no mismatch across all 320 cells. Evaluator hash, task, condition, and seed fields are identical between methods for every cell (same fields checked in Section 3, now swept across the full population).

### 10.2 Source-difference classification, all 320 cells

| Classification | Count | Meaning |
|---|---|---|
| `status_changing` | 1 | Method1 evaluated-artifact final_status disagrees with Method2 raw_status — the one already-known cell. |
| `eligibility_only` | 1 | PASS/FAIL agrees; eligibility/rule_id bookkeeping disagrees — the one already-known `L1_PROSE_RESIDUE_NARROW` cell. |
| `equivalent_extraction` | 239 | Scored/raw source hashes differ, both sides parse and both reach the same final status — two independently-implemented extractors landing on functionally equivalent code. |
| `normalization_only` | 70 | Neither side's source parses (both agree there is no usable code — largely non-code / `nonchoice` prose-answer tasks), both FAILED; differing hashes are just two different non-code text spans. |
| `extraction_abstain_difference` | 9 | One side parses and the other does not, but this did not change the final PASS/FAIL status. |
| `no_difference` | 0 | Method1's `raw_artifact_sha256` never equals its own `candidate_hash` for any of the 320 cells — these are, by Method1's schema, always distinct fields (representing different pipeline stages), so a nonzero hash delta between the two is normal and by itself is not evidence of a bug. |

Zero cells beyond the one already-known cell exhibit the "wrong_block_selection" bug signature (Method2's source parses cleanly while Method1's scored artifact does not, with status still agreeing) — i.e. the sweep confirms the extraction-selection bug identified in Section 2 is **isolated to exactly one cell** and did not silently affect any other cell's PASS/FAIL status.

### 10.3 Confirmatory re-evaluation (evaluator re-invoked, read-only w.r.t. all existing files)

Re-invoked the same pinned evaluator's post-extraction scoring logic (`ast.parse` → entry-point check → `_execute_generate_all_ops` → schema check → oracle check, importing the exact same functions used by `scripts/evaluate_math16_pilot02_full_v4.py` and `scripts/run_math16_latex_v1_gemini_live.py::classify_math16_response`) directly against:

- (a) Method 1's evaluated-artifact candidate texts (`cell_level_baseline.jsonl["classifier_source"]`, present for 316/320 cells; the remaining 4 have no persisted candidate text because Method 1 recorded a parse failure with nothing to store, and were scored FAILED without re-execution, consistent with their recorded `g1_parse: FAIL`)
- (b) Method 2's canonical raw sources (`raw_sources/*.py`, all 320 present)

Zero LLM calls, zero Healer invocations. Result: **78/320 PASS reproduced exactly for (a)** and **79/320 PASS reproduced exactly for (b)**, with **zero mismatches** against each method's own recorded final/raw status across all 320 cells in both directions. This independently confirms both officially-reported numbers are internally consistent with what was actually scored (not merely self-reported), and confirms the 78-vs-79 gap traces to input-source selection, not evaluator behavior.

All new output was written only to `docs/experiments/reports/_scratch_confirmatory_reeval_320/` — no existing results, journal, Healer, Eligibility, extractor, Evaluator, Protocol, or Manifest file was modified.

### 10.4 Consequences for Primary (83/320) and corrected-chain (84/320)

Method 1's eligibility inventory (`eligibility_inventory.jsonl`) shows the status-changing cell (`..._polynomial_division_l1__ab1__seed_2026072003`) as `healer_eligible: false / noneligible`, reason `"No extractable candidate source for frozen healer."` — this cell **never entered** Method 1's 10-cell eligible-rescue population and was never touched by the Healer/rescue mechanism. Its correction (were it applied) is therefore additive to Primary and corrected-chain independently of rescue counts:

- Baseline: 78/320 → 79/320 (+1, proposed)
- Primary: 83/320 → 84/320 (+1, proposed)
- Corrected-chain: 84/320 → 85/320 (+1, proposed)
- Rescue count: unchanged at 5 (Primary) / 6 (corrected-chain) — this cell was never part of that population.

These are proposals only, pending human sign-off; no official number was changed by this audit.

### 10.5 Proposed list of files needing correction if 79/320 (and downstream 84/320 / 85/320) is adopted

See `docs/experiments/reports/math16_method1_method2_extraction_closure_summary_v1.json` → `answers.files_that_would_need_correction_if_79_320_is_adopted_PROPOSED_ONLY` for the itemized list (baseline JSONL row, all Method 1 v4_r001 summary JSONs, the 40/120-split report, the Method 2 report cross-reference, and the progress-handoff doc). No file in that list was modified by this audit.

## 9. File modification confirmation

No file other than this report and its two new companion deliverables (`math16_method1_method2_extraction_closure_320.csv`, `math16_method1_method2_extraction_closure_summary_v1.json`), plus a new scratch subdirectory (`_scratch_confirmatory_reeval_320/`) holding confirmatory-evaluator output, was created, edited, or deleted during this audit (original pass) and its Section 10 extension. All commands run were read-only against existing data (`grep`, `find`, Python read-only scripts, `sha256sum`, and a read-only re-invocation of the pinned evaluator's scoring functions against already-existing source texts). No existing results, journal, Healer, Eligibility, extractor, Evaluator, Protocol, or Manifest file was modified. No git commit was made.
