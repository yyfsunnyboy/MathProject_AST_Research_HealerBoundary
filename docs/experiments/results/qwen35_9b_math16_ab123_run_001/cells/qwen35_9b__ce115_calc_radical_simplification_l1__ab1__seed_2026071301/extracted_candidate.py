def generate(level=1, **kwargs):
    return {
        "question_text": r"Simplify $\sqrt{%d}$.",
        "correct_answer": f"{3} \cdot 3^{{{\frac{{{level}}}{{{2}}}}}}}",
        "oracle_payload": {"radicand": kwargs.get("radicand", 27)}
    }