def generate(level=1, **kwargs):
    # Frozen sampled parameters
    radicand_input = 27
    
    # Simplify the radical
    coefficient = 1
    radicand_remain = radicand_input
    d = 2
    while d * d <= radicand_remain:
        while radicand_remain % (d * d) == 0:
            coefficient *= d
            radicand_remain //= (d * d)
        d += 1
        
    if radicand_remain == 1:
        canonical_latex = f"{coefficient}"
    elif coefficient == 1:
        canonical_latex = f"\\sqrt{{{radicand_remain}}}"
    else:
        canonical_latex = f"{coefficient}\\sqrt{{{radicand_remain}}}"
        
    question_text = f"Simplify the radical expression: $\\sqrt{{{radicand_input}}}$"
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "coefficient": coefficient,
            "radicand": radicand_remain,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": {
            "radicand": radicand_input
        }
    }