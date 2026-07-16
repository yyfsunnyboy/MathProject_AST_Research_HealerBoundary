def generate(level=1, **kwargs):
    frozen_params = {"dividend_coefficients": [6, 0, 6], "divisor_coefficients": [1, -4]}
    
    from core.prompts.domain_function_library import PolynomialOps
    
    dividend_coeffs = frozen_params["dividend_coefficients"]
    divisor_coeffs = frozen_params["divisor_coefficients"]
    
    quotient_coeffs, remainder_coeffs = PolynomialOps.div_qr(dividend_coeffs, divisor_coeffs)
    
    correct_answer = {
        "quotient_coefficients": quotient_coeffs,
        "remainder_coefficients": remainder_coeffs
    }
    
    return {
        "question_text": f"Divide the polynomial with coefficients {dividend_coeffs} by the polynomial with coefficients {divisor_coeffs}.",
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }