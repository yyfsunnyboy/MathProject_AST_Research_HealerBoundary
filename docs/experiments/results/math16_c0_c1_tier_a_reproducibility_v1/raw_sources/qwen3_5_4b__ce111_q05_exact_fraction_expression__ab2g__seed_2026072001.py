def generate(level=1, **kwargs):
    question_text = r"Compute the exact fraction expression: \(\frac{9}{22} + \frac{11}{18} - \left( \frac{23}{22} - \frac{7}{18} \right)\)."
    
    # Calculate the result manually to ensure correctness
    # Expression: 9/22 + 11/18 - (23/22 - 7/18)
    # Combine terms with common denominators where possible or use LCM of 22 and 18 which is 198
    
    term1 = 9 / 22
    term2 = 11 / 18
    inner_parenthesis = (23 / 22) - (7 / 18)
    
    result_float = term1 + term2 - inner_parenthesis
    
    # Convert to fraction for irreducible form
    from fractions import Fraction
    frac_result = Fraction(term1).as_numer_denom() if isinstance(term1, float) else None
    
    # Re-calculate using integers directly to avoid floating point issues during conversion logic simulation
    # 9/22 + 11/18 - (23/22 - 7/18)
    # = 9/22 + 11/18 - 23/22 + 7/18
    
    # Group by denominator:
    # Denom 22 terms: 9/22 - 23/22 = (9-23)/22 = -14/22 = -7/11
    # Denom 18 terms: 11/18 + 7/18 = (11+7)/18 = 18/18 = 1
    
    # Total sum: (-7/11) + 1 = 4/11
    
    numerator, denominator = Fraction(9).as_numer_denom()[0], Fraction(23).as_numer_denom()[0]
    
    # Let's do it step by step with integers to be absolutely sure of the irreducible form
    num_22_part = 9 - 23  # Numerator for denominator 22 part after subtraction inside parens and first term
    
    # Wait, let's re-evaluate: 
    # A + B - (C - D) = A + B - C + D
    # Terms with denom 22: 9/22 - 23/22 -> num = 9-23 = -14. Denom = 22. Simplifies to -7/11.
    # Terms with denom 18: 11/18 + 7/18 -> num = 11+7 = 18. Denom = 18. Simplifies to 1.
    
    # Sum: (-7/11) + 1 = -7/11 + 11/11 = 4/11
    
    correct_num, correct_den = 4, 11
    
    canonical_latex = f"\\frac{{{correct_num}}}{{"{correct_den}"}}"
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "numerator": correct_num,
            "denominator": correct_den,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": {"expression": "9/22 + 11/18 - (23/22 - 7/18)"}
    }