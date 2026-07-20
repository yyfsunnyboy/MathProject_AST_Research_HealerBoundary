def generate(level=1, **kwargs):
    import random
    
    # Frozen sampled parameters as per task specification
    factor_order_policy = "strict_source_template"
    quadratic_coefficients = [39, 5, -14]
    template_left_x_coefficient = 3
    
    a = random.randint(0, 26)
    
    if level == 1:
        b_quadratic = quadratic_coefficients[0] + (template_left_x_coefficient * quadratic_coefficients[1])
        
        question_text = r"\text{Let } P(x) \text{ be a polynomial with integer coefficients. We know that one factor of } P(x) \text{ is } (3x+a). \text{ If we divide the remaining part by } 2, \text{ we get an expression involving quadratic terms: } bx^2 + cx - d = 0."
        
        correct_answer = a + b_quadratic
        
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": {
            "factor_order_policy": factor_order_policy,
            "quadratic_coefficients": quadratic_coefficients,
            "template_left_x_coefficient": template_left_x_coefficient
        }
    }