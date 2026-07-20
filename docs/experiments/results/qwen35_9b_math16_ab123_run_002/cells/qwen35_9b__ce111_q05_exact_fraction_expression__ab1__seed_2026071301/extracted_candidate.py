def generate(level=1, **kwargs):
    return {
        "question_text": r"Compute $9/22 + 11/18 - (23/22 - 7/18)$.",
        "correct_answer": {"numerator": 5, "denominator": 6},
        "canonical_latex": "\\frac{5}{6}",
        "oracle_payload": {"expression": "9/22 + 11/18 - (23/22 - 7/18)"}
    }