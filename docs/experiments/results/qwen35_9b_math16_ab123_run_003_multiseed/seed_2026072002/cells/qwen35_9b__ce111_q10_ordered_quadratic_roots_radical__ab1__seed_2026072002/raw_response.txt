def generate(level=1, **kwargs):
    return {
        "question_text": r"Given the equation $(x-2)^2 = 3$, find the sum of $a$ and $b$ where $a > b$ are the two roots expressed in simplest radical form as $2 \pm \sqrt{d}$. Calculate $2a + b$.",
        "correct_answer": {
            "result": "10",
            "rational": 8,
            "radical_coefficient": -1,
            "radicand": 3,
            "canonical_latex": "-\\sqrt{3}"
        },
        "oracle_payload": {"equation": "(x-2)^2=3", "order": "a>b", "target": "2a+b"}
    }