# -*- coding: utf-8 -*-

from core.prompts.domain_function_library import PolynomialOps

def generate(level=1, **kwargs):
    # Frozen parameters
    dividend_coefficients = [6, 4, 0]
    divisor_coefficients = [2, 0, 0]
    
    # Perform division using PolynomialOps
    quotient, remainder = PolynomialOps.div_qr(dividend_coefficients, divisor_coefficients)
    
    # Format using PolynomialOps
    dividend_latex = PolynomialOps.to_latex(dividend_coefficients)
    divisor_latex = PolynomialOps.to_latex(divisor_coefficients)
    remainder_latex = PolynomialOps.to_latex(remainder)
    
    question_text = f"Find the remainder when the polynomial ${dividend_latex}$ is divided by ${divisor_latex}$."
    
    correct_answer = {
        "remainder": remainder,
        "canonical_latex": remainder_latex
    }
    
    oracle_payload = {
        "dividend_coefficients": dividend_coefficients,
        "divisor_coefficients": divisor_coefficients
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload,
    }