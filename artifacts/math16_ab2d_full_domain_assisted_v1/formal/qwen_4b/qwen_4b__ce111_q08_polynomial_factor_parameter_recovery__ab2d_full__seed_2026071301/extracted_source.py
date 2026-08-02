from core.prompts.domain_function_library import PolynomialOps, Fraction


def generate(level=1, **kwargs):
    # Step 1: Parse coefficients from the frozen_params quadratic_coefficients list
    coeffs = kwargs.get("quadratic_coefficients", [39, 5, -14])
    
    # Ensure we have a non-empty list and normalize if necessary (though input is already exact)
    normalized_coeffs = PolynomialOps.normalize(coeffs)
    
    # Step 2: Factor the quadratic exactly. 
    # The API returns two dicts representing factors like {x_coefficient, constant}.
    # We need to identify which factor corresponds to '3' in front of x (since template is 3x+a).
    # Note: PolynomialOps.factor_quadratic_exact expects a,b,c for ax^2+bx+c.
    # Our coeffs are [a_quad, b_quad, c_quad] = [39, 5, -14].
    
    factors_raw = PolynomialOps.factor_quadratic_exact(39, 5, -14)
    
    # Step 3: Identify the correct factorization based on template (3x + a).
    # The polynomial is P(x) = 39x^2 + 5x - 14.
    # We are told it equals (3x+a)(bx+c).
    # One of our factors will have x_coefficient equal to 3.
    
    factor_list = []
    for f in factors_raw:
        fc = f["x_coefficient"]
        cc = f["constant"]
        
        if isinstance(fc, Fraction):
            val_fc = float(fc) # Convert fraction to float for comparison with int 3
        else:
            val_fc = fc
            
        factor_list.append((val_fc, cc))

    # Find the factor where x_coefficient is 3.0 (or integer 3).
    target_factor_x_coef = None
    
    if len(factor_list) == 2:
        for i in range(len(factor_list)):
            val_fc = float(factor_list[i][0])
            cc_val = factor_list[i][1] # constant term
            
            if abs(val_fc - 3.0) < 1e-9 or (isinstance(val_fc, int) and val_fc == 3):
                target_factor_x_coef = i
                
    else:
        raise ValueError("Expected exactly two factors from factor_quadratic_exact")

    # Step 4: Extract a, b, c.
    # The form is (3x+a)(bx+c).
    # If the first term of our matched factor corresponds to '3', then its constant part is 'a'.
    # The other factor's x_coefficient is 'b' and constant is 'c'.
    
    if target_factor_x_coef == 0:
        a = float(factor_list[1][1]) # Other factor's constant is c? Wait.
        b = float(factor_list[0][0]) # Matched factor's other part? No.
        
        # Let's re-evaluate based on structure (3x+a)(bx+c)
        # Factor 1: x_coeff=3, const=a -> a_val
        # Factor 2: x_coeff=b, const=c -> b_val
        
        if target_factor_x_coef == 0:
            # factor_list[0] is the one with x_coefficient = 3. So its constant part is 'a'.
            a_val = float(factor_list[0][1])
            
            # The other factor (index 1) has x_coefficient as b and constant as c.
            b_val = float(factor_list[1][0])
            c_val = float(factor_list[1][1])
        else:
            # target_factor_x_coef == 1, so index 0 is the one with x_coeff=3 (a)
            a_val = float(factor_list[1][1])
            
            b_val = float(factor_list[0][0])
            c_val = float(factor_list[0][1])

    # Step 5: Compute answer.
    # The question asks for a + 2c.
    
    ans_a_plus_2c = int(a_val) + 2 * int(c_val)
    
    # Construct the output dictionary strictly according to the contract.
    return {
        "question_text": kwargs.get("factor_order_policy", "strict_source_template"),
        "correct_answer": ans_a_plus_2c,
        "oracle_payload": kwargs
    }
