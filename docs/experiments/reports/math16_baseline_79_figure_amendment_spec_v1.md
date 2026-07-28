# Math16 Baseline 79/320 Figure Amendment Spec v1

Spec date: 2026-07-28
Status: **specification only — not regenerated in this round.** No SVG, PNG, or generator script was modified, executed, or re-rendered to produce this document. All values below were located by direct inspection of the raw SVG XML (both `<!-- comment -->` markers and, where present, drawn `<text>`/glyph structure), not assumed from filenames or captions alone.

## 0. Figure directory and figure-number mapping (verified, not assumed)

Figure directory: `docs/experiments/visualization/math16_pilot02_core_figures_v1/`
Figure numbering/captions verified against: `docs/experiments/visualization/math16_pilot02_core_figure_spec_v1/core_figure_spec.json`

| Figure # | Filename (svg/png) | Caption topic | Affected by 78→79 correction? |
|---|---|---|---|
| 1 | `figure_01_baseline_overall.svg/.png` | Three-model Baseline overall pass rate | **Yes** |
| 2 | `figure_02_prompt_conditions.svg/.png` | Prompt-condition effects by model | No — grepped for `78/320`, `24.38`, `83/320`, `84/320`, `25.94`, `26.25`; zero hits |
| 3 | `figure_03_family_breakdown.svg/.png` | Qwen 4B vs 9B pass counts by math family | **Yes** |
| 4 | `figure_04_tier1_paired_analysis.svg/.png` | Qwen 4B vs 9B 2x2 paired McNemar/CI analysis | **Yes** |
| 5 | `figure_05_healer_eligibility_boundary.svg/.png` | Healer eligibility/rescue boundary | **Yes** |
| 6 | `figure_06_healer_concept_zones.svg/.png` | Healer 3-zone safety concept (Zone 1/2/3) | No — grepped for the same token set; zero hits (this figure is a conceptual diagram with no cell counts) |

**Total affected figures: 4 (Figures 1, 3, 4, 5). Figures 2 and 6 require no change.**

Generator script for all six figures: `scripts/build_math16_pilot02_core_figures_v1.py`
Build manifest/report: `docs/experiments/visualization/math16_pilot02_core_figures_v1/figure_build_manifest.json`, `figure_build_report.md`
Governance/spec docs gating regeneration: `docs/experiments/visualization/math16_pilot02_core_figure_spec_v1/{core_figure_spec.json, figure_caption_bank.md, figure_data_tables.json, primary_posthoc_visual_governance.md, source_traceability.json, one_pager_figure_selection.md, poster_and_oral_figure_order.md, figure_spec_report.md}`

Documents that embed or reference these figure files (verified via repo-wide search on the filenames): the current One-Pager (`docs/experiments/presentation/math16_pilot02_one_pager_v23/`, plus superseded v1/v2/v21/v22 kept historical), the current Poster (`docs/experiments/presentation/math16_pilot02_poster_v11/`, plus superseded v1), the Final Report (`docs/experiments/reports/math16_pilot02_final_report_v13.md` and its manifest, plus superseded v1/v11/v12), and both `決賽文件` copies of the Final Report (`20260724_Math16/01_...` canonical, `20260722_Math16/01_...` excluded per scope). Superseded/historical versions and the excluded `20260722_Math16` copy are not amendment targets — see `docs/experiments/reports/math16_baseline_79_amendment_decision_record_v1.md` Lists A/B/D for the full disposition.

---

## 1. Figure 1 — `figure_01_baseline_overall.svg`

- **File path**: `docs/experiments/visualization/math16_pilot02_core_figures_v1/figure_01_baseline_overall.svg` (+ `.png`)
- **Generator**: `scripts/build_math16_pilot02_core_figures_v1.py`
- **Referencing documents**: Final Report v13 (both the plain-path copy and the canonical `決賽文件/20260724_Math16` copy, if either embeds this figure inline or via the One-Pager/Poster pipeline), current One-Pager v23, current Poster v11.
- **Exact old literal text found in raw SVG** (via direct XML inspection, `<!-- comment -->` markers paired with adjacent drawn glyph-path text runs):
  - Line 1537: `<!-- 289/320 -->` (Gemini — unaffected, not part of this correction)
  - Line 1625: `<!-- (90.3%) -->` (Gemini — unaffected)
  - **Line 1637: `<!-- 78/320 -->`** (Qwen 4B Baseline bar label — affected)
  - **Line 1658: `<!-- (24.4%) -->`** (Qwen 4B Baseline percentage label — affected)
  - Line 1670: `<!-- 101/320 -->` (Qwen 9B — unaffected)
  - Line 1680: `<!-- (31.6%) -->` (Qwen 9B — unaffected)
- **Exact proposed new text**:
  - `<!-- 78/320 -->` → `<!-- 79/320 -->`
  - `<!-- (24.4%) -->` → `<!-- (24.7%) -->` (79/320 = 24.6875%, displayed to one decimal as the existing convention does, i.e. 24.7%)
- **Not regenerated in this round — specification only.**

---

## 2. Figure 3 — `figure_03_family_breakdown.svg`

- **File path**: `docs/experiments/visualization/math16_pilot02_core_figures_v1/figure_03_family_breakdown.svg` (+ `.png`)
- **Generator**: `scripts/build_math16_pilot02_core_figures_v1.py`
- **Referencing documents**: same set as Figure 1 (Final Report, One-Pager v23, Poster v11), plus `core_figure_spec.json`/`figure_data_tables.json` (governance/data-table source that gates this figure's values — `figure_data_tables.json` L18 in particular records `pass_rate_pct: 24.38`-family figures per the amendment plan's Section 2.1 row 16, and would need the Polynomial-family cell updated in lockstep before regeneration).
- **Exact old literal text found in raw SVG** (bar-value comments, in family order Integer → Polynomial → Radical → Fraction, 4B group then 9B group — order verified against the figure's own caption text in `core_figure_spec.json`, which states "9B 在 Integer (42 vs 30)、Fraction (31 vs 17) 與 Radical (19 vs 15) 均高於 4B；惟在 Polynomial 呈現反向低下 (9 vs 16)"):
  - Line 1696: `<!-- 30/80 -->` (Integer, 4B — unaffected)
  - **Line 1740: `<!-- 16/80 -->`** (Polynomial, 4B — affected)
  - Line 1793: `<!-- 15/80 -->` (Radical, 4B — unaffected)
  - Line 1825: `<!-- 17/80 -->` (Fraction, 4B — unaffected; note this is a pre-existing, unrelated "17/80" for Fraction, not to be confused with the corrected Polynomial value below)
  - Line 1847: `<!-- 42/80 -->` (Integer, 9B — unaffected)
  - Line 1901: `<!-- 9/80 -->` (Polynomial, 9B — unaffected; 9B Polynomial count does not change)
  - Line 1940: `<!-- 19/80 -->` (Radical, 9B — unaffected)
  - Line 1950: `<!-- 31/80 -->` (Fraction, 9B — unaffected)
- **Exact proposed new text**:
  - `<!-- 16/80 -->` (Polynomial, 4B, line 1740) → `<!-- 17/80 -->`
  - Caption text in `core_figure_spec.json` (`caption_report`/`caption_oral` for Figure 3) stating "Polynomial 呈現反向低下 (9 vs 16)" → "Polynomial 呈現反向低下 (9 vs 17)"; the family-breakdown source note at SVG line 2635 ("Polynomial反向結果不可外推為9B整體能力較差...") requires no numeric change, only the bar value and caption number.
- **Not regenerated in this round — specification only.**

---

## 3. Figure 4 — `figure_04_tier1_paired_analysis.svg`

- **File path**: `docs/experiments/visualization/math16_pilot02_core_figures_v1/figure_04_tier1_paired_analysis.svg` (+ `.png`)
- **Generator**: `scripts/build_math16_pilot02_core_figures_v1.py`
- **Referencing documents**: Final Report (Tier-1 comparison section/abstract callouts), and the Tier-1 paired-analysis results directly (`docs/experiments/results/math16_pilot02_qwen4b_vs_qwen9b_tier1_paired_analysis_v1/analysis_report.md` and its JSON siblings), which this figure visualizes.
- **Exact old literal text found in raw SVG**:
  - Line 366: `<!-- 52 -->` (BOTH_PASS — unaffected)
  - **Line 829: `<!-- 26 -->`** (4B ONLY PASS count — affected)
  - Line 1013: `<!-- 49 -->` (9B ONLY PASS — unaffected)
  - **Line 1049: `<!-- 193 -->`** (BOTH FAIL count — affected)
  - **Line 3175: `<!-- • 4B-only PASS:  26 格 -->`** (affected)
  - Line 2836: `<!-- • 9B-only PASS:  49 格 -->` (unaffected)
  - **Line 3250: `<!-- • Net Cell Gain (Δ):  +23 格 -->`** (affected)
  - **Line 3504: `<!-- • Paired Risk Diff:  +7.19% -->`** (affected)
  - **Line 4285: `<!-- • Exact McNemar:  p = 0.010582 * -->`** (affected)
  - **Line 4610: `<!--    [-0.94%, +14.38%] -->`** (task-clustered bootstrap 95% CI — affected)
  - Line 5885: narrative footnote "註：Cell-level discordant方向偏向9B，但task-level外推仍有不確定性。* exact McNemar p在細胞層級顯著。" — no numeric literal to change; qualitative claim unchanged (still significant, still crosses zero at task level).
  - No literal odds-ratio (`1.88`) text/comment was found drawn anywhere in this SVG — the odds ratio is apparently not rendered as visible text in this figure, so no OR change is needed here (it would need updating only in the Final Report/analysis_report.md narrative text, not this figure).
- **Exact proposed new text**:
  - `<!-- 26 -->` (line 829) → `<!-- 27 -->`
  - `<!-- 193 -->` (line 1049) → `<!-- 192 -->`
  - `<!-- • 4B-only PASS:  26 格 -->` → `<!-- • 4B-only PASS:  27 格 -->`
  - `<!-- • Net Cell Gain (Δ):  +23 格 -->` → `<!-- • Net Cell Gain (Δ):  +22 格 -->`
  - `<!-- • Paired Risk Diff:  +7.19% -->` → `<!-- • Paired Risk Diff:  +6.88% -->`
  - `<!-- • Exact McNemar:  p = 0.010582 * -->` → `<!-- • Exact McNemar:  p = 0.015440 * -->`
  - `<!--    [-0.94%, +14.38%] -->` → `<!--    [-1.56%, +14.37%] -->`
  - `BOTH_PASS` (52), `NINE_B_ONLY_PASS` (49), and the Wald CI/odds-ratio values are not drawn as literal text in this SVG and require no in-figure change; if a future regeneration adds them as text they should use the NEW values from `math16_baseline_correction_note_v1.md` Section 5.1 (Wald 95% CI [0.0159, 0.1216], OR 1.81).
- **Not regenerated in this round — specification only.**

---

## 4. Figure 5 — `figure_05_healer_eligibility_boundary.svg`

- **File path**: `docs/experiments/visualization/math16_pilot02_core_figures_v1/figure_05_healer_eligibility_boundary.svg` (+ `.png`)
- **Generator**: `scripts/build_math16_pilot02_core_figures_v1.py` (annotation string built at script line ~509, per the amendment plan's Section 2.1 row 15: `ax.annotate("Primary rescue = 5 (83/320)\nPost-hoc rescue = 6 (84/320)\n[Post-hoc mechanism validation]", ...)`)
- **Referencing documents**: Final Report (Healer eligibility/rescue section), One-Pager v23, Poster v11.
- **Exact old literal text found in raw SVG**:
  - **Line 1101: `<!-- Primary rescue = 5 (83/320) -->`**
  - **Line 1273: `<!-- Post-hoc rescue = 6 (84/320) -->`**
  - Line 1341: `<!-- [Post-hoc mechanism validation] -->` (label, no number — may be retained or folded into the collapsed annotation, per figure-owner's design call)
  - Line 2324: `<!-- Eligible Cases -->` (label only, count of 10 unaffected — the eligible population size does not change)
  - Line 2443: `<!-- Primary Rescue (Solid) -->` (visual-style label, may become obsolete if Primary/Post-hoc split bars are collapsed)
  - Line 2718: `<!-- Post-hoc Rescue (Dashed Overlay) -->` (visual-style label, same consideration)
  - Line 2854: `<!-- 註：在本次320個測試單元中觀察到Regression=0。Gemini與9B未命中規則主動Abstain (Eligible=0)。 -->` — no numeric change needed; statement remains true.
- **Exact proposed new text**: per the adopted principle (Primary 84/320 demoted from main tables, single Verified-rescue headline), collapse the two separate annotations into one:
  - `<!-- Primary rescue = 5 (83/320) -->` + `<!-- Post-hoc rescue = 6 (84/320) -->` → a single `<!-- Verified rescue = 6 (79/320 → 85/320) -->` annotation, replacing both. The separate "Primary Rescue (Solid)" / "Post-hoc Rescue (Dashed Overlay)" dual-visual-encoding (lines 2443, 2718) would likewise collapse to a single rescue-encoding if the figure owner agrees this is a visual-design change, not just a text substitution — **final call on the visual redesign (single bar/marker vs. retaining a dashed/solid distinction for historical Primary vs. corrected-chain framing) belongs to whoever owns figure design**, per the amendment plan's own note on this figure (row 14).
  - The "Eligible Cases" count (10) is unaffected — the corrected cell was never eligible.
- **Not regenerated in this round — specification only.**

---

## 5. Summary table

| Figure | File | Literal values to change | New values |
|---|---|---|---|
| 1 | `figure_01_baseline_overall.svg` | `78/320`, `(24.4%)` | `79/320`, `(24.7%)` |
| 3 | `figure_03_family_breakdown.svg` | Polynomial 4B `16/80` (+ caption "9 vs 16") | `17/80` (+ caption "9 vs 17") |
| 4 | `figure_04_tier1_paired_analysis.svg` | `26`, `193`, `26 格`, `+23 格`, `+7.19%`, `p = 0.010582`, `[-0.94%, +14.38%]` | `27`, `192`, `27 格`, `+22 格`, `+6.88%`, `p = 0.015440`, `[-1.56%, +14.37%]` |
| 5 | `figure_05_healer_eligibility_boundary.svg` | `Primary rescue = 5 (83/320)` / `Post-hoc rescue = 6 (84/320)` (two annotations) | `Verified rescue = 6 (79/320 → 85/320)` (single annotation; visual-encoding collapse is a figure-owner design decision) |

Figures 2 (`figure_02_prompt_conditions.svg`) and 6 (`figure_06_healer_concept_zones.svg`) were checked against the same token set (`78/320`, `24.38`, `83/320`, `84/320`, `25.94`, `26.25`) and produced zero hits — no change needed.

## 6. Explicit scope statement

**Not regenerated in this round — specification only.** No SVG, PNG, or generator script (`scripts/build_math16_pilot02_core_figures_v1.py`) was executed, edited, or re-rendered to produce this document. No figure-spec/governance file under `docs/experiments/visualization/math16_pilot02_core_figure_spec_v1/` was edited. This spec exists solely so a future engineering/design pass can apply the changes above without re-deriving them from scratch.
