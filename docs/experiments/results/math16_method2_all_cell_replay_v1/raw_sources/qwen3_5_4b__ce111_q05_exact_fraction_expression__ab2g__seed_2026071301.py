def generate(level=1, **kwargs):
    question_text = r"\text{Simplify the expression: } \frac{9}{22} + \frac{11}{18} - \left( \frac{23}{22} - \frac{7}{18} \right)"
    
    # Calculate the correct answer manually to ensure irreducibility and correctness
    # Expression: 9/22 + 11/18 - (23/22 - 7/18)
    # Combine terms with common denominators where possible or use LCM(22, 18) = 198
    
    term1_num = 9 * 9   # 9/22 -> 81/198 (since 198/22=9)
    term1_den = 198
    
    term2_num = 11 * 11 # 11/18 -> 121/198 (since 198/18=11)
    term2_den = 198
    
    inner_parenthesis_term3_num = 23 * 9   # 23/22 -> 207/198
    inner_parenthesis_term4_num = -7 * 9   # -7/18 -> -63/198 (note the negative sign from subtraction)
    
    # Let's re-calculate carefully: A + B - (C - D) = A + B - C + D
    
    a = 9 / 22
    b = 11 / 18
    c = 23 / 22
    d = 7 / 18
    
    result_val = a + b - (c - d)
    
    # Convert to fraction using math.fraction for precision and irreducibility check
    from fractions import Fraction
    frac_result = Fraction(result_val).limit_denominator()
    
    numerator = frac_result.numerator
    denominator = frac_result.denominator
    
    canonical_latex = f"\\frac{{{numerator}}}{{denominator}}" if isinstance(denominator, int) else str(frac_result)
    
    # Ensure the latex string format matches requirements (irreducible fraction representation)
    correct_answer_dict = {
        "numerator": numerator,
        "denominator": denominator,
        "canonical_latex": f"\\frac{{{numerator}}}{{denominator}}"
    }
    
    oracle_payload = {"expression": "9/22 + 11/18 - (23/22 - 7/18)"}
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer_dict,
        "oracle_payload": oracle_payload
    }