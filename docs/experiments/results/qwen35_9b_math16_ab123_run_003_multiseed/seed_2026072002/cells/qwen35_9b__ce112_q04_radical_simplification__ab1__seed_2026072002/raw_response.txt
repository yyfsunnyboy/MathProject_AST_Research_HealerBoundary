def generate(level=1, **kwargs):
    return {
        "question_text": r"Simplify $\sqrt{135}$.",
        "correct_answer": "9\\sqrt{5}",
        "oracle_payload": {"radicand": 135}
    }