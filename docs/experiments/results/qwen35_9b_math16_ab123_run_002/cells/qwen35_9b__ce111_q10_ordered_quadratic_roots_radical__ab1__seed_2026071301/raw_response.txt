def generate(level=1, **kwargs):
    return {
        "question_text": r"Given the quadratic equation $(x-2)^2 = 3$, find its two real roots $a$ and $b$ such that $a > b$. Express your answer in the form of radicals. Then compute the value of $2a + b$.",
        "correct_answer": {
            "result": -4,
            "radical_coefficient": 1,
            "radicand": 3,
            "canonical_latex": "-4"
        },
        "oracle_payload": {"equation": "(x-2)^2=3", "order": "a>b", "target": "2a+b"}
    }