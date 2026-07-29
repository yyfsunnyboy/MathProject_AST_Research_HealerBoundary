def generate(level=1, **kwargs):
    return {
        "question_text": r"Given the set of candidate integers $C = \\{11, 12, 13, 14\\}$ and a target integer $n = 156$, find the smallest positive integer $k$ such that there exists a subset $S \\subseteq C$ with $|S| = k$ where the product of elements in $S$ divides $n$. If no non-empty subset satisfies this condition, return -1.",
        "correct_answer": 2,
        "oracle_payload": {"candidates": [11, 12, 13, 14], "n": 156}
    }