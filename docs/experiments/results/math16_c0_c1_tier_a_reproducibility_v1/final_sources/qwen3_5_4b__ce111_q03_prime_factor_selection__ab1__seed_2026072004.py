def generate(level=1, **kwargs):
    candidates = kwargs.get("candidates", [11, 12, 13, 14])
    n = kwargs.get("n", 156)
    
    def get_prime_factors(num):
        factors = []
        d = 2
        temp = num
        while d * d <= temp:
            if temp % d == 0:
                factors.append(d)
                while temp % d == 0:
                    temp //= d
            d += 1
        if temp > 1:
            factors.append(temp)
        return sorted(factors)
    
    all_factors = []
    for c in candidates:
        all_factors.extend(get_prime_factors(c))
    
    target_factorization = get_prime_factors(n)
    selected_factors = [f for f in target_factorization if f in set(all_factors)]
    
    correct_answer = sum(selected_factors)
    
    question_text = r"""Find the sum of prime factors that divide $n$ and are present in the list $\{11, 12, 13, 14\}$. Note: Only include distinct prime values.

Given: $n = \text{\(156\)}$, Candidates = $\text{\(\{11, 12, 13, 14\}\)}$"""
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": {"candidates": candidates, "n": n}
    }