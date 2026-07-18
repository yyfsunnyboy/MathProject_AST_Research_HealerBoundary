from core.prompts.domain_function_library import PolynomialOps

def generate(level=1, **kwargs):
    dividend_coefficients = [6, 4, 0]
    divisor_coefficients = [2, 0, 0]
    
    quotient_coeffs, remainder_coeffs = PolynomialOps.div_qr(dividend_coefficients, divisor_coefficients)
    
    dividend_latex = PolynomialOps.format_latex(dividend_coefficients)
    divisor_latex = PolynomialOps.format_latex(divisor_coefficients)
    remainder_latex = PolynomialOps.format_latex(remainder_coeffs)
    
    question_text = f"Find the remainder when the polynomial ${dividend_latex}$ is divided by ${divisor_latex}$."
    correct_answer = remainder_latex
    
    oracle_payload = {
        "dividend_coefficients": dividend_coefficients,
        "divisor_coefficients": divisor_coefficients
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }