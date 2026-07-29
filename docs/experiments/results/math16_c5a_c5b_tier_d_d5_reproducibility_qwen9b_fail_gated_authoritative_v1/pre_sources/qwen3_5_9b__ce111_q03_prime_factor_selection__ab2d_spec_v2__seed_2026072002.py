# -*- coding: utf-8 -*-

def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

def generate(level=1, **kwargs):
    # Define all frozen parameters directly as per specification
    candidates = [11, 12, 13, 14]
    n = 156
    
    correct_answer = None
    
    for candidate in candidates:
        if is_prime(candidate) and (n % candidate == 0):
            correct_answer = candidate
            break
            
    question_text = r"Given the integer $n = \text{" + str(n) + "}" + ", select a prime factor from the list of candidates $\{11, 12, 13, 14\}$ that divides $n$ exactly."

    oracle_payload = {"candidates": [11, 12, 13, 14], "n": n}
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload,
    }