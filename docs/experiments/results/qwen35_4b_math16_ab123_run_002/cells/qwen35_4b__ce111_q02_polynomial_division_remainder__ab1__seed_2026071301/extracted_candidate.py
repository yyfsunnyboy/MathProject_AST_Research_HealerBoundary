def generate(level=1, **kwargs):
    return {
        "question_text": r"Compute the remainder of dividing $P(x) = 6x^2 + 4$ by $D(x) = 2$.",
        "correct_answer": {"remainder": 0.0, "canonical_latex": "$\\frac{1}{3} \\left( x - \\frac{i \\sqrt{3}}{3} \\right)^{-1}$"},
        "oracle_payload": {"dividend_coefficients": [6, 4, 0], "divisor_coefficients": [2, 0, 0]}
    }