# 📋 Historical Healer Rule Inventory

This document inventories all individual rules executed by the historical Healer pipeline, including their triggers, exact transformations, risks, and recommended statuses for formal boundaries.

| Rule ID | File | Function | Stage | Deterministic | Recommended Status |
| :--- | :--- | :--- | :--- | :---: | :--- |
| `R01_markdown_fence_strip` | `core/code_generator.py` | `_basic_cleanup` | basic | yes | `SAFE_GENERIC_CANDIDATE` |
| `R02_outro_chinese_strip` | `core/code_generator.py` | `_basic_cleanup` | basic | yes | `SAFE_GENERIC_CANDIDATE` |
| `R03_trailing_artifact_remove` | `core/healers/regex_healer.py` | `RegexHealer.remove_trailing_artifacts` | regex | yes | `SAFE_GENERIC_CANDIDATE` |
| `R04_mismatched_braces_fix` | `core/healers/regex_healer.py` | `RegexHealer.fix_mismatched_braces` | regex | yes | `SAFE_GENERIC_CANDIDATE` |
| `R05_input_call_removal` | `core/healers/regex_healer.py` | `RegexHealer.remove_input_calls` | regex | yes | `VALIDATION_ONLY` |
| `R06_fullwidth_punctuation_normalize` | `core/healers/regex_healer.py` | `RegexHealer.fix_common_syntax_errors` | regex | yes | `SAFE_GENERIC_CANDIDATE` |
| `R07_missing_class_prefix_autocomplete` | `core/healers/regex_healer.py` | `RegexHealer.fix_missing_class_prefix` | regex | yes | `SAFE_DOMAIN_CANDIDATE` |
| `R08_incorrect_class_method_calls_patch` | `core/healers/regex_healer.py` | `RegexHealer.fix_incorrect_class_method_calls` | regex | yes | `SAFE_DOMAIN_CANDIDATE` |
| `R09_remove_invalid_dependencies` | `core/healers/regex_healer.py` | `RegexHealer.remove_invalid_dependencies` | regex | yes | `SAFE_GENERIC_CANDIDATE` |
| `R10_professor_strong_meds` | `core/healers/regex_healer.py` | `RegexHealer.apply_professor_strong_meds` | regex | yes | `SEMANTIC_OR_UNSAFE` |
| `R11_simplify_term_arg_order_fix` | `core/healers/regex_healer.py` | `RegexHealer.fix_simplify_term_arg_order` | regex | yes | `SEMANTIC_OR_UNSAFE` |
| `R12_xor_to_pow_ast` | `core/healers/ast_healer.py` | `ASTHealer.visit_BinOp` | AST | yes | `SAFE_GENERIC_CANDIDATE` |
| `R13_dangerous_eval_exec_intercept` | `core/healers/ast_healer.py` | `ASTHealer.visit_Call` | AST | yes | `VALIDATION_ONLY` |
| `R14_hallucinated_functions_rename` | `core/healers/ast_healer.py` | `ASTHealer.visit_Call` | AST | yes | `SAFE_DOMAIN_CANDIDATE` |
| `R15_fmt_num_tuple_assignment_split` | `core/healers/ast_healer.py` | `ASTHealer.visit_Assign` | AST | yes | `SAFE_DOMAIN_CANDIDATE` |
| `R16_while_true_circuit_breaker` | `core/healers/ast_healer.py` | `ASTHealer.visit_While` | AST | yes | `SAFE_GENERIC_CANDIDATE` |
| `R17_missing_generate_fallback_injector` | `core/healers/ast_healer.py` | `ASTHealer.heal` | AST | yes | `VALIDATION_ONLY` |
| `R18_duplicate_shadow_killer` | `core/healers/ast_healer.py` | `ASTHealer.visit_FunctionDef` | AST | yes | `SAFE_GENERIC_CANDIDATE` |
| `R19_semantic_self_healing_llm` | `core/healers/ast_healer.py` | `ASTHealer.semantic_heal` | fallback | no | `SEMANTIC_OR_UNSAFE` |

---

## Rule Details

### R01_markdown_fence_strip - _basic_cleanup
- **Source File**: [code_generator.py](file:///core/code_generator.py)
- **Approximate Lines**: 760-764
- **Stage**: `basic`
- **Deterministic**: yes
- **Model Calls**: no
- **Requires Scaffold Contract**: no
- **Changes Program Semantics Risk**: `LOW`
- **Trigger Condition**: Presence of ```python or ``` fences enclosing raw generated code
- **Exact Transformation**: *Removes the fences, leaving only the enclosed code block*
- **Recommended Status**: **`SAFE_GENERIC_CANDIDATE`**

---

### R02_outro_chinese_strip - _basic_cleanup
- **Source File**: [code_generator.py](file:///core/code_generator.py)
- **Approximate Lines**: 765-820
- **Stage**: `basic`
- **Deterministic**: yes
- **Model Calls**: no
- **Requires Scaffold Contract**: no
- **Changes Program Semantics Risk**: `MEDIUM`
- **Trigger Condition**: Presence of conversational text (Chinese characters or intro headers) outside code structures
- **Exact Transformation**: *Strips lines containing Chinese characters or headers like 'Explanation:' from the start/end of the file*
- **Recommended Status**: **`SAFE_GENERIC_CANDIDATE`**

---

### R03_trailing_artifact_remove - RegexHealer.remove_trailing_artifacts
- **Source File**: [regex_healer.py](file:///core/healers/regex_healer.py)
- **Approximate Lines**: 75-129
- **Stage**: `regex`
- **Deterministic**: yes
- **Model Calls**: no
- **Requires Scaffold Contract**: no
- **Changes Program Semantics Risk**: `LOW`
- **Trigger Condition**: Code block ends with trailing syntax residues such as dangling closing curly braces '}' or literal text 'python'
- **Exact Transformation**: *Strips trailing non-Python characters and whitespace from the end of the script*
- **Recommended Status**: **`SAFE_GENERIC_CANDIDATE`**

---

### R04_mismatched_braces_fix - RegexHealer.fix_mismatched_braces
- **Source File**: [regex_healer.py](file:///core/healers/regex_healer.py)
- **Approximate Lines**: 130-174
- **Stage**: `regex`
- **Deterministic**: yes
- **Model Calls**: no
- **Requires Scaffold Contract**: no
- **Changes Program Semantics Risk**: `MEDIUM`
- **Trigger Condition**: Presence of unmatched opening brackets (, [, or { in the generated return statement
- **Exact Transformation**: *Appends the appropriate matching closing brackets to balance the expression*
- **Recommended Status**: **`SAFE_GENERIC_CANDIDATE`**

---

### R05_input_call_removal - RegexHealer.remove_input_calls
- **Source File**: [regex_healer.py](file:///core/healers/regex_healer.py)
- **Approximate Lines**: 685-700
- **Stage**: `regex`
- **Deterministic**: yes
- **Model Calls**: no
- **Requires Scaffold Contract**: no
- **Changes Program Semantics Risk**: `MEDIUM`
- **Trigger Condition**: Presence of `input()` or `input('prompt')` calls in code, which would cause execution hangs
- **Exact Transformation**: *Replaces `input(...)` calls with `'0'` or `0`*
- **Recommended Status**: **`VALIDATION_ONLY`**

---

### R06_fullwidth_punctuation_normalize - RegexHealer.fix_common_syntax_errors
- **Source File**: [regex_healer.py](file:///core/healers/regex_healer.py)
- **Approximate Lines**: 391-466
- **Stage**: `regex`
- **Deterministic**: yes
- **Model Calls**: no
- **Requires Scaffold Contract**: no
- **Changes Program Semantics Risk**: `LOW`
- **Trigger Condition**: Presence of fullwidth/Chinese punctuation marks inside active code lines (excluding comments)
- **Exact Transformation**: *Normalizes `（` -> `(`, `）` -> `)`, `，` -> `,`, `：` -> `:`, etc.*
- **Recommended Status**: **`SAFE_GENERIC_CANDIDATE`**

---

### R07_missing_class_prefix_autocomplete - RegexHealer.fix_missing_class_prefix
- **Source File**: [regex_healer.py](file:///core/healers/regex_healer.py)
- **Approximate Lines**: 1138-1185
- **Stage**: `regex`
- **Deterministic**: yes
- **Model Calls**: no
- **Requires Scaffold Contract**: yes
- **Changes Program Semantics Risk**: `LOW`
- **Trigger Condition**: Model invokes standard helper methods (e.g. `simplify_term()`) directly without class prefix, where method is not locally defined
- **Exact Transformation**: *Prepends `RadicalOps.` or corresponding class prefix to the method call*
- **Recommended Status**: **`SAFE_DOMAIN_CANDIDATE`**

---

### R08_incorrect_class_method_calls_patch - RegexHealer.fix_incorrect_class_method_calls
- **Source File**: [regex_healer.py](file:///core/healers/regex_healer.py)
- **Approximate Lines**: 576-606
- **Stage**: `regex`
- **Deterministic**: yes
- **Model Calls**: no
- **Requires Scaffold Contract**: yes
- **Changes Program Semantics Risk**: `LOW`
- **Trigger Condition**: Model calls bare functions like `fmt_num` or `to_latex` without the class name prefix, e.g. `fmt_num(a)`
- **Exact Transformation**: *Prepends class names: `fmt_num` -> `IntegerOps.fmt_num`, `to_latex` -> `FractionOps.to_latex`*
- **Recommended Status**: **`SAFE_DOMAIN_CANDIDATE`**

---

### R09_remove_invalid_dependencies - RegexHealer.remove_invalid_dependencies
- **Source File**: [regex_healer.py](file:///core/healers/regex_healer.py)
- **Approximate Lines**: 1187-1220
- **Stage**: `regex`
- **Deterministic**: yes
- **Model Calls**: no
- **Requires Scaffold Contract**: no
- **Changes Program Semantics Risk**: `LOW`
- **Trigger Condition**: Presence of imports referencing domain libraries from the codebase (which will be injected inline later)
- **Exact Transformation**: *Deletes lines like `from domain_function_library import ...` or `from core.healers import ...` (excluding DomainFunctionHelper)*
- **Recommended Status**: **`SAFE_GENERIC_CANDIDATE`**

---

### R10_professor_strong_meds - RegexHealer.apply_professor_strong_meds
- **Source File**: [regex_healer.py](file:///core/healers/regex_healer.py)
- **Approximate Lines**: 210-289
- **Stage**: `regex`
- **Deterministic**: yes
- **Model Calls**: no
- **Requires Scaffold Contract**: yes
- **Changes Program Semantics Risk**: `HIGH`
- **Trigger Condition**: Dangling math variables, unmapped pattern IDs, or nested tuple call contradictions in Radicals
- **Exact Transformation**: *Replaces unmapped pattern IDs, fixes `int(simplify())` -> `simplify()[0]`, and injects local fallback assignments before `return {`*
- **Recommended Status**: **`SEMANTIC_OR_UNSAFE`**

---

### R11_simplify_term_arg_order_fix - RegexHealer.fix_simplify_term_arg_order
- **Source File**: [regex_healer.py](file:///core/healers/regex_healer.py)
- **Approximate Lines**: 632-684
- **Stage**: `regex`
- **Deterministic**: yes
- **Model Calls**: no
- **Requires Scaffold Contract**: yes
- **Changes Program Semantics Risk**: `HIGH`
- **Trigger Condition**: Model invokes `simplify_term` with incorrect argument ordering (e.g. `(coeff, radicand)` flipped)
- **Exact Transformation**: *Detects parameter semantics and flips argument order to match the API contract*
- **Recommended Status**: **`SEMANTIC_OR_UNSAFE`**

---

### R12_xor_to_pow_ast - ASTHealer.visit_BinOp
- **Source File**: [ast_healer.py](file:///core/healers/ast_healer.py)
- **Approximate Lines**: 63-73
- **Stage**: `AST`
- **Deterministic**: yes
- **Model Calls**: no
- **Requires Scaffold Contract**: no
- **Changes Program Semantics Risk**: `LOW`
- **Trigger Condition**: Model uses the BitXor operator `^` (e.g., `x^2`) instead of power operator `**` (e.g., `x**2`)
- **Exact Transformation**: *Converts `ast.BitXor` node to `ast.Pow` node*
- **Recommended Status**: **`SAFE_GENERIC_CANDIDATE`**

---

### R13_dangerous_eval_exec_intercept - ASTHealer.visit_Call
- **Source File**: [ast_healer.py](file:///core/healers/ast_healer.py)
- **Approximate Lines**: 106-118
- **Stage**: `AST`
- **Deterministic**: yes
- **Model Calls**: no
- **Requires Scaffold Contract**: no
- **Changes Program Semantics Risk**: `LOW`
- **Trigger Condition**: Presence of native `eval()` or `exec()` calls in generated code
- **Exact Transformation**: *Replaces the call with `safe_eval()` and strips extra arguments*
- **Recommended Status**: **`VALIDATION_ONLY`**

---

### R14_hallucinated_functions_rename - ASTHealer.visit_Call
- **Source File**: [ast_healer.py](file:///core/healers/ast_healer.py)
- **Approximate Lines**: 92-105
- **Stage**: `AST`
- **Deterministic**: yes
- **Model Calls**: no
- **Requires Scaffold Contract**: yes
- **Changes Program Semantics Risk**: `MEDIUM`
- **Trigger Condition**: Model invokes hallucinated functions such as `format_polynomial()` or `poly_to_latex()`
- **Exact Transformation**: *Renames the function node ID to `build_polynomial_text`*
- **Recommended Status**: **`SAFE_DOMAIN_CANDIDATE`**

---

### R15_fmt_num_tuple_assignment_split - ASTHealer.visit_Assign
- **Source File**: [ast_healer.py](file:///core/healers/ast_healer.py)
- **Approximate Lines**: 342-371
- **Stage**: `AST`
- **Deterministic**: yes
- **Model Calls**: no
- **Requires Scaffold Contract**: yes
- **Changes Program Semantics Risk**: `LOW`
- **Trigger Condition**: Model assigns `fmt_num` to a tuple, e.g. `val, latex = fmt_num(x)` (due to hallucination that fmt_num returns 2 values)
- **Exact Transformation**: *Splits the statement into `val = x` and `latex = fmt_num(x)`*
- **Recommended Status**: **`SAFE_DOMAIN_CANDIDATE`**

---

### R16_while_true_circuit_breaker - ASTHealer.visit_While
- **Source File**: [ast_healer.py](file:///core/healers/ast_healer.py)
- **Approximate Lines**: 309-341
- **Stage**: `AST`
- **Deterministic**: yes
- **Model Calls**: no
- **Requires Scaffold Contract**: no
- **Changes Program Semantics Risk**: `MEDIUM`
- **Trigger Condition**: Presence of a potentially infinite loop block `while True:` or `while 1:`
- **Exact Transformation**: *Converts the `While` node into a bounded `For` node over `range(1000)` using a safety variable*
- **Recommended Status**: **`SAFE_GENERIC_CANDIDATE`**

---

### R17_missing_generate_fallback_injector - ASTHealer.heal
- **Source File**: [ast_healer.py](file:///core/healers/ast_healer.py)
- **Approximate Lines**: 406-490
- **Stage**: `AST`
- **Deterministic**: yes
- **Model Calls**: no
- **Requires Scaffold Contract**: no
- **Changes Program Semantics Risk**: `MEDIUM`
- **Trigger Condition**: The compiled AST completely misses the required entry-point function (e.g. `generate()`)
- **Exact Transformation**: *Appends a fallback `generate()` function returning safe placeholder error strings to prevent pipeline crashes*
- **Recommended Status**: **`VALIDATION_ONLY`**

---

### R18_duplicate_shadow_killer - ASTHealer.visit_FunctionDef
- **Source File**: [ast_healer.py](file:///core/healers/ast_healer.py)
- **Approximate Lines**: 215-288
- **Stage**: `AST`
- **Deterministic**: yes
- **Model Calls**: no
- **Requires Scaffold Contract**: no
- **Changes Program Semantics Risk**: `LOW`
- **Trigger Condition**: Model defines a local stub/empty function that shadows an injected library function (e.g., empty `fmt_num()`)
- **Exact Transformation**: *Removes the local function definition so the code falls back to the injected domain utility definition*
- **Recommended Status**: **`SAFE_GENERIC_CANDIDATE`**

---

### R19_semantic_self_healing_llm - ASTHealer.semantic_heal
- **Source File**: [ast_healer.py](file:///core/healers/ast_healer.py)
- **Approximate Lines**: 491-596
- **Stage**: `fallback`
- **Deterministic**: no
- **Model Calls**: yes
- **Requires Scaffold Contract**: no
- **Changes Program Semantics Risk**: `HIGH`
- **Trigger Condition**: The generated code fails syntax compilation or sandbox verification (throws runtime exception)
- **Exact Transformation**: *Calls the LLM API, providing the code and the error trace, requesting a self-healed replacement code block*
- **Recommended Status**: **`SEMANTIC_OR_UNSAFE`**

---

