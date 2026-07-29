def generate(level=1, **kwargs):
    frozen_params = {"radicand": 135}
    
    radicand = frozen_params["radicand"]
    
    # Factorize radicand to simplify radical: sqrt(n * k^2) -> k*sqrt(n)
    factors = []
    temp = radicand
    d = 2
    while d * d <= temp:
        if temp % d == 0:
            count = 0
            while temp % d == 0:
                count += 1
                temp //= d
            factors.append((d, count))
        else:
            d += 1
    
    # Separate perfect square parts and remaining part
    coeff_part = 1
    new_radicand = 1
    
    for base, exponent in factors:
        if exponent % 2 == 0:
            q = exponent // 2
            coeff_part *= (base ** q)
        else:
            remainder = exponent - ((exponent + 1) // 2 * 2) # This logic is slightly off for odd, let's fix
            # Correct logic: take even part out to coefficient
            full_pairs = exponent // 2
            coeff_part *= (base ** full_pairs)
            new_radicand *= base
    
    if temp > 1:
        new_radicand *= temp
        
    simplified_coefficient = coeff_part
    simplified_radicand = new_radicand
    
    # Construct LaTeX strings
    canonical_latex = f"\\sqrt{{{simplified_radicand}}}"
    
    question_text = (f"Simplify the radical expression: $\\\\sqrt{{{radicand}}}$. "
                     f"The answer should be in the form of a coefficient times a simplified radical, e.g., $a\\\\sqrt{b}$ where b is square-free.")
    
    correct_answer = {
        "coefficient": str(simplified_coefficient),
        "radicand": str(simplified_radicand),
        "canonical_latex": canonical_latex
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }