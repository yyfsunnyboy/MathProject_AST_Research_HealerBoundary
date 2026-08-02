from core.prompts.domain_function_library import PolynomialOps

def generate(level=1, **kwargs):
    frozen_params = {
        "dividend_coefficients": [6, 0, 6],
        "divisor_coefficients": [1, -4]
    }
    
    quotient_coeffs, remainder_coeffs = PolynomialOps.div_qr(
        frozen_params["dividend_coefficients"], 
        frozen_params["divisor_coefficients"]
    )
    
    return {
        "question_text": r"將多項式 \(6x^2+6\) 除以 \(x-4,\) 求商式與餘式。",
        "correct_answer": {
            "quotient_coefficients": quotient_coeffs,
            "remainder_coefficients": remainder_coeffs,
            "quotient_latex": PolynomialOps.format_latex(quotient_coeffs),
            "remainder_latex": PolynomialOps.format_latex(remainder_coeffs)
        },
        "oracle_payload": frozen_params
    }