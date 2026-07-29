def generate(level=1, **kwargs):
    question_text = r"Rationalize the denominator of $\frac{9}{4-\sqrt{7}}$."
    correct_answer = 36 + 28 * (7 ** 0.5)
    oracle_payload = {"denominator": "4-sqrt(7)", "numerator": 9, "radicand": 7}

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }