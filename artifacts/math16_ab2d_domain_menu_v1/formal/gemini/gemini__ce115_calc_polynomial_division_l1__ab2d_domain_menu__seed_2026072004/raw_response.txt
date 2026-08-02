from core.prompts.domain_function_library import PolynomialOps

def generate(level=1, **kwargs):
    dividend = [6, 0, 6]
    divisor = [1, -4]
    
    q, r = PolynomialOps.div_qr(dividend, divisor)
    
    # Convert coefficients to integers for format_latex
    q_num = [int(x) for x in q]
    r_num = [int(x) for x in r]
    
    q_latex = PolynomialOps.format_latex(q_num)
    r_latex = PolynomialOps.format_latex(r_num)
    
    question_text = "將多項式\n\\[\n6x^2+6\n\\]\n除以\n\\[\nx-4,\n\\]\n求商式與餘式。"
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "quotient_coefficients": q,
            "remainder_coefficients": r,
            "quotient_latex": q_latex,
            "remainder_latex": r_latex
        },
        "oracle_payload": {
            "dividend_coefficients": dividend,
            "divisor_coefficients": divisor
        }
    }