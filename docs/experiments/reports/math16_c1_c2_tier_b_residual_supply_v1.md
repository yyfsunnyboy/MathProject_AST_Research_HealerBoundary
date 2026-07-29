# Math16 C1→C2 Tier B Residual Supply Census v1

> **status:** `c1_c2_tier_b_residual_supply_v1`
> **HEAD:** `f0eae63fe8c3760e9912589654657510119175ce`
> **layering_protocol:** `docs/experiments/design/math16_cumulative_healer_layering_protocol_v1.md`
> **rule_id_tier_mapping:** `docs/experiments/manifests/math16_healer_rule_id_tier_mapping_v1.json`

## 1. Scope

Static eligibility census for Tier B four structural rules on the **C1 residual**
pool only（4B Pilot-02 cells that remain FAIL after Tier A / Method2 C1）.
Input = **Tier A post-source**（`final_sources`）, **not** raw source.
No Tier B mutation, no evaluator, no Tier C.

## 2. Residual pool

- Expected still_failed: **235**
- Actual residual pool: **235**
- Duplicate cell_ids: **0**
- Missing vs 235: **0**
- Raw source used: **False**

## 3. Tier B eligible counts

| Rule ID | Eligible (incl. overlap slots) |
|---|---:|
| `core.normalize_fullwidth_python_punctuation` | 0 |
| `TIER_A_UNIQUE_MISSING_DELIMITER_REPAIR_V1` | 0 |
| `TIER_A_EMPTY_SUITE_INSERT_PASS_V1` | 5 |
| `TIER_A_UNIQUE_IMPORT_BINDING_REPAIR_V1` | 0 |

- Unique eligible cells (marginal supply): **5**
- Unique non-overlap eligible: **5**
- Multi-rule overlap cells: **0**
- Total eligible rule-slots: **5**

## 4. Status tallies by rule

### ALREADY_CORRECT

| Rule | Count |
|---|---:|
| `core.normalize_fullwidth_python_punctuation` | 158 |
| `TIER_A_UNIQUE_MISSING_DELIMITER_REPAIR_V1` | 158 |
| `TIER_A_EMPTY_SUITE_INSERT_PASS_V1` | 158 |
| `TIER_A_UNIQUE_IMPORT_BINDING_REPAIR_V1` | 136 |

### AMBIGUOUS_ABSTAIN

| Rule | Count |
|---|---:|
| `core.normalize_fullwidth_python_punctuation` | 0 |
| `TIER_A_UNIQUE_MISSING_DELIMITER_REPAIR_V1` | 0 |
| `TIER_A_EMPTY_SUITE_INSERT_PASS_V1` | 0 |
| `TIER_A_UNIQUE_IMPORT_BINDING_REPAIR_V1` | 0 |

### INELIGIBLE

| Rule | Count |
|---|---:|
| `core.normalize_fullwidth_python_punctuation` | 77 |
| `TIER_A_UNIQUE_MISSING_DELIMITER_REPAIR_V1` | 77 |
| `TIER_A_EMPTY_SUITE_INSERT_PASS_V1` | 72 |
| `TIER_A_UNIQUE_IMPORT_BINDING_REPAIR_V1` | 99 |

## 5. Primary abstention reasons (top 20)

| Reason key | Count |
|---|---:|
| `core.normalize_fullwidth_python_punctuation::no_unprotected_mapped_or_fail_closed` | 235 |
| `TIER_A_UNIQUE_MISSING_DELIMITER_REPAIR_V1::source_already_parses` | 158 |
| `TIER_A_EMPTY_SUITE_INSERT_PASS_V1::source_already_parses` | 158 |
| `TIER_A_UNIQUE_IMPORT_BINDING_REPAIR_V1::no_unique_stdlib_binding_gap` | 136 |
| `TIER_A_UNIQUE_IMPORT_BINDING_REPAIR_V1::source_not_parseable` | 77 |
| `TIER_A_EMPTY_SUITE_INSERT_PASS_V1::no_empty_suite_site` | 72 |
| `TIER_A_UNIQUE_MISSING_DELIMITER_REPAIR_V1::syntax_error_not_delimiter` | 55 |
| `TIER_A_UNIQUE_MISSING_DELIMITER_REPAIR_V1::no_unique_closing_insert` | 22 |
| `TIER_A_UNIQUE_IMPORT_BINDING_REPAIR_V1::missing_names_not_uniquely_mappable` | 12 |
| `TIER_A_UNIQUE_IMPORT_BINDING_REPAIR_V1::ops_class_shadowing` | 7 |
| `TIER_A_UNIQUE_IMPORT_BINDING_REPAIR_V1::domain_ops_or_excluded_binding` | 3 |

## 6. Comparison vs raw 960 census

- Raw 960 unique eligible: **9**
- Raw qwen4b eligible-by-rule: `{"core.normalize_fullwidth_python_punctuation": 0, "TIER_A_UNIQUE_MISSING_DELIMITER_REPAIR_V1": 0, "TIER_A_EMPTY_SUITE_INSERT_PASS_V1": 5, "TIER_A_UNIQUE_IMPORT_BINDING_REPAIR_V1": 0}`
- Residual 235 unique eligible: **5**
- Residual eligible-by-rule: `{"core.normalize_fullwidth_python_punctuation": 0, "TIER_A_UNIQUE_MISSING_DELIMITER_REPAIR_V1": 0, "TIER_A_EMPTY_SUITE_INSERT_PASS_V1": 5, "TIER_A_UNIQUE_IMPORT_BINDING_REPAIR_V1": 0}`
- Note: Residual census uses C1 Tier A post-source on still_failed only; raw 960 census used C0 raw on all cells including PASS.

## 7. Development replay gate

- Tier B true marginal supply: **5**
- Can enter C1→C2 Development replay: **True**
- Rationale: Non-zero residual unique eligible cells on C1 post-source still_failed pool constitutes Tier B marginal supply for a C1→C2 Development replay; Validation/Confirmatory split still undefined.

## 8. Declarations

- Model calls: **0**
- Tier B mutation applied: **No**
- Evaluator executed for census: **No**
- Tier C processed: **No**
- Commit / push: **No**
