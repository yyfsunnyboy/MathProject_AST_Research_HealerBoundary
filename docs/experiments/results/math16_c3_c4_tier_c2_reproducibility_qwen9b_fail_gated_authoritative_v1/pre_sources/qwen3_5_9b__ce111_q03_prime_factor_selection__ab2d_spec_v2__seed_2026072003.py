# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen sampled parameters defined directly as per specification
    candidates = [11, 12, 13, 14]
    n = 156
    
    def is_prime(num):
        if num < 2:
            return False
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                return False
        return True

    # Filter candidates that are prime and divide n exactly
    valid_primes = [c for c in candidates if is_prime(c) and (n % c == 0)]
    
    # Select the first valid candidate as the correct answer
    if valid_primes:
        correct_answer = valid_primes[0]
    else:
        # Fallback to a default prime from candidates if none match, though logic ensures one exists here
        for c in candidates:
            if is_prime(c):
                correct_answer = c
                break
    
    question_text = r"Select the smallest prime number $p$ from the list of candidates such that $p$ divides $n$ exactly. Candidates: $\{11, 12, 13, 14\}$, Target integer $n$: $156$."
    
    oracle_payload = {"candidates": [11, 12, 13, 14], "n": 156}

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload,
    }