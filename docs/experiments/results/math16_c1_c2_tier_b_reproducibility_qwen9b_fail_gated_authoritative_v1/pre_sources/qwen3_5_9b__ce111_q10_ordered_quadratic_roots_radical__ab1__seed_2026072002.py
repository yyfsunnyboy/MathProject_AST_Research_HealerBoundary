def generate(level=1, **kwargs):
    return {
        "question_text": r"Given the equation $(x-2)^2=3$, find $a$ and $b$ such that the roots are ordered as $a>b$. Then compute the value of $2a+b$.",
        "correct_answer": {
            "result": 6 + 4 * (2 ** 0.5),
            "rational": 6,
            "radical_coefficient": 4,
            "radicand": 2,
            "canonical_latex": r"6+4\\sqrt{2}"
        },
        "oracle_payload": {"equation": "(x-2)^2=3", "order": "a>b", "target": "2a+b"}
    }