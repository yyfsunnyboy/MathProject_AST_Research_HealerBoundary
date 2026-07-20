def generate(level=1, **kwargs):
    question_text = r"Calculate the exact fraction resulting from: $\frac{9}{22} + \frac{11}{18} - (\frac{23}{22} - \frac{7}{18})$."
    
    # Manual calculation to ensure correctness
    term1_num, term1_den = 9, 22
    term2_num, term2_den = 11, 18
    
    inner_parenthesis:
        p_inner_1, q_inner_1 = 23, 22
        p_inner_2, q_inner_2 = 7, 18
        
        # LCM of 22 and 18 is 198
        lcm_inner = (q_inner_1 * q_inner_2) // math.gcd(q_inner_1, q_inner_2)
        
        p_inner_adj_1 = p_inner_1 * (lcm_inner // q_inner_1)
        p_inner_adj_2 = p_inner_2 * (lcm_inner // q_inner_2)
        
        inner_result_num = p_inner_adj_1 - p_inner_adj_2
        inner_result_den = lcm_inner
    
    # LCM of 22 and 18 is 198. Term1 has denom 22, Term3 has denom 198.
    lcm_total = (term1_den * term3_den) // math.gcd(term1_den, term3_den)
    
    t1_adj_num = term1_num * (lcm_total // term1_den)
    t3_adj_num = inner_result_num * (lcm_total // inner_result_den) # Note: subtraction
    
    final_num = t1_adj_num - t3_adj_num
    final_den = lcm_total
    
    common_divisor = math.gcd(final_num, final_den)
    
    correct_answer_numerator = final_num // common_divisor
    correct_answer_denominator = final_den // common_divisor

return {
    "question_text": question_text, 
    "correct_answer": {
        "numerator": correct_answer_numerator, 
        "denominator": correct_answer_denominator, 
        "canonical_latex": f"${\\frac{{correct\_answer\_numerator}}{{correct\_answer\_denominator}}}$"
    }, 
    "oracle_payload": {"expression": "9/22 + 11/18 - (23/22 - 7/18)"}
}