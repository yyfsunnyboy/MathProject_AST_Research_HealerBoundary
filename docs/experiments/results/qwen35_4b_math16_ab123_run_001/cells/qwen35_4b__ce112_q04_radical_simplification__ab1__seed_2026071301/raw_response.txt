def generate(level=1, **kwargs):
    return {
        "question_text": r" Simplify the radical $\sqrt{135}$. Express your answer in the form $a\sqrt{n}$ where $n$ has no square factors greater than 1.",
        "correct_answer": {"coefficient": 9, "radicand": 5, "canonical_latex": r"9\\sqrt{5}"},
        "oracle_payload": {"radicand": 135}
    }