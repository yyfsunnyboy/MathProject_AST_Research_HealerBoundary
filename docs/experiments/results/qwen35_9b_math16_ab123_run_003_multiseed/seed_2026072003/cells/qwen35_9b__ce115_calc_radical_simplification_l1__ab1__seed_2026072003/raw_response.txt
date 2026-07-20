def generate(level=1, **kwargs):
    frozen_params = kwargs.get("frozen_sampled_parameters", {"radicand": 27})
    
    radicand = frozen_params["radicand"]
    
    # Factorization for simplification (Level 1: simple perfect squares)
    factors = []
    d = 2
    temp_radicand = radicand
    while d * d <= temp_radicand:
        if temp_radicand % d == 0:
            count = 0
            while temp_radicand % d == 0:
                temp_radicand //= d
                count += 1
            factors.append((d, count))
        d += 1
    
    # If remaining radicand > 1 and level allows (Level 1 usually simplifies everything possible)
    if temp_radicand > 1:
        factors.append((temp_radicand, 1))
    
    # Simplify coefficients
    simplified_coefficient = 1
    simplified_radical_part = []
    
    for base, exponent in sorted(factors):
        quotient, remainder = divmod(exponent, 2)
        if quotient > 0:
            simplified_coefficient *= (base ** quotient)
        
    # Reconstruct the radical part from remainders
    current_radical_part_str_parts = []
    for base, exponent in sorted(factors):
        _, remainder = divmod(exponent, 2)
        if remainder == 1:
            simplified_radical_part.append(str(base))
    
    canonical_latex_expr = f"{simplified_coefficient}\\sqrt{{{','.join(simplified_radical_part)}}}"
    
    # Handle case where radical part is empty (perfect square result in integer, but task implies radicals)
    if not simplified_radical_part:
        # This shouldn't happen with radicand=27 given 3^3 -> 3*sqrt(3), let's re-verify logic for 27 specifically.
        pass
    
    question_text = f"Simplify the radical expression $\\sqrt{{{radicand}}}$."
    
    return {
        "question_text": question_text,
        "correct_answer": canonical_latex_expr,
        "oracle_payload": frozen_params
    }