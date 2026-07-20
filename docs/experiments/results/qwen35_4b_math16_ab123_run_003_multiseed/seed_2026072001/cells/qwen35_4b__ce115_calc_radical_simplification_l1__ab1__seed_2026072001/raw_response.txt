def generate(level=1, **kwargs):
    return {
        "question_text": r"$$ \text{Simplify } \\sqrt[3]{27} $$",
        "correct_answer": {"coefficient": 3, "radicand": 1, "canonical_latex": "$$ 3 $$"},
        "oracle_payload": {"radicand": 27}
    }