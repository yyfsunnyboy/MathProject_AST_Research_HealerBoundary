# Math16 C2→C4 Tier C2 Residual Supply Census v1

> **Verdict / Go-NoGo:** `EXPLORATORY_ONLY`
> **HEAD:** `f0eae63fe8c3760e9912589654657510119175ce`
> **rule_id:** `TIER_B_DOMAIN_SIGNATURE_FORM_REPAIR_V1`（current_tier = Tier C2）
> **spec:** `docs/experiments/design/math16_aggressive_healer_domain_api_binding_spec_v1.md`

## 1. Scope

Static eligibility census for Tier C2 Domain Signature Form Repair on the
**C2 residual** pool（4B Pilot-02 still FAIL after C0→C1→C2）.
Input = **C2 final post-source** only. No mutation, no evaluator, no other rules,
no Aggressive Healer v2. Tier C1 census is **linked, not re-run**.

## 2. Link to Tier C1（NO_GO）

- Tier C1 manifest: `docs/experiments/manifests/math16_c2_c3_tier_c1_residual_supply_v1.json`
- Tier C1 verdict: **NO_GO_TIER_C1**
- Tier C1 eligible / marginal supply: **0**
- This round does **not** re-adjudicate Tier C1.

## 3. Residual pool construction

| Layer | PASS | still FAIL |
|---|---:|---:|
| C0 | 79 | 241 |
| C1 Tier A | 85 | 235 |
| C2 Tier B | 86 | **234** |

- Actual residual pool: **234**
- Tier B modified-but-still-failed SHA checks: **4／4**
- Raw／C1-pre-Tier-B source used: **No**

## 4. Status tallies

| Status | Count |
|---|---:|
| C2_ELIGIBLE | 5 |
| C2_AMBIGUOUS_ABSTAIN | 0 |
| C2_INELIGIBLE | 218 |
| SYSTEM_CONTRACT_EXCLUDED | 11 |
| OVERLAP_UNRESOLVED | 0 |

- Unique marginal supply: **5**
- Defect／unresolved excluded: **11**

## 5. Eligible distribution

- By model: `{"qwen4b": 5}`
- By condition: `{"ab2d": 1, "ab2d_spec_v2": 4}`
- By task: `{"ce111_q02_polynomial_division_remainder": 5}`
- Repair subtypes: `{"default_optional_pure_form_cleanup": 5}`
- Concentrated single cell／task: **False**／**True**

### Status by condition

- `ab1`: `{"C2_INELIGIBLE": 64}`
- `ab2d`: `{"C2_INELIGIBLE": 68, "C2_ELIGIBLE": 1}`
- `ab2d_spec_v2`: `{"C2_ELIGIBLE": 4, "C2_INELIGIBLE": 27, "SYSTEM_CONTRACT_EXCLUDED": 11}`
- `ab2g`: `{"C2_INELIGIBLE": 59}`

## 6. Primary exclusion／abstention reasons

| Reason | Count |
|---|---:|
| `condition_has_no_domain_api_contract` | 123 |
| `candidate_not_parseable` | 39 |
| `no_allowed_signature_form_defect` | 29 |
| `no_domain_api_call_present` | 16 |
| `ops_class_shadowing` | 7 |
| `SYSTEM_CONTRACT_DEFECT` | 7 |
| `eligible` | 5 |
| `no_ssot_unique_exposed_method` | 4 |
| `UNRESOLVED` | 4 |

## 7. Go／No-Go

- Decision: **EXPLORATORY_ONLY**
- Rationale: Non-zero supply (n=5) but concentrated on single task ce111_q02_polynomial_division_remainder.
- Guards were **not** relaxed due to small n.

## 8. Combined Tier C1＋C2 conclusion

Tier C1 = NO_GO_TIER_C1 (eligible=0). Tier C2 = EXPLORATORY_ONLY (eligible=5, tasks={'ce111_q02_polynomial_division_remainder': 5}, subtypes={'default_optional_pure_form_cleanup': 5}). Method-binding repair has no residual supply; signature-form supply exists only as single-task exploratory evidence (not cross-task GO). No GO_TIER_C* implementation path; do not name Aggressive Healer v2; do not relax guards.

## 9. Declarations

- Mutation executed: **No**
- Candidate／evaluator executed: **No**
- Other rules processed: **No**
- Aggressive Healer v2 created: **No**
- Post-source artifacts produced: **No**
- Commit／push: **No**

## 10. Eligible cell list

- `qwen3_5_4b__ce111_q02_polynomial_division_remainder__ab2d__seed_2026072003`: PolynomialOps.format_latex default_optional_pure_form_cleanup @ L18
- `qwen3_5_4b__ce111_q02_polynomial_division_remainder__ab2d_spec_v2__seed_2026071301`: PolynomialOps.format_latex default_optional_pure_form_cleanup @ L16
- `qwen3_5_4b__ce111_q02_polynomial_division_remainder__ab2d_spec_v2__seed_2026072001`: PolynomialOps.format_latex default_optional_pure_form_cleanup @ L16
- `qwen3_5_4b__ce111_q02_polynomial_division_remainder__ab2d_spec_v2__seed_2026072002`: PolynomialOps.format_latex default_optional_pure_form_cleanup @ L19
- `qwen3_5_4b__ce111_q02_polynomial_division_remainder__ab2d_spec_v2__seed_2026072003`: PolynomialOps.format_latex default_optional_pure_form_cleanup @ L16
