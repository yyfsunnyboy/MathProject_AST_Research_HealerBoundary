# -*- coding: utf-8 -*-
from core.prompts.domain_function_library import PolynomialOps

def generate(level=1, **kwargs):
    # Frozen sampled parameters defined directly as per specification
    dividend_coefficients = [6, 4, 0]
    divisor_coefficients = [2, 0, 0]

    # Perform polynomial division to get quotient and remainder coefficients
    _, remainder_coeffs = PolynomialOps.div_qr(dividend_coefficients, divisor_coeffices)

    # Format the remainder into canonical LaTeX string using format_latex
    correct_answer = {
        "remainder": remainder_coeffs,
        "canonical_latex": PolynomialOps.format_latex(remainder_coeffs)
    }

    question_text = r"Find the remainder when $6x^2 + 4$ is divided by $2x^3$. Express your answer as a polynomial in canonical form."

    oracle_payload = {
        "dividend_coefficients": [6, 4, 0],
        "divisor_coefficients": [2, 0, 0]
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }