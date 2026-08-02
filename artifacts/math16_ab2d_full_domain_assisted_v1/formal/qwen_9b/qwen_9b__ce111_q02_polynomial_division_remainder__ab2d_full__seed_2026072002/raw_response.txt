from core.prompts.domain_function_library import PolynomialOps

def generate(level=1, **kwargs):
    dividend = [6, 4, 0]
    divisor = [2, 0, 0]
    
    q, r = PolynomialOps.div_qr(dividend, divisor)
    
    remainder_latex = PolynomialOps.format_latex(r) if len(r) > 1 else "0"
    
    return {
        "question_text": "計算多項式 \(6x^2+4x\) 除以 \(2x^2\) 所得的餘式。",
        "correct_answer": {"remainder": remainder_latex, "canonical_latex": remainder_latex},
        "oracle_payload": {
            "dividend_coefficients": [6, 4, 0],
            "divisor_coefficients": [2, 0, 0]
        }
    }