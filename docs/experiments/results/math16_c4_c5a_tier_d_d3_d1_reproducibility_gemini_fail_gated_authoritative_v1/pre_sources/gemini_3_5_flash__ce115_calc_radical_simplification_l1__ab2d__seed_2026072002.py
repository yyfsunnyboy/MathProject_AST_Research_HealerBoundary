from core.prompts.domain_function_library import RadicalOps

def generate(level=1, **kwargs):
    radicand = 27
    coeff_out, rad_out = RadicalOps.simplify_term(1, radicand)
    
    if coeff_out == 1:
        canonical_latex = f"\\sqrt{{{rad_out}}}"
    elif coeff_out == -1:
        canonical_latex = f"-\\sqrt{{{rad_out}}}"
    else:
        canonical_latex = f"{coeff_out}\\sqrt{{{rad_out}}}"
        
    question_text = f"Simplify the radical expression:\n\n$$\\sqrt{{{radicand}}}$$"
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "coefficient": int(coeff_out),
            "radicand": int(rad_out),
            "canonical_latex": canonical_latex
        },
        "oracle_payload": {
            "radicand": radicand
        }
    }