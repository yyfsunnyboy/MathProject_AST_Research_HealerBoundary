def generate(level=1, **kwargs):
    assert level == 1
    
    frozen_params = {
        "factor_order_policy": "strict_source_template", 
        "quadratic_coefficients": [39, 5, -14], 
        "template_left_x_coefficient": 3
    }
    
    # Derive 'a' from the quadratic factor's rational root.
    # Quadratic: 39x^2 + 5x - 14. Discriminant D = 25 - 4*39*(-14) = 2209 = 47^2.
    # Roots x = (-5 +/- 47)/78 -> One root is (42/78)? No, signs: 
    # Root 1: (-5+47)/78 = 42/78 = -6/13? Wait, 42/-78? No.
    # Correct calculation: x = [-b +/- sqrt(D)] / (2a) where a=39, b=5.
    # Root 1: (-5 + 47)/78 = 42/78 = -6/13? No, positive/negative doesn't matter for sign of root if denominator is fixed. 
    # Wait, standard formula: x = [-b +/- sqrt(D)] / (2a).
    # Root 1: (-5 + 47)/78 = 42/78 = -6/13? No, 42/78 simplifies to 7/13. Positive root? 
    # If x=7/13, then factor is (x-7/13) or (13x-7). Not matching (3x+a).
    # Root 2: (-5 - 47)/78 = -52/78 = -2/3. Factor is (x+2/3) -> 3x+2. 
    # So a=2 matches factor (3x+2).
    
    from fractions import Fraction as F
    
    a_val = 2
    c_val = frozen_params["quadratic_coefficients"][1]
    
    correct_answer_int = a_val + 2 * c_val
    
    return {
        "question_text": r"\text{Consider the polynomial } P(x) \text{ that factors as } (3x+a)(bx^2+cx+d). \\ 
                     \text{Given frozen parameters, one root of the quadratic factor is rational. Find integer } a \text{ and compute } a+2c.",
        "correct_answer": correct_answer_int,
        "oracle_payload": frozen_params.copy()
    }
