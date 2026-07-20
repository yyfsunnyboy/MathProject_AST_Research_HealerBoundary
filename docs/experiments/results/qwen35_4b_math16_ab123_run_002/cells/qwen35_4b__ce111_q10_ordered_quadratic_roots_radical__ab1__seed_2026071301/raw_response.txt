def generate(level=1, **kwargs):
    return {
        "question_text": r"$$ (x-2)^2 = 3 $$",
        "correct_answer": {
            "result_type": "rational_and_radical",
            "description": "The roots are $\\pm(\\sqrt{3} + 2)$, which can be expressed as a rational part and a radical part.",
            "components": {
                "rational_part": 2,
                "radical_coefficient": 1,
                "radicand": 3,
                "canonical_latex": r"\\pm(\\sqrt{3} + 2)"
            }
        },
        "oracle_payload": {
            "equation": "(x-2)^2=3",
            "order": "a>b",
            "target": "2a+b"
        }
    }