def generate(level=1, **kwargs):
    candidates = [11, 12, 13, 14]
    n = 156
    
    correct_answer = None
    for candidate in candidates:
        temp_n = n
        count = 0
        divisor = candidate
        
        while temp_n > 1 and divisor <= temp_n:
            if temp_n % divisor == 0:
                count += 1
                temp_n //= divisor
            
        # Check if the product of all prime factors equals original n
        current_product = 1
        for c in candidates:
            t_temp = candidate
            p_count = 0
            d = 2
            while t_temp > 1 and d <= t_temp:
                if t_temp % d == 0:
                    p_count += 1
                    temp_val = t_temp // d
                    # Reconstruct logic to check prime factorization count or sum?
                    # Let's re-evaluate based on standard "prime factor selection" tasks.
                    # Usually it asks for the number of distinct prime factors, 
                    # or a specific property derived from them.
                    
            pass
        
        # Simple heuristic: Find candidate that relates to n=156 via primes in candidates list [11, 13] (since they are prime)
        # 156 = 2 * 2 * 3 * 13
        # Candidate must be one of the factors or related. 
        # If we assume the task is "find x such that x divides n and x is in candidates":
        # 156 % 11 != 0, 156 % 12 = 13*12 (no), 156 % 13 == 0. 
        # So answer might be 13.
        
        if n % candidate == 0:
            correct_answer = candidate

    question_text = r"Given the integer $n=156$ and a set of candidates $\{11, 12, 13, 14\}$, determine which element from the candidates is a prime factor of $n$. Express your answer as an integer."
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": {"candidates": [11, 12, 13, 14], "n": 156}
    }