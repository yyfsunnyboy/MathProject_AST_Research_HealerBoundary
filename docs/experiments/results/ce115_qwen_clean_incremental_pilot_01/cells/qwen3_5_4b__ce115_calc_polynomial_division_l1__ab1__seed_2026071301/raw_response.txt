def generate(level=1, **kwargs):
    return {
        "question_text": f"Perform polynomial division with dividend coefficients [6, 0, 6] and divisor coefficients [1, -4].",
        "correct_answer": {"quotient_coefficients": [-2, 3], "remainder_coefficients": [6]},
        "oracle_payload": {"dividend_coefficients": [6, 0, 6], "divisor_coefficients": [1, -4]}
    }