def generate(level=1, **kwargs):
    return {
        "question_text": r"Find the remainder when $P(x) = 6x^2 + 4$ is divided by $D(x) = x$. Express your answer as a constant.",
        "correct_answer": {"remainder": 4},
        "oracle_payload": {"dividend_coefficients": [6, 4, 0], "divisor_coefficients": [2, 0, 0]}
    }