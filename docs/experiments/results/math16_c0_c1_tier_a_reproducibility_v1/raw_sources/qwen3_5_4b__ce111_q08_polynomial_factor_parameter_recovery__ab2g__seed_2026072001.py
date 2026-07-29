def generate(level=1, **kwargs):
    frozen_params = {
        "factor_order_policy": "strict_source_template",
        "quadratic_coefficients": [39, 5, -14],
        "template_left_x_coefficient": 3
    }
    
    a, b, c = frozen_params["quadratic_coefficients"]
    template_left_x_coefficient = frozen_params["template_left_x_coefficient"]
    
    # Factor order policy: strict_source_template means first factor is fixed as (3x+a)
    # The quadratic coefficients [a, b, c] correspond to ax^2 + bx + c
    # We need to find the second factor such that their product matches the polynomial.
    # Let factors be (mx+n)(px+q). Given m=3 from template_left_x_coefficient.
    # Product = 3x * px + ... 
    # The constant term of the quadratic is c = -14. So n*q = -14.
    # The x coefficient of the product is b = 5. So (m*p + n) = m*p + q? No, standard expansion:
    # (3x+n)(px+q) = 3p*x^2 + (3q+n)*x + n*q
    # We have coefficients [a, b, c] -> a=39, b=5, c=-14.
    # So 3*p = 39 => p = 13.
    # n*q = -14.
    # 3q + n = 5.
    
    import math
    
    possible_n_values = []
    for i in range(1, abs(c)+1):
        if c % i == 0:
            possible_n_values.append(i)
            possible_n_values.append(-i)
            
    solutions = []
    for n in possible_n_values:
        q = c // n
        # Check linear coefficient condition: 3*q + n should equal b (5)
        if 3 * q + n == frozen_params["quadratic_coefficients"][1]:
            solutions.append((n, q))
    
    # There might be multiple factorizations. The problem asks for parameter recovery 'a' in the context of a specific template.
    # Usually these problems imply integer factors. Let's check our found solution.
    if len(solutions) == 1:
        n_sol, q_sol = solutions[0]
        
        # Factor order policy says first factor is fixed as (3x+a). 
        # In our expansion (3x+n)(px+q), the 'a' in the template corresponds to 'n'.
        # So a_template_value = n.
        a_val = n_sol
        
        # The correct_answer must be the integer a + 2c? Or is it related to the recovered parameter?
        # Specification says: "correct_answer must be the integer a+2c". 
        # Here 'a' likely refers to the constant term of the first factor found (n).
        # Let's calculate val = n_sol + 2 * c.
        
        correct_ans_val = a_val + 2 * frozen_params["quadratic_coefficients"][2]
    else:
        raise ValueError("No unique integer solution found for factors.")

    question_text = r"""Find the value of $a$ in the factorization $(3x+a)(13x+b) = 39x^2 + 5x - 14$. The correct answer is then computed as $a+2c$, where $c=-14$."""
    
    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": int(correct_ans_val),
        "oracle_payload": oracle_payload
    }