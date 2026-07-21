def generate(level=1, **kwargs):
    from core.prompts.domain_function_library import PolynomialOps
    
    frozen_params = {
        "dividend_coefficients": [6, 4, 0], 
        "divisor_coefficients": [2, 0, 0]
    }
    
    dividend_coeffs = frozen_params["dividend_coefficients"]
    divisor_coeffs = frozen_params["divisor_coefficients"]
    
    quotient, remainder = PolynomialOps.div_qr(dividend_coeffs, divisor_coeffs)
    
    if len(remainder) == 1 and remainder[0] == 0:
        latex_remainder = "0"
    else:
        coeffs_to_format = [str(c).replace('-', '\\-') for c in remainder]
        latex_remainder = PolynomialOps.format_latex(coeffs_to_format, var='x') if len(remainder) > 1 else str(int(remainder[0]))

    question_text = r"\text{Find the remainder when } P(x)=6+4x \text{ is divided by } Q(x)=2."
    
    correct_answer_dict = {
        "question": question_text, 
        "correct_remainder": int(remainder[0]) if len(remainder) == 1 else str(int(float(''.join(map(str, remainder))))) if all(isinstance(c, (int, float)) for c in remainder) else ''.join(map(str, remainder)),
        "canonical_latex": latex_remainder
    }

    return {
        "question_text": question_text, 
        "correct_answer": correct_answer_dict, 
        "oracle_payload": frozen_params
    }