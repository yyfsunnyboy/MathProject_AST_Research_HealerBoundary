def generate(level=1, **kwargs):
    candidates = [11, 12, 13, 14]
    n = 156
    
    question_text = r"Find the prime factor of $n$ that is present in the list $\{c \mid c \in \text{\textbackslash{}candidates\}\}$."
    
    correct_answer = None
    for candidate in candidates:
        if isinstance(candidate, int) and n % candidate == 0:
            # Check primality
            is_prime = True
            check_limit = int(candidate ** 0.5) + 1
            for i in range(2, check_limit):
                if candidate % i == 0:
                    is_prime = False
                    break
            if is_prime:
                correct_answer = candidate
    
    oracle_payload = {"candidates": candidates, "n": n}
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }