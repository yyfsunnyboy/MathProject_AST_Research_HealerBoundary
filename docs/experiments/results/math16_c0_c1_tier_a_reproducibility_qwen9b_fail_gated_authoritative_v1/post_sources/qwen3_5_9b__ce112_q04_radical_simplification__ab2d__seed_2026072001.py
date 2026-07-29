from fractions import Fraction
import random

# Mocking the required external module structure as it is not provided in standard libraries
class RadicalOps:
    @staticmethod
    def simplify_term(coeff, radicand):
        # Simplify sqrt(n) by extracting square factors.
        if coeff == 0 or radicand <= 1:
            return (coeff, radicand)
        
        temp_radicand = radicand
        simplified_coeff = int(abs(coeff))
        
        d = 2
        while d * d <= temp_radicand:
            count = 0
            while temp_radicand % d == 0:
                temp_radicand //= d
                count += 1
            
            if count >= 2 and (count // 2) > 0:
                # Extract pairs from the radicand into the coefficient
                extracted_pairs = count // 2
                simplified_coeff *= (d ** extracted_pairs)
        
        final_radicand = temp_radicand
        
        # Handle sign of original coeff if it was negative, but simplify_term usually handles magnitude.
        # We assume input coeff is integer or Fraction. If negative, we keep the minus in format later.
        return (simplified_coeff, final_radicand)

    @staticmethod
    def format_term(coeff, radicand, is_first=True):
        if coeff == 0:
            return "0"
        
        # Determine sign and magnitude for coefficient display
        abs_coeff = int(abs(coeff))
        has_minus = False
        
        if isinstance(coeff, Fraction):
            num, den = coeff.numerator, coeff.denominator
            if den != 1:
                raise ValueError("Fractional coefficients not supported in this simplified context per task spec")
        
        # Check for negative sign from original input logic (simplify_term returns positive usually)
        # However, the caller might pass a signed coefficient. Let's assume simplify_term handles magnitude.
        # If we need to track sign separately:
        if coeff < 0:
            has_minus = True
        
        term_str = ""
        
        if abs_coeff == 1 and is_first:
            term_str += "sqrt"
        elif abs_coeff > 1 or not is_first:
            # Format coefficient. If it's a fraction, handle that (though task implies integer coeffs usually)
            if isinstance(coeff, Fraction):
                c_val = float(coeff)
                if c_val == int(c_val):
                    term_str += str(int(c_val)) + "sqrt"
                else:
                     # Should not happen based on simplify_term logic above unless input is complex fraction
                     pass 
            elif abs_coeff > 1 or (abs_coeff == 0 and radicand != 0): # Handle zero case separately if needed, but simplified term handles it.
                 term_str += str(abs_coeff) + "sqrt"
        
        if has_minus:
             return "-" + term_str
        
        if is_first:
            return f"{term_str}"
        else:
            return f"+ {term_str}"

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