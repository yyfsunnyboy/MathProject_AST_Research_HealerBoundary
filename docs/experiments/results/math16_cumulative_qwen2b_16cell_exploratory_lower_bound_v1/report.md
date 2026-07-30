# Math16 Cumulative Report — qwen2b_16cell_exploratory_lower_bound_v1

> **AUTHORITY:** `EXPLORATORY_LOWER_BOUND_FAIL_GATED_V1`
> **Evidence role:** exploratory lower-bound（非三模型正式主表）
> **HEAD:** `2e9711f7847231880150f9d549dfc74aed6ade85`

## Headline

- Baseline → Final PASS: **0／16 → 0／16**
- Total verified rescue: **0**
- Total regression: **0**
- Model calls: **0**

## PASS curve

| Stage | PASS | FAIL |
|---|---:|---:|
| C0 | 0 | 16 |
| Tier A | 0 | 16 |
| Tier B | 0 | 16 |
| Tier C1 | 0 | 16 |
| Tier C2 | 0 | 16 |
| D3 | 0 | 16 |
| D1 | 0 | 16 |
| D5 | 0 | 16 |
| D2 | 0 | 16 |

## Per-layer ledger

| Layer | gated | eligible | ambiguous | modified | abstained | rescue | parse | exec | blocker | msf | regression |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Tier A | 16 | 2 | 0 | 2 | 14 | 0 | 1 | 0 | 1 | 2 | 0 |
| Tier B | 16 | 0 | 0 | 0 | 16 | 0 | 0 | 0 | 0 | 0 | 0 |
| Tier C1 | 16 | 0 | 0 | 0 | 16 | 0 | 0 | 0 | 0 | 0 | 0 |
| Tier C2 | 16 | 0 | 0 | 0 | 16 | 0 | 0 | 0 | 0 | 0 | 0 |
| D3 | 16 | 1 | 2 | 1 | 15 | 0 | 0 | 0 | 0 | 1 | 0 |
| D1 | 16 | 1 | 0 | 1 | 15 | 0 | 0 | 0 | 0 | 1 | 0 |
| D5 | 16 | 0 | 0 | 0 | 16 | 0 | 0 | 0 | 0 | 0 | 0 |
| D2 | 16 | 0 | 0 | 0 | 16 | 0 | 0 | 0 | 0 | 0 | 0 |

## Declarations

- No model calls; sealed raw only (smoke + timeout-rerun fill).
- No new rules; no guard／threshold／order changes.
- No Round 2; not mixed into three-model Round 1 primary tables.
