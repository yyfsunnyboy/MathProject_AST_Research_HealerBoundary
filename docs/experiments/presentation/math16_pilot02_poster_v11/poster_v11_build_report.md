# Math16 Pilot-02 Poster v1.1 Readability Hotfix Report

## Scope
- Pure visual hotfix: layout, font size, contrast, and information density only.
- No official number, conclusion, core figure, Final Report, Poster v1, spec, or One-Pager change.

## Improvements
- Header adds high-contrast `Math16 Pilot-02 子實驗` and a large standalone `960 cells` statement.
- Cards use enlarged 30pt core numbers; Qwen 4B `救回 5 格` is independently highlighted.
- Figure 4 remains the largest figure; Figure 1/5 panels enlarged; right-column prose is compressed.
- Figure 2 uses four readable accounting lines; limitations use one line each; conclusion is isolated.

## Three-second messages
- Math16 Pilot-02 子實驗 • 960 cells • 救回 5 格 • 49 vs 26 • Healer只修窄小且可驗證的窗口。

## Frozen accounting retained
- 4B Baseline 78/320; Primary 83/320 (rescue=5); Post-hoc 84/320 (total rescue=6; +1 PASS).
- Gemini Primary 289/320; Gemini Post-hoc 306/320.

## Figure 2 warning
- Gemini 80/80 is Post-hoc.
- Primary spec-v1=63/80.
- Qwen uses spec-v2.
- No fully matched-condition causal inference.

## BBox verification
- Named elements: 20; pairs: 190; passing: 190; collisions: 0.
- Renderer get_window_extent() and get_position() measurements were used; any overlap fails the build.

## Output SHA-256
- PNG: `9468ce23bbdc9af01878eb9e5c02b08febdad980ebca22449653d9fe8e92e5e4`
- PDF: `6a7f495092167d95a7bebbddf735bd4a680c23adbac611df290d1caea55f44bd`
