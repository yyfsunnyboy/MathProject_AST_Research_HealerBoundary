from core.prompts.domain_function_library import PolynomialOps

def generate(level=1, **kwargs):
    dividend = [6, 0, 6]
    divisor = [1, -4]
    
    q_coefficients, r_coefficients = PolynomialOps.div_qr(dividend, divisor)
    
    quotient_latex = PolynomialOps.format_latex(q_coefficients)
    remainder_latex = PolynomialOps.format_latex(r_coefficients)
    
    return {
        "question_text": "$\\left(6x^2+6\\right)$ 除以 $\\left(x-4\\right)$，求商式與餘式。",
        "correct_answer": {
            "quotient_coefficients": q_coefficients,
            "remainder_coefficients": r_coefficients,
            "quotient_latex": quotient_latex,
            "remainder_latex": remainder_latex
        },
        "oracle_payload": {
          "dividend_coefficients": [6, 0, 6],
          "divisor_coefficients": [1, -4]
        }
    }