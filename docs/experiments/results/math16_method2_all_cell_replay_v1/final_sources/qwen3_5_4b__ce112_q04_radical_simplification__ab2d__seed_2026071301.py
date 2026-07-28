import math
from fractions import Fraction
from typing import Dict, Any, Tuple, Union

# Mocking the required domain functions as they are not in standard library
class RadicalOps:
    @staticmethod
    def simplify_term(coeff: int, radicand: int) -> Tuple[int, int]:
        # Simplify sqrt(radicand) by removing perfect square factors
        temp_radicand = abs(radicand) if radicand < 0 else radicand
        simplified_coeff = coeff * -1 if radicand < 0 and math.isqrt(temp_radicand)**2 == temp_radicand else coeff
        
        # Handle negative numbers carefully for sqrt domain usually implies non-negative, 
        # but assuming standard simplification logic: factor out squares.
        i = 2
        while i * i <= temp_radicand:
            if temp_radicand % (i*i) == 0:
                count = 0
                d = i*i
                while temp_radicand % d == 0:
                    count += 1
                    temp_radicand //= d
                simplified_coeff *= int(d ** (count // 2)) if count >= 2 else 1 # Logic adjustment for single factor extraction
            i += 1
        
        return coeff, abs(temp_radicand)

    @staticmethod
    def format_term(coeff: Union[int, Fraction], radicand: int, is_first: bool = True) -> str:
        sign = "-" if (isinstance(coeff, float) and coeff < 0 or isinstance(coeff, int) and coeff < 0) else ""
        num_str = f"{coeff}" if not isinstance(coeff, Fraction) else str(coeff.numerator / coeff.denominator)
        
        # Handle coefficient formatting for LaTeX
        if is_first:
            latex_coeff = r"\text{" + sign + str(abs(num_str)) + "}\sqrt"
        else:
            latex_coeff = f"{sign}{num_str}\\sqrt"
            
        return latex_coeff + radicand

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