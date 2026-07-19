def generate(level=1, **kwargs):
    return {
        "question_text": r"Given the dividend \( P(x) = 6x^2 + 0x + 6 \) and the divisor \( D(x) = x - 4 \), perform polynomial long division to find the quotient \( Q(x) \) and the remainder \( R(x) \). Express your answer in the form where \( P(x) = D(x)Q(x) + R(x) \).",
        "correct_answer": {
            "quotient_coefficients": [6, -24],
            "remainder_coefficients": [150],
            "quotient_latex": r"6x - 24",
            "remainder_latex": r"150"
        },
        "oracle_payload": {"dividend_coefficients": [6, 0, 6], "divisor_coefficients": [1, -4]}
    }