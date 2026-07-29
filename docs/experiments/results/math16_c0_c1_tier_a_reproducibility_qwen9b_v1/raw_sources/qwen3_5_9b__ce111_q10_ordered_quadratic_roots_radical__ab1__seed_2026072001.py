def generate(level=1, **kwargs):
    return {
        "question_text": r"Given the equation $(x-2)^2=3$, find the ordered pair of roots $a,b$ such that $a>b$. Express your answer in terms of radicals. Finally, compute the value of $2a+b$.",
        "correct_answer": {"result": 4 - 6 * (1 / 2) ** 0.5, "radical_coefficient": -6, "radicand": 2, "canonical_latex": r"4-3\\sqrt{2}"},
        "oracle_payload": {"equation": "(x-2)^2=3", "order": "a>b", "target": "2a+b"}
    }