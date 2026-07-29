def generate(level=1, **kwargs):
    return {
        "question_text": r"Compute the exact value of $2.79 \times 89.3 - (-0.21) \times 89.3$.",
        "correct_answer": {"value": "256", "canonical_latex": "$256$"},
        "oracle_payload": {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}
    }