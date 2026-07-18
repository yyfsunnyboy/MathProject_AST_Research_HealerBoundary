from core.prompts.domain_function_library import RadicalOps

def generate(level=1, **kwargs):
    # Frozen sampled parameters
    radicand = 135
    
    # Simplify the radical \sqrt{135} with coefficient 1
    coeff, simplified_radicand = RadicalOps.simplify_term(1, radicand)
    
    # Generate canonical LaTeX representation
    canonical_latex = RadicalOps.to_latex((coeff, simplified_radicand))
    
    question_text = f"Simplify the radical expression: $\\sqrt{{{radicand}}}$."
    
    correct_answer = {
        "coefficient": coeff,
        "radicand": simplified_radicand,
        "canonical_latex": canonical_latex
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": {
            "radicand": radicand
        }
    }