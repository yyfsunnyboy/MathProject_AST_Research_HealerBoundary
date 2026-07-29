# Math16 C5a Final-Source Closure v1

> **verdict:** `C5A_CLOSURE_PASSED`
> **definition:** `C5a = C4 + D3 + D1`
> **HEAD:** `f0eae63fe8c3760e9912589654657510119175ce`

## Validation

- Cells: **320** (unique 320, duplicates 0)
- PASS / FAIL: **88** / **232** (expected 88 / 232)
- source_origin: `{'C4_PRESERVED': 227, 'PRIOR_PASS_PRESERVED': 86, 'TIER_D_D3_D1_POST_SOURCE': 7}`
- Verified rescue (2): ['qwen3_5_4b__ce112_q04_radical_simplification__ab2d__seed_2026071301', 'qwen3_5_4b__ce112_q04_radical_simplification__ab2d__seed_2026072002']
- Modified-still-failed (5): post-source SHA matched replay
- Passed: **True**

## Lineage policy

- Prior PASS 86 → `PRIOR_PASS_PRESERVED`
- D3/D1 modified → `TIER_D_D3_D1_POST_SOURCE`
- Unmodified C4 residual → `C4_PRESERVED`

## Declarations

- No mutation beyond lineage bookkeeping of existing replay post-sources
- No evaluator / model calls in this closure step
