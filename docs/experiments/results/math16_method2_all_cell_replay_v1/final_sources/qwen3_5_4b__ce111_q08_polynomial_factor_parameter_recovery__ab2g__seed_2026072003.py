def generate(level=1, **kwargs):
    factor_order_policy = "strict_source_template"
    quadratic_coefficients = [39, 5, -14]
    template_left_x_coefficient = 3
    
    a, b, c = quadratic_coefficients[0], quadratic_coefficients[1], quadratic_coefficients[2]
    
    correct_answer = a + 2 * c
    
    question_text = r"Given the polynomial $P(x) = (3x+a)(bx+c)$ where coefficients are integers derived from frozen parameters, find the value of $(a+2c)$."
    
    oracle_payload = {
        "factor_order_policy": factor_order_policy,
        "quadratic_coefficients": quadratic_coefficients,
        "template_left_x_coefficient": template_left_x_coefficient
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }