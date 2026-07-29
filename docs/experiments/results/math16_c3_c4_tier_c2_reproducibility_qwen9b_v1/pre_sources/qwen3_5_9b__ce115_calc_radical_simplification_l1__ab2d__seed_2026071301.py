from fractions import Fraction
import random
from math import gcd

# Mocking the required external module structure as per "Clean-incremental DOMAIN" constraints
class RadicalOps:
    @staticmethod
    def simplify_term(coeff, radicand):
        """
        Simplifies a radical term.
        Returns (coefficient, square-free_rad) tuple.
        Logic for level 1 radicals: extract perfect squares from the radicand.
        """
        if not isinstance(radicand, int) or radicand <= 0:
            return coeff, radicand
        
        # Factor out perfect squares
        temp_radicand = radicand
        extracted_factor = 1
        
        d = 2
        while d * d <= temp_radicand:
            count = 0
            while temp_radicand % d == 0:
                count += 1
                temp_radicand //= d
            
            if count >= 2:
                pairs = count // 2
                extracted_factor *= (d ** pairs)
        
        # Calculate new coefficient and radicand
        simplified_coeff = coeff * extracted_factor
        square_free_radicand = temp_radicand
        
        return simplified_coeff, square_free_radicand

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