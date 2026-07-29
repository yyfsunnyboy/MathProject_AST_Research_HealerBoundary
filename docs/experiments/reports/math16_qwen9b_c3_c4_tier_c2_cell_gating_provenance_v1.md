# Math16 Qwen9B C3→C4 Tier C2 Cell-Gating Provenance v1

> **AUTHORITY:** NONAUTHORITATIVE_ALL_CELL_EXPLORATORY — exploratory all-cell; not FAIL-only authoritative.
> **Authoritative namespace:** qwen9b_fail_gated_authoritative_v1


> **Verdict:** `ALL_CELL_SCAN_NO_FAIL_GATE`／`DIFFERENT_SCOPE_BUT_VALID`
> **HEAD:** `72117d3facd48b8e78af534290dc7dcd2001149a`
> **rule_id:** `TIER_B_DOMAIN_SIGNATURE_FORM_REPAIR_V1`（current_tier = Tier C2）
> **subtype:** `default_optional_pure_form_cleanup` only

## Purpose

Close provenance for the **4 PASS→PASS** modified cells observed in 9B C3→C4 Tier C2,
and reconcile 4B vs 9B census scope without re-running the evaluator or changing transition tallies.

## Classification

| Code | Meaning | Applies? |
|---|---|---|
| **A. ALL_CELL_SCAN_NO_FAIL_GATE** | Candidate pool = full C3 final 320; eligibility is contract／AST only; PASS/FAIL not used for trigger | **Yes** |
| B. FAIL_GATE_IMPLEMENTATION_BUG | Intended FAIL-only gate but PASS cells leaked into mutation | No |
| C. MISCLASSIFIED_RESCUE | PASS→PASS wrongly booked as rescue／gain | No |
| D. OTHER | — | No |

**Direct cause of the 4 PASS→PASS cells:** the 9B runner scanned **all 320 C3 final sources** with the same frozen signature-form pipeline; `adjudicate_c2` is answer-blind (`pass_fail_used_for_eligibility: false`). Those 4 cells already PASSED at C3 but still carried a unique redundant optional default keyword (`var='x'` or `mixed=False`), so they were `C2_ELIGIBLE`, mutated, and remained PASSED (`preserved_pass`).

They are **not** in any FAIL-only residual pool; they arise only because the candidate pool is all-cell.

## Four PASS→PASS cells

| cell_id | C3 | C4 | C3 SHA-256 | C4 SHA-256 | eligibility | triggered／modified | in FAIL-only residual? |
|---|---|---|---|---|---|---|---|
| `…ce111_q02…ab2d_spec_v2…2026072001` | PASSED | PASSED | `8b67a9de…57d967` | `d3f804d9…045cc` | C2_ELIGIBLE | true／true | **No** |
| `…ce113_q01…ab2d…2026072001` | PASSED | PASSED | `9fda1a85…8dd6b1` | `84e5568f…8b10a` | C2_ELIGIBLE | true／true | **No** |
| `…ce111_q02…ab2d_spec_v2…2026072003` | PASSED | PASSED | `be74a1a5…ca331a` | `87bb880c…9bf782` | C2_ELIGIBLE | true／true | **No** |
| `…ce113_q01…ab2d…2026072003` | PASSED | PASSED | `a219ea70…62cf7f` | `4ca256ab…b75de` | C2_ELIGIBLE | true／true | **No** |

Repair sites (unchanged argument values; keyword removal only):

- 2× `PolynomialOps.format_latex(..., var='x')` → drop `var`
- 2× `FractionOps.to_latex(..., mixed=False)` → drop `mixed`

All four: `transition=preserved_pass`, `source_origin=TIER_C2_POST_SOURCE`, SHA changed, status unchanged PASSED→PASSED.

## Candidate-pool generation (9B)

- **Input:** `math16_c3_final_source_closure_qwen9b_v1` — all **320** identities
- **Runner:** `scripts/run_math16_c3_c4_tier_c2_qwen9b_v1.py`
- **Gate:** contract matrix + frozen `apply_once`／`run_tier_c2_default_optional_cleanup`
- **Fail-gate:** **none** (consistent with user brief: full-320 same pipeline; PASS cells checked for preserved pass／regression)
- **Evaluator role:** scoring only after selection; not used for trigger／eligibility

## 4B／9B scope comparison

| Axis | 4B Tier C2 | 9B Tier C2 |
|---|---|---|
| Census scope | **Residual FAIL-only** C2 still-FAIL **234** | **All-cell** C3 final **320** |
| Eligible denominator | 234 residual FAIL | 320 all-cell |
| Modified denominator | Development replay on residual eligible **5** | All-cell eligible／modified **10** |
| PASS→PASS included? | **No** (pool excludes PASS by construction) | **Yes** (4 of 10) |
| verified_rescue | FAIL→PASS only; 4B=0 | same definition; 9B=0 |
| regression | PASS→FAIL; 4B=0 | same; 9B=0 |
| Lineage | C2→C4 residual／`TIER_C2_POST_SOURCE` on 5 FAIL | C3→C4／`TIER_C2_POST_SOURCE` on 10 (6 FAIL + 4 PASS) |
| Rule package | same frozen narrow subtype | same package SHA |

**Scope judgment:** `DIFFERENT_SCOPE_BUT_VALID`

- Not `SAME_SCOPE` (234 FAIL-only ≠ 320 all-cell).
- Not `IMPLEMENTATION_INCONSISTENCY`／not a gating bug: 9B cumulative layers C0–C4 were explicitly all-cell; 4B Tier C2 residual census was a FAIL-only supply study. Definitions of rescue／regression match; PASS→PASS is booked as `preserved_pass`, not rescue.

## Unified accounting (9B; transition stats unchanged)

| Ledger | n |
|---|---:|
| all-cell eligible | **10** |
| all-cell modified | **10** |
| original PASS eligible (PASS→PASS) | **4** |
| residual-FAIL eligible (C3 FAIL∧eligible) | **6** |
| modified-still-failed | **6** |
| verified rescue | **0** |
| regression | **0** |
| preserved pass | **102** |

Identity check: **10 = 4 PASS→PASS + 6 FAIL→FAIL**.

## Re-run decision

**Do not re-run C3→C4.** Provenance is closed; counts are internally consistent; no B／C defect.

## Declarations

- Rule implementation not modified
- C3／C4 sources not modified
- Evaluator not re-run
- Tier D not executed
- No model calls
- No commit／push
- This note only documents gating／scope; it does not alter transition tallies
