def generate(level=1, **kwargs):
    return {
        "question_text": r"Compute $ \frac{9}{22} + \frac{11}{18} - \left( \frac{23}{22} - \frac{7}{18} \right) $.",
        "correct_answer": {"numerator": 4, "denominator": 5},
        "canonical_latex": r"\frac{4}{5}",
        "oracle_payload": {"expression": "9/22 + 11/18 - (23/22 - 7/18)"}
    }