def generate(level=1, **kwargs):
    question_text = r"Given the set of candidate integers $C = \{11, 12, 13, 14\}$ and a target integer $n = 156$, select a subset of candidates whose product equals $n$. If no such subset exists or if multiple subsets exist with different products equal to $n$ (which is impossible here), handle accordingly. Find the sum of all elements in the unique valid subset that multiplies exactly to $n$."
    correct_answer = 30
    oracle_payload = {"candidates": [11, 12, 13, 14], "n": 156}
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }