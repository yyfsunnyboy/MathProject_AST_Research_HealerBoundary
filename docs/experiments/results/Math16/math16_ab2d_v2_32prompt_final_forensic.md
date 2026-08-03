# Math16 Ab2d V2 — 32-prompt final forensic review

## Verdict

**PASS** for the frozen prompt/API/scaffold artifact under review. The artifact is cleared for the remaining Qwen 9B and Gemini qualification cells. It is **not yet cleared for a formal 480-cell rerun** because those two qualification cells remain unexecuted.

Review scope was exactly 16 `ab2d_domain_menu_v2` prompts, 16 `ab2d_full_v2` prompts, four Domain API classes, and all 33 `SUPPORTED_PUBLIC` methods. No formal 480-cell run, Healer run, V1 edit, commit, or push was performed.

## Final counts

| Check | Result |
|---|---:|
| API missing/mismatch | 0 |
| domain-menu prompt defects | 0 |
| domain-menu solution-leakage findings | 0 |
| full-plan prompt defects | 0 |
| fairness violations | 0 |
| hardcoded-answer / answer-lookup findings | 0 |
| unresolved artifact defects | 0 |

## Domain API forensic result

The public inventory is complete: IntegerOps 7, FractionOps 8, RadicalOps 9, PolynomialOps 9; total 33. All 33 have the required import, signature, ordered parameters, input constraints, model-facing return type, return shape/field semantics, JSON boundary, normalization responsibility, and executable example. Inventory missing/stale entries, missing contract fields, rendered-card mismatches, and example execution failures are all zero.

The SSOT was compared with the actual callables in `core.prompts.domain_function_library`: callable names and positional/default parameter order agree for all 33 methods, and all 33 have implementation docstrings. `IntegerOps.safe_eval` has a runtime return annotation (`-> int | float`) in addition to the documented call signature `(expr)`; this is not a parameter/signature mismatch and agrees with the documented return type. Return shapes and JSON adapters used by the scaffolds agree with implementation behavior.

Classification: **PASS**. `API_DOCUMENTATION_DEFECT=0`; `API_SEMANTICS_DEFECT=0`.

## Prompt review

All 16 domain-menu prompts state and demonstrate the zero-argument `generate()` runtime contract, embed the task's frozen literals, preserve the exact answer contract and `oracle_payload`, and do not depend on values arriving through kwargs. No prompt selects an API, fixes an API call order, supplies task solution steps, hints answer assembly, exposes a computed answer, or contains a task-id answer branch/lookup.

All 16 full-plan prompts use an API appropriate to the task. Parameter binding/order, return names and destructuring, intermediate operations, JSON-safe conversion, `correct_answer` shape, and `oracle_payload` were checked against the SSOT, implementation, task contract, and evaluator. No extra/missing scored computation, literal ground-truth substitution, answer lookup, or task-id branch was found.

Per-prompt classification: all 16 domain-menu and all 16 full-plan prompts are **PASS**. `PROMPT_DEFECT_FOUND=0`; `SOLUTION_LEAKAGE=0`; `HARDCODED_ANSWER=0`; `UNRESOLVED=0` for artifact review.

## Fairness

For each of 16 task pairs, the shared portion is byte-identical. The only pairwise difference is the allowed full-plan task-specific scaffold. Answer contract, `frozen_params`, zero-argument runtime contract, and Domain API menu are identical. All 16 answer contracts also remain byte-identical to their V1 source blocks; V1 was not modified.

Classification: **PASS**. `FAIRNESS_VIOLATION=0`.

## Executable verification

- Prompt files found: 32/32.
- Python code fences parsed with `ast.parse`: 80/80; failures 0.
- Full-plan task scaffolds executed directly: 16/16.
- Execution failures: 0.
- Exact three-key schema failures: 0.
- `oracle_payload != frozen_params`: 0.
- Real evaluator answer mismatches: 0.
- Targeted test: `tests/test_math16_ab2d_spec_v2.py`: 6 passed.

| task_id | exec | schema | oracle_payload | real evaluator |
|---|---|---|---|---|
| ce115_calc_polynomial_division_l1 | PASS | PASS | PASS | PASS |
| ce115_calc_polynomial_factor_roots_l1 | PASS | PASS | PASS | PASS |
| ce115_calc_exact_rational_expression_l1 | PASS | PASS | PASS | PASS |
| ce115_calc_radical_simplification_l1 | PASS | PASS | PASS | PASS |
| ce111_q02_polynomial_division_remainder | PASS | PASS | PASS | PASS |
| ce111_q08_polynomial_factor_parameter_recovery | PASS | PASS | PASS | PASS |
| ce111_q03_prime_factor_selection | PASS | PASS | PASS | PASS |
| ce112_q01_negative_integer_power | PASS | PASS | PASS | PASS |
| ce112_q09_divisor_multiple_intersection | PASS | PASS | PASS | PASS |
| ce111_nonchoice_q01_part1_exponential_growth | PASS | PASS | PASS | PASS |
| ce111_q05_exact_fraction_expression | PASS | PASS | PASS | PASS |
| ce113_q01_negative_fraction_subtraction | PASS | PASS | PASS | PASS |
| ce112_q12_independent_probability_fraction | PASS | PASS | PASS | PASS |
| ce112_q04_radical_simplification | PASS | PASS | PASS | PASS |
| ce111_q10_ordered_quadratic_roots_radical | PASS | PASS | PASS | PASS |
| ce113_q11_rationalize_denominator | PASS | PASS | PASS | PASS |

## Qualification gate and evidence gap

Qwen 9B and Gemini qualification is allowed. Existing Qwen 4B qualification executed 6 cells: 4 passed and 2 domain-menu cells failed because generated model code selected/used an API incorrectly; neither failure reproduces the prior kwargs runtime-contract defect, and neither is evidence of a frozen-prompt/API/scaffold defect.

The remaining evidence gap is external/model qualification: one Qwen 9B cell is `PENDING_9B_CAPACITY` and one Gemini cell is `PENDING_API_KEY`. Consequently, the prompt package may proceed to those qualifications, but a formal 480-cell rerun is not authorized by this review until the preregistered 9B/Gemini qualification gate is executed and accepted.

No commit or push was performed.
