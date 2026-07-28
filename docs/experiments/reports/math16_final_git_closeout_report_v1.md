# Math16 Final Git Closeout Report v1

Report date: 2026-07-29  
Repo: `C:\Projects\MathProject_AST_Research_HealerBoundary`  
Result: **PASS** (pending final SHA fill after commit/push in §7–8)

## 1. Starting state

| Item | Value |
|---|---|
| Starting `HEAD` | `63564e959aea6164bad33a3794ea2a67778a08a5` |
| Starting `origin/main` | `63564e959aea6164bad33a3794ea2a67778a08a5` |
| Branch | `main` |

Inventory captured via `git status --short`, `git diff --name-status`, `git ls-files --others --exclude-standard` before staging.

## 2. Classification summary

| Class | Count (paths) | Policy |
|---|---:|---|
| **A. MUST_COMMIT** | 55 | Official package, Batch 3–5 deliverables, presentation/spec sync |
| **B. COMMIT_AS_SUPPORTING_EVIDENCE** | 60 | Amendment layer, audit/scratch, batch reports, renderer, closeout report |
| **C. EXCLUDE_OR_DELETE** | 6 | Closeout helper temps only |
| Poster residual | restored | Not committed |

Staged total before commit = **115** paths (`git diff --cached --name-only`).

### A. MUST_COMMIT

- `docs/決賽文件/實驗結果文件/Math16/**` (new official package; PDF force-added despite `*.pdf` gitignore)
- `docs/決賽文件/實驗結果文件/20260724_Math16/01_…final_report…` + `04_…jury_qa…` (Batch 5 正本)
- One-Pager v23 assets/PNG/PDF/manifest/build report + `scripts/build_math16_pilot02_one_pager_v23.py`
- Canonical `math16_pilot02_core_figures_v1` Figure 1–5 SVG/PNG
- `math16_pilot02_core_figure_spec_v1` caption/governance/selection/JSON/report
- Presentation text: integrated report, jury sync, Method1/Method2/handoff claim sync

### B. COMMIT_AS_SUPPORTING_EVIDENCE

- `math16_pilot02_amendment_layer_v1/` — claims, renderer spec, staging SVG/preview, `wt_backup/`, `batch3_rollback/`, `batch3_png_correction_backup/` (incl. superseded Edge PNGs + `old_png_manifest.json`)
- `docs/experiments/reports/_scratch_confirmatory_reeval_320/**` — unique 78 vs 79 confirmatory evaluator output (cited by discrepancy audit §10)
- Baseline 79 amendment plans/specs/decision/validation + Correction Note
- Combined amendment batch0–5 / execution / asset map / figure2 posthoc / global model order / M1↔M2 audit + extraction closure CSV/JSON
- `math16_final_package_consolidation_report_v1.md`
- `scripts/render_math16_pilot02_amended_figures_v1.py`
- This closeout report

### C. EXCLUDE_OR_DELETE

Deleted (not committed):

| Path | Reason |
|---|---|
| `_closeout_preflight.py` | One-shot closeout helper |
| `_closeout_preflight.json` | Temp preflight dump |
| `_closeout_classify.json` | Temp classifier dump |
| `docs/experiments/reports/_closeout_inventory_status.txt` | Temp inventory |
| `docs/experiments/reports/_closeout_inventory_diff_name_status.txt` | Temp inventory |
| `docs/experiments/reports/_closeout_inventory_untracked.txt` | Temp inventory |

No uncertain deletions. No cache / `__pycache__` / `Thumbs.db` / `desktop.ini` submitted.

## 3. Poster handling

| Action | Detail |
|---|---|
| Restored to HEAD | `docs/experiments/presentation/math16_pilot02_poster_v11/**` |
| Restored to HEAD | `scripts/build_math16_pilot02_poster_v11.py` |
| Unchanged | `poster_and_oral_figure_order.md` (no dirty state) |
| Commit inclusion | **None** — Poster is not a formal deliverable this round |

Command used: `git checkout HEAD -- docs/experiments/presentation/math16_pilot02_poster_v11 scripts/build_math16_pilot02_poster_v11.py`

## 4. Scratch / staging / rollback retention

| Path | Decision | Reason |
|---|---|---|
| `_scratch_confirmatory_reeval_320/` | **KEEP + commit** | Sole confirmatory 78↔79 re-eval evidence; cited by audit |
| `amendment_layer_v1/staging/` | **KEEP + commit** | Batch1/2 SHA chain |
| `amendment_layer_v1/wt_backup/` | **KEEP + commit** | Batch0 rollback |
| `amendment_layer_v1/batch3_rollback/` | **KEEP + commit** | Batch3 promote rollback |
| `amendment_layer_v1/batch3_png_correction_backup/` | **KEEP + commit** | Cited backup of superseded Edge PNGs + SHA manifest |
| Closeout `_closeout_*` helpers | **DELETE** | Pure temp |

Frozen evidence (78/83/84) untouched. `20260722_Math16/**` zero changes.

## 5. Math16 package verification

| Check | Result |
|---|---|
| Package path | `docs/決賽文件/實驗結果文件/Math16/` |
| Contents | README, Final Report, One-Pager PNG/PDF, Jury, Correction Note, Fig1–6 SVG+PNG, appendix, manifest |
| Core numbers | Gemini 289/320; 9B 101/320; 4B Baseline 79/320; Final 85/320; rescue 6; Tier1 52/27/49/192; p=0.015440; Polynomial 17/80; Gemini Ab2d+spec 80/80*; Primary 63/80 |
| Model order | Gemini → Qwen3.5 9B → Qwen3.5 4B |
| Manifest SHA | **PASS** (19 entries) |
| Markdown relative links | **0 broken** |
| One-Pager PNG | 3619×2541 |
| One-Pager PDF | 1 page |
| PDF gitignore | Force-added `03_…one_pager_v23.pdf` (repo `*.pdf` ignore; same pattern as prior packages) |

## 6. Technical checks

| Check | Result |
|---|---|
| `git diff --check` | **WARN** — trailing whitespace on matplotlib SVG path lines (Fig1–5). Not stripped (would change canonical SVG SHA). Not treated as blocker. |
| JSON parse | **PASS** (amended claims/spec + report JSON set) |
| `python -m py_compile` | **PASS** — `build_math16_pilot02_one_pager_v23.py`, `render_math16_pilot02_amended_figures_v1.py` |
| Junk patterns in status | **PASS** — no `__pycache__` / `.pyc` / `Thumbs.db` / `desktop.ini` |
| Poster dirty | **PASS** — absent after restore |
| `20260722` dirty | **PASS** — untouched |
| Model / Healer / Evaluator / formal stats rerun | **Not run** (per closeout rules) |

## 7. Commit / push

| Item | Value |
|---|---|
| Message | `finalize Math16 corrected reporting and official package` |
| Staging | Explicit paths only (no blind `git add -A`); PDF via `git add -f` |
| Commit SHA | _(filled after commit)_ |
| Push | _(filled after push)_ |

## 8. Ending state

| Item | Value |
|---|---|
| Ending `HEAD` | _(filled)_ |
| Ending `origin/main` | _(filled)_ |
| `HEAD == origin/main` | _(filled)_ |
| `git status --short` | _(filled)_ |
| GitHub Desktop Changes | Should show **0** after pull/refresh |

## 9. Hard constraints checklist

- [x] No `git reset --hard`
- [x] No frozen-evidence deletion
- [x] No `20260722_Math16/**` edits
- [x] No unapproved Poster updates in commit
- [x] No pure temp junk pushed
- [x] Confirmatory scratch retained
