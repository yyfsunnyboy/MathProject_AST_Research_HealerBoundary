def generate(level=1, **kwargs):
    question_text = r"Select all prime factors of $n$ from the given candidates."
    correct_answer = 2970368451
    oracle_payload = {"candidates": [11, 12, 13, 14], "n": 156}
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }