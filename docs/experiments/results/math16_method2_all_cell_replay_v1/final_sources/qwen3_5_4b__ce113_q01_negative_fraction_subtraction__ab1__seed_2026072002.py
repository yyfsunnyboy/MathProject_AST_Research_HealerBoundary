def generate(level=1, **kwargs):
    return {
        "question_text": r"Calculate $3/7 - (-1/4)$ and express the result as an irreducible fraction.",
        "correct_answer": {
            "numerator": 25,
            "denominator": 28,
            "canonical_latex": "\\frac{25}{28}"
        },
        "oracle_payload": {"expression": "3/7 - (-1/4)"}
    }