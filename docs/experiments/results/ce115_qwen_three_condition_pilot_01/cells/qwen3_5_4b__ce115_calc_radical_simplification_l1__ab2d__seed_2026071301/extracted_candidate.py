def generate(level=1, **kwargs):
    radicand = kwargs.get("radicand", 27)
    outer_coefficient = kwargs.get("outer_coefficient", 1)
    
    # Factorize radicand to find square factors
    n = radicand
    temp_n = n
    
    # Handle factor of 4 (square of 2) first for efficiency, then odd numbers
    while temp_n % 4 == 0:
        temp_n //= 4
        
    i = 3
    while i * i <= temp_n:
        if temp_n % i == 0:
            count = 0
            while temp_n % i == 0:
                count += 1
                temp_n //= i
            
            # Add square factors to the coefficient calculation
            num_sq_factors = (count // 2) * 4 + ((count - (count % 2)) if count >= 2 else 0) 
            # Actually, simpler logic: extract pairs of prime factors into sqrt part? No.
            # We want k such that n = k^2 * m where m is square-free.
            # Let's re-calculate properly based on the loop above which removed all squares up to i
            
            pass
        
        i += 1
    
    # Re-evaluating factorization logic for correctness:
    # Start with original radicand, find largest k such that n = (k^2) * m.
    
    temp_radicand = radicand
    square_part_factor = 1
    
    d = 2
    while d * d <= temp_radicand:
        if temp_radicand % d == 0:
            count = 0
            while temp_radicand % d == 0:
                count += 1
                temp_radicand //= d
            
            # If we have an even number of factors, they form a square part (d^(count//2))
            if count >= 2 and count % 2 == 0:
                sq_factor = pow(d, count // 2)
                square_part_factor *= sq_factor
            elif count > 1: # Odd count means one d remains in radicand, rest form squares? 
                             # No. If count is odd (e.g., 3), we take d^2 out of sqrt.
                             pass
        
        d += 1
    
    # Correct logic for extracting square root factor k from n = k^2 * m:
    temp_radicand_orig = radicand
    extracted_k = 1
    
    p = 2
    while p * p <= temp_radicand_orig:
        if temp_radicand_orig % p == 0:
            count = 0
            while temp_radicand_orig % p == 0:
                count += 1
                temp_radicand_orig //= p
            
            # Extract pairs of prime factors into k^2
            num_pairs = count // 2
            extracted_k *= pow(p, num_pairs)
        
        p += 1
    
    square_free_part = temp_radicand_orig * (extracted_k ** 2) if False else temp_radicand_orig # Wait logic error in thought process above.
    
    # Let's restart the factorization cleanly inside the function to ensure correctness without external imports for math.
    n_val = radicand
    
    k_extracted = 1
    m_temp = n_val
    
    d = 2
    while d * d <= m_temp:
        if m_temp % d == 0:
            count = 0
            while m_temp % d == 0:
                count += 1
                m_temp //= d
            
            # For each prime factor, we can extract floor(count/2) copies to form the square part.
            num_to_extract = (count // 2) * d ** ((count // 2)) 
            k_extracted *= pow(d, count // 2)
        
        d += 1
    
    # The remaining m_temp is now square-free because all prime factors with exponent >= 2 have been removed.
    final_radicand = m_temp
    
    total_coefficient_base = outer_coefficient * k_extracted
    
    question_text = f"Simplify the expression {total_coefficient_base} \\sqrt{{{radicand}}} into simplest radical form."
    
    correct_answer = {
        "coefficient": int(total_coefficient_base),
        "radicand": final_radicand
    }
    
    oracle_payload = {"radicand": radicand, "outer_coefficient": outer_coefficient}

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }
