from fractions import Fraction
import math

def generate(level=1, **kwargs):
    frozen_params = {"radicand": 27}
    
    radicand_input = kwargs.get("radicand", frozen_params["radicand"])
    coeff_input = 1
    
    # Use domain API for simplification
    from core.prompts.domain_function_library import RadicalOps
    simplified_coeff, simplified_radicand = RadicalOps.simplify_term(coeff_input, radicand_input)
    
    correct_answer_dict = {
        "coefficient": int(simplified_coeff),
        "radicand": int(simplified_radicand),
        "canonical_latex": f"{int(simplified_coeff)}\\sqrt{{{int(simplified_radicand)}}}}"
    }
    
    return {
        "question_text": r"$$\text{Simplify the radical: }\sqrt{\text{" + str(radicand_input) + r"}}$$",
        "correct_answer": correct_answer_dict,
        "oracle_payload": frozen_params
    }