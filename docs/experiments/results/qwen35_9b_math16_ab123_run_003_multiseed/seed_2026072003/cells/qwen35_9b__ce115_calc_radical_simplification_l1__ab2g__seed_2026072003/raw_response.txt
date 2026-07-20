def generate(level=1, **kwargs):
    import copy
    
    # Frozen sampled parameters provided in task specification context
    frozen_params = {"radicand": 27}
    
    # Ensure we use exactly these frozen parameters as per oracle_payload requirement
    current_oracle_payload = copy.deepcopy(frozen_params)
    
    radicand_value = current_oracle_payload["radicand"]
    
    # Task: Radical simplification for level 1 (difficulty 1)
    # Input expression will be the radical of the frozen radicand.
    # We need to simplify sqrt(radicand).
    # For 27, sqrt(27) = sqrt(9*3) = 3*sqrt(3).
    
    # Factorization logic for simplification:
    # Find largest square factor of radicand_value
    
    def find_largest_square_factor(n):
        """Returns (square_part, remainder) where n = square_part * remainder and remainder is square-free."""
        if n == 0:
            return (1, 0)
        
        factors = {}
        d = 2
        temp_n = n
        
        while d * d <= temp_n:
            while temp_n % d == 0:
                factors[d] += 1
                temp_n //= d
            d += 1
        
        if temp_n > 1:
            factors[temp_n] += 1
            
        # Construct square part and remainder
        square_part = 1
        for base, exponent in sorted(factors.items()):
            count_pairs = exponent // 2
            if count_pairs == 0:
                continue
            square_part *= (base ** count_pairs) * (base ** count_pairs) # Actually we want the full squared part inside
        
        # Re-calculate properly: 
        # We want n = s^2 * r where r is square-free.
        # The largest square factor corresponds to taking min(floor(exp/2), floor((exp+1)/2)) pairs? No.
        # Correct logic: For each prime p with exponent e, the contribution to square part is p^(2*(e//2)).
        
        final_square_part = 1
        for base in sorted(factors.keys()):
            exp = factors[base]
            count_in_sqrt = (exp // 2) * 2 # The power inside the perfect square we can extract
            if count_in_sqrt > 0:
                final_square_part *= (base ** (count_in_sqrt))
        
        remainder = n // final_square_part
        
        return (final_square_part, remainder)

    sq_part, rem = find_largest_square_factor(radicand_value)
    
    # Simplified form: coefficient * sqrt(remainder)
    if rem == 1:
        coeff = radicand_value ** 0.5 # This would be integer but let's compute via int math to avoid float issues in logic, though result is rational/integer here? 
        # Actually for perfect squares, remainder is 1, coefficient is sqrt(n). But task says exact integers only.
        # If rem == 1, the answer is just an integer (coefficient) times sqrt(1)? Or just the integer?
        # Standard form usually keeps it as coeff * sqrt(rem). If rem=1, typically we write just the number or coeff*sqrt(1). 
        # However, canonical latex for simplified radical often implies non-perfect squares. But let's stick to formula: a*b^c -> a*sqrt(b)
        if sq_part == radicand_value:
             # Perfect square case. Usually represented as integer? Or 3*sqrt(9)? No. 
             # Let's assume standard simplification removes perfect squares entirely, leaving just the root of remaining part.
             # If rem=1, then sqrt(n) = int(sqrt(n)). We can represent this as coefficient * sqrt(1) or just number?
             # The prompt asks for "coefficient, radicand, and canonical_latex". 
             # Let's output coeff=sqrt_value if perfect square else 0*sqrt(...) ? No.
             # If n is a perfect square k^2, then sqrt(n)=k. We can write this as k * sqrt(1) to fit the template or just handle it specially?
             # Given "exact integers", let's try to express perfectly simplified radicals. 
             # Convention: if radicand becomes 1 under root, we usually drop the radical sign and keep integer. 
             # BUT the fields require 'coefficient', 'radicand'. If I output coeff=27, radicand=0? No.
             # Let's assume for perfect squares, we set coefficient = sqrt(n), radicand = 1 (conceptually) or handle as special case where latex is just number.
             # However, the instruction says "correct_answer must include coefficient, radicand...". 
             # If I write "3\sqrt{9}", that's not simplified. Simplified is "3" if it was sqrt(27)? No 27=3^3 -> 3*sqrt(3).
             
        # Let's re-eval: n = 27. Factors of 27: 3^3. Square part from factors: 3^(2*(3//2)) = 3^2 = 9. Remainder = 3.
        # So coeff = sqrt(9) = 3, radicand (remainder) = 3. 
        # Correct answer string: "3\sqrt{3}"
        
    else:
        pass

    import math
    
    def get_coefficient_and_remainder(n):
        """Returns coefficient and simplified radicand for sqrt(n)."""
        if n <= 0: return (None, None)
        
        # Prime factorization approach to find square factors
        d = 2
        temp_n = n
        prime_counts = {}
        
        while d * d <= temp_n:
            while temp_n % d == 0:
                if d not in prime_counts:
                    prime_counts[d] = 0
                prime_counts[d] += 1
                temp_n //= d
            d += 1
            
        if temp_n > 1:
            if temp_n not in prime_counts:
                prime_counts[temp_n] = 0
            prime_counts[temp_n] += 1
            
        # Build square part (inside the root) and non-square part (coefficient outside? No, coefficient is from even powers)
        # sqrt(n) = product(p_i^(e_i)) -> p_i^floor(e_i/2) * sqrt(product(p_i^(e_i mod 2)))
        
        coeff_val = 1
        new_radicand = 1
        
        for prime in sorted(prime_counts.keys()):
            count = prime_counts[prime]
            
            # Contribution to coefficient: p ^ (count // 2)
            exp_outside = count // 2
            
            if exp_outside > 0:
                coeff_val *= (prime ** exp_outside)
                
            # Contribution to radicand inside sqrt: p ^ (count % 2)
            rem_exp = count % 2
            new_radicand *= (prime ** rem_exp)
            
        return coeff_val, new_radicand

    coefficient, simplified_radicand = get_coefficient_and_remainder(radicand_value)
    
    # Construct LaTeX strings
    if simplified_radicand == 1:
        canonical_latex = str(coefficient)
        correct_answer_str = f"{canonical_latex}"
        # In this case, technically coefficient is the whole number and radicand is empty or handled differently? 
        # But usually simplification of perfect square results in integer. The template asks for coeff/radicand/latex.
        # If we strictly follow "coefficient * sqrt(radicand)", then 3*sqrt(1) -> but standard math says just 3.
        # Let's assume the system expects non-perfect-square outputs or handles perfect squares as integer latex with specific fields?
        # Given "exact integers", if result is integer, we might set radicand=0 and coeff=result? Or radixand=1? 
        # Safest bet for generic radical simplification logic: output 3*sqrt(1) -> No, standard form drops sqrt.
        # Let's check the constraints again: "correct_answer must include coefficient, radicand...".
        # If I return coeff=27, radicand=0? That implies 27 * sqrt(0) = 0 wrong.
        # If result is integer K, we can represent as K + 0*sqrt(...) or just K. 
        # Let's assume the test cases are such that remainder != 1 for level 1 unless specified.
        # But 27 -> rem=3. So it won't be perfect square in this specific frozen param case.
        
    else:
        canonical_latex = f"{coefficient}\\sqrt{{{simplified_radicand}}}"
        correct_answer_str = canonical_latex

    question_text = (f"Simplify the radical expression \\(\\sqrt{{{radicand_value}}}\\).")
    
    # Constructing oracle_payload exactly as frozen parameters dict
    oracle_payload_dict = {"radicand": radicand_value}
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer_str,
        "oracle_payload": oracle_payload_dict
    }