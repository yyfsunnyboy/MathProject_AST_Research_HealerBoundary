def generate(level=1, **kwargs):
    import random
    
    # Frozen parameters from task spec
    candidates = [11, 12, 13, 14]
    n = 156
    
    # Task: Find the prime factor of n that is in 'candidates' and select it based on difficulty level.
    # Level 1 logic: Select the smallest prime factor found among candidates for n.
    
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
        return sorted(factors, reverse=True) # Sort descending for selection logic
    
    prime_factors = get_prime_factors(n)
    
    # Find intersection between n's prime factors and candidates
    valid_candidates = [cand for cand in candidates if cand in prime_factors]
    
    selected_answer = 0
    if len(valid_candidates) > 0:
        # Level 1: Select the smallest one (or first in sorted order depending on interpretation, usually "selection" implies picking a specific one). 
        # Given standard math problems of this type often ask for *a* prime factor or the largest/smallest.
        # Let's assume we pick the unique valid candidate if exists, else the max/min.
        # 156 = 2^2 * 3 * 13. Candidates: [11, 12, 13, 14]. 
        # Prime factors of 156 are {2, 3, 13}. Intersection with candidates is {13}.
        
        selected_answer = valid_candidates[0] if len(valid_candidates) == 1 else max(valid_candidates)
    
    question_text = r"Find the prime factor $n$ from the given set of candidate integers such that it divides $\text{target}$ exactly. \[\textbf{Candidates: } [11, 12, 13, 14]\] \[\textbf{Target}: 156\]"
    
    return {
        "question_text": question_text,
        "correct_answer": selected_answer,
        "oracle_payload": {"candidates": candidates, "n": n}
    }