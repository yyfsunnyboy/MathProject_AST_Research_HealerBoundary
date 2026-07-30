def generate(level=1, **kwargs):
    import math
    radicand_input = kwargs.get("radicand", 27)
    
    d = 1
    temp = radicand_input
    for i in range(2, int(math.isqrt(temp)) + 1):
        while temp % (i * i) == 0:
            d *= i
            temp //= (i * i)
            
    coefficient = d
    simplified_radicand = temp
    
    if coefficient == 1:
        canonical_latex = f"\\sqrt{{{simplified_radicand}}}"
    else:
        if simplified_radicand == 1:
            canonical_latex = f"{coefficient}"
        else:
            canonical_latex = f"{coefficient}\\sqrt{{{simplified_radicand}}}"
            
    question_text = f"Simplify the radical expression: \\(\\sqrt{{{radicand_input}}}\\)"
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "coefficient": coefficient,
            "radicand": simplified_radicand,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": {
            "radicand": radicand_input
        }
    }