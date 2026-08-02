from core.prompts.domain_function_library import PolynomialOps

def generate(level=1, **kwargs):
    # Extract frozen parameters from kwargs or defaults if not present in task block context
    # The oracle_payload must exactly match the provided frozen_params object.
    
    quadratic_coeffs = [39, 5, -14]
    template_left_x_coefficient = 3
    
    # We need to find integer a and b such that (3x+a)(bx+c) expands to 39x^2 + 5x - 14.
    # Expansion: 3b x^2 + (3c+ab)x + ac
    # Equations:
    # 1) 3*b = 39 => b = 13
    # 2) a*c = -14
    # 3) 3*c + a*13 = 5
    
    # From (1), b is determined as 13.
    # Substitute b=13 into (3): 3c + 13a = 5 => c = (5 - 13a)/3
    # Since c must be an integer, (5 - 13a) % 3 == 0.
    # Also a*c = -14. So ac is negative. One of a,c is positive, one negative.
    
    # Let's iterate possible factors of -14 for 'ac'. Pairs (a, c):
    # Factors of -14: (-1, 14), (1, -14), (-2, 7), (2, -7), (-7, 2), (7, -2), (-14, 1), (14, -1)
    
    possible_pairs = [(-1, 14), (1, -14), (-2, 7), (2, -7), (-7, 2), (7, -2), (-14, 1), (14, -1)]
    
    valid_solution = None
    
    for a_val, c_val in possible_pairs:
        # Check if this pair satisfies the middle term condition with b=13
        calculated_middle_term_coeff = template_left_x_coefficient * c_val + a_val * 13
        
        if calculated_middle_term_coeff == quadratic_coeffs[1]: # which is 5
            valid_solution = (a_val, c_val)
            break
            
    if valid_solution:
        a, c = valid_solution
        result_value = a + 2*c
    else:
        # Fallback or error handling not expected given problem constraints usually guarantee solution
        return {
            "question_text": r"已知\[39x^2+5x-14=(3x+a)(bx+c),\]其中 \(a,b,c\) 均為整數，求 \(a+2c\)。",
            "correct_answer": None, 
            "oracle_payload": {
                "factor_order_policy": "strict_source_template",
                "quadratic_coefficients": [39, 5, -14],
                "template_left_x_coefficient": 3
            }
        }

    return {
        "question_text": r"已知\[39x^2+5x-14=(3x+a)(bx+c),\]其中 \(a,b,c\) 均為整數，求 \(a+2c\)。",
        "correct_answer": result_value,
        "oracle_payload": {
            "factor_order_policy": "strict_source_template",
            "quadratic_coefficients": [39, 5, -14],
            "template_left_x_coefficient": 3
        }
    }