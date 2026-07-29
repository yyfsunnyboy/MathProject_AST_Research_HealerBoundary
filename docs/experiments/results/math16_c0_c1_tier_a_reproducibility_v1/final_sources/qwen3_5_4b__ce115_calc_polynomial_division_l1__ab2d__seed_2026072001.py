def generate(level=1, **kwargs):
    from core.prompts.domain_function_library import PolynomialOps
    
    frozen_params = {"dividend_coefficients": [6, 0, 6], "divisor_coefficients": [1, -4]}
    
    dividend_coeffs = frozen_params["dividend_coefficients"]
    divisor_coeffs = frozen_params["divisor_coefficients"]
    
    quotient, remainder = PolynomialOps.div_qr(dividend_coeffs, divisor_coeffs)
    
    question_text = r"""Perform polynomial division of \( 6x^2 + 0x + 6 \) by \( x - 4 \). Find the quotient and remainder."""
    
    correct_answer = {
        "quotient_coefficients": quotient[0],
        "remainder_coefficients": remainder[0],
        "quotient_latex": r"\( 6x + 18 \)",
        "remainder_latex": r"\( -30 \)"
    }
    
    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }