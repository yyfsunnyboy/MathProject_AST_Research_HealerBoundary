def generate(level=1, **kwargs):
    dividend_coefficients = [6, 0, 6]
    divisor_coefficients = [1, -4]
    
    # Polynomial: P(x) = 6x^2 + 0x + 6 (coeffs from highest to lowest degree implied by context of division usually, but let's verify standard list format).
    # Standard Python polynomial libraries often store coeffs as [a_n, ..., a_0]. 
    # Dividend: 6x^2 + 6. Divisor: x - 4.
    # Division: (6x^2 + 6) / (x - 4) = 6x + 24 with remainder 102? Let's check manually.
    # Long division of 6x^2 + 6 by x-4:
    # 1. 6x^2 / x = 6x. Multiply divisor (x-4) by 6x -> 6x^2 - 24x. Subtract from dividend: (0 - (-24))x = 24x. Bring down +6. New remainder term: 24x + 6.
    # 2. 24x / x = 24. Multiply divisor by 24 -> 24x - 96. Subtract from (24x+6): 6 - (-96) = 102.
    # Quotient: 6x + 24. Remainder: 102.
    
    quotient_coefficients = [6, 24]
    remainder_coefficients = [102]
    
    quotient_latex = r"6x + 24"
    remainder_latex = r"102"
    
    return {
        "question_text": f"Divide the polynomial $P(x) = {'+'.join([f'{c}x^{i}' if c!=0 and i>0 else str(c) for i, c in enumerate(dividend_coefficients[::-1])])}$ by $D(x) = {''.join(['+'] + [str(c)+'x' if len(str(c))<=2 else ''].replace('+-', '-').split())}$. Specifically: Divide \( 6x^2 + 0x + 6 \) by \( x - 4 \). Find the quotient and remainder.",
        "correct_answer": {
            "quotient_coefficients": [6, 24],
            "remainder_coefficients": [102],
            "quotient_latex": r"6x + 24",
            "remainder_latex": r"102"
        },
        "oracle_payload": {
            "dividend_coefficients": [6, 0, 6],
            "divisor_coefficients": [1, -4]
        }
    }