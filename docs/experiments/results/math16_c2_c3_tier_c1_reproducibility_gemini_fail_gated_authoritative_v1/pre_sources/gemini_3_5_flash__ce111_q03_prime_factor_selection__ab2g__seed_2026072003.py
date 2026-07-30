def generate(level=1, **kwargs):
    candidates = [11, 12, 13, 14]
    n = 156
    correct_answer = 13

    question_text = (
        f"Which of the following is a prime factor of ${n}$?\n"
        f"Candidates: " + ", ".join(f"${c}$" for c in candidates)
    )

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": {
            "candidates": candidates,
            "n": n
        }
    }