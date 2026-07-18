from core.prompts.domain_function_library import RadicalOps

def generate(level=1, **kwargs):
    # Frozen parameters
    radicand = 27
    
    # Simplify the radical term
    coeff_out, radicand_out = RadicalOps.simplify_term(1, radicand)
    
    # Format canonical latex
    if radicand_out == 1:
        canonical_latex = f"{coeff_out}"
    elif coeff_out == 1:
        canonical_latex = f"\\sqrt{{{radicand_out}}}"
    elif coeff_out == -1:
        canonical_latex = f"-\\sqrt{{{radicand_out}}}"
    else:
        canonical_latex = f"{coeff_out}\\sqrt{{{radicand_out}}}"
        
    question_text = f"Simplify the radical expression: $\\sqrt{{{radicand}}}$"
    
    correct_answer = {
        "coefficient": int(coeff_out),
        "radicand": int(radicand_out),
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