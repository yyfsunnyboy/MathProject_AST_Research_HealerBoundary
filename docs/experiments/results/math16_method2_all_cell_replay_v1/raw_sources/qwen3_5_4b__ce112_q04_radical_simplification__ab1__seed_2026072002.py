def generate(level=1, **kwargs):
    return {
        "question_text": r"$$\text{Simplify } \sqrt[3]{135}.$$",
        "correct_answer": {"coefficient": 3, "radicand": 27, "canonical_latex": "$$\\frac{3}{\\sqrt[3]{27}}$$"},
        "oracle_payload": {"radicand": 135}
    }