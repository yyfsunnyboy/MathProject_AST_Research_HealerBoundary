def generate(level=1, **kwargs):
    return {
        "question_text": r"Calculate the exact value of $2.79 \times 89.3 - (-0.21) \times 89.3$. Express your final answer as an irreducible fraction.",
        "correct_answer": {"value": "-465/5", "canonical_latex": "$-\\frac{465}{5}$"},
        "oracle_payload": {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}
    }