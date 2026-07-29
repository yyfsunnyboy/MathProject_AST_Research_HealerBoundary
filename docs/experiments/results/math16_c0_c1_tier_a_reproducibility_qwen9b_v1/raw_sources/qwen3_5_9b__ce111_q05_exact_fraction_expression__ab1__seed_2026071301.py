def generate(level=1, **kwargs):
    return {
        "question_text": r"Compute the exact value of $\\frac{9}{22} + \\frac{11}{18} - (\\frac{23}{22} - \\frac{7}{18})$ and express it as an irreducible fraction.",
        "correct_answer": {
            "numerator": 0,
            "denominator": 1,
            "canonical_latex": r"0/1"
        },
        "oracle_payload": {"expression": "9/22 + 11/18 - (23/22 - 7/18)"}
    }