import sys
sys.setrecursionlimit(2000)

from core.prompts.domain_function_library import PolynomialOps


def generate(level=1, **kwargs):
    frozen_params = {"dividend_coefficients": [6, 4, 0], "divisor_coefficients": [2, 0, 0]}
    
    dividend_coeffs = frozen_params["dividend_coefficients"]
    divisor_coeffs = frozen_params["divisor_coefficients"]
    
    quotient, remainder = PolynomialOps.div_qr(dividend_coeffs, divisor_coeffs)
    
    var_name = 'x'
    latex_dividend = PolynomialOps.format_latex(dividend_coeffs, var=var_name)
    latex_remainder = PolynomialOps.format_latex(remainder, var=var_name) if len(remainder) > 0 else "0"
    
    question_text = r"\text{Find the remainder when } $P(x)=\underbrace{\sum_{i=0}^{n-1}{a_i x^i}}_{6+4x}$ \text{ is divided by } Q(x)=\underbrace{\sum_{j=0}^{m-1}{b_j x^j}}_{2}"
    
    correct_answer = f"remainder: {str(remainder[0])}, canonical_latex: \\({latex_remainder}\\)"
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params.copy()
    }