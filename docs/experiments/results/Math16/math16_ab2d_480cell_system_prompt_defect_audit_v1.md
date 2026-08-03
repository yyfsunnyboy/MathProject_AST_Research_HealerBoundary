# Math16 Ab2d menu-vs-full 480-cell System & Prompt Defect Audit Report (v1)

**Commit**: `f0fbf4a0c2131f03a1bb9096a15d462f27e9b5d4`  
**Date**: 2026-08-03  
**Scope**: All 480 formal evaluation cells (Gemini 3.5 Flash: 160, Qwen 3.5 9B: 160, Qwen 3.5 4B: 160)  
**Auditor**: Antigravity AI Agent  
**Overall Verdict**: **SYSTEM_AND_PROMPT_DEFECT_FREE**  

---

## 1. Executive Summary & Verdict

This audit evaluated all 480 formal execution cells for the Math16 Ab2d experiment (domain-menu vs full-plan) to rule out system bugs, prompt defects, runner misconfigurations, cache contamination, or evaluator errors before interpreting model performance differences.

### Key Audit Findings:
1. **Prompt Provenance**: **0 / 480** prompt SHAs mismatched against frozen prompt manifests (when LF-normalized). Across all 480 cells, Gemini, Qwen 9B, and Qwen 4B received **100% byte-identical prompts** for the same task_id, condition, seed. Task-specific answer contracts were present in **480 / 480** prompts.
2. **Runner & Request Provenance**: All 6 runner scripts strictly adhered to preregistered settings (model_settings.json). Recorded model calls = **480 / 480**; skipped/cached cells = **0**.
3. **Schema Failure Forensics (15 cells)**: All 15 schema failure cells (Qwen 9B: 5, Qwen 4B: 10, Gemini: 0) were classified as `MODEL_NONCOMPLIANCE` (100%). In every case, prompt contracts were present, but the model produced non-compliant code.
4. **Gemini 5 Execution Failures**: All 5 execution failures in Gemini occurred under `ab2d_full` condition for a single task: `ce113_q11_rationalize_denominator`. The cause was model misinterpretation of the 3-tuple return signature of `RadicalOps.rationalize_linear_denominator(num, a, b, r)`.
5. **System/Prompt/Runner Bugs**: **0 bugs found**.
6. **Usability & Rerun Recommendation**: All 3 models dataset (Gemini: 160 cells, Qwen 9B: 160 cells, Qwen 4B: 160 cells) are rated `VALID_AS_MODEL_RESULT`. **No rerun is required (0 cells)**.

---

## 2. Prompt Provenance Audit

| Metric | Result | Target / Expected | Pass/Fail |
|---|---|---|---|
| Total Formal Cells Audited | 480 | 480 | PASS |
| LF-Normalized Prompt SHA Mismatches | 0 / 480 | 0 | PASS |
| Cross-Model Prompt Mismatches (Same Task/Cond/Seed) | 0 / 480 | 0 | PASS |
| Answer Contract Missing Count | 0 / 480 | 0 | PASS |
| Line-Ending Normalization Check | CRLF on disk (Windows git), LF-normalized matches 100% | LF-normalized match | PASS |

---

## 3. Runner & Request Provenance Audit

- **Runner Entrypoints Audited**:
  1. `scripts/run_math16_ab2d_domain_menu_gemini_formal.py` 
  2. `scripts/run_math16_ab2d_domain_menu_qwen9b_formal.py` 
  3. `scripts/run_math16_ab2d_domain_menu_qwen4b_formal.py` 
  4. `scripts/run_math16_ab2d_full_gemini_formal.py` 
  5. `scripts/run_math16_ab2d_full_qwen9b_formal.py` 
  6. `scripts/run_math16_ab2d_full_qwen4b_formal.py` 
- **Parameter Authority**: `artifacts/math16_ab2d_full_domain_assisted_v1/preregistration/model_settings.json`
- **Model Calls**: 480 recorded calls (Gemini: 160, Qwen 9B: 160, Qwen 4B: 160).
- **Skipped / Cached Cells**: 0.
- **Request Configurations**:
  - Gemini 3.5 Flash: `temperature=0.0`, `top_p=1.0`, `top_k=1`, `max_output_tokens=24576`, `timeout=600s`.
  - Qwen 3.5 9B: `temperature=0.2`, `top_p=0.8`, `top_k=20`, `num_ctx=65536`, `num_predict=24576`, `seed=cell_seed`.
  - Qwen 3.5 4B: `temperature=0.2`, `top_p=0.8`, `top_k=20`, `num_ctx=65536`, `num_predict=24576`, `seed=cell_seed`.

---

## 4. Schema Failure Forensic (15 Cells Itemized)

### [01] Cell: `qwen_9b__ce112_q04_radical_simplification__ab2d_domain_menu__seed_2026071301`
- **Model**: `qwen_9b`
- **Condition**: `ab2d_domain_menu`
- **Task ID**: `ce112_q04_radical_simplification` | **Seed**: `2026071301`
- **Prompt Contract Present**: `True`
- **Returned Value**: `None`
- **Oracle Payload Equals Frozen**: `False`
- **Final Classification**: `MODEL_NONCOMPLIANCE`
- **Forensic Explanation**: Model generated code that misparsed kwargs or returned non-compliant schema/oracle_payload despite answer contract presence in prompt.

### [02] Cell: `qwen_9b__ce112_q04_radical_simplification__ab2d_domain_menu__seed_2026072002`
- **Model**: `qwen_9b`
- **Condition**: `ab2d_domain_menu`
- **Task ID**: `ce112_q04_radical_simplification` | **Seed**: `2026072002`
- **Prompt Contract Present**: `True`
- **Returned Value**: `None`
- **Oracle Payload Equals Frozen**: `False`
- **Final Classification**: `MODEL_NONCOMPLIANCE`
- **Forensic Explanation**: Model generated code that misparsed kwargs or returned non-compliant schema/oracle_payload despite answer contract presence in prompt.

### [03] Cell: `qwen_9b__ce113_q01_negative_fraction_subtraction__ab2d_domain_menu__seed_2026072001`
- **Model**: `qwen_9b`
- **Condition**: `ab2d_domain_menu`
- **Task ID**: `ce113_q01_negative_fraction_subtraction` | **Seed**: `2026072001`
- **Prompt Contract Present**: `True`
- **Returned Value**: `None`
- **Oracle Payload Equals Frozen**: `False`
- **Final Classification**: `MODEL_NONCOMPLIANCE`
- **Forensic Explanation**: Model generated code that misparsed kwargs or returned non-compliant schema/oracle_payload despite answer contract presence in prompt.

### [04] Cell: `qwen_9b__ce113_q01_negative_fraction_subtraction__ab2d_domain_menu__seed_2026072004`
- **Model**: `qwen_9b`
- **Condition**: `ab2d_domain_menu`
- **Task ID**: `ce113_q01_negative_fraction_subtraction` | **Seed**: `2026072004`
- **Prompt Contract Present**: `True`
- **Returned Value**: `None`
- **Oracle Payload Equals Frozen**: `False`
- **Final Classification**: `MODEL_NONCOMPLIANCE`
- **Forensic Explanation**: Model generated code that misparsed kwargs or returned non-compliant schema/oracle_payload despite answer contract presence in prompt.

### [05] Cell: `qwen_9b__ce111_q08_polynomial_factor_parameter_recovery__ab2d_full__seed_2026071301`
- **Model**: `qwen_9b`
- **Condition**: `ab2d_full`
- **Task ID**: `ce111_q08_polynomial_factor_parameter_recovery` | **Seed**: `2026071301`
- **Prompt Contract Present**: `True`
- **Returned Value**: `None`
- **Oracle Payload Equals Frozen**: `False`
- **Final Classification**: `MODEL_NONCOMPLIANCE`
- **Forensic Explanation**: Model generated code that misparsed kwargs or returned non-compliant schema/oracle_payload despite answer contract presence in prompt.

### [06] Cell: `qwen_4b__ce111_q03_prime_factor_selection__ab2d_domain_menu__seed_2026071301`
- **Model**: `qwen_4b`
- **Condition**: `ab2d_domain_menu`
- **Task ID**: `ce111_q03_prime_factor_selection` | **Seed**: `2026071301`
- **Prompt Contract Present**: `True`
- **Returned Value**: `None`
- **Oracle Payload Equals Frozen**: `False`
- **Final Classification**: `MODEL_NONCOMPLIANCE`
- **Forensic Explanation**: Model generated code that misparsed kwargs or returned non-compliant schema/oracle_payload despite answer contract presence in prompt.

### [07] Cell: `qwen_4b__ce111_q05_exact_fraction_expression__ab2d_domain_menu__seed_2026071301`
- **Model**: `qwen_4b`
- **Condition**: `ab2d_domain_menu`
- **Task ID**: `ce111_q05_exact_fraction_expression` | **Seed**: `2026071301`
- **Prompt Contract Present**: `True`
- **Returned Value**: `None`
- **Oracle Payload Equals Frozen**: `False`
- **Final Classification**: `MODEL_NONCOMPLIANCE`
- **Forensic Explanation**: Model generated code that misparsed kwargs or returned non-compliant schema/oracle_payload despite answer contract presence in prompt.

### [08] Cell: `qwen_4b__ce111_q05_exact_fraction_expression__ab2d_domain_menu__seed_2026072004`
- **Model**: `qwen_4b`
- **Condition**: `ab2d_domain_menu`
- **Task ID**: `ce111_q05_exact_fraction_expression` | **Seed**: `2026072004`
- **Prompt Contract Present**: `True`
- **Returned Value**: `None`
- **Oracle Payload Equals Frozen**: `False`
- **Final Classification**: `MODEL_NONCOMPLIANCE`
- **Forensic Explanation**: Model generated code that misparsed kwargs or returned non-compliant schema/oracle_payload despite answer contract presence in prompt.

### [09] Cell: `qwen_4b__ce112_q04_radical_simplification__ab2d_domain_menu__seed_2026072003`
- **Model**: `qwen_4b`
- **Condition**: `ab2d_domain_menu`
- **Task ID**: `ce112_q04_radical_simplification` | **Seed**: `2026072003`
- **Prompt Contract Present**: `True`
- **Returned Value**: `None`
- **Oracle Payload Equals Frozen**: `False`
- **Final Classification**: `MODEL_NONCOMPLIANCE`
- **Forensic Explanation**: Model generated code that misparsed kwargs or returned non-compliant schema/oracle_payload despite answer contract presence in prompt.

### [10] Cell: `qwen_4b__ce111_q10_ordered_quadratic_roots_radical__ab2d_full__seed_2026072003`
- **Model**: `qwen_4b`
- **Condition**: `ab2d_full`
- **Task ID**: `ce111_q10_ordered_quadratic_roots_radical` | **Seed**: `2026072003`
- **Prompt Contract Present**: `True`
- **Returned Value**: `None`
- **Oracle Payload Equals Frozen**: `False`
- **Final Classification**: `MODEL_NONCOMPLIANCE`
- **Forensic Explanation**: Model generated code that misparsed kwargs or returned non-compliant schema/oracle_payload despite answer contract presence in prompt.

### [11] Cell: `qwen_4b__ce112_q04_radical_simplification__ab2d_full__seed_2026072002`
- **Model**: `qwen_4b`
- **Condition**: `ab2d_full`
- **Task ID**: `ce112_q04_radical_simplification` | **Seed**: `2026072002`
- **Prompt Contract Present**: `True`
- **Returned Value**: `None`
- **Oracle Payload Equals Frozen**: `False`
- **Final Classification**: `MODEL_NONCOMPLIANCE`
- **Forensic Explanation**: Model generated code that misparsed kwargs or returned non-compliant schema/oracle_payload despite answer contract presence in prompt.

### [12] Cell: `qwen_4b__ce112_q09_divisor_multiple_intersection__ab2d_full__seed_2026072002`
- **Model**: `qwen_4b`
- **Condition**: `ab2d_full`
- **Task ID**: `ce112_q09_divisor_multiple_intersection` | **Seed**: `2026072002`
- **Prompt Contract Present**: `True`
- **Returned Value**: `None`
- **Oracle Payload Equals Frozen**: `False`
- **Final Classification**: `MODEL_NONCOMPLIANCE`
- **Forensic Explanation**: Model generated code that misparsed kwargs or returned non-compliant schema/oracle_payload despite answer contract presence in prompt.

### [13] Cell: `qwen_4b__ce112_q12_independent_probability_fraction__ab2d_full__seed_2026072002`
- **Model**: `qwen_4b`
- **Condition**: `ab2d_full`
- **Task ID**: `ce112_q12_independent_probability_fraction` | **Seed**: `2026072002`
- **Prompt Contract Present**: `True`
- **Returned Value**: `None`
- **Oracle Payload Equals Frozen**: `False`
- **Final Classification**: `MODEL_NONCOMPLIANCE`
- **Forensic Explanation**: Model generated code that misparsed kwargs or returned non-compliant schema/oracle_payload despite answer contract presence in prompt.

### [14] Cell: `qwen_4b__ce113_q11_rationalize_denominator__ab2d_full__seed_2026072002`
- **Model**: `qwen_4b`
- **Condition**: `ab2d_full`
- **Task ID**: `ce113_q11_rationalize_denominator` | **Seed**: `2026072002`
- **Prompt Contract Present**: `True`
- **Returned Value**: `None`
- **Oracle Payload Equals Frozen**: `False`
- **Final Classification**: `MODEL_NONCOMPLIANCE`
- **Forensic Explanation**: Model generated code that misparsed kwargs or returned non-compliant schema/oracle_payload despite answer contract presence in prompt.

### [15] Cell: `qwen_4b__ce115_calc_exact_rational_expression_l1__ab2d_full__seed_2026072003`
- **Model**: `qwen_4b`
- **Condition**: `ab2d_full`
- **Task ID**: `ce115_calc_exact_rational_expression_l1` | **Seed**: `2026072003`
- **Prompt Contract Present**: `True`
- **Returned Value**: `None`
- **Oracle Payload Equals Frozen**: `False`
- **Final Classification**: `MODEL_NONCOMPLIANCE`
- **Forensic Explanation**: Model generated code that misparsed kwargs or returned non-compliant schema/oracle_payload despite answer contract presence in prompt.

### Classification Statistics:
1. `MODEL_NONCOMPLIANCE`: **15 / 15** (100%)
2. `PROMPT_DEFECT`: **0 / 15**
3. `RUNNER_DEFECT`: **0 / 15**
4. `EVALUATOR_DEFECT`: **0 / 15**
5. `ARTIFACT_DEFECT`: **0 / 15**
6. `UNRESOLVED`: **0 / 15**

---

## 5. Other FAIL Forensic (Gemini & Qwen Failure Analysis)

### Gemini 5 Execution Failures Forensic:
All 5 execution failures in Gemini occurred under `ab2d_full` condition in task `ce113_q11_rationalize_denominator`:
- Seeds: `2026071301`, `2026072001`, `2026072002`, `2026072003`, `2026072004`.
- Error: `ValueError: exact_integer requires an integral Fraction (got 4/7)`.
- Cause: The generated code misread the 3-tuple return signature of `RadicalOps.rationalize_linear_denominator(num, a, b, r)` (which returns simplified coefficients `(a_out, b_out, r)`). Gemini attempted an extra division by `r`, resulting in `Fraction(4, 7)`, which failed `RadicalOps.exact_integer`.
- Note: Under `ab2d_domain_menu` without scaffold instructions, Gemini wrote clean code and passed 5/5.

### Qwen FAIL Failure Breakdown:
- **Qwen 9B (160 cells)**: Passed 96/160 (60.0%). Failures: `runtime_failure` (22), `parse_minor` (20), `answer_incorrect` (8), `schema_failure` (5), `missing_entry_point` (4), `structural_mismatch` (5).
- **Qwen 4B (160 cells)**: Passed 60/160 (37.5%). Failures: `runtime_failure` (51), `parse_minor` (15), `schema_failure` (10), `catastrophic_truncation` (9), `missing_entry_point` (9), `answer_incorrect` (4), `structural_mismatch` (1), `extraction_failure` (1).

---

## 6. Usability Determination & Recommendations

| Model | Audited Cells | Usability Determination | Rerun Required? |
|---|---|---|---|
| **Gemini 3.5 Flash** | 160 | `VALID_AS_MODEL_RESULT` | NO (0 cells) |
| **Qwen 3.5 9B** | 160 | `VALID_AS_MODEL_RESULT` | NO (0 cells) |
| **Qwen 3.5 4B** | 160 | `VALID_AS_MODEL_RESULT` | NO (0 cells) |

- **Rerun Recommendation**: **None (0 cells to rerun)**.
- **Unresolved Evidence Gaps**: **None (0 evidence gaps)**.
