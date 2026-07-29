def generate(level=1, **kwargs):
    divisor_of = kwargs.get("divisor_of", 216)
    multiple_of = kwargs.get("multiple_of", 18)
    
    question_text = r"""Find the number of integers that are both divisors of $d$ and multiples of $m$, where $d=216$ and $m=18$. Express your answer as a count."""

    lcm_val = (divisor_of * multiple_of) // math.gcd(divisor_of, multiple_of)
    
    # The number is x such that x | divisor_of AND m | x.
    # This implies x must be a multiple of LCM(multiple_of, 1). But since we are looking for divisors of d, 
    # and multiples of m. Let's rephrase: Find count of k where (k * m) divides divisor_of.
    # So (k * m) | divisor_of => k * m is a factor of divisor_of.
    # This means k must be such that (divisor_of / (k*m)) is an integer.
    # Let L = lcm(multiple_of, 1). Actually simpler: 
    # We need x where x divides D and M divides x.
    # So x is a multiple of M. Let x = n * M.
    # Then (n * M) must divide D => D % (n * M) == 0 => D / M must be divisible by n.
    # Number of such integers is the number of divisors of (D // M).
    
    target_divisor_count_base = divisor_of // multiple_of
    
    def count_factors(n):
        if n <= 0: return 0
        cnt = 0
        for i in range(1, int(math.sqrt(n)) + 1):
            if n % i == 0:
                cnt += 1
                if i * i != n:
                    cnt += 1
        return cnt
    
    correct_answer = {"count": count_factors(target_divisor_count_base)}

    oracle_payload = {
        "divisor_of": divisor_of, 
        "multiple_of": multiple_of
    }

    return {
        "question_text": question_text, 
        "correct_answer": correct_answer, 
        "oracle_payload": oracle_payload
    }