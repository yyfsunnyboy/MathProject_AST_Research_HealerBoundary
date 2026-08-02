def generate(level=1, **kwargs):
    # 1) factor_quadratic_exact using coefficients [39, 5, -14] for 39x^2 + 5x - 14
    factors = PolynomialOps.factor_quadratic_exact(39, 5, -14)

    # The API returns a list of two dicts. We need to match the template constraint:
    # "first factor fixed as (3x+a)". This means the first dict in our result must have x_coefficient == 3.
    
    left_factor = None
    right_factor = None
    
    for f in factors:
        if f["x_coefficient"] == 3:
            left_factor = f
        else:
            right_factor = f
            
    # If the API returned them in a different order, we swap to satisfy strict_source_template.
    # The contract says "first factor fixed as (3x+a)". So list[0] must be the one with x_coeff=3.
    
    if left_factor is None or right_factor is None:
        raise ValueError("Factorization failed to produce integer factors matching template.")

    # Ensure order matches strict_source_template requirement for 'correct_answer' calculation logic context,
    though the final answer a+2c depends on identifying which variable corresponds to what.
    
    # Re-assign based on content check if necessary (though loop above handles it)
    result_factors = [left_factor, right_factor]

    # Extract parameters from the factors: (3x + a)(bx + c)
    # left_factor is (3x + a), so x_coefficient=3, constant=a.
    # right_factor is (bx + c).
    
    a_val = result_factors[0]["constant"]  # This is 'a' in (3x+a)
    b_val = result_factors[1]["x_coefficient"]  # This is 'b'
    c_val = result_factors[1]["constant"]      # This is 'c'

    # Compute a + 2*c using native arithmetic
    final_answer = a_val + 2 * c_val
    
    return {
        "question_text": r"已知\[39x^2+5x-14=(3x+a)(bx+c),其中 \(a,b,c\) 均為整數，求 \(a+2c\。",
        "correct_answer": final_answer,
        "oracle_payload": {
            "factor_order_policy": "strict_source_template",
            "quadratic_coefficients": [39, 5, -14],
            "template_left_x_coefficient": 3
        }
    }