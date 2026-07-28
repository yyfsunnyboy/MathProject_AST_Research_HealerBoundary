# Math16 Combined Amendment — Batch 3 PNG Correction Report v1

Report date: 2026-07-28  
Scope: **PNG export correction only** (no Batch 4–7).  
Result: **PASS**

## 1. Problem

Batch 3 initially exported Figure 1–5 PNG via **Edge headless full-page screenshot**. That produced oversized canvases with the chart stranded in a corner and large empty page margins. SVG promote itself was correct; PNG export method was not.

## 2. SVG intrinsic sizes (unchanged)

| Figure | width | height | viewBox | aspect |
|---|---|---|---|---|
| 1 | 576pt | 396pt | `0 0 576 396` | 576:396 |
| 2 | 756pt | 432pt | `0 0 756 432` | 756:432 |
| 3 | 648pt | 396pt | `0 0 648 396` | 648:396 |
| 4 | 684pt | 396pt | `0 0 684 396` | 684:396 |
| 5 | 684pt | 396pt | `0 0 684 396` | 684:396 |

Canonical SVG SHA values were verified unchanged after this correction (promote SHAs from Batch 3 still match). Figure 6 untouched.

## 3. Rasterizer and command

**Tool:** Inkscape 1.4.4 (`C:\Program Files\Inkscape\bin\inkscape.exe`)  
**Method:** native SVG → PNG; export width = viewBox_width × 3 (scale=3); height follows aspect.

Example (Figure 1):

```text
"C:\Program Files\Inkscape\bin\inkscape.exe" ^
  -o "docs/experiments/visualization/math16_pilot02_core_figures_v1/figure_01_baseline_overall.png" ^
  -w 1728 ^
  "docs/experiments/visualization/math16_pilot02_core_figures_v1/figure_01_baseline_overall.svg"
```

Widths used: Fig1 1728 · Fig2 2268 · Fig3 1944 · Fig4 2052 · Fig5 2052.

Forbidden for formal PNG: Edge/Chrome full-page screenshot.  
Not used: frozen core-figure builder; CairoSVG (cairo DLL unavailable); rsvg-convert (not installed).

Old Edge PNGs backed up under:
`docs/experiments/visualization/math16_pilot02_amendment_layer_v1/batch3_png_correction_backup/`

## 4. Per-figure old → new

| Fig | Old dims (Edge) | Old SHA-256 | New dims (Inkscape) | New SHA-256 | Whitespace | Visual |
|---|---|---|---|---|---|---|
| 1 | 2400×1700 | `9a6d6f8c171d834c346dc5ca7ce3420731ac47d4edb650cd56d3c5f13262210e` | **1728×1188** | `c5e091eedd82c4a39c78b596b970cd538d6503022546315b7832f3df4ba8d684` | eliminated page blank; content≈92% | **PASS** |
| 2 | 2800×1700 | `f26496caed2c6e425bf1d19a409815c114c48298b924ed45c12f6ca3bdbf6407` | **2268×1296** | `cf5cc62a967a4afc40f8f6d546e546bf2d3e9309a42cdbb94d2803ce94ea7f11` | eliminated page blank; right gap = SVG legend room | **PASS** |
| 3 | 2400×1700 | `f9a23c1e2d9f1ef19d3d6786e47ac2125c158164123924ba653b3d1dbb6c3cbf` | **1944×1188** | `2d225e069a62529d3657aec629a0b90df10ba63df9f68c927e81ab35e5b729c2` | eliminated page blank | **PASS** |
| 4 | 2600×1600 | `c52a3a6e1362344f5a11ef0936a49bc636d95a2326c867f7b1b1baf6b07d74ce` | **2052×1188** | `0daa7d332941709708f021b6f20bbb2d180f41a7ab7a36cc4f4c1572a7ac6da9` | eliminated page blank | **PASS** |
| 5 | 2600×1600 | `a9e5b1cc45596bbe5b2adcf058c9d31035418e567fcb745da7b86cdd07996581` | **2052×1188** | `05b81728393037f0657a42af34de883bbc860e44eccdfbfbf40553e86e6f1849` | eliminated page blank; ~15% right = SVG external-legend design | **PASS** |

Aspect ratios match viewBox exactly (scale=3). Not an upscale of the Edge PNGs.

## 5. Visual checks (PNG files opened)

- **Fig1:** G→9B→4B; 289/101/79; chart fills canvas; footnote visible; no page chrome  
- **Fig2:** group/legend G→9B→4B; hatch identity OK; no crop/clip  
- **Fig3:** two-model; Polynomial 17/80; tight frame  
- **Fig4:** 52/27/49/192; p=0.015440; RD=+6.88%; CI [-1.56%,+14.37%]  
- **Fig5:** FAIL [31,219,241]; 79→85 rescue=6; arrow at 4B (3rd); no Primary 84  

## 6. Scope confirmation

- Canonical SVG: **not modified**  
- Figure 6: **not modified**  
- Formal docs / One-Pager / Poster / package / frozen evidence: **not modified**  
- No model/Healer/Evaluator rerun; no commit/push  
- Batch 4–7: **not executed**

## 7. Verdict

**PASS** — formal Figure 1–5 PNGs are Inkscape viewBox-tight rasters; Edge screenshot PNGs superseded.
