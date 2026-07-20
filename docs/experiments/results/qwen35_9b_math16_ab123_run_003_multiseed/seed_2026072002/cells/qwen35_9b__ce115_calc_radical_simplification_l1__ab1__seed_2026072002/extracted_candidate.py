def generate(level=1, **kwargs):
    return {
        "question_text": r"Simplify $\sqrt{27}$ to the form $a\sqrt{b}$ where $b$ is as small as possible.",
        "correct_answer": {"coefficient": 3, "radicand": 3, "canonical_latex": "$3\\sqrt{3}$"},
        "oracle_payload": {"radicand": 27}
    }