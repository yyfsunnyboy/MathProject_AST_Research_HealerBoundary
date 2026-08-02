from core.prompts.domain_function_library import PolynomialOps

def generate(level=1, **kwargs):
    # 1. Factor the quadratic using exact coefficients provided in frozen_params logic (reconstructed here as needed or passed)
    # The task provides specific coefficients: [39, 5, -14] for 39x^2 + 5x - 14
    coeffs = kwargs.get("quadratic_coefficients", [39, 5, -14])
    
    # We need to factor this. The API `factor_quadratic_exact` takes (a,b,c) from ax^2+bx+c.
    a_quad, b_quad, c_quad = coeffs
    
    factors_raw = PolynomialOps.factor_quadratic_exact(a_quad, b_quad, c_quad)
    
    # 2. Swap so left x_coefficient equals template_left_x_coefficient (which is 3).
    # The API returns a list of two dicts: [{"x_coefficient": ..., "constant": ...}, {"x_coefficient": ..., "constant": ...}]
    # We need to ensure the first factor has x_coefficient == 3.
    
    f1 = factors_raw[0]
    f2 = factors_raw[1]
    
    if f1["x_coefficient"] != 3:
        # Swap them
        f1, f2 = f2, f1
        
    # Now f1 is (3x + a) and f2 is (bx + c) based on the problem statement structure.
    # Problem says: (3x+a)(bx+c). So first factor corresponds to 3x+a.
    
    left_factor_x_coeff = f1["x_coefficient"]
    left_factor_const = f1["constant"]   # This is 'a' in (3x + a)
    right_factor_x_coeff = f2["x_coefficient"] # This is 'b'
    right_factor_const = f2["constant"]        # This is 'c' in (bx + c)
    
    # 3. Extract a, b, c and compute a+2*c with native arithmetic.
    # Note: The API returns ints or strings like "p/q". Since inputs are integers and discriminant check usually yields rational roots,
    # but the problem states a,b,c are integers. Let's assume they come out as exact numbers (int).
    
    val_a = left_factor_const
    val_b = right_factor_x_coeff
    val_c = right_factor_const
    
    result_value = int(val_a) + 2 * int(val_c)
    
    # 4. Assemble correct_answer exactly according to the Answer contract.
    return {
        "question_text": kwargs.get("frozen_description", ""),
        "correct_answer": result_value,
        "oracle_payload": kwargs.get("frozen_params", {})
    }