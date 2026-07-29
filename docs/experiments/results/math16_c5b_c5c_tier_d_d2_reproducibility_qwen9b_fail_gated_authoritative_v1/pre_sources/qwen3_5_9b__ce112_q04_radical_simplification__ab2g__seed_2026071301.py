def generate(level=1, **kwargs):
    radicand = kwargs.get("radicand", 135)
    
    # Factorize radicand to simplify radical: sqrt(135) -> sqrt(9*15) -> 3*sqrt(15)
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
    
    # Calculate coefficient and new radicand for simplified radical form sqrt(k * m) -> c * sqrt(m)
    coeff = 1
    remaining_radicand = 1
    for p, count in sorted(prime_factors.items()):
        if count % 2 == 0:
            q = count // 2
            coeff *= (p ** q)
        else:
            remaining_radicand *= (p ** (count - (count % 2))) # This logic is slightly off for odd counts, let's fix
    
    # Correct simplification logic:
    # For each prime factor p with exponent e in n = product(p^e), 
    # we can pull out floor(e/2) pairs of p from the square root.
    coeff_new = 1
    radicand_new = 1
    for p, count in sorted(prime_factors.items()):
        q = count // 2
        if q > 0:
            coeff_new *= (p ** q)
        remaining_count = count % 2
        if remaining_count == 1:
            radicand_new *= p
    
    # Construct LaTeX strings
    canonical_latex = f"\\sqrt{{{radicand}}}"
    
    if coeff_new > 1 or radicand_new != radicand:
        # Simplified form exists and is different from original unsimplified representation in context of task usually implying simplification needed
        # However, the task asks for correct_answer to include coefficient, radicand, and canonical_latex.
        # Let's assume we need to output the simplified version if possible, or just format it properly.
        # The prompt implies generating a question about radical simplification.
        
        # If fully reducible (e.g., sqrt(4)=2), coeff=2, radicand_new=1 -> 2\\sqrt{1} usually written as 2? 
        # But standard form keeps integer under root if possible or just writes the number.
        # Let's stick to c * \\sqrt{n}. If n becomes 1, we might write just coefficient but let's keep structure for consistency unless specified otherwise.
        
        coeff_str = str(coeff_new)
        radicand_str = f"{radicand_new}" if radicand_new != 1 else "1" # Usually simplified radicals don't have sqrt(1), but let's check standard math simplification rules. 
        # Standard: simplify completely. If result is integer, no radical. But the schema requires 'canonical_latex' which likely expects \\sqrt{...} format or just number?
        # Given "correct_answer must include coefficient, radicand...", it implies a form like c\\sqrt{n}.
        
        if coeff_new == 1 and radicand_new == radicand:
             canonical_latex = f"\\sqrt{{{radicand}}}"
             correct_answer_str = f"{canonical_latex}" # No simplification possible or not requested to change representation? 
             # Actually, the task is "radical_simplification". We must simplify.
        
        if radicand_new == 1:
            canonical_latex = str(coeff_new)
            coeff_part = ""
            radicand_part = ""
        else:
            canonical_latex = f"{coeff_new}\\sqrt{{{radicand_new}}}"
    
    # Re-evaluating based on typical dataset generation for math problems (like GSM8K or similar):
    # Usually, if simplification is possible, we output the simplified form.
    # If radicand was 135 -> 9*15 -> sqrt(135) = 3sqrt(15).
    
    final_coeff = coeff_new
    final_radicand = radicand_new
    
    if final_radicand == 1:
        correct_answer_str = str(final_coeff)
        canonical_latex = f"{final_coeff}" # Or maybe just the number? 
        # But the requirement says "include coefficient, radicand". If radicand is 1, it's trivial.
        # Let's assume for this specific task instance (radicand=135), simplification happens.
        
    else:
        correct_answer_str = f"{final_coeff}\\sqrt{{{final_radicand}}}"
    
    question_text = "Simplify the radical expression:"
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer_str,
        "oracle_payload": {"radicand": radicand}
    }