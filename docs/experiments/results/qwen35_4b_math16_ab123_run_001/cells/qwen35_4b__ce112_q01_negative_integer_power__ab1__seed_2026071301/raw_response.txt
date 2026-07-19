def generate(level=1, **kwargs):
    return {
        "question_text": r"Evaluate $(-3)^3$.",
        "correct_answer": -27,
        "oracle_payload": {"base": -3, "exponent": 3}
    }