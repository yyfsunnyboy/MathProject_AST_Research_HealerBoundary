def generate(level=1, **kwargs):
    dividend_coefficients = [6, 0, 6]
    divisor_coefficients = [1, -4]
    
    # Polynomial: P(x) = 6x^2 + 6 (since coeff at x is 0)
    # Divisor: D(x) = x - 4
    
    # Division: (6x^2 + 6) / (x - 4)
    # Step 1: 6x^2 / x = 6x. Multiply divisor by 6x -> 6x^2 - 24x. Subtract from dividend: (0 - (-24))x = 24x. Bring down +6. New remainder part: 24x + 6.
    # Step 2: 24x / x = 24. Multiply divisor by 24 -> 24x - 96. Subtract from (24x + 6): 6 - (-96) = 102.
    
    quotient_coefficients = [6, 24]   # Represents 6x + 24
    remainder_coefficients = [102]    # Constant term
    
    quotient_latex = r"6x+24"
    remainder_latex = r"102"
    
    return {
        "question_text": f"Divide the polynomial $\\left( \\sum_{i=0}^{n-1} a_i x^i \\right) = 6x^2 + 6$ by the divisor $D(x) = x - 4$. Find the quotient and remainder.",
        "correct_answer": {
            "quotient_coefficients": [6, 24],
            "remainder_coefficients": [102],
            "quotient_latex": r"6x+24",
            "remainder_latex": r"102"
        },
        "oracle_payload": {
            "dividend_coefficients": [6, 0, 6],
            "divisor_coefficients": [1, -4]
        }
    }