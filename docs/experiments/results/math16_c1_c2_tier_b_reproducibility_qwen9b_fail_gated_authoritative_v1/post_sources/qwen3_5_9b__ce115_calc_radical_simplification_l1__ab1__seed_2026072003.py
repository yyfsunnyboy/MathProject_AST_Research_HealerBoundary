def generate(level=1, **kwargs):
    return {
        "question_text": r"Simplify $\sqrt{27}$.",
        "correct_answer": {"coefficient": 3, "radicand": 3, "canonical_latex": "$3\\sqrt{3}$"},
        "oracle_payload": {"radicand": 27}
    }