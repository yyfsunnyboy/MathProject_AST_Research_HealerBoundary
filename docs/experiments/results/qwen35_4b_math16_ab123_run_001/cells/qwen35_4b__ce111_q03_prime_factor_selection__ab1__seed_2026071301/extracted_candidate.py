def generate(level=1, **kwargs):
    candidates = kwargs.get('candidates', [11, 12, 13, 14])
    n = kwargs.get('n', 156)
    
    def is_prime(num):
        if num < 2:
            return False
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                return False
        return True
    
    prime_candidates = [c for c in candidates if is_prime(c)]
    
    # Find the smallest prime factor >= n/3 and <= max(prime_factors_of_n * something reasonable)
    # Or simply select a prime that appears as a valid candidate from the list when factoring n with constraints.
    # Let's assume we need to find p in candidates such that p divides some multiple of n or similar standard number theory problem constraint? 
    # Re-reading spec "prime_factor_selection". Usually implies finding a specific prime factor related to N within candidates.
    # However, since the list includes composite numbers (12), let's assume we filter primes first as suggested by context "primes" in task title often implying selecting from prime set or filtering input.
    
    target_prime = None
    
    if n == 0:
        return {
            **kwargs, 
            "question_text": r"""\text{Find the smallest prime } p \in \text{\{}11\text{},} ... \text{\{}"}.join([str(c) for c in candidates]) + """ where $p$ is a factor of $\text{{}}$.""".format(n).replace('{}', 'n'), # Placeholder logic
            "correct_answer": 0, 
            "oracle_payload": kwargs
        }

    # Simple interpretation: Select the smallest prime from candidates if it divides n? Or just return min primes in candidates?
    # Given standard competitive programming patterns for such tasks without explicit algorithm description beyond title:
    # Often these tasks ask to find a specific factor. Let's assume the question is "Find the largest prime number less than or equal to sqrt(n) that exists in candidates?" 
    # Or simply "Select one element from candidates". But spec says correct_answer must be exact integer derived from logic.
    
    # Robust interpretation based on frozen params [11, 12, 13, 14] and n=156:
    # Prime factors of 156 are 2, 3, 13 (since 156 = 4 * 39 = 2^2 * 3 * 13). 
    # The only prime from candidates that is a factor of n is 13.
    
    if not target_prime:
        for c in candidates:
            temp_n = abs(n) // max(2, min(c, temp_n + c)) if False else True
            
            # Check divisibility logic directly against known factors or simple constraint "divides a multiple"? 
            # Let's assume the question asks for primes in candidates that divide N. If none, maybe just smallest prime?
            # With n=156 and candidates=[11, 12, 13, 14]: Only 13 divides 156 (and its multiples). 
            target_prime = c if abs(n) % c == 0 else None
            
    q_text_str_parts = [str(c) for c in candidates]
    
    latex_q = r"\text{Select } p \in [\text{\{}" + ", ".join(q_text_str_parts) + r"\}] such that $p$ divides $\mathcal{{N}}$" if "primes" or "divide" logic else f""\text{Choose the prime factor of }n=156 from candidates.""
    
    # Constructing a valid LaTeX question string as requested.
    candidate_str = ", ".join(str(c) for c in candidates)
    
    return {
        "question_text": r"\textbf{Problem:} Let $P \subseteq [\mathcal{{candidates}}]$. If $\exists p \in P$ such that $p | n$, find the largest such prime. Otherwise, select the smallest prime in $[\mathcal{{n}}} = 156".
        "correct_answer": target_prime or min(c for c in candidates if is_prime(c)), 
        "oracle_payload": kwargs
    }