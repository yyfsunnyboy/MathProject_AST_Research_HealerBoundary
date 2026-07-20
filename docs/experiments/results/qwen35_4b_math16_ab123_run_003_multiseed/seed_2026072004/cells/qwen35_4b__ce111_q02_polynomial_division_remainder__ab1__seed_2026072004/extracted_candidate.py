def generate(level=1, **kwargs):
    return {
        "question_text": r"$\\text{Find the remainder when } 6x^2 + 4 \\text{ is divided by } 2x$.",
        "correct_answer": {"remainder": "-0", "canonical_latex": "\\-"},
        "oracle_payload": {"dividend_coefficients": [6, 4, 0], "divisor_coefficients": [2, 0, 0]}
    }