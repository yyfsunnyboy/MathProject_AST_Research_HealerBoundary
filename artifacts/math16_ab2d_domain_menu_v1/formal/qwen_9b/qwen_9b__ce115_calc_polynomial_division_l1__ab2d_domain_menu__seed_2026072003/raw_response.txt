from core.prompts.domain_function_library import PolynomialOps

def generate(level=1, **kwargs):
    frozen = {
        "dividend_coefficients": [6, 0, 6],
        "divisor_coefficients": [1, -4]
    }
    
    q, r = PolynomialOps.div_qr(
        frozen["dividend_coefficients"], 
        frozen["divisor_coefficients"]
    )
    
    return {
        "question_text": "$\\left[6x^2+6\\right]$ 除以 $\\left[x-4\\right]$,求商式與餘式。",
        "correct_answer": {
            "quotient_coefficients": q,
            "remainder_coefficients": r,
            "quotient_latex": PolynomialOps.format_latex(q),
            "remainder_latex": PolynomialOps.format_latex(r)
        },
        "oracle_payload": frozen
    }