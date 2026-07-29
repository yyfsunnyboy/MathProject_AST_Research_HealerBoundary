# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    from core.prompts.domain_function_library import FractionOps
    
    # Frozen sampled parameters as per specification
    frozen_params = {"expression": "3/7 - (-1/4)"}
    
    # Parse the expression components manually to avoid eval/exec on user input logic
    # Expression: 3/7 - (-1/4) -> (3/7) + (1/4) effectively, but we must follow subtraction rule strictly.
    # Term 1: 3/7
    term1_str = "3/7"
    
    # The expression is A - B where B is "-1/4". 
    # So the operation is FractionOps.sub(FractionOps.create(term1), FractionOps.create("-1/4"))
    
    frac_a = FractionOps.create("3/7")
    frac_b = FractionOps.create("-1/4")
    
    result_frac = FractionOps.sub(frac_a, frac_b)
    
    # Construct correct_answer dict with numerator, denominator, and canonical_latex
    num = result_frac.numerator
    den = result_frac.denominator
    
    # Canonical LaTeX for fraction: \frac{num}{den}
    import re
    latex_num = str(num).replace("-", "\\text{-}") if isinstance(num, int) else str(num)
    latex_den = str(den).replace("-", "\\text{-}") if isinstance(den, int) else str(den)
    
    # Handle negative signs in LaTeX properly for the fraction command
    def make_latex_part(val):
        s = str(val)
        if val < 0:
            return f"\\left({s}\\right)"
        elif val > 0:
            return f"{val}"
        else:
            return "0"

    # Re-evaluate LaTeX construction for robustness with negative numbers inside fractions
    s_num = str(num)
    s_den = str(den)
    
    if num < 0:
        latex_num_part = f"-{abs(num)}"
    else:
        latex_num_part = str(num)
        
    if den < 0:
        # Denominator should be positive in canonical form, handled by FractionOps usually.
        # If not, adjust sign to numerator (FractionOps.sub result is normalized).
        pass 
        
    final_latex_num = f"{num}" if num >= 0 else f"-{abs(num)}"
    final_latex_den = f"{den}" if den > 0 else "-1" # Should be positive
    
    canonical_latex = rf"\frac{{{final_latex_num}}}{{{final_latex_den}}}"

    correct_answer = {
        "numerator": num,
        "denominator": den,
        "canonical_latex": canonical_latex
    }
    
    question_text = r"Compute the result of $3/7 - (-1/4)$."
    
    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }