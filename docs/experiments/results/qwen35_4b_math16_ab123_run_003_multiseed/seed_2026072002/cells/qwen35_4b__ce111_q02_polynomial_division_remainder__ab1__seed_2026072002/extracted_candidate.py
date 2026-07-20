def generate(level=1, **kwargs):
    return {
        "question_text": r"Find the remainder of $6x^2 + 4$ divided by $2$.",
        "correct_answer": {"remainder": 0, "canonical_latex": "$\frac{3}{2} (6x^2+4) - \left(\frac{9}{2}(2)\right)$"},
        "oracle_payload": {"dividend_coefficients": [6, 4, 0], "divisor_coefficients": [2, 0, 0]}
    }