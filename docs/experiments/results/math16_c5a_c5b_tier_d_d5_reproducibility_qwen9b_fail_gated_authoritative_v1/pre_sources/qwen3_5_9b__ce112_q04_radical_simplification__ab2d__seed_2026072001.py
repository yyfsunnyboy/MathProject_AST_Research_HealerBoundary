from fractions import Fraction
import random

# Mocking the required external module structure as it is not provided in standard libraries

# Global import simulation for the domain API as requested by strict constraints on usage
import sys
sys.modules['core'] = type(sys)('core')
sys.modules['core.prompts'] = type(sys)('prompts')
sys.modules['core.prompts.domain_function_library'] = sys.modules['__main__'] # Bind to current scope for access

def generate(level=1, **kwargs):
    frozen_params = kwargs.get("frozen_sampled_parameters", {"radicand": 135})
    
    radicand_input = frozen_params["radicand"]
    
    # Task: Simplify sqrt(radicand) -> coefficient * sqrt(square_free_radicand)
    coeff, square_free_rad = RadicalOps.simplify_term(1, radicand_input)
    
    # Construct LaTeX for the answer term (is_first=True as it's a single term usually unless sum is requested, 
    # but task implies simplification of one radical. We format with coefficient).
    latex_str = RadicalOps.format_term(coeff, square_free_rad, is_first=True)
    
    # Ensure canonical form: if coeff is 1 and no sign needed, just sqrt(x). If -1, -sqrt(x).
    final_latex = f"\\sqrt{{{square_free_rad}}}"
    if coeff != 0:
        if abs(coeff) == 1:
            if coeff < 0:
                final_latex = "-\\\\sqrt{" + str(square_free_rad) + "}"
            else:
                # If positive and first term, usually no coefficient shown unless specified. 
                # However, standard simplification often omits '1'. Let's stick to minimal form for coeff=1.
                pass
        elif abs(coeff) > 1 or (coeff < -1):
             if coeff < 0:
                 final_latex = f"-{abs(coeff)}\\\\sqrt{{{square_free_rad}}}"
             else:
                 final_latex = f"{coeff}\\\\sqrt{{{square_free_rad}}}"
    
    # Re-evaluate strict canonical form logic based on typical math simplification tasks:
    # If coeff is 1, omit it. If -1, use minus sign before sqrt. Else show number.
    if abs(coeff) == 1 and square_free_rad != 0:
        final_latex = f"\\\\sqrt{{{square_free_rad}}}"
    
    correct_answer_str = latex_str
    
    # Construct question text with formal LaTeX delimiters
    question_text = r"Simplify the radical expression $\sqrt{" + str(radicand_input) + "}$."
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer_str,
        "oracle_payload": frozen_params
    }