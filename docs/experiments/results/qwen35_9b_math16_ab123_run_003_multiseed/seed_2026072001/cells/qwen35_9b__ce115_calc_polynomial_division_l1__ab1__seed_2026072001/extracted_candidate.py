def generate(level=1, **kwargs):
    return {
        "question_text": r"Divide the polynomial $6x^2 + 0x + 6$ by $x - 4$. Find the quotient and remainder.",
        "correct_answer": {
            "quotient_coefficients": [6, 24],
            "remainder_coefficients": [150],
            "quotient_latex": r"6x + 24",
            "remainder_latex": r"150"
        },
        "oracle_payload": {"dividend_coefficients": [6, 0, 6], "divisor_coefficients": [1, -4]}
    }