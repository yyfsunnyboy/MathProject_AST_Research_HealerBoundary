def generate(level=1, **kwargs):
    return {
        "question_text": r"Find the smallest positive integer $k$ such that $\frac{156}{k}$ is a product of distinct prime factors chosen from the set $\{11, 12, 13, 14\}$. Note: Only elements in the given set can be used as factors.",
        "correct_answer": 12,
        "oracle_payload": {"candidates": [11, 12, 13, 14], "n": 156}
    }