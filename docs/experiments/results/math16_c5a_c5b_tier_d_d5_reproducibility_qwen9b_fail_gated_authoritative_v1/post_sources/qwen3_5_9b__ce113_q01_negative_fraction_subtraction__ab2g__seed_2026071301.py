def generate(level=1, **kwargs):
    expression = kwargs.get("expression", "3/7 - (-1/4)")
    
    # Parse components from the fixed expression string provided in frozen parameters
    term1_num, term1_den = 3, 7
    sign2_str = "-(-1"
    if "-" not in sign2_str:
        # Handle case where negative is explicit like - (-1/4) vs + (1/4) logic implicitly handled by math
        pass
    
    # Logic to compute the result of expression "3/7 - (-1/4)" which equals 3/7 + 1/4
    num1, den1 = term1_num, term1_den
    sign2_str_val = "-(-1" in expression and True or False
    
    if "-" in expression:
        # It is subtraction of a negative fraction -> addition
        op_sign = -1 * (-1)  # effectively +1 for the second numerator magnitude relative to original string representation logic, but let's compute directly from values derived from "3/7" and "-(-1/4)"
    else:
        pass

    # Direct computation based on frozen parameters {"expression": "3/7 - (-1/4)"}
    n1 = 3
    d1 = 7
    
    # The second term is explicitly negative of a positive fraction in the string "-(-1/4)"? 
    # Actually standard interpretation: A/B - (C/D). Here C=-1, D=4. So -( (-1)/4 ) = +1/4.
    n2_raw = 1
    d2 = 4
    
    common_denominator = den1 * d2 // gcd(den1, d2) if False else den1 * d2 # Simplified logic below for correctness without external imports in strict env usually implies math.gcd exists or manual impl. Assuming standard lib available.
    
    import math

    def compute_result():
        n1 = 3
        d1 = 7
        
        # The expression is "3/7 - (-1/4)"
        # This simplifies to: (3 * 4) / 28 + (1 * 7) / 28
        numerator = (n1 * d2_raw) + (abs(-1) * d1) 
        denominator = d1 * d2_raw
        
        return numerator, denominator

    # Re-evaluating strictly based on string "3/7 - (-1/4)"
    # Term 1: 3/7. Term 2 inside parens is -1/4. Operation is minus Term 2.
    # Result = (3 * 4) + ((-(-1)) * 7) all over (7*4)? 
    # Wait, standard math parsing of "A/B - (-C/D)" where C=1, D=4:
    # Value = A/B - (-C/D) = A/B + C/D.
    
    n_a = 3; d_a = 7
    n_b = -1; d_b = 4
    
    common_denom = math.gcd(d_a, abs(d_b)) * (d_a // math.gcd(d_a, abs(d_b))) * (abs(d_b) // math.gcd(d_a, abs(d_b))) # No, just product divided by gcd
    g = math.gcd(abs(d_a), abs(d_b))
    lcm_denom = (d_a * d_b) // g
    
    term1_scaled_num = n_a * (lcm_denom // d_a)
    term2_value = -n_b # Because we subtract the fraction (-1/4). Subtracting a negative is adding. 
                      # Wait, expression is "3/7" MINUS "(-1/4)".
                      # So it's 3/7 + 1/4.
    
    val_numerator_2 = -n_b * (lcm_denom // d_b) # This handles the sign of n_b correctly if we just add them? 
    # Let's do pure arithmetic: x/y - z/w = (xw - zy)/yw
    # Here z = -1, w = 4.
    # Numerator = 3*4 - (-1)*7 = 12 + 7 = 19. Denominator = 28.
    
    num_result = n_a * d_b - (n_b) * d_a
    den_result = d_a * d_b
    
    g_res = math.gcd(abs(num_result), abs(den_result))
    final_num = num_result // g_res
    final_den = den_result // g_res
    
    # Construct canonical LaTeX for irreducible fraction: \frac{num}{den}
    if final_den == 1:
        latex_frac = str(final_num)
    else:
        latex_frac = f"\\frac{{{final_num}}}{{{final_den}}}"

    return {
        "question_text": r"The value of the expression $3/7 - (-1/4)$ is equal to \_\_.",
        "correct_answer": {
            "numerator": final_num,
            "denominator": final_den,
            "canonical_latex": latex_frac
        },
        "oracle_payload": {"expression": "3/7 - (-1/4)"}
    }