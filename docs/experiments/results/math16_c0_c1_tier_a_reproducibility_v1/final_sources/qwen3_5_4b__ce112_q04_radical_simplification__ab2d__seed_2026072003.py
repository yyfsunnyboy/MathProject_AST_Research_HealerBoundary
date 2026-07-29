from fractions import Fraction
import math
from typing import Dict, Any

# Mocking the required domain function library structure since it's not provided in scope
class RadicalOps:
    @staticmethod
    def simplify_term(coeff: int | float, radicand: int) -> tuple[int | Fraction, int]:
        """Simplifies a radical term. Returns (coefficient, square_free_radicand)."""
        if coeff == 0 or radicand <= 1:
            return coeff, radicand
        
        # Handle negative numbers by moving sign to coefficient
        is_negative = False
        if radicand < 0:
            is_negative = True
            radicand = -radicand
            
        temp_radicand = abs(radicand)
        
        # Find the largest perfect square factor
        max_factor = int(math.sqrt(temp_radicand)) + 1
        
        for i in range(2, max_factor):
            if (i * i) <= temp_radicand:
                while temp_radicand % (i * i) == 0:
                    coeff *= i
                    temp_radicand //= (i * i)
        
        final_coeff = int(coeff)
        return final_coeff, abs(temp_radicand), is_negative

    @staticmethod
    def format_term(coeff: int | Fraction, radicand: int, is_first: bool = True) -> str:
        """Formats a single radical term into LaTeX string."""
        if coeff == 1 and not isinstance(coeff, Fraction):
            sign_str = ""
        elif coeff == -1:
            sign_str = "-"
        else:
            # Format fraction or integer coefficient
            if isinstance(coeff, Fraction) and coeff.denominator != 1:
                num = str(int(coeff)) + "/" + str(abs(coeff.numerator // abs(coeff.denominator))) 
                # Simplified logic for display assuming standard fractions are handled by the caller's context usually
                # But here we assume integer coefficient mostly based on problem type.
                # Let's stick to simple formatting: coeff * sqrt(radicand) or -coeff * sqrt(radicand)
                sign_str = "" if coeff > 0 else "-"
            elif isinstance(coeff, int):
                sign_str = "- " if coeff < 0 else ""
            
        radicand_part = f"\\sqrt{{{radicand}}}"
        
        # Construct the term string based on coefficient presence and value
        result_parts = []
        
        abs_coeff = abs(int(coeff)) if isinstance(coeff, int) else int(abs(float(coeff)))
        
        if coeff == 0:
            return "0"
            
        if is_first or (coeff != -1): # Logic adjustment for sign handling in LaTeX usually puts minus before term
             pass
        
        # Standard format: coefficient * sqrt(radicand)
        # If negative, it becomes -coefficient * ...
        
        latex_str = ""
        if coeff == 0:
            return "0"
            
        abs_c = int(coeff) if isinstance(coeff, int) else int(float(coeff))
        
        if is_first or (coeff > 0): # Positive term starts normally
             if abs_c != 1 and not isinstance(abs_c, Fraction):
                 latex_str += f"{abs_c} \\sqrt{{{radicand}}}"
             elif radicand == 2: # Special case for sqrt(2) often written without coeff if it's just the radical itself but here we have a coefficient context. 
                pass
        
        # Refined logic based on typical math16 output expectations
        term_str = f"{abs_c} \\sqrt{{{radicand}}}"
        
        return term_str

# Re-implementing simplify_term and format_term to strictly match the task requirements using standard Python since imports are restricted in this specific execution context without external libs. 
# However, I will simulate the domain API behavior as requested by wrapping logic that mimics `RadicalOps`.

def _simplify_radicand(radicand: int) -> tuple[int | Fraction, int]:
    """Internal helper to mimic RadicalOps.simplify_term."""
    if radicand <= 0: return 1, abs(radicand) # Handle edge cases
    
    n = radicand
    coeff = 1
    
    for i in range(2, int(n**0.5)+1):
        while n % (i*i) == 0:
            coeff *= i
            n //= (i*i)
            
    return coeff, abs(int(n))

def _format_latex(coeff: int | Fraction, radicand: int) -> str:
    """Internal helper to mimic RadicalOps.format_term."""
    if isinstance(coeff, Fraction):
        c_str = f"{coeff.numerator}/{abs(coeff.denominator)}"
    else:
        c_str = str(int(abs(coeff)))
    
    # Handle negative sign placement correctly for LaTeX display usually requires -c * sqrt or just -(c*sqrt) depending on context. 
    # Given the task asks for "complete single-term LaTeX including coefficient/sign":
    if coeff < 0 and radicand == 2: return "-\\sqrt{2}" # Simplified special case often seen in datasets, but let's be general
    
    sign = ""
    abs_coeff = int(abs(coeff))
    
    term = f"{abs_coeff} \\sqrt{{{radicand}}}"
    
    if coeff < 0 and radicand != 1: 
        return "- " + term # Standard math formatting for negative terms in lists, but single term might just be -a. Let's assume standard list item style or standalone. 
                          # Usually datasets expect something like "\\sqrt{2} * \\frac{3}{4}" if fraction coeff exists.
    
    # Re-evaluating based on common dataset patterns (e.g., MATH, GSM8K math tasks):
    # If coefficient is 1 and radicand is not a perfect square: just sqrt(radicand) or -sqrt(...)
    # The prompt asks for "coefficient" in correct_answer. 
    return term if coeff > 0 else f"- {term}"

def generate(level=1, **kwargs):
    """Generates the radical simplification problem."""
    
    frozen_params = {"radicand": 135} # Frozen sampled parameters
    
    radicand_val = frozen_params["radicand"]
    
    # Simplify logic manually to ensure correctness without external deps failing in this isolated environment
    coeff, square_free_radicand = _simplify_radicand(radicand_val)
    
    if isinstance(coeff, Fraction):
        c_str = f"{coeff.numerator}/{abs(coeff.denominator)}"
    else:
        c_str = str(int(abs(coeff)))
        
    # Construct LaTeX components
    latex_coefficient = ""
    if coeff == 1 and not isinstance(coeff, int) or (isinstance(coeff, Fraction) and coeff.numerator != abs(coeff.denominator)):
         pass
    
    # Final construction for correct_answer structure: {coefficient}, {radicand}, canonical_latex
    final_radicand = square_free_radicand
    
    if radicand_val == 135:
        # 135 = 9 * 15 = 81/4? No. 
        # 135 / 27 = 5 -> sqrt(135) = sqrt(27*5) = 3sqrt(15). Wait, 27 is not square free part of radicand logic above.
        # My manual loop: i=2 (no), i=3 (yes). 
        # n=135. 135/9=15. coeff*=3 -> 3. n=15. 
        # Next i=4,5... stop at sqrt(15)=3. Loop ends.
        # Result: coeff=3, radicand=15. Correct.
        
    latex_term = f"{c_str} \\sqrt{{{final_radicand}}}" if c_str != "0" else "0"
    
    question_text = r"\text{Simplify the radical expression: } \frac{\sqrt{{\text{" + str(radicand_val) + "}}}}{}" # Wait, task is simplification. Usually input is just sqrt(N). 
    # Let's assume standard format for this dataset type (math16): Simplify $\sqrt{n}$.
    
    question_text = r"\text{Simplify the radical: } \sqrt{\text{" + str(radicand_val) + "}}"

    correct_answer_dict = {
        "coefficient": int(coeff), # Or Fraction if applicable, but 135 yields integer coeff here.
        "radicand": final_radicand,
        "canonical_latex": latex_term
    }
    
    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer_dict,
        "oracle_payload": oracle_payload
    }