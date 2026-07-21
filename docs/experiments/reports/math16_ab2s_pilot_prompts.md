# Math16 Ab2s Pilot Prompts Specification & Diff Report

This document contains the exact model-visible prompts for both **ab2d_replication** and **ab2s_integer_skill** conditions across the 4 pilot integer tasks, along with precise unified diffs proving their strictly incremental structural relationship.

## Verification Summary

- **Prefix Exact-Match**: Passed. All `ab2s_integer_skill` prompts start with the byte-exact `ab2g` prompt prefix.

- **No Answer/Evaluator Leakage**: Passed. No correct answers, healer rules, or evaluator internals exist in the prompts.

- **Module Import Paths Omitted**: Passed. All `core.prompts.domain_function_library` import paths are omitted from `ab2s_integer_skill` blocks.


---

## Task: ce111_q03_prime_factor_selection

### ab2d_replication — exact model-visible prompt

```text
Write only Python source. Implement def generate(level=1, **kwargs).
Task: ce111_q03_prime_factor_selection (integers, difficulty level 1).
Task specification: math16_prime_factor_selection.
Frozen sampled parameters: {"candidates": [11, 12, 13, 14], "n": 156}
generate() must return a dict with exactly question_text, correct_answer, and oracle_payload. question_text must use formal LaTeX delimiters where math appears. correct_answer must be a single exact integer. oracle_payload must exactly equal the frozen sampled parameters. Do not use input, files, network, subprocess, Markdown fences, or explanations.

## Clean-incremental GENERIC
Output complete Python source only. Do not use Markdown fences or explanatory prose. Preserve frozen parameters exactly. Verify that generate() exists. Verify that the return value has exactly the three required top-level keys. Verify field types match the stated contract and that oracle_payload equals the frozen parameters.

## Clean-incremental DOMAIN
Task-local domain APIs (use only these):
- `IntegerOps.is_divisible` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: bool
- `IntegerOps.safe_eval` | import: `core.prompts.domain_function_library` | signature: `(expr)` | returns: int | float  # bool and container results raise ValueError
Use the listed domain API for each supported core operation, and ensure the returned value contributes to correct_answer.
```

- **SHA-256**: `8704669323fb45ef6bd34331151b350845425d2d14e19b36c58bd2c2c86bc75f`
- **UTF-8 Byte Count**: 1443 bytes
- **Character Count**: 1443 chars

### ab2s_integer_skill — exact model-visible prompt

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

- **SHA-256**: `ab392355fff80ad0886d645a1df5444d9b1fe9151bd567238abcb0e49fb40994`
- **UTF-8 Byte Count**: 2651 bytes
- **Character Count**: 2651 chars

### Prompt diff

```diff
--- ab2d_replication
+++ ab2s_integer_skill
@@ -7,8 +7,27 @@
 ## Clean-incremental GENERIC
 Output complete Python source only. Do not use Markdown fences or explanatory prose. Preserve frozen parameters exactly. Verify that generate() exists. Verify that the return value has exactly the three required top-level keys. Verify field types match the stated contract and that oracle_payload equals the frozen parameters.
 
-## Clean-incremental DOMAIN
-Task-local domain APIs (use only these):
-- `IntegerOps.is_divisible` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: bool
-- `IntegerOps.safe_eval` | import: `core.prompts.domain_function_library` | signature: `(expr)` | returns: int | float  # bool and container results raise ValueError
-Use the listed domain API for each supported core operation, and ensure the returned value contributes to correct_answer.+## Skill-style Precise Specification (Ab2s)
+For integer tasks, you must strictly follow these engineering specifications:
+1. Structural Tag: divisibility-and-prime-factor selection
+2. Namespace & Injection: Direct call IntegerOps.method(...) where needed. Do not import IntegerOps; it is pre-injected.
+3. Native Operators First: Prefer native Python syntax (e.g., +, -, *, //, %, **, loops, comparisons) for basic arithmetic. Plain int math is encouraged.
+4. Forbidden APIs: Do not use IntegerOps.add or IntegerOps.sub (they are not supported by the runtime injection template). Do not use eval() or invent any undocumented helpers.
+5. Task-Local Domain API Allowlist:
+   - IntegerOps.is_divisible(a, b) -> bool
+     Availability: already injected into runtime scope.
+     Call exactly as IntegerOps.is_divisible(a, b).
+     Do not import IntegerOps.
+6. Quality Gate Self-Check: Before outputting, you must verify that:
+   - generate() exists.
+   - The returned dict has exactly the top-level keys: question_text, correct_answer, and oracle_payload.
+   - Frozen parameters are unchanged, and oracle_payload fields, values, and types match the contract.
+   - correct_answer type matches this task's contract.
+   - All names and variables are defined before use.
+   - API calls use the full dotted path.
+   - No APIs outside the allowlist are used.
+   - IntegerOps.add, IntegerOps.sub, and built-in eval() are not used.
+   - No helpers, adapters, or converters are fabricated.
+   - All output values are JSON-serializable.
+   - Exact computation is completed first, and then question_text and LaTeX are constructed.
+   - Output contains no Markdown fences and no explanatory prose.
```


---

## Task: ce112_q01_negative_integer_power

### ab2d_replication — exact model-visible prompt

```text
Write only Python source. Implement def generate(level=1, **kwargs).
Task: ce112_q01_negative_integer_power (integers, difficulty level 1).
Task specification: math16_negative_integer_power.
Frozen sampled parameters: {"base": -3, "exponent": 3}
generate() must return a dict with exactly question_text, correct_answer, and oracle_payload. question_text must use formal LaTeX delimiters where math appears. correct_answer must be a single exact integer. oracle_payload must exactly equal the frozen sampled parameters. Do not use input, files, network, subprocess, Markdown fences, or explanations.

## Clean-incremental GENERIC
Output complete Python source only. Do not use Markdown fences or explanatory prose. Preserve frozen parameters exactly. Verify that generate() exists. Verify that the return value has exactly the three required top-level keys. Verify field types match the stated contract and that oracle_payload equals the frozen parameters.

## Clean-incremental DOMAIN
Task-local domain APIs (use only these):
- `IntegerOps.safe_eval` | import: `core.prompts.domain_function_library` | signature: `(expr)` | returns: int | float  # bool and container results raise ValueError
- `IntegerOps.fmt_num` | import: `core.prompts.domain_function_library` | signature: `(n)` | returns: str
Use the listed domain API for each supported core operation, and ensure the returned value contributes to correct_answer.
```

- **SHA-256**: `a03c40a37de8c5652476da0fcd76dfc714ca55c19b0279b0452358c81ccde8d4`
- **UTF-8 Byte Count**: 1419 bytes
- **Character Count**: 1419 chars

### ab2s_integer_skill — exact model-visible prompt

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

- **SHA-256**: `6e6b5a69864db02dd5237cc448bd71b1103888998ee83b5b3f72a74e5699b733`
- **UTF-8 Byte Count**: 2541 bytes
- **Character Count**: 2541 chars

### Prompt diff

```diff
--- ab2d_replication
+++ ab2s_integer_skill
@@ -7,8 +7,25 @@
 ## Clean-incremental GENERIC
 Output complete Python source only. Do not use Markdown fences or explanatory prose. Preserve frozen parameters exactly. Verify that generate() exists. Verify that the return value has exactly the three required top-level keys. Verify field types match the stated contract and that oracle_payload equals the frozen parameters.
 
-## Clean-incremental DOMAIN
-Task-local domain APIs (use only these):
-- `IntegerOps.safe_eval` | import: `core.prompts.domain_function_library` | signature: `(expr)` | returns: int | float  # bool and container results raise ValueError
-- `IntegerOps.fmt_num` | import: `core.prompts.domain_function_library` | signature: `(n)` | returns: str
-Use the listed domain API for each supported core operation, and ensure the returned value contributes to correct_answer.+## Skill-style Precise Specification (Ab2s)
+For integer tasks, you must strictly follow these engineering specifications:
+1. Structural Tag: signed integer exponentiation
+2. Domain API Use: No IntegerOps API is allowed or needed for this task. Do not import or call IntegerOps.
+3. Native Operators First: Prefer native Python syntax (e.g., +, -, *, //, %, **, loops, comparisons) for basic arithmetic. Plain int math is encouraged.
+4. Forbidden APIs: Do not use IntegerOps.add or IntegerOps.sub (they are not supported by the runtime injection template). Do not use eval() or invent any undocumented helpers.
+5. Task-Local Domain API Allowlist: none.
+   Do not call any IntegerOps method for this task.
+   Use native Python integer exponentiation with **.
+6. Quality Gate Self-Check: Before outputting, you must verify that:
+   - generate() exists.
+   - The returned dict has exactly the top-level keys: question_text, correct_answer, and oracle_payload.
+   - Frozen parameters are unchanged, and oracle_payload fields, values, and types match the contract.
+   - correct_answer type matches this task's contract.
+   - All names and variables are defined before use.
+   - API calls use the full dotted path.
+   - No APIs outside the allowlist are used.
+   - IntegerOps.add, IntegerOps.sub, and built-in eval() are not used.
+   - No helpers, adapters, or converters are fabricated.
+   - All output values are JSON-serializable.
+   - Exact computation is completed first, and then question_text and LaTeX are constructed.
+   - Output contains no Markdown fences and no explanatory prose.
```


---

## Task: ce112_q09_divisor_multiple_intersection

### ab2d_replication — exact model-visible prompt

```text
Write only Python source. Implement def generate(level=1, **kwargs).
Task: ce112_q09_divisor_multiple_intersection (integers, difficulty level 1).
Task specification: math16_divisor_multiple_intersection.
Frozen sampled parameters: {"divisor_of": 216, "multiple_of": 18}
generate() must return a dict with exactly question_text, correct_answer, and oracle_payload. question_text must use formal LaTeX delimiters where math appears. correct_answer must be a JSON-compatible dict with exactly count (int). oracle_payload must exactly equal the frozen sampled parameters. Do not use input, files, network, subprocess, Markdown fences, or explanations.

## Clean-incremental GENERIC
Output complete Python source only. Do not use Markdown fences or explanatory prose. Preserve frozen parameters exactly. Verify that generate() exists. Verify that the return value has exactly the three required top-level keys. Verify field types match the stated contract and that oracle_payload equals the frozen parameters.

## Clean-incremental DOMAIN
Task-local domain APIs (use only these):
- `IntegerOps.is_divisible` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: bool
- `IntegerOps.safe_eval` | import: `core.prompts.domain_function_library` | signature: `(expr)` | returns: int | float  # bool and container results raise ValueError
Use the listed domain API for each supported core operation, and ensure the returned value contributes to correct_answer.
```

- **SHA-256**: `f4d5abe47b1d3dad2095dbc473b4f58b6f1c8cd4f9ece0ba8a1de9f5c68ad5cb`
- **UTF-8 Byte Count**: 1478 bytes
- **Character Count**: 1478 chars

### ab2s_integer_skill — exact model-visible prompt

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

- **SHA-256**: `90090224429cfaaac0e824563f56000b260796571bc464fa44a9b23e1ee6afb0`
- **UTF-8 Byte Count**: 2676 bytes
- **Character Count**: 2676 chars

### Prompt diff

```diff
--- ab2d_replication
+++ ab2s_integer_skill
@@ -7,8 +7,27 @@
 ## Clean-incremental GENERIC
 Output complete Python source only. Do not use Markdown fences or explanatory prose. Preserve frozen parameters exactly. Verify that generate() exists. Verify that the return value has exactly the three required top-level keys. Verify field types match the stated contract and that oracle_payload equals the frozen parameters.
 
-## Clean-incremental DOMAIN
-Task-local domain APIs (use only these):
-- `IntegerOps.is_divisible` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: bool
-- `IntegerOps.safe_eval` | import: `core.prompts.domain_function_library` | signature: `(expr)` | returns: int | float  # bool and container results raise ValueError
-Use the listed domain API for each supported core operation, and ensure the returned value contributes to correct_answer.+## Skill-style Precise Specification (Ab2s)
+For integer tasks, you must strictly follow these engineering specifications:
+1. Structural Tag: divisor-multiple intersection
+2. Namespace & Injection: Direct call IntegerOps.method(...) where needed. Do not import IntegerOps; it is pre-injected.
+3. Native Operators First: Prefer native Python syntax (e.g., +, -, *, //, %, **, loops, comparisons) for basic arithmetic. Plain int math is encouraged.
+4. Forbidden APIs: Do not use IntegerOps.add or IntegerOps.sub (they are not supported by the runtime injection template). Do not use eval() or invent any undocumented helpers.
+5. Task-Local Domain API Allowlist:
+   - IntegerOps.is_divisible(a, b) -> bool
+     Availability: already injected into runtime scope.
+     Call exactly as IntegerOps.is_divisible(a, b).
+     Do not import IntegerOps.
+6. Quality Gate Self-Check: Before outputting, you must verify that:
+   - generate() exists.
+   - The returned dict has exactly the top-level keys: question_text, correct_answer, and oracle_payload.
+   - Frozen parameters are unchanged, and oracle_payload fields, values, and types match the contract.
+   - correct_answer type matches this task's contract.
+   - All names and variables are defined before use.
+   - API calls use the full dotted path.
+   - No APIs outside the allowlist are used.
+   - IntegerOps.add, IntegerOps.sub, and built-in eval() are not used.
+   - No helpers, adapters, or converters are fabricated.
+   - All output values are JSON-serializable.
+   - Exact computation is completed first, and then question_text and LaTeX are constructed.
+   - Output contains no Markdown fences and no explanatory prose.
```


---

## Task: ce111_nonchoice_q01_part1_exponential_growth

### ab2d_replication — exact model-visible prompt

```text
Write only Python source. Implement def generate(level=1, **kwargs).
Task: ce111_nonchoice_q01_part1_exponential_growth (integers, difficulty level 1).
Task specification: math16_exponential_growth_generation_count.
Frozen sampled parameters: {"days": 15, "hours_per_generation": 20, "initial": 1, "split_factor": 4}
generate() must return a dict with exactly question_text, correct_answer, and oracle_payload. question_text must use formal LaTeX delimiters where math appears. correct_answer must be a JSON-compatible dict with exactly k (int). oracle_payload must exactly equal the frozen sampled parameters. Do not use input, files, network, subprocess, Markdown fences, or explanations.

## Clean-incremental GENERIC
Output complete Python source only. Do not use Markdown fences or explanatory prose. Preserve frozen parameters exactly. Verify that generate() exists. Verify that the return value has exactly the three required top-level keys. Verify field types match the stated contract and that oracle_payload equals the frozen parameters.

## Clean-incremental DOMAIN
Task-local domain APIs (use only these):
- `IntegerOps.safe_eval` | import: `core.prompts.domain_function_library` | signature: `(expr)` | returns: int | float  # bool and container results raise ValueError
- `IntegerOps.fmt_num` | import: `core.prompts.domain_function_library` | signature: `(n)` | returns: str
Use the listed domain API for each supported core operation, and ensure the returned value contributes to correct_answer.
```

- **SHA-256**: `1f1491d3b68e9620550398001b27cd72e2f8b6c08c2debbf346396314a69cb42`
- **UTF-8 Byte Count**: 1511 bytes
- **Character Count**: 1511 chars

### ab2s_integer_skill — exact model-visible prompt

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

- **SHA-256**: `8747d0e6d20071da196ac0481ce2f8b285a1ae45bdde54c47c92fabf36974fd5`
- **UTF-8 Byte Count**: 2624 bytes
- **Character Count**: 2624 chars

### Prompt diff

```diff
--- ab2d_replication
+++ ab2s_integer_skill
@@ -7,8 +7,25 @@
 ## Clean-incremental GENERIC
 Output complete Python source only. Do not use Markdown fences or explanatory prose. Preserve frozen parameters exactly. Verify that generate() exists. Verify that the return value has exactly the three required top-level keys. Verify field types match the stated contract and that oracle_payload equals the frozen parameters.
 
-## Clean-incremental DOMAIN
-Task-local domain APIs (use only these):
-- `IntegerOps.safe_eval` | import: `core.prompts.domain_function_library` | signature: `(expr)` | returns: int | float  # bool and container results raise ValueError
-- `IntegerOps.fmt_num` | import: `core.prompts.domain_function_library` | signature: `(n)` | returns: str
-Use the listed domain API for each supported core operation, and ensure the returned value contributes to correct_answer.+## Skill-style Precise Specification (Ab2s)
+For integer tasks, you must strictly follow these engineering specifications:
+1. Structural Tag: discrete exponential growth
+2. Domain API Use: No IntegerOps API is allowed or needed for this task. Do not import or call IntegerOps.
+3. Native Operators First: Prefer native Python syntax (e.g., +, -, *, //, %, **, loops, comparisons) for basic arithmetic. Plain int math is encouraged.
+4. Forbidden APIs: Do not use IntegerOps.add or IntegerOps.sub (they are not supported by the runtime injection template). Do not use eval() or invent any undocumented helpers.
+5. Task-Local Domain API Allowlist: none.
+   Do not call any IntegerOps method for this task.
+   Use native Python integer arithmetic only.
+6. Quality Gate Self-Check: Before outputting, you must verify that:
+   - generate() exists.
+   - The returned dict has exactly the top-level keys: question_text, correct_answer, and oracle_payload.
+   - Frozen parameters are unchanged, and oracle_payload fields, values, and types match the contract.
+   - correct_answer type matches this task's contract.
+   - All names and variables are defined before use.
+   - API calls use the full dotted path.
+   - No APIs outside the allowlist are used.
+   - IntegerOps.add, IntegerOps.sub, and built-in eval() are not used.
+   - No helpers, adapters, or converters are fabricated.
+   - All output values are JSON-serializable.
+   - Exact computation is completed first, and then question_text and LaTeX are constructed.
+   - Output contains no Markdown fences and no explanatory prose.
```


---
