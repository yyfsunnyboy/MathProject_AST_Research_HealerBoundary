def generate(level=1, **kwargs):
    return {
        "question_text": r"$$\sqrt{27} = a \cdot \sqrt{b}$$ where $a$ and $b$ are integers with no perfect square factors greater than 1. Find the values of $a$ and $b$.",
        "correct_answer": {"coefficient": 3, "radicand": 3, "canonical_latex": r"3 \cdot \sqrt{3}"},
        "oracle_payload": {"radicand": 27}
    }