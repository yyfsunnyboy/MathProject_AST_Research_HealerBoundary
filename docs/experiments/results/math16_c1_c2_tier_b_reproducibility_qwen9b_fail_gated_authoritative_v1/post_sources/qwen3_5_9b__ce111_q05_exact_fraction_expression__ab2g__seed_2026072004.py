def generate(level=1, **kwargs):
    expression = "9/22 + 11/18 - (23/22 - 7/18)"
    
    # Calculate numerator: 9*18 + 11*22 - (23*18 - 7*22)
    term1_num = 9 * 18
    term2_num = 11 * 22
    inner_parenthesis_term1_num = 23 * 18
    inner_parenthesis_term2_num = 7 * 22
    
    numerator = (term1_num + term2_num) - (inner_parenthesis_term1_num - inner_parenthesis_term2_num)
    
    # Calculate denominator: LCM of denominators is not needed for the whole expression directly, 
    # but we can compute common denominator step by step or use product.
    # Common denom for 9/22 and 11/18 (denoms 22=2*11, 18=2*3^2) -> LCM = 2*3^2*11 = 198
    term1_denom = 198 // 22 * 18 # Wait, simpler: just use the common denominator of all terms.
    
    # Let's re-calculate using a single common denominator for clarity in logic check, 
    # though the previous numerator calculation assumed a specific path.
    # Path used above: (9/22 + 11/18) - (23/22 - 7/18)
    # = ((9*9)/(22*9)) ... no, let's stick to LCM(22, 18) = 198.
    
    term1_val_num = 9 * (198 // 22)
    term2_val_num = 11 * (198 // 18)
    inner_term1_val_num = 23 * (198 // 22)
    inner_term2_val_num = 7 * (198 // 18)
    
    total_numerator = term1_val_num + term2_val_num - (inner_term1_val_num - inner_term2_val_num)
    denominator_common = 198
    
    # Simplify fraction
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return abs(a)
    
    common_divisor = gcd(total_numerator, denominator_common)
    simplified_num = total_numerator // common_divisor
    simplified_denom = denominator_common // common_divisor
    
    # Ensure canonical form (denominator positive)
    if simplified_denom < 0:
        simplified_num *= -1
        simplified_denom *= -1
        
    correct_answer_dict = {
        "numerator": simplified_num,
        "denominator": simplified_denom,
        "canonical_latex": f"\\frac{{{simplified_num}}}{{{simplified_denom}}}"
    }
    
    return {
        "question_text": r"Simplify the expression: $9/22 + 11/18 - (23/22 - 7/18)$",
        "correct_answer": correct_answer_dict,
        "oracle_payload": {"expression": "9/22 + 11/18 - (23/22 - 7/18)"}
    }