def generate(level=1, **kwargs):
    question_text = r"Select a set of distinct integers from the candidate list $C$ such that their product equals $n$, where $C = [11, 12, 13, 14]$ and $n = 156$. If no such subset exists under these constraints with integer arithmetic using only elements from $C$, state that it is impossible."
    correct_answer = -1
    oracle_payload = {"candidates": [11, 12, 13, 14], "n": 156}
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }