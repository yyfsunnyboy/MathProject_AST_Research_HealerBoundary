def generate(level=1, **kwargs):
    return {
        "question_text": r"Given the set of candidate integers $C = \\{11, 12, 13, 14\\}$ and a target integer $N = 156$, find the sum of all distinct prime factors that divide at least one element in $C$ but do not divide any other element in $C$.",
        "correct_answer": 0,
        "oracle_payload": {"candidates": [11, 12, 13, 14], "n": 156}
    }