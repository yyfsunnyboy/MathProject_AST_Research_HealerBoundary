# Math16 C4→C5 Tier D Supply Census v1

> **Verdict:** `TIER_D_SUPPLY_CENSUS_COMPLETE`
> **HEAD:** `f0eae63fe8c3760e9912589654657510119175ce`
> **input:** C4 still-FAIL 234／C4 final post-source（not pure C2）

## 1. Scope

Read-only static eligibility census for six Tier D placeholder rules on the
**C4 final-source closure** residual pool. No mutation, no evaluator, no model,
no Tier D implementation.

## 2. Aggregate

- Residual pool: **234**
- Unique eligible cells (ELIGIBLE∪RANKED_ELIGIBLE): **13**
- Multi-rule overlap cells: **1**
- Supply intersecting Tier C2 post-source cells: **0**

### Eligible by rule (ELIGIBLE + RANKED_ELIGIBLE)

| Rule | Count |
|---|---:|
| `TIER_D_OPS_SHADOW_REMOVAL_V1` | 4 |
| `TIER_D_DUPLICATE_DEFINITION_SELECTION_V1` | 1 |
| `TIER_D_SYNTAX_RESIDUE_QUARANTINE_V1` | 5 |
| `TIER_D_UNIQUE_NATIVE_TO_DOMAIN_API_REWRITE_V1` | 0 |
| `TIER_D_RANKED_DOMAIN_METHOD_BINDING_V1` | 4 |
| `TIER_D_FIXED_TEMPLATE_LOCAL_BODY_REPAIR_V1` | 0 |

### Status by rule

- `TIER_D_OPS_SHADOW_REMOVAL_V1`: `{"INELIGIBLE": 227, "ELIGIBLE": 4, "AMBIGUOUS_ABSTAIN": 3}`
- `TIER_D_DUPLICATE_DEFINITION_SELECTION_V1`: `{"INELIGIBLE": 232, "RANKED_ELIGIBLE": 1, "AMBIGUOUS_ABSTAIN": 1}`
- `TIER_D_SYNTAX_RESIDUE_QUARANTINE_V1`: `{"INELIGIBLE": 226, "ELIGIBLE": 5, "AMBIGUOUS_ABSTAIN": 3}`
- `TIER_D_UNIQUE_NATIVE_TO_DOMAIN_API_REWRITE_V1`: `{"INELIGIBLE": 234}`
- `TIER_D_RANKED_DOMAIN_METHOD_BINDING_V1`: `{"INELIGIBLE": 230, "RANKED_ELIGIBLE": 4}`
- `TIER_D_FIXED_TEMPLATE_LOCAL_BODY_REPAIR_V1`: `{"INELIGIBLE": 234}`

## 3. Priority

- Top rules: `["TIER_D_SYNTAX_RESIDUE_QUARANTINE_V1", "TIER_D_OPS_SHADOW_REMOVAL_V1"]`
- Rationale: Prefer non-zero supply rules with clearer mechanical gates; top by eligible+ranked counts: [('TIER_D_SYNTAX_RESIDUE_QUARANTINE_V1', 5), ('TIER_D_OPS_SHADOW_REMOVAL_V1', 4), ('TIER_D_RANKED_DOMAIN_METHOD_BINDING_V1', 4)]

## 4. Primary reasons (top 30)

| Reason | Count |
|---|---:|
| `TIER_D_DUPLICATE_DEFINITION_SELECTION_V1::no_duplicate_definitions` | 160 |
| `TIER_D_FIXED_TEMPLATE_LOCAL_BODY_REPAIR_V1::body_not_template_precondition` | 159 |
| `TIER_D_OPS_SHADOW_REMOVAL_V1::no_ops_shadow` | 155 |
| `TIER_D_SYNTAX_RESIDUE_QUARANTINE_V1::no_trailing_residue` | 151 |
| `TIER_D_UNIQUE_NATIVE_TO_DOMAIN_API_REWRITE_V1::condition_has_no_domain_api_contract` | 94 |
| `TIER_D_RANKED_DOMAIN_METHOD_BINDING_V1::condition_has_no_domain_api_contract` | 94 |
| `TIER_D_OPS_SHADOW_REMOVAL_V1::candidate_not_parseable` | 72 |
| `TIER_D_DUPLICATE_DEFINITION_SELECTION_V1::candidate_not_parseable` | 72 |
| `TIER_D_SYNTAX_RESIDUE_QUARANTINE_V1::candidate_not_parseable` | 72 |
| `TIER_D_UNIQUE_NATIVE_TO_DOMAIN_API_REWRITE_V1::candidate_not_parseable` | 72 |
| `TIER_D_RANKED_DOMAIN_METHOD_BINDING_V1::candidate_not_parseable` | 72 |
| `TIER_D_FIXED_TEMPLATE_LOCAL_BODY_REPAIR_V1::candidate_not_parseable` | 72 |
| `TIER_D_UNIQUE_NATIVE_TO_DOMAIN_API_REWRITE_V1::native_pattern_registry_not_frozen` | 61 |
| `TIER_D_RANKED_DOMAIN_METHOD_BINDING_V1::no_ranked_wrong_method_site` | 57 |
| `TIER_D_SYNTAX_RESIDUE_QUARANTINE_V1::parseable_trailing_non_def_residue` | 5 |
| `TIER_D_OPS_SHADOW_REMOVAL_V1::unique_ops_shadow` | 4 |
| `TIER_D_RANKED_DOMAIN_METHOD_BINDING_V1::unique_wrong_method_site_with_ge2_candidates` | 4 |
| `TIER_D_UNIQUE_NATIVE_TO_DOMAIN_API_REWRITE_V1::system_contract_SYSTEM_CONTRACT_DEFECT` | 4 |
| `TIER_D_RANKED_DOMAIN_METHOD_BINDING_V1::system_contract_SYSTEM_CONTRACT_DEFECT` | 4 |
| `TIER_D_SYNTAX_RESIDUE_QUARANTINE_V1::no_unique_generate_or_end_lineno` | 3 |
| `TIER_D_FIXED_TEMPLATE_LOCAL_BODY_REPAIR_V1::no_unique_generate` | 3 |
| `TIER_D_SYNTAX_RESIDUE_QUARANTINE_V1::trailing_contains_definitions` | 3 |
| `TIER_D_OPS_SHADOW_REMOVAL_V1::multiple_ops_shadows` | 3 |
| `TIER_D_UNIQUE_NATIVE_TO_DOMAIN_API_REWRITE_V1::system_contract_UNRESOLVED` | 3 |
| `TIER_D_RANKED_DOMAIN_METHOD_BINDING_V1::system_contract_UNRESOLVED` | 3 |
| `TIER_D_DUPLICATE_DEFINITION_SELECTION_V1::exactly_one_name_with_two_defs_needs_ranking` | 1 |
| `TIER_D_DUPLICATE_DEFINITION_SELECTION_V1::multiple_duplicate_groups_or_gt2` | 1 |

## 5. By condition (cell primary)

- `ab1`: `{"INELIGIBLE": 63, "ELIGIBLE": 1}`
- `ab2d`: `{"INELIGIBLE": 57, "MULTI_RULE_OVERLAP": 1, "ELIGIBLE": 6, "RANKED_ELIGIBLE": 2, "AMBIGUOUS_ABSTAIN": 3}`
- `ab2d_spec_v2`: `{"INELIGIBLE": 37, "RANKED_ELIGIBLE": 3, "AMBIGUOUS_ABSTAIN": 2}`
- `ab2g`: `{"INELIGIBLE": 58, "AMBIGUOUS_ABSTAIN": 1}`

## 6. Declarations

- Used C4 final source only: **Yes**
- Pure C2 as Tier D input: **No**
- Tier D implemented: **No**
- Mutation／evaluator／model: **No**
