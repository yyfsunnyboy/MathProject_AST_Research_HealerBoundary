from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    frozen_params = {
        "candidates": [11, 12, 13, 14],
        "n": 156
    }
    
    # We need to find which candidate is a prime factor of n.
    # A number x is a prime factor if:
    # 1. It divides n (IntegerOps.is_divisible(n, x))
    # 2. It is prime. Since the domain API doesn't have an explicit "is_prime" function 
    # that returns bool directly for checking primality of arbitrary numbers in one go without side effects,
    # we can rely on IntegerOps.prime_factorization(x). If it has exactly one entry and its exponent is 1 (or just check if the factorization result matches x), or simpler:
    # We know candidates are small. Let's use prime_factorization to verify primality implicitly? 
    # Actually, a number > 1 with no divisors other than 1 and itself is prime.
    # However, IntegerOps.prime_factorization returns {prime: exponent}. If we pass x, the keys should be just [x] if it's prime (and x>0).
    
    n = frozen_params["n"]
    candidates = frozen_params["candidates"]
    
    correct_answer = None
    
    for c in candidates:
        # Check divisibility first to save computation on non-divisors, though is_divisible handles b=0 gracefully.
        if IntegerOps.is_divisible(n, c):
            # Now check if 'c' itself is prime using its factorization signature
            factors = IntegerOps.prime_factorization(c)
            # If c is composite, it will have multiple keys or a key different from c (unless c=1 which isn't in list).
            # For a prime p > 1, the dict should be {p: 1}. The only key must equal c.
            if len(factors) == 1 and factors[c] == 1:
                correct_answer = c
    
    return {
        "question_text": "下列整數 \(11,12,13,14\) 中，哪一個是 \(156\) 的質因數？",
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }