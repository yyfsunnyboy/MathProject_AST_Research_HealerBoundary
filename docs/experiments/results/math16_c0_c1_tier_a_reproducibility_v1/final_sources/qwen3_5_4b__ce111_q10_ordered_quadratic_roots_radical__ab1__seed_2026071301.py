def generate(level=1, **kwargs):
    return {
        "question_text": r"Find $a$ and $b$ such that $(x-2)^2 = 3$, where the order is defined as $a > b$. Express your answer in terms of a rational number, a radical coefficient (either +1 or -1), and an integer radicand.",
        "correct_answer": {
            "rational": 0.5,
            "radical_coefficient": 1,
            "radicand": 3,
            "canonical_latex": r"\frac{1}{2}\sqrt{3}"
        },
        "oracle_payload": {"equation": "(x-2)^2=3", "order": "a>b", "target": "2a+b"}
    }