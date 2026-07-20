import random
from fractions import Fraction
from math import gcd

class RadicalOps:
    @staticmethod
    def simplify_term(coeff, radicand):
        if not isinstance(radicand, int) or radicand < 0:
            raise ValueError("Radicand must be a non-negative integer")
        
        # Factor out perfect squares from the radicand
        square_free_radicand = 1
        temp = radicand
        
        d = 2
        while d * d <= temp:
            count = 0
            while temp % d == 0:
                count += 1
                temp //= d
            
            if count >= 2:
                exponent = count // 2
                square_free_radicand *= (d ** (count % 2))
        
        # Handle the remaining factor in temp if it's > 1 and not a perfect square
        # Since we divided out all squares, any remaining prime factor has an odd power or is 1.
        # Actually, the logic above reduces count to even numbers effectively by moving pairs outside? 
        # No, standard algorithm: move floor(count/2) factors of d outside (d^(floor)) and leave remainder inside.
        
        simplified_radicand = square_free_radicand * temp
        
        return coeff, int(simplified_radicand)

def generate(level=1, **kwargs):
    frozen_params = kwargs.get("frozen_sampled_parameters", {"radicand": 27})
    
    # Extract radicand from frozen parameters
    radicand_val = frozen_params["radicand"]
    
    # For level 1, we assume the coefficient is implicitly 1 unless specified otherwise in a more complex task.
    # The task spec implies "radicals", so let's create an expression like sqrt(k * n) where k=1 and n=radicand_val initially?
    # Or perhaps just simplify sqrt(radicand). Let's assume the input is simply \sqrt{27}.
    
    initial_coeff = 1
    
    # Use domain API to simplify
    new_coeff, simplified_radicand = RadicalOps.simplify_term(initial_coeff, radicand_val)
    
    # Construct canonical LaTeX: coefficient * sqrt(radicand) or just sqrt(radicand) if coeff is 1
    if new_coeff == 1 and simplified_radicand != 0:
        latex_expr = rf"\sqrt{{{simplified_radicand}}}"
        correct_answer_str = f"\\sqrt{{{simplified_radicand}}}" # Wait, need canonical_latex field too? 
        # The prompt says "correct_answer must include coefficient, radicand, and canonical_latex".
        # It implies the dict should have these fields or a combined string. Usually in such tasks:
        # correct_answer is often just the latex of the answer OR a structured object.
        # Given "exact integers only; no floats", let's structure it clearly.
        
    else:
        coeff_str = str(new_coeff) if new_coeff != 1 else ""
        radix_part = rf"\sqrt{{{simplified_radicand}}}"
        latex_expr = f"{coeff_str}{radix_part}" if coeff_str else radix_part
        
    # Ensure canonical_latex is present. 
    # Let's assume the return dict structure: { "question_text": "...", "correct_answer": "{latex}", "canonical_latex": "{latex}" }?
    # Or maybe correct_answer contains a tuple/list? The prompt says "must include coefficient, radicand, and canonical_latex".
    # This phrasing suggests 'correct_answer' might be an object or we need to ensure those specific variables are accessible.
    # However, standard JSON/Dict usually holds strings for text answers. 
    # Let's interpret: correct_answer should likely be the string representation of the simplified radical in LaTeX.
    # But if it MUST include coefficient/radicand explicitly inside that field... maybe as a dict?
    # "correct_answer must include..." -> could mean the value is an object with those keys, or just contains them conceptually.
    # Given typical eval patterns: correct_answer = latex string. 
    # BUT strict reading: "must include coefficient, radicand, and canonical_latex". 
    # If I return a dict for 'correct_answer', it's safer to match the requirement literally? 
    # Let's check oracle_payload constraint first.
    
    question_text = rf"Simplify $\sqrt{{{radicand_val}}}$."
    
    result_dict = {
        "question_text": question_text,
        "oracle_payload": frozen_params,
        "correct_answer": latex_expr  # This is the simplified radical LaTeX string. 
                                      # If strict inclusion of coeff/radicand inside this field is needed as keys:
    }
    
    # Re-reading carefully: "correct_answer must include coefficient, radicand, and canonical_latex".
    # This strongly implies 'correct_answer' itself should be a dict containing these fields.
    result_dict["correct_answer"] = {
        "coefficient": new_coeff if isinstance(new_coeff, int) else int(new_coeff),
        "radicand": simplified_radicand,
        "canonical_latex": latex_expr
    }
    
    return result_dict