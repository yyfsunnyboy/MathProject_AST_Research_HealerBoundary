# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen sampled parameters for this task instance
    radicand = 27
    
    # Import RadicalOps to handle radical simplification logic
    from core.prompts.domain_function_library import RadicalOps
    
    # Compute the simplified form a*sqrt(b) using the frozen radicand
    coeff, new_radicand = RadicalOps.simplify_term(1, radicand)
    
    # Construct the correct answer components (integers only)
    coefficient = int(coeff)
    final_radicand = int(new_radicand)
    
    # Generate canonical LaTeX representation: a\sqrt{b}
    latex_str = f"{coefficient}\\sqrt{{{final_radicand}}}"
    
    return {
        "question_text": r"$\sqrt{\text{{27}}}$",
        "correct_answer": {
            "coefficient": coefficient,
            "radicand": final_radicand,
            "canonical_latex": latex_str
        },
        "oracle_payload": {"radicand": radicand}
    }