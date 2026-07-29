import sys
sys.path.insert(0, '.')
from core.prompts.domain_function_library import PolynomialOps


def generate(level=1, **kwargs):
    frozen = {"dividend_coefficients": [6, 4, 0], "divisor_coefficients": [2, 0, 0]}

    dividend_coeffs = frozen["dividend_coefficients"]
    divisor_coeffs = frozen["divisor_coefficients"]

    quotient_list, remainder_list = PolynomialOps.div_qr(dividend_coeffs, divisor_coeffs)
    
    # Format LaTeX for the question text (showing coefficients as lists or polynomials if needed)
    dividend_latex = PolynomialOps.format_latex(dividend_coeffs, var='x')
    divisor_latex = PolynomialOps.format_latex(divisor_coeffs, var='x')

    remainder_latex = PolynomialOps.format_latex(remainder_list, var='x')

    question_text = f"Find the remainder when $P(x) = {dividend_latex}$ is divided by $D(x) = {divisor_latex}$. Express your answer as a polynomial in standard form."
    
    correct_answer_dict = {
        "remainder": remainder_list, 
        "canonical_latex": f"r(x) = {remainder_latex}"
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer_dict,
        "oracle_payload": frozen
    }