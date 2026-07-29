# Math16 C3→C4 Tier C2 Reproducibility — Qwen9B v1

> **AUTHORITY:** NONAUTHORITATIVE_ALL_CELL_EXPLORATORY — exploratory all-cell; not FAIL-only authoritative.
> **Authoritative namespace:** qwen9b_fail_gated_authoritative_v1


> **verdict:** `C3_C4_TIER_C2_QWEN9B_COMPLETE`
> **Go/No-Go:** `EXPLORATORY_ONLY`
> **HEAD:** `72117d3facd48b8e78af534290dc7dcd2001149a`

## Core counts

- C3 PASS observed／C4 PASS: **102／102**
- verified_rescue／regression: **0／0**
- preserved_pass／still_failed: **102／218**
- triggered／modified／abstained: **10／10／310**
- parse_gain／execution_gain／modified_still_failed: **0／0／6**
- Second replay zero-diff: **True**

## Cell-gating provenance (notes only; tallies unchanged)

- Candidate pool: **ALL_CELL_SCAN_NO_FAIL_GATE** over C3 final **320** (not FAIL-only residual).
- Modified split: **10 = 4 PASS→PASS + 6 FAIL→FAIL**; PASS→PASS booked as `preserved_pass`, not rescue.
- vs 4B Tier C2 residual (234 FAIL-only): **DIFFERENT_SCOPE_BUT_VALID**; no runner／gating bug; no C3→C4 re-run.
- Detail: `docs/experiments/reports/math16_qwen9b_c3_c4_tier_c2_cell_gating_provenance_v1.md`

## Declarations

- Model calls: **0**
- Guards relaxed: **No**
- Tier D executed: **No**
- Commit／push: **No**
