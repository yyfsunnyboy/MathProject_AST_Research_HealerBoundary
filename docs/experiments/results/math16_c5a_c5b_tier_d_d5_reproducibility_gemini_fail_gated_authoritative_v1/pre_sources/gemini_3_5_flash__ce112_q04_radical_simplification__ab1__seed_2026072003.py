def generate(level=1, **kwargs):
    radicand_orig = kwargs.get("radicand", 135)
    
    coef = 1
    temp = radicand_orig
    d = 2
    while d * d <= temp:
        while temp % (d * d) == 0:
            coef *= d
            temp //= (d * d)
        d += 1
    
    if temp == 1:
        canonical_latex = f"{coef}"
    elif coef == 1:
        canonical_latex = f"\\sqrt{{{temp}}}"
    else:
        canonical_latex = f"{coef}\\sqrt{{{temp}}}"
        
    question_text = f"Simplify the radical expression: $\\sqrt{{{radicand_orig}}}$."
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "coefficient": coef,
            "radicand": temp,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": {
            "radicand": radicand_orig
        }
    }