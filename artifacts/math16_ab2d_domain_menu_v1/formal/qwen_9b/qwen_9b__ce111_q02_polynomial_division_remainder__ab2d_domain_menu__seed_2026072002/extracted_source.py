from core.prompts.domain_function_library import PolynomialOps

def generate(level=1, **kwargs):
    frozen_params = {
        "dividend_coefficients": [6, 4, 0],
        "divisor_coefficients": [2, 0, 0]
    }
    
    q_coeffs, r_coeffs = PolynomialOps.div_qr(
        frozen_params["dividend_coefficients"], 
        frozen_params["divisor_coefficients"]
    )
    
    remainder_latex = PolynomialOps.format_latex(r_coeffs)
    
    return {
        "question_text": "計算多項式 \(6x^2+4x\) 除以 \(2x^2\) 所得的餘式。",
        "correct_answer": {
            "remainder": str(r_coeffs[0]) if r_coeffs else "",
            "canonical_latex": remainder_latex
        },
        "oracle_payload": frozen_params
    }