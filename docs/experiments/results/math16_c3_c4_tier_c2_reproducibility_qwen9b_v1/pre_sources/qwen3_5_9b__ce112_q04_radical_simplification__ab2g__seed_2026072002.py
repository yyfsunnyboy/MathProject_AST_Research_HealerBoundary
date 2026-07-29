def generate(level=1, **kwargs):
    radicand = kwargs.get("radicand", 135)
    
    # Factorize radicand to simplify radical: sqrt(135) = sqrt(9*15) = 3*sqrt(15)
    import math
    
    def get_prime_factors(n):
        factors = {}
        d = 2
        while d * d <= n:
            while n % d == 0:
                factors[d] = factors.get(d, 0) + 1
                n //= d
            d += 1
        if n > 1:
            factors[n] = factors.get(n, 0) + 1
        return factors
    
    prime_factors = get_prime_factors(radicand)
    
    # Calculate coefficient and remaining radicand for simplified radical form sqrt(a*b^2*c...) -> b*sqrt(ac...)
    coeff = 1
    new_radicand = 1
    
    for p, exponent in sorted(prime_factors.items()):
        if exponent % 2 == 0:
            # Even power comes out completely as part of coefficient? 
            # Wait, standard simplification: sqrt(p^k) where k is even -> p^(k/2). If odd -> p^((k-1)/2)*sqrt(p)
            # Actually for general radical simplification sqrt(n): we pull out pairs.
            count = exponent // 2
            coeff *= (p ** count)
        else:
            # Odd power: one remains inside, rest come out
            count = (exponent - 1) // 2
            new_radicand *= (p ** count)
    
    # Re-evaluate logic for standard simplification sqrt(n):
    # We want to write n = s^2 * r where r is square-free. Then sqrt(n) = s*sqrt(r).
    # To find s: take product of p^(floor(exponent/2)) for each prime factor? No.
    # Actually, if exponent is k, we pull out floor(k/2) copies of the base? 
    # Example: 135 = 3^3 * 5^1. sqrt(3^3*5) = sqrt(3^2 * 3 * 5) = 3 * sqrt(15).
    # So for each prime p with exponent e, we pull out p^(e//2)? No, that would be wrong if e=3 -> pulls 3^1? 
    # Wait: 3^3. floor(3/2)=1. We pull out 3^1? But 3^2 is the square part.
    # Correct logic: The largest square divisor d = product(p^(e - (e%2))). Then s = sqrt(d). r = n/d.
    
    def simplify_radical(n):
        if n <= 0:
            return None, None, None
        
        factors = get_prime_factors(abs(n))
        
        # Calculate the square part and remaining non-square part
        square_part = 1
        remainder_radicand = 1
        
        for p in sorted(factors.keys()):
            exponent = factors[p]
            
            if exponent % 2 == 0:
                # Even power, all comes out as sqrt(p^e) = p^(e/2). But we want to keep it simple.
                # Actually standard form is coefficient * sqrt(square_free_part).
                # If e=4 -> p^4 inside -> p^2 outside. Square part contributes p^2 to coeff? 
                # No, let's stick to: pull out pairs.
                count_out = exponent // 2
                square_root_factor = (p ** count_out) if count_out > 0 else 1
                remainder_radicand *= (p ** (exponent % 2))
            else:
                # Odd power, e.g., p^3 -> sqrt(p^3)=p*sqrt(p). Pull out one p.
                count_out = exponent // 2
                square_root_factor = (p ** count_out) if count_out > 0 else 1
                remainder_radicand *= (p ** (exponent % 2)) # which is p^(e-1) effectively since e%2=1
                
            coeff_part = square_root_factor
        
        # Wait, my loop logic above was flawed. Let's restart the simplification function cleanly.
        
    def get_simplified_radical(n):
        if n <= 0: return None, None, None
        factors = get_prime_factors(abs(n))
        coefficient = 1
        radicand_part = 1
        
        for p in sorted(factors.keys()):
            exponent = factors[p]
            
            # Number of pairs we can pull out is floor(exponent / 2)
            num_pairs = exponent // 2
            
            if num_pairs > 0:
                coefficient *= (p ** num_pairs)
                
                # The remaining part inside the radical is p^(exponent % 2)
                remainder_exp = exponent % 2
                radicand_part *= (p ** remainder_exp)
        
        return coefficient, abs(radicand), f"{coefficient}\\sqrt{{{radicand}}}" if radicand > 1 else str(coefficient).replace(" ", "")

    # Re-run simplification for the specific frozen parameter or general case? 
    # The task says "frozen sampled parameters: {"radicand": 135}".
    # But generate() should probably work generally, using kwargs if provided.
    # However, to strictly follow "oracle_payload must exactly equal the frozen sampled parameters",
    # we use the radicand from kwargs or default.
    
    current_radicand = kwargs.get("radicand", 135)
    
    coeff_val, final_rad, latex_expr = get_simplified_radical(current_radicand)
    
    if coeff_val is None:
        return {"question_text": "", "correct_answer": "", "oracle_payload": {}}
        
    # Construct question text with LaTeX delimiters
    q_text = f"Simplify the radical expression $\\sqrt{{{current_radicand}}}$. Express your answer in simplest form as a coefficient times a square root."
    
    correct_ans_str = latex_expr
    
    oracle_data = {"radicand": current_radicand}
    
    return {
        "question_text": q_text,
        "correct_answer": correct_ans_str,
        "oracle_payload": oracle_data
    }