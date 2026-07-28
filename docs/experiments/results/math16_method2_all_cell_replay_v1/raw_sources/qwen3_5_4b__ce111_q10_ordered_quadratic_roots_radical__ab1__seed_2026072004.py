def generate(level=1, **kwargs):
    return {
        "question_text": r"Find $a$ and $b$ such that $(x-2)^2 = 3$, where the order is defined as $a > b$. Express your answer in the form of a linear combination $c \cdot a + d \cdot b$. Determine the value corresponding to the target expression $2a + b$.",
        "correct_answer": {
            "result_type": "rational_and_radical",
            "value": 1,
            "radical_coefficient": -1,
            "radicand": 3,
            "canonical_latex": "-\\sqrt{3}"
        },
        "oracle_payload": {
            "equation": "(x-2)^2=3",
            "order": "a>b",
            "target": "2a+b"
        }
    }