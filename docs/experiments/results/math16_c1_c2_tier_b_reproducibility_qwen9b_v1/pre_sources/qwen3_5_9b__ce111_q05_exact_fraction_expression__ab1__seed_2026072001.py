def generate(level=1, **kwargs):
    return {
        "question_text": r"Compute $9/22 + 11/18 - (23/22 - 7/18)$ and express the result as an irreducible fraction.",
        "correct_answer": {"numerator": 4, "denominator": 5},
        "canonical_latex": r"\frac{4}{5}",
        "oracle_payload": {"expression": "9/22 + 11/18 - (23/22 - 7/18)"}
    }