def generate(level=1, **kwargs):
    dividend_coeffs = [6, 0, 6]
    divisor_coeffs = [1, -4]
    
    # Perform polynomial division: (6x^2 + 6) / (x - 4)
    # Step 1: Leading term of dividend is 6x^2. Divide by x -> 6x.
    # Subtract 6x * (x - 4) = 6x^2 - 24x from (6x^2 + 0x + 6).
    # New remainder part: 24x + 6.
    
    # Step 2: Leading term of new remainder is 24x. Divide by x -> 24.
    # Subtract 24 * (x - 4) = 24x - 96 from (24x + 6).
    # Final remainder part: 102.
    
    quotient_coefficients = [int(6), int(24)] 
    remainder_coefficients = [int(102)] 
    
    question_text = r"Divide the polynomial \( 6x^2 + 6 \) by \( x - 4 \). Express your answer as a quotient and a remainder."
    
    correct_answer_dict = {
        "quotient_coefficients": quotient_coefficients,
        "remainder_coefficients": remainder_coefficients,
        "quotient_latex": "\\left( 6x + 24 \\right)",
        "remainder_latex": "\\text{102}"
    }

    oracle_payload = {
        "dividend_coefficients": dividend_coeffs,
        "divisor_coefficients": divisor_coeffs
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer_dict,
        "oracle_payload": oracle_payload
    }
