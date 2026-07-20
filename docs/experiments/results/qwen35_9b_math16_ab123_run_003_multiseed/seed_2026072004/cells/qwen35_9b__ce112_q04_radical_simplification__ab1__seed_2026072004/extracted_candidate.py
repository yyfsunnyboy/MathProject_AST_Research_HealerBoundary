def generate(level=1, **kwargs):
    return {
        "question_text": r"Simplify $\sqrt{\\text{{radicand}}}$.",
        "correct_answer": f"coefficient: 3, radicand: {5}, canonical_latex: $3\\\\sqrt{{{5}}}$".replace("{{radicand}}", str(kwargs.get('radicand', 135))).split(",")[-2].strip(),
        "oracle_payload": {"radicand": kwargs.get('radicand', 135)}
    }