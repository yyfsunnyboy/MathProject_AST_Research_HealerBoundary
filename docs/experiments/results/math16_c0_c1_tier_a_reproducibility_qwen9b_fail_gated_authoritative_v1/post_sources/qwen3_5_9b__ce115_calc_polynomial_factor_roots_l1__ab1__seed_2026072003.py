def generate(level=1, **kwargs):
    return {
        "question_text": r"Find the roots and factorization of the quadratic polynomial $P(x) = 1x^2 + 4x - 12$. Express the roots in ascending order.",
        "correct_answer": {
            "roots": [-6, 2],
            "factorization_latex": "(x+6)(x-4)",
            "roots_latex": "-6,\\;2"
        },
        "oracle_payload": {"quadratic_coefficients": [1, 4, -12]}
    }