def generate(level=1, **kwargs):
    return {
        "question_text": r"Compute $3/7 - (-1/4)$.",
        "correct_answer": {"numerator": 19, "denominator": 28, "canonical_latex": "$\\frac{19}{28}$"},
        "oracle_payload": {"expression": "3/7 - (-1/4)"}
    }