from core.prompts.domain_function_library import FractionOps, Fraction

def generate(level=1, **kwargs):
    # Parse the frozen parameters to construct fractions from decimal strings
    products = kwargs.get("oracle_payload", {}).get("products")
    
    term1_left_str = products[0]["left"]   # "2.79"
    term1_right_str = products[0]["right"] # "89.3"
    sign1 = products[0]["sign"]            # 1
    
    term2_left_str = products[1]["left"]   # "-0.21" (includes the negative sign in string)
    term2_right_str = products[1]["right"] # "89.3"
    sign2 = products[1]["sign"]            # -1

    def parse_decimal(s):
        """Convert a decimal string to an irreducible Fraction."""
        if '.' not in s:
            return FractionOps.from_parts(int(s), 1)
        
        integer_part, fractional_part = s.split('.')
        numerator_str = integer_part + fractional_part
        denominator = 10 ** len(fractional_part)
        
        # Handle negative numbers correctly by parsing the sign separately if needed, 
        # but here we assume the string contains the full value including '-' at start.
        val_float = float(s)
        return FractionOps.from_parts(int(numerator_str), denominator)

    f1_left = parse_decimal(term1_left_str)
    f2_right = parse_decimal(term2_right_str)
    
    # Calculate term 1: left * right
    prod1 = FractionOps.mul(f1_left, f2_right)
    
    # Parse the second term's left operand. The string "-0.21" is passed directly.
    f2_left_raw = parse_decimal(term2_left_str) 
    
    # Calculate term 2: left * right (ignoring sign for a moment to apply later or via subtraction logic)
    prod2_base = FractionOps.mul(f2_left_raw, f2_right)
    
    # The expression is: (term1) - (-0.21 * 89.3) ? 
    # Wait, the frozen params say sign for second product is -1.
    # Usually this implies we compute value = term1 + (sign2 * prod2_base).
    # Let's re-read standard interpretation of such lists: sum(sign_i * prod_i).
    
    final_value = FractionOps.add(prod1, FractionOps.mul(FractionOps.from_parts(1, 1), sign2)) \
        if isinstance(sign2, int) else None
    
    # Correction based on typical math problem generation logic with 'sign' field:
    # We compute the product of magnitudes then apply signs. 
    # However, parse_decimal("-0.21") already includes the negative value (-21/100).
    # If we multiply -21/100 * 893/10, we get a negative number.
    # The 'sign' field in frozen_params might be redundant if parsed from string, 
    # OR it indicates an explicit multiplier separate from the string value (e.g., "left" is magnitude).
    
    # Let's check consistency: 
    # If left="-0.21", float("-0.21") = -0.21. 
    # If sign=-1, maybe we should multiply by -1 again? That would make it positive 0.21 * 89.3.
    # But the text says "(-0.21 x 89.3)". This is a negative product inside parentheses.
    # Then subtracting that: A - (B) where B = (-0.21)*C. 
    # So result = A + |B|.
    
    # Let's assume the 'sign' field in frozen_params overrides or clarifies the intended operation 
    # relative to a positive magnitude if "left" was meant as magnitude, OR it confirms direction.
    # Given "left": "-0.21", let's trust the string value for parsing first.
    
    # Re-evaluating based on strict instruction: "oracle_payload must equal this object".
    # The task is to calculate 2.79*89.3 - (-0.21*89.3).
    # Term 1 = 2.79 * 89.3 (Positive)
    # Term 2 part inside bracket: -0.21 * 89.3 (Negative result)
    # Operation: Subtract the negative term -> Add absolute value.
    
    # Let's parse strictly from strings to get exact fractions.
    def str_to_frac(s):
        if '.' in s:
            int_part, frac_part = s.split('.')
            num_str = int_part + frac_part
            den = 10 ** len(frac_part)
            return FractionOps.from_parts(int(num_str), den)
        else:
            return FractionOps.from_parts(int(s), 1)

    val_a = str_to_frac(term1_left_str) # 2.79 -> 279/100
    val_b = str_to_frac(term1_right_str)# 89.3 -> 893/10
    
    term_1_res = FractionOps.mul(val_a, val_b)

    val_c = str_to_frac(term2_left_str) # -0.21 -> -21/100
    val_d = str_to_frac(term2_right_str)# 89.3 -> 893/10
    
    term_2_res_inside_paren = FractionOps.mul(val_c, val_d)

    # The expression is: Term1 - (Term2_inside)
    final_result = FractionOps.sub(term_1_res, term_2_res_inside_paren)

    # Prepare output according to contract
    return {
        "question_text": kwargs.get("frozen_description", ""), 
        "correct_answer": {
            "value": str(FractionOps.to_exact(final_result)),
            "canonical_latex": FractionOps.to_latex(final_result, mixed=False)
        },
        "oracle_payload": products
    }