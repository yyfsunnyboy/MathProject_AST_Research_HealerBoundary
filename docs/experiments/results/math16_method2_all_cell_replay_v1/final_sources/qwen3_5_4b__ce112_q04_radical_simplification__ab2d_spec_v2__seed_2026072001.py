# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    from core.prompts.domain_function_library import RadicalOps
    
    # Frozen parameters used exactly as provided in task specification
    frozen_params = {"radicand": 135}
    
    # Compute simplification using the specified API method
    coeff, radicand = RadicalOps.simplify_term(0, frozen_params["radicand"])
    
    # Construct canonical LaTeX string for a\sqrt{b} form
    correct_answer_latex = f"{coeff}\\sqrt{{{int(radicand)}}}}"
    
    return {
        "question_text": r"$\sqrt{135}$",
        "correct_answer": {
            "coefficient": coeff,
            "radicand": int(radicand),
            "canonical_latex": correct_answer_latex
        },
        "oracle_payload": frozen_params
    }
