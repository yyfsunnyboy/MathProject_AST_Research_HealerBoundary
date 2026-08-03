# Math16 Contract-Aware Aggressive Healer v2 — 28-cell evaluator replay summary

**Tag:** `PC_R01_TO_R04_FINAL`  
**Git HEAD at freeze record:** `fbf010151e6bf89d2b56f4d8a0c79a506a561f69`  
**Replay UTC:** `2026-08-03T14:36:09.408897+00:00`

## Freeze SHA inventory

| Component | SHA-256 |
|---|---|
| `aggressive_healer_contract_v2/` tree | `f6dcfd2f79015a0541d8bbcd3e388f548adee49c154e3c685dd5752277c0857e` |
| `aggressive_healer_v2_integrated.py` | `dbd3880d181f7ac4792c4bf1dad239cb38fc5f4874aa0ccaba8e54b914440e8a` |
| frozen_manifest content | `4b45ec08784146b567b01ae5f46d561d76cf10209df7b50f5eedd87d396853e5` |
| **PC_R01_TO_R04_FINAL aggregate** | `1d5ecbc4a21f9985e38f418adbeba41672c757668c4a05f83e40dc97d59ec128` |

Full-machine replay ledgers (cell sources, large JSON) remain under gitignored  
`artifacts/math16_contract_aware_aggressive_healer_v2/`.

## Overview (28 changed cells only)

| Metric | n |
|---|---:|
| verified_rescue | 9 |
| modified_still_failed | 19 |
| regression | 0 |
| PASS→PASS | 0 |

### By rule source

- **PC_ONLY**: n=6, rescue=6, still_fail=0, regression=0
- **TIER_AD_ONLY**: n=22, rescue=3, still_fail=19, regression=0
- **BOTH**: n=0

### By model × condition

- **qwen_4b+full**: verified_rescue=5, modified_still_failed=1
- **qwen_4b+menu**: verified_rescue=4, modified_still_failed=13
- **qwen_9b+menu**: modified_still_failed=5

## V2 final Raw → Healed PASS

| | n | /480 |
|---|---:|---:|
| Raw PASS | 381 | 79.375% |
| Healed PASS | 390 | 81.250% |
| Net gain | +9 | +1.875 pp |

Method: `raw_pass + verified_rescue - regression` (unchanged cells keep raw outcome).  
381 raw PASS use PASS_IDENTITY_PRESERVE (zero healer mutation).

## Verified rescue cells (9)

| cell_id | rule_source | rules | pre → post |
|---|---|---|---|
| `qwen_4b__ce111_q02_polynomial_division_remainder__ab2d_domain_menu_v2__seed_2026072002` | PC_ONLY | PC-R01_ANSWER_SOURCE_REWIRE_V2 | answer_incorrect → passed |
| `qwen_4b__ce111_q02_polynomial_division_remainder__ab2d_domain_menu_v2__seed_2026072004` | TIER_AD_ONLY | TIER_D_RANKED_DOMAIN_METHOD_BINDING_V1 | answer_incorrect → passed |
| `qwen_4b__ce111_q02_polynomial_division_remainder__ab2d_full_v2__seed_2026071301` | PC_ONLY | PC-R01_ANSWER_SOURCE_REWIRE_V2 | answer_incorrect → passed |
| `qwen_4b__ce111_q02_polynomial_division_remainder__ab2d_full_v2__seed_2026072001` | PC_ONLY | PC-R01_ANSWER_SOURCE_REWIRE_V2 | answer_incorrect → passed |
| `qwen_4b__ce111_q08_polynomial_factor_parameter_recovery__ab2d_domain_menu_v2__seed_2026072001` | TIER_AD_ONLY | TIER_D_SYNTAX_RESIDUE_QUARANTINE_V1 | runtime_failure → passed |
| `qwen_4b__ce112_q04_radical_simplification__ab2d_full_v2__seed_2026072004` | PC_ONLY | PC-R03_DOMAIN_API_NORMALIZE_V2 | runtime_failure → passed |
| `qwen_4b__ce113_q01_negative_fraction_subtraction__ab2d_domain_menu_v2__seed_2026072003` | TIER_AD_ONLY | TIER_A_UNIQUE_IMPORT_BINDING_REPAIR_V1 | runtime_failure → passed |
| `qwen_4b__ce115_calc_exact_rational_expression_l1__ab2d_full_v2__seed_2026072003` | PC_ONLY | PC-R02_OPERAND_ORDER_RESTORE_V2 | structural_mismatch → passed |
| `qwen_4b__ce115_calc_exact_rational_expression_l1__ab2d_full_v2__seed_2026072004` | PC_ONLY | PC-R02_OPERAND_ORDER_RESTORE_V2 | structural_mismatch → passed |

## Modified still failed (count=19)

See gitignored `artifacts/math16_contract_aware_aggressive_healer_v2/integrated_28_evaluator_replay/cell_replay.json` for the full 28-row table.

## Evaluator

- `scripts.run_math16_latex_v1_gemini_live.classify_math16_response`
- same_as_v2_formal=true
- retries=0, llm_calls=0
- rules_modified=false, formal_artifacts_overwritten=false

## Pipeline

Aggressive Healer v2 integrated sequence:

`A→B→C1→C2→D3→D1→D5→D2 → AST_PARSE_GATE → API_CONTRACT_CHECKER → PC-R01→PC-R04 → CERT_VERIFY → STATIC_RECHECK`

No R05+ shipped (`NO_SHIPPABLE_R05_PLUS` after final repairability census).
