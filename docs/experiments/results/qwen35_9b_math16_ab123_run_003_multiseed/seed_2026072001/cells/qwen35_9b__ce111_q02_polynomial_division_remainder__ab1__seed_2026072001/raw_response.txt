def generate(level=1, **kwargs):
    return {
        "question_text": r"Find the remainder when $6x^2 + 4x$ is divided by $2x^3$. The dividend coefficients are given as [6, 4, 0] and the divisor coefficients as [2, 0, 0].",
        "correct_answer": {
            "remainder": None,
            "canonical_latex": r"\\text{The remainder is } \\infty."
        },
        "oracle_payload": {"dividend_coefficients": [6, 4, 0], "divisor_coefficients": [2, 0, 0]}
    }