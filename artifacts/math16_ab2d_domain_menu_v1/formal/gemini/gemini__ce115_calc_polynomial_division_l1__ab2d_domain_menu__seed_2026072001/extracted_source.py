from core.prompts.domain_function_library import PolynomialOps
from fractions import Fraction

def generate(level=1, **kwargs):
    oracle_payload = {
        "dividend_coefficients": [6, 0, 6],
        "divisor_coefficients": [1, -4]
    }
    
    dividend = oracle_payload["dividend_coefficients"]
    divisor = oracle_payload["divisor_coefficients"]
    
    q, r = PolynomialOps.div_qr(dividend, divisor)
    
    # Convert to numeric for format_latex
    def to_numeric(coeffs):
        res = []
        for x in coeffs:
            if isinstance(x, str):
                if '/' in x:
                    res.append(Fraction(x))
                else:
                    res.append(int(x))
            else:
                res.append(x)
        return res

    q_num = to_numeric(q)
    r_num = to_numeric(r)
    
    quotient_latex = PolynomialOps.format_latex(q_num)
    remainder_latex = PolynomialOps.format_latex(r_num)
    
    question_text = "將多項式\n\\[\n6x^2+6\n\\]\n除以\n\\[\nx-4,\n\\]\n求商式與餘式。"
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "quotient_coefficients": q,
            "remainder_coefficients": r,
            "quotient_latex": quotient_latex,
            "remainder_latex": remainder_latex
        },
        "oracle_payload": oracle_payload
    }
