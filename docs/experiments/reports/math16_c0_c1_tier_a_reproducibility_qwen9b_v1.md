# Math16 C0→C1 Tier A Reproducibility — Qwen9B v1

> **AUTHORITY:** NONAUTHORITATIVE_ALL_CELL_EXPLORATORY — exploratory all-cell; not FAIL-only authoritative.
> **Authoritative namespace:** qwen9b_fail_gated_authoritative_v1


> **verdict:** `C0_C1_TIER_A_QWEN9B_COMPLETE`
> **HEAD:** `72117d3facd48b8e78af534290dc7dcd2001149a`
> **results:** `docs/experiments/results/math16_c0_c1_tier_a_reproducibility_qwen9b_v1`

## Core counts

| Metric | Value |
|---|---:|
| C0 authority PASS | 101 |
| Phase B raw PASS | 101 |
| C1 final PASS | 101 |
| verified_rescue | 0 |
| regression | 0 |
| preserved_pass | 101 |
| still_failed | 219 |
| eligible / modified | 0 / 0 |
| modified still failed | 0 |
| parse_gain | 0 |
| execution_gain | 0 |

## Rule accounting

Frozen Tier A six-rule allowlist (order unchanged vs Method2 4B):

| Rule | triggered | modified | rescue |
|---|---:|---:|---:|
| `L1_CLOSE_UNBALANCED_PARENTHESIS` | 0 | 0 | 0 |
| `L1_CLOSE_UNBALANCED_DELIMITER_EXTENDED` | 0 | 0 | 0 |
| `L1_PROSE_RESIDUE_NARROW` | 0 | 0 | 0 |
| `L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP` | 0 | 0 | 0 |
| `L2_KWARGS_EMPTY_BAG_INLINE_UNIQUE_PARAM` | 0 | 0 | 0 |
| `L2_CORRECT_ANSWER_JSON_DUMPS_UNWRAP` | 0 | 0 | 0 |
| `NONELIGIBLE` (all 320) | 0 | 0 | 0 |

## Determinism / tests

- Second Phase A replay zero-diff: **True**
- Focused protocol unit tests: **7 passed**; 1 pre-existing 4B `verify_pins` failure on CRLF-vs-LF working-tree bytes for two L1 files (content-equal after newline normalization; **not** introduced by this 9B run)

## Declarations

- Model calls: **0**
- Healer rules / thresholds / order modified: **No**
- 4B artifacts modified: **No**
- Commit / push: **No**
