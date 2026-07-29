# Math16 C2→C3 Tier C1 Residual Supply Census v1

> **Verdict / Go-NoGo:** `NO_GO_TIER_C1`
> **HEAD:** `f0eae63fe8c3760e9912589654657510119175ce`
> **rule_id:** `TIER_B_EXPLICIT_DOMAIN_METHOD_BINDING_REPAIR_V1`（current_tier = Tier C1）
> **spec:** `docs/experiments/design/math16_aggressive_healer_domain_api_binding_spec_v1.md`

## 1. Scope

Static eligibility census for Tier C1 Explicit Domain Method Binding Repair on the
**C2 residual** pool only（4B Pilot-02 cells still FAIL after C0→C1→C2）.
Input = **C2 post-source** only. No mutation, no evaluator, no Tier C2 adjudication,
no Aggressive Healer v2.

## 2. Residual pool construction

| Layer | PASS | still FAIL |
|---|---:|---:|
| C0 baseline | 79 | 241 |
| C1 Tier A | 85 | 235 |
| C2 Tier B (empty-suite n=5 replay) | 86 | **234** |

- Actual residual pool: **234**
- Duplicate / missing: **0** / **0**
- C2 source policy: Tier B post-source if modified-still-fail; else unchanged C1 final_source
- Raw source used: **No**

## 3. Status tallies

| Status | Count |
|---|---:|
| C1_ELIGIBLE | 0 |
| C1_AMBIGUOUS_ABSTAIN | 4 |
| C1_INELIGIBLE | 219 |
| SYSTEM_CONTRACT_EXCLUDED | 11 |
| OVERLAP_UNRESOLVED | 0 |

- Unique marginal supply: **0**
- Defect／unresolved excluded: **11**

## 4. Eligible distribution

- By model: `{"qwen4b": 0}`
- By condition: `{}`
- By task: `{}`
- Concentrated single cell: **False**
- Concentrated single task: **False**

### Status by condition

- `ab1`: `{"C1_INELIGIBLE": 64}`
- `ab2d`: `{"C1_INELIGIBLE": 68, "C1_AMBIGUOUS_ABSTAIN": 1}`
- `ab2d_spec_v2`: `{"C1_INELIGIBLE": 28, "C1_AMBIGUOUS_ABSTAIN": 3, "SYSTEM_CONTRACT_EXCLUDED": 11}`
- `ab2g`: `{"C1_INELIGIBLE": 59}`

## 5. Primary abstention／exclusion reasons

| Reason | Count |
|---|---:|
| `condition_has_no_domain_api_contract` | 123 |
| `candidate_not_parseable` | 39 |
| `domain_calls_already_match_exposed_methods` | 30 |
| `no_domain_api_call_present` | 16 |
| `ops_class_shadowing` | 7 |
| `SYSTEM_CONTRACT_DEFECT` | 7 |
| `no_ssot_unique_exposed_method` | 4 |
| `wrong_method_but_expected_not_unique` | 4 |
| `UNRESOLVED` | 4 |

## 6. Go／No-Go

- Decision: **NO_GO_TIER_C1**
- Rationale: Tier C1 marginal supply is zero on C2 residual pool.
- Guards were **not** relaxed due to small n.

## 7. Declarations

- Mutation executed: **No**
- Candidate／evaluator executed: **No**
- Tier C2 processed: **No**
- Aggressive Healer v2 created: **No**
- Post-source artifacts produced: **No**
- Commit／push: **No**
