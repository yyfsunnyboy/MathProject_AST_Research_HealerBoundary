from core.prompts.domain_function_library import PolynomialOps

def generate(level=1, **kwargs):
    frozen_params = {
        "dividend_coefficients": [6, 4, 0],
        "divisor_coefficients": [2, 0, 0]
    }
    
    dividend = frozen_params["dividend_coefficients"]
    divisor = frozen_params["divisor_coefficients"]
    
    q, r = PolynomialOps.div_qr(dividend, divisor)
    
    # Convert remainder coefficients to numeric for formatting
    r_numeric = []
    for coeff in r:
        if isinstance(coeff, str):
            if '/' in coeff:
                from fractions import Fraction
                r_numeric.append(Fraction(coeff))
            else:
                r_numeric.append(int(coeff))
        else:
            r_numeric.append(coeff)
            
    # Normalize remainder to remove leading zeros
    r_normalized = PolynomialOps.normalize(r_numeric)
    
    remainder_latex = PolynomialOps.format_latex(r_normalized)
    
    question_text = r"計算多項式 \(6x^2+4x\) 除以 \(2x^2\) 所得的餘式。"
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "remainder": remainder_latex,
            "canonical_latex": remainder_latex
        },
        "oracle_payload": frozen_params
    }