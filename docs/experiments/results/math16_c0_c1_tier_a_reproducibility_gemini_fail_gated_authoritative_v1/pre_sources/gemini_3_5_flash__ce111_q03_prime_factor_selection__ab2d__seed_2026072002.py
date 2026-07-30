from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    # Frozen sampled parameters
    candidates = [11, 12, 13, 14]
    n = 156
    
    # Helper to check if a number is prime using the allowed domain API
    def is_prime(p):
        if p < 2:
            return False
        for i in range(2, int(p**0.5) + 1):
            if IntegerOps.is_divisible(p, i):
                return False
        return True

    # Find the candidate that is both prime and a divisor of n
    correct_answer = None
    for c in candidates:
        if is_prime(c) and IntegerOps.is_divisible(n, c):
            correct_answer = c
            break
            
    # Format candidates for question text
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