def generate(level=1, **kwargs):
    return {
        "question_text": r"Perform polynomial division: $6x^2 + 0x + 6$ divided by $x - 4$. Express the result with quotient and remainder.",
        "correct_answer": {
            "quotient_coefficients": [1, 8],
            "remainder_coefficients": [-30],
            "quotient_latex": r"8x^2 + (-6)x",
            "remainder_latex": "-34"
        },
        "oracle_payload": {"dividend_coefficients": [6, 0, 6], "divisor_coefficients": [1, -4]}
    }