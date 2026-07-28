def generate(level=1, **kwargs):
    return {
        "question_text": r"Perform polynomial division of \( P(x) = 6x^2 + 0x + 6 \) by \( D(x) = x - 4 \). Find the quotient and remainder.",
        "correct_answer": {
            "quotient_coefficients": [6, 24],
            "remainder_coefficients": [-138],
            "quotient_latex": r"Q(x) = 6x + 24",
            "remainder_latex": r"R(x) = -138"
        },
        "oracle_payload": {"dividend_coefficients": [6, 0, 6], "divisor_coefficients": [1, -4]}
    }