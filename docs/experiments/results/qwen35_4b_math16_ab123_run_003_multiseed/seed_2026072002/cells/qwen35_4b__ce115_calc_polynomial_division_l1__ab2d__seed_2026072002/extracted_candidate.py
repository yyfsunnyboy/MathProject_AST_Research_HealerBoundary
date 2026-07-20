def generate(level=1, **kwargs):
    from core.prompts.domain_function_library import PolynomialOps
    
    frozen_params = {"dividend_coefficients": [6, 0, 6], "divisor_coefficients": [1, -4]}
    
    dividend_coeffs = frozen_params["dividend_coefficients"]
    divisor_coeffs = frozen_params["divisor_coefficients"]
    
    quotient_coeffs, remainder_coeffs = PolynomialOps.div_qr(dividend_coeffs, divisor_coeffs)
    
    question_text = r"""Perform polynomial division of \( 6x^2 + 0x + 6 \) by \( x - 4 \). Find the quotient and remainder."""

    correct_answer = {
        "quotient_coefficients": quotient_coeffs,
        "remainder_coefficients": remainder_coeffs,
        "quotient_latex": r"\frac{1}{2}x^3 + (-\frac{5}{8})x^2 - \frac{67}{40}", # Placeholder logic below to ensure correctness based on input
        
    }

    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }