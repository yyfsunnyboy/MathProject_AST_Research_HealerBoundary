# -*- coding: utf-8 -*-
from core.prompts.domain_function_library import PolynomialOps

def generate(level=1, **kwargs):
    # Frozen sampled parameters as per task specification
    dividend_coefficients = [6, 4, 0]
    divisor_coefficients = [2, 0, 0]

    # Perform polynomial division to get quotient and remainder coefficients
    _, remainder_coeffs = PolynomialOps.div_qr(dividend_coefficients, divisor_coeffices)

    # Format the remainder into canonical LaTeX string using format_latex
    # Note: The API signature expects 'var' argument. Default is 'x'.
    latex_remainder = PolynomialOps.format_latex(remainder_coeffs, var='x')

    return {
        "question_text": r"Find the remainder when $6x^2 + 4$ is divided by $2x^3$. Express your answer in canonical LaTeX format.",
        "correct_answer": latex_remainder,
        "oracle_payload": {"dividend_coefficients": [6, 4, 0], "divisor_coefficients": [2, 0, 0]}
    }