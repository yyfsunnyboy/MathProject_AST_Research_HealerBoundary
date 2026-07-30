def generate(level=1, **kwargs):
    base = -3
    exponent = 3

    correct_answer = base ** exponent

    question_text = f"Evaluate $({base})^{{{exponent}}}$."

    oracle_payload = {
        "base": base,
        "exponent": exponent
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload,
    }