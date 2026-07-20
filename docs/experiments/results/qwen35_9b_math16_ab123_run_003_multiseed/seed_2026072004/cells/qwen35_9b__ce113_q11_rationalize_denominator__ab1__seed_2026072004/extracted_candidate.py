def generate(level=1, **kwargs):
    return {
        "question_text": r"Rationalize the denominator of $\frac{9}{4-\sqrt{7}}$.",
        "correct_answer": 36 + 28 * (7) ** (1/2),
        "oracle_payload": {"denominator": "4-sqrt(7)", "numerator": 9, "radicand": 7}
    }