def generate(level=1, **kwargs):
    candidates = kwargs.get("candidates", [11, 12, 13, 14])
    n = kwargs.get("n", 156)
    
    # Find prime factors of n that are in the candidate list
    target_factors = []
    temp_n = n
    
    for c in candidates:
        if temp_n % c == 0 and c > 1:
            count = 0
            while temp_n % c == 0:
                count += 1
                temp_n //= c
            
            # Only include the prime itself, not powers, as per standard factor selection tasks unless specified otherwise.
            # However, looking at n=156 and candidates [11, 12, 13, 14]:
            # 156 = 2 * 2 * 3 * 13
            # Only 13 is a prime in the candidate list.
            # If the task implies selecting primes from the set that divide n:
            
    if temp_n == 1 and len(target_factors) > 0:
        correct_answer = target_factors[0]
    else:
        # Re-evaluating based on standard "prime factor selection" logic where we pick prime factors present in candidates.
        # Primes in [11, 12, 13, 14]: 11 (no), 12 (no), 13 (yes), 14 (no).
        # Only 13 is a prime factor of 156? 
        # Wait, maybe the task allows composite candidates if they are factors? 
        # But "prime_factor_selection" implies primes.
        # Let's check standard interpretations for ce111_q03: usually it asks to sum or find specific factors.
        # Given n=156 = 2^2 * 3 * 13.
        # Candidates containing actual prime factors of n: only {13}.
        # If the question is "select all primes from candidates that divide n", answer is [13] -> sum? product? 
        # Usually these tasks ask for a single integer result like the sum or count, but spec says "single exact integer".
        # Let's assume it asks for the sum of such factors. Sum = 13.
        
        # Alternative interpretation: Maybe I need to find primes in candidates that divide n? 
        # Or maybe factorize using only these candidates as divisors?
        # If we strictly follow "prime_factor_selection", we look for prime numbers in `candidates` that are factors of `n`.
        # Primes in [11, 12, 13, 14]: 11 is not a factor (156/11 = 14.18), 13 IS a factor.
        # Result could be the prime itself: 13. Or sum of them: 13. Or count: 1.
        # Given "single exact integer", and typical difficulty level 1, it's likely just the value or its simple aggregation. 
        # Let's assume the question asks for the product of such primes? No, usually sum in these specific generated tasks if multiple exist. Here only one exists.
        
        correct_answer = target_factors[0]

    oracle_payload = {
        "candidates": candidates,
        "n": n
    }

    return {
        "question_text": f"Find the product of all prime factors from the given list that divide \\({n}\\).",
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }