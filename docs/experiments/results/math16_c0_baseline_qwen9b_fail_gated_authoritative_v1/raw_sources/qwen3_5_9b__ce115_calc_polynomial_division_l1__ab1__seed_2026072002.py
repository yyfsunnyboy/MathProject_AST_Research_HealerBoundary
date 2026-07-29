def generate(level=1, **kwargs):
    dividend_coefficients = [6, 0, 6]
    divisor_coefficients = [1, -4]
    
    # Polynomial: P(x) = 6x^2 + 0x + 6 (coeffs from highest to lowest degree implied by typical format or vice versa? 
    # Standard math notation lists coeffs for descending powers. Let's assume standard convention: [a_n, ..., a_0]
    # Dividend: 6x^2 + 6
    # Divisor: x - 4
    
    # Synthetic division / Long division logic manually calculated to ensure exact integers
    # P(x) = 6x^2 + 6. Root of divisor is 4.
    # Evaluate at 4? No, we need quotient and remainder for (6x^2+6)/(x-4).
    
    # Coefficients: [6, 0, 6] -> Degree 2 down to 0. 
    # Step 1: Bring down 6. Multiply by 4 -> 24. Add to next coeff (0) -> 24.
    # Step 2: Take 24. Multiply by 4 -> 96. Add to last coeff (6) -> 102.
    
    quotient_coefficients = [6, 24]   # Represents 6x + 24
    remainder_coefficients = [102]    # Constant term
    
    quotient_latex = r"6x + 24"
    remainder_latex = "102"
    
    return {
        "question_text": f"Determine the quotient and remainder when dividing $\\left( \\sum_{i=0}^{n} a_i x^i \\right)$ by $(x-4)$. Given dividend coefficients \${dividend_coefficients}\$ (representing ${dividend_coefficients[0]}x^2 + {dividend_coefficients[1]}x + {dividend_coefficients[2]})\$ and divisor coefficients \${divisor_coefficients}\$ (representing $x - 4$), find the result.",
        "correct_answer": {
            "quotient_coefficients": quotient_coefficients,
            "remainder_coefficients": remainder_coefficients,
            "quotient_latex": quotient_latex,
            "remainder_latex": remainder_latex
        },
        "oracle_payload": {"dividend_coefficients": [6, 0, 6], "divisor_coefficients": [1, -4]}
    }