def generate(level=1, **kwargs):
    return {
        "question_text": r"Given the list of candidate integers $\\text{candidates} = [11, 12, 13, 14]$, find the product of all elements in this list that are prime numbers.",
        "correct_answer": 143,
        "oracle_payload": {"candidates": [11, 12, 13, 14], "n": 156}
    }