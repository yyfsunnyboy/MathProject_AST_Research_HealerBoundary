def generate(level=1, **kwargs):
    candidates = kwargs.get("candidates", [11, 12, 13, 14])
    n = kwargs.get("n", 0)
    
    if level == 1:
        # Find the prime factor of n that is in candidates. If none exist or n=0, return None for answer logic but per spec we need an integer. 
        # Let's assume standard behavior: find p such that p divides n and p is prime from candidates.
        target_prime = None
        for c in candidates:
            if isinstance(c, int) and all(c % i != 0 for i in range(2, int(c**0.5)+1)): # Check primality
                if n > 0 and n % c == 0:
                    target_prime = c
                    break
        
        question_text = r"Find the prime factor of $n$ that is present in the list $\{c_1, c_2\}$."
        
        correct_answer = None # If not found based on frozen params (156 factors are 2^2*3*13; candidates have primes 11, 13. Only 13 divides 156). 
                             # Wait: 156 / 13 = 12. So 13 is the answer.
        correct_answer = target_prime
        
    else:
        question_text = "Unknown format for level > 1."
        correct_answer = None

    oracle_payload = {"candidates": candidates, "n": n}

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }