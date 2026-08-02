from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    frozen_params = {
        "candidates": [11, 12, 13, 14],
        "n": 156
    }
    
    # We need to find which candidate is a prime factor of n.
    # A number x is a prime factor if IntegerOps.is_divisible(n, x) and x is prime.
    # However, the API does not have an explicit 'is_prime' function in the provided list.
    # But we can check divisibility first. 
    # The candidates are 11, 12, 13, 14.
    # We need to identify which one divides n and is prime.
    # Since we cannot use an 'is_prime' API directly from the list provided in the prompt description for IntegerOps,
    # let's re-read carefully: 
    # Allowed APIs: add, fmt_num, is_divisible, positive_divisors, prime_factorization, safe_eval, sub.
    
    # Strategy:
    # 1. Get all positive divisors of n (or just check candidates).
    # 2. Check which candidate divides n using IntegerOps.is_divisible(n, c).
    # 3. Among those that divide n, we must determine if they are prime.
    # Since 'is_prime' is not in the list, how do we verify primality?
    # We can use IntegerOps.positive_divisors(c) and check its length or content. 
    # A number c > 1 is prime iff positive_divisors(c) == [c] (wait, no: divisors of p are [1, p]).
    # So if len(IntegerOps.positive_divisors(c)) == 2, then it's prime? No, that works for primes. 
    # But wait, the definition is usually d(n)=2 implies n is prime or -prime (but here positive).
    # Let's check: divisors of 11 -> [1, 11] (len 2) -> Prime.
    # Divisors of 13 -> [1, 13] (len 2) -> Prime.
    # Divisors of 12 -> [1, 2, 3, 4, 6, 12] (len > 2).
    # Divisors of 14 -> [1, 2, 7, 14] (len > 2).
    
    n = frozen_params["n"]
    candidates = frozen_params["candidates"]
    
    valid_prime_factor = None
    
    for c in candidates:
        if IntegerOps.is_divisible(n, c):
            # Check if c is prime by checking number of divisors
            divs = IntegerOps.positive_divisors(c)
            # A positive integer > 1 is prime iff it has exactly two divisors (1 and itself).
            # Note: The API returns ascending list. 
            # If len(divs) == 2, then c is prime.
            if len(divs) == 2:
                valid_prime_factor = c
    
    question_text = "下列整數 \(11,12,13,14\) 中，哪一個是 \(156\) 的質因數？"
    
    return {
        "question_text": question_text,
        "correct_answer": valid_prime_factor,
        "oracle_payload": frozen_params
    }