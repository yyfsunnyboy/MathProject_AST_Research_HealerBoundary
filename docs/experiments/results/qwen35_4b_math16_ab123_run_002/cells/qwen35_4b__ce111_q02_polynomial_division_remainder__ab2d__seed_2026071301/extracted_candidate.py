import sys
sys.path.insert(0, '.')
from core.prompts.domain_function_library import PolynomialOps

def generate(level=1, **kwargs):
    frozen_params = {"dividend_coefficients": [6, 4, 0], "divisor_coefficients": [2, 0, 0]}
    
    dividend_coeffs = frozen_params["dividend_coefficients"]
    divisor_coeffs = frozen_params["divisor_coefficients"]
    
    quotient, remainder = PolynomialOps.div_qr(dividend_coeffs, divisor_coeffs)
    
    latex_dividend = PolynomialOps.format_latex(dividend_coeffs)
    latex_divisor = PolynomialOps.format_latex(divisor_coeffs)
    latex_remainder = PolynomialOps.format_latex(remainder)
    
    question_text = r"""Perform polynomial division of $6x^2 + 4$ by $2$. Find the remainder."""
    
    correct_answer = f"{latex_remainder}"
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }