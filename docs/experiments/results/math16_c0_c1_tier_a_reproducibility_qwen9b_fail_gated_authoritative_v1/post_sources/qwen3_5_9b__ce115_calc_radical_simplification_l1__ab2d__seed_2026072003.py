from fractions import Fraction
import random

def generate(level=1, **kwargs):
    frozen_params = {"radicand": 27}
    
    # Ensure radicand is an integer if passed as float in kwargs (though spec says exact integers)
    radicand_input = kwargs.get("radicand", frozen_params["radicand"])
    if isinstance(radicand_input, float):
        radicand_int = int(round(radicand_input))
    else:
        radicand_int = radicand_input
    
    # Use domain API to simplify the term
    from core.prompts.domain_function_library import RadicalOps
    coeff_simplified, square_free_radicand = RadicalOps.simplify_term(1, radicand_int)
    
    # Construct canonical LaTeX string for the answer: coefficient * sqrt(radicand)
    if coeff_simplified == 0:
        canonical_latex = "0"
    else:
        coef_str = str(coeff_simplified)
        rad_str = str(square_free_radicand)
        canonical_latex = f"{coef_str}\\sqrt{{{rad_str}}}"

    question_text = (
        r"Simplify the radical expression $\sqrt{" + 
        str(radicand_int) + "}$. Express your answer in simplest form."
    )
    
    correct_answer_dict = {
        "coefficient": coeff_simplified,
        "radicand": square_free_radicand,
        "canonical_latex": canonical_latex
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer_dict,
        "oracle_payload": frozen_params
    }