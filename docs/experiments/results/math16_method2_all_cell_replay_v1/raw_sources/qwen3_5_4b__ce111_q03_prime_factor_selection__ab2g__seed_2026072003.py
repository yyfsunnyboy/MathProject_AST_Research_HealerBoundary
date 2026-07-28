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
    
    # Select one factor from the candidates that divides n
    selected_factor = None
    for c in candidates:
        if n % c == 0 and c != 1:
            selected_factor = c
            break
            
    correct_answer = selected_factor
    
    question_text = f"Find a prime number $p$ such that $p \in \\{\\text{{candidates}}\\}$ divides the integer $n$. The set of candidates is given as [11, 12, 13, 14] and $n = {n}$. What is one valid value for $p$?"
    
    oracle_payload = {"candidates": candidates, "n": n}
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }