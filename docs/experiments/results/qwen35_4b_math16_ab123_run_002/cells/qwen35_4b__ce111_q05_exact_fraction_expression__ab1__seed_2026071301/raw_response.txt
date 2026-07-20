def generate(level=1, **kwargs):
    question_text = r"\text{Evaluate the exact fractional expression: } \frac{9}{22} + \frac{11}{18} - \left( \frac{23}{22} - \frac{7}{18} \right)"
    
    # Manual calculation to ensure correctness without external libraries
    term1_num, term1_den = 9, 22
    term2_num, term2_den = 11, 18
    
    # Parentheses part: (23/22 - 7/18)
    p_term1_num, p_term1_den = 23, 22
    p_term2_num, p_term2_den = 7, 18
    common_p = lcm(22, 18) # LCM of 22 and 18 is 198
    p_sum_num = (p_term1_num * (common_p // p_term1_den)) + (-p_term2_num * (common_p // p_term2_den))
    
    term3_num, term3_den = p_sum_num, common_p
    
    # Total: term1 + term2 - term3
    total_common_lcm = lcm(lcm(term1_den, term2_den), term3_den)
    final_num = (term1_num * (total_common_lcm // term1_den)) + \
                (term2_num * (total_common_lcm // term2_den)) + \
                (-term3_num * (total_common_lcm // term3_den))
    
    # Reduce fraction by GCD
    common_divisor = gcd(final_num, total_common_lcm)
    reduced_num = final_num // common_divisor
    reduced_den = total_common_lcm // common_divisor
    
    correct_answer = {
        "numerator": str(reduced_num),
        "denominator": str(reduced_den),
        "canonical_latex": f"\\frac{{{reduced_num}}}{{{reduced_den}}}"
    }
    
    oracle_payload = {"expression": "9/22 + 11/18 - (23/22 - 7/18)"}

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }