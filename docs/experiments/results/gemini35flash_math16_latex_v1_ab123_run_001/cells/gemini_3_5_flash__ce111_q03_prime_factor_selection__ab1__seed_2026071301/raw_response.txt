def generate(level=1, **kwargs):
    candidates = [11, 12, 13, 14]
    n = 156

    def is_prime(k):
        if k < 2:
            return False
        for i in range(2, int(k**0.5) + 1):
            if k % i == 0:
                return False
        return True

    correct_answer = None
    for c in candidates:
        if n % c == 0 and is_prime(c):
            correct_answer = c
            break

    candidates_str = ", ".join(f"${c}$" for c in candidates)
    question_text = f"Which of the following candidates is a prime factor of ${n}$?\nCandidates: {candidates_str}"

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": {
            "candidates": candidates,
            "n": n
        }
    }