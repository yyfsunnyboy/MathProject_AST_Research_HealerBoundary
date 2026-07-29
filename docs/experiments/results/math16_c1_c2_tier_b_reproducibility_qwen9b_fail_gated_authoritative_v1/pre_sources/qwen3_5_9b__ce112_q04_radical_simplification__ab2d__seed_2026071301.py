from fractions import Fraction
import random

# Mocking the required imports from a hypothetical library structure as per instructions
class RadicalOps:
    @staticmethod
    def simplify_term(coeff, radicand):
        # Simplify sqrt(n * k^2) -> k * sqrt(n)
        if coeff == 0 or radicand <= 1:
            return (coeff, radicand)
        
        temp_radicand = radicand
        simplified_coeff = 1
        
        d = 2
        while d * d <= temp_radicand:
            count = 0
            while temp_radicand % d == 0:
                count += 1
                temp_radicand //= d
            
            if count >= 2 and (count // 2) > 0:
                simplified_coeff *= (d ** (count // 2))
        
        return (simplified_coeff, temp_radicand)

    @staticmethod
    def format_term(coeff, radicand, is_first=True):
        # Format LaTeX term
        if coeff == 1 and not is_first:
            latex = f"\\sqrt{{{radicand}}}"
        elif coeff == -1 and not is_first:
            latex = f"-\\sqrt{{{radicand}}}"
        else:
            sign_str = "-" if coeff < 0 else ""
            abs_coeff = abs(coeff)
            
            # Handle coefficient formatting (e.g., 2 vs 4, fractions)
            if isinstance(abs_coeff, Fraction):
                num, den = abs_coeff.numerator, abs_coeff.denominator
                latex_part = f"\\frac{{{num}}}{{\\sqrt{{{radicand}}}}}"
                full_term = sign_str + latex_part
            else:
                # Integer coefficient
                if radicand == 1:
                    latex_part = str(abs_coeff)
                    full_term = sign_str + latex_part
                elif abs_coeff > 0 and is_first or (abs_coeff != 1):
                     latex_part = f"{sign_str}{abs_coeff}\\sqrt{{{radicand}}}" if not is_first else f"\\pm{abs_coeff}\\sqrt{{{radicand}}}" # Simplified logic for first term usually implies positive start unless specified otherwise, but standard math format: coeff sqrt(n)
                     full_term = latex_part.replace(" ", "") 
                elif abs_coeff == 1 and radicand != 1:
                    if is_first:
                        full_term = f"\\sqrt{{{radicand}}}" # Coefficient omitted for 1 at start usually, but let's stick to standard form c*sqrt(n) where c=1 often implied or explicit. Let's assume explicit 1 only if needed by format logic below. 
                    else:
                        full_term = f"\\sqrt{{{radicand}}}" # Wait, if coeff is 1 and not first term? Usually just sqrt(x). If it was -1, handled above.
                elif abs_coeff == 0:
                     return "0"

        # Re-evaluating standard LaTeX generation for the specific task context usually implies a clean string like "3\\sqrt{5}" or "\\sqrt{2}". 
        # Let's refine format_term to be robust based on typical math16 expectations.
        
        if coeff == 0: return "0"
        
        sign = "-" if coeff < 0 else ""
        abs_c = int(coeff) if isinstance(coeff, Fraction) and coeff.denominator == 1 else float(coeff) # Simplify logic
        
        # Re-implementing strictly based on the simplified result from simplify_term which returns (coeff, radicand) where radicand is square-free.
        
        c_val = coeff
        r_val = radicand
        
        if isinstance(c_val, Fraction):
            num, den = c_val.numerator, c_val.denominator
            
            # If denominator > 1: \frac{num}{\sqrt{r}} -> but usually we pull out square factors from denom too? 
            # simplify_term handles integer extraction. So r is square free. 
            # We assume the input to format_term comes after simplification where coeff might be fractional if original radicand had odd powers of primes in denominator (not applicable here as inputs are integers).
            
        term_str = ""
        
        if c_val == 1:
             term_str = f"\\sqrt{{{r_val}}}"
        elif c_val == -1:
             term_str = "-\\sqrt{{{r_val}}}"
        else:
            # Integer coefficient != +/- 1, or Fraction with denom=1 (handled as int)
            if isinstance(c_val, Fraction):
                num, den = c_val.numerator, c_val.denominator
                # If we have a fraction like 2/3 * sqrt(5), it's \frac{2}{\sqrt[6]{...}}? No. 
                # Standard simplification of integer radicand results in integer coeff and square-free int radicand.
                term_str = f"{sign}\\frac{{{num}}}{{\\sqrt{{{r_val}}}}}" if den != 1 else f"{sign}{c_val}\\\\sqrt{{{r_val}}}"
            else:
                 term_str = f"{sign}{c_val}\\sqrt{{{r_val}}}"

        return term_str


# Frozen sampled parameters
frozen_params = {"radicand": 135}

def generate(level=1, **kwargs):
    radicand_input = frozen_params.get("radicand", kwargs.get('radicand', None))
    
    # Task: Radical simplification for sqrt(radicand) -> coeff * sqrt(square_free_radicand)
    if radicand_input is None:
        raise ValueError("No radicand provided.")

    # Initial state: coefficient 1, full radicand input
    initial_coeff = 1
    
    # Simplify the term
    simplified_tuple = RadicalOps.simplify_term(initial_coeff, radicand_input)
    
    coeff_result = simplified_tuple[0]
    radicand_result = simplified_tuple[1]
    
    # Format the LaTeX string. 
    # Note: The prompt implies a single-term answer usually starting with positive sign or just the term.
    # We use format_term with is_first=True to get the standard representation of the first (and only) term in this context.
    latex_string = RadicalOps.format_term(coeff_result, radicand_result, is_first=True)
    
    # Construct correct_answer string. Usually "3\\sqrt{5}" or "\\frac{1}{2}\\sqrt{...}". 
    # Ensure no extra spaces if not needed, but LaTeX requires specific spacing often handled by the formatter logic above.
    # Let's ensure canonical_latex is clean.
    
    question_text = f"Simplify \\sqrt{{{radicand_input}}}."
    
    return {
        "question_text": question_text,
        "correct_answer": latex_string,
        "oracle_payload": frozen_params
    }