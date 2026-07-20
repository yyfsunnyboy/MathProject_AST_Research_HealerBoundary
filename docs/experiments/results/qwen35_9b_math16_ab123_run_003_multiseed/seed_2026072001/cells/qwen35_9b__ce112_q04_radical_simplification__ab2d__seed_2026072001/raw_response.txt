from fractions import Fraction
import random

# Mocking the required external module structure as it is not provided in standard libraries
class RadicalOps:
    @staticmethod
    def simplify_term(coeff, radicand):
        # Simplify radical term by extracting square factors from radicand
        if coeff == 0 or radicand <= 0:
            return (Fraction(0), 1)
        
        temp_radicand = int(radicand)
        simplified_coeff = Fraction(int(coeff))
        
        i = 2
        while i * i <= temp_radicand:
            count = 0
            while temp_radicand % i == 0:
                count += 1
                temp_radicand //= i
            
            if count >= 2:
                num_pairs = count // 2
                simplified_coeff *= (i ** num_pairs)
                
        canonical_radicand = int(temp_radicand)
        
        # Ensure coefficient is an integer or Fraction, radicand positive square-free
        return (simplified_coeff, canonical_radicand)

    @staticmethod
    def format_term(coeff, radicand, is_first=True):
        if coeff == 0:
            return "0"
        
        sign = "-" if float(coeff) < 0 else ""
        abs_coeff = int(abs(float(coeff))) if isinstance(coeff, Fraction) and coeff.denominator == 1 else str(abs(coeff))
        
        # Determine coefficient display style (e.g., sqrt(2) vs 3sqrt(5))
        term_str = f"{sign}\\frac{{{abs_coeff}}}{{\\sqrt{{{radicand}}}}}" if abs_coeff != 1 and radicand > 0 else ""
        
        if is_first:
            return term_str
        
        # For non-first terms, just the coefficient part usually in a sum context
        if float(coeff) < 0:
             term_str = f"-\\frac{{{abs_coeff}}}{{\\sqrt{{{radicand}}}}}"
        else:
             term_str = f"+{term_str}".replace("+", "") # Remove leading + for addition
        
        return term_str

# Global frozen parameters as specified in the prompt context
frozen_params = {"radicand": 135}

def generate(level=1, **kwargs):
    radicand_val = kwargs.get("radicand", frozen_params["radicand"])
    
    # Since no specific coefficient was provided in frozen params or level logic for a single term generation:
    # We assume the task is to simplify 1 * sqrt(radicand) based on standard simplification tasks.
    coeff = 1
    
    simplified_coeff, canonical_radicand = RadicalOps.simplify_term(coeff, radicand_val)
    
    question_text = f"Simplify $\\sqrt{{{radicand_val}}}$."
    
    # Format the correct answer term (assuming this is a single-term response for difficulty level 1)
    formatted_answer = RadicalOps.format_term(simplified_coeff, canonical_radicand, is_first=True)
    
    # Construct canonical_latex string explicitly as requested: coefficient, radicand, and canonical_latex structure
    if simplified_coeff == Fraction(0):
        correct_ans_str = "0"
    else:
        coeff_display = str(int(simplified_coeff)) if isinstance(simplified_coeff, int) or (isinstance(simplified_coeff, float) and simplified_coeff.is_integer()) else f"{simplified_coeff.numerator}/{simplified_coeff.denominator}"
        
        # If coefficient is 1 or -1, omit it in standard LaTeX radical notation unless required otherwise. 
        # Standard form: c * sqrt(n). Here we use the formatted term which handles spacing/sign logic implicitly if needed,
        # but let's build a robust canonical string manually to match "coefficient, radicand" requirement clearly.
        
        final_coeff = int(simplified_coeff) if simplified_coeff.denominator == 1 else f"{simplified_coeff.numerator}/{simplified_coeff.denominator}"
        
        if float(final_coeff) < 0:
            sign_str = "-"
            val = abs(int(float(final_coeff))) if isinstance(simplified_coeff, Fraction) and simplified_coeff.denominator==1 else int(abs(float(final_coeff))) # Simplified logic for display
            
            # Re-evaluating format_term output vs manual construction. 
            # Let's stick to the mathematical truth: coeff * sqrt(radicand).
            
        correct_ans_str = f"{sign}{final_coeff}\\sqrt{{{canonical_radicand}}}" if sign != "" else (f"\\frac{{1}}{{\\sqrt{{{canonical_radicand}}}}}" if float(final_coeff) == 0.5 else f"{int(float(final_coeff))}\\\\sqrt{{{canonical_radicand}}}".replace(" ", "")).lstrip("-")
        
        # Correction: Use the specific format_term result for consistency with domain API usage requirement, 
        # but ensure it matches "coefficient, radicand" description in correct_answer field.
        # Let's rebuild to be safe and explicit about components.
        
        if simplified_coeff.denominator == 1:
            c = int(simplified_coeff)
            latex_c = str(c) if abs(c) != 1 else ""
            sign_latex = "-" if c < 0 else ("" if c > 0 else "") # Handle zero separately above
            
            if c == 0:
                correct_ans_str = "0"
            elif c < 0:
                 latex_c_part = str(-c) + "\\sqrt{" + str(canonical_radicand) + "}"
                 sign_latex = "-"
            else:
                 latex_c_part = (str(c) if int(float(simplified_coeff)) != 1 else "") + "\\sqrt{" + str(canonical_radicand) + "}"
            
            # Actually, standard LaTeX for radicals usually writes -\\sqrt or \\frac{c}{...} 
            # Let's use the format_term logic but ensure canonical_latex is a clean string.
            
    # Refined Canonical Answer Construction:
    if simplified_coeff == 0:
        correct_ans_str = "0"
    else:
        c_val = int(simplified_coeff) if simplified_coeff.denominator == 1 else f"{simplified_coeff.numerator}/{simplified_coeff.denominator}"
        
        # If coefficient is a fraction, use \frac{num}{den}\sqrt{} or just num/den sqrt? 
        # Usually simplification results in integer coefficients. Let's assume canonical_radicand extraction yields integer coeff here for level 1 unless radicand has cube factors etc. but problem says square root simplification.
        
        if simplified_coeff.denominator == 1:
            c = int(simplified_coeff)
            latex_c = str(c).lstrip("-") # Handle sign separately? No, keep negative in string or prefix -
            
            if c < 0:
                correct_ans_str = f"-\\sqrt{{{canonical_radicand}}}" * (abs(int(float(simplified_coeff))) == 1) \
                    if abs(int(float(simplified_coeff))) == 1 else f"{c}\\\\sqrt{{{canonical_radicand}}}".replace(" ", "") # This is getting messy. Let's trust format_term but ensure it's in the dict correctly.
            else:
                latex_c = str(c).lstrip("-") if c != 0 else "1"
                
        # Re-implementing simple, robust canonical string generation based on simplified_coeff and canonical_radicand
        
        sign_str = "-" if float(simplified_coeff) < 0 else ""
        
        if abs(float(simplified_coeff)) == 1:
            coeff_part = ""
        elif isinstance(simplified_coeff, Fraction):
             # For fractions like 2/3, we might need \frac{2}{3}\sqrt{}, but standard simplification usually avoids this unless necessary. 
             # Assuming integer coefficients for level 1 radical simplification of integers.
            coeff_part = str(int(float(simplified_coeff))) + "/" if simplified_coeff.denominator != 1 else ""
        else:
            coeff_part = str(abs(int(float(simplified_coeff))))

        # Wait, let's just use the format_term result as correct_answer string and build canonical_latex from parts for clarity.
        formatted_str = RadicalOps.format_term(simplified_coeff, canonical_radicand, is_first=True)
        
        if float(formatted_str.strip()) < 0:
             pass
            
        # Let's construct manually to be precise with "coefficient" requirement in the field name explanation.
        final_c_str = str(int(float(simplified_coeff))) if simplified_coeff.denominator == 1 else f"{simplified_coeff.numerator}/{simplified_coeff.denominator}"
        
        # Remove sign for coefficient part, add it back at start or handle via LaTeX logic? 
        # Better: "coefficient" in the field usually implies the number.
        
        correct_ans_str = formatted_str
        
    canonical_latex = f"{sign_str}\\sqrt{{{canonical_radicand}}}" if abs(float(simplified_coeff)) == 1 else (f"{int(abs(float(simplified_coeff)))}{sign_str}\\\\sqrt{{{canonical_radicand}}}").replace(" ", "")
    
    # Correction: If coeff is negative, format_term returns "-\\frac{...}". 
    # Let's just use the formatted string as correct_answer.
    canonical_latex = RadicalOps.format_term(simplified_coeff, canonical_radicand, is_first=True)

    return {
        "question_text": question_text,
        "correct_answer": canonical_latex,
        "oracle_payload": frozen_params
    }