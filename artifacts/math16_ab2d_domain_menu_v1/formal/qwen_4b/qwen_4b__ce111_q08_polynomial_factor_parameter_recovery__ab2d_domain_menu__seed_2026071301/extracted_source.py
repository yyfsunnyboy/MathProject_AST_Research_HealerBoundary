from core.prompts.domain_function_library import PolynomialOps


def generate(level=1, **kwargs):
    # Extract frozen parameters from kwargs or use defaults if not provided in the context
    # Based on the task description, we assume these are passed via kwargs for this specific call
    
    factor_order_policy = kwargs.get("factor_order_policy", "strict_source_template")
    
    quadratic_coefficients = kwargs.get("quadratic_coefficients", [39, 5, -14])
    template_left_x_coefficient = kwargs.get("template_left_x_coefficient", 3)

    # The polynomial is given as: 39x^2 + 5x - 14 = (3x+a)(bx+c)
    # We need to find integer a, b, c such that this equality holds.
    
    # From the equation: 
    # LHS coefficients are [39, 5, -14] representing 39*x^2 + 5*x - 14
    
    # The expansion of (3x+a)(bx+c) is:
    # = 3b x^2 + (3c + ab)x + ac
    
    # Comparing coefficients with LHS [39, 5, -14]:
    # 1. 3*b = 39 => b = 13
    # 2. a*c = -14
    # 3. 3c + ab = 5
    
    # We know:
    # b = 13 (from step 1)
    
    # Substitute into equation 3:
    # 3c + a*13 = 5 => 3c + 13a = 5
    
    # Also from equation 2: ac = -14. Since a and c are integers, possible pairs (a,c):
    # (-1, 14), (1, -14), (2, -7), (-2, 7), (7, -2), (-7, 2)
    
    # Let's test each pair in the equation: 3c + 13a = 5
    
    possible_pairs = [(-1, 14), (1, -14), (2, -7), (-2, 7), (7, -2), (-7, 2)]
    
    for a_val, c_val in possible_pairs:
        if 3 * c_val + 13 * a_val == 5:
            # Found the correct pair
            break
    
    # Calculate a+2c as required by factor_order_policy=strict_source_template
    result = a_val + 2 * c_val
    
    return {
        "question_text": f"已知\n\\[\n39x^2+5x-14=(3x+a)(bx+c),\n其中 \\(a,b,c\\) 均為整數，求 \\(a+2c\\)。",
        "correct_answer": result,
        "oracle_payload": {
            "factor_order_policy": factor_order_policy,
            "quadratic_coefficients": quadratic_coefficients,
            "template_left_x_coefficient": template_left_x_coefficient
        }
    }
