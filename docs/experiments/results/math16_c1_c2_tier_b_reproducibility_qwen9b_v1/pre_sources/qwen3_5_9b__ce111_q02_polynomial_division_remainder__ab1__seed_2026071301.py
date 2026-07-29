def generate(level=1, **kwargs):
    return {
        "question_text": r"Find the remainder when $P(x) = 6x^2 + 4x$ is divided by $D(x) = x^3$. Note that only the remainder will be scored.",
        "correct_answer": {"remainder": [0, 0, 0], "canonical_latex": r"0"},
        "oracle_payload": {"dividend_coefficients": [6, 4, 0], "divisor_coefficients": [2, 0, 0]}
    }