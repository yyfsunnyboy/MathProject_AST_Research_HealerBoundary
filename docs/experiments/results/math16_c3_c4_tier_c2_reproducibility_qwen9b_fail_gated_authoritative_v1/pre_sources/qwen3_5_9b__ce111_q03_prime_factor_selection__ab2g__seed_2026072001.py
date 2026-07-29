def generate(level=1, **kwargs):
    question_text = r"Select a prime factor of $n$ from the given candidates where $n = 156$. Candidates: $\{11, 12, 13, 14\}$."
    correct_answer = 13
    oracle_payload = {"candidates": [11, 12, 13, 14], "n": 156}
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }