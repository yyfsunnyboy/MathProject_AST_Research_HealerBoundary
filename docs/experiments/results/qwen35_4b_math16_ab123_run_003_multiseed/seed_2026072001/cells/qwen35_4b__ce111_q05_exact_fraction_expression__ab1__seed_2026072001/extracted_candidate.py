def generate(level=1, **kwargs):
    return {
        "question_text": r"Express $\\frac{9}{22} + \\frac{11}{18} - \\left( \\frac{23}{22} - \\frac{7}{18} \\right)$ as an irreducible fraction.",
        "correct_answer": {
            "numerator": 4,
            "denominator": 99,
            "canonical_latex": "\\frac{4}{99}"
        },
        "oracle_payload": {"expression": "9/22 + 11/18 - (23/22 - 7/18)"}
    }