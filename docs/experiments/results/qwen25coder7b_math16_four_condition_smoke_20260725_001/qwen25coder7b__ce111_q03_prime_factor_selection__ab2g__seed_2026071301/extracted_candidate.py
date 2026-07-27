def generate(level=1, **kwargs):
    candidates = [11, 12, 13, 14]
    n = 156
    question_text = r"Which of the following is a prime factor of \( n \)?"
    correct_answer = 13
    oracle_payload = {"candidates": candidates, "n": n}
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }
