# Math16 Combined Amendment — Batch 2 Report v1

Report date: 2026-07-28  
Batch: **2 — staging full render + visual validation (no promote)**  
Result: **PASS**

## 0. Start staging SVG SHA-256 (Batch 2 entry)

Recorded before this batch’s preview re-render:

| File | SHA-256 |
|---|---|
| `…/staging/figure_01_baseline_overall.staging.svg` | `455297d4893eec022bca770c6a32fe8208c381ad2d54c526b411f8b3a1c801db` |
| `…/staging/figure_02_condition_breakdown.staging.svg` | `bc2feed3c5b5bebf9e08886d035bde8a450c47db5c99deb2634b076f100ba277` |
| `…/staging/figure_03_family_breakdown.staging.svg` | `a5240cc79b4196121441a9962f39fc6b0de9bb4b94cb7106852843500d58e9b2` |
| `…/staging/figure_05_healer_eligibility_boundary.staging.svg` | `19930f2665ea6250b13ffe140b3bb1a064e0e57e20f678a832d5dffec4f57b13` |

## 1. Preview render method

Environment had no Inkscape / rsvg-convert / cairosvg. Preview PNGs were produced by re-invoking `scripts/render_math16_pilot02_amended_figures_v1.py` figure functions and saving PNG beside SVG, **only** under:

`docs/experiments/visualization/math16_pilot02_amendment_layer_v1/staging/preview/`

No canonical / compact / One-Pager / Poster / 決賽 package writes.

## 2. Per-figure validation

### Figure 1 — `figure_01_baseline_overall`

| Item | Result |
|---|---|
| Staging SVG (final) | `…/staging/figure_01_baseline_overall.staging.svg` — `c2ed3d1ada213933d9c980dfb2852879296490a422a7846c970db170f10243ef` |
| Preview PNG | `…/staging/preview/figure_01_baseline_overall.preview.png` — `78a24f610084e476f032ecfa4e17f15794aeaebb1070891977531fc0ce5531f3` |
| XML parse | PASS |
| Model positions | L Gemini 289/320 (90.3%) · M 9B 101/320 (31.6%) · R 4B 79/320 (24.7%) |
| Colors / labels / bars | Blue / amber / green identity-aligned with labels |
| Order | Gemini→9B→4B (not Gemini→4B→9B) |
| Old residuals | no `78/320` in figure text |
| Visual (PNG opened) | PASS — bars/labels clear; order/values correct |
| Verdict | **PASS** |

### Figure 2 — `figure_02_condition_breakdown`

| Item | Result |
|---|---|
| Staging SVG (final) | `…/staging/figure_02_condition_breakdown.staging.svg` — `2ab8530ad91c4f7c7de4710b8609f05cc5050761093cd741d625b516e31ff925` |
| Preview PNG | `…/staging/preview/figure_02_condition_breakdown.preview.png` — `4ad42891a3c87c7b5c0f3a460c1516e27cc3b5212beb53a3ec2f2a29308bc398` |
| XML parse | PASS |
| Per-group order | Ab1/Ab2g/Ab2d+api/Ab2d+spec each Gemini→9B→4B |
| Legend | Gemini Primary · Gemini Post-hoc hatch · 9B · 4B |
| Values with identity | Ab1 72/18/15; Ab2g 76/27/19; Ab2d+api 78/16/8; Ab2d+spec hatch 80 + Primary 63, 40, 36 |
| Hatch / color | Hatch remains Gemini-identity blue; 9B amber; 4B green |
| Visual (PNG opened) | PASS — no overlap/cutoff/group offset errors observed |
| Verdict | **PASS** |

### Figure 3 — `figure_03_family_breakdown`

| Item | Result |
|---|---|
| Staging SVG (final) | `…/staging/figure_03_family_breakdown.staging.svg` — `51e3ed62d2f8b6164f045f97e432d19842f065837ca84ffb738727bfab02bee3` |
| Preview PNG | `…/staging/preview/figure_03_family_breakdown.preview.png` — `f823a13ec50f699ec6346b9692b295f135f64b79f5255b6951800f8bc5ea06dc` |
| XML parse | PASS |
| Structure | Two-model only (4B green, 9B amber); no Gemini forced in |
| Polynomial 4B | **17/80** (footnote 9 vs 17); no `16/80` label residual |
| Other families | Integer 30/42; Radical 15/19; Fraction 17/31 |
| Visual (PNG opened) | PASS |
| Verdict | **PASS** |

### Figure 5 — `figure_05_healer_eligibility_boundary`

| Item | Result |
|---|---|
| Staging SVG (final) | `…/staging/figure_05_healer_eligibility_boundary.staging.svg` — `c8e76aff8d53acbccf276459c70344db37f3309e4c287b25a3823a4c22d013fe` |
| Preview PNG | `…/staging/preview/figure_05_healer_eligibility_boundary.preview.png` — `13101268c2e62376e0501d8ddb7b0c964cab570e408c2f0afb3f442e20c9aa25` |
| XML parse | PASS |
| Model order | Gemini→9B→4B |
| PASS implied / FAIL | PASS [289,101,79]; FAIL [31,219,241] |
| 4B main track | Baseline 79/241 → Final 85/235; Verified rescue=6 |
| Primary 84 | Not presented as main track |
| Overlay / arrow | Annotation arrow points to Verified Rescue bar at **third** (4B) position |
| Visual (PNG opened) | PASS — no overlap, truncation, or arrow misplacement |
| Verdict | **PASS** |

## 3. Layout fix applied during Batch 2

Visual review flagged Fig1 footnote crowding risk. Allowed fix only:

- `scripts/render_math16_pilot02_amended_figures_v1.py`
  - Fig1: larger bottom `tight_layout` margin + slightly smaller footnote font
  - Fig5: `subplots_adjust(bottom=0.12)`

Then re-rendered staging SVG + preview PNG; re-opened Fig1/Fig5 PNGs — PASS.

Final renderer SHA-256: `2caab9e3615a68473185e3fa6be1800bd0f25bc33136824afda537bdd894da9c`

## 4. Canonical zero-change

| Path | SHA-256 |
|---|---|
| `…/core_figures_v1/figure_01_baseline_overall.svg` | `608a3aa4a2f3cb3b4387c81177e3952c05575039f22fb84829f718a9e523860c` |
| `…/core_figures_v1/figure_04_tier1_paired_analysis.svg` | `0b7f004abf518db36a55b868b88618c6074574d7140d4145dd3d871e998fcf79` |

Unchanged vs Batch 0/1. Expected that canonical Fig1/4 still lack new trio order (staging-only).

## 5. Forbidden-scope confirmation

| Class | Touched? |
|---|---|
| Promote staging → canonical | No |
| Canonical SVG/PNG/PDF | No |
| Formal reports / Jury / Method / Integrated / One-Pager / Poster | No |
| Frozen builder / claims / results / tests | No |
| Model/Healer/Evaluator / stats recompute | No |
| commit / push | No |
| Batches 3–7 | Not executed |

## 6. Batch 2 verdict

**PASS** — all four staging figures visually and structurally PASS; canonical untouched; ready for Batch 3 promote gate (not executed here).
