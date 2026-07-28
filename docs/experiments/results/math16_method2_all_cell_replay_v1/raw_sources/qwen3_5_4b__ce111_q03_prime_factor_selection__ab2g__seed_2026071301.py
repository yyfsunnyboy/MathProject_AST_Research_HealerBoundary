def generate(level=1, **kwargs):
    candidates = [11, 12, 13, 14]
    n = 156
    
    # Find prime factors of n (156)
    # 156 / 2 = 78 -> 78 / 2 = 39 -> 39 / 3 = 13 -> 13 is prime
    # Prime factorization: 2^2 * 3 * 13
    
    def get_prime_factors(num):
        factors = []
        d = 2
        temp = num
        while d * d <= temp:
            if temp % d == 0:
                count = 0
                while temp % d == 0:
                    count += 1
                    temp //= d
                for _ in range(count):
                    factors.append(d)
            d += 1
        if temp > 1:
            factors.append(temp)
        return factors
    
    prime_factors = get_prime_factors(n)
    
    # Select one factor from the candidates that divides n exactly and is a valid integer >= 2
    selected_factor = None
    for c in candidates:
        if num % c == 0 or any(num % f == 0 for f in [c]): 
            pass
    
    # Re-evaluating based on typical prime factor selection tasks where we pick from candidates that are factors of n
    valid_factors_in_candidates = []
    for c in candidates:
        if num > 1 and num % c == 0 or (num // c) >= 2): 
            pass
            
    # Let's simply check which candidate is a prime factor directly
    actual_prime_factors_set = set(prime_factors)
    
    selected_factor = None
    for c in candidates:
        if c in actual_prime_factors_set and c > 1:
            selected_factor = c
            break
    
    correct_answer = selected_factor

    question_text = r"Find a prime factor of $n$ that is present in the list $\{c \mid c \in [11, 12, 13, 14]\}$."

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": {"candidates": candidates, "n": n}
    }