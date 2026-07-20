def generate(level=1, **kwargs):
    """Generate a math problem instance for prime factor selection."""
    
    # Frozen sampled parameters as per specification
    candidates = [11, 12, 13, 14]
    n = 156
    
    oracle_payload = {
        "candidates": candidates,
        "n": n
    }
    
    # Determine the correct answer: find an element in candidates that divides n.
    # We select the largest such candidate to ensure a unique non-trivial solution if possible,
    or simply any valid one. Let's pick 13 as it is prime and divides 156 (156 = 12 * 13).
    
    correct_answer = None
    
    for c in candidates:
        if n % c == 0:
            correct_answer = c
            break
            
    # Fallback logic if no candidate works directly, though problem guarantees validity usually.
    # For this specific frozen set: 156 / 12 = 13 (integer), 156/13=12, others don't divide evenly? 
    # Wait: 156 % 11 != 0; 156 % 12 == 0; 156 % 13 == 0; 156 % 14 = 8.
    # There are two valid answers (12 and 13). The prompt implies a single correct_answer integer.
    # Usually in such tasks, we might pick the prime factor or just one of them. 
    # Let's assume the task expects *a* valid selection. We will return 13 as it is a prime factor often preferred in 'prime' contexts if applicable, 
    # but strictly mathematically both are factors. Given "prime_factor_selection" title context might imply picking primes?
    # However, 12 is not prime. The task name suggests selecting from candidates to form or be a factor.
    # Let's pick the first valid one found in sorted order of validity or just the largest for uniqueness if needed. 
    # To ensure deterministic behavior based on standard test patterns: let's return the largest divisor? Or smallest?
    # Without specific instruction, returning 13 (the prime) is a safe bet for "prime_factor" context.
    
    valid_factors = [c for c in candidates if n % c == 0]
    correct_answer = max(valid_factors) 
    
    question_text = f"Determine the largest integer from the list $\\{{ {', '.join(map(str, sorted(candidates)))} }}$ that divides evenly into ${n}$."

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }