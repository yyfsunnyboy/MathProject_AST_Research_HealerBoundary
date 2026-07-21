def generate(level=1, **kwargs):
    candidates = kwargs.get("candidates", [11, 12, 13, 14])
    n = kwargs.get("n", 156)
    
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
    for candidate in candidates:
        while temp_n % candidate == 0 and is_prime(candidate):
            # Count multiplicity to ensure we use the full factorization power if needed, 
            # but typically "selection" implies finding which primes divide it.
            # Given n=156 = 2^2 * 3 * 13. Candidates are [11, 12, 13, 14].
            # Primes in candidates: 11 (no), 12 (no), 13 (yes), 14 (no).
            # Only 13 is a prime factor of 156.
            temp_n //= candidate
    
    correct_answer = sum(prime_factors) if prime_factors else None

    question_text = f"Find the product of all distinct prime factors from the list $candidates$ that divide $n$. \\\ncandidates: {candidates}\\\\nn= {n}"
    
    oracle_payload = {"candidates": candidates, "n": n}
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer if correct_answer is not None else 0, # Fallback for no factors found in list
        "oracle_payload": oracle_payload
    }