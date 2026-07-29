def generate(level=1, **kwargs):
    radicand = kwargs.get("radicand", 135)
    
    # Factorize radicand to simplify radical: sqrt(135) -> sqrt(9*15) -> 3*sqrt(15)
    import math
    
    def get_prime_factors(n):
        factors = {}
        d = 2
        while d * d <= n:
            while n % d == 0:
                factors[d] = factors.get(d, 0) + 1
                n //= d
            d += 1
        if n > 1:
            factors[n] = factors.get(n, 0) + 1
        return factors
    
    prime_factors = get_prime_factors(radicand)
    
    # Calculate coefficient and remaining radicand for simplified form sqrt(a * b) -> c * sqrt(b)
    coeff = 1
    new_radicand = 1
    for p, count in sorted(prime_factors.items()):
        if count % 2 == 0:
            q = count // 2
            coeff *= (p ** q)
        else:
            new_radicand *= (p ** (count % 2))
    
    # Construct LaTeX strings
    canonical_latex = f"\\sqrt{{{radicand}}}" if radicand == new_radicand and coeff == 1 else f"{coeff}\\sqrt{{{new_radicand}}}"
    
    question_text = f"Simplify the radical expression: {canonical_latex}."
    correct_answer = f"Coefficient: {coeff}, Radicand: {new_radicand}, Canonical LaTeX: {canonical_latex}"
    
    oracle_payload = {"radicand": radicand}
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }