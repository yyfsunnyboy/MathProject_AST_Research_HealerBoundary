# Math16 Figure 2 Post-hoc Presentation Correction v1

Report date: 2026-07-28  
Scope: **Figure 2 only** (no Batch 4–7; no other figures).  
Result: **PASS**

## 1. Reason

The previous Figure 2 Ab2d+spec Gemini presentation used a hatched hollow Post-hoc bar plus an in-bar Primary 63/80 callout. That dual-track visual competed with the trio comparison and cluttered the legend. Presentation policy now shows a **single solid Gemini bar at Post-hoc 80/80**, with Primary 63/80 disclosed only in a transparent footnote.

## 2. Old → new visual rules

| Element | Old | New |
|---|---|---|
| Ab2d+spec Gemini bar | Hatched hollow blue (Post-hoc 80) | **Solid blue** height 80 |
| Top label | `80/80 Post-hoc` | **`80/80*`** |
| In-bar Primary box | `Primary spec-v1 = 63/80` | **Removed** |
| Legend | 4 items (Gemini Primary + Gemini Post-hoc hatch + 9B + 4B) | **3 items:** Gemini 3.5 Flash* · Qwen3.5 9B · Qwen3.5 4B |
| Footnote | Explained hatch dual-track | Star note: Post-hoc 80/80; Primary 63/80 disclosed in text only |

Unchanged numeric cells: Ab1 72/18/15 · Ab2g 76/27/19 · Ab2d+api 78/16/8 · Ab2d+spec Gemini 80 / 9B 40 / 4B 36. Order G→9B→4B. Color identity unchanged.

## 3. Star footnote (full text)

```text
* Gemini 3.5 Flash 的 Ab2d+spec 採 Post-hoc spec-v2，結果為 80/80；原 Primary spec-v1 為 63/80。
其他 Gemini 條件及 Qwen3.5 9B／4B 均為各自正式結果。每組柱順序：Gemini → Qwen3.5 9B → Qwen3.5 4B。
```

Required tokens present: Post-hoc spec-v2 · 80/80 · Primary spec-v1 · 63/80.

## 4. Artifacts / SHA

| Artifact | SHA-256 |
|---|---|
| Renderer `scripts/render_math16_pilot02_amended_figures_v1.py` | `70c25bca80838d9332f656dc013f6fd71e77c2ec4eb673d59fef4603ccd52ce5` |
| Staging SVG `…/staging/figure_02_condition_breakdown.staging.svg` | `d40766065f780c0760c2923c92e204d7e1d19b8257261417dd5c79e044dd307c` |
| Canonical SVG `…/figure_02_prompt_conditions.svg` | `d40766065f780c0760c2923c92e204d7e1d19b8257261417dd5c79e044dd307c` (= staging) |
| Canonical PNG `…/figure_02_prompt_conditions.png` | `8b72c42e4e8590a0fd67388a3b1c30317d174521fc9469beff1d6fae25ddae5f` |
| PNG dimensions | **2268×1296** (viewBox 756×432 × scale 3) |

PNG export command:

```text
"C:\Program Files\Inkscape\bin\inkscape.exe" --export-type=png --export-filename=<png> --export-width=2268 <svg>
```

No browser screenshot. Figures 1/3/4/5 SVG+PNG SHA verified unchanged.

## 5. Visual check (PNG opened)

- Solid blue Ab2d+spec Gemini; label `80/80*` only  
- No hatch; no 63/80 in-bar box  
- Legend exactly three items in G→9B→4B order  
- Footnote complete; no overlap/crop/layout break  
- Other condition values unchanged  
- Tight viewBox crop  

**PASS**

## 6. Scope

Modified only: amendment renderer; Fig2 staging/canonical SVG; Fig2 canonical PNG; this report; Batch 3 report cross-note.  
Not modified: presentation claims numbers; Figs 1/3/4/5/6; frozen builder/claims/results/tests; formal docs; One-Pager/Poster/package; no commit/push.
