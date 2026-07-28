def generate(level=1, **kwargs):
    dividend_coefficients = [6, 0, 6]
    divisor_coefficients = [1, -4]
    
    quotient_coefficients = [-2, 3]
    remainder_coefficients = []
    
    question_text = r"""Perform polynomial division of \( P(x) \) by \( Q(x) \).

Given:
\( P(x) = 6x^2 + 0x + 6 \) (coefficients: [6, 0, 6])
\( Q(x) = x - 4 \) (coefficients: [1, -4])

Find the quotient \( S(x) \), remainder \( R(x) \), and verify that \( P(x) = Q(x)S(x) + R(x) \)."""
    
    correct_answer = {
        "quotient_coefficients": [-2, 3],
        "remainder_coefficients": [],
        "quotient_latex": r"S(x) = -2x^1 + 3",
        "remainder_latex": r"R(x) = 0"
    }
    
    oracle_payload = {
        "dividend_coefficients": [6, 0, 6],
        "divisor_coefficients": [1, -4]
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }