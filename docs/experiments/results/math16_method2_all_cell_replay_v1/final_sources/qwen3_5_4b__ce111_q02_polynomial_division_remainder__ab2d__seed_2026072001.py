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
    
    question_text = r"\text{Find the remainder when } $6x^2 + 4$ \text{ is divided by } $2x$.}"
    
    correct_answer = {
        "remainder": [0],
        "canonical_latex": f"\\boxed{{\frac{{{latex_dividend}}}{{{latex_divisor}}}=Q(x) \\cdot ({latex_divisor}) + 0}}"
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }