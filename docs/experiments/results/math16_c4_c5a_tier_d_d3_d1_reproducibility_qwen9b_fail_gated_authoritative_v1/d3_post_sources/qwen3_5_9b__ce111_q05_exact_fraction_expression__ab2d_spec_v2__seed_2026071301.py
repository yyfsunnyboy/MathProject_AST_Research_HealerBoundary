# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    from core.prompts.domain_function_library import FractionOps
    
    # Frozen sampled parameters as defined in task specification
    frozen_params = {"expression": "9/22 + 11/18 - (23/22 - 7/18)"}
    
    # Parse components using native Python for robustness before passing to API if needed, 
    # but strictly following the instruction to use FractionOps for arithmetic.
    # We will construct fractions manually or via string parsing compatible with standard logic,
    # then apply FractionOps methods as per signature cards (create/from_parts).
    
    # Define terms: 9/22 + 11/18 - (23/22 - 7/18)
    # Term A: 9/22
    term_a = FractionOps.from_parts(9, 22)
    
    # Term B: 11/18
    term_b = FractionOps.from_parts(11, 18)
    
    # Inner Parenthesis: (23/22 - 7/18)
    inner_part_1 = FractionOps.from_parts(23, 22)
    inner_part_2 = FractionOps.from_parts(7, 18)
    inner_result = FractionOps.sub(inner_part_1, inner_part_2)
    
    # Full Expression: A + B - InnerResult
    step1 = FractionOps.add(term_a, term_b)
    final_fraction = FractionOps.sub(step1, inner_result)
    
    # Extract numerator and denominator from the resulting Fraction object
    num = final_fraction.numerator
    den = final_fraction.denominator
    
    # Construct canonical LaTeX for irreducible fraction: \frac{num}{den}
    import re
    latex_num_str = str(num).replace("-", "\\text{-}") if isinstance(num, int) else str(num)
    latex_den_str = str(den).replace("-", "\\text{-}") if isinstance(den, int) else str(den)
    
    # Handle negative sign placement for canonical LaTeX (usually before fraction or in numerator)
    # Standard convention: \frac{a}{b} where a can be negative. 
    # If denominator is 1, just the number. Here den != 1.
    if num < 0 and den > 0:
        latex_str = f"-\\frac{{{abs(num)}}}{{{den}}}"
    else:
        latex_str = f"\\frac{{{num}}}{{{den}}}"

    # Construct correct_answer dict with required fields
    correct_answer = {
        "numerator": num,
        "denominator": den,
        "canonical_latex": latex_str
    }
    
    question_text = r"The value of the expression $9/22 + 11/18 - (23/22 - 7/18)$ is:"

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }