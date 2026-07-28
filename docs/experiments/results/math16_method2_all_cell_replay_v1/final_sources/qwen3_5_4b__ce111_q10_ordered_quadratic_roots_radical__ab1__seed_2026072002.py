def generate(level=1, **kwargs):
    return {
        "question_text": r"Find the ordered roots of $(x-2)^2 = 3$ in the form $a > b$. Express your answer as a tuple where each element is represented by its rational part (if any), radical coefficient ($\pm 1$), and radicand.",
        "correct_answer": {
            "roots": [
                {"rational_part": -2, "radical_coefficient": 1, "radicand": 3},
                {"rational_part": -2, "radical_coefficient": -1, "radicand": 3}
            ],
            "canonical_latex": "-2 + \\sqrt{3},\\quad -2 - \\sqrt{3}"
        },
        "oracle_payload": {
            "equation": "(x-2)^2=3",
            "order": "a>b",
            "target": "2a+b"
        }
    }