def generate(level=1, **kwargs):
    return {
        "question_text": r"Find all roots and factorize the quadratic polynomial $P(x) = 1x^2 + 4x - 12$ completely over real numbers.",
        "correct_answer": {
            "roots": [-6.0, 2.0],
            "factorization_latex": r"(x+6)(x-2)",
            "roots_latex": r"\\{-6, 2\\}"
        },
        "oracle_payload": {"quadratic_coefficients": [1, 4, -12]}
    }