def generate(level=1, **kwargs):
    radicand_input = 135
    
    # 135 = 9 * 15, so sqrt(135) = 3 * sqrt(15)
    coef = 3
    rad_simplified = 15
    canonical_latex = f"{coef}\\sqrt{{{rad_simplified}}}"
    
    question_text = f"Simplify the radical expression: $\\sqrt{{{radicand_input}}}$."
    
    correct_answer = {
        "coefficient": coef,
        "radicand": rad_simplified,
        "canonical_latex": canonical_latex
    }
    
    oracle_payload = {
        "radicand": radicand_input
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }