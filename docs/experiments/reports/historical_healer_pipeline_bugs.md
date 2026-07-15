# 🐛 Historical Healer Pipeline Bugs & Schema Drifts

This document catalogs the execution bugs, variable mismatches, duplicate functions, and architectural conflicts identified in the historical Healer pipeline during the audit.

---

## 1. Major Variable & Return Unpacking Mismatches

### Mismatch A: `_advanced_healer` Unpacking Crash
*   **Location**: `core/code_generator.py` line 1181 (caller) vs line 830 (definition).
*   **Description**: 
    The function `_advanced_healer` is defined to return **9 values**:
    `return code_after_anti_dup, regex_fixes, ast_fixes, ast_stats, garbage_cleaner_count, removed_list, healer_fixes, eval_eliminator_count, healing_duration`
    
    However, the caller in `auto_generate_skill_code` unpacks exactly **8 variables**:
    `clean_code, regex_fixes, ast_fixes, garbage_cleaner_count, removed_list, healer_fixes, eval_eliminator_count, healing_duration = _advanced_healer(...)`
*   **Outcome**: If this path is executed (e.g. Ab3 is enabled in `code_generator.py`), it will crash immediately with `ValueError: too many values to unpack (expected 8)`.
*   **Avoidance**: In the runner `scaler.py`, this is bypassed via list unpacking: `healed_code, *healer_stats = _advanced_healer(...)`.

### Mismatch B: `_call_ai` Unpacking Crash
*   **Location**: `core/code_generator.py` line 1138 (caller) vs line 449 (definition).
*   **Description**:
    The function `_call_ai` is defined to return **4 values**:
    `return raw_output, prompt_tokens, completion_tokens, thinking_output`
    
    However, the caller in `auto_generate_skill_code` unpacks exactly **3 variables**:
    `raw_output, prompt_tokens, completion_tokens = _call_ai(...)`
*   **Outcome**: Whenever `code_generator.py` attempts to run a generation, it crashes with `ValueError: too many values to unpack (expected 3)`.

---

## 2. Undefined Variable References (NameErrors)

### Mismatch C: Undefined `markdown_cleanup_count`
*   **Location**: `core/code_generator.py` lines 1163-1164.
*   **Description**:
    Under `VERBOSE_LEVEL == 2` in `auto_generate_skill_code`, the following lines are executed:
    `log_fix_detail("[1/4] 檢查 ```python 標記", "fixed" if markdown_cleanup_count > 0 else "skip", ...)`
    
    However, `markdown_cleanup_count` is never defined inside `auto_generate_skill_code`. The variable returned from the cleanup stage is `basic_cleanup_fixes`.
*   **Outcome**: The script raises a `NameError: name 'markdown_cleanup_count' is not defined` and aborts if run with detailed verbosity.

---

## 3. Duplicate Method Definitions

### Mismatch D: `remove_invalid_dependencies` Defined Twice
*   **Location**: `core/healers/regex_healer.py` line 349 and line 1187.
*   **Description**:
    The method `remove_invalid_dependencies` is defined twice inside the `RegexHealer` class. 
    *   The first definition (line 349) strips standard `domain_function_library` imports.
    *   The second definition (line 1187) is more advanced, adding the removal of `RadicalOps` imports (V3.4 rule) and applying negative lookahead filters to protect `DomainFunctionHelper` (V3.5 rule).
*   **Outcome**: Because Python processes class definitions sequentially, the second definition silently overrides the first one. This is technically functional but represents code redundancy and potential maintenance errors.

---

## 4. Documentation vs. Code Direction Conflict

### Mismatch E: V2.8 Method Direction Conflict
*   **Location**: `core/healers/regex_healer.py` line 25 (comment) vs line 576 (code).
*   **Description**:
    The class header documentation at line 25 states that `fix_incorrect_class_method_calls` repairs method calls by mapping:
    `IntegerOps.fmt_num() → fmt_num()` (removing prefix)
    
    However, the actual code implementation at lines 584-601 does the exact opposite:
    `fmt_num(...)` -> `IntegerOps.fmt_num(...)` (adding prefix)
*   **Analysis**: The code implementation is correct and matches the intended API contract of standard domain functions. The documentation comment is reversed.

---

## 5. Temporal Coupling and Injection Sequencing

### Mismatch F: Healing Prior to Scaffold Prepend
*   **Location**: `core/code_generator.py` lines 1180-1205.
*   **Description**:
    The pipeline executes `_advanced_healer` (AST/Regex repairs) directly on the raw model output *before* the scaffold skeleton (`PERFECT_UTILS` and domain library classes) is prepended.
*   **Implications**: 
    1.  The AST parsed by `ASTHealer` is incomplete, meaning it only represents the model's raw output and has no access to the structural context of the standard library classes.
    2.  This requires the healer to proactively strip stubs and duplicate class definitions created by the model, as they would otherwise clash with the skeleton injected in the next step.
