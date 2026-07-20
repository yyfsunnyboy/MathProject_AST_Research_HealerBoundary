def generate(level=1, **kwargs):
    return {
        "question_text": r"Find the remainder when $6x^2 + 4x$ is divided by $2x$. Express your answer as a polynomial in standard form.",
        "correct_answer": {"remainder": "-8", "canonical_latex": "-8"},
        "oracle_payload": {"dividend_coefficients": [6, 4, 0], "divisor_coefficients": [2, 0, 0]}
    }