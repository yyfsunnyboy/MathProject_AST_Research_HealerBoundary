def generate(level=1, **kwargs):
    import random
    
    # Frozen sampled parameters from task specification
    frozen_params = {"expression": "3/7 - (-1/4)"}
    
    def simplify_fraction(numerator, denominator):
        if denominator == 0:
            return numerator, denominator
        
        common_divisor = abs(gcd_func(abs(numerator), abs(denominator)))
        
        simplified_numerator = (numerator // common_divisor) * (-1 if denominator < 0 else 1)
        simplified_denominator = abs(denominator) // common_divisor
        
        return simplified_numerator, simplified_denominator

    def gcd_func(a, b):
        while b:
            a, b = b, a % b
        return a
    
    # Parse the frozen expression to extract components for validation and generation logic
    expr_str = frozen_params["expression"]
    
    # The task is specifically about negative fraction subtraction with this fixed example.
    # We will construct the question text based on the specific frozen parameters provided.
    # Expression: 3/7 - (-1/4)
    
    numerator_a, denominator_a = 3, 7
    sign_b = -1 if "-" in expr_str.split("-")[-1] else 1 
    # Actually parsing "(-1/4)" implies the second term is negative.
    # Let's strictly follow the frozen string to build the text.
    
    question_text = r"Compute the result of $3/7 - \left(-\frac{1}{4}\right)$."
    
    # Calculate correct answer for 3/7 - (-1/4) which is 3/7 + 1/4
    num_a, den_a = numerator_a, denominator_a
    num_b, den_b = -1, 4
    
    common_denom = abs(den_a * den_b // gcd_func(abs(den_a), abs(den_b))) # Simplified logic for specific case: lcm(7,4)=28
    # LCM of 7 and 4 is 28.
    
    term1_num = num_a * (common_denom // den_a)
    term2_num = num_b * (common_denom // den_b)
    
    final_numerator = term1_num + term2_num
    final_denominator = common_denom
    
    # Simplify result
    gcd_res = abs(gcd_func(final_numerator, final_denominator))
    canonical_numerator = final_numerator // gcd_res
    canonical_denominator = final_denominator // gcd_res
    
    if canonical_denominator < 0:
        canonical_numerator *= -1
        canonical_denominator *= -1
        
    correct_answer_dict = {
        "numerator": canonical_numerator,
        "denominator": canonical_denominator,
        "canonical_latex": f"\\frac{{{canonical_numerator}}}{{{{{canonical_denominator}}}}}" if abs(canonical_numerator) != 0 else "\\text{undefined}", # Handle zero case though unlikely here
    }
    
    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer_dict,
        "oracle_payload": oracle_payload
    }