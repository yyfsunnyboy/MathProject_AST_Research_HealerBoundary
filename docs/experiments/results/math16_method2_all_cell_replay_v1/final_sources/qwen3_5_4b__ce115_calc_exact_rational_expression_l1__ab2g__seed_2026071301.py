def generate(level=1, **kwargs):
    import fractions
    
    # Frozen sampled parameters as per specification
    frozen_params = {
        "products": [
            {"left": "2.79", "right": "89.3", "sign": 1},
            {"left": "-0.21", "right": "89.3", "sign": -1}
        ]
    }

    # Parse the first product: left = 2.79, right = 89.3, sign = +1
    p1_str = str(frozen_params["products"][0]["left"])
    q1_num, p1_denom = fractions.Fraction(p1_str).numerator, fractions.Fraction(p1_str).denominator
    
    r1_str = str(frozen_params["products"][0]["right"])
    q2_num, p2_denom = fractions.Fraction(r1_str).numerator, fractions.Fraction(r1_str).denom

    # Calculate the first term: 2.79 * 89.3
    term1_numerator = q1_num * q2_num
    term1_denominator = p1_denom * p2_denom
    
    # Parse the second product: left = -0.21, right = 89.3, sign = -1
    p3_str = str(frozen_params["products"][1]["left"])
    q3_num, p3_denom = fractions.Fraction(p3_str).numerator, fractions.Fraction(p3_str).denominator
    
    r2_str = str(frozen_params["products"][1]["right"])
    q4_num, p4_denom = fractions.Fraction(r2_str).numerator, fractions.Fraction(r2_str).denom

    # Calculate the second term: -0.21 * 89.3 (with sign applied)
    # The expression is effectively: (2.79 * 89.3) + (-(-0.21 * 89.3)) 
    # Wait, looking at standard rational arithmetic problems of this type:
    # Usually it's a sum or difference of products. Given the "sign" field in params often indicates operation direction relative to subtraction.
    # Let's interpret as: Result = (left1 * right1) - (abs(left2) * right2) if sign is negative? 
    # Or simply calculate both and combine based on standard algebraic structure implied by such tasks.
    # A common pattern for "exact rational expression" level 1 with two products is a subtraction: Term1 - Term2 or Term1 + Term2.
    # Given the second product has sign=-1, it likely implies we subtract its magnitude from the first term, 
    # OR we calculate (A * B) and then add/subtract based on signs provided in input strings directly?
    
    # Let's assume the expression is: (2.79 * 89.3) - (-0.21 * 89.3) ? No, that would be addition of negatives.
    # Standard interpretation for such datasets often involves constructing an equation like A*B + C*D or similar.
    # However, the "sign" field suggests a specific operation logic: 
    # Expression = (left_0 * right_0) - |left_1| * right_1 if sign is negative?
    # Let's try to construct: Result = Fraction(2.79)*Fraction(89.3) + (-0.21)*Fraction(89.3). 
    # This simplifies to (2.79 - 0.21) * 89.3? No, the second left is negative already.
    
    # Let's stick to strict arithmetic based on the values provided and signs indicating operation polarity if needed.
    # Most likely: Calculate Term A = 2.79 * 89.3. Calculate Term B = -0.21 * 89.3. 
    # The "sign" field might indicate whether to add or subtract this term from the first? 
    # If sign=+1, we add (or it's positive). If sign=-1, we subtract (or it's negative contribution)?
    # Actually, a very common pattern is: Result = Term1 - |Term2| if signs differ in context.
    # But let's look at the numbers: 2.79 and -0.21. 
    # If we simply compute sum of products as written with their explicit values including sign:
    # (2.79 * 89.3) + (-0.21 * 89.3). This equals (2.79 - 0.21) * 89.3 = 2.58 * 89.3.
    
    term_a_numerator, term_a_denominator = fractions.Fraction(p1_str), fractions.Fraction(r1_str) # Wait, p/q logic above was mixed up in variable names
    
    # Re-calculation cleanly:
    val_0_left = Fraction(frozen_params["products"][0]["left"])
    val_0_right = Fraction(frozen_params["products"][0]["right"])
    
    val_1_left = Fraction(frozen_params["products"][1]["left"])
    val_1_right = Fraction(frozen_params["products"][1]["right"])

    # The expression is likely: (val_0_left * val_0_right) + (val_1_left * val_1_right) 
    # OR (val_0_left * val_0_right) - abs(val_1_left) * val_1_right?
    # Given the "sign" field exists, it probably dictates the operation between the two products.
    # If sign is +1: Add. If sign is -1: Subtract. 
    # But wait, the second product already has a negative left operand (-0.21).
    # Let's assume the task asks for (Product 1) +/- (Product 2 magnitude)?
    # Or simply sum of two terms where one term uses the signed value?
    
    # Hypothesis: The expression is Term1 - |Term2| if sign=-1, else Term1 + |Term2|. 
    # But usually "sign" in these datasets indicates the operation operator between the main components.
    # Let's try: Result = (val_0_left * val_0_right) - abs(val_1_left * val_1_right)? No, that ignores sign=+1 case logic if it was subtraction too? 
    # Actually, looking at similar problems: "sign" often indicates the operation relative to a base.
    # Let's assume the simplest exact arithmetic interpretation of the provided data structure as an expression generator.
    # Expression = (2.79 * 89.3) - (-0.21 * 89.3)? That is addition. 
    # Maybe: Result = (val_0_left * val_0_right) + sign * abs(val_1_left) * val_1_right?
    
    # Let's go with the most robust interpretation for "exact rational":
    # Compute T1 = 2.79 * 89.3
    # Compute T2 magnitude = |-0.21| * 89.3
    # If sign is +1, add? Or maybe the expression is just a sum of two products where one has negative input?
    # Let's calculate both terms and combine them as: (Term1) - |Term2| if we assume "sign" overrides the explicit value? 
    # No, let's treat it as: Result = Term1 + sign * T2_explicit.
    
    term1_numerator = val_0_left.numerator * val_0_right.numerator
    term1_denominator = val_0_left.denominator * val_0_right.denominator
    
    abs_val_1_left = Fraction(abs(val_1_left)) # 0.21
    t2_mag_numerator = abs_val_1_left.numerator * val_1_right.numerator
    t2_mag_denominator = abs_val_1_left.denominator * val_1_right.denom
    
    if frozen_params["products"][1]["sign"] == 1:
        # Add the second term (positive contribution)
        total_numerator = term1_numerator + t2_mag_numerator
        total_denominator = term1_denominator
    else:
        # Subtract the magnitude of the second term? Or add the negative value? 
        # If sign=-1, usually implies subtraction in these templates.
        total_numerator = term1_numerator - t2_mag_numerator
        total_denominator = term1_denom

    # Simplify fraction
    common_divisor = fractions.gcd(total_numerator, total_denominator)
    
    final_p = total_numerator // common_divisor
    final_q = total_denominator // common_divisor
    
    correct_answer_value = f"{final_p}/{final_q}"
    canonical_latex = r"\frac{" + str(final_p) + "}{"} + str(final_q) + r"}"

    question_text = rf"Evaluate the expression: {val_0_left} \\times {val_0_right} \\\\ - {{abs({val_1_left})}} \times {val_1_right}"
    
    # Wait, let's refine the question text to be generic and formal based on inputs.
    q_str = f"Calculate: ({p1_str} * {r1_str}) + sign_{frozen_params['products'][0]['sign']}({abs_val_1_left.numerator}/{abs_val_1_left.denom} * {r2_str})" 
    # Actually, let's just construct a clean LaTeX string.
    
    final_question = r"Evaluate the expression: $ \frac{279}{100} \times \frac{893}{10} - |\frac{-21}{100}| \times \frac{893}{10} $"

    return {
        "question_text": final_question,
        "correct_answer": f"{final_p}/{final_q}",
        "oracle_payload": frozen_params
    }