def generate(level=1, **kwargs):
    return {
        "question_text": r"$$\sqrt{27} = a \cdot \sqrt{b}$$",
        "correct_answer": {"coefficient": 3, "radicand": 3, "canonical_latex": "$$\\sqrt{27}=3 \\cdot \\sqrt{3}$$"},
        "oracle_payload": {"radicand": 27}
    }