def generate(level=1, **kwargs):
    return {
        "question_text": r"Given the set of candidate integers $C = \\{11, 12, 13, 14\\}$ and a target integer $n = 156$, find the product of all distinct prime factors that divide at least one element in $C$ such that their sum equals $n$. If no subset satisfies this condition using only elements from $C$, return $0$",
        "correct_answer": 39,
        "oracle_payload": {"candidates": [11, 12, 13, 14], "n": 156}
    }