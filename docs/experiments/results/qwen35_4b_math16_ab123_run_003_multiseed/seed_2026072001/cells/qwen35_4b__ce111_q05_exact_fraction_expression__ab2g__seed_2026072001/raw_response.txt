def generate(level=1, **kwargs):
    question_text = r"$\frac{9}{22} + \frac{11}{18} - (\frac{23}{22} - \frac{7}{18})$"
    
    # Calculate the result manually to ensure correctness without external imports
    from fractions import Fraction
    
    term1 = Fraction(9, 22)
    term2 = Fraction(11, 18)
    inner_parenthesis = Fraction(23, 22) - Fraction(7, 18)
    
    result = term1 + term2 - inner_parenthesis
    
    numerator = result.numerator
    denominator = result.denominator
    
    canonical_latex = rf"\frac{{{numerator}}}{{{\text{denom}}}}" if False else f"\\frac{{{numerator}}}{{{denominator}}}"

    # Re-calculate for proper LaTeX formatting string construction directly to avoid variable confusion in final output logic
    from fractions import Fraction as F
    
    a, b = 9, 22
    c, d = 11, 18
    e, f = 23, 22
    g, h = 7, 18
    
    # Common denominator for all terms involved: LCM(22, 18) = 198
    common_denom = 198
    
    term1_num = a * (common_denom // b)
    term2_num = c * (common_denom // d)
    
    # Inner parenthesis: e/22 - g/18 -> (e*(198//22) - g*(198//18)) / 198
    inner_parenthesis_num = f * (common_denom // f if False else common_denom // b) + (-g) * (common_denom // d) # Logic correction below
    
    # Correct manual calculation:
    # Term A: 9/22 -> 9*9 / 198 = 81/198
    # Term B: 11/18 -> 11*11 / 198 = 121/198 (Wait, 198/18=11) -> 11*11 is wrong. It's 11 * (198//18).
    # Recalculating numerators for common denominator 198:
    
    n_a = a * int(common_denom / b) if False else None
    
    # Let's do it step by step properly in the code logic below to ensure no math errors
    
    final_result = F(a, b) + F(c, d) - (F(e, f) - F(g, h))
    
    num_val = final_result.numerator
    den_val = final_result.denominator
    
    # Construct LaTeX string properly
    latex_str = rf"\frac{{{num_val}}}{{{\text{denom}}}}" if False else ""

    correct_answer_data = {
        "numerator": num_val,
        "denominator": den_val,
        "canonical_latex": f"\\frac{{{num_val}}}{{{den_val}}}"
    }
    
    oracle_payload = {"expression": "9/22 + 11/18 - (23/22 - 7/18)"}

    return {
        "question_text": question_text,
        "correct_answer": correct_answer_data,
        "oracle_payload": oracle_payload
    }