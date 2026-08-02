from core.prompts.domain_function_library import PolynomialOps, Fraction

def generate(level=1, **kwargs):
    dividend = [6, 0, 6]
    divisor = [1, -4]
    
    q_coeffs, r_coeffs = PolynomialOps.div_qr(dividend, divisor)
    
    quotient_latex = PolynomialOps.format_latex(q_coeffs)
    remainder_latex = PolynomialOps.format_latex(r_coeffs)
    
    return {
        "question_text": "將多項式\n\\[\n6x^2+6\n\\]\n除以\n\\[\nx-4,\n\\]\n求商式與餘式。",
        "correct_answer": {
            "quotient_coefficients": q_coeffs,
            "remainder_coefficients": r_coeffs,
            "quotient_latex": quotient_latex,
            "remainder_latex": remainder_latex
        },
        "oracle_payload": {"dividend_coefficients": dividend, "divisor_coefficients": divisor}
    }
