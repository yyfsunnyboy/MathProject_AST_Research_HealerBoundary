def generate(level=1, **kwargs):
    radicand = kwargs.get("radicand", 27)
    
    # Simplify the radical \sqrt{radicand} -> k \sqrt{m}
    n = radicand
    k = 1
    m = n
    d = 2
    while d * d <= m:
        while m % (d * d) == 0:
            k *= d
            m //= (d * d)
        d += 1
        
    if k == 1:
        canonical_latex = f"\\sqrt{{{m}}}"
    elif m == 1:
        canonical_latex = f"{k}"
    else:
        canonical_latex = f"{k}\\sqrt{{{m}}}"
        
    question_text = f"Simplify the radical expression: $\\sqrt{{{radicand}}}$"
    
    correct_answer = {
        "coefficient": k,
        "radicand": m,
        "canonical_latex": canonical_latex
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": {"radicand": radicand}
    }