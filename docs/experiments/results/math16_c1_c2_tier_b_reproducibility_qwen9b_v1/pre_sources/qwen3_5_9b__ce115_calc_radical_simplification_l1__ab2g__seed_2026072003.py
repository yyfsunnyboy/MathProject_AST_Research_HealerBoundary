def generate(level=1, **kwargs):
    # Frozen sampled parameters as per task specification
    radicand = 27
    
    # Mathematical logic for level 1 radical simplification: sqrt(27) -> 3*sqrt(3)
    # Factorization of 27 is 9 * 3. Since 9 is a perfect square (3^2), we pull out 3.
    
    import math
    
    def simplify_radical(n):
        if n <= 0:
            return None, None
        
        factors = {}
        temp_n = n
        d = 2
        while d * d <= temp_n:
            while temp_n % d == 0:
                factors[d] = factors.get(d, 0) + 1
                temp_n //= d
            d += 1
        
        if temp_n > 1:
            factors[temp_n] = factors.get(temp_n, 0) + 1
            
        # Find perfect square parts to pull out of the radical
        coefficient_parts = []
        remaining_radicand = 1
        
        for base, exponent in sorted(factors.items()):
            if exponent % 2 == 1:
                remaining_radicand *= base
            else:
                coeff_val = int(math.pow(base, (exponent // 2)))
                coefficient_parts.append(coeff_val)
        
        total_coefficient = 1
        for val in coefficient_parts:
            total_coefficient *= val
            
        if total_coefficient == 0 or remaining_radicand == 0: # Edge case handling not strictly needed here but good practice
             return None, None

        canonical_latex_str = f"{total_coefficient}\\sqrt{{{remaining_radicand}}}"
        
        # Handle the specific case where result is just an integer (no radical left)
        if remaining_radicand == 1:
            final_answer_int = total_coefficient
            return int(final_answer_int), canonical_latex_str
            
        return total_coefficient, f"{total_coefficient}\\sqrt{{{remaining_radicand}}}"

    coeff_simplified, latex_simplified = simplify_radical(radicand)
    
    # Construct the question text using formal LaTeX delimiters
    original_radicand_str = str(radicand)
    if radicand == 1:
        q_text = r"Simplify $\sqrt{1}$."
    else:
        q_text = rf"Simplify $\sqrt{{{original_radicand_str}}}$."

    # Construct the correct answer string including coefficient and canonical latex
    if coeff_simplified is not None:
        ans_string = f"{coeff_simplified}, {latex_simplified}"
    else:
        ans_string = "None"

    return {
        "question_text": q_text,
        "correct_answer": ans_string,
        "oracle_payload": {"radicand": radicand}
    }