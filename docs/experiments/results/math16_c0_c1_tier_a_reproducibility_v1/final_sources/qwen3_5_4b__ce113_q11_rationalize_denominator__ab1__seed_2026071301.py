def generate(level=1, **kwargs):
    return {
        "question_text": r"Rationalize the denominator of $\frac{9}{4-\sqrt{7}}$. Express your answer as a single integer.",
        "correct_answer": 23,
        "oracle_payload": {"denominator": "4-sqrt(7)", "numerator": 9, "radicand": 7}
    }