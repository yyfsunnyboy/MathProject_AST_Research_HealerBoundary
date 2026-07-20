def generate(level=1, **kwargs):
    return {
        "question_text": r"$(x-2)^{2}=3$",
        "correct_answer": {"result": 4 + 5 * (7)**(0.5), "rational_coefficient": 4, "radical_coefficient": -1, "radicand": 7, "canonical_latex": r"\\pm \\sqrt{2}+3"},
        "oracle_payload": {"equation": "(x-2)^2=3", "order": "a>b", "target": "2a+b"}
    }