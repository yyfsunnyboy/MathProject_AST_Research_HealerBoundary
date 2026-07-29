# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen sampled parameters as per task specification
    radicand = 135
    
    # Compute simplification manually to avoid external dependencies or eval/exec
    # Factorize 135 into perfect squares and remaining factors
    # 135 = 9 * 15, where 9 is a perfect square (sqrt(9) = 3)
    
    coeff = 0
    simplified_radicand = radicand
    
    # Check for largest square factor starting from small primes or direct division
    i = 2
    while i * i <= simplified_radicand:
        count = 0
        temp = simplified_radicand
        while temp % (i * i) == 0 and temp > 1:
            # Actually, we need to find the largest square factor. 
            # Better approach: iterate through squares or prime factors.
            pass
        
    # Direct calculation for this specific frozen value is safer and cleaner without complex loops if logic gets tricky
    # However, let's implement a robust simplification function inline
    
    def simplify_radical(n):
        result = 1
        current_n = n
        d = 2
        while d * d <= current_n:
            count = 0
            while current_n % (d * d) == 0 and current_n > 0:
                # This logic is slightly flawed for general case if we just divide by square. 
                # Correct approach: find exponent of prime factors.
                pass
        
        # Re-implementing robustly:
        temp = n
        coeff_val = 1
        remaining = 1
        d = 2
        while d * d <= temp:
            count = 0
            while temp % d == 0:
                count += 1
                temp //= d
            if count >= 2:
                # We can pull out sqrt(d^k) where k is even part of exponent? 
                # No, standard simplification pulls out pairs.
                num_pairs = count // 2
                coeff_val *= (d ** num_pairs)
                remaining *= d % (count - 2 * num_pairs if count > 0 else 1) # Logic error in thought process above
        
        # Let's restart the logic for correctness:
        temp = n
        coeff_val = 1
        remaining_part = 1
        d = 2
        while d * d <= temp:
            exponent = 0
            while temp % d == 0:
                exponent += 1
                temp //= d
            
            if exponent > 0:
                pairs = exponent // 2
                coeff_val *= (d ** pairs)
                remaining_part *= (d ** (exponent - 2 * pairs))
        
        # Handle the case where a prime factor remains with odd power or just itself
        if temp > 1:
            remaining_part *= temp
            
        return coeff_val, remaining_part

    coefficient, simplified_radicand = simplify_radical(radicand)
    
    # Construct LaTeX strings
    import re
    
    def format_latex(coeff, rad):
        if coeff == 1 and rad != 0:
            return f"\\sqrt{{{rad}}}"
        elif coeff == -1 and rad != 0:
            return f"-\\sqrt{{{rad}}}"
        else:
            sign = "+" if coeff > 0 else "-"
            abs_coeff = abs(coeff)
            # Format radicand for LaTeX (remove braces around single digit numbers usually, but keep for clarity in math mode context or standard practice? 
            # Standard: \\sqrt{15} vs \\sqrt{a}. Let's use minimal braces.
            rad_str = str(rad).replace(" ", "")
            if len(str(abs_coeff)) == 1 and abs_coeff != 0:
                return f"{sign}\\sqrt{{{rad_str}}}"
            else:
                # If coeff is multi-digit or negative (handled by sign), ensure proper spacing/formatting isn't strictly enforced but standard LaTeX usually puts number before sqrt.
                if rad_str.isdigit():
                    return f"{coeff}\\\\sqrt{{{rad_str}}}" 
                else:
                     return f"{sign}\\sqrt{{{rad_str}}}"

    # Refining format_latex for canonical output consistency with typical math platforms (e.g., Khan Academy, etc.)
    # Usually: 3\\sqrt{15}, -2\\sqrt{7}
    
    if coefficient == 0:
        latex_ans = "0"
    else:
        sign_str = "+" if coefficient > 0 else ""
        
        # Format radicand without spaces inside braces for simplicity unless it's a variable (not the case here)
        rad_int = simplified_radicand
        
        # Construct string carefully
        term_part = f"{rad_int}"
        
        if abs(coefficient) == 1:
            latex_ans = sign_str + "\\sqrt{" + str(rad_int) + "}"
        else:
            latex_ans = sign_str + str(abs(coefficient)) + "\\\\sqrt{" + str(rad_int) + "}"

    # Ensure canonical format matches expected output structure exactly as per typical tasks
    # Re-evaluating the specific frozen value 135 -> 9*15 -> coeff=3, rad=15.
    
    final_coeff = coefficient
    final_radicand = simplified_radicand
    
    if final_coeff == 0:
        canonical_latex = "0"
    else:
        sgn = "+" if final_coeff > 0 else ""
        
        # Check if we need to handle the negative sign placement correctly in LaTeX string construction for display vs internal rep.
        # The prompt asks for 'canonical_latex'. Usually, this is just the rendered math expression.
        
        r_str = str(final_radicand)
        
        if abs(final_coeff) == 1:
            canonical_latex = sgn + "\\sqrt{" + r_str + "}"
        else:
            # For multi-digit coefficients or negative ones, standard is coeff\\sqrt{rad}
            c_abs = abs(final_coeff)
            canonical_latex = sgn + str(c_abs) + "\\\\sqrt{" + r_str + "}"

    question_text = f"Simplify the radical expression $\\\\sqrt{{{radicand}}}$."
    
    correct_answer_dict = {
        "coefficient": final_coeff,
        "radicand": final_radicand,
        "canonical_latex": canonical_latex
    }
    # The task says 'correct_answer must include coefficient, radicand, and canonical_latex'. 
    # It implies the value of correct_answer should be this dict or a string representation? 
    # Looking at typical patterns: usually it's a structured object if JSON serializable is required.
    # However, often these tasks expect `correct_answer` to be the LaTeX string itself in some contexts, BUT here spec says "include coefficient...".
    # Let's assume correct_answer IS the dictionary containing those fields as per strict reading of "must include". 
    # Wait, re-reading: "Return a dict with exactly question_text, correct_answer, and oracle_payload."
    # And inside that return value, `correct_answer` field must contain coefficient, radicand, canonical_latex.
    
    final_correct_answer = {
        "coefficient": final_coeff,
        "radicand": final_radicand,
        "canonical_latex": canonical_latex
    }

    oracle_payload = {"radicand": 135}

    return {
        "question_text": question_text,
        "correct_answer": final_correct_answer,
        "oracle_payload": oracle_payload
    }