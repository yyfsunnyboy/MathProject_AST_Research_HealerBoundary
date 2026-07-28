# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen sampled parameters for this task instance
    frozen_params = {"radicand": 27}

    from core.prompts.domain_function_library import RadicalOps
    
    radicand_input = frozen_params["radicand"]
    
    # Simplify the radical expression using RadicalOps.simplify_term
    coeff, simplified_radicand = RadicalOps.simplify_term(1, radicand_input)
    
    # Construct canonical LaTeX string: a\sqrt{b}
    correct_answer_latex = f"{coeff}\\sqrt{{{simplified_radicand}}}"
    
    question_text = r"$$ \text{simplify } \sqrt{\overline{{frozen\_params['radicand']}}} $$"

    return {
        "question_text": question_text,
        "correct_answer": {
            "coefficient": coeff,
            "radicand": simplified_radicand,
            "canonical_latex": correct_answer_latex
        },
        "oracle_payload": frozen_params.copy()
    }
