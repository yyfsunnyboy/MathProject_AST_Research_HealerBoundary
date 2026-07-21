import math
from fractions import Fraction
from typing import Dict, Any

def generate(level: int = 1, **kwargs: Any) -> Dict[str, Any]:
    radicand_input = kwargs.get("radicand", 27)
    
    coeff = 1
    
    if isinstance(radicand_input, str):
        try:
            radicand_int = int(float(radicand_input))
        except ValueError:
            raise ValueError(f"Invalid integer input for radicand: {radicand_input}")
    else:
        radicand_int = int(radicand_input)
    
    if radicand_int < 0 or not isinstance(radicand_int, int):
        raise ValueError("Radicand must be a non-negative integer")

    def simplify_term(coeff_val: int | Fraction, radicand_val: int) -> tuple[int | Fraction, int]:
        from core.prompts.domain_function_library import RadicalOps
        
        return RadicalOps.simplify_term(int(coeff_val), radicand_val)

    coeff_simplified, square_free_radicand = simplify_term(coeff, radicand_int)
    
    if not isinstance(square_free_radicand, int):
        raise TypeError("simplify_term must return an integer for the second element")
        
    canonical_latex = f"{coeff_simplified}\\sqrt{{{square_free_radicand}}}"

    question_text = r"$$\text{Simplify: } \sqrt{\text{" + str(radicand_int) + "}}$$"
    
    correct_answer_dict = {
        "coefficient": int(coeff_simplified),
        "radicand": square_free_radicand,
        "canonical_latex": canonical_latex
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer_dict,
        "oracle_payload": {"radicand": radicand_input}
    }