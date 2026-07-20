import math

from core.prompts.domain_function_library import PolynomialOps


def generate(level=1, **kwargs):
    frozen_params = {"dividend_coefficients": [6, 4, 0], "divisor_coefficients": [2, 0, 0]}
    
    quotient_coeffs, remainder_coeffs = PolynomialOps.div_qr(
        dividend_coefficients=frozen_params["dividend_coefficients"], 
        divisor_coefficients=frozen_params["divisor_coefficients"]
    )
    
    latex_quotient = PolynomialOps.format_latex(coeffs=quotient_coeffs)
    latex_remainder = PolynomialOps.format_latex(coeffs=remainder_coeffs)
    
    question_text = (r"Given the polynomial $P(x)$ with coefficients $(6, 4, 0)$ and divisor $D(x)$ with coefficients $(2, 0, 0)$, find the remainder when $P(x)$ is divided by $D(x)$." )
    
    correct_answer_latex = latex_remainder
    
    return {
        "question_text": question_text, 
        "correct_answer": {"remainder": correct_answer_latex},
        "oracle_payload": frozen_params
    }