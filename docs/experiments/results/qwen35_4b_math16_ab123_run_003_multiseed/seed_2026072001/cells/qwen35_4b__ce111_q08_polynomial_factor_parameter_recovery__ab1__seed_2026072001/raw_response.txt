def generate(level=1, **kwargs):
    import re
    
    polynomials = {}
    
    factor_order_policy = "strict_source_template"
    quadratic_coefficients = [39, 5, -14]
    template_left_x_coefficient = 3
    
    frozen_parameters = {
        "factor_order_policy": factor_order_policy,
        "quadratic_coefficients": quadratic_coefficients,
        "template_left_x_coefficient": template_left_x_coefficient
    }
    
    a, b, c = [int(x) for x in quadratic_coefficients]
    
    question_text = r"\text{Given the polynomial } P(x) = 39x^2 + 5x - 14 \text{ which factors as } (3x+a)(bx+c), \text{ find the integer value of } a+2c."
    
    correct_answer = str(a + 2*c)
    
    oracle_payload = frozen_parameters
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }