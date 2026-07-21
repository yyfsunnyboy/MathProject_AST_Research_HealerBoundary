# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen parameters as per task specification
    frozen_params = {"dividend_coefficients": [6, 4, 0], "divisor_coefficients": [2, 0, 0]}
    
    from core.prompts.domain_function_library import PolynomialOps
    
    dividend_coeffs = frozen_params["dividend_coefficients"]
    divisor_coeffs = frozen_params["divisor_coefficients"]
    
    # Perform polynomial division to get quotient and remainder
    _, remainder = PolynomialOps.div_qr(dividend_coeffs, divisor_coeffs)
    
    # Format the remainder as LaTeX using the specified API signature (coeffs, var='x')
    canonical_latex = PolynomialOps.format_latex(remainder, var='x')
    
    question_text = r"\text{Find the remainder when } P(x)=6+4x+x^2 \text{ is divided by } Q(x)=2."
    
    correct_answer = {
        "remainder": [0],  # Remainder coefficients (constant polynomial)
        "canonical_latex": canonical_latex
    }
    
    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }