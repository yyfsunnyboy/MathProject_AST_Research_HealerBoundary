from core.prompts.domain_function_library import PolynomialOps

def generate(level=1, **kwargs):
    dividend = [6, 4, 0]
    divisor = [2, 0, 0]
    
    quotient, remainder_coeffs = PolynomialOps.div_qr(dividend, divisor)
    
    # The API returns coefficients highest degree first. 
    # We need to format the LaTeX for this list directly.
    remainder_latex = PolynomialOps.format_latex(remainder_coeffs)
    
    return {
        "question_text": "計算多項式 \(6x^2+4x\) 除以 \(2x^2\) 所得的餘式。",
        "correct_answer": {
            "remainder": remainder_latex,
            "canonical_latex": remainder_latex
        },
        "oracle_payload": {
            "dividend_coefficients": [6, 4, 0],
            "divisor_coefficients": [2, 0, 0]
        }
    }