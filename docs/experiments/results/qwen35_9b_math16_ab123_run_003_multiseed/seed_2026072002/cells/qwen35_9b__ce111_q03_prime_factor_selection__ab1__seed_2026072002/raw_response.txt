def generate(level=1, **kwargs):
    return {
        "question_text": r"Given the candidate set $C = \\{11, 12, 13, 14\\}$ and target integer $n = 156$, find a subset of $C$ such that every prime factor of each element in the subset is also a prime factor of $n$. What is the maximum possible size (cardinality) of such a valid subset?",
        "correct_answer": 2,
        "oracle_payload": {"candidates": [11, 12, 13, 14], "n": 156}
    }