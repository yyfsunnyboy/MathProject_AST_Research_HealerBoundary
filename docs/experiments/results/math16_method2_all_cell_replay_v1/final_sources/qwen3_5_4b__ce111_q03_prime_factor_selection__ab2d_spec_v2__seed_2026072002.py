# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen sampled parameters defined directly as per task specification
    candidates = [11, 12, 13, 14]
    n = 156
    
    def is_prime(num):
        if num < 2:
            return False
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                return False
        return True

    # Find the prime candidate that divides n exactly
    correct_answer = None
    for cand in candidates:
        if is_prime(cand) and (n % cand) == 0:
            correct_answer = cand
            break
    
    question_text = r"Find a prime number $p$ from the given list of integers such that $p$ divides $n=156$ exactly. The available candidates are $\{11, 12, 13, 14\}$."

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": {"candidates": [11, 12, 13, 14], "n": 156}
    }