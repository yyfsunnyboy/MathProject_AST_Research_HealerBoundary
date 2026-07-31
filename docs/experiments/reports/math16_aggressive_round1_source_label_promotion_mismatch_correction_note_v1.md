# Math16 Aggressive Round 1 — Source–Label Promotion Mismatch Correction Note v1

Note date: 2026-07-30  
Status: **formal correction note, analysis/reporting overlay only.**  
Frozen manifests／journals／labels／sealed sources／evaluator／rules／runner／protocol are **not** modified.

Machine-readable overlay:  
`docs/experiments/manifests/math16_aggressive_round1_corrected_overlay_v1.json`

---

## 1. What is frozen and never changes

- Round 1 sealed population lock remains **Final PASS 88／FAIL 232** in:
  - `docs/experiments/manifests/math16_c5a_final_source_closure_v1.json`
  - `docs/experiments/manifests/math16_three_model_round1_summary_v1.json`
  - all C0–C5 journals／post_sources／fixpoint & Aggressive population loaders
- Cell journal labels, `c5a_outcome`, `source_origin`, and sealed source bytes are permanent historical evidence.
- Conservative／Method 1／Method 2 formal ledger **Baseline 79 → Final 85、verified rescue 6** is **unaffected**.
- This note corrects **analysis／reporting／downstream accounting overlays only**.

---

## 2. Anomalous cell (evidence)

| Field | Value |
|---|---|
| `cell_id` | `qwen3_5_4b__ce112_q04_radical_simplification__ab2d__seed_2026072003` |
| Sealed path | `docs/experiments/results/math16_c0_c1_tier_a_reproducibility_v1/final_sources/…seed_2026072003.py` |
| Manifest SHA (text／UTF-8) | `67844bb65356bdce44c35032033d3d80099b822e843dcd07ef4000bb5d18eed4` |
| `source_origin` | `PRIOR_PASS_PRESERVED` |
| `c5a_outcome` | `PASS` |
| `verified_rescue` (C5a flag) | `false` |
| Round 1 D3／D1 | `NO_OP`／`not_in_c4_residual` |
| `ast.parse` | `IndentationError`／empty suite after `if radicand_val == 135:` |
| Observational evaluator | `parse_minor` → `final_status=FAILED` |

**Qualitative label:** lineage bookkeeping／source–label promotion mismatch — **not** an evaluator determinism failure (319／320 sealed-source revalidation matches frozen labels).

C2 Tier B development replay once produced EMPTY_SUITE repair (`67844…` → `f00f3e…`, FAIL→PASS), but **repaired bytes were not promoted** into the Round 1 sealed final source. Cumulative accounting still booked C2 **+1**, which later entered Final PASS via `PRIOR_PASS_PRESERVED`.

---

## 3. Aggressive Round 1 overlay

| Ledger | Baseline P／F | Final P／F | verified rescue | rate (／Baseline FAIL) |
|---|---:|---:|---:|---|
| **Frozen archive** | 79／241 | **88／232** | **9** | **9／241 = 3.73%** |
| **Corrected overlay** | 79／241 | **87／233** | **8** | **8／241 = 3.32%** |

True sealed-source rescue decomposition:

- Tier A (Conservative allowlist): **6**
- D1 active-shadow (`ACTIVE_SHADOW_REPLACED_BY_RUNTIME_API`, seeds 2026071301／2002): **2**
- C2 +1: **phantom account** (development replay success without sealed-byte promotion)

Corrected pass curve (analysis overlay):  
`C0 79 → C1 85 → C2 85 → C3 85 → C4 85 → C5a/C5b/C5c 87`

Frozen curve remains:  
`79 → 85 → 86 → 86 → 86 → 88 → 88 → 88`

---

## 4. Fixpoint limitation

- Fixpoint v1 executed under **frozen** population lock **88 PASS excluded／232 FAIL active**.
- Result **232／232 `ZERO_CHANGE_CONVERGENCE`、additional rescue＝0** holds **only** for that frozen active set.
- Corrected residual FAIL count is **233**; the anomalous cell was **not scanned** (excluded as frozen PASS).
- **Do not** claim fixpoint v1 covers all corrected residual FAIL cells.
- **This round does not** re-run fixpoint v2.

---

## 5. Aggressive 320-cell safety benchmark dual account

Formal run artifacts (uncommitted results root) retain frozen-label **primary** journal accounting.  
Analysis adds **sealed-source sensitivity** for the single mismatched cell (EMPTY_SUITE → PASS; subsequent D1＝dead-shadow cleanup only; **not** the D1 active-shadow rescues of 1301／2002).

| Account | input P／F | preserved_pass | regression | verified_rescue | unchanged_fail | net PASS change |
|---|---:|---:|---:|---:|---:|---:|
| Frozen-label primary | 88／232 | 88 | 0 | 0 | 232 | 0 |
| Sealed-source sensitivity | 87／233 | 87 | 0 | 1 | 232 | +1 |

---

## 6. Three-model Final PASS sealed-source consistency（479 cells）

Read-only revalidation of **all frozen Final PASS** sealed sources（no model／Healer／benchmark／fixpoint re-run; frozen labels／bytes untouched）:

| Model | Frozen Final PASS source | n | PASS→PASS | PASS→FAIL | SHA mismatch | missing | eval error |
|---|---|---:|---:|---:|---:|---:|---:|
| Qwen 4B | C5a closure | 88 | 87 | **1** | 0 | 0 | 0 |
| Qwen 9B | C5c closure | 102 | 102 | 0 | 0 | 0 | 0 |
| Gemini | C5c closure | 289 | 289 | 0 | 0 | 0 | 0 |
| **Total** | Round1 Final PASS | **479** | **478** | **1** | **0** | **0** | **0** |

- Unique mismatch：`qwen3_5_4b__ce112_q04_radical_simplification__ab2d__seed_2026072003`（same cell as §2；text SHA matches manifest；reval `FAILED／parse_minor`）.
- 9B／Gemini：**0** mismatch.
- Conclusion：**not** a systemic evaluator or sealed-source failure；single 4B lineage bookkeeping／promotion defect. Sealed-consistent three-model Final PASS＝**478**（frozen archive still **479** labels）.

---

## 6.1 479-cell final overlay audit

The local, read-only audit records the two accounts separately: frozen Final PASS＝**479**（Qwen 4B **88**／Qwen 9B **102**／Gemini **289**）；the corrected overlay matches **1** target and gives **PASS→FAIL＝1**, so corrected Final PASS＝**478**（Qwen 4B **87**／Qwen 9B **102**／Gemini **289**）. The other **478** cells retain their frozen final result. `duplicate=0`、`missing=0`、`unmatched=0`、`SHA mismatch=0`, and two deterministic builds are byte-stable. The sole target is `qwen3_5_4b__ce112_q04_radical_simplification__ab2d__seed_2026072003`; its sealed source SHA-256 is `67844bb65356bdce44c35032033d3d80099b822e843dcd07ef4000bb5d18eed4`. Audit evidence: `scripts/build_math16_historical_round1_final_overlay_audit_v1.py`; `docs/experiments/results/math16_historical_round1_final_overlay_audit_v1/final_overlay_audit.jsonl`; `docs/experiments/results/math16_historical_round1_final_overlay_audit_v1/validation_summary.json`; `docs/experiments/results/math16_historical_round1_final_overlay_audit_v1/sha256_manifest.json`.

---

## 7. Documents／artifacts disposition

| Class | Action |
|---|---|
| Frozen C5a／Round1 summary／journals／sealed sources | **never edit** |
| Analysis reports／handoff／teacher brief／comparison／Final Report／Jury Q&A | cite frozen + corrected overlay |
| Round1 chart SVG／primary `round1_chart_data_v1.json` | retain frozen display; overlay JSON is authoritative for corrected numbers |
| Aggressive `summary.json` | primary fields unchanged; add sensitivity block |
| Fixpoint protocol／results | annotate limitation only; no re-run |

---

## 8. Declarations

- Zero model calls; zero Healer re-runs; zero formal benchmark／fixpoint re-execution for this note.
- No rule／runner／protocol／evaluator edits.
- No overwrite of frozen labels or sealed bytes.
- Conservative 79→85／rescue 6 unchanged.
- 479-cell audit＝import-only observational re-score of sealed Final PASS sources（stdout／memory only）.
