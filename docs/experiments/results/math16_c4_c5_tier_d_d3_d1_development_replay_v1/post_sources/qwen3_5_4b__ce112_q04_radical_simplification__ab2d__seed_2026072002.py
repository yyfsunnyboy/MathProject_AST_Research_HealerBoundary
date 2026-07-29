import math
from fractions import Fraction
from typing import Dict, Any

# Mocking the required domain functions as they are not in standard library

def generate(level: int = 1, **kwargs) -> Dict[str, Any]:
    frozen_params = kwargs.get("frozen_parameters", {}) or {"radicand": 135}
    
    radicand_val = frozen_params["radicand"]
    
    # Initial coefficient is assumed to be 1 for this specific task unless specified otherwise in a broader context not present here. 
    # Based on the sample, we start with coeff=1 and radicand=135.
    initial_coeff = 1
    
    simplified_coeff, simplified_radicand = RadicalOps.simplify_term(initial_coeff, radicand_val)
    
    latex_str = RadicalOps.format_term(simplified_coeff, simplified_radicand)
    
    question_text = r"\text{Simplify the radical: } $\\sqrt{" + str(radicand_val) + "}$"
    
    correct_answer_dict = {
        "coefficient": int(simplified_coeff),
        "radicand": int(simplified_radicand),
        "canonical_latex": latex_str
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer_dict,
        "oracle_payload": frozen_params
    }