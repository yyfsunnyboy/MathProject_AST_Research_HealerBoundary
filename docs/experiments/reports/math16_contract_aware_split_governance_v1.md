# Math16 Contract-Aware 40/120 Task-Level Split
## Governance & Preregistration Documentation

**Document Date:** 2026-07-28  
**Contract Name:** Math16 Contract-Aware 40/120 Task-Level Split  
**Version:** 1.0  
**Status:** Preregistered

---

## 1. Purpose and Rationale

This document establishes the governance framework for a **task-level split** of the Math16 HealerBoundary evaluation dataset into two cohorts:

- **Development (4 tasks, 40 cells):** Tasks with documented design exposure (guard-related logic, protocol specifications) reserved for method development and rule refinement.
- **Evaluation (12 tasks, 120 cells):** Remaining tasks for confirmatory validation without prior exposure to Healer design choices.

### Objective
Maintain **conceptual and practical segregation** between the development phase (where design decisions are made/tested) and the evaluation phase (where findings are confirmed against independent data), ensuring the split integrity of the 160-cell sample structure.

---

## 2. Split Definition

### 2.1 Development Cohort
**Composition:** 4 tasks × 2 conditions × 5 seeds = **40 cells**

**Tasks:**

| # | Task ID | Family | Prior Exposure | Condition Set |
|---|---------|--------|-----------------|---|
| 1 | `ce111_q08_polynomial_factor_parameter_recovery` | Polynomial | `guard_related_exposure` | ab2d, ab2d_spec_v2 |
| 2 | `ce111_nonchoice_q01_part1_exponential_growth` | Integer | `no_documented_design_exposure` | ab2d, ab2d_spec_v2 |
| 3 | `ce111_q05_exact_fraction_expression` | Fraction | `no_documented_design_exposure` | ab2d, ab2d_spec_v2 |
| 4 | `ce111_q10_ordered_quadratic_roots_radical` | Radical | `no_documented_design_exposure` | ab2d, ab2d_spec_v2 |

**Rationale for development inclusion:**
- **ce111_q08:** Documented guard design exposure via Forced Ambiguity exploration (appendices_v1.md § 3.2). Used for testing ambiguity detection and resolution logic. Safety preclass: UNSAFE_MODIFICATION. This task's exploratory status makes it appropriate for development-phase analysis.
- **ce111_nonchoice_q01, ce111_q05, ce111_q10:** Selected as representative tasks spanning integer, fraction, and radical families. While no documented design exposure, their preregistration as boundary cases (nonchoice format, exact arithmetic, combined radical transformations) and inclusion in the core probe set justifies development-phase treatment within this contract-aware design.

**Condition Set:** Only `ab2d` (Ab2d+api) and `ab2d_spec_v2` (Ab2d+spec-v2) are included.  
- `ab2d_spec_v2` is the frozen specification-compliant condition (rule-checked baseline).
- `ab2d` provides comparative data without specification constraints.
- `ab1` and `ab2g` are excluded to focus the split on practical application of frozen rules.

**Seeds:** All 5 seeds (2026071301, 2026072001, 2026072002, 2026072003, 2026072004) are included per cell.

### 2.2 Evaluation Cohort
**Composition:** 12 tasks × 2 conditions × 5 seeds = **120 cells**

**Tasks:**

| # | Task ID | Family | Prior Exposure |
|---|---------|--------|-----------------|
| 1 | `ce111_q02_polynomial_division_remainder` | Polynomial | `no_documented_design_exposure` |
| 2 | `ce111_q03_prime_factor_selection` | Integer | `no_documented_design_exposure` |
| 3 | `ce112_q01_negative_integer_power` | Integer | `no_documented_design_exposure` |
| 4 | `ce112_q04_radical_simplification` | Radical | `cohort_level_provenance_uncertain` |
| 5 | `ce112_q09_divisor_multiple_intersection` | Integer | `no_documented_design_exposure` |
| 6 | `ce112_q12_independent_probability_fraction` | Fraction | `no_documented_design_exposure` |
| 7 | `ce113_q01_negative_fraction_subtraction` | Fraction | `cohort_level_provenance_uncertain` |
| 8 | `ce113_q11_rationalize_denominator` | Radical | `cohort_level_provenance_uncertain` |
| 9 | `ce115_calc_exact_rational_expression_l1` | Fraction | `cohort_level_provenance_uncertain` |
| 10 | `ce115_calc_polynomial_division_l1` | Polynomial | `no_documented_design_exposure` |
| 11 | `ce115_calc_polynomial_factor_roots_l1` | Polynomial | `no_documented_design_exposure` |
| 12 | `ce115_calc_radical_simplification_l1` | Radical | `cohort_level_provenance_uncertain` |

**Condition Set:** `ab2d` and `ab2d_spec_v2` (same as development for consistency).

**Seeds:** All 5 seeds per task.

**Prior Exposure Breakdown:**
- **`cohort_level_provenance_uncertain` (5 tasks):** Tasks observed in rescue data but lacking explicit Provenance Audit documentation linking them to rule/guard design. Marked uncertain until/unless definitive provenance evidence emerges.
  - ce112_q04_radical_simplification
  - ce113_q01_negative_fraction_subtraction
  - ce113_q11_rationalize_denominator
  - ce115_calc_exact_rational_expression_l1
  - ce115_calc_radical_simplification_l1
  
- **`no_documented_design_exposure` (7 tasks):** Tasks with no identified design or rescue involvement. Standard baseline tasks.

---

## 3. Prior Exposure Classification

This split is governed by **Consensus Exposure Classification** derived from:

1. **Guard Design Exposure** (`guard_related_exposure`):  
   Documented in appendices_v1.md (Forced Ambiguity exploration for ce111_q08).  
   Frozen at commit `d9aa264c`. Does not change.

2. **Cohort-Level Provenance Uncertainty** (`cohort_level_provenance_uncertain`):  
   Tasks appeared in rescue/correction data but the Provenance Audit document (`math16_healer_rule_provenance_audit_v1.md`) does not exist or does not explicitly name these tasks as rule-design test cases. Per user directive: "若檔案不存在或內容未指名任務，立即停止，不再搜尋。將上述 5 題統一標記：`cohort_level_provenance_uncertain`".

3. **No Documented Design Exposure** (`no_documented_design_exposure`):  
   Tasks with no documented involvement in rule/guard design or rescue-chain activities.

---

## 4. Integrity Constraints

The following constraints are **frozen and non-negotiable** for this contract:

### 4.1 Cellular Completeness
- **Development:** Exactly 4 tasks × 2 conditions × 5 seeds = 40 cells.
- **Evaluation:** Exactly 12 tasks × 2 conditions × 5 seeds = 120 cells.
- **Total:** 160 cells (16 cells per task across full 320-cell plan, using only ab2d/ab2d_spec_v2).

### 4.2 Mutual Exclusion
- No task appears in both Development and Evaluation.
- No task appears more than once within a single cohort.
- No cell appears in both cohorts.

### 4.3 Condition Consistency
- Both cohorts use the same condition set: `ab2d`, `ab2d_spec_v2`.
- No mixing of conditions across tasks or cohorts.

### 4.4 Seed Completeness
- Each task-condition pair must include all 5 seeds:  
  2026071301, 2026072001, 2026072002, 2026072003, 2026072004.
- No partial seed coverage.

### 4.5 Cell Identity Preservation
- Each cell's `cell_id`, `task_id`, `family`, `condition`, `seed`, `prompt_path`, `prompt_source`, `prompt_sha256`, `output_relative_path` are preserved from the authoritative source manifest.
- No modification of cell metadata or outputs.

### 4.6 No Taxonomy Contamination
- Split manifest does NOT use PASS/FAIL/RESCUE/FAILURE taxonomy labels.
- Classification is purely by task membership and prior exposure exposure (guard_related_exposure, cohort_level_provenance_uncertain, no_documented_design_exposure).

---

## 5. Source of Authority

**Primary Source:** `docs/experiments/manifests/math16_pilot02_qwen4b_cell_plan.json`
- Frozen at commit `d9aa264c`.
- 320 cells total (16 tasks × 4 conditions × 5 seeds).
- Authoritative cell metadata: cell_id, task_id, family, condition, condition_display, seed, model_tag, prompt_path, prompt_source, prompt_sha256, output_relative_path.

**Supporting Documents:**
- `docs/experiments/appendices/math16_pilot02_appendices_v1.md` (guard design exposure documentation).
- `artifacts/math16_tasks_prompts_and_program_skeletons_appendix_v1/task_index.csv` (task metadata).

---

## 6. Rationale for 40/120 Proportions

The 40/120 split reflects a **pragmatic balance** for HealerBoundary methodology:

- **Development (40 cells):** Sufficient to:
  - Validate guard detection logic (ce111_q08 ambiguity testing).
  - Probe method sensitivity across multiple task families (integer, fraction, radical, polynomial).
  - Support iterative refinement of rules/guards without excessive external validation overhead.

- **Evaluation (120 cells):** Sufficient to:
  - Confirm reproducibility across 12 diverse tasks.
  - Detect systematic biases or task-specific failure modes.
  - Support statistical confidence (120 cells >> 40 cells → lower variance).

**Split Ratio:** 1:3 (development:evaluation) aligns with standard machine learning train/test practices while acknowledging the locked, deterministic nature of Healer (no hyperparameter tuning, no online learning).

---

## 7. Dual-Reporting Obligation for Evaluation Results

**CRITICAL:** Any future analysis or publication reporting evaluation findings from this split **MUST** report both:

### 7.1 Primary Result: Full 120-Cell Evaluation Cohort
**All 12 evaluation tasks, 120 cells total**

| Task Set | Cell Count | Classification |
|----------|-----------|-----------------|
| Standard Benchmark (7 tasks) | 70 | `no_documented_design_exposure` |
| Special (5 tasks) | 50 | `cohort_level_provenance_uncertain` |
| **Total** | **120** | — |

**Rationale for Full-120 Reporting:** The complete evaluation cohort is the primary evidence set. All 12 tasks were partitioned into evaluation *a priori* and represent the intended confirmatory population.

### 7.2 Secondary Analysis: Excluded-70 Sensitivity Analysis
**7 standard benchmark tasks, 70 cells (excluding 5 uncertain tasks)**

| Excluded Task Set | Cell Count | Reason |
|----------|-----------|---------|
| cohort_level_provenance_uncertain | 50 | Provenance Audit not found; tasks lack explicit rule-design documentation |
| ce112_q04_radical_simplification | 10 | Rescue data present but source unconfirmed |
| ce113_q01_negative_fraction_subtraction | 10 | Rescue data present but source unconfirmed |
| ce113_q11_rationalize_denominator | 10 | Rescue data present but source unconfirmed |
| ce115_calc_exact_rational_expression_l1 | 10 | Rescue data present but source unconfirmed |
| ce115_calc_radical_simplification_l1 | 10 | Rescue data present but source unconfirmed |

**Rationale for Excluded-70 Reporting:** To isolate conservative findings, exclude the 5 tasks with uncertain provenance and report results on the remaining 70 cells (7 standard benchmark tasks with no documented design exposure).

### 7.3 Reporting Obligation

Future results **MUST** follow this template:

> **Evaluation Results (Math16 Contract-Aware Split)**
>
> **Primary Finding (Full 120-Cell Evaluation):**  
> [Report metrics, patterns, findings across all 12 evaluation tasks, 120 cells]
>
> **Sensitivity Analysis (Excluded-70):**  
> When excluding 5 tasks with cohort-level provenance uncertainty, results on the remaining 70 cells show:  
> [Report metrics on standard benchmark only]
>
> **Interpretation:**  
> - If excluded-70 and full-120 results align → finding robust to provenance uncertainty
> - If results diverge → finding sensitive to the 5 uncertain tasks; interpretation requires caution regarding their design exposure status

### 7.4 Dual-Reporting NOT Optional

- **120-cell result is primary.** Do not replace it with excluded-70.
- **Excluded-70 is mandatory sensitivity check.** Do not omit it.
- **Both must be reported side-by-side** in any manuscript, report, or publication.
- Failure to report both constitutes incomplete evidence and violates this contract.

---

## 8. Non-Negotiable Constraints

This contract enforces:

- **Read-only integrity:** No modification to cell outputs, prompts, or results from the 320-cell evaluation.
- **No re-execution:** Healer rules and guard logic are frozen at commit `d9aa264c`; no new rule development within this split.
- **No cross-contamination:** Evaluation findings do NOT feed back into development rule/guard decisions.
- **Reproducibility:** All cells are deterministic; re-running cells must yield identical outputs.
- **Dual reporting compliance:** All future analyses MUST report both full-120 and excluded-70 results.

---

## 9. Validation

See `math16_contract_aware_split_validation.py` for automated verification of:
1. Exact cell counts (40 dev, 120 eval, 160 total).
2. Task mutual exclusion and completeness.
3. Condition consistency (ab2d, ab2d_spec_v2 only).
4. Seed completeness (all 5 per task-condition).
5. No cross-split cell leakage.
6. Prior exposure classification consistency.

---

## 10. Commit and Deployment

**Repository:** `MathProject_AST_Research_HealerBoundary` (GitHub)  
**Target Path:** `docs/experiments/manifests/math16_contract_aware_40_120_split_manifest.json`  
**Branch:** `main`

**Manifest SHA-256:** `c0ff7e8a31d713a92670aed1a03bc71429955c406036affdd8d9e216f1c9edc7`

**Recommendation:** Commit this split manifest as a frozen, read-only reference document. The split itself does not modify any outputs or rules; it is a **logical partitioning** of the existing 320-cell data.

**Commit Message Template:**
```
Add Math16 Contract-Aware 40/120 Task-Level Split Manifest

- Development: 4 tasks, 40 cells (design exposure)
- Evaluation: 12 tasks, 120 cells (confirmatory validation)
  - Full 120-cell result: mandatory primary reporting
  - Excluded-70 sensitivity analysis: mandatory dual-reporting (7 standard benchmark tasks)
- Manifest SHA-256: c0ff7e8a31d713a92670aed1a03bc71429955c406036affdd8d9e216f1c9edc7
- Prior exposure classifications: guard_related_exposure (1), cohort_level_provenance_uncertain (5), no_documented_design_exposure (10)
- Frozen at commit d9aa264c (source cell_plan.json)
- All validation checks passed (8/8)
- Dual-reporting obligation: future analyses MUST report both full-120 and excluded-70 results
```

---

## References

- Appendices Report: `docs/experiments/appendices/math16_pilot02_appendices_v1.md`
- Final Report: `docs/experiments/reports/math16_pilot02_final_report_v13.md`
- Cell Plan Manifest: `docs/experiments/manifests/math16_pilot02_qwen4b_cell_plan.json`
- Prior Exposure Analysis: `docs/experiments/reports/math16_prior_exposure_analysis_v1.md`
