from fractions import Fraction
import sys
sys.path.insert(0, '.')
from core.prompts.domain_function_library import RadicalOps

def generate(level=1, **kwargs):
    radicand = kwargs.get("radicand", 27) if "radicand" in kwargs else 27
    
    coeff = 1
    simplified_coeff, square_free_radicand = RadicalOps.simplify_term(coeff, radicand)
    
    correct_answer_dict = {
        "coefficient": int(simplified_coeff),
        "radicand": int(square_free_radicand),
        "canonical_latex": f"{int(simplified_coeff)}\\sqrt{{{square_free_radicand}}}"
    }
    
    return {
        "question_text": r"$$\text{Simplify the radical: }\sqrt{\overline{\text{{radicand}}}}$$",
        "correct_answer": correct_answer_dict,
        "oracle_payload": {"radicand": radicand}
    }