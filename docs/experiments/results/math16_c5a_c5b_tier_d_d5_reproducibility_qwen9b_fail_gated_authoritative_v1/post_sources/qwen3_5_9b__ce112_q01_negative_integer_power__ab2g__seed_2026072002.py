def generate(level=1, **kwargs):
    question_text = r"Calculate $(-3)^{3}$."
    correct_answer = -27
    oracle_payload = {"base": -3, "exponent": 3}
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }