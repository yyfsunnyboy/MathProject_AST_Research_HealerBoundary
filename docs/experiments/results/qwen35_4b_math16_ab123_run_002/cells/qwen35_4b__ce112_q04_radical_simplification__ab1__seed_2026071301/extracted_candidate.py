def generate(level=1, **kwargs):
    return {
        "question_text": r"Radical Simplification: Express $\sqrt{135}$ in simplest form as $a\sqrt{n}$. What are the values of coefficient $a$ and radicand $n$, where $n$ is square-free?",
        "correct_answer": {"coefficient": 9, "radicand": 5},
        "oracle_payload": {"radicand": 135}
    }