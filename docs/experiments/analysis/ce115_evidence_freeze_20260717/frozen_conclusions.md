# CE115 Evidence Freeze — Frozen Conclusions

**Freeze id:** `ce115_evidence_freeze_20260717`
**Status:** frozen for formal report drafting
**real_model_calls:** 0

## Mandatory separations

| Layer / track | Status | Scope |
|---|---|---|
| **L2** | Single formal **repair-to-pass** | Fixture `fail_radical_ab1_l2` / cell `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab1__seed_2026071301` only. Positioning: *frozen-oracle-assisted deterministic structural repair*. |
| **L1** | Exploratory only | `L1_COMMENT_ONLY_IF_INSERT_PASS` on `fail_exact_ab2d_l1`. **Not** production-approved. **Not** a formal success. |
| **L5 (q09)** | Equation-reconstruction failure | Primary `EQUATION_RECONSTRUCTION_WRONG`; secondary canonical `SPURIOUS_SHARED_BINOMIAL_SQUARE_TEMPLATE`. **Not Healer-repairable** in this freeze. |
| Cohorts A / B / C | Separate denominators | **Must not** be mixed into one success rate. |

## Cohort conclusions

### A — Core clean pilot
- Gemini: 9/9 PASSED (natural).
- Qwen: 2/9 PASSED; 7 natural failures forensically labelled.
- Healer was **not** applied inside the pilot run artifacts.

### B — Healer (Qwen core failures)
- Natural failures: 7.
- Production eligible: 1.
- Formal L2 triggered + repair-to-pass: **1**.
- Exploratory L1: **1** (parse probe only).
- Repair-to-next-layer: **0**.
- Regression no-op guards: **4** (false-positive: **0**).

### C — q09 diagnostic
- Formal q09: 6 cells; sign-pairing: 24 cells; total 30.
- Gemini L5 forensic (15 cells): dominant wrong shared-binomial square template; unrepairable by current Healer allowlist.
- Qwen q09/sign-pairing: status recorded; mechanism **NOT_VERIFIED** (Gemini-only forensic).

## q09 mechanism name freeze

- Primary: `EQUATION_RECONSTRUCTION_WRONG`
- Secondary canonical: `SPURIOUS_SHARED_BINOMIAL_SQUARE_TEMPLATE` (retires alias `SHARED_BINOMIAL_U_TEMPLATE`)
- Other confirmed secondaries: `SHIFT_PM_SUBTRACTED`, `PARAMS_COPIED_AS_ROOTS`, `SHIFT_AND_SHIFT_MINUS_SUB`, `SHIFT_AND_SHIFT_PLUS_SUB_NO_DIV`, `SHIFT_PM_SUB_OVER_LEADING`

## Report readiness

Evidence freeze is sufficient to begin formal report drafting **provided** claims stay within the publication-safe list and respect prohibited aggregations.
