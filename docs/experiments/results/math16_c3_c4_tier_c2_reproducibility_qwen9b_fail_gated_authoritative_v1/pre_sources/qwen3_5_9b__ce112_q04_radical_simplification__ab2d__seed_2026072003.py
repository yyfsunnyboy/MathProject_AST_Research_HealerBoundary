from fractions import Fraction
import random
from math import gcd

# Mocking the required imports as they are not available in standard Python environments without specific package installation.
# In a real environment with `core.prompts.domain_function_library`, these would be actual function calls.
class RadicalOps:
    @staticmethod
    def simplify_term(coeff, radicand):
        # Simplify sqrt(n * k^2) -> k * sqrt(n)
        if coeff == 0 or radicand <= 0:
            return (coeff, radicand)
        
        temp_radicand = abs(radicand)
        simplified_coeff = 1
        
        while temp_radicand > 1:
            for i in range(2, int(temp_radicand**0.5) + 1):
                if temp_radicand % (i * i) == 0:
                    factor_sq = i * i
                    simplified_coeff *= i
                    temp_radicand //= factor_sq
        
        # Handle sign of original radicand in coefficient
        if radicand < 0 and coeff > 0:
            simplified_coeff = -simplified_coeff
            
        return (simplified_coeff, temp_radicand)

    @staticmethod
    def format_term(coeff, radicand, is_first=True):
        # Format LaTeX term
        sign_str = "-" if coeff == -1 else ""
        
        # Coefficient formatting
        if abs(coeff) != 1:
            coef_part = f"{coeff}"
        elif coeff > 0 and not is_first:
            coef_part = "+"
        elif coeff < 0:
            coef_part = "-"
        else:
            coef_part = "" # +1 or -1 handled by sign logic above, but need to be careful with first term
            
        if abs(coeff) == 1 and (is_first or not is_first): 
             # Re-evaluating simple case for latex generation inside format_term context usually implies full string construction
             pass

        # Let's reconstruct the standard LaTeX representation based on simplified values
        c_val = coeff
        r_val = radicand
        
        if abs(c_val) == 1:
            coef_str = ""
        else:
            coef_str = f"{c_val}"
            
        sign_prefix = "-" if (coef_str.startswith("-") or (abs(coef_str)==0)) else ("+" if not is_first and c_val > 0 else "")
        
        # Correction for the specific logic of format_term usually expected in these tasks:
        final_coeff = coef_str.lstrip("+").lstrip("-") if abs(c_val) != 1 else ""
        
        term_parts = []
        if sign_prefix == "-":
            term_parts.append("-")
            
        # Handle coefficient display
        if c_val > 0 and not is_first:
             term_parts.append(f"+{c_val}")
        elif abs(c_val) != 1:
             term_parts.append(str(abs(c_val)))
             
        radicand_str = f"{r_val}" if r_val == 1 else (f"\\sqrt{{{r_val}}}" if r_val > 0 else "i") # Assuming real domain mostly
        
        return "".join(term_parts) + ("+" if not is_first and c_val > 0 else "")

def generate(level=1, **kwargs):
    frozen_params = kwargs.get('frozen_sampled_parameters', {"radicand": 135})
    
    # Extract radicand from frozen parameters or default
    raw_radicand = frozen_params.get("radicand", 1)
    
    # Simplify the radical term: sqrt(raw_radicand) -> coeff * sqrt(square_free_part)
    simplified_coeff, square_free_rad = RadicalOps.simplify_term(1, raw_radicand)
    
    # Construct correct_answer string manually to ensure canonical LaTeX format as per domain constraints logic
    if abs(simplified_coeff) == 0:
        answer_str = "0"
    else:
        term_parts = []
        
        # Sign handling for the first (and only in this specific task context usually, but let's be robust)
        sign_needed = False
        
        # Coefficient part
        if abs(simplified_coeff) != 1:
            coef_str = str(abs(simplified_coeff))
            term_parts.append(coef_str)
        else:
            coef_str = ""
            
        # Radicand part
        radicand_val = square_free_rad
        
        # Construct LaTeX
        latex_term = f"\\sqrt{{{radicand_val}}}" if abs(simplified_coeff) == 1 and (simplified_coeff > 0 or raw_radicand < 0 else "") 
        
        final_answer_parts = []
        
        # Re-implementing format logic strictly for the output string construction to match expected canonical form
        c = simplified_coeff
        r = square_free_rad
        
        if abs(c) == 1:
            coef_latex = ""
        elif c > 0 and not (r==1): # If it's just a number, usually we don't write coefficient unless necessary or specific format required. 
             # However, standard simplification of sqrt(135) is 9sqrt(3). Coefficient must be shown if != 1.
            coef_latex = str(c)
        else:
            coef_latex = ""

        sign_latex = "-" if c < 0 and r > 0 else ("+" if (c > 0 and not is_first_term_logic(r==1)) else "") # Simplified logic
        
        # Let's build the string directly for correctness based on math rules:
        latex_str = f"{coef_latex}\\sqrt{{{r}}}" if abs(c) != 1 or r!=1 else (f"\\sqrt{{{r}}}" if c > 0 else "-\\sqrt{{{r}}}")
        
        # Refining the string construction to be canonical:
        term_parts = []
        
        # Determine sign and coefficient display
        has_coeff_display = abs(c) != 1
        
        if c < 0:
            term_parts.append("-")
            
        if not (c == -1): 
             term_parts.append(str(abs(c)))
             
        radicand_str = f"{r}" if r==1 else str(r) # Just the number inside sqrt usually, unless it's a product. Here single radical.
        
        final_latex = "".join(term_parts) + (f"\\sqrt{{{radicand_val}}}" if abs(c)==1 or not has_coeff_display else f"{coef_latex}\\sqrt{{{radicand_val}}}")

    # Re-evaluating the specific requirement: "correct_answer must include coefficient, radicand, and canonical_latex."
    # This implies a structured dict inside correct_answer? Or just the string representation containing these elements.
    # Given typical task formats for this prompt style (ce112), correct_answer is often the full LaTeX string or a specific object.
    # Let's assume it wants the final simplified expression as a string, but also explicitly ensuring components are present if parsed.
    
    # Actually, looking at "canonical_latex" requirement in keys suggests:
    # Maybe correct_answer should be an object? 
    # Re-reading: "correct_answer must include coefficient, radicand, and canonical_latex."
    # This likely means the string itself represents these, OR it's a dict. 
    # But usually `generate` returns question_text (str), correct_answer (str or latex), oracle_payload (dict).
    
    # Let's construct the final LaTeX string properly:
    if raw_radicand == 0:
        ans_str = "0"
    else:
        c, r = RadicalOps.simplify_term(1, raw_radicand)
        
        parts = []
        sign = ""
        coef_part = ""
        
        if abs(c) != 1:
            coef_part = str(abs(c))
            
        if c < 0 and (abs(coef_part) == 0 or True): # If negative, start with minus
             sign = "-"
             
        term_str = f"{sign}{coef_part}\\sqrt{{{r}}}" if abs(c) != 1 else (f"\\sqrt{{{r}}}" if c > 0 else "-\\sqrt{{{r}}}")
        
        # Handle the case where coefficient is implicit +1 or -1
        final_latex_str = term_str
        
    question_text = f"Simplify \\sqrt{{{raw_radicand}}}"
    
    return {
        "question_text": question_text,
        "correct_answer": final_latex_str,
        "oracle_payload": frozen_params
    }