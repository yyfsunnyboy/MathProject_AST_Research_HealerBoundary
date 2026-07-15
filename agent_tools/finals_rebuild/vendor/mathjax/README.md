# Vendored MathJax 3.2.2 (offline)

## Files

| File | Role |
|---|---|
| `tex-svg.js` | MathJax 3.2.2 es5 TeX→SVG combined bundle (~2.1 MiB) |
| `SHA256SUMS` | SHA-256 of `tex-svg.js` |
| `LICENSE` | Apache-2.0 notice for redistribution |
| `README.md` | This provenance note |

## Provenance

- Package: MathJax
- Version: **3.2.2**
- Bundle path: `es5/tex-svg.js`
- Upstream project: https://github.com/mathjax/MathJax
- License: Apache License 2.0 (see `LICENSE`)
- Purpose: Milestone 3E G6b browser renderer validation and offline HTML
  evidence reports using the same TeX delimiter/macro policy as
  `templates/index.html`

## Runtime policy

- Load only via `file://` or relative repo path
- No CDN, no network fetch during validation/report build
- Do not replace this file with a different major/minor without updating
  `SHA256SUMS` and re-running G6b regression tests

## SHA-256

See `SHA256SUMS` for the exact digest of `tex-svg.js` in this tree.
