from fractions import Fraction
import random

def generate(level=1, **kwargs):
    frozen_params = kwargs.get("frozen_sampled_parameters", {"radicand": 27})
    
    # Extract radicand from frozen parameters or use default if not provided in a way that overrides logic
    radicand_input = frozen_params.get("radicand")
    
    # Ensure we work with integers as per "Exact integers only" requirement for inputs/outputs where applicable, 
    # but the domain API returns Fraction for coefficient. We must handle this carefully to return exact integers if possible or follow spec.
    # The task says correct_answer must include coefficient... Exact integers only; no floats.
    # However, RadicalOps.simplify_term returns tuple[int | Fraction, int]. 
    # If the result is a fraction like 3/1, we might need to convert? Or just return as is if it's an integer type in Python (Fraction(3) != 3).
    # Let's assume standard math simplification: sqrt(27) = 3*sqrt(3). Coefficient=3.
    
    from core.prompts.domain_function_library import RadicalOps
    
    coeff, square_free_radicand = RadicalOps.simplify_term(radicand_input, radicand_input)
    
    # Construct the canonical LaTeX string: coefficient * sqrt(square-free radicand)
    # If coefficient is 1 or -1, usually just write sqrt(...). But let's stick to a standard format.
    # The spec says "include coefficient". Let's assume if coeff is Fraction(3), we print '3'. 
    # We need to ensure the output string uses LaTeX delimiters.
    
    def get_coeff_str(c):
        from fractions import Fraction as F
        c_val = float(c)
        if abs(c_val - round(c_val)) < 1e-9:
            return str(int(round(c_val)))
        else:
            # Should not happen with exact integers input and standard radicals, but fallback to string rep
            return f"{c}"

    coeff_str = get_coeff_str(coeff)
    
    if coeff == 0 or (isinstance(coeff, Fraction) and abs(float(coeff)) < 1e-9):
        latex_expr = "\\sqrt{" + str(square_free_radicand) + "}"
    else:
        # Handle negative coefficients? The radicand is usually positive in these tasks. 
        # If coeff is -3, we write "-3\\sqrt{...}".
        if isinstance(coeff, Fraction):
            sign = "-" if float(coeff) < 0 else ""
            abs_coeff_str = get_coeff_str(abs(coeff))
            latex_expr = f"{sign}{abs_coeff_str}\\sqrt{{{square_free_radicand}}}"
        else:
             # Fallback for integer coeff directly (though API returns Fraction or int)
             if float(coeff) < 0:
                 sign = "-"
                 abs_c = -coeff
             else:
                 sign = ""
                 abs_c = coeff
             
             latex_expr = f"{sign}{abs_c}\\sqrt{{{square_free_radicand}}}"

    # Ensure the radicand in LaTeX is formatted correctly (no spaces inside sqrt usually)
    
    question_text = "Simplify \\sqrt{" + str(radicand_input) + "}."
    correct_answer_latex = latex_expr
    
    return {
        "question_text": question_text,
        "correct_answer": f"{coeff_str}\\sqrt{{{square_free_radicand}}}", # Reconstructing to ensure clean string representation if Fraction was used internally but we want exact text. 
                                # Actually, let's use the logic derived above for correct_answer directly.
    }

# Wait, I need to fix the return statement inside generate based on my thought process in the function body properly without defining it twice or having errors.
# Let me rewrite cleanly.

from core.prompts.domain_function_library import RadicalOps
import re

def generate(level=1, **kwargs):
    frozen_params = kwargs.get("frozen_sampled_parameters", {"radicand": 27})
    
    radicand_input = frozen_params["radicand"]
    
    # Call domain API
    coeff_raw, square_free_radicand = RadicalOps.simplify_term(radicand_input, radicand_input)
    
    # Convert coefficient to a clean string representation (integer if possible)
    from fractions import Fraction as F
    
    def format_coeff(c):
        if isinstance(c, int):
            return str(c)
        elif isinstance(c, float):
            # If it's an integer value in float form due to some reason? Unlikely here.
            return str(int(round(c))) 
        else:
            val = c.numerator / c.denominator
            if abs(val - round(val)) < 1e-9:
                return str(int(round(val)))
            else:
                # Return fraction string like "3/4" or just numerator? Task implies integer coefficients usually.
                # For sqrt simplification, coeff is always integer.
                return f"{c.numerator}/{c.denominator}"

    c_str = format_coeff(coeff_raw)
    
    # Build LaTeX answer
    if float(c_str.replace('/', '')) == 0: 
        ans_latex = r"\sqrt{" + str(square_free_radicand) + "}"
    else:
        sign = "-" if coeff_raw < 0 else ""
        abs_c_val = -coeff_raw if coeff_raw < 0 else float(coeff_raw) # This logic is messy with mixed types. 
        # Let's simplify: use string manipulation on the formatted coefficient and check sign from raw value
        
        c_sign = "minus" if isinstance(coeff_raw, F) and (coeff_raw.numerator % coeff_raw.denominator == 0 and int(coeff_raw.numerator/coeff_raw.denominator) < 0) else ""
        
        # Simpler approach: 
        val_float = float(coeff_raw)
        sign_str = "-" if val_float < 0 else ""
        abs_val_int = round(abs(val_float))
        c_final_str = f"{sign_str}{abs_val_int}"
        
        ans_latex = r"\sqrt{" + str(square_free_radicand) + "}"
        if float(coeff_raw) != 1 and float(coeff_raw) != -1: # If coeff is not +/- 1, include it. 
            # Wait, standard convention: 3\sqrt{2} vs \sqrt{8}. 
            # My code above handles sign separately.
            pass
            
        if abs_val_int == 0:
             ans_latex = r"\sqrt{" + str(square_free_radicand) + "}"
        else:
             ans_latex = f"{sign_str}{abs_val_int}\\sqrt{{{square_free_radicand}}}"

    # Re-evaluating the logic to be robust. 
    # If coeff is 3, square_free is 3 -> "3\\sqrt{3}".
    # If coeff is -2, square_free is 5 -> "-2\\sqrt{5}".
    
    final_ans = ans_latex
    
    return {
        "question_text": f"Simplify \\sqrt{{{radicand_input}}}.",
        "correct_answer": final_ans,
        "oracle_payload": frozen_params
    }