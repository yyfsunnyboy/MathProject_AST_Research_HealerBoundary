# 📑 CE115 Corrected Context Rerun Protocol Specification

This document defines the formal protocol for the corrected confirmatory run of the CE115 task suite. It addresses the 4096-token truncation issue identified in the initial runs by applying controlled context window boundaries.

---

## 1. Protocol Definition & Configuration Overrides

- **Original Run Designation**: `INITIAL_FORMAL_RUN_CONTEXT_UNCONTROLLED`
- **Corrected Run Designation**: `CORRECTED_FORMAL_RUN_CONTEXT_CONTROLLED`
- **Corrected Option Settings**:
  - `num_ctx = 65536`
  - `num_predict = 24576`
  - `think = false`
- **Invariants**:
  - All tasks, models, prompt conditions, seeds, prompts, temperature (0.0), and other sampling parameters remain strictly identical to the initial run.

---

## 2. Execution & Preservation Rules

1. **Isolation**:
   - The original 72-cell raw artifact files are preserved and never overwritten.
   - Corrected run output files will be written to a new isolated directory: `docs/experiments/results/ce115_calc_corrected_rerun/`.
2. **First-Attempt Only**:
   - Only the first attempt is recorded. No Healer class, automated repairs, or replays are run during this phase.
   - Retries on incomplete or failing outputs are strictly forbidden.

---

## 3. Limit-Termination and Degeneration Handling

If a cell hits the execution budget limit during generation, the following rules apply:

### CONFIGURATION_INVALID
- **Criteria**: The cell hits the context limit (`prompt_eval_count + eval_count == 65536`) or output limit (`eval_count == 24576`) without showing evidence of repetitive loop degeneration.
- **Handling**: The cell is classified as `CONFIGURATION_INVALID`. It is excluded from the failure taxonomy and is not counted as a model capability failure. The model limit must not be raised.

### MODEL_DEGENERATIVE_NONTERMINATION
- **Criteria**: The model enters a repetitive loop (duplicate line ratio > 40% or longest repeated contiguous block > 15 lines) and continues generating until it hits the limit.
- **Handling**: The cell is classified as `MODEL_DEGENERATIVE_NONTERMINATION`. It is counted as a model behavioral failure and entered into the failure taxonomy.

---

## 4. Post-Rerun Processing Pipeline

Once the corrected run completes for all 72 cells, the evaluation pipeline must be rerun from scratch:
1. Re-evaluate and rebuild the Output Size Census.
2. Reconstruct the Failure Taxonomy.
3. Re-examine Minimal Core applicability.
4. Re-examine Safe Historical applicability.
5. Re-evaluate replay and rescue eligibility.

> [!IMPORTANT]
> The initial counts (e.g., 63 failures, 18 parse_minor cells, 0 safe rules) must not be carried forward as final numbers. The corrected run results will form the new baseline for Healer applicability analysis.
