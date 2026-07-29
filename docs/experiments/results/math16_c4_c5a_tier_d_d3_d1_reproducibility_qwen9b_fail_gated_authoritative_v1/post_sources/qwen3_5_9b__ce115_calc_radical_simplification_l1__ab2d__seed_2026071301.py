from fractions import Fraction
import random
from math import gcd

# Mocking the required external module structure as per "Clean-incremental DOMAIN" constraints

# Mocking the frozen sampled parameters from the prompt context
frozen_sampled_params = {"radicand": 27}

def generate(level=1, **kwargs):
    # Ensure we use the frozen parameters if provided in kwargs or fallback to default logic for generation
    # The task specifies "Frozen sampled parameters: {'radicand': 27}" must be used.
    
    radicand = frozen_sampled_params.get("radicand", 1)
    coeff_input = 1
    
    # Use the domain API to simplify
    simplified_coeff, square_free_radicand = RadicalOps.simplify_term(coeff_input, radicand)
    
    # Construct canonical LaTeX string for answer: coefficient * sqrt(radicand) or just number if radical is 1
    if square_free_radicand == 1 and simplified_coeff != 0:
        ans_str = str(simplified_coeff)
    else:
        if simplified_coeff == 1:
            ans_str = f"\\sqrt{{{square_free_radicand}}}"
        elif simplified_coeff == -1:
            ans_str = f"-\\sqrt{{{square_free_radicand}}}"
        else:
            # Handle negative radicands or complex cases not expected in level 1, but safe fallback
             if square_free_radicand < 0:
                 return {"question_text": "", "correct_answer": "", "oracle_payload": frozen_sampled_params}
             
             ans_str = f"{simplified_coeff}\\sqrt{{{square_free_radicand}}}"

    # Construct question text with formal LaTeX delimiters
    q_latex = r"Express $\\sqrt{" + str(radicand) + r"}$ in simplest form."
    
    return {
        "question_text": q_latex,
        "correct_answer": ans_str,
        "oracle_payload": frozen_sampled_params
    }