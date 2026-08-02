from core.prompts.domain_function_library import PolynomialOps

def generate(level=1, **kwargs):
    frozen_params = {
        "dividend_coefficients": [
            6,
            0,
            6
        ],
        "divisor_coefficients": [
            1,
            -4
        ]
    }
    
    dividend = frozen_params["dividend_coefficients"]
    divisor = frozen_params["divisor_coefficients"]
    
    q, r = PolynomialOps.div_qr(dividend, divisor)
    
    q_latex = PolynomialOps.format_latex(q)
    r_latex = PolynomialOps.format_latex(r)
    
    question_text = "將多項式\n\\[\n6x^2+6\n\\]\n除以\n\\[\nx-4,\n\\]\n求商式與餘式。"
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "quotient_coefficients": q,
            "remainder_coefficients": r,
            "quotient_latex": q_latex,
            "remainder_latex": r_latex
        },
        "oracle_payload": frozen_params
    }