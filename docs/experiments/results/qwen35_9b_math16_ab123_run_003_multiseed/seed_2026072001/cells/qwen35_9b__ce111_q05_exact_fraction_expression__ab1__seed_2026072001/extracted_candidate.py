def generate(level=1, **kwargs):
    return {
        "question_text": r"Compute $\frac{9}{22} + \frac{11}{18} - (\frac{23}{22} - \frac{7}{18})$.",
        "correct_answer": {"numerator": 0, "denominator": 44, "canonical_latex": "$\\frac{0}{44}$"},
        "oracle_payload": {"expression": "9/22 + 11/18 - (23/22 - 7/18)"}
    }