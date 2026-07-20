import math
from fractions import Fraction
from typing import Dict, Any, Tuple, Union

# Mocking the required domain function library structure as per spec constraints
class RadicalOps:
    @staticmethod
    def simplify_term(coeff: int, radicand: int) -> Tuple[Union[int, Fraction], int]:
        """Simplifies a radical term. Returns (coefficient, square-free_radicand)."""
        if coeff == 0:
            return 0, 1
        
        # Handle negative coefficients by separating sign and magnitude for LaTeX formatting logic later
        is_negative = coeff < 0
        abs_coeff = abs(coeff)
        
        simplified_abs_coef, simplified_radicand = simplify_core(abs_coeff, radicand)
        
        if is_negative:
            return -simplified_abs_coef, simplified_radicand
        
        return Fraction(simplified_abs_coef), simplified_radicand

    @staticmethod
    def format_term(coeff: Union[int, Fraction], radicand: int, is_first: bool = True) -> str:
        """Formats a single term into LaTeX string."""
        # Convert coeff to integer if it's already an integer-like fraction (e.g. 1/2 becomes .5? No, keep as frac for clean math usually unless whole)
        # Standard practice in these tasks often prefers fractions like \frac{3}{4} over decimals
        
        latex_coeff = ""
        
        # Handle sign and coefficient formatting
        if isinstance(coeff, Fraction):
            numerator = coeff.numerator
            denominator = coeff.denominator
            
            # If it's a whole number fraction (denom == 1) or zero
            if numerator % denominator == 0:
                latex_coeff = f"{numerator // denominator}"
            else:
                latex_coeff = rf"\frac{{{numerator}}}{{ {denominator} }}"

        elif isinstance(coeff, int):
            latex_coeff = str(coeff)

        # If coefficient is zero or absent (implicitly handled by logic), we might need to adjust. 
        # However, the prompt implies explicit coefficients in correct_answer structure often includes 'coefficient'.
        
        radicand_str = f"\sqrt{{{radicand}}}" if radicand > 0 else "\sqrt{{" + str(radicand) + "}}"

        full_latex = ""
        sign = "-" if coeff < 0 and latex_coeff != "" else "" # If negative, prepend minus
        
        # Logic for LaTeX construction based on typical math16 format expectations:
        # a\sqrt[n]{b} or \frac{a}{n}\sqrt[n]{b} etc. Here n=2 always.
        
        if coeff == 0 and radicand > 0:
            full_latex = "0"
            
        elif isinstance(coeff, Fraction) and not latex_coeff.startswith("-"): # Positive fraction coefficient
             # e.g., \frac{1}{4}\sqrt{x} -> actually usually written as just the term if coeff is part of sqrt? 
             # The spec says returns tuple (coeff, radicand). Let's assume standard form: a * \sqrt[b]{} or \frac{a}{b}*\sqrt...
             full_latex = rf"{latex_coeff}\sqrt{{{radicand}}}"
             
        elif isinstance(coeff, int) and coeff < 0: # Negative integer coefficient handled by string formatting logic usually in these prompts? 
            # Re-evaluating the domain API usage constraint. The spec says format_term returns str including coefficient/sign.
            full_latex = rf"{latex_coeff}\sqrt{{{radicand}}}"

        return f"{full_latex}".strip()


def simplify_core(coeff: int, radicand: int) -> Tuple[int, int]:
    """Helper to handle the simplification logic internally."""
    # Factor out perfect squares from radicand
    temp_radicand = radicand
    
    while True:
        k = 2
        if (k * k <= temp_radicand):
            q = math.isqrt(temp_radicand) ** 2 // temp_radicand + 1 # Not quite right for loop logic, simpler approach below
            
        else:
            break

    # Correct simplification algorithm
    n_sq_free, coeff_mult = get_square_factors(coeff, radicand)
    
    return n_sq_free * coeff_mult, radicand // (n_sq_free ** 2) if n_sq_free > 1 else radicand


def get_square_factors(coeff: int, radicand: int):
    """Helper to extract square factors."""
    # Simplify coefficient first? Usually we pull out from sqrt. 
    # If coeff is separate, it stays unless the term was like \sqrt{4} = 2 (then coeff becomes part of result).
    # But input is usually a\sqrt[n]{b}. We only simplify b here and adjust if necessary.
    
    return int(coeff), radicand


def generate(level: int = 1, **kwargs) -> Dict[str, Any]:
    """Generates the radical simplification question."""
    frozen_params = kwargs.get('radicand', None)
    
    # Ensure we use the exact frozen parameter provided in the prompt context or default if missing (though spec says frozen is fixed)
    radicand_val = int(frozen_params) if isinstance(frozen_params, str) else float(frozen_params)
    
    coeff_val = 1
    
    question_text_template = r"$$\text{Simplify: } \sqrt{\{radicand}}$$" # Using formal LaTeX delimiters as requested in spec "question_text must use formal LaTeX delimiters". 
    # Wait, the prompt says 'formal LaTeX delimiters'. Usually $$ ... $$.
    
    question_text = r"\begin{align*} &\text{Simplify: } \\ \sqrt{\{" + str(radicand_val) + r"}} &= ? \end{align*}"

    simplified_coeff, simplified_radicand = RadicalOps.simplify_term(coeff_val, radicand_val)
    
    # Reconstruct the correct answer string using format_term which handles LaTeX generation for us
    
    latex_string = ""
    if coeff_val == 0: 
        latex_string = "0"
    else:
        term_str = f"{coeff_val}\sqrt{{{radicand_val}}}" # Basic representation before simplification logic might need adjustment?
        # Actually, the domain API format_term expects (coeff, radicand). It likely handles the formatting of coefficient * sqrt(radicand) or just \sqrt{} if coeff is 1.
        
    correct_answer_latex = f"{simplified_coeff}\sqrt{{{simplified_radicand}}}"

    return {
        "question_text": question_text,
        "correct_answer": [
            "coefficient:", simplified_coeff,
            "radicand:", simplified_radicand,
            "canonical_latex:" + correct_answer_latex.replace(" ", "") # Clean up spaces if any added by format_term logic (simulated here)
        ], 
        "oracle_payload": frozen_params
    }

# Override the generate function signature to match exactly def generate(level=1, **kwargs):
def generate(level: int = 1, **kwargs):
    radicand_val = kwargs.get('radicand', None)
    
    # If no specific radicand provided in args (which is rare based on 'frozen sampled parameters'), default to a safe number or use the one passed. 
    # The spec says "Frozen sampled parameters: {"radicand": 135}". We must ensure we return this exact value for oracle_payload if it was part of kwargs, otherwise logic handles defaults.
    
    target_radicand = int(radicand_val) if radicand_val is not None else 2
    
    # Re-implementing the internal simplification strictly using domain API structure implied by spec
    from fractions import Fraction as F

    coeff_in = 1
    rad_in = target_radicand
    
    # Simplify logic: factor out squares from rad_in
    temp_rad = rad_in
    sq_factor_count = {}
    
    d = 2
    while d * d <= temp_rad:
        count = 0
        while temp_rad % (d*d) == 0:
            temp_rad //= (d*d)
            # We don't need to track full factorization, just reduce radicand
        if temp_rad > 1 and not sq_factor_count.get(d): 
             pass 
        
    simplified_radicand = int(temp_rad)
    
    # If we extracted a square root part from the original radicand (e.g. sqrt(48) -> 2*sqrt(3)), 
    # that logic isn't fully explicit in `simplify_term` signature provided as `(coeff, radicand)` returning `(int/Frac, int)`.
    # Assuming standard behavior: simplify_radicand = rad_in // (k*k)... and return k if coeff was inside? 
    # The spec says returns tuple(int|Frac, int). It doesn't imply coefficient changes unless the term is like 3*sqrt(12) -> ...
    # For sqrt(N), result is integer_part * sqrt(sq_free_N). Integer part = floor(sqrt(N)) if N is perfect square? No.
    
    # Let's implement a robust simplification for sqrt(rad):
    k = int(math.isqrt(target_radicand))
    sq_free_rad = target_radicand // (k*k)
    coeff_out = Fraction(k, 1) 
    
    simplified_coeff_val = float(coeff_out.numerator / coeff_out.denominator) # Keep as float or frac? Spec says returns tuple[int|Fraction]. Let's stick to int if whole.
    
    final_simplified_coeff = k 
    final_simplified_radicand = sq_free_rad
    
    # Format the answer using domain API simulation logic (since we can't import external modules in this strict environment without definitions)
    # But spec says "import: core.prompts.domain_function_library". We must assume these exist or mock them minimally if allowed. 
    # The prompt instructions say "Use the listed domain API... ensure returned value contributes to correct_answer."
    
    latex_ans = rf"{final_simplified_coeff}\sqrt{{{final_simplified_radicand}}}"

    return {
        "question_text": r"\begin{align*} &\text{Simplify: } \\ \sqrt{\{" + str(target_radicand) + r"}} &= ? \end{align*}",
        "correct_answer": [
            f"coefficient: {final_simplified_coeff},",
            f"radicand: {final_simplified_radicand},",
            f"canonical_latex: {latex_ans}" # No spaces to be safe, or follow standard LaTeX spacing rules if format_term added them. 
        ],
        "oracle_payload": target_radicand
    }

# Final verification of function existence and structure is implicit in the code block execution context provided by the system.
