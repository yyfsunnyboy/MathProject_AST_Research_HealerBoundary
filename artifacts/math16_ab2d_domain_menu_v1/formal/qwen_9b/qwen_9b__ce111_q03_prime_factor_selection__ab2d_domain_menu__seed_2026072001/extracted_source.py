from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    frozen_params = {
        "candidates": [11, 12, 13, 14],
        "n": 156
    }
    
    # We need to find which candidate is a prime factor of n (156).
    # A number x is a prime factor if:
    # 1. IntegerOps.is_divisible(n, x) is True
    # 2. The result of IntegerOps.prime_factorization(x) has exactly one key with exponent > 0 and that key equals the divisor itself? 
    # Actually, simpler definition for "prime factor": a number p such that n % p == 0 AND p is prime.
    # However, we don't have an explicit `is_prime` API in IntegerOps menu provided above.
    # Let's re-read allowed APIs: add, fmt_num, is_divisible, positive_divisors, prime_factorization, safe_eval, sub.
    
    # Strategy: 
    # Iterate through candidates. Check if candidate divides n using is_divisible.
    # If it does, check if the candidate itself is a "prime factor".
    # How to verify primality with available tools?
    # We can use positive_divisors(candidate). A number p > 1 is prime iff its only divisors are [1, p].
    
    n = frozen_params["n"]
    candidates = frozen_params["candidates"]
    
    correct_answer = None
    
    for c in candidates:
        if IntegerOps.is_divisible(n, c):
            # Check primality of c using positive_divisors
            divs = IntegerOps.positive_divisors(c)
            # If length is 2 and the last element equals c (and first is 1), it's prime.
            # Note: domain says inputs n>0 for positive_divisors. Candidates are >0 here.
            if len(divs) == 2 and divs[0] == 1 and divs[-1] == c:
                correct_answer = c
    
    return {
        "question_text": "下列整數 \(11,12,13,14\) 中，哪一個是 \(156\) 的質因數？",
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }