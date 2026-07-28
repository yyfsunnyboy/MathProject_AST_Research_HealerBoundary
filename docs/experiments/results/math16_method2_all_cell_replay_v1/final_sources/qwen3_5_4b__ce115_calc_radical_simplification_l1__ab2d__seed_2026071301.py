import math
from fractions import Fraction
from typing import Dict, Any

def generate(level: int = 1, **kwargs: Any) -> Dict[str, Any]:
    radicand_input = kwargs.get("radicand", 27)
    
    coeff = 1
    
    # Use the domain API to simplify the radical term
    simplified_coeff, square_free_radicand = RadicalOps.simplify_term(coeff, radicand_input)
    
    correct_answer_dict = {
        "coefficient": int(simplified_coeff),
        "radicand": int(square_free_radicand),
        "canonical_latex": f"{int(simplified_coeff)}\\sqrt{{{square_free_radicand}}}"
    }
    
    return {
        "question_text": r"$$\text{Simplify the radical: }\sqrt{\text{" + str(radicand_input) + "}\cdot 1}$$",
        "correct_answer": correct_answer_dict,
        "oracle_payload": {'radicand': 27}
    }