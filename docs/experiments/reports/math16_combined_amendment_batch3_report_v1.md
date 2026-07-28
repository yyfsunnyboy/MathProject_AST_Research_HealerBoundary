# Math16 Combined Amendment — Batch 3 Report v1

Report date: 2026-07-28  
Batch: **3 — promote staging Fig1/2/3/5 + regenerate Fig1–5 PNG; retain amended Fig4 SVG**  
Result: **PASS (after PNG correction — see also `math16_combined_amendment_batch3_png_correction_report_v1.md`)**

## 0. Naming note (Figure 2)

Staging file is named `figure_02_condition_breakdown.staging.svg`.  
Live canonical / asset-map path remains **`figure_02_prompt_conditions.svg/.png`**.  
Batch 3 promoted staging bytes **into** `figure_02_prompt_conditions.*` to avoid a dual Fig2 SOT. No `figure_02_condition_breakdown.svg` was created.

## 1. Rollback (pre-promote)

Directory: `docs/experiments/visualization/math16_pilot02_amendment_layer_v1/batch3_rollback/`  
Manifest: `batch3_rollback/rollback_manifest_v1.json`  
Batch 0 `wt_backup/` was **not** overwritten.

| Source | Backup | Pre-promote SHA-256 | Role |
|---|---|---|---|
| `…/figure_01_baseline_overall.svg` | `pre_promote_figure_01_baseline_overall.svg` | `608a3aa4a2f3cb3b4387c81177e3952c05575039f22fb84829f718a9e523860c` | canonical_fig1_svg_pre_promote |
| `…/figure_02_prompt_conditions.svg` | `pre_promote_figure_02_prompt_conditions.svg` | `76211c220a8eb3040495a59fe42a49139e8379514ee8868f52f95029cbf590ad` | canonical_fig2_svg_pre_promote |
| `…/figure_03_family_breakdown.svg` | `pre_promote_figure_03_family_breakdown.svg` | `8daf1901ca83b8f96bddad3bef73dd586bcd35ba8ae5a537ef0b615e954c9f9e` | canonical_fig3_svg_pre_promote |
| `…/figure_05_healer_eligibility_boundary.svg` | `pre_promote_figure_05_healer_eligibility_boundary.svg` | `45126972a0373fca4c48e5c615f91e31b5814ed5e6573b8750b93df84bf1e2e9` | canonical_fig5_svg_pre_promote |
| `…/figure_01_baseline_overall.png` | `pre_promote_figure_01_baseline_overall.png` | `5bc0c714769c987710dd124b7f126a53a4c77f96ccd578fbff4a0c82bdb52db2` | canonical_fig1_png_pre_promote |
| `…/figure_02_prompt_conditions.png` | `pre_promote_figure_02_prompt_conditions.png` | `7df829db88a30c34aeb3e9b000a5d96aec08c3134abfbfdc1475ebaac3da7e4b` | canonical_fig2_png_pre_promote |
| `…/figure_03_family_breakdown.png` | `pre_promote_figure_03_family_breakdown.png` | `f164edc807659c45628cbab4711074879af58d3beaa825f59aaf2ebce4c9fb79` | canonical_fig3_png_pre_promote |
| `…/figure_04_tier1_paired_analysis.png` | `pre_promote_figure_04_tier1_paired_analysis.png` | `f18bbb774e9a75c51da364f080281172e7c35c4a5b2e30245142de0993565fdf` | canonical_fig4_png_pre_promote_stale |
| `…/figure_05_healer_eligibility_boundary.png` | `pre_promote_figure_05_healer_eligibility_boundary.png` | `5887f0b829797ab63f30a096ec2e27c80530c1f988dcc16e3bead4bd7feb9885` | canonical_fig5_png_pre_promote |

## 2. Promote (byte-for-byte staging → canonical)

| Staging | Canonical | SHA-256 (staging = post) |
|---|---|---|
| `figure_01_baseline_overall.staging.svg` | `figure_01_baseline_overall.svg` | `c2ed3d1ada213933d9c980dfb2852879296490a422a7846c970db170f10243ef` |
| `figure_02_condition_breakdown.staging.svg` | `figure_02_prompt_conditions.svg` | `2ab8530ad91c4f7c7de4710b8609f05cc5050761093cd741d625b516e31ff925` |
| `figure_03_family_breakdown.staging.svg` | `figure_03_family_breakdown.svg` | `51e3ed62d2f8b6164f045f97e432d19842f065837ca84ffb738727bfab02bee3` |
| `figure_05_healer_eligibility_boundary.staging.svg` | `figure_05_healer_eligibility_boundary.svg` | `c8e76aff8d53acbccf276459c70344db37f3309e4c287b25a3823a4c22d013fe` |

- Staging was **not** regenerated.  
- **Figure 4 SVG** retained amended WT: `0b7f004abf518db36a55b868b88618c6074574d7140d4145dd3d871e998fcf79`  
- **Figure 6** untouched (SVG `855f348a…`, PNG unchanged).

## 3. PNG regeneration — corrected after Edge export failure

### 3.1 SVG promote: PASS

Figures 1/2/3/5 SVG promote lockstep (§2) remains valid. Figure 4 SVG WT retained. Figure 6 unchanged.

### 3.2 Original Edge screenshot PNG export: FAIL (superseded)

Initial Batch 3 PNG method used Microsoft Edge headless `--screenshot` (full-page canvas).  
That produced oversized page canvases (e.g. Fig1 **2400×1700**) with the chart stranded and large empty margins — **not acceptable** as formal PNG.

| PNG (Edge, superseded) | SHA-256 | Dims |
|---|---|---|
| `figure_01_baseline_overall.png` | `9a6d6f8c171d834c346dc5ca7ce3420731ac47d4edb650cd56d3c5f13262210e` | 2400×1700 |
| `figure_02_prompt_conditions.png` | `f26496caed2c6e425bf1d19a409815c114c48298b924ed45c12f6ca3bdbf6407` | 2800×1700 |
| `figure_03_family_breakdown.png` | `f9a23c1e2d9f1ef19d3d6786e47ac2125c158164123924ba653b3d1dbb6c3cbf` | 2400×1700 |
| `figure_04_tier1_paired_analysis.png` | `c52a3a6e1362344f5a11ef0936a49bc636d95a2326c867f7b1b1baf6b07d74ce` | 2600×1600 |
| `figure_05_healer_eligibility_boundary.png` | `a9e5b1cc45596bbe5b2adcf058c9d31035418e567fcb745da7b86cdd07996581` | 2600×1600 |

### 3.3 Final PNG: Inkscape native SVG rasterizer — PASS

Re-exported from unchanged canonical SVG with **Inkscape 1.4.4**, scale=3 (`-w` = viewBox_width×3).  
Details: `docs/experiments/reports/math16_combined_amendment_batch3_png_correction_report_v1.md`

| PNG (final) | Dims | SHA-256 |
|---|---|---|
| `figure_01_baseline_overall.png` | **1728×1188** | `c5e091eedd82c4a39c78b596b970cd538d6503022546315b7832f3df4ba8d684` |
| `figure_02_prompt_conditions.png` | **2268×1296** | `cf5cc62a967a4afc40f8f6d546e546bf2d3e9309a42cdbb94d2803ce94ea7f11` |
| `figure_03_family_breakdown.png` | **1944×1188** | `2d225e069a62529d3657aec629a0b90df10ba63df9f68c927e81ab35e5b729c2` |
| `figure_04_tier1_paired_analysis.png` | **2052×1188** | `0daa7d332941709708f021b6f20bbb2d180f41a7ab7a36cc4f4c1572a7ac6da9` |
| `figure_05_healer_eligibility_boundary.png` | **2052×1188** | `05b81728393037f0657a42af34de883bbc860e44eccdfbfbf40553e86e6f1849` |

Command template:

```text
"C:\Program Files\Inkscape\bin\inkscape.exe" -o <png> -w <viewBox_w*3> <svg>
```

Frozen core-figure builder was **not** used. Canonical SVG was **not** modified by the PNG correction.

## 4. Per-figure validation

### Figure 1 — SVG promote **PASS** · PNG (final Inkscape) **PASS**
- Pre SVG `608a3aa4…` → Post SVG `c2ed3d1a…` (= staging)  
- Final PNG `c5e091ee…` 1728×1188 (aspect 576:396); chart fills canvas; footnote visible  
- Visual: G→9B→4B; 289/320, 101/320, 79/320  

### Figure 2 — SVG promote **PASS** · PNG (final Inkscape) **PASS**
- Pre SVG `76211c22…` → Post SVG `2ab8530a…` (= staging)  
- Final PNG `cf5cc62a…` 2268×1296  
- Visual: each group + legend G→9B→4B; hatch identity OK  

### Figure 3 — SVG promote **PASS** · PNG (final Inkscape) **PASS**
- Pre SVG `8daf1901…` → Post SVG `51e3ed62…` (= staging)  
- Final PNG `2d225e06…` 1944×1188  
- Visual: two-model; Polynomial 4B **17/80**  

### Figure 4 — SVG retain **PASS** · PNG (final Inkscape) **PASS**
- SVG unchanged WT `0b7f004a…`  
- Final PNG `0daa7d33…` 2052×1188 (from amended SVG; not Edge screenshot)  
- Visual: 52/27/49/192; p=0.015440; RD=+6.88%; CI [-1.56%, +14.37%]  

### Figure 5 — SVG promote **PASS** · PNG (final Inkscape) **PASS**
- Pre SVG `45126972…` → Post SVG `c8e76aff…` (= staging)  
- Final PNG `05b81728…` 2052×1188  
- Visual: FAIL [31,219,241]; 79→85; rescue=6; arrow at 4B; no Primary 84  

### Figure 6 — zero change confirmed
- SVG SHA `855f348a23fd78eea1c8983d153c652fe81b992ec335d4930fa43dad3a34b214` unchanged  

## 5. Diff / scope limits

Modified under `math16_pilot02_core_figures_v1/` only:
- Fig1/2/3/5 SVG (staging promote)
- Fig1–5 PNG (final: Inkscape viewBox-tight raster; Edge screenshots superseded)
- Fig4 SVG remains prior WT amendment
- Fig4 PNG regenerated via Inkscape from amended SVG

Not touched: presentation claims, amendment renderer, frozen builder/claims/results/tests, formal reports, Jury/Method/Integrated, One-Pager/Poster, compact, 決賽 package, Batches 4–7.

## 6. Batch 3 verdict

**PASS (after PNG correction)**  
- SVG promote: PASS  
- Original Edge screenshot PNG export: **FAIL / superseded**  
- Final Inkscape PNG export: PASS (see `math16_combined_amendment_batch3_png_correction_report_v1.md`)  
- Ready for Batch 4 only after this PNG correction (Batch 4 not executed here).

## 7. Follow-on — Figure 2 Post-hoc presentation correction (same day)

After Batch 3 PNG correction, Figure 2 Ab2d+spec Gemini was further simplified to a **single solid blue 80/80*** bar (no hatch dual-track; Primary 63/80 footnote-only).  
See `docs/experiments/reports/math16_figure2_posthoc_presentation_correction_v1.md`.  
Figures 1/3/4/5/6 were not modified by that follow-on.
