from core.prompts.domain_function_library import RadicalOps

def generate(level=1, **kwargs):
    radicand = 135
    
    # Simplify the radical
    coeff_out, rad_out = RadicalOps.simplify_term(1, radicand)
    
    # Format the simplified term and original term
    canonical_latex = RadicalOps.format_term(coeff_out, rad_out, is_first=True)
    orig_latex = RadicalOps.format_term(1, radicand, is_first=True)
    
    question_text = f"Simplify the radical expression: \\({orig_latex}\\)"
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "coefficient": coeff_out,
            "radicand": rad_out,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": {
            "radicand": radicand
        }
    }