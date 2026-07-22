# Math16 Pilot-02 Poster v1 Render Build Report

## Layout
- Landscape 36 × 24 inches; three columns.
- Figure 4 is the largest named figure; header cards are level 2; Figures 1/5 level 3; Figures 2/3/6 level 4.

## Frozen accounting
- 4B: Baseline 78/320; Primary 83/320 (rescue=5); Post-hoc 84/320 (total rescue=6; +1 PASS vs Primary).
- Gemini: Primary 289/320; Post-hoc 306/320.
- Figure 2 warning: Gemini 80/80 is Post-hoc; Primary spec-v1=63/80; Qwen uses spec-v2; no direct Primary causal inference.

## Renderer BBox verification
- Named elements: 21
- Pairwise comparisons: 210
- Passing pairs: 210
- Collisions: 0
- Measured with get_window_extent(renderer=renderer) and get_position(); any positive intersection fails the build.

## Integrity
- Frozen source SHA values matched before and after rendering.
- PNG SHA-256: `f3823157b170af72ea0b50d241d8498f74513f962ade6716c0c8ff0f75a0580c`
- PDF SHA-256: `8bc26788758dd812768bcefa5dddf25c81e8969b153304174fa23bc4a95e07e8`
- Model calls=0; rescoring=false; Healer execution=false.
