from core.prompts.domain_function_library import PolynomialOps

def generate(level=1, **kwargs):
    # 1. Initialize frozen_params from task description (oracle_payload must equal this object)
    oracle_payload = {
        "factor_order_policy": "strict_source_template",
        "quadratic_coefficients": [39, 5, -14],
        "template_left_x_coefficient": 3
    }

    # 2. Factor the quadratic polynomial using exact coefficients
    a_fact, b_fact = PolynomialOps.factor_quadratic_exact(39, 5, -14)
    
    # The API returns two dicts: {"x_coefficient", "constant"} for each factor.
    # We need to identify which one matches the template requirement (left x-coeff == 3).
    
    f1 = a_fact[0] if isinstance(a_fact, list) else a_fact
    f2 = b_fact[0] if isinstance(b_fact, list) else b_fact
    
    # Handle potential single dict return or tuple/list depending on implementation nuance.
    # Based on docstring: returns list of dicts. Let's assume standard behavior for two factors.
    # Re-evaluating API signature in docs: `returns: list[dict, dict]` implies a list containing 2 dicts? 
    # Or just the objects themselves? The example shows `list[dict, dict]`. 
    # Usually Python lists contain items of same type. Let's assume it returns [d1, d2].
    
    factors = PolynomialOps.factor_quadratic_exact(39, 5, -14)
    
    # Ensure we have a list of two dictionaries representing the linear factors (x + c/a_x_part?) 
    # Actually factor_quadratic usually returns roots or coefficients. 
    # Docstring: `returns: list[dict, dict]` with keys x_coefficient, constant.
    # Example input: 1*x^2 -5x +6 -> (x-3)(x-2). Factors would be {x_coefficient:1, constant:-3}, {x_coefficient:1, constant:-2}.
    
    if not isinstance(factors, list):
        factors = [factors] # Fallback if single item returned unexpectedly
    
    while len(factors) < 2:
         # If the API behaves differently than expected in this specific environment simulation, 
         # we might need to handle edge cases. But assuming standard behavior for quadratic factorization into two linear terms.
         pass

    d1 = factors[0] if isinstance(factors, list) else (factors.get("x_coefficient") is not None and factors or {})
    d2 = factors[1] if len(factors) > 1 else {} 
    
    # Let's robustly extract the two factor dicts. 
    # If `factor_quadratic_exact` returns a tuple of lists/dicts, we handle that.
    # Re-reading docstring: "returns: list[dict, dict]" -> This is likely Pseudo-code for List[Dict].
    
    if isinstance(factors, (list, tuple)):
        factor_list = factors
    else:
        # Fallback logic just in case the API returns something unexpected like a single object or needs unpacking differently.
        # Given constraints, we assume standard list return of 2 dicts.
        raise ValueError("Unexpected output from PolynomialOps.factor_quadratic_exact")

    d1 = factor_list[0] if isinstance(factor_list, (list, tuple)) else {}
    
    # Correct extraction logic based on typical Python API patterns for this domain:
    # It returns a list of two dicts.
    f_a = factors[0] if len(factors) > 0 else None
    f_b = factors[1] if len(factors) > 1 else None
    
    # Identify the factor where x_coefficient is equal to template_left_x_coefficient (3).
    target_factor = None
    other_factor = None
    
    for i in range(len([f_a, f_b])):
        curr = [f_a, f_b][i] if len([f_a, f_b]) == 2 else ([None])[0] # Simplified loop logic
        
    # Let's restart the extraction cleanly.
    raw_factors = PolynomialOps.factor_quadratic_exact(39, 5, -14)
    
    # Assuming `raw_factors` is a list of two dicts based on "list[dict, dict]" description interpretation as List[Dict].
    if not isinstance(raw_factors, list):
        raw_factors = [raw_factors] 
    while len(raw_factors) < 2:
         # If the API returns fewer than expected due to monic assumption or similar, we might need adjustment.
         # But for non-monic (39x^2), it must return two factors with x-coeffs multiplying to 39.
         pass

    f1 = raw_factors[0] if len(raw_factors) > 0 else None
    f2 = raw_factors[1] if len(raw_factors) > 1 else None
    
    # Filter out any potential empty/None entries if the API behaves oddly, though unlikely for valid input.
    factors_list = [f for f in (raw_factors,) + ([],)[len(raw_factors)==0]] 
    # Simpler: just use raw_factors directly assuming it's a list of 2 items.
    
    candidates = []
    if isinstance(raw_factors, list):
        candidates = raw_factors[:2] # Ensure we take exactly two
    
    left_factor = None
    right_factor = None
    
    for f in candidates:
        x_coeff = f.get("x_coefficient")
        const_val = f.get("constant")
        
        if isinstance(x_coeff, int) and x_coeff == 3:
            # This is the one we want on the left.
            pass
        
    # Re-evaluating logic to be absolutely sure about assignment order matching "strict_source_template".
    # We need (3x + a). So x_coefficient must be 3.
    
    found_left = None
    found_right = None
    
    for f in candidates:
        if isinstance(f, dict):
            xc = f.get("x_coefficient")
            c_val = f.get("constant")
            
            # Check types to ensure we are dealing with integers as per problem statement "a,b,c 均為整數"
            # The API returns int or 'p/q'. Here inputs are ints, so outputs should be ints.
            
            if xc == 3:
                found_left = f
            else:
                found_right = f
                
    # If strict_source_template requires specific ordering and we didn't find exactly one with x=3 (unlikely for this problem), 
    # there might be an issue. But mathematically, factors of 39x^2+5x-14 are likely (3x+a)(13x+c).
    
    if found_left is None:
        # Fallback or error handling? In a real scenario this shouldn't happen for valid inputs.
        # Perhaps the API returns them in arbitrary order and we must sort/swap manually.
        pass
        
    left = found_left
    right = found_right
    
    # Extract parameters based on (3x + a)(bx + c) format implied by "left x_coefficient equals 3"
    # Left factor: 3*x + a -> coefficient of x is 3, constant term is 'a'.
    # Right factor: b*x + c -> coefficient of x is 'b', constant term is 'c'.
    
    if left and right:
        val_a = left.get("constant")
        val_b = right.get("x_coefficient")
        val_c = right.get("constant")
        
        # Compute result a + 2*c
        # Ensure arithmetic compatibility (integers)
        res_val = int(val_a) + 2 * int(val_c)
    else:
        raise ValueError("Could not identify factors matching template.")

    return {
        "question_text": "已知\\n[39x^2+5x-14=(3x+a)(bx+c),]\\n其中 \\(a,b,c\\) 均為整數，求 \\(a+2c\\)。",
        "correct_answer": res_val,
        "oracle_payload": oracle_payload
    }