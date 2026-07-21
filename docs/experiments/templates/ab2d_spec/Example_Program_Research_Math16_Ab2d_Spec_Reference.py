# -*- coding: utf-8 -*-
"""
Example Program Research Math16 Ab2d Spec Reference
==================================================
Researcher-facing reference only.
Do not inject this file verbatim into model prompts.

This is a researcher-facing reference template demonstrating the standard data flow
and execution contract for Ab2d+spec. It highlights the expected steps to generate a
question program using frozen parameters, local computation, and returning the exact contract.
"""

def generate(level=1, **kwargs):
    # 1. Define frozen parameters directly.
    # Do not read frozen parameters from kwargs or external state.
    # (In actual prompt injection, these are hardcoded values from frozen evidence)
    # frozen_param_a = 12
    # frozen_param_b = 34

    # 2. Compute the exact result.
    # Use native Python computation or designated compact scaffold APIs (if allowed).
    # For Integer Pilot-02 tasks, this must use native Python arithmetic and structures only.
    # (Do not call external APIs, database, or domain classes unless allowed by spec policy)

    # 3. Build the required correct_answer type.
    # The correct_answer must adhere exactly to the expected schema (e.g. integer, list).
    # correct_answer = ...

    # 4. Render question_text after computation.
    # Interpolate the frozen parameters into the required LaTeX or text format.
    # question_text = ...

    # 5. Preserve frozen parameters.
    # The oracle_payload must contain the exact parameter mapping that was frozen.
    # oracle_payload = {
    #     "param_a": frozen_param_a,
    #     "param_b": frozen_param_b,
    # }

    # 6. Return the exact contract.
    return {
        "question_text": "question_text",
        "correct_answer": "correct_answer",
        "oracle_payload": "oracle_payload",
    }
