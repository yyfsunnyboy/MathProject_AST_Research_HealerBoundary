# Qwen4B Pilot-02 Post-hoc Corrected-Chain Healer Replay

```text
QWEN4B_POSTHOC_HEALER_REPLAY_COMPLETED
QWEN4B_CORRECTED_CHAIN_RESULTS_FROZEN
QWEN4B_PRIMARY_RESULT_PRESERVED
QWEN4B_QWEN9B_COMPARISON_READY
```

**Nature:** post-hoc corrected-chain — **not** preregistered primary.

- Primary post-Healer (preserved): **83/320** (rescued=5)
- Corrected-chain post-Healer: **84/320**
- Replayed eligible only: **10**
- Noneligible executed: **0**
- Rescued / repaired-still-fail / no-op / regression: **6 / 4 / 0 / 0**
- Healer runner SHA: `38453d1294382f061efe149484f5a3059a47d085d2aeef358874a954e37adebf`
- Protocol SHA: `bdb4121ee266f91bfa116019a334cf4a528da0d71629b96540a5f763826aff39`
- LLM calls: **0**

## Primary vs corrected-chain (eligible 10)

| Cell | Primary | Corrected | Same |
| :--- | :--- | :--- | :---: |
| `qwen3_5_4b__ce112_q04_radical_simplification__ab2g__seed_2026072002` | repaired_still_fail | repaired_still_fail | true |
| `qwen3_5_4b__ce112_q04_radical_simplification__ab2g__seed_2026072004` | rescued | rescued | true |
| `qwen3_5_4b__ce112_q09_divisor_multiple_intersection__ab2d__seed_2026072001` | no_op | repaired_still_fail | false |
| `qwen3_5_4b__ce113_q01_negative_fraction_subtraction__ab2d_spec_v2__seed_2026072002` | rescued | rescued | true |
| `qwen3_5_4b__ce113_q01_negative_fraction_subtraction__ab2g__seed_2026072003` | rescued | rescued | true |
| `qwen3_5_4b__ce115_calc_exact_rational_expression_l1__ab1__seed_2026072004` | repaired_still_fail | repaired_still_fail | true |
| `qwen3_5_4b__ce115_calc_polynomial_factor_roots_l1__ab2d_spec_v2__seed_2026072002` | repaired_still_fail | repaired_still_fail | true |
| `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d__seed_2026071301` | no_op | rescued | false |
| `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d__seed_2026072002` | rescued | rescued | true |
| `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d_spec_v2__seed_2026071301` | rescued | rescued | true |

## Condition

| Condition | Baseline | Post-Healer | Eligible | Rescued |
| :--- | ---: | ---: | ---: | ---: |
| Ab1 | 15/80 | 15/80 | 1 | 0 |
| Ab2g | 19/80 | 21/80 | 3 | 2 |
| Ab2d+api | 8/80 | 10/80 | 3 | 2 |
| Ab2d+spec-v2 | 36/80 | 38/80 | 3 | 2 |

## Family

| Family | Baseline | Post-Healer | Eligible | Rescued |
| :--- | ---: | ---: | ---: | ---: |
| Integer | 30/80 | 30/80 | 1 | 0 |
| Polynomial | 16/80 | 16/80 | 1 | 0 |
| Radical | 15/80 | 19/80 | 5 | 4 |
| Fraction | 17/80 | 19/80 | 3 | 2 |
