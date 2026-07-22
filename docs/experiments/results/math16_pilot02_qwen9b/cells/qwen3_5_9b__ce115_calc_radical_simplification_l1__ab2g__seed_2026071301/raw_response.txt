def generate(level=1, **kwargs):
    frozen_params = {"radicand": 27}
    
    radicand = frozen_params["radicand"]
    
    # Simplify radical: sqrt(27) -> 3*sqrt(3)
    # Factorization of 27 is 3^3. One factor comes out as coefficient (3), remainder inside is 3.
    import math
    
    temp = radicand
    coeff = 1
    inner = 1
    
    for i in range(2, int(math.sqrt(radicand)) + 1):
        count = 0
        while temp % i == 0:
            temp //= i
            count += 1
        
        if count > 0 and level >= 1:
            # For sqrt (level 1), we pull out factors with exponent >= 2
            num_out = count // 2
            coeff *= (i ** num_out)
            inner *= (i ** (count % 2))
    
    if temp > 1 and level >= 1:
        # Remaining prime factor inside
        inner *= temp
    
    final_coeff = coeff
    final_inner = inner
    
    # Construct LaTeX strings
    correct_answer_str = f"{final_coeff}\\sqrt{{{final_inner}}}"
    canonical_latex = f"\\frac{{3}}{{1}}\\sqrt{{{3}}}" if (radicand == 27) else correct_answer_str.replace(" ", "")

    question_text = r"Simplify the radical expression: $\sqrt{27}$."
    
    return {
        "question_text": question_text,
        "correct_answer": f"{final_coeff}\\sqrt{{{final_inner}}}",
        "oracle_payload": frozen_params
    }