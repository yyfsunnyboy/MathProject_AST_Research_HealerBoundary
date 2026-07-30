def generate(level=1, **kwargs):
    radicand_orig = kwargs.get("radicand", 135)
    
    coeff = 1
    temp = radicand_orig
    d = 2
    while d * d <= temp:
        while temp % (d * d) == 0:
            coeff *= d
            temp //= (d * d)
        d += 1
    simplified_radicand = temp
    
    if coeff == 1:
        canonical_latex = f"\\sqrt{{{simplified_radicand}}}"
    elif simplified_radicand == 1:
        canonical_latex = f"{coeff}"
    else:
        canonical_latex = f"{coeff}\\sqrt{{{simplified_radicand}}}"
        
    question_text = f"Simplify the radical expression: $\\sqrt{{{radicand_orig}}}$."
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "coefficient": coeff,
            "radicand": simplified_radicand,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": {
            "radicand": radicand_orig
        }
    }