def generate(level=1, **kwargs):
    return {
        "question_text": r"Find the exact value of the expression: $\frac{9}{22} + \frac{11}{18} - \left(\frac{23}{22} - \frac{7}{18}\right)$.",
        "correct_answer": {
            "numerator": 5,
            "denominator": 6,
            "canonical_latex": "\\frac{5}{6}"
        },
        "oracle_payload": {"expression": "9/22 + 11/18 - (23/22 - 7/18)"}
    }