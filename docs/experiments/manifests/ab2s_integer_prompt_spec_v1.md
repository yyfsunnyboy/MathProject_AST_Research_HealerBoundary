# Ab2s Integer Prompt Specification Draft (v1)

This document contains the exact prompt assembly drafts for the 4 pilot integer tasks under the **Ab2s (Skill-style Precise Specification)** condition. 

The prompt assembly structure is:
$$\text{Ab2s Prompt} = \text{Exact Frozen Ab2g Prompt} + \text{\n\n} + \text{Task-local Ab2s Skill Block}$$

---

## 1. ce111_q03_prime_factor_selection

* **Task ID**: `ce111_q03_prime_factor_selection`
* **Task-local Allowlist APIs**: `IntegerOps.is_divisible`, `IntegerOps.safe_eval`
* **Ab2s Prompt Draft**:

```text
Write only Python source. Implement def generate(level=1, **kwargs).
Task: ce111_q03_prime_factor_selection (integers, difficulty level 1).
Task specification: math16_prime_factor_selection.
Frozen sampled parameters: {"candidates": [11, 12, 13, 14], "n": 156}
generate() must return a dict with exactly question_text, correct_answer, and oracle_payload. question_text must use formal LaTeX delimiters where math appears. correct_answer must be a single exact integer. oracle_payload must exactly equal the frozen sampled parameters. Do not use input, files, network, subprocess, Markdown fences, or explanations.

## Clean-incremental GENERIC
Output complete Python source only. Do not use Markdown fences or explanatory prose. Preserve frozen parameters exactly. Verify that generate() exists. Verify that the return value has exactly the three required top-level keys. Verify field types match the stated contract and that oracle_payload equals the frozen parameters.

## Skill-style Precise Specification (Ab2s)
For integers tasks, you must strictly follow these engineering specifications:
1. Namespace & Injection: Direct call IntegerOps.method(...) where needed. Do not import IntegerOps; it is pre-injected.
2. Native Operators First: Prefer native Python syntax (e.g., +, -, *, //, %, **, loops, comparisons) for basic arithmetic. Plain int math is encouraged.
3. Decouple Logic: Compute the mathematical answer (stored in a JSON-safe int/bool/dict/list) first, then format question_text (LaTeX) and correct_answer separately.
4. Forbidden APIs: Do not use IntegerOps.add or IntegerOps.sub (they are not supported by the runtime injection template). Do not use eval() or invent any undocumented helpers.
5. Task-Local Allowlist (use only these if calling IntegerOps):
   - `IntegerOps.is_divisible` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: bool
   - `IntegerOps.safe_eval` | import: `core.prompts.domain_function_library` | signature: `(expr)` | returns: int | float
6. Quality Gate Self-Check: Verify that generate() exists, returns exactly 3 top-level keys matching the task schema, does not alter frozen parameters, and output contains no markdown fences or explanations.
```

---

## 2. ce112_q01_negative_integer_power

* **Task ID**: `ce112_q01_negative_integer_power`
* **Task-local Allowlist APIs**: `IntegerOps.safe_eval`, `IntegerOps.fmt_num`
* **Ab2s Prompt Draft**:

```text
Write only Python source. Implement def generate(level=1, **kwargs).
Task: ce112_q01_negative_integer_power (integers, difficulty level 1).
Task specification: math16_negative_integer_power.
Frozen sampled parameters: {"base": -3, "exponent": 3}
generate() must return a dict with exactly question_text, correct_answer, and oracle_payload. question_text must use formal LaTeX delimiters where math appears. correct_answer must be a single exact integer. oracle_payload must exactly equal the frozen sampled parameters. Do not use input, files, network, subprocess, Markdown fences, or explanations.

## Clean-incremental GENERIC
Output complete Python source only. Do not use Markdown fences or explanatory prose. Preserve frozen parameters exactly. Verify that generate() exists. Verify that the return value has exactly the three required top-level keys. Verify field types match the stated contract and that oracle_payload equals the frozen parameters.

## Skill-style Precise Specification (Ab2s)
For integers tasks, you must strictly follow these engineering specifications:
1. Namespace & Injection: Direct call IntegerOps.method(...) where needed. Do not import IntegerOps; it is pre-injected.
2. Native Operators First: Prefer native Python syntax (e.g., +, -, *, //, %, **, loops, comparisons) for basic arithmetic. Plain int math is encouraged.
3. Decouple Logic: Compute the mathematical answer (stored in a JSON-safe int/bool/dict/list) first, then format question_text (LaTeX) and correct_answer separately.
4. Forbidden APIs: Do not use IntegerOps.add or IntegerOps.sub (they are not supported by the runtime injection template). Do not use eval() or invent any undocumented helpers.
5. Task-Local Allowlist (use only these if calling IntegerOps):
   - `IntegerOps.safe_eval` | import: `core.prompts.domain_function_library` | signature: `(expr)` | returns: int | float
   - `IntegerOps.fmt_num` | import: `core.prompts.domain_function_library` | signature: `(n)` | returns: str
6. Quality Gate Self-Check: Verify that generate() exists, returns exactly 3 top-level keys matching the task schema, does not alter frozen parameters, and output contains no markdown fences or explanations.
```

---

## 3. ce112_q09_divisor_multiple_intersection

* **Task ID**: `ce112_q09_divisor_multiple_intersection`
* **Task-local Allowlist APIs**: `IntegerOps.is_divisible`, `IntegerOps.safe_eval`
* **Ab2s Prompt Draft**:

```text
Write only Python source. Implement def generate(level=1, **kwargs).
Task: ce112_q09_divisor_multiple_intersection (integers, difficulty level 1).
Task specification: math16_divisor_multiple_intersection.
Frozen sampled parameters: {"divisor_of": 216, "multiple_of": 18}
generate() must return a dict with exactly question_text, correct_answer, and oracle_payload. question_text must use formal LaTeX delimiters where math appears. correct_answer must be a JSON-compatible dict with exactly count (int). oracle_payload must exactly equal the frozen sampled parameters. Do not use input, files, network, subprocess, Markdown fences, or explanations.

## Clean-incremental GENERIC
Output complete Python source only. Do not use Markdown fences or explanatory prose. Preserve frozen parameters exactly. Verify that generate() exists. Verify that the return value has exactly the three required top-level keys. Verify field types match the stated contract and that oracle_payload equals the frozen parameters.

## Skill-style Precise Specification (Ab2s)
For integers tasks, you must strictly follow these engineering specifications:
1. Namespace & Injection: Direct call IntegerOps.method(...) where needed. Do not import IntegerOps; it is pre-injected.
2. Native Operators First: Prefer native Python syntax (e.g., +, -, *, //, %, **, loops, comparisons) for basic arithmetic. Plain int math is encouraged.
3. Decouple Logic: Compute the mathematical answer (stored in a JSON-safe int/bool/dict/list) first, then format question_text (LaTeX) and correct_answer separately.
4. Forbidden APIs: Do not use IntegerOps.add or IntegerOps.sub (they are not supported by the runtime injection template). Do not use eval() or invent any undocumented helpers.
5. Task-Local Allowlist (use only these if calling IntegerOps):
   - `IntegerOps.is_divisible` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: bool
   - `IntegerOps.safe_eval` | import: `core.prompts.domain_function_library` | signature: `(expr)` | returns: int | float
6. Quality Gate Self-Check: Verify that generate() exists, returns exactly 3 top-level keys matching the task schema, does not alter frozen parameters, and output contains no markdown fences or explanations.
```

---

## 4. ce111_nonchoice_q01_part1_exponential_growth

* **Task ID**: `ce111_nonchoice_q01_part1_exponential_growth`
* **Task-local Allowlist APIs**: `IntegerOps.safe_eval`, `IntegerOps.fmt_num`
* **Ab2s Prompt Draft**:

```text
Write only Python source. Implement def generate(level=1, **kwargs).
Task: ce111_nonchoice_q01_part1_exponential_growth (integers, difficulty level 1).
Task specification: math16_exponential_growth_generation_count.
Frozen sampled parameters: {"days": 15, "hours_per_generation": 20, "initial": 1, "split_factor": 4}
generate() must return a dict with exactly question_text, correct_answer, and oracle_payload. question_text must use formal LaTeX delimiters where math appears. correct_answer must be a JSON-compatible dict with exactly k (int). oracle_payload must exactly equal the frozen sampled parameters. Do not use input, files, network, subprocess, Markdown fences, or explanations.

## Clean-incremental GENERIC
Output complete Python source only. Do not use Markdown fences or explanatory prose. Preserve frozen parameters exactly. Verify that generate() exists. Verify that the return value has exactly the three required top-level keys. Verify field types match the stated contract and that oracle_payload equals the frozen parameters.

## Skill-style Precise Specification (Ab2s)
For integers tasks, you must strictly follow these engineering specifications:
1. Namespace & Injection: Direct call IntegerOps.method(...) where needed. Do not import IntegerOps; it is pre-injected.
2. Native Operators First: Prefer native Python syntax (e.g., +, -, *, //, %, **, loops, comparisons) for basic arithmetic. Plain int math is encouraged.
3. Decouple Logic: Compute the mathematical answer (stored in a JSON-safe int/bool/dict/list) first, then format question_text (LaTeX) and correct_answer separately.
4. Forbidden APIs: Do not use IntegerOps.add or IntegerOps.sub (they are not supported by the runtime injection template). Do not use eval() or invent any undocumented helpers.
5. Task-Local Allowlist (use only these if calling IntegerOps):
   - `IntegerOps.safe_eval` | import: `core.prompts.domain_function_library` | signature: `(expr)` | returns: int | float
   - `IntegerOps.fmt_num` | import: `core.prompts.domain_function_library` | signature: `(n)` | returns: str
6. Quality Gate Self-Check: Verify that generate() exists, returns exactly 3 top-level keys matching the task schema, does not alter frozen parameters, and output contains no markdown fences or explanations.
```
