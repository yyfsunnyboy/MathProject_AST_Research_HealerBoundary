def generate(level=1, **kwargs):
    return {
        "question_text": r"Simplify $\sqrt{135}$.",
        "correct_answer": {"coefficient": 3, "radicand": 5, "canonical_latex": "$$3\\sqrt{5}$$"},
        "oracle_payload": {"radicand": 135}
    }