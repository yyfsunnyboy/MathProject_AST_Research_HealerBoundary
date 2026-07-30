from core.prompts.domain_function_library import PolynomialOps

def generate(level=1, **kwargs):
    dividend_coeffs = [6, 4, 0]
    divisor_coeffs = [2, 0, 0]
    
    # Calculate quotient and remainder
    quotient, remainder = PolynomialOps.div_qr(dividend_coeffs, divisor_coeffs)
    
    # Format polynomials to LaTeX
    dividend_latex = PolynomialOps.format_latex(dividend_coeffs)
    divisor_latex = PolynomialOps.format_latex(divisor_coeffs)
    remainder_latex = PolynomialOps.format_latex(remainder)
    
    question_text = f"Find the remainder when the polynomial \\({dividend_latex}\\) is divided by \\({divisor_latex}\\)."
    correct_answer = remainder_latex
    
    oracle_payload = {
        "dividend_coefficients": dividend_coeffs,
        "divisor_coefficients": divisor_coeffs
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }