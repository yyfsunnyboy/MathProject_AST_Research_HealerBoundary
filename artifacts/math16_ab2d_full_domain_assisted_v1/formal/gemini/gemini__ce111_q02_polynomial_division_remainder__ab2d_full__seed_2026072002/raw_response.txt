from core.prompts.domain_function_library import PolynomialOps
from fractions import Fraction

def generate(level=1, **kwargs):
    oracle_payload = {
      "dividend_coefficients": [
        6,
        4,
        0
      ],
      "divisor_coefficients": [
        2,
        0,
        0
      ]
    }
    
    dividend = oracle_payload["dividend_coefficients"]
    divisor = oracle_payload["divisor_coefficients"]
    
    q, r = PolynomialOps.div_qr(dividend, divisor)
    
    # Convert r to numeric for format_latex
    r_numeric = []
    for c in r:
        if isinstance(c, (int, float)):
            r_numeric.append(c)
        elif isinstance(c, str):
            if '/' in c:
                r_numeric.append(Fraction(c))
            else:
                r_numeric.append(int(c))
                
    r_latex = PolynomialOps.format_latex(r_numeric)
    
    return {
        "question_text": "計算多項式 \(6x^2+4x\) 除以 \(2x^2\) 所得的餘式。",
        "correct_answer": {
            "remainder": r_latex,
            "canonical_latex": r_latex
        },
        "oracle_payload": oracle_payload
    }