def generate(level=1, **kwargs):
    return {
        "question_text": r"Given the equation $(x-2)^2=3$, let $a$ and $b$ be the roots of the equation such that $a>b$. Find the value of $2a+b$.",
        "correct_answer": {"value": 4 + 6 ** (1 / 2), "rational_coefficient": 4, "radical_coefficient": 1, "radicand": 3},
        "oracle_payload": {"equation": "(x-2)^2=3", "order": "a>b", "target": "2a+b"}
    }