from core.prompts.domain_function_library import RadicalOps

def generate(level=1, **kwargs):
    # Frozen parameters
    radicand = kwargs.get("radicand", 27)
    
    # Simplify the radical \sqrt{radicand} (coeff = 1)
    outer_coeff, inner_radicand = RadicalOps.simplify_term(1, radicand)
    
    # Ensure they are integers
    outer_coeff = int(outer_coeff)
    inner_radicand = int(inner_radicand)
    
    # Format canonical latex
    if outer_coeff == 1:
        canonical_latex = f"\\sqrt{{{inner_radicand}}}"
    elif outer_coeff == -1:
        canonical_latex = f"-\\sqrt{{{inner_radicand}}}"
    else:
        canonical_latex = f"{outer_coeff}\\sqrt{{{inner_radicand}}}"
        
    question_text = f"Simplify the radical expression: $\\sqrt{{{radicand}}}$"
    
    correct_answer = {
        "coefficient": outer_coeff,
        "radicand": inner_radicand,
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