def generate(level=1, **kwargs):
    return {
        "question_text": r"$$ (x-2)^2 = 3 $$",
        "correct_answer": {"result": "+\\sqrt{7}", "rational_coefficient": None, "radical_coefficient": 1, "radicand": 7, "canonical_latex": "\\pm \\sqrt{7} - 2"},
        "oracle_payload": {"equation": "(x-2)^2=3", "order": "a>b", "target": "2a+b"}
    }