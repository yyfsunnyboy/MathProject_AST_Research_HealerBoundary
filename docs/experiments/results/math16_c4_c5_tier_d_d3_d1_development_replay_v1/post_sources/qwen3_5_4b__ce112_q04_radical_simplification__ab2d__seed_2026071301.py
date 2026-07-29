import math
from fractions import Fraction
from typing import Dict, Any, Tuple, Union

# Mocking the required domain functions as they are not in standard library

def generate(level=1, **kwargs):
    frozen_params = {"radicand": 135}
    
    # Extract parameters (frozen)
    radicand_val = frozen_params["radicand"]
    
    # Initial coefficient is assumed to be 1 for this task unless specified otherwise in kwargs
    coeff_init = 1
    
    # Perform simplification using domain API
    simplified_coeff, final_radicand = RadicalOps.simplify_term(coeff_init, radicand_val)
    
    # Format the answer term
    latex_str = RadicalOps.format_term(simplified_coeff, final_radicand, is_first=True)
    
    # Construct correct_answer dict structure for internal use before returning full string if needed or just components
    # The task asks for canonical_latex in correct_answer
    
    question_text = r"\text{Simplify the radical: } \sqrt{\{" + str(radicand_val) + r"\}}"
    
    correct_answer_data = {
        "coefficient": simplified_coeff,
        "radicand": final_radicand,
        "canonical_latex": latex_str
    }
    
    # Construct the full LaTeX string for correct answer if needed, or just use canonical_latex as requested structure implies components. 
    # Re-reading: "correct_answer must include coefficient, radicand, and canonical_latex". This suggests a dict inside or specific fields.
    # Given the return type is a dict with keys question_text, correct_answer, oracle_payload.
    
    final_correct_ans = {
        "coefficient": simplified_coeff,
        "radicand": final_radicand,
        "canonical_latex": latex_str
    }

    return {
        "question_text": question_text,
        "correct_answer": final_correct_ans,
        "oracle_payload": frozen_params
    }