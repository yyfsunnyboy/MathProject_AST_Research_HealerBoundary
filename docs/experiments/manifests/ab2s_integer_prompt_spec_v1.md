# Ab2s Integer Prompt Specification Draft (v1)

This document contains the exact prompt assembly drafts for the 4 pilot integer tasks under the **ab2s_integer_skill** condition.

The prompt assembly structure is:
$$\text{Ab2s Prompt} = \text{Exact Frozen Ab2g Prompt} + \text{\n\n} + \text{Task-local Ab2s Skill Block}$$

No module import paths are included in the model-visible prompts.

---

## 1. ce111_q03_prime_factor_selection

* **Task ID**: `ce111_q03_prime_factor_selection`
* **Structural Tag**: `divisibility-and-prime-factor selection`
* **Task-local Allowlist APIs**: `IntegerOps.is_divisible`
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
For integer tasks, you must strictly follow these engineering specifications:
1. Structural Tag: divisibility-and-prime-factor selection
2. Namespace & Injection: Direct call IntegerOps.method(...) where needed. Do not import IntegerOps; it is pre-injected.
3. Native Operators First: Prefer native Python syntax (e.g., +, -, *, //, %, **, loops, comparisons) for basic arithmetic. Plain int math is encouraged.
4. Forbidden APIs: Do not use IntegerOps.add or IntegerOps.sub (they are not supported by the runtime injection template). Do not use eval() or invent any undocumented helpers.
5. Task-Local Domain API Allowlist:
   - IntegerOps.is_divisible(a, b) -> bool
     Availability: already injected into runtime scope.
     Call exactly as IntegerOps.is_divisible(a, b).
     Do not import IntegerOps.
6. Quality Gate Self-Check: Before outputting, you must verify that:
   - generate() exists.
   - The returned dict has exactly the top-level keys: question_text, correct_answer, and oracle_payload.
   - Frozen parameters are unchanged, and oracle_payload fields, values, and types match the contract.
   - correct_answer type matches this task's contract.
   - All names and variables are defined before use.
   - API calls use the full dotted path.
   - No APIs outside the allowlist are used.
   - IntegerOps.add, IntegerOps.sub, and built-in eval() are not used.
   - No helpers, adapters, or converters are fabricated.
   - All output values are JSON-serializable.
   - Exact computation is completed first, and then question_text and LaTeX are constructed.
   - Output contains no Markdown fences and no explanatory prose.
```

---

## 2. ce112_q01_negative_integer_power

* **Task ID**: `ce112_q01_negative_integer_power`
* **Structural Tag**: `signed integer exponentiation`
* **Task-local Allowlist APIs**: none
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
For integer tasks, you must strictly follow these engineering specifications:
1. Structural Tag: signed integer exponentiation
2. Domain API Use: No IntegerOps API is allowed or needed for this task. Do not import or call IntegerOps.
3. Native Operators First: Prefer native Python syntax (e.g., +, -, *, //, %, **, loops, comparisons) for basic arithmetic. Plain int math is encouraged.
4. Forbidden APIs: Do not use IntegerOps.add or IntegerOps.sub (they are not supported by the runtime injection template). Do not use eval() or invent any undocumented helpers.
5. Task-Local Domain API Allowlist: none.
   Do not call any IntegerOps method for this task.
   Use native Python integer exponentiation with **.
6. Quality Gate Self-Check: Before outputting, you must verify that:
   - generate() exists.
   - The returned dict has exactly the top-level keys: question_text, correct_answer, and oracle_payload.
   - Frozen parameters are unchanged, and oracle_payload fields, values, and types match the contract.
   - correct_answer type matches this task's contract.
   - All names and variables are defined before use.
   - API calls use the full dotted path.
   - No APIs outside the allowlist are used.
   - IntegerOps.add, IntegerOps.sub, and built-in eval() are not used.
   - No helpers, adapters, or converters are fabricated.
   - All output values are JSON-serializable.
   - Exact computation is completed first, and then question_text and LaTeX are constructed.
   - Output contains no Markdown fences and no explanatory prose.
```

---

## 3. ce112_q09_divisor_multiple_intersection

* **Task ID**: `ce112_q09_divisor_multiple_intersection`
* **Structural Tag**: `divisor-multiple intersection`
* **Task-local Allowlist APIs**: `IntegerOps.is_divisible`
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
For integer tasks, you must strictly follow these engineering specifications:
1. Structural Tag: divisor-multiple intersection
2. Namespace & Injection: Direct call IntegerOps.method(...) where needed. Do not import IntegerOps; it is pre-injected.
3. Native Operators First: Prefer native Python syntax (e.g., +, -, *, //, %, **, loops, comparisons) for basic arithmetic. Plain int math is encouraged.
4. Forbidden APIs: Do not use IntegerOps.add or IntegerOps.sub (they are not supported by the runtime injection template). Do not use eval() or invent any undocumented helpers.
5. Task-Local Domain API Allowlist:
   - IntegerOps.is_divisible(a, b) -> bool
     Availability: already injected into runtime scope.
     Call exactly as IntegerOps.is_divisible(a, b).
     Do not import IntegerOps.
6. Quality Gate Self-Check: Before outputting, you must verify that:
   - generate() exists.
   - The returned dict has exactly the top-level keys: question_text, correct_answer, and oracle_payload.
   - Frozen parameters are unchanged, and oracle_payload fields, values, and types match the contract.
   - correct_answer type matches this task's contract.
   - All names and variables are defined before use.
   - API calls use the full dotted path.
   - No APIs outside the allowlist are used.
   - IntegerOps.add, IntegerOps.sub, and built-in eval() are not used.
   - No helpers, adapters, or converters are fabricated.
   - All output values are JSON-serializable.
   - Exact computation is completed first, and then question_text and LaTeX are constructed.
   - Output contains no Markdown fences and no explanatory prose.
```

---

## 4. ce111_nonchoice_q01_part1_exponential_growth

* **Task ID**: `ce111_nonchoice_q01_part1_exponential_growth`
* **Structural Tag**: `discrete exponential growth`
* **Task-local Allowlist APIs**: none
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
For integer tasks, you must strictly follow these engineering specifications:
1. Structural Tag: discrete exponential growth
2. Domain API Use: No IntegerOps API is allowed or needed for this task. Do not import or call IntegerOps.
3. Native Operators First: Prefer native Python syntax (e.g., +, -, *, //, %, **, loops, comparisons) for basic arithmetic. Plain int math is encouraged.
4. Forbidden APIs: Do not use IntegerOps.add or IntegerOps.sub (they are not supported by the runtime injection template). Do not use eval() or invent any undocumented helpers.
5. Task-Local Domain API Allowlist: none.
   Do not call any IntegerOps method for this task.
   Use native Python integer arithmetic only.
6. Quality Gate Self-Check: Before outputting, you must verify that:
   - generate() exists.
   - The returned dict has exactly the top-level keys: question_text, correct_answer, and oracle_payload.
   - Frozen parameters are unchanged, and oracle_payload fields, values, and types match the contract.
   - correct_answer type matches this task's contract.
   - All names and variables are defined before use.
   - API calls use the full dotted path.
   - No APIs outside the allowlist are used.
   - IntegerOps.add, IntegerOps.sub, and built-in eval() are not used.
   - No helpers, adapters, or converters are fabricated.
   - All output values are JSON-serializable.
   - Exact computation is completed first, and then question_text and LaTeX are constructed.
   - Output contains no Markdown fences and no explanatory prose.
```
