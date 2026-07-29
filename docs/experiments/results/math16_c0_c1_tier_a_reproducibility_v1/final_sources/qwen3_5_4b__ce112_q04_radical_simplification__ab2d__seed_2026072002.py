import math
from fractions import Fraction
from typing import Dict, Any

# Mocking the required domain functions as they are not in standard library
class RadicalOps:
    @staticmethod
    def simplify_term(coeff: int | float, radicand: int) -> tuple[int | Fraction, int]:
        # Simplify logic for perfect squares within the integer part of coeff and radicand
        if isinstance(coeff, (int, float)):
            c = round(coeff)
        else:
            c = 0
        
        simplified_radicand = radicand
        temp_c = c
        
        while True:
            sqrt_val = math.isqrt(simplified_radicand)
            if sqrt_val * sqrt_val == simplified_radicand:
                factor = int(sqrt_val)
                # Distribute the square root into coefficient
                new_coeff = Fraction(factor, 1) * temp_c
                simplified_radicand //= (factor ** 2)
                break
            
            else:
                if c != 0 or radicand > 1:
                    raise ValueError("No perfect square factor found to simplify further")
                return int(c), simplified_radicand
        
        # Handle the case where coefficient was a float that needs rounding for integer math logic in this specific context
        final_coeff = round(coeff) if isinstance(coeff, (int, float)) else 0
        return final_coeff, simplified_radicand

    @staticmethod
    def format_term(coeff: int | Fraction, radicand: int, is_first: bool = True) -> str:
        sign = ""
        if coeff < 0:
            sign = "-"
            coeff = abs(coeff)
        
        latex_coeff = f"{coeff}"
        latex_radicand = f"{{{radicand}}}"
        
        term_str = f"{sign}{latex_coeff}\\sqrt{latex_radicand}"
        return term_str

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