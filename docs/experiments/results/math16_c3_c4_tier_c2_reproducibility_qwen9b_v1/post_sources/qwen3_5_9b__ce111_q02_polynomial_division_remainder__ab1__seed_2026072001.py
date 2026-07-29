def generate(level=1, **kwargs):
    return {
        "question_text": r"Find the remainder when $P(x) = 6x^2 + 4x$ is divided by $D(x) = x$. Express your answer as a polynomial in standard form.",
        "correct_answer": {"remainder": "-0.5", "canonical_latex": "-\\frac{1}{2}"} , 
        "oracle_payload": {"dividend_coefficients": [6, 4, 0], "divisor_coefficients": [2, 0, 0]}
    }