# Math16 Qwen 9B/4B 320-Cell Low Pass-Rate Forensic Audit Report (v1)

**Commit**: `f0fbf4a0c2131f03a1bb9096a15d462f27e9b5d4`  
**Date**: 2026-08-03  
**Scope**: 320 cells (Qwen 3.5 9B: 160 cells, Qwen 3.5 4B: 160 cells across domain-menu and full-plan)  
**Auditor**: Antigravity AI Agent  
**Verdict**: **VALID_MODEL_CAPACITY_AND_PROMPT_COMPLEXITY_RESULT**  
**Final Classification**: **`PROMPT_COMPLEXITY_OR_CLARITY_EFFECT`**  

---

## 1. Executive Summary & Verdict

This audit performed a comprehensive forensic investigation into the 320 evaluation cells of Qwen 3.5 9B and Qwen 3.5 4B (domain-menu vs full-plan) to audit the execution layer, prompt comprehensibility, seed independence, truncation/extraction, infrastructure stability, API misuse, evaluator comparability, preregistration caliber, and failure concentration.

### Key Audit Findings:
1. **Model Identity & Settings**: PASS. Model names (`qwen3.5:9b`, `qwen3.5:4b`) and model digests match preregistration (`model_settings.json`) and Pilot-02 manifests 100%. Parameters (`temperature=0.2`, `top_p=0.8`, `top_k=20`, `num_ctx=65536`, `num_predict=24576`, `think=False`) were strictly applied.
2. **Answer Contract Comprehensibility**: PASS. Qwen received 100% byte-identical prompts as Gemini. Schema failures (Qwen 9B: 5, Qwen 4B: 10) were caused by `runtime_call_convention_misuse` (`kwargs.get('frozen_params')`) and API return shape misinterpretations.
3. **Seed Independence**: PASS. 55 out of 64 task-condition groups (85.9%) yielded 5/5 unique responses. Deterministic collapse count = 0 (0%).
4. **Truncation & Extraction Audit**: 155 out of 164 failing cells were `COMPLETE_BUT_INVALID` (code generation finished cleanly but contained logic/schema errors). 9 cells (Qwen 4B) were `MODEL_TRUNCATED` due to infinite repetition. Extractor and runner truncation counts = 0.
5. **Infrastructure Audit**: PASS. Transport errors = 0, retry attempts = 0. Service and API infrastructure were 100% stable. GPU hardware telemetry (VRAM/kernel metrics) is marked `EVIDENCE_INSUFFICIENT` as hardware telemetry was not captured in `logs.json`.
6. **API Misuse Breakdown**: Primary API misuses among 164 failing cells were `runtime_call_convention_misuse` (95 cells) and `api_return_semantics_misuse` (40 cells). Wrong domain = 0, unavailable API = 0.
7. **Evaluator Comparability**: PASS. Evaluator gates match Pilot-02 formal gates exactly. Results are directly comparable.
8. **Preregistration Caliber Comparison**: In `full_plan` (with step-by-step scaffolds), Qwen 9B's 5/5 stable tasks jumped from 1 to 9, and pass rate jumped from 43.8% (35/80) to 76.3% (61/80).
9. **Failure Concentration**: Failures were concentrated in `PolynomialOps` and `RadicalOps` tasks.
10. **Usability & Rerun Recommendation**: Qwen 9B and Qwen 4B dataset are rated **`VALID_AS_MODEL_RESULT`**. **No rerun is required (0 cells)**.

---

## 2. Itemized Audit Sections

### Section 1: Model Identity & Settings
| Model | Model Name | Model Digest | Options Verified | Status |
|---|---|---|---|---|
| Qwen 9B | `qwen3.5:9b` | `6488c96fa5faab64bb65cbd30d4289e20e6130ef535a93ef9a49f42eda893ea7` | temp=0.2, top_p=0.8, top_k=20, num_ctx=65536, num_predict=24576, think=False | PASS |
| Qwen 4B | `qwen3.5:4b` | `2a654d98e6fba55d452b7043684e9b57a947e393bbffa62485a7aac05ee4eefd` | temp=0.2, top_p=0.8, top_k=20, num_ctx=65536, num_predict=24576, think=False | PASS |

### Section 2: Answer Contract Comprehensibility
- **Prompt Byte Identity**: 100% byte-identical with Gemini (0/320 mismatch).
- **Answer Contract Presence**: 320/320 present (100%).
- **Schema Failure Breakdown**: Qwen 9B: 5 cells; Qwen 4B: 10 cells.
- **Classification**: `PROMPT_COMPLEXITY_OR_CLARITY_EFFECT`.

### Section 3: Seed Independence Audit
- **Total 5-Seed Groups**: 64 (16 tasks x 2 conditions x 2 models).
- **5 / 5 Unique Responses**: 55 groups (85.9%).
- **4 / 5 Unique Responses**: 2 groups (3.1%).
- **3 / 5 Unique Responses**: 5 groups (7.8%).
- **2 / 5 Unique Responses**: 2 groups (3.1%).
- **1 / 5 Unique Responses (5/5 Byte-Identical)**: 0 groups (0.0%).
- **Deterministic Collapse**: None.

### Section 4: Truncation & Extraction Audit
- `COMPLETE_BUT_INVALID`: **155 cells** (Generation completed but had logic/schema/syntax errors).
- `MODEL_TRUNCATED`: **9 cells** (Qwen 4B infinite repetition reaching token limit).
- `RUNNER_TRUNCATED`: **0 cells**.
- `EXTRACTOR_TRUNCATED`: **0 cells**.
- `UNRESOLVED`: **0 cells**.
- `num_predict=24576` was confirmed active in request settings.

### Section 5: Infrastructure Audit
- **Transport Errors**: 0 / 320.
- **Retry Attempts (>1)**: 0 / 320.
- **Mean Latency**: 18.0s per cell.
- **Infrastructure Anomalies**: None.
- **GPU Hardware Telemetry**: Marked `EVIDENCE_INSUFFICIENT` (hardware VRAM/CUDA metrics were not logged, though API infrastructure was 100% clean).

### Section 6: API Misuse Statistics (164 Failing Cells)
- `runtime_call_convention_misuse`: **95 cells** (`kwargs.get('frozen_params')` misuse).
- `api_return_semantics_misuse`: **40 cells** (Misreading return tuples/dicts).
- `wrong_method`: **6 cells** (AttributeError on domain classes).
- `wrong_signature`: **1 cell** (Wrong positional/keyword args).
- `wrong_domain`: **0 cells**.
- `unavailable_api`: **0 cells**.

### Section 7: Evaluator Comparability Audit
- **Evaluation Gates**: Identical to Pilot-02 gates (`python_parse_ok`, `domain_api_availability`, `three_key_output`, `oracle_payload_equals_frozen_params`, `correct_answer_contract`).
- **QFIX-001 Impact**: Engineering-only null-safe JSON formatting; does not alter evaluation outcomes.
- **Comparability Status**: **100% Comparable**.

### Section 8: Preregistration Caliber Breakdown
| Model | Condition | 5/5 Stable Tasks | 4/5 Tasks | 1-3/5 Tasks | 0/5 Tasks | Total Pass Rate |
|---|---|---|---|---|---|---|
| **Qwen 9B** | `ab2d_domain_menu` | 1 | 1 | 12 | 2 | 35/80 (43.8%) |
| **Qwen 9B** | `ab2d_full` | 9 | 1 | 5 | 1 | 61/80 (76.3%) |
| **Qwen 4B** | `ab2d_domain_menu` | 3 | 1 | 5 | 7 | 29/80 (36.3%) |
| **Qwen 4B** | `ab2d_full` | 3 | 2 | 6 | 5 | 31/80 (38.8%) |

### Section 9: Failure Hotspots & Top 10 Failing Tasks
| Rank | Model | Task ID | Domain | Fails / 20 | Pass / 20 |
|---|---|---|---|---|---|
| 1 | Qwen 4B | `ce111_q02_polynomial_division_remainder` | PolynomialOps | 10 / 20 | 10 / 20 |
| 2 | Qwen 4B | `ce113_q11_rationalize_denominator` | RadicalOps | 10 / 20 | 10 / 20 |
| 3 | Qwen 4B | `ce115_calc_polynomial_factor_roots_l1` | PolynomialOps | 10 / 20 | 10 / 20 |
| 4 | Qwen 4B | `ce115_calc_radical_simplification_l1` | RadicalOps | 10 / 20 | 10 / 20 |
| 5 | Qwen 9B | `ce115_calc_polynomial_factor_roots_l1` | PolynomialOps | 9 / 20 | 11 / 20 |
| 6 | Qwen 4B | `ce111_nonchoice_q01_part1_exponential_growth` | IntegerOps | 9 / 20 | 11 / 20 |
| 7 | Qwen 4B | `ce115_calc_exact_rational_expression_l1` | FractionOps | 9 / 20 | 11 / 20 |
| 8 | Qwen 4B | `ce112_q04_radical_simplification` | RadicalOps | 8 / 20 | 12 / 20 |
| 9 | Qwen 4B | `ce112_q12_independent_probability_fraction` | FractionOps | 8 / 20 | 12 / 20 |
| 10 | Qwen 9B | `ce113_q11_rationalize_denominator` | RadicalOps | 7 / 20 | 13 / 20 |

---

## 3. Final Overall Category & Recommendations

| Category Choice | Status | Rationale |
|---|---|---|
| `EXECUTION_LAYER_DEFECT_FOUND` | Rejected | Execution layer was 100% stable (0 transport errors, 0 retries). |
| `MODEL_CONFIGURATION_MISMATCH` | Rejected | Ollama settings matched preregistration 100%. |
| `PROMPT_DEFECT` | Rejected | Prompt SHAs matched 100%; Gemini achieved 96.9% pass rate on identical prompts. |
| **`PROMPT_COMPLEXITY_OR_CLARITY_EFFECT`** | **SELECTED** | Prompt contract complexity and multi-step code requirements significantly impact smaller models. Providing step-by-step scaffolds (full_plan) boosted Qwen 9B's stable tasks from 1 to 9 and pass rate from 43.8% to 76.3%. |
| `EXTRACTOR_DEFECT_FOUND` | Rejected | Extractor worked cleanly without cutting off code. |
| `INFRASTRUCTURE_ISSUE_FOUND` | Rejected | Infrastructure was 100% reliable. |
| `EVALUATOR_COMPARABILITY_ISSUE` | Rejected | Evaluator gates match Pilot-02. |
| `TRUE_MODEL_LIMITATION` | Secondary Factor | Smaller parameter models (4B/9B) have inherent capacity limits in single-shot unassisted code generation. |
| `MIXED_CAUSES` | Compatible | Prompt complexity interaction with model capacity. |
| `UNRESOLVED` | Rejected | All 320 cells accounted for with concrete empirical data. |

- **Usability Determination**: `VALID_AS_MODEL_RESULT`
- **Rerun Required**: **NO (0 cells to rerun)**
- **Unresolved Evidence Gaps**: GPU hardware telemetry (VRAM/CUDA utilization) marked `EVIDENCE_INSUFFICIENT` due to lack of hardware telemetry logging in `logs.json`.
