# Math16 C1→C2 Tier B Reproducibility — Qwen9B v1

> **AUTHORITY:** NONAUTHORITATIVE_ALL_CELL_EXPLORATORY — exploratory all-cell; not FAIL-only authoritative.
> **Authoritative namespace:** qwen9b_fail_gated_authoritative_v1


> **verdict:** `C1_C2_TIER_B_QWEN9B_COMPLETE`
> **HEAD:** `72117d3facd48b8e78af534290dc7dcd2001149a`
> **results:** `docs/experiments/results/math16_c1_c2_tier_b_reproducibility_qwen9b_v1`
> **input:** 9B C1 final source 320（PASS=101）

## Core counts

| Metric | Value |
|---|---:|
| C1 PASS (authority／observed) | 101／101 |
| C2 PASS／FAIL | 102／218 |
| verified_rescue | 1 |
| regression | 0 |
| preserved_pass | 101 |
| still_failed | 218 |
| modified／modified still failed | 4／3 |
| parse_gain | 4 |
| execution_gain | 2 |
| blocker_removal_only（≠ verified rescue） | 3 |

## Tier B rule accounting

| Rule | triggered | modified | abstained | rescue |
|---|---:|---:|---:|---:|
| `core.normalize_fullwidth_python_punctuation` | 0 | 0 | 320 | 0 |
| `TIER_A_UNIQUE_MISSING_DELIMITER_REPAIR_V1` | 0 | 0 | 320 | 0 |
| `TIER_A_EMPTY_SUITE_INSERT_PASS_V1` | 4 | 4 | 316 | 1 |
| `TIER_A_UNIQUE_IMPORT_BINDING_REPAIR_V1` | 0 | 0 | 320 | 0 |

## Determinism / freeze

- Second pipeline replay zero-diff: **True**
- Rule order matches frozen: **True**
- Order: `['core.normalize_fullwidth_python_punctuation', 'TIER_A_UNIQUE_MISSING_DELIMITER_REPAIR_V1', 'TIER_A_EMPTY_SUITE_INSERT_PASS_V1', 'TIER_A_UNIQUE_IMPORT_BINDING_REPAIR_V1']`

## Declarations

- Model calls: **0**
- Rules／thresholds／order modified: **No**
- 4B artifacts modified: **No**
- Tier C／D executed: **No**
- Commit／push: **No**
