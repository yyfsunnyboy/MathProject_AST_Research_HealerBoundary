def generate(level=1, **kwargs):
    radicand = 27
    if level == 1:
        coefficient = 3
        simplified_radicand = 3
        canonical_latex = r"3\\sqrt{3}"
    else:
        raise ValueError("Level must be 1")

    return {
        "question_text": f"Simplify the radical $\\sqrt{{{radicand}}}$.",
        "correct_answer": {
            "coefficient": coefficient,
            "radicand": simplified_radicand,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": radicand
    }