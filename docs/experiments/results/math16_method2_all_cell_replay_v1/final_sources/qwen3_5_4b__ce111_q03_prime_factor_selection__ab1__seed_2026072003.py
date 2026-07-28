def generate(level=1, **kwargs):
    candidates = [11, 12, 13, 14]
    n = 156
    
    # Find prime factors of n that are in the candidate list
    def is_prime(num):
        if num < 2:
            return False
        for i in range(2, int(num**0.5) + 1):
            if num % i == 0:
                return False
        return True
    
    prime_factors = []
    temp_n = n
    for c in candidates:
        while temp_n > 1 and temp_n % c == 0:
            # Check if candidate is actually a factor (it must be)
            # We only care about primes from the list that divide n
            prime_factors.append(c)
            temp_n //= c
    
    correct_answer = sum(prime_factors)
    
    return {
        "question_text": r"Find the sum of all distinct prime factors of $n$ where each factor is present in the set $\{11, 12, 13, 14\}$. Given that $n = 156$, what is this sum?",
        "correct_answer": correct_answer,
        "oracle_payload": {"candidates": candidates, "n": n}
    }