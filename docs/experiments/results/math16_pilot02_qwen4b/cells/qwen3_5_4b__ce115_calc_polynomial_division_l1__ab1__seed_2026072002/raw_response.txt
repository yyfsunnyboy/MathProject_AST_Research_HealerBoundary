def generate(level=1, **kwargs):
    return {
        "question_text": r"Perform polynomial division of \( 6x^2 + 0x + 6 \) by \( x - 4 \). Express the result as quotient and remainder.",
        "correct_answer": {
            "quotient_coefficients": [6, 24],
            "remainder_coefficients": [-150],
            "quotient_latex": r"6x + 24",
            "remainder_latex": "-150"
        },
        "oracle_payload": {"dividend_coefficients": [6, 0, 6], "divisor_coefficients": [1, -4]}
    }