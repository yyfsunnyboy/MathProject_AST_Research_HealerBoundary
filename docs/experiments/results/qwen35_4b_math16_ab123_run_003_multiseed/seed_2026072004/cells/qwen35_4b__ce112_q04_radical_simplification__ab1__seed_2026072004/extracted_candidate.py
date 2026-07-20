def generate(level=1, **kwargs):
    return {
        "question_text": r"\text{Simplify } \sqrt{\overline{\textbf{$\boldsymbol{radicand}$}}}",
        "correct_answer": {"coefficient": 3, "radicand": 5, "canonical_latex": "\\frac{\\left(3}{1}\\right) \\cdot \\sqrt[2]{5}"},
        "oracle_payload": {"radicand": 135}
    }