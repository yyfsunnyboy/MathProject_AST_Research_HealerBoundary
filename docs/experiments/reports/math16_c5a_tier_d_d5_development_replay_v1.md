# Math16 C5a Tier D D5 Development Replay v1

> **verdict:** `NO_DEVELOPMENT_GAIN`
> **cell:** `qwen3_5_4b__ce113_q11_rationalize_denominator__ab2d__seed_2026072003`
> **HEAD:** `f0eae63fe8c3760e9912589654657510119175ce`
> **TIER_D_4B_EXPLORATION_CLOSED:** true

## Ledger (separate from D2 / D3 / D1)

| Field | Value |
|---|---|
| triggered / modified / abstained | true / true / false |
| pre → post SHA | `add4133b…` → `bd3201f6…` |
| parse / executable | no gain; no regression |
| PASS/FAIL | FAILED → FAILED (`answer_incorrect` → `answer_incorrect`) |
| verified rescue | 0 |
| still failed | 1 |
| degradation | none |
| edit distance | 2 |
| binding | `FractionOps.sqrt` → `create` (score=18.4, margin≈3.4) |
| reason | Ranked binding applied; answer still incorrect |

## Declarations

- C5a final source only; 1 cell; no model calls
- Evaluator observation-only (not used for selection)
- Second apply zero-diff; arguments preserved
- Not Confirmatory; no other Tier D rules in this replay
