def generate(level=1, **kwargs):
    from core.prompts.domain_function_library import PolynomialOps
    
    frozen_params = {
        "dividend_coefficients": [6, 0, 6], 
        "divisor_coefficients": [1, -4]
    }
    
    dividend_coeffs = frozen_params["dividend_coefficients"]
    divisor_coeffs = frozen_params["divisor_coefficients"]
    
    quotient, remainder = PolynomialOps.div_qr(dividend_coeffs, divisor_coeffs)
    
    correct_answer = {
        "quotient_coefficients": quotient, 
        "remainder_coefficients": remainder, 
        "quotient_latex": "\\(" + str(quotient).replace(",", ", ") + "\\)", 
        "remainder_latex": "\\(" + str(remainder).replace(",", ", ") + "\\)"
    }
    
    question_text = """Compute the polynomial division of $P(x) = 6x^2 + 0x + 6$ by $D(x) = x - 4$. 
Provide the quotient coefficients and remainder coefficients using exact arithmetic.

Let:
- Dividend coefficients (descending powers): \[ [6, 0, 6] \]
- Divisor coefficients (descending powers): \[ [1, -4] \]"""
    
    return {
        "question_text": question_text, 
        "correct_answer": correct_answer, 
        "oracle_payload": frozen_params
    }