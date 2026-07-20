def generate(level=1, **kwargs):
    return {
        "question_text": r"Simplify $\sqrt{" + str(kwargs.get("radicand", 27)) + r"}$.",
        "correct_answer": {"coefficient": 3, "radicand": 3, "canonical_latex": "$3\\sqrt{3}$"},
        "oracle_payload": kwargs
    }