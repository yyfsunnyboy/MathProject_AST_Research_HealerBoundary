from fractions import Fraction
import random
from math import gcd

# Mocking the required external module structure as per "Clean-incremental DOMAIN" constraints
class RadicalOps:
    @staticmethod
    def simplify_term(coeff, radicand):
        # Simplify radical term by extracting square factors from radicand
        if not isinstance(radicand, int) or radicand < 0:
            return coeff, radicand
        
        temp_radicand = radicand
        extracted_coeff = 1
        
        d = 2
        while d * d <= temp_radicand:
            count = 0
            while temp_radicand % d == 0:
                count += 1
                temp_radicand //= d
            
            if count >= 2:
                # Extract pairs of factors as part of the coefficient
                num_pairs = count // 2
                extracted_coeff *= (d ** num_pairs)
        
        return int(extracted_coeff), temp_radicand

class CorePromptsDomainFunctionLibrary:
    RadicalOps = RadicalOps
    
def generate(level=1, **kwargs):
    # Frozen sampled parameters override any kwargs or defaults if present in the call context logic
    frozen_params = {"radicand": 27}
    
    radicand_input = frozen_params.get("radicand", random.randint(4, 50))
    
    # For level 1 (ce115_calc_radical_simplification_l1), we assume coefficient is implicitly 1 unless specified otherwise in a more complex task.
    # The prompt implies generating a question based on the radicand. 
    # We will construct an expression like "sqrt(radicand)".
    
    coeff_input = 1
    
    # Use domain API to simplify
    simplified_coeff, square_free_radicand = RadicalOps.simplify_term(coeff_input, radicand_input)
    
    # Construct canonical LaTeX for the answer: coefficient * sqrt(square-free-radicand)
    if simplified_coeff == 1 and square_free_radicand == 1:
        correct_answer_str = "1"
    elif simplified_coeff == 1:
        correct_answer_str = f"\\sqrt{{{square_free_radicand}}}"
    else:
        # Ensure coefficient is formatted correctly (no space if coeff is negative? usually standard form)
        sign = "-" if simplified_coeff < 0 else ""
        abs_coeff = -simplified_coeff if simplified_coeff < 0 else simplified_coeff
        correct_answer_str = f"{sign}\\{{{abs_coeff}}}\\sqrt{{{square_free_radicand}}}"

    # Construct question text using formal LaTeX delimiters
    question_text = f"Simplify the radical expression: \\sqrt{{{radicand_input}}}"
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer_str,
        "oracle_payload": frozen_params
    }