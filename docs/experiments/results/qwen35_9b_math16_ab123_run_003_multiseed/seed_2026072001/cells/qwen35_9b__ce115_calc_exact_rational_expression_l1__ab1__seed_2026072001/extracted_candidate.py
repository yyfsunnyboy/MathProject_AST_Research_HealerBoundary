def generate(level=1, **kwargs):
    return {
        "question_text": r"Compute $\frac{2.79}{89.3} + \left(-\frac{-0.21}{89.3}\right)$.",
        "correct_answer": {"value": "4/5", "canonical_latex": "\\frac{4}{5}"},
        "oracle_payload": {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}
    }