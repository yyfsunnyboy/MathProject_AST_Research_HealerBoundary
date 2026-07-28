def generate(level=1, **kwargs):
    dividend_coefficients = [6, 4, 0]
    divisor_coefficients = [2, 0, 0]
    
    # Perform polynomial division: (6x^2 + 4x) / (2x^2)
    # Dividend P(x) = 6x^2 + 4x + 0
    # Divisor Q(x) = 2x^2
    
    # Leading term of quotient: (6/2)x^(2-2) = 3
    remainder_coeffs = [4, 0]  # The original dividend minus the product of divisor and first quotient term
                            # P - Q*Q_1 = (6x^2 + 4x) - (2x^2 * 3) = 6x^2 + 4x - 6x^2 = 4x
    
    correct_answer = {
        "remainder": [4, 0],
        "canonical_latex": "\\text{rem}(P(x), Q(x)) = 4x"
    }
    
    return {
        "question_text": r"$\\frac{6x^2 + 4x}{2x^2}$",
        "correct_answer": correct_answer,
        "oracle_payload": {"dividend_coefficients": [6, 4, 0], "divisor_coefficients": [2, 0, 0]}
    }