from core.prompts.domain_function_library import PolynomialOps

def generate(level=1, **kwargs):
    dividend = [6, 0, 6]
    divisor = [1, -4]
    
    q, r = PolynomialOps.div_qr(dividend, divisor)
    
    quotient_latex = PolynomialOps.format_latex(q)
    remainder_latex = PolynomialOps.format_latex(r)
    
    return {
        "question_text": "將多項式 $6x^2+6$ 除以 $x-4,$求商式與餘式。",
        "correct_answer": {
            "quotient_coefficients": q,
            "remainder_coefficients": r,
            "quotient_latex": quotient_latex,
            "remainder_latex": remainder_latex
        },
        "oracle_payload": {"dividend_coefficients": [6, 0, 6], "divisor_coefficients": [1, -4]}
    }