def generate(level=1, **kwargs):
    radicand_orig = kwargs.get("radicand", 27)
    
    best_d = 1
    for i in range(1, int(radicand_orig**0.5) + 1):
        if radicand_orig % (i*i) == 0:
            best_d = i
    r = radicand_orig // (best_d * best_d)
    
    if best_d == 1:
        canonical_latex = f"\\sqrt{{{r}}}"
    else:
        canonical_latex = f"{best_d}\\sqrt{{{r}}}"
        
    question_text = f"Simplify the radical expression: $\\sqrt{{{radicand_orig}}}$"
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "coefficient": best_d,
            "radicand": r,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": {
            "radicand": radicand_orig
        }
    }