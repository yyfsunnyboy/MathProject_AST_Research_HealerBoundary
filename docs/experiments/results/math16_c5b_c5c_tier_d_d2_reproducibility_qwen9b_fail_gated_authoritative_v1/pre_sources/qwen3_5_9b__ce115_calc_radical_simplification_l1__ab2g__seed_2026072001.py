def generate(level=1, **kwargs):
    radicand = kwargs.get("radicand", 27)
    
    # Factorization for simplification: 27 = 3^3 * 1 (or just 3^3 if we consider perfect cubes directly inside radical)
    # sqrt(27) -> simplify to 3*sqrt(3). 
    # However, the task is "radical_simplification_l1". Usually this implies simplifying a square root.
    # Let's assume standard form: k * sqrt(n).
    # For radicand = 27 (which is 9*3), sqrt(27) = 3*sqrt(3).
    
    import math
    
    def simplify_radical(r):
        if r <= 0:
            return None, None
        
        # Find largest square factor k^2 such that n = k^2 * m
        simplified_radicand = r
        coefficient = 1
        
        for i in range(5, -1, -1): # Check squares from 25 down to 1 (since sqrt is involved)
            sq = i ** 2
            if sq <= simplified_radicand:
                count = 0
                temp = simplified_radicand
                while temp % sq == 0 and int(math.sqrt(temp)) == math.isqrt(temp): # Check divisibility by square? No, simpler logic.
                    pass
                
        # Better approach for integer radicands in sqrt context (level 1 usually implies square roots)
        # Find largest perfect square factor d such that r = d * m where d is a perfect square > 0
        simplified_radicand = r
        coefficient = 1
        
        for i in range(2, int(math.sqrt(r)) + 1):
            count = 0
            while (r % (i*i) == 0):
                r //= (i*i)
                count += 1
            
            if count > 0:
                coefficient *= i ** count
        
        # If the original number was a perfect square, radicand becomes 1 and coeff is sqrt(original). 
        # But usually canonical form keeps integer inside. Let's refine logic for standard simplification.
        
    # Re-implementing simplify correctly without complex loops first:
    def get_simplified_form(n):
        if n <= 0: return None, None
        
        simplified_radicand = n
        coefficient = 1
        
        d = 2
        while d * d <= simplified_radicand:
            count = 0
            while (simplified_radicand % (d*d) == 0): # This checks if we can pull out a pair? No, standard is to check divisibility by square.
                pass
            
            # Correct logic: Check how many times d divides n, then take floor(count/2).
            temp = simplified_radicand
            count_d = 0
            while temp % d == 0:
                count_d += 1
                temp //= d
            
            if count_d >= 2:
                pull_out_count = count_d // 2
                coefficient *= (d ** pull_out_count)
                simplified_radicand = int(temp * (simplified_radicand / (temp))) # Wait, logic error above.
        
        # Let's restart the simplification function cleanly inside generate to avoid state issues
        
    def simplify(n):
        if n <= 0: return None, None
        temp_n = n
        coeff = 1
        d = 2
        while d * d <= temp_n:
            count = 0
            while temp_n % (d*d) == 0 and int(temp_n / (d*d)) < temp_n: # This is wrong. 
                pass
            
            # Correct standard algorithm:
            cnt = 0
            curr = n
            for p in range(2, int(n**0.5)+1):
                c = 0
                while curr % p == 0:
                    c += 1
                    curr //= p
                if c >= 2:
                    coeff *= (p ** (c // 2))
            # Handle remaining prime factor in 'curr' which is < d*d, so it's square free.
            
        return coefficient, simplified_radicand

    # Actually, let's just hardcode the logic for specific input or generic loop properly:
    
    def calc_simplified(n):
        if n <= 0: return None, None
        
        temp = n
        coeff = 1
        
        d = 2
        while d * d <= temp:
            count = 0
            while (temp % (d*d) == 0 and int(temp / (d**2)) < temp): # No. 
                pass
            
            # Proper factorization loop
            cnt = 0
            curr_temp = n
            for p in range(2, int(n**0.5)+1):
                c = 0
                while curr_temp % p == 0:
                    c += 1
                    curr_temp //= p
                if c >= 2:
                    coeff *= (p ** (c // 2))
            
            # The remaining part in curr_temp is square-free. 
            # But wait, the loop above modifies curr_temp but I need to multiply back? No.
            # Let's do it simply: factorize n completely into primes p1^e1 * ... then coeff = product(pi^(ei//2)), radicand = product(pi^(ei%2)).
            
        return None

    def get_canonical_form(n):
        if n <= 0: return None, None
        
        # Factorization
        temp_n = n
        factors = {}
        
        d = 2
        while d * d <= temp_n:
            while temp_n % d == 0:
                factors[d] = factors.get(d, 0) + 1
                temp_n //= d
            d += 1
        
        if temp_n > 1:
            factors[temp_n] = factors.get(temp_n, 0) + 1
            
        coeff = 1
        radicand = 1
        
        for p, exp in factors.items():
            pull_out = exp // 2
            remaining = exp % 2
            if pull_out > 0:
                coeff *= (p ** pull_out)
            if remaining == 1:
                radicand *= p
                
        return coeff, radicand

    # Apply to frozen parameter or default
    n_val = kwargs.get("radicand", 27)
    
    coefficient, simplified_radicand = get_canonical_form(n_val)
    
    canonical_latex = f"{coefficient}\\sqrt{{{simplified_radicand}}}" if (coeff != 1 and simplified_radicand > 0) else f"\\sqrt{{{n_val}}" # Wait, if coeff is 1, latex usually omits it or writes just sqrt. 
    # Standard canonical form: k * sqrt(n). If k=1, write \\sqrt{n}.
    
    final_latex = ""
    if coefficient == 1 and simplified_radicand > 0:
        final_latex = f"\\sqrt{{{simplified_radicand}}}"
    elif coefficient != 1 or (coefficient == 1 and simplified_radicand <= 0): # Should not happen for positive input
         pass 
    else:
        if coefficient == 1:
             # This case handled above. What if n=4? coeff=2, rad=1 -> 2\\sqrt{1} = 2. Usually we write integer result if radicand is 1.
             final_latex = f"{coefficient}" 
         else:
             final_latex = f"{coefficient}\\sqrt{{{simplified_radicand}}}"

    # Correction for perfect squares resulting in integers (radicand=1)
    if simplified_radicand == 1 and coefficient > 0:
        canonical_latex = str(coefficient)
    else:
        if coefficient == 1:
            canonical_latex = f"\\sqrt{{{simplified_radicand}}}"
        else:
            canonical_latex = f"{coefficient}\\sqrt{{{simplified_radicand}}}"

    question_text = (f"Simplify the radical expression $\\\\sqrt{{{n_val}}}$. "
                     f"The simplified form is of the shape $k\\\\sqrt{n}$ where $n$ has no perfect square factors greater than 1. "
                     f"Provide your answer in LaTeX format.")
    
    # Ensure correct_answer matches canonical_latex exactly as a string for grading, but also ensure it's valid math representation.
    # The prompt asks: correct_answer must include coefficient, radicand, and canonical_latex. 
    # It implies the value of correct_answer IS the canonical_latex? Or a dict? "return a dict with ... correct_answer". Usually correct_answer is the string to compare against.
    
    return {
        "question_text": question_text,
        "correct_answer": canonical_latex,
        "oracle_payload": {"radicand": n_val}
    }