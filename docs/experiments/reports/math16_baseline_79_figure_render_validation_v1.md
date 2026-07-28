# Math16 Baseline 79/320 Figure Render Validation v1

Validation date: 2026-07-28
Status: **execution round — real SVG file changes performed and validated for 2 of 4 target figures; 2 figures marked BLOCKED per explicit instruction not to force ambiguous/design-level edits.**

This report validates the regeneration of the 4 figures identified in `docs/experiments/reports/math16_baseline_79_figure_amendment_spec_v1.md` as affected by the Baseline 78/320 → 79/320 correction documented in `docs/experiments/reports/math16_baseline_correction_note_v1.md`.

## 0. Method decision (generator script vs. hand-edit)

The generator script `scripts/build_math16_pilot02_core_figures_v1.py` was read in full. Regeneration via the script was **not used**, for three concrete reasons found on inspection:

1. **SHA Protection**: `main()` explicitly skips re-rendering Figures 1, 3, 4, 5 if their PNGs already exist (`if not fig1_png.exists(): render...else: print("Skipping ... (SHA Preserved)")`). Forcing a re-render requires deleting the existing PNGs first.
2. **Hard-coded assertions tied to the OLD numbers.** The script reads its ground truth from `docs/experiments/milestones/math16_pilot02_evidence_complete_v1/frozen_numeric_claims.json` and then *asserts* the old values inline in multiple functions, e.g. `assert claims["qwen_4b"]["baseline_pass"] == 78`, `assert q4b_counts == [30, 16, 15, 17]`, `assert fails == [31, 242, 219]`, `assert primary_rescues == [0, 5, 0]`, `assert posthoc_rescues == [0, 6, 0]`. Regenerating with the corrected numbers would require editing these pinned assertions inside the generator script itself — not just a data-source update — which goes beyond "update a data source and re-run."
3. **`frozen_numeric_claims.json` lives under a milestone directory literally named `evidence_complete_v1`** and is titled "frozen numeric claims." Although this exact file is not named in the correction note's explicit never-touch list, its name and location signal frozen-evidence status. Editing it to feed the generator was judged too risky relative to the scope of this task (regenerate 4 figures), and was avoided.

Given this, **direct hand-editing of the SVG XML was used**, per the task's fallback path. Matplotlib's SVG output does not use `<text>`/`<tspan>` elements — every glyph is a vector `<path>` referenced via `<use xlink:href="#GlyphID">`. Each figure's font subset assigns digits 0–9 a stable hex glyph ID following the pattern `id = hex(0x13 + digit)` (i.e. 0→13, 1→14, 2→15, 3→16, 4→17, 5→18, 6→19, 7→1a, 8→1b, 9→1c) — verified empirically per file by cross-checking multiple independent numeric strings (e.g. `289/320`, `101/320`, `(31.6%)`, `9B`) before making any edit. All required numeric changes for Figures 1 and 4 turned out to be same-length, same-position digit-for-digit substitutions (old and new strings have identical character counts), which made safe surgical `<use>`-reference swaps possible without touching layout, spacing, or any other glyph.

## 1. Figure 1 — `figure_01_baseline_overall.svg` — **PASS**

- **File(s) modified**: `docs/experiments/visualization/math16_pilot02_core_figures_v1/figure_01_baseline_overall.svg`
- **Generator/command used**: hand-edited XML (reason above); no script executed.
- **Old → new values**: `78/320` → `79/320`; `(24.4%)` → `(24.7%)`.
- **Edit mechanics**: comment `<!-- 78/320 -->` → `<!-- 79/320 -->`; the '8' glyph `<use xlink:href="#MicrosoftJhengHeiBold-1b" .../>` → `#MicrosoftJhengHeiBold-1c` (digit 9), reusing the glyph path already locally defined for '7' (`-1a`) at the same block. Comment `<!-- (24.4%) -->` → `<!-- (24.7%) -->`; the second '4' glyph `<use xlink:href="#MicrosoftJhengHeiBold-17" .../>` (at translate `179.703125`) → `#MicrosoftJhengHeiBold-1a` (digit 7).
- **SVG parse result**: `xml.etree.ElementTree.parse()` — OK, no errors.
- **Old-string residue check**: `grep -c "78/320\|(24.4%)"` → **0**.
- **New-string presence check**: `grep -c "79/320\|(24.7%)"` → **2** (comment + none other; both target strings present).
- **Visual inspection (rendered via headless Chrome, 1400×1000 PNG)**: Three-bar chart renders cleanly. Qwen 3.5 4B bar now shows "79/320 (24.7%)" centered above its bar, same position/size as before, no overlap with the 289/320 (Gemini) or 101/320 (Qwen 9B) labels, no clipping, footnote intact. Layout is visually identical to the original except for the two corrected digits.
- **Unrelated-diff check**: Extracted every `<!-- comment -->` text run from the original vs. edited file (21 comments each, same count). Diff shows exactly 2 changed entries: `78/320`→`79/320` and `(24.4%)`→`(24.7%)`. No other comment/text changed.
- **Verdict: PASS.**

## 2. Figure 3 — `figure_03_family_breakdown.svg` — **BLOCKED**

- **File(s) modified**: none (file left untouched; confirmed via `git status --short` showing no diff for this file).
- **Reason for BLOCKED**: The task instructions ask for `20.0%` → `21.25%` on the Polynomial 4B bar, "matching the existing figure's display precision convention — check whether other bars in the same figure show 1 or 2 decimal places." On inspection, **the SVG contains zero `%` characters anywhere** (`grep -c "%"` → 0) and the generator function `render_figure_3()` only ever draws bar labels as `f"{int(height)}/80"` — no percentage is rendered on this figure at all, for any family or model. This is precisely the ambiguous case the task instructions describe as an example for when to stop rather than guess ("you can't tell where to put '21.25%' because the figure doesn't show percentages elsewhere"). Inventing a percentage display that doesn't exist in the original figure design would be a layout/design decision, not a value correction.
- The unambiguous part of the requested change — Polynomial 4B `16/80` → `17/80` — was identified in the SVG (comment `<!-- 16/80 -->`) and is mechanically safe to apply on its own, but per the task's instruction to mark the whole figure BLOCKED rather than partially force an edit when part of the requested change is ambiguous, **no edit was applied to this file.**
- **Verdict: BLOCKED** — reason: figure does not display percentages anywhere; adding one requires a design decision outside a value-correction edit.

## 3. Figure 4 — `figure_04_tier1_paired_analysis.svg` — **PASS**

- **File(s) modified**: `docs/experiments/visualization/math16_pilot02_core_figures_v1/figure_04_tier1_paired_analysis.svg`
- **Generator/command used**: hand-edited XML; no script executed.
- **Old → new values applied**:
  - `26` → `27` (2×2 matrix cell, "4B ONLY PASS")
  - `193` → `192` (2×2 matrix cell, "BOTH FAIL")
  - `• 4B-only PASS:  26 格` → `• 4B-only PASS:  27 格`
  - `• Net Cell Gain (Δ):  +23 格` → `• Net Cell Gain (Δ):  +22 格`
  - `• Paired Risk Diff:  +7.19%` → `• Paired Risk Diff:  +6.88%`
  - `• Exact McNemar:  p = 0.010582 *` → `p = 0.015440 *`
  - `[-0.94%, +14.38%]` → `[-1.56%, +14.37%]`
  - Odds ratio (`1.88`→`1.81`) and Wald CI (`[1.94%, 12.43%]`→`[1.59%, 12.16%]`): confirmed **not rendered as text anywhere in this SVG** (no literal match found), so per the task's own conditional ("if the figure shows OR/Wald CI") — no change needed/possible here.
  - `BOTH_PASS` (52) and `NINE_B_ONLY_PASS` (49) — unaffected, unchanged, verified still present.
- **Edit mechanics**: every change was a same-length digit-for-digit `<use xlink:href>` swap (old and new numeral strings have identical character counts at every affected position), so no glyph spacing/`translate()` values needed to change. One new glyph path definition was added locally (Bold "7", `MicrosoftJhengHeiBold-1a`, copied verbatim from the identical glyph already defined elsewhere in the same font in Figure 1's SVG) since digit '7' had not previously appeared in this figure's Bold-font subset.
- **SVG parse result**: `xml.etree.ElementTree.parse()` — OK, no errors.
- **Old-string residue check**: `grep -c` for `<!-- 26 -->`, `<!-- 193 -->`, `4B-only PASS:  26`, `+23 格`, `+7.19%`, `0.010582`, `[-0.94%, +14.38%]` (combined pattern) → **0**.
- **New-string presence check**: each of `<!-- 27 -->`, `<!-- 192 -->`, `27 格`, `+22 格`, `+6.88%`, `0.015440`, `[-1.56%, +14.37%]` → **1 occurrence each** (all present).
- **Visual inspection (rendered via headless Chrome, 1400×900 PNG)**: 2×2 matrix + stats panel renders cleanly. Matrix shows 52 / 27 / 49 / 192 in the four cells with correct labels (BOTH PASS, 4B ONLY PASS, 9B ONLY PASS, BOTH FAIL). Stats panel shows "9B-only PASS: 49 格", "4B-only PASS: 27 格", "Net Cell Gain (Δ): +22 格", "Paired Risk Diff: +6.88%", "Exact McNemar: p = 0.015440 *", "Cluster Bootstrap 95% CI: [-1.56%, +14.37%]". No overlapping text, no truncation, no misplacement; box borders and text alignment identical to original layout.
- **Unrelated-diff check**: Extracted every `<!-- comment -->` text run from original vs. edited file (35 comments each, same count). Diff shows exactly 7 changed entries, matching the intended list above one-for-one. No other comment/text changed.
- **Verdict: PASS.**

## 4. Figure 5 — `figure_05_healer_eligibility_boundary.svg` — **BLOCKED**

- **File(s) modified**: none (file left untouched; confirmed via `git status --short` showing no diff for this file).
- **Reason for BLOCKED**: The requested change is not a value correction but a **structural/visual redesign**:
  - The two existing annotations (`Primary rescue = 5 (83/320)` and `Post-hoc rescue = 6 (84/320)`, drawn together as one 3-line callout box with an arrow) must be **removed and replaced** with new content ("Baseline 79/320 → Final 85/320", "Verified rescue = 6") that has a different character count, different line structure, and includes a "→" arrow glyph. This "→" glyph is **not currently defined anywhere in this SVG's font subsets** — inserting it correctly would require sourcing real glyph outline path data from an actual font renderer (matplotlib/a real TTF), which is not achievable via safe character-substitution editing the way Figures 1 and 4 were.
  - The callout box's background rectangle, arrow pointer target, and text bounding box are all sized for the current 3-line text; new text of different length/shape requires re-computing box dimensions and arrow anchor — a genuine layout decision, not a text edit.
  - The spec doc (`math16_baseline_79_figure_amendment_spec_v1.md`, Section 4) itself flags this as requiring a figure-owner design call regarding whether the "Primary Rescue (Solid)" / "Post-hoc Rescue (Dashed Overlay)" dual bar-encoding also collapses to a single encoding.
  - Additionally, on inspection, the Qwen 3.5 4B "Baseline FAIL" bar in this same figure currently displays `242` (= 320 − 78, the pre-correction baseline). Under the correction, this would arithmetically become `241` (= 320 − 79), but this bar/value is **not** in the task's explicit list of Figure 5 changes to make — a further sign that a full, correct redesign of this figure needs a scoped decision beyond the literal instructions given, rather than a partial/guessed edit.
- Per the explicit instruction to stop and mark BLOCKED rather than force a guess when a figure requires "a real layout call you're not confident making," **no edit was applied to this file.**
- **Verdict: BLOCKED** — reason: requires new arrow glyph not present in the font subset, box/arrow layout redesign, and a resolution of the also-visible-but-unlisted `242`→`241` FAIL-count inconsistency; none of this is safely achievable via mechanical digit substitution.

## 5. Summary

| Figure | Verdict | File modified | Old-string residue | New-string presence |
|---|---|---|---|---|
| 1 — `figure_01_baseline_overall.svg` | **PASS** | Yes | 0 | confirmed present |
| 3 — `figure_03_family_breakdown.svg` | **BLOCKED** | No | n/a | n/a |
| 4 — `figure_04_tier1_paired_analysis.svg` | **PASS** | Yes | 0 | confirmed present |
| 5 — `figure_05_healer_eligibility_boundary.svg` | **BLOCKED** | No | n/a | n/a |

No PNG counterparts were regenerated (no matplotlib re-run occurred); `figure_01_baseline_overall.png` and `figure_04_tier1_paired_analysis.png` still reflect the pre-correction render and would need separate regeneration if a PNG asset is required downstream. `figure_build_manifest.json` / `figure_build_report.md` (which record per-file SHA-256 hashes) were **not** updated and now describe stale hashes for the 2 edited SVGs; this is out of this task's explicit scope (only the 4 named figures) but is noted here for downstream awareness.

Figures 2 and 6 were not touched. No results/journal/manifest/protocol/test file, main report, Q&A, One-Pager, Poster, or `決賽文件/實驗結果文件/20260722_Math16/**` file was touched. No git commit was made.
