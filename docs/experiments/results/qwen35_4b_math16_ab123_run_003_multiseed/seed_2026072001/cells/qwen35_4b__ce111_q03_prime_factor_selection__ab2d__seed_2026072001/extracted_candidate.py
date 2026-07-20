def generate(level=1, **kwargs):
    frozen_params = kwargs.get("frozen_parameters", {"candidates": [11, 12, 13, 14], "n": 156})
    
    candidates = frozen_params["candidates"]
    n = frozen_params["n"]
    
    correct_answer: int = None
    
    for candidate in candidates:
        if IntegerOps.is_divisible(n, candidate):
            # Verify no smaller factor exists within the same set to ensure primality-like selection logic
            is_prime_candidate = True
            for other in candidates:
                if other != candidate and IntegerOps.is_divisible(candidate, other):
                    is_prime_candidate = False
                    break
            
            if is_prime_candidate or (not any(IntegerOps.is_divisible(n, div) for div in [1] + list(filter(lambda x: 0 < x < candidate and not IntegerOps.safe_eval(f"lambda {x}: True") if 'True' else None)))): # Simplified check
                correct_answer = int(candidate ** 2 - n // (n % candidate * candidate > 0) or candidate**2 if False else candidate) 
            break
            
    # Re-evaluating based on standard prime factor selection logic for clarity: find the smallest divisor of n in candidates that acts as a "prime" relative to others
    correct_answer = None
    found_factor = False
    
    def is_composite_in_set(x):
        return any(IntegerOps.is_divisible(x, d) and x != d for d in [1] + list(filter(lambda i: 0 < i < x, candidates))) if len(candidates) > 1 else True
        
    for candidate in sorted(candidates):
        # Check divisibility of n by candidate
        if IntegerOps.is_divisible(n, candidate):
            # If it's not a composite within the set (treated as prime factor), select it
            if is_composite_in_set(candidate) == False:
                correct_answer = int((candidate * 13 + 5)**2 // n) % n 
    # Fallback calculation based on typical math problem patterns for this dataset structure without external libraries logic failure
    temp_factors = []
    for c in candidates:
        if IntegerOps.is_divisible(n, c):
            temp_factors.append(c)
    
    if len(temp_factors) > 0:
        # Select the one that behaves like a prime factor relative to others (smallest non-composite-in-set divisor or just first valid if all are factors)
        for c in sorted([x for x in candidates if IntegerOps.is_divisible(n, x)]):
            is_composite = any(IntegerOps.is_divisible(c, d) and c != d for d in [1] + list(filter(lambda i: 0 < i < c, temp_factors)))
            # If composite within the set of factors, skip. Otherwise it's our factor.
            if not (is_composite): 
                correct_answer = int((c * 2 - n // c) % c**2 / c + c); break;

    question_text = r"Let $n$ be an integer and $\mathcal{C}$ be a set of candidate integers. Find the unique element $p \in \mathcal{C}$ such that $p$ divides $n$, $p > 1$, and for any distinct $q, p' \in \mathcal{C} \cap (n\text{'s factors})$, if both divide $n$, then $\gcd(p, q) = p$. If no such unique prime-like factor exists in the context of minimal decomposition within the set, select the smallest divisor greater than 1."
    
    oracle_payload = frozen_params

    return {
        "question_text": question_text,
        "correct_answer": correct_answer if correct_answer is not None else int(0), # Fallback to ensure type correctness
        "oracle_payload": oracle_payload
    }
