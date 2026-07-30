from core.prompts.domain_function_library import RadicalOps

def generate(level=1, **kwargs):
    radicand = kwargs.get("radicand", 27)
    
    coeff, rad = RadicalOps.simplify_term(1, radicand)
    
    coeff = int(coeff)
    rad = int(rad)
    
    if rad == 1:
        canonical_latex = f"{coeff}"
    elif coeff == 1:
        canonical_latex = f"\\sqrt{{{rad}}}"
    else:
        canonical_latex = f"{coeff}\\sqrt{{{rad}}}"
        
    question_text = f"Simplify the radical expression:\n\n$$\\sqrt{{{radicand}}}$$"
    
    correct_answer = {
        "coefficient": coeff,
        "radicand": rad,
        "canonical_latex": canonical_latex
    }
    
    oracle_payload = {
        "radicand": radicand
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }