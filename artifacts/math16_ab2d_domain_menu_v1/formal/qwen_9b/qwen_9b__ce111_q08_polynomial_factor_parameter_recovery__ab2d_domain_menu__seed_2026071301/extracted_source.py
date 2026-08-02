from core.prompts.domain_function_library import PolynomialOps

def generate(level=1, **kwargs):
    frozen_params = {
        "factor_order_policy": "strict_source_template",
        "quadratic_coefficients": [39, 5, -14],
        "template_left_x_coefficient": 3
    }

    # The task requires solving for integer a and c given the factorization:
    # (3x + a)(bx + c) = 39x^2 + 5x - 14
    # Expanding LHS: 3b x^2 + (3c + ab)x + ac
    # Matching coefficients with RHS [39, 5, -14]:
    # 1. 3b = 39 => b = 13
    # 2. ac = -14
    # 3. 3c + a*b = 5 => 3c + 13a = 5
    
    # We need to find integer pairs (a, c) such that:
    # a * c = -14
    # 3*c + 13*a = 5
    
    # Possible factors of -14 for (a, c):
    # (-1, 14), (1, -14), (-2, 7), (2, -7), (-7, 2), (7, -2) ... etc.
    
    solutions = []
    target_ac = -14
    
    # Iterate through divisors of ac to find integer candidates for a and c
    import math
    abs_target = abs(target_ac)
    limit = int(math.sqrt(abs_target)) + 1
    
    possible_pairs = set()
    for i in range(-abs_target, abs_target + 1):
        if i == 0: continue
        if target_ac % i != 0: continue
        
        a_candidate = i
        c_candidate = target_ac // i
        # Check the linear equation constraint
        if (3 * c_candidate) + (a_candidate * 13) == 5:
            possible_pairs.add((a_candidate, c_candidate))

    # According to factor_order_policy="strict_source_template", 
    # "first factor fixed as (3x+a)". This implies we just need the valid solution.
    # The problem asks for a+2c. Since integer solutions are unique in this context usually:
    
    if possible_pairs:
        a, c = list(possible_pairs)[0]
        result_value = a + 2 * c
        
        return {
            "question_text": f"已知\\n[39x^2+5x-14=(3x+a)(bx+c),]\\n其中 \\(a,b,c\\) 均為整數，求 \\(a+2c\\)。",
            "correct_answer": result_value,
            "oracle_payload": frozen_params
        }

    # Fallback if no integer solution found (should not happen for this specific math problem)
    return {
        "question_text": f"已知\\n[39x^2+5x-14=(3x+a)(bx+c),]\\n其中 \\(a,b,c\\) 均為整數，求 \\(a+2c\\)。",
        "correct_answer": None, 
        "oracle_payload": frozen_params
    }