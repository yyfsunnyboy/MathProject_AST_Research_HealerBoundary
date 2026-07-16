import json
from typing import Dict, Any

def generate(level=1, **kwargs):
    frozen_params = {"radicand": 27}
    
    radicand_input = frozen_params["radicand"]
    
    # Simplify the radical term manually for level 1: sqrt(27) -> 3 * sqrt(3)
    # Since we must use domain APIs, and RadicalOps.simplify_term expects (coeff, radicand),
    # we treat input as coeff=1. However, to get coefficient out of simplify_term correctly 
    # for the output format where it returns (outer_coefficient, square_free_radicand):
    
    from core.prompts.domain_function_library import RadicalOps
    
    initial_coeff = 1
    simplified_result = RadicalOps.simplify_term(initial_coeff, radicand_input)
    
    outer_coefficient, final_radicand = simplified_result
    
    # Construct the question text based on frozen parameters
    original_radical_text = f"\\sqrt{{{radicand_input}}}"
    correct_answer_str = f"{outer_coefficient} \\sqrt{{final_radicand}}"
    question_text = f"Simplify: {original_radical_text}. Answer in simplest radical form."
    
    # Build the answer dict with exact integer types
    correct_answer_dict = {
        "coefficient": outer_coefficient,
        "radicand": final_radicand
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer_dict,
        "oracle_payload": frozen_params
    }