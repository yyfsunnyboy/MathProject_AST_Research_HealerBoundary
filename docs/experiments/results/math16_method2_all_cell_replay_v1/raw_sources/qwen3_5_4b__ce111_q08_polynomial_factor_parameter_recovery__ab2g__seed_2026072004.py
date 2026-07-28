def generate(level=1, **kwargs):
    frozen_params = {"factor_order_policy": "strict_source_template", "quadratic_coefficients": [39, 5, -14], "template_left_x_coefficient": 3}
    
    a = frozen_params["quadratic_coefficients"][0] // (frozen_params["template_left_x_coefficient"] ** 2) + 1
    
    question_text = r"\text{Given the polynomial } P(x) = ax^2 + bx + c \text{ where } a=39, b=5, c=-14. \text{ It is known that one factor is fixed as } (3x+a). \text{ Find the integer value of } a+2c."
    
    correct_answer = int(a) + 2 * (-14)
    
    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }