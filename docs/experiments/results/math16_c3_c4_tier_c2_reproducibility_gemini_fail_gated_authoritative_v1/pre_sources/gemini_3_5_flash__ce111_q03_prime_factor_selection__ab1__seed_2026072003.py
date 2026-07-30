def generate(level=1, **kwargs):
    candidates = kwargs.get("candidates", [11, 12, 13, 14])
    n = kwargs.get("n", 156)
    
    def is_prime(m):
        if m < 2:
            return False
        for i in range(2, int(m**0.5) + 1):
            if m % i == 0:
                return False
        return True

    correct_answer = None
    for c in candidates:
        if n % c == 0 and is_prime(c):
            correct_answer = c
            break
            
    candidates_str = ", ".join(f"${c}$" for c in candidates)
    question_text = f"Which of the following is a prime factor of ${n}$?\nCandidates: {candidates_str}"
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": {
            "candidates": candidates,
            "n": n
        }
    }