# CE115 G6 Renderer Equivalence (Milestone 3E)

Compares the offline G6b probe / evidence report renderer with the formal
frontend in `templates/index.html`.

## Identical settings

| Item | Formal frontend | G6b / report probe |
|---|---|---|
| Engine | MathJax 3 `tex-svg.js` | Vendored MathJax **3.2.2** `tex-svg.js` |
| inlineMath | `[['$', '$'], ['\\(', '\\)']]` | same |
| macro `dfrac` | `{\\displaystyle\\frac{#1}{#2}}` | same |
| svg.fontCache | `global` | same |

## Equivalent substitutions

| Item | Formal frontend | Evidence / G6b |
|---|---|---|
| Script source | CDN `mathjax@3/es5/tex-svg.js` | Local vendor file (no CDN) |
| displayMath | not explicitly set (MathJax defaults) | explicit `$$` / `\\[` (compatible) |
| startup.typeset | default auto | `false` then explicit `typesetPromise` (same end state) |

## Known differences (require G6c human visual review)

| Item | Formal frontend | G6b probe | Impact |
|---|---|---|---|
| Markdown pipeline | App may transform text before MathJax | Probe inserts raw `actual_question_text` / answer HTML | Escaping / markdown order may differ |
| Container width | Fluid chat / question pane | Fixed **720px** probe root | Line wraps / clipping thresholds differ |
| Font size / line-height | Question pane ~1.25em / 1.8; chat 16px / 1.8 | Probe `.mjx-target` 18px / 1.5 | Visual density differs |
| mjx CSS tweaks | `mjx-container` margins; STIX math font override | Minimal probe CSS only | Spacing / font metrics differ |
| overflow | Chat panes `overflow-y: auto`; several `overflow: hidden` | Probe block `overflow: auto; max-height: 480px` | Clipping signals are heuristic |
| Overlap | Not auto-gated in UI | Recorded as **evidence/warning only** (not automatic FAIL) | Human G6c adjudicates |

G6b FAIL is reserved for renderer errors, leftover TeX commands after typeset,
and overflow/clipping beyond the probe threshold. Visual readability remains G6c.
