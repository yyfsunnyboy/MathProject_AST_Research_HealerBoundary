def generate(level=1, **kwargs):
    return {
        "question_text": r"\text{Solve for } x \text{ in the equation } (x-2)^2 = 3.",
        "correct_answer": {"rational": -7/4, "radical_coefficient": 0, "radicand": 96},
        "oracle_payload": {
            "equation": "(x-2)^2=3",
            "order": "a>b",
            "target": "2a+b"
        }
    },