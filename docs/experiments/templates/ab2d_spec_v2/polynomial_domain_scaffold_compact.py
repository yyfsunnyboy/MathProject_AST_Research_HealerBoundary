# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Rules:
    # - Do not read frozen parameters from kwargs or external state.
    # - For API-only / mixed tasks, import and use PolynomialOps.
    # - For native-only tasks, use native Python arithmetic and lists.
    # - Do not use eval, exec, safe_eval, files, network, or fabricated helpers.
    # - Return exactly question_text, correct_answer, and oracle_payload.
    # - All returned values must be JSON-serializable.

    # 1. Import PolynomialOps if needed (only for API-only / mixed tasks)
    # from core.prompts.domain_function_library import PolynomialOps

    # 2. Define frozen parameters directly. Do not read kwargs.
    pass

    # 3. Compute the exact result using PolynomialOps or native code.
    # Example: quotient, remainder = PolynomialOps.div_qr(dividend_coefficients, divisor_coefficients)
    # Example: latex = PolynomialOps.format_latex(remainder, var='x')  # NOT to_latex
    pass

    correct_answer = "correct_answer"
    question_text = "question_text"
    oracle_payload = "oracle_payload"

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload,
    }
