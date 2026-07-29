def generate(level=1, **kwargs):
    return {
        "question_text": r"Find the remainder when dividing $P(x) = 6x^2 + 4$ by $D(x) = 2$.",
        "correct_answer": {"remainder": 0.5, "canonical_latex": "\\frac{1}{2}"},
        "oracle_payload": {"dividend_coefficients": [6, 4, 0], "divisor_coefficients": [2, 0, 0]}
    }