import json
from pathlib import Path

# Build JSON artifact
audit_data = {
    "audit_metadata": {
        "title": "Math16 Gemini Full-Plan Rationalize Denominator 5-Cell Forensic Audit",
        "target_commit": "f0fbf4a0c2131f03a1bb9096a15d462f27e9b5d4",
        "audit_date": "2026-08-03",
        "auditor": "Antigravity AI Agent",
        "task_id": "ce113_q11_rationalize_denominator",
        "condition": "ab2d_full",
        "seeds": [2026071301, 2026072001, 2026072002, 2026072003, 2026072004],
        "verdict": "CONFIRMED_MODEL_MISINTERPRETATION",
        "final_classification": "MODEL_MISINTERPRETATION"
    },
    "prompt_audit": {
        "prompt_file": "docs/experiments/prompts/ab2d_full/prompts/ce113_q11_rationalize_denominator.txt",
        "prompt_error": False,
        "processing_steps": [
            "1) Interpret the frozen denominator as (denom_rational) + (denom_radical_coeff)*sqrt(radicand); call RadicalOps.rationalize_linear_denominator(numerator, denom_rational, denom_radical_coeff, radicand).",
            "2) RadicalOps.exact_integer on both returned coefficients.",
            "3) Native int add of those coefficients.",
            "4) Assemble correct_answer exactly according to the Answer contract."
        ],
        "analysis": "Processing steps explicitly state: 'call RadicalOps.rationalize_linear_denominator' and apply 'RadicalOps.exact_integer on both returned coefficients'. No step implies or suggests dividing by the 3rd return value r."
    },
    "api_documentation_audit": {
        "api_name": "RadicalOps.rationalize_linear_denominator",
        "docstring": "化簡 numerator / (a + b√r)，傳回 (a_out, b_out, r) 使得結果 = a_out + b_out√r。",
        "signature": "(numerator, denom_rational, denom_radical_coeff, radicand)",
        "return_type": "tuple[int | Fraction, int | Fraction, int]",
        "return_semantics": {
            "elem_1": "a_out: rational term coefficient (Fraction/int)",
            "elem_2": "b_out: radical term coefficient (Fraction/int)",
            "elem_3": "r: radicand (int)"
        },
        "documentation_error": False,
        "analysis": "Docstring and menu unambiguously state that a_out and b_out are already the final simplified coefficients a and b of a + b√r."
    },
    "api_implementation_audit": {
        "implementation_file": "core/prompts/domain_function_library.py",
        "implementation_error": False,
        "zero_model_local_call": {
            "input": {"numerator": 9, "denom_rational": 4, "denom_radical_coeff": -1, "radicand": 7},
            "output": [
                {"value": "Fraction(4, 1)", "type": "Fraction"},
                {"value": "Fraction(1, 1)", "type": "Fraction"},
                {"value": 7, "type": "int"}
            ],
            "exact_integer_a": 4,
            "exact_integer_b": 1,
            "sum": 5
        },
        "analysis": "Implementation strictly matches documentation and mathematical definition. Calling exact_integer on a_out (Fraction(4, 1)) and b_out (Fraction(1, 1)) yields 4 and 1, producing sum = 5."
    },
    "evaluator_parameter_binding_audit": {
        "frozen_params": {"denominator": "4-sqrt(7)", "numerator": 9, "radicand": 7},
        "ground_truth_answer": 5,
        "binding_error": False,
        "domain_menu_pass_analysis": {
            "domain_menu_outcome": "5 / 5 PASS",
            "explanation": "In ab2d_domain_menu condition, Gemini wrote defensive code: 'if val3 == 7: a = exact_integer(val1); b = exact_integer(val2)'. Because val3 equaled 7 (the radicand), it bypassed division and passed 5/5. In ab2d_full condition, Gemini unconditionally assigned 'common_denom = val3' and performed '/ common_denom', causing ValueError."
        }
    },
    "five_cell_forensics": [
        {
            "cell_id": "gemini__ce113_q11_rationalize_denominator__ab2d_full__seed_2026071301",
            "seed": 2026071301,
            "outcome": "runtime_failure",
            "erroneous_code_lines": [
                "num_rational, num_radical_coeff, common_denom = RadicalOps.rationalize_linear_denominator(numerator, denom_rational, denom_radical_coeff, radicand)",
                "a_frac = Fraction(num_rational) / common_denom",
                "b_frac = Fraction(num_radical_coeff) / common_denom",
                "a = RadicalOps.exact_integer(a_frac)",
                "b = RadicalOps.exact_integer(b_frac)"
            ],
            "exception_raised": "ValueError: exact_integer requires an integral Fraction (got 4/7)"
        },
        {
            "cell_id": "gemini__ce113_q11_rationalize_denominator__ab2d_full__seed_2026072001",
            "seed": 2026072001,
            "outcome": "runtime_failure",
            "erroneous_code_lines": [
                "num_rational, num_radical_coeff, common_denom = RadicalOps.rationalize_linear_denominator(numerator, denom_rational, denom_radical_coeff, radicand)",
                "a_frac = Fraction(num_rational) / common_denom",
                "b_frac = Fraction(num_radical_coeff) / common_denom",
                "a = RadicalOps.exact_integer(a_frac)",
                "b = RadicalOps.exact_integer(b_frac)"
            ],
            "exception_raised": "ValueError: exact_integer requires an integral Fraction (got 4/7)"
        },
        {
            "cell_id": "gemini__ce113_q11_rationalize_denominator__ab2d_full__seed_2026072002",
            "seed": 2026072002,
            "outcome": "runtime_failure",
            "erroneous_code_lines": [
                "num_rational, num_radical_coeff, common_denom = RadicalOps.rationalize_linear_denominator(numerator, denom_rational, denom_radical_coeff, radicand)",
                "a_frac = Fraction(num_rational) / common_denom",
                "b_frac = Fraction(num_radical_coeff) / common_denom",
                "a = RadicalOps.exact_integer(a_frac)",
                "b = RadicalOps.exact_integer(b_frac)"
            ],
            "exception_raised": "ValueError: exact_integer requires an integral Fraction (got 4/7)"
        },
        {
            "cell_id": "gemini__ce113_q11_rationalize_denominator__ab2d_full__seed_2026072003",
            "seed": 2026072003,
            "outcome": "runtime_failure",
            "erroneous_code_lines": [
                "num_rational, num_radical_coeff, common_denom = RadicalOps.rationalize_linear_denominator(numerator, denom_rational, denom_radical_coeff, radicand)",
                "a_frac = Fraction(num_rational) / common_denom",
                "b_frac = Fraction(num_radical_coeff) / common_denom",
                "a = RadicalOps.exact_integer(a_frac)",
                "b = RadicalOps.exact_integer(b_frac)"
            ],
            "exception_raised": "ValueError: exact_integer requires an integral Fraction (got 4/7)"
        },
        {
            "cell_id": "gemini__ce113_q11_rationalize_denominator__ab2d_full__seed_2026072004",
            "seed": 2026072004,
            "outcome": "runtime_failure",
            "erroneous_code_lines": [
                "num_rational, num_radical_coeff, common_denom = RadicalOps.rationalize_linear_denominator(numerator, denom_rational, denom_radical_coeff, radicand)",
                "a_frac = Fraction(num_rational) / common_denom",
                "b_frac = Fraction(num_radical_coeff) / common_denom",
                "a = RadicalOps.exact_integer(a_frac)",
                "b = RadicalOps.exact_integer(b_frac)"
            ],
            "exception_raised": "ValueError: exact_integer requires an integral Fraction (got 4/7)"
        }
    ],
    "rerun_recommendation": {
        "requires_rerun": False,
        "affected_cells": []
    }
}

json_path = Path("docs/experiments/results/Math16/math16_gemini_full_rationalize_5cell_forensic_v1.json")
json_path.parent.mkdir(parents=True, exist_ok=True)
json_path.write_text(json.dumps(audit_data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("Wrote JSON:", json_path)

# Build Markdown artifact
md_lines = [
    "# Math16 Gemini Full-Plan Rationalize Denominator 5-Cell Forensic Audit Report (v1)",
    "",
    "**Commit**: `f0fbf4a0c2131f03a1bb9096a15d462f27e9b5d4`  ",
    "**Date**: 2026-08-03  ",
    "**Target Task**: `ce113_q11_rationalize_denominator` (Condition: `ab2d_full`)  ",
    "**Target Seeds**: `2026071301`, `2026072001`, `2026072002`, `2026072003`, `2026072004`  ",
    "**Auditor**: Antigravity AI Agent  ",
    "**Verdict**: **CONFIRMED_MODEL_MISINTERPRETATION**  ",
    "**Final Classification**: **`MODEL_MISINTERPRETATION`**  ",
    "",
    "---",
    "",
    "## 1. Executive Summary",
    "",
    "This audit performed a deep forensic investigation into the 5 `runtime_failure` cells of Gemini 3.5 Flash under `ab2d_full` condition for task `ce113_q11_rationalize_denominator`. The objective was to isolate whether the failure was caused by Prompt flaws, API documentation defects, API implementation errors, parameter binding issues, or model misinterpretation.",
    "",
    "### Key Findings:",
    "1. **Prompt Check**: PASS. Full-plan processing steps explicitly directed calling `RadicalOps.rationalize_linear_denominator(numerator, denom_rational, denom_radical_coeff, radicand)` and applying `RadicalOps.exact_integer` directly to the returned coefficients. No step suggested or implied dividing by the 3rd return value.",
    "2. **API Documentation Check**: PASS. Docstring and menu explicitly define the return tuple as `(a_out, b_out, r)` where `a_out` and `b_out` are already the final simplified coefficients $a$ and $b$ of $a + b\\sqrt{r}$, and `r` is the radicand.",
    "3. **API Implementation Check**: PASS. Zero-model local execution with frozen params `(9, 4, -1, 7)` returns `(Fraction(4, 1), Fraction(1, 1), 7)`. Calling `exact_integer` on `Fraction(4, 1)` and `Fraction(1, 1)` yields `4` and `1`, whose sum is `5` (exact ground truth).",
    "4. **Parameter Binding Check**: PASS. Evaluator passed frozen parameters and evaluated ground truth answer `5` correctly. Under `ab2d_domain_menu`, Gemini passed 5/5 using the exact same API and parameters.",
    "5. **Five-Cell Forensics**: In all 5 cells, Gemini generated **100% byte-identical code** that misidentified the 3rd return tuple element `r = 7` as `common_denom`, performed `Fraction(num_rational) / common_denom` (getting `4/7`), causing `RadicalOps.exact_integer` to fail with `ValueError: exact_integer requires an integral Fraction (got 4/7)`.",
    "6. **Why domain-menu Passed 5/5**: In `ab2d_domain_menu`, Gemini wrote defensive code `if val3 == 7:` to check if `val3` was the radicand. Seeing `val3 == 7`, it bypassed division and called `exact_integer` directly, passing 5/5. In `ab2d_full`, Gemini strictly mapped the 3 tuple returns to `(num_rational, num_radical_coeff, common_denom)` and executed the extra division.",
    "",
    "---",
    "",
    "## 2. Itemized Audit Components",
    "",
    "### Component 1: Prompt Audit",
    "- **Processing Steps File**: `docs/experiments/prompts/ab2d_full/prompts/ce113_q11_rationalize_denominator.txt`",
    "- **Processing Steps Text**:",
    "  ```text",
    "  1) Interpret the frozen denominator as (denom_rational) + (denom_radical_coeff)*sqrt(radicand); call RadicalOps.rationalize_linear_denominator(numerator, denom_rational, denom_radical_coeff, radicand).",
    "  2) RadicalOps.exact_integer on both returned coefficients.",
    "  3) Native int add of those coefficients.",
    "  4) Assemble correct_answer exactly according to the Answer contract.",
    "  ```",
    "- **Prompt Audit Verdict**: **PASS (Prompt is 100% correct)**.",
    "",
    "### Component 2: API Documentation Audit",
    "- **API Menu Entry**: `- RadicalOps.rationalize_linear_denominator | signature: (numerator, denom_rational, denom_radical_coeff, radicand) | returns: tuple[int | Fraction, int | Fraction, int]`",
    "- **Docstring**: `化簡 numerator / (a + b√r)，傳回 (a_out, b_out, r) 使得結果 = a_out + b_out√r。`",
    "- **API Doc Verdict**: **PASS (API Documentation is 100% correct)**.",
    "",
    "### Component 3: API Implementation Audit",
    "- **Local Zero-Model Test**:",
    "  ```python",
    "   RadicalOps.rationalize_linear_denominator(9, 4, -1, 7)",
    "   # -> (Fraction(4, 1), Fraction(1, 1), 7)",
    "   a = RadicalOps.exact_integer(Fraction(4, 1))  # 4",
    "   b = RadicalOps.exact_integer(Fraction(1, 1))  # 1",
    "   a + b  # 5",
    "  ```",
    "- **API Implementation Verdict**: **PASS (API Implementation is 100% correct)**.",
    "",
    "### Component 4: Evaluator & Parameter Binding Audit",
    "- **Frozen Params**: `{\"denominator\": \"4-sqrt(7)\", \"numerator\": 9, \"radicand\": 7}`",
    "- **Evaluator Ground Truth Answer**: `5`",
    "- **Domain-Menu Outcome**: `5 / 5 PASS`",
    "- **Evaluator Verdict**: **PASS (Evaluator and Binding are 100% correct)**.",
    "",
    "### Component 5: Five-Cell Code Forensics",
    "Across all 5 cells (`2026071301`, `2026072001`, `2026072002`, `2026072003`, `2026072004`), the extracted Python source and raw response are **100% byte-identical**.",
    "",
    "```python",
    "# Common Erroneous Code Generated across all 5 cells:",
    "num_rational, num_radical_coeff, common_denom = RadicalOps.rationalize_linear_denominator(",
    "    numerator, denom_rational, denom_radical_coeff, radicand",
    ")",
    "",
    "# Erroneous extra division:",
    "a_frac = Fraction(num_rational) / common_denom",
    "b_frac = Fraction(num_radical_coeff) / common_denom",
    "",
    "# Triggered ValueError:",
    "a = RadicalOps.exact_integer(a_frac)  # ValueError: exact_integer requires an integral Fraction (got 4/7)",
    "b = RadicalOps.exact_integer(b_frac)",
    "```",
    "",
    "---",
    "",
    "## 3. Final Classification & Recommendation",
    "",
    "| Category Choice | Status | Reason |",
    "|---|---|---|",
    "| `PROMPT_STEP_DEFECT` | Rejected | Prompt steps are accurate and explicit. |",
    "| `API_DOCUMENTATION_DEFECT` | Rejected | API docstring states return is `(a_out, b_out, r)` for `a_out + b_out√r`. |",
    "| `API_IMPLEMENTATION_DEFECT` | Rejected | Local zero-model call produces correct result `(4, 1, 7)` and sum `5`. |",
    "| `PARAMETER_BINDING_DEFECT` | Rejected | Evaluator binding is exact; domain-menu passed 5/5. |",
    "| **`MODEL_MISINTERPRETATION`** | **SELECTED** | Model misread tuple elements and inserted invalid `/ common_denom` division. |",
    "| `UNRESOLVED` | Rejected | Empirical cause is 100% verified. |",
    "",
    "- **Usability Determination**: `VALID_AS_MODEL_RESULT`",
    "- **Rerun Required**: **NO (0 cells to rerun)**",
    "- **Unresolved Evidence Gaps**: **None**"
]

md_path = Path("docs/experiments/results/Math16/math16_gemini_full_rationalize_5cell_forensic_v1.md")
md_path.parent.mkdir(parents=True, exist_ok=True)
md_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
print("Wrote MD:", md_path)
