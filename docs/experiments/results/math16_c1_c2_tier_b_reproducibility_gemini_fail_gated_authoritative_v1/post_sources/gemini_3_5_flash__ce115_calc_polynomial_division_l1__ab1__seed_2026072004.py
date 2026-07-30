def generate(level=1, **kwargs):
    dividend_coefficients = [6, 0, 6]
    divisor_coefficients = [1, -4]
    
    quotient_coefficients = [6, 24]
    remainder_coefficients = [102]
    
    dividend_latex = "6x^2 + 6"
    divisor_latex = "x - 4"
    quotient_latex = "6x + 24"
    remainder_latex = "102"
    
    question_text = f"Divide the polynomial \\( {dividend_latex} \\) by \\( {divisor_latex} \\). Find the quotient and the remainder."
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "quotient_coefficients": quotient_coefficients,
            "remainder_coefficients": remainder_coefficients,
            "quotient_latex": quotient_latex,
            "remainder_latex": remainder_latex
        },
        "oracle_payload": {
            "dividend_coefficients": dividend_coefficients,
            "divisor_coefficients": divisor_coefficients
        }
    }