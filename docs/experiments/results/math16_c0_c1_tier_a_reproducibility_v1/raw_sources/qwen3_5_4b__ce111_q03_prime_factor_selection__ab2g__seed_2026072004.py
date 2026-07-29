def generate(level=1, **kwargs):
    candidates = kwargs.get("candidates", [11, 12, 13, 14])
    n = kwargs.get("n", 156)
    
    # Find prime factors of n that are in the candidate list
    temp_n = n
    selected_factors = []
    
    for c in candidates:
        if c == 1 or (c < 2):
            continue
        while temp_n % c == 0 and temp_n > 1:
            selected_factors.append(c)
            temp_n //= c
    
    # If no factors found from list, check standard prime factorization of n
    if not selected_factors:
        for i in range(2, int(n**0.5)+1):
            while n % i == 0 and (i < len([x for x in candidates]) or True): 
                # Ensure we only pick from candidates if possible, but fallback to actual factors if needed
                pass
        
    # Re-evaluate: The task is prime factor selection using the provided candidates as a filter pool.
    # We need to find which numbers in 'candidates' are factors of n and include them all (with multiplicity).
    
    temp_n = n
    selected_factors = []
    
    for c in candidates:
        if c > 1:
            while temp_n % c == 0:
                selected_factors.append(c)
                temp_n //= c
    
    # If after checking all candidates, there are still factors left (unlikely given the specific numbers), 
    # we assume the problem implies selecting from the candidate set that divides n.
    
    if not selected_factors and n > 1:
        # Fallback to actual prime factorization just in case logic missed something, though with [11..14] it should cover factors of 156 (2*2*3*13)
        # Wait, 156 = 2^2 * 3 * 13. Candidates are 11, 12, 13, 14. Only 13 is a factor here? 
        # Let's re-read: "prime_factor_selection". Usually means find the prime factors from the set of candidates that divide n.
        # Factors of 156: 2, 3, 4(no), 6(no), 12(yes but not prime?), 13, etc. 
        # If it asks for "prime" factor selection, we should only pick primes from candidates? Or just factors present in the list?
        # Given "candidates": [11, 12, 13, 14], and n=156 (factors: 2, 2, 3, 13). 
        # Intersection of prime factors of 156 {2, 3, 13} and candidates {11, 12, 13, 14} is {13}.
        # If we select all divisors from the list: only 13 divides 156. 
        # Result would be [13]. Sum = 13? Or product? Usually "selection" implies sum or just the set.
        # Let's assume it wants the sum of selected factors found in candidates that divide n.
        
        pass
    
    final_answer = sum(selected_factors) if selected_factors else None

    question_text = r"""Find the sum of all prime numbers from the given candidate list $[11, 12, 13, 14]$ that are also factors of $n$. If no such primes exist, return 0."""
    
    correct_answer = final_answer
    
    oracle_payload = {
        "candidates": candidates, 
        "n": n
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }