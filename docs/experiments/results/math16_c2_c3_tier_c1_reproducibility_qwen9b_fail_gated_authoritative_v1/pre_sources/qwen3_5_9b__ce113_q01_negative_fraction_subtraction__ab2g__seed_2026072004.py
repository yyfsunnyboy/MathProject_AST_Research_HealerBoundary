def generate(level=1, **kwargs):
    expression = kwargs.get("expression", "3/7 - (-1/4)")
    
    # Parse components from the specific expression string provided in frozen parameters
    term1_num = 3
    term1_den = 7
    
    term2_str = "-(-1/4)"
    # Extract inner fraction for second term: -1/4
    inner_term2_num = -1
    inner_term2_den = 4
    
    # Operation is subtraction of the second term from the first
    # Expression logic: A/B - (C/D) where C/D is negative, so it becomes addition.
    # Mathematically: 3/7 - (-1/4) = 3/7 + 1/4
    
    numerator_a = term1_num * inner_term2_den
    denominator_b = term1_den * inner_term2_den
    numerator_c = term1_den * inner_term2_num
    
    # Calculate combined numerator and common denominator for subtraction logic: A/B - C/D
    final_numerator = (term1_num * inner_term2_den) + (-inner_term2_num * term1_den) 
    # Wait, let's re-evaluate strictly based on the expression "3/7 - (-1/4)"
    # This is equivalent to 3/7 + 1/4.
    
    n1 = 3
    d1 = 7
    
    n2_inner = -1
    d2_inner = 4
    
    # Operation: (n1/d1) - (n2_inner/d2_inner)
    common_denominator = d1 * d2_inner
    final_numerator = (n1 * d2_inner) - (n2_inner * d1)
    
    gcd_val = abs(final_numerator if final_numerator != 0 else common_denominator) # Avoid div by zero, though unlikely here
    
    def compute_gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    actual_gcd = compute_gcd(abs(final_numerator), abs(common_denominator)) if final_numerator != 0 else common_denominator
    
    simplified_numerator = final_numerator // actual_gcd
    simplified_denominator = common_denominator // actual_gcd
    
    # Ensure canonical form (denominator positive)
    if simplified_denominator < 0:
        simplified_numerator *= -1
        simplified_denominator *= -1
        
    correct_answer_str = f"{simplified_numerator}/{simplified_denominator}"
    
    return {
        "question_text": r"Compute the result of $\frac{3}{7} - \left(-\frac{1}{4}\right)$.",
        "correct_answer": {
            "numerator": simplified_numerator,
            "denominator": simplified_denominator,
            "canonical_latex": f"${simplified_numerator}/{simplified_denominator}$"
        },
        "oracle_payload": {"expression": "3/7 - (-1/4)"}
    }