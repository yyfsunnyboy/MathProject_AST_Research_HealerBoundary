def generate(level=1, **kwargs):
    return {
        "question_text": r"$(x-2)^2 = 3$",
        "correct_answer": {"result": 4 + 5 * (3)**(0.5), "rational_coefficient": 4, "radical_coefficient": 1, "radicand": 3, "canonical_latex": r"\\frac{8}{2} \\pm \\sqrt{7}$"},
        "oracle_payload": {"equation": "(x-2)^2=3", "order": "a>b", "target": "2a+b"}
    }