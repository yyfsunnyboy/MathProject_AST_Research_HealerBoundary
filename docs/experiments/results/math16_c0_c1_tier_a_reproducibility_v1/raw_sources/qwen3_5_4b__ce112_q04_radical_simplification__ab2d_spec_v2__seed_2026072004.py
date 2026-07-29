# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen sampled parameters used for this task instance
    frozen_params = {"radicand": 135}
    
    from core.prompts.domain_function_library import RadicalOps
    
    radicand_input = frozen_params["radicand"]
    
    coeff, simplified_radicand = RadicalOps.simplify_term(0, radicand_input)
    
    # Construct the correct answer components
    coefficient = coeff
    final_radicand = simplified_radicand
    
    # Format canonical LaTeX: a\sqrt{b} -> \text{{a}}\sqrt{\text{{b}}} or similar standard representation
    # Assuming standard mathjax/latex rendering where '1' is implied if integer, but here we have coeff=3, radicand=5
    # The form requested is coefficient * sqrt(radicand)
    
    correct_answer = {
        "coefficient": int(coefficient),
        "radicand": int(final_radicand),
        "canonical_latex": f"\\text{{3}}\\sqrt{{{final_radicand}}}"
    }

    question_text = r"\text{Simplify the radical expression: } \sqrt{\text{{135}}}."

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params.copy()
    }
