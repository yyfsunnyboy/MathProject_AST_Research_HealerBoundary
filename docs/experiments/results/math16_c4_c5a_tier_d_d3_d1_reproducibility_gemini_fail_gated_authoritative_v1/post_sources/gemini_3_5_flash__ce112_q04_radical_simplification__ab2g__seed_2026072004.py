def generate(level=1, **kwargs):
    radicand_input = kwargs.get("radicand", 135)
    
    # Simplify the radical
    coeff = 1
    temp = radicand_input
    d = 2
    while d * d <= temp:
        while temp % (d * d) == 0:
            coeff *= d
            temp //= (d * d)
        d += 1
        
    if temp == 1:
        canonical_latex = f"{coeff}"
    elif coeff == 1:
        canonical_latex = f"\\sqrt{{{temp}}}"
    else:
        canonical_latex = f"{coeff}\\sqrt{{{temp}}}"
        
    question_text = f"Simplify the radical expression: $\\sqrt{{{radicand_input}}}$."
    
    correct_answer = {
        "coefficient": coeff,
        "radicand": temp,
        "canonical_latex": canonical_latex
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": {"radicand": radicand_input}
    }