def generate(level=1, **kwargs):
    radicand = kwargs.get("radicand", 27)
    
    coef = 1
    temp = radicand
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
        
    question_text = f"Simplify the radical: $\\sqrt{{{radicand}}}$"
    
    correct_answer = {
        "coefficient": coef,
        "radicand": temp,
        "canonical_latex": canonical_latex
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": {"radicand": radicand}
    }