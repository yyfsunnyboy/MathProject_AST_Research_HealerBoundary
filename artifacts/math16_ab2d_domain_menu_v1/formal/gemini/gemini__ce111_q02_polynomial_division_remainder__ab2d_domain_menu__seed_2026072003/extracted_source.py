from core.prompts.domain_function_library import PolynomialOps

def generate(level=1, **kwargs):
    frozen_params = {
        "dividend_coefficients": [6, 4, 0],
        "divisor_coefficients": [2, 0, 0]
    }
    
    dividend = frozen_params["dividend_coefficients"]
    divisor = frozen_params["divisor_coefficients"]
    
    q, r = PolynomialOps.div_qr(dividend, divisor)
    
    # Normalize remainder to remove leading zeros if any
    r_normalized = PolynomialOps.normalize(r)
    
    remainder_latex = PolynomialOps.format_latex(r_normalized)
    
    return {
        "question_text": "計算多項式 \\(6x^2+4x\\) 除以 \\(2x^2\\) 所得的餘式。",
        "correct_answer": {
            "remainder": remainder_latex,
            "canonical_latex": remainder_latex
        },
        "oracle_payload": frozen_params
    }