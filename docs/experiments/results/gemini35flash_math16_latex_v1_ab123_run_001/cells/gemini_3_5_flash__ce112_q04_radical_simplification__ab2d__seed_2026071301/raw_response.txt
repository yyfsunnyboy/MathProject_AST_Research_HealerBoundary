from core.prompts.domain_function_library import RadicalOps

def generate(level=1, **kwargs):
    radicand = 135
    
    # Simplify the radical term
    coeff, simplified_radicand = RadicalOps.simplify_term(1, radicand)
    
    # Convert to canonical LaTeX representation
    canonical_latex = RadicalOps.to_latex((coeff, simplified_radicand))
    
    question_text = f"Simplify the radical expression: $\\sqrt{{{radicand}}}$"
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "coefficient": coeff,
            "radicand": simplified_radicand,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": {
            "radicand": radicand
        }
    }