from core.prompts.domain_function_library import PolynomialOps
from fractions import Fraction

def generate(level=1, **kwargs):
    frozen_params = {
        "dividend_coefficients": [6, 4, 0],
        "divisor_coefficients": [2, 0, 0]
    }
    
    dividend = frozen_params["dividend_coefficients"]
    divisor = frozen_params["divisor_coefficients"]
    
    q, r = PolynomialOps.div_qr(dividend, divisor)
    
    # Convert remainder coefficients to numeric types (int or Fraction)
    r_numeric = []
    for x in r:
        if isinstance(x, str):
            if '/' in x:
                r_numeric.append(Fraction(x))
            else:
                r_numeric.append(int(x))
        else:
            r_numeric.append(x)
            
    r_normalized = PolynomialOps.normalize(r_numeric)
    remainder_latex = PolynomialOps.format_latex(r_normalized)
    
    return {
        "question_text": "計算多項式 \\(6x^2+4x\\) 除以 \\(2x^2\\) 所得的餘式。",
        "correct_answer": {
            "remainder": remainder_latex,
            "canonical_latex": remainder_latex
        },
        "oracle_payload": frozen_params
    }