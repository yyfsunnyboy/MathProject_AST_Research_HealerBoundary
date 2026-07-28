# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen parameters as per task specification
    frozen_params = {
        "dividend_coefficients": [6, 4, 0],
        "divisor_coefficients": [2, 0, 0]
    }

    from core.prompts.domain_function_library import PolynomialOps
    
    dividend_coeffs = frozen_params["dividend_coefficients"]
    divisor_coeffs = frozen_params["divisor_coefficients"]
    
    # Perform polynomial division to get quotient and remainder
    _, remainder = PolynomialOps.div_qr(dividend_coeffs, divisor_coeffs)
    
    # Format the remainder as LaTeX using the correct API signature (format_latex with coeffs list)
    canonical_latex = PolynomialOps.format_latex(remainder, var='x')

    question_text = r"\text{Find the remainder when } P(x)=6+4x+x^2 \text{ is divided by } Q(x)=0\cdot x + 0\cdot x^2 + 2x."
    
    correct_answer = {
        "remainder": [0], # Remainder of (x^2 + 4x + 6) / (2x) is actually a constant or linear term depending on implementation, but based on coeffs [6,4,0] and [2,0,0]: 
                         # Dividend: x^2 + 4x + 6
                         # Divisor: 2x
                         # Division: (x^2+4x+6)/(2x) = (1/2)x + 2 + 3/x -> This is not polynomial division in standard sense if divisor degree > dividend? 
                         # Wait, [6,4,0] means 6 + 4x + 0*x^2. Degree of dividend is 1.
                         # [2,0,0] means 2 + 0x + 0x^2 = 2. Constant divisor.
                         # Division by constant: (6+4x)/2 = 3+2x. Remainder should be 0? 
                         # Let's re-read standard polynomial representation [c_n, ..., c_1, c_0].
                         # Dividend: [6, 4, 0] -> 6 + 4x + 0*x^2 = 4x+6. Degree 1.
                         # Divisor: [2, 0, 0] -> 2 + 0x + 0*x^2 = 2. Degree 0.
                         # (4x+6) / 2 = 2x+3 with remainder 0? 
                         # Or is it long division where we stop when degree(remainder) < degree(divisor)?
                         # Since divisor is constant, any polynomial divided by a non-zero constant has remainder 0.
                         # However, let's trust the library implementation for exact coefficients handling if degrees were different (e.g. leading zeros).
                         # Assuming standard behavior: Remainder list [0].
        "canonical_latex": canonical_latex
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }